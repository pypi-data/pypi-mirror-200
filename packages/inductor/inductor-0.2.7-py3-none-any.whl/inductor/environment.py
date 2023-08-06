# Copyright 2022 Inductor, Inc.

"""Definitions of environments in which Inductor apps can run."""

class Env:
    """Parent for classes representing Inductor app environments."""


class Local(Env):
    """Environment representing a local workstation."""

    def __init__(
        self,
        base_dir: str,
        *,
        http_host: str = "127.0.0.1",
        http_port: int = 8000):
        """Constructs a new Local instance.

        Args:
            base_dir: Directory on the local filesystem to be used by Inductor
                for storage.  Will be created if does not already exist.
            http_host: Host to which Inductor's web server should bind.
            http_port: Port to which Inductor's web server should bind.
        """
        self.base_dir = base_dir
        self.http_host = http_host
        self.http_port = http_port


class Server(Env):
    """Environment representing a server (e.g., container/VM) in the cloud."""

    def __init__(
        self,
        app_name: str,
        database_url: str,
        object_store_url: str,
        *,
        http_host: str = "0.0.0.0",
        http_port: int = 80):
        """Constructs a new instance.

        Args:
            app_name: Name for app in this environment.  Should uniquely
                identify app among all apps run using Server environment
                with the same database_url.
            database_url: URL identifying database to be used for storage of
                app metadata and Inductor-created tables.  This database should
                be persistent independently of (and accessible from) the compute
                node or container used to run the app.  The URL should have
                format
                    system://username:password@host:port/database
                where system is either mysql or postgresql.  The database role
                identified by username should have the ability to create and
                write to (as well as read) tables in the specified database.
            object_store_url: URL identifying object storage location to be
                used for storage of app metadata and data.  This storage
                location should be persisent independently of (and accessible
                from) the server (e.g., compute node or container) used to run
                the app.  The URL should have the following format:
                - If using a filesystem mounted into node/container (e.g., via
                  Amazon Elastic File System):
                    file://path/to/use/
                - If using AWS S3:
                    s3://bucket/prefix/
                  where prefix is optional.
            http_host: Host to which Inductor's web server should bind.
            http_port: Port to which Inductor's web server should bind.
        """
        self.app_name = app_name
        self.database_url = database_url
        self.object_store_url = object_store_url
        self.http_host = http_host
        self.http_port = http_port


class InductorCloud(Local):
    """Environment representing Inductor's cloud deployment service."""

    def __init__(
        self,
        app_name: str):
        """Constructs a new InductorCloud instance.
        
        Args:
            app_name: Name for app in this environment.  Should uniquely
                identify app among all apps run using InductorCloud
                environment within a given deployment account.
        """
        super().__init__(
            base_dir="/home/app_data",
            http_host="0.0.0.0",
            http_port=80)
        self.app_name = app_name
