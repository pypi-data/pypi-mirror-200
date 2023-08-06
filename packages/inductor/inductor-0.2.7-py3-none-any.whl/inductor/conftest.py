# Copyright 2022 Inductor, Inc.

"""Globally accessible PyTest fixtures for tests."""

import contextlib
import time
from typing import ContextManager, Dict, Generator, Optional, Tuple, Union

import docker
import psycopg2
import pymysql
import pytest


@contextlib.contextmanager
def _start_docker_container(
    image: str,
    client: Optional[docker.DockerClient] = None,
    **kwargs,
) -> Generator[
    Tuple[docker.DockerClient, docker.models.containers.Container],
    None,
    None,
]:
    """Spins up a Docker container, yields the client and connection to it.

    This context manager spins up and yields a newly spun-up Docker container,
    and then kills the container when the context is exited.

    Example:
        with _start_docker_container(
            image="mysql",
            environment={ "MYSQL_ROOT_PASSWORD": "password" },
            ports={ "3306/tcp": 1110 },
            command="echo \"Hello, world!\""
        )
        as (client, container):

    Args:
        image: The name of the Docker Hub image which the new container should
            be started with.
        client: A specified Docker client with which to spin up the
            container.
        **kwargs: Any other parameters which should be passed to the docker-py
            run method.

    Yields:
        A tuple containing the Docker client and container.
    """
    if client is None:
        client = docker.from_env()
    container = client.containers.run(image, detach=True, **kwargs)
    yield (client, container)
    container.reload()
    if container.status == "running":
        container.kill()


@contextlib.contextmanager
def _make_pymysql_conn(
    *,
    environment: Optional[Dict[str, Union[str, int]]] = None,
    ports: Optional[Dict[Union[str, int], Union[str, int]]] = None,
    connection_args: Optional[Dict[str, Union[str, int]]] = None,
    image_tag: Optional[str] = None,
    **kwargs,
) -> Generator[pymysql.Connection, None, None]:
    """See make_pymysql_conn fixture."""
    default_db_name = "testdb"
    default_env = {
        "MYSQL_ALLOW_EMPTY_PASSWORD": "true",
        "MYSQL_DATABASE": default_db_name,
    }
    default_ports = { "3306/tcp": 0 }
    image_name = ("mysql:latest"
        if image_tag is None
        else f"mysql:{image_tag}")
    if environment is not None:
        if (
            "MYSQL_ROOT_PASSWORD" not in environment
            and "MYSQL_ALLOW_EMPTY_PASSWORD" not in environment
        ):
            raise ValueError(
                "Provided environment must include MYSQL_ROOT_PASSWORD "
                "or MYSQL_ALLOW_EMPTY_PASSWORD."
            )
    create_args = {
        "image": image_name,
        "environment": default_env if environment is None else environment,
        "ports": default_ports if ports is None else ports,
        **kwargs,
    }
    with _start_docker_container(**create_args) as (_, container):
        container.reload()
        host_connections = container.ports["3306/tcp"]
        if len(host_connections) < 1:
            raise RuntimeError("The Docker container was unable to start.")
        host_ip = host_connections[0]["HostIp"]
        host_port = host_connections[0]["HostPort"]
        default_connection_args = {
            "host": host_ip,
            "port": int(host_port),
            "user": "root",
            "database": default_db_name,
        }
        combined_args = (default_connection_args
            if connection_args is None
            else { **default_connection_args, **connection_args })
        attempts = 0
        is_connected = False
        while not is_connected:
            try:
                if attempts > 10:
                    raise RuntimeError("Unable to connect to the container.")
                time.sleep(1)
                connection = pymysql.connect(**combined_args)
                is_connected = True
            except pymysql.err.OperationalError:
                attempts += 1
        yield connection
        connection.close()


@contextlib.contextmanager
def _make_psycopg2_conn(
    *,
    environment: Optional[Dict[str, Union[str, int]]] = None,
    ports: Optional[Dict[Union[str, int], Union[str, int]]] = None,
    connection_args: Optional[Dict[str, Union[str, int]]] = None,
    image_tag: Optional[str] = None,
    **kwargs,
) -> Generator[psycopg2._psycopg.connection, None, None]:
    """See make_psycopg2_conn fixture."""
    default_db_name = "testdb"
    default_pw = "testpw"
    default_env = {
        "POSTGRES_DB": default_db_name,
        "POSTGRES_PASSWORD": default_pw,
    }
    default_ports = { "5432/tcp": 0 }
    image_name = ("postgres:latest"
        if image_tag is None
        else f"postgres:{image_tag}")
    if environment is not None:
        if "POSTGRES_PASSWORD" not in environment:
            raise ValueError(
                "Provided environment must include POSTGRES_PASSWORD"
            )
    create_args = {
        "image": image_name,
        "environment": default_env if environment is None else environment,
        "ports": default_ports if ports is None else ports,
        **kwargs,
    }
    with _start_docker_container(**create_args) as (_, container):
        container.reload()
        host_connections = container.ports["5432/tcp"]
        if len(host_connections) < 1:
            raise RuntimeError("The Docker container was unable to start.")
        host_ip = host_connections[0]["HostIp"]
        host_port = host_connections[0]["HostPort"]
        default_connection_args = {
            "host": host_ip,
            "port": int(host_port),
            "user": "postgres",
            "password": default_pw,
            "database": default_db_name,
        }
        combined_args = (default_connection_args
            if connection_args is None
            else { **default_connection_args, **connection_args })
        attempts = 0
        is_connected = False
        while not is_connected:
            try:
                if attempts > 10:
                    raise RuntimeError("Unable to connect to the container.")
                time.sleep(1)
                connection = psycopg2.connect(**combined_args)
                is_connected = True
            except psycopg2.Error:
                attempts += 1
        yield connection
        connection.close()


@pytest.fixture(scope="session")
def make_pymysql_conn() -> ContextManager[pymysql.Connection]:
    """Returns a context manager that yields a PyMySQL connection.

    This fixture returns a context manager which, provided some or
    none of the listed named arguments, yields a PyMySQL connection to a
    Docker-hosted MySQL database. When the context is exited, the connection
    is closed and the Docker container is killed.

    Args (of the returned context manager):
        environment: An optional key-value dictionary of environment variables
            to be loaded into the MySQL Docker container. The default value
            is a dictionary containing the `MYSQL_ALLOW_EMPTY_PASSWORD`
            variable, which configures the MySQL connection to not require a
            password for the root user. A provided environment must include
            either `MYSQL_ROOT_PASSWORD` (with the desired root password as
            the value) or else `MYSQL_ALLOW_EMPTY_PASSWORD`.
            See https://hub.docker.com/_/mysql for documentation of the
            environment variables supported by the MySQL Docker container.
        ports: An optional key-value dictionary of port mappings to be applied
            to the MySQL Docker container. The keys represent internal Docker
            ports and the values represent the external ports to which the
            Docker ports should be forwarded. Defaults to mapping port 3306
            on the Docker instance to the next available port on the host.
        connection_args: An optional key-value dictionary of supplemental
            pymysql connection arguments to be passed into the
            `pymysql.connect` call.
        image_tag: An optional Docker tag for the specific version of
            the `mysql` image that should be started. Defaults to
            "latest".
        **kwargs: Any additional arguments to be passed through to the
            _start_docker_container function.

    Yields (from the returned context manager):
        A PyMySQL connection to a MySQL database running on a dedicated
        Docker container.
    """
    return _make_pymysql_conn


@pytest.fixture(scope="session")
def make_psycopg2_conn() -> ContextManager[psycopg2._psycopg.connection]:
    """Returns a context manager that yields a Psycopg2 connection.

    This fixture returns a context manager which, provided some or
    none of the listed named arguments, yields a Psycopg2 connection to a
    Docker-hosted Postgres database. When the context is exited, the connection
    is closed and the Docker container is killed.

    Args (of the returned context manager):
        environment: An optional key-value dictionary of environment variables
            to be loaded into the Postgres Docker container. A provided
            environment must include `POSTGRES_PASSWORD` (with the desired root
            password as the value).
            See https://hub.docker.com/_/postgres for documentation of the
            environment variables supported by the Postgres Docker container.
        ports: An optional key-value dictionary of port mappings to be applied
            to the Postgres Docker container. The keys represent internal Docker
            ports and the values represent the external ports to which the
            Docker ports should be forwarded. Defaults to mapping port 5432
            on the Docker instance to the next available port on the host.
        connection_args: An optional key-value dictionary of supplemental
            psycopg2 connection arguments to be passed into the
            `psycopg2.connect` call.
        image_tag: An optional Docker tag for the specific version of
            the `postgres` image that should be started. Defaults to
            "latest".
        **kwargs: Any additional arguments to be passed through to the
            _start_docker_container function.

    Yields (from the returned context manager):
        A Psycopg2 connection to a Postgres database running on a dedicated
        Docker container.
    """
    return _make_psycopg2_conn
