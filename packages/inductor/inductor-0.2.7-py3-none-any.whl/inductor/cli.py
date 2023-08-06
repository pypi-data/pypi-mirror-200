# Copyright 2022 Inductor, Inc.

"""The Inductor CLI."""

import importlib
import multiprocessing
import os
import signal
import sys

import typer
import watchgod

import inductor

app = typer.Typer()


@app.callback()
def app_callback():
    """The Inductor CLI."""


class _InductorAppWatcher(watchgod.DefaultDirWatcher):
    """Watchgod watcher for files that define an Inductor App."""

    # Directory names to be ignored
    _ignored_dirnames = {
        ".devcontainer", ".vscode", ".git", "__pycache__", "node_modules"}

    def should_watch_dir(self, entry: os.DirEntry) -> bool:
        """See base class."""
        return (
            entry.name not in _InductorAppWatcher._ignored_dirnames and
            not entry.name.startswith("."))

    def should_watch_file(self, entry: os.DirEntry) -> bool:
        """See base class."""
        return (
            entry.name.endswith(".py") and
            not entry.name.startswith("."))


def _may_import_inductor_app(path: str, app_fullname: str) -> bool:
    """Returns True iff Python file at path may explicitly import app_fullname.

    Args:
        path: Path to Python file to test for potential import.
        app_fullname: Location of Inductor App for which to test for potential
            import, in the format "{module}:{object}".
    """
    app_module_qualname, _ = app_fullname.split(":")
    app_module_name = app_module_qualname.split(".")[-1]
    may_import = False
    with open(path) as f:
        for line in f.readlines():
            if "import " in line and app_module_name in line:
                may_import = True
                break
    return may_import


def _load_app(app_fullname: str) -> inductor.App:
    """Loads and returns Inductor App object given by app_fullname.

    Specifically, imports the Inductor App object given by app_fullname, as
    well as all Python modules in the current working directory or in packages
    in the current working directory's subtree that may explicitly import the
    Inductor App's module to ensure that all App-decorated functions are
    registered with the App object.

    Args:
        app_fullname: Location of Inductor App to load, in the format
            "{module}:{object}".

    Returns:
        The loaded Inductor App object.
    """
    app_module_qualname, app_object_qualname = app_fullname.split(":")
    # Add current working directory to sys.path
    orig_sys_path = list(sys.path)
    sys.path[0] = os.getcwd()
    # Obtain Inductor App object
    inductor_app = importlib.import_module(app_module_qualname)
    for name in app_object_qualname.split("."):
        inductor_app = getattr(inductor_app, name)
    # Import Python modules that may import app_fullname
    cwd = os.getcwd()
    in_cwd = True
    for dirpath, dirnames, filenames in os.walk(cwd):
        cur_dirname = os.path.dirname(dirpath)
        if ((in_cwd or "__init__.py" in filenames) and
            cur_dirname not in _InductorAppWatcher._ignored_dirnames and  # pylint: disable=protected-access
            not cur_dirname.startswith(".")):
            for filename in filenames:
                if (filename.endswith(".py") and
                    not filename.startswith(".") and
                    _may_import_inductor_app(
                        os.path.join(dirpath, filename), app_fullname)):
                    module_qualname, _ = os.path.splitext(filename)
                    package_path = os.path.relpath(dirpath, start=cwd)
                    if package_path != ".":
                        while package_path:
                            package_path, tail = os.path.split(package_path)
                            assert tail
                            module_qualname = tail + "." + module_qualname
                    if module_qualname.endswith(".__init__"):
                        module_qualname = module_qualname[
                            :-len(".__init__")]
                    importlib.import_module(module_qualname)
        else:
            del dirnames[:]
        in_cwd = False
    # Restore sys.path
    sys.path = orig_sys_path
    # Return the App object
    return inductor_app


def _app_up(app_fullname: str):
    """Loads and calls up() on the Inductor App given by app_fullname.

    Args:
        app_fullname: Location of Inductor App on which to call up(), in the
            format "{module}:{object}".
    """
    # Add current working directory to sys.path
    orig_sys_path = list(sys.path)
    sys.path[0] = os.getcwd()
    # Up the Inductor app
    _load_app(app_fullname).up()
    # Restore sys.path
    sys.path = orig_sys_path


@app.command()
def up(
    app_fullname: str = typer.Argument(..., metavar="APP", help=(
        "The Inductor app to start or update, "
        "in the format \"{module}:{object}\".  "
        "{object} defaults to \"app\" if not provided.")),
    reload: bool = typer.Option(False, help=(
        "Automatically reload the app whenever its code changes?  Ignored if "
        "not using a Local environment."))):
    """Start an Inductor app, or update an already running app."""
    if ":" not in app_fullname:
        app_fullname += ":app"
    if not reload:
        _app_up(app_fullname)
    else:
        app_module_qualname, _ = app_fullname.split(":")
        app_module_realpath = os.path.realpath(os.path.join(
            os.getcwd(), *app_module_qualname.split(".")) + ".py")
        process = multiprocessing.Process(target=_app_up, args=[app_fullname])
        process.start()
        for changes in watchgod.watch(
            os.getcwd(), watcher_cls=_InductorAppWatcher):
            reload_now = False
            for change_type, path in changes:
                if (change_type == watchgod.Change.deleted or
                    os.path.realpath(path) == app_module_realpath or
                    _may_import_inductor_app(path, app_fullname)):
                    reload_now = True
                    break
            if reload_now:
                if process.is_alive():
                    os.kill(process.pid, signal.SIGINT)
                    process.join(2)
                    if process.is_alive():
                        process.kill()
                        process.join(2)
                    assert not process.is_alive()
                process = multiprocessing.Process(
                    target=_app_up, args=[app_fullname])
                process.start()


if __name__ == "__main__":
    app()
