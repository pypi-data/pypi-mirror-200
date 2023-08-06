# Copyright 2022 Inductor, Inc.

"""Functionality for Inductor function execution in a local environment."""

import concurrent.futures
from typing import Any, Dict, List

from inductor.compute import common


class LocalFuture(common.Future):
    """The result of a local asynchronous call to an Inductor app function."""

    def __init__(self, concurrent_future: concurrent.futures.Future):
        """Constructs a new LocalFuture instance.

        Args:
            concurrent_future: The concurrent.futures.Future for the function
                call underlying this LocalFuture.
        """
        self._concurrent_future = concurrent_future

    def wait(self) -> Any:
        """See base class."""
        return self._concurrent_future.result()


def execute_qualname_async(
    module_qualname: str, fn_qualname: str,
    args: List[Any], kwargs: Dict[str, Any]) -> LocalFuture:
    """Asynchronously executes function given by module_qualname, fn_qualname.

    Args:
        module_qualname: Fully qualified name of module containing the function
            to be executed.
        fn_qualname: Qualified name, within module given by module_qualname,
            of function to be executed.
        args: Positional arguments to be passed to function.  Must be picklable.
        kwargs: Keyword arguments to be passed to function.  Must be picklable.

    Returns:
        A LocalFuture representing the result of asynchronously calling the
        specified function.
    """
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=1)
    local_future = LocalFuture(executor.submit(
        common.execute_qualname, module_qualname, fn_qualname, args, kwargs))
    executor.shutdown(wait=False)
    return local_future
