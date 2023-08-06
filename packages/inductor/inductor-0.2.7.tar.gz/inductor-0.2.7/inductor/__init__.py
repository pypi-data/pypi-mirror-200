# Copyright 2022 Inductor, Inc.

"""The entrypoint for creating Inductor apps."""

from dataclasses import dataclass
import functools
import inspect
import json
import os
import threading
import traceback
from typing import Any, Callable, Coroutine, Dict, Iterable, List, Optional, Tuple, Union
from urllib import parse

from apscheduler.schedulers import asyncio as apscheduler_asyncio
from apscheduler.triggers import cron as apscheduler_cron
import fastapi
from fastapi import routing, staticfiles
import typing_extensions
from typing_extensions import Literal
import uvicorn

from inductor import compute
from inductor import environment
from inductor import ui
from inductor import util
from inductor.compute import local
from inductor.data.table import sqlite
from inductor.data.table import table_catalog
from inductor.data.table import table_util
from inductor.ml import model_store


# Alias providing users of this module with access to inductor.environment
# without the need to explicitly import that module.
env = environment


# HTTP URL path prefix for HTTP URLs of Inductor-internal endpoints.
# Should not end with /.
_INTERNAL_HTTP_URL_PATH_PREFIX = "/inductor_internal"


# Type for values representing HTTP methods.
HttpMethod = Literal["get", "post", "put", "delete"]


# Type for values representing accelerator hardware types.
# "A100", "V100", and "K80" are NVIDIA GPU types.
AcceleratorType = Literal["A100", "V100", "K80"]


@dataclass
class _InductorFunction:
    """Metadata for a function fn registered with Inductor.

    All fields beyond fn have the same semantics as the correspondingly
    named parameters of App.__call__().
    """
    fn: Callable
    http_url_path: Optional[str] = None
    http_method: HttpMethod = "get"
    schedule: Optional[str] = None
    schedule_timezone: str = "UTC"
    cpus: Optional[int] = None
    accelerators: Optional[Tuple[int, AcceleratorType]] = None
    memory: Optional[float] = None

    def __post_init__(self):
        """Validates this instance's fields' values.

        Raises:
            ValueError if one or more of this instance's fields do not contain
            valid values.
        """
        if self.http_method not in typing_extensions.get_args(HttpMethod):
            raise ValueError(f"Unsupported http_method ({self.http_method}).")

    def fastapi_wrapper(self) -> Callable:
        """Returns wrapped version of f for use as a FastAPI endpoint."""
        fn = self.fn
        http_method = self.http_method
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            ret_val = fn(*args, **kwargs)
            # pylint: disable-next=protected-access
            if isinstance(ret_val, ui._ContainerStack):
                if http_method != "get":
                    raise ValueError(
                        "Inductor's ui package requires that HTTP "
                        "endpoints returning UI pages "
                        "use http_method == \"get\" "
                        f"(rather than \"{http_method}\").")
                return fastapi.responses.HTMLResponse(
                    ui.html_scaffold(), status_code=200)
            else:
                return ret_val
        return wrapper

    def fastapi_wrapper_ui_internal(
        self,
        app_env: environment.Env,
    ) -> Coroutine:
        """Returns wrapped version of f for use as a UI-specific HTTP endpoint.

        (Specifically, for use as an Inductor-internal UI-specific FastAPI
        endpoint.)

        Args:
            app_env: The environment in which this function is being called.
        """
        # Wrap f
        fn = self.fn
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            # Extract request from kwargs, parse request body as JSON, and
            # set ui.element_values
            request = kwargs["inductor_wrapper_ui_internal_request"]
            element_values = await request.json()
            ui.element_values.set(element_values)
            # Remove request from kwargs so that kwargs conforms to fn's
            # expectations
            kwargs = kwargs.copy()
            del kwargs["inductor_wrapper_ui_internal_request"]
            # Call fn, process its return value, and return
            ret_val = None
            try:
                ret_val = fn(*args, **kwargs)
            # If fn raises an exception, return a UI page containing the
            # exception's traceback
            except Exception: # pylint: disable=broad-except
                page = ui.Page("Exception")
                if isinstance(app_env, environment.Local):
                    page.heading("A Python exception was raised:")
                    page.code(traceback.format_exc(), lang="python")
                else:
                    page.print("An error has occurred.")
                traceback.print_exc()
                return page.to_element().to_json_dict()
            # pylint: disable-next=protected-access
            if isinstance(ret_val, ui._ContainerStack):
                return ret_val.to_element().to_json_dict()
            else:
                raise ValueError(
                    f"Function ({fn.__qualname__}) unexpectedly "
                    "did not return a UI container.")
        # Adjust wrapper's signature to include request as a parameter
        orig_signature = inspect.signature(fn)
        orig_params = [
            orig_param for _, orig_param in orig_signature.parameters.items()]
        new_params = []
        for orig_param in orig_params:
            if orig_param.kind != inspect.Parameter.VAR_KEYWORD:
                new_params.append(orig_param)
            else:
                break
        new_params.append(inspect.Parameter(
            "inductor_wrapper_ui_internal_request",
            inspect.Parameter.KEYWORD_ONLY,
            annotation=fastapi.Request))
        new_params.extend(orig_params[(len(new_params) - 1):])
        wrapper.__signature__ = inspect.Signature(new_params)
        # Return
        return wrapper


class App:
    """Class whose instances represent Inductor apps."""

    def __init__(
        self,
        env: Union[environment.Env, Dict[str, environment.Env]],  # pylint: disable=redefined-outer-name
    ):
        """Constructs a new App instance.

        Args:
            env: The environment in which this app should run, or a map from
                names to environments in which this app can run.  If the
                latter, then the environment variable INDUCTOR_ENV must be
                set to the name of the environment in which to run.
        """
        # Boolean value indicating whether or not we are currently executing
        # in an app's run-time context (rather than creation- or update-time
        # context)
        self._run_time = (
            "INDUCTOR_RUN_TIME" in os.environ and
            os.environ["INDUCTOR_RUN_TIME"] == "1")
        self._functions: List[_InductorFunction] = []

        if isinstance(env, environment.Env):
            self._env = env
        else:
            self._env = env[os.environ["INDUCTOR_ENV"]]

        self._app_id = None

        if isinstance(self._env, environment.Local):
            # Base directory for all table-related storage
            self._table_dir = os.path.join(self._env.base_dir, "table")
            # Path for sqlite db storing Inductor-internal table catalog
            self._internal_table_catalog_path = os.path.join(
                self._table_dir, "internal_table_catalog.db")
            # URL for sqlite db storing Inductor-internal tables (with
            # the exception of the unique ID state table)
            self._internal_table_db_url = "sqlite://" + os.path.join(
                self._table_dir, "internal.db")
            # Path for sqlite table storing unique ID state
            self._unique_id_state_table_path = os.path.join(
                self._table_dir, "unique_id_state.db")
            # Path for sqlite db storing app table catalog
            self._app_table_catalog_path = os.path.join(
                self._table_dir, "app_table_catalog.db")
            # URL for sqlite db storing app-created tables
            self._app_table_db_url = "sqlite://" + os.path.join(
                self._table_dir, "app.db")
            # Base directory for ML model storage
            self._model_storage_dir = os.path.join(
                self._env.base_dir, "ml", "models")

    def _get_secrets(self) -> Dict[str, Any]:
        """Get secrets from file.

        Returns:
            Secrets from file as a dictionary.
        """
        secrets_path = "./secrets.json"
        alt_secrets_path = "~/.inductor/secrets.json"
        if not os.path.exists(secrets_path):
            if os.path.exists(alt_secrets_path):
                secrets_path = alt_secrets_path
            else:
                return {}
        with open(secrets_path) as f:
            return json.load(f)

    @property
    def secrets(self) -> Dict[str, Any]:
        """Returns this app's custom secrets."""
        return self._get_secrets().get("custom", {})

    def up(self):
        """Starts or updates (if already running) this app."""
        if self._run_time:
            raise RuntimeError(
                "Cannot execute up() in an app's run-time context.")
        if isinstance(self._env, environment.Local):
            # Create self._env.base_dir as necessary
            if (os.path.exists(self._env.base_dir) and
                not os.path.isdir(self._env.base_dir)):
                raise ValueError(
                    f"base_dir ({self._env.base_dir}) already exists but is "
                    "not a directory.")
            os.makedirs(self._env.base_dir, exist_ok=True)
            # Create base directory for all table-related storage
            os.makedirs(self._table_dir, exist_ok=True)
            # Initialize table storing state for unique id generation
            unique_id_state_table = sqlite.SqliteKeyedTable(
                self._unique_id_state_table_path,
                table_name="unique_id_state",
                primary_key_column="universe_id",)
            unique_id_state_table.set(0, {"value": 0}, skip_if_exists=True)
        elif isinstance(self._env, environment.Server):
            # Create global apps table and add row for this app, as needed
            apps_table = table_util.table_from_url(
                database_url=self._env.database_url,
                table_name="inductor_apps",
                primary_key_column="app_name",
                indexed_columns=["app_id"])
            repeated_id = True
            while repeated_id:
                app_id = str(len(apps_table))
                added = apps_table.set(
                    self._env.app_name,
                    {"app_id": app_id},
                    skip_if_exists=True)
                if not added:
                    repeated_id = False
                else:
                    count = apps_table.select(
                        "COUNT(*)", "WHERE app_id = {app_id}").value()
                    if count != 1:
                        del apps_table[self._env.app_name]
            # Retrieve app ID
            self._app_id = apps_table[self._env.app_name]["app_id"]
            # Initialize table storing state for unique id generation
            unique_id_state_table = table_util.table_from_url(
                database_url=self._env.database_url,
                table_name=f"inductor_app_{self._app_id}_uid",
                primary_key_column="universe_id")
            unique_id_state_table.set(0, {"value": 0}, skip_if_exists=True)
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")
        if isinstance(self._env, (environment.Local, environment.Server)):
            # Add internal table for storage of ML model metadata
            self._internal_tables.create_keyed_table(
                "ml_model_metadata", "model_name")
            # Create tables as necessary
            self._run_time = True
            self._internal_tables._up()  # pylint: disable=protected-access
            self._run_time = True
            self.tables._up()  # pylint: disable=protected-access
            self._run_time = False
            # Create FastAPI app and add functions having an http_url_path
            self._fastapi_app = fastapi.FastAPI()
            self._fastapi_app.mount(
                f"{_INTERNAL_HTTP_URL_PATH_PREFIX}/frontend",
                staticfiles.StaticFiles(
                    directory=ui.frontend_assets_dir_path()),
                name=f"{_INTERNAL_HTTP_URL_PATH_PREFIX}/frontend")
            for f in self._functions:
                if f.http_url_path:
                    module_qualname = util.module_qualname(f.fn)
                    # Add HTTP endpoint.
                    getattr(self._fastapi_app, f.http_method)(
                        f.http_url_path,
                        response_model=None,
                        tags=[module_qualname])(f.fastapi_wrapper())
                    # Add UI HTTP endpoint for Inductor-internal use.
                    if not f.http_url_path.startswith("/"):
                        raise ValueError(
                            f"http_url_path ({f.http_url_path}) must "
                            "start with a slash.")
                    self._fastapi_app.post(
                        f"{_INTERNAL_HTTP_URL_PATH_PREFIX}/ui" +
                        f.http_url_path)(
                            f.fastapi_wrapper_ui_internal(self._env))
            # Create scheduler, add functions having schedules, and add the
            # scheduler to fastapi_app's startup sequence
            scheduler = apscheduler_asyncio.AsyncIOScheduler()
            for f in self._functions:
                if f.schedule and f.schedule != "@up":
                    if f.schedule == "@yearly":
                        cron_string = "0 0 1 1 *"
                    elif f.schedule == "@monthly":
                        cron_string = "0 0 1 * *"
                    elif f.schedule == "@weekly":
                        cron_string = "0 0 * * 0"
                    elif f.schedule == "@daily":
                        cron_string = "0 0 * * *"
                    elif f.schedule == "@hourly":
                        cron_string = "0 * * * *"
                    elif f.schedule == "@minutely":
                        cron_string = "* * * * *"
                    else:
                        cron_string = f.schedule
                    scheduler.add_job(
                        f.fn.exec_async,
                        trigger=apscheduler_cron.CronTrigger.from_crontab(
                            cron_string, timezone=f.schedule_timezone))
            @self._fastapi_app.on_event("startup")
            async def start_scheduler():
                scheduler.start()
            # Enter app's run-time context
            self._run_time = True
            # Execute any functions having schedule == "@up"
            for f in self._functions:
                if f.schedule == "@up":
                    f.fn()
            # Start FastAPI app (this call is blocking)
            uvicorn.run(
                self._fastapi_app,
                host=self._env.http_host,
                port=self._env.http_port,
                reload=False,
                access_log=False)
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")

    # Lock used to ensure that _unique_id_gen() below is thread-safe
    _unique_id_gen_lock = threading.Lock()

    @property
    def _unique_id_gen(self) -> util.UniqueIdGen:
        """Returns this App instance's UniqueIdGen."""
        with App._unique_id_gen_lock:
            if hasattr(self, "_unique_id_gen_instance"):
                # pylint: disable-next=access-member-before-definition
                return self._unique_id_gen_instance
            if isinstance(self._env, environment.Local):
                unique_id_state_table = sqlite.SqliteKeyedTable(
                    self._unique_id_state_table_path,
                    "unique_id_state",
                    "universe_id")
            elif isinstance(self._env, environment.Server):
                assert self._app_id is not None
                unique_id_state_table = table_util.table_from_url(
                    database_url=self._env.database_url,
                    table_name=f"inductor_app_{self._app_id}_uid",
                    primary_key_column="universe_id")
            else:
                raise TypeError(f"Unsupported env type ({type(self._env)})")
            prefix_value = unique_id_state_table.increment(0, "value", 1)
            self._unique_id_gen_instance = util.UniqueIdGen(
                str(prefix_value))
            return self._unique_id_gen_instance

    def unique_id(self, count: int = 1) -> Union[str, Iterable[str]]:
        """Returns strings that are unique across all calls within this app.

        In particular, every string returned by this method is guaranteed to
        never before have been returned by this method within this app.

        Args:
            count: Number of unique strings to return.

        Returns:
            A single unique string if count == 1; otherwise, an iterable of
            unique strings.  All returned strings contain only characters in
            {a-z, A-Z, 0-9, _}.
        """
        return self._unique_id_gen.unique_id(count)

    @property
    def _internal_tables(self) -> table_catalog.TableCatalog:
        """Returns the TableCatalog for Inductor-internal tables."""
        if isinstance(self._env, environment.Local):
            database_url = self._internal_table_db_url
        elif isinstance(self._env, environment.Server):
            database_url = self._env.database_url
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")
        if not self._run_time:
            if hasattr(self, "_internal_tables_instance_pre_run"):
                # pylint: disable-next=access-member-before-definition, protected-access
                self._internal_tables_instance_pre_run._run_time = (
                    self._run_time)
            else:
                self._internal_tables_instance_pre_run = (
                    table_catalog.TableCatalog(
                        None,
                        None,
                        self._env,
                        self._run_time,
                        database_url,
                        self.unique_id))
            return self._internal_tables_instance_pre_run
        if isinstance(self._env, environment.Local):
            internal_tables_instance = table_catalog.TableCatalog(
                sqlite.SqliteKeyedTable(
                    self._internal_table_catalog_path,
                    "catalog_internal_metadata",
                    primary_key_column="id"),
                sqlite.SqliteKeyedTable(
                    self._internal_table_catalog_path,
                    "catalog_internal_name_to_id",
                    primary_key_column="name"),
                self._env,
                self._run_time,
                database_url,
                self.unique_id,
                physical_table_name_prefix="table_")
        elif isinstance(self._env, environment.Server):
            internal_tables_instance = table_catalog.TableCatalog(
                table_util.table_from_url(
                    database_url=self._env.database_url,
                    table_name=(f"inductor_app_{self._app_id}_"
                                "catalog_internal_metadata"),
                    primary_key_column="id"),
                table_util.table_from_url(
                    database_url=self._env.database_url,
                    table_name=(f"inductor_app_{self._app_id}_"
                                "catalog_internal_name_to_id"),
                    primary_key_column="name"),
                self._env,
                self._run_time,
                database_url,
                self.unique_id,
                physical_table_name_prefix=(f"inductor_app_{self._app_id}_"
                                            "internal"))
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")
        if hasattr(self, "_internal_tables_instance_pre_run"):
            internal_tables_instance._table_creation_instructions = (  # pylint: disable=protected-access
                self._internal_tables_instance_pre_run._table_creation_instructions)  # pylint: disable=line-too-long,protected-access
        return internal_tables_instance

    @property
    def tables(self) -> table_catalog.TableCatalog:
        """Returns this app's TableCatalog."""
        if isinstance(self._env, environment.Local):
            database_url = self._app_table_db_url
        elif isinstance(self._env, environment.Server):
            database_url = self._env.database_url
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")
        if not self._run_time:
            if hasattr(self, "_tables_instance_pre_run"):
                # pylint: disable-next=access-member-before-definition, protected-access
                self._tables_instance_pre_run._run_time = self._run_time
            else:
                self._tables_instance_pre_run = table_catalog.TableCatalog(
                    None,
                    None,
                    self._env,
                    self._run_time,
                    database_url,
                    self.unique_id,
                    self._get_secrets().get("tables"))
            return self._tables_instance_pre_run
        if isinstance(self._env, environment.Local):
            tables_instance = table_catalog.TableCatalog(
                sqlite.SqliteKeyedTable(
                    self._app_table_catalog_path,
                    "catalog_app_metadata",
                    primary_key_column="id"),
                sqlite.SqliteKeyedTable(
                    self._app_table_catalog_path,
                    "catalog_app_name_to_id",
                    primary_key_column="name"),
                self._env,
                self._run_time,
                database_url,
                self.unique_id,
                self._get_secrets().get("tables"),
                physical_table_name_prefix="table_")
        elif isinstance(self._env, environment.Server):
            tables_instance = table_catalog.TableCatalog(
                table_util.table_from_url(
                    database_url=self._env.database_url,
                    table_name=(f"inductor_app_{self._app_id}_"
                                "catalog_app_metadata"),
                    primary_key_column="id"),
                table_util.table_from_url(
                    database_url=self._env.database_url,
                    table_name=(f"inductor_app_{self._app_id}_"
                                "catalog_app_name_to_id"),
                    primary_key_column="name"),
                self._env,
                self._run_time,
                database_url,
                self.unique_id,
                self._get_secrets().get("tables"),
                physical_table_name_prefix=f"inductor_app_{self._app_id}_app")
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")
        if hasattr(self, "_tables_instance_pre_run"):
            tables_instance._table_creation_instructions = (  # pylint: disable=protected-access
                self._tables_instance_pre_run._table_creation_instructions)  # pylint: disable=protected-access
        return tables_instance

    @property
    def models(self) -> model_store.ModelStore:
        """Returns this app's ModelStore."""
        if isinstance(self._env, environment.Local):
            return model_store.LocalModelStore(
                self._model_storage_dir,
                self._internal_tables["ml_model_metadata"],
                self._unique_id_gen)
        elif isinstance(self._env, environment.Server):
            if self._env.object_store_url.startswith("file://"):
                return model_store.LocalModelStore(
                    os.path.join(
                        self._env.object_store_url[len("file://"):],
                        "ml",
                        "models"),
                    self._internal_tables["ml_model_metadata"],
                    self._unique_id_gen)
            elif self._env.object_store_url.startswith("s3://"):
                s3_url = self._env.object_store_url
                if not s3_url.endswith("/"):
                    s3_url += "/"
                return model_store.S3ModelStore(
                    s3_url + "ml/models/",
                    self._internal_tables["ml_model_metadata"],
                    self._unique_id_gen)
            else:
                raise RuntimeError(
                    "Unrecognized environment object_store_url prefix: " +
                    self._env.object_store_url)
        else:
            raise TypeError(f"Unsupported env type ({type(self._env)})")

    def __call__(
        self,
        # Triggering via HTTP
        http_url_path: Optional[str] = None,
        http_method: HttpMethod = "get",
        *,  # all subsequent parameters are keyword-only
        # Triggering on a schedule
        schedule: Optional[str] = None,
        schedule_timezone: str = "UTC") -> Callable[[Callable], Callable]:
        """Registers a function with this App when called as a decorator.

        In particular, returns a function that registers its argument with this
        App as specified by the arguments to this method.  Enables registering
        functions for Inductor-enabled triggering and execution.

        Args:
            http_url_path: If non-None, then the decorated function will be
                exposed as an HTTP endpoint at the given http_url_path, via
                the HTTP method given by http_method.  Must not begin with
                _INTERNAL_HTTP_URL_PATH_PREFIX.
            http_method: The HTTP method via which this function will be exposed
                if http_url_path is non-None.
            schedule: Optional schedule on which to execute the decorated
                function.  Can be one of the values "@yearly", "@monthly",
                "@weekly", "@daily", "@hourly", "@minutely", or "@up" (i.e.,
                execute the decorated function immediately after every app
                startup or update), or a string in standard
                [cron syntax](https://en.wikipedia.org/wiki/Cron). If a schedule
                is provided, then the decorated function must be callable
                without arguments, and all scheduled calls will be made without
                providing any explicit arguments to it.
            schedule_timezone: The timezone based upon which executions should
                be scheduled if schedule is non-None.  Must be an
                [IANA timezone name](
                https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
        """
        # Enable App instances to be used as decorators without parentheses;
        # if an App instance is used in this way, then the decorated function
        # is directly passed in to this method within http_url_path, and this
        # method in turn must return the resulting decorator-processed
        # function, rather than a decorator.
        if isinstance(http_url_path, Callable):
            return self.__call__()(http_url_path)
        # Validate arguments
        if http_url_path and http_url_path.startswith(
            _INTERNAL_HTTP_URL_PATH_PREFIX):
            raise ValueError(
                f"http_url_path ({http_url_path}) must not "
                f"start with {_INTERNAL_HTTP_URL_PATH_PREFIX}.")
        # Create decorator function
        def decorator(fn: Callable) -> Callable:
            module_qualname = util.module_qualname(fn)
            # Add exec_async field to fn
            if isinstance(self._env, (environment.Local, environment.Server)):
                @functools.wraps(fn)
                def exec_async_wrapper(*args, **kwargs) -> compute.Future:
                    return local.execute_qualname_async(
                        module_qualname, fn.__qualname__ + "._fn_async",
                        args, kwargs)
                exec_async_wrapper.__name__ += ".exec_async"
                exec_async_wrapper.__qualname__ += ".exec_async"
                exec_async_wrapper.__annotations__["return"] = compute.Future
                fn.exec_async = exec_async_wrapper
            else:
                raise TypeError(f"Unsupported env type ({type(self._env)})")
            # Add version of fn to be executed by exec_async as fn._fn_async
            @functools.wraps(fn)
            def fn_async_wrapper(*args, **kwargs):
                return fn(*args, **kwargs)
            fn._fn_async = fn_async_wrapper  # pylint: disable=protected-access
            # Add fn.url_path() if http_url_path is present
            if http_url_path is not None:
                def fn_url_path_wrapper(*args, **kwargs):
                    fn_name = fn.__name__
                    fn_args = dict(
                        inspect.signature(fn).bind_partial(*args,
                                                           **kwargs).arguments)
                    module_qualname = util.module_qualname(fn)
                    route = next(route for route in self._fastapi_app.routes
                                 if route.name == fn_name and
                                 module_qualname in route.tags)
                    if not isinstance(route, routing.APIRoute):
                        raise TypeError(
                            f"{fn_name} route is not instance of APIRoute")
                    path_params = {}
                    query_params = {}
                    for param in route.dependant.path_params:
                        value = fn_args.get(param.name)
                        if value is None:
                            raise ValueError(
                                f"missing a required argument: '{param.name}'")
                        path_params[param.name] = value
                    for param in route.dependant.query_params:
                        value = fn_args.get(param.name)
                        if value is not None:
                            query_params[param.name] = value
                    url = route.url_path_for(fn_name, **path_params)
                    parsed = list(parse.urlparse(url))
                    parsed[4] = parse.urlencode(query_params)
                    return parse.urlunparse(parsed)
                fn.url_path = fn_url_path_wrapper
            # Register fn with this app
            self._functions.append(_InductorFunction(
                fn=fn,
                http_url_path=http_url_path,
                http_method=http_method,
                schedule=schedule,
                schedule_timezone=schedule_timezone,
                cpus=None,
                accelerators=None,
                memory=None))
            # Return fn
            return fn
        # Return decorator function
        return decorator

    def set_navbar(
        self,
        logo: ui.TextLike,
        left: Optional[List[ui.TextLike]] = None,
        center: Optional[List[ui.TextLike]] = None,
        right: Optional[List[ui.TextLike]] = None):
        """Instructs this App to add a navbar to all Pages returned by Page().

        Args:
            logo: Content (e.g., text or link) to display in the most prominent
                leftmost position in the navbar.
            left: Content (e.g., text or links) to display immediately after
                the logo.
            center: Content (e.g., text or links) to display in the horizontal
                center of the navbar.
            right: Content (e.g., text or links) to display on the righthand
                side of the navbar.
        """
        self._navbar_args = {
            "logo": logo, "left": left, "center": center, "right": right}

    def Page(  # pylint: disable=invalid-name
        self,
        title: str,
        *,
        vertical_align: Literal["top", "center"] = "top") -> ui.Page:
        """Returns a new web page container.

        See ui.Page for more information on how to use the returned object.

        Args:
            title: The page title to be displayed in the browser.
            vertical_align: The vertical alignment for content added to the
                page body.
        """
        p = ui.Page(title, vertical_align=vertical_align)
        if hasattr(self, "_navbar_args"):
            p.navbar(**self._navbar_args)
        return p
