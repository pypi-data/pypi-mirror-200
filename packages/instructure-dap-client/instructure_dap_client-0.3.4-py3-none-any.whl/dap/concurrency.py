import asyncio
from asyncio import Task
from typing import Any, Awaitable, Iterable, List, Set, Tuple, TypeVar, overload

T = TypeVar("T")
T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")


def _make_task(aw: Awaitable[T]) -> Task:
    "Wraps an awaitable into a task, and schedules its execution."

    return asyncio.create_task(aw)  # type: ignore


async def wait_n(awaitables: Iterable[Awaitable[None]], *, concurrency: int) -> None:
    """
    Waits for all awaitables to complete, scheduling at most a fixed number of tasks concurrently.

    :param awaitables: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    iterator = iter(awaitables)
    pending = set(
        _make_task(awaitable) for _, awaitable in zip(range(concurrency), iterator)
    )
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            if task.cancelled():
                raise asyncio.CancelledError
            exc = task.exception()
            if exc:
                raise exc

        for _, awaitable in zip(range(len(done)), iterator):
            pending.add(_make_task(awaitable))


def _task_result(task: Task) -> Any:
    "Unwraps the result or exception from a task."

    exc = task.exception()
    if exc:
        return exc
    else:
        return task.result()


async def _gather_n(
    awaitables: Iterable[Awaitable[T]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Iterable[T]:
    """
    Runs awaitable objects, with at most the specified degree of concurrency.

    :param awaitables: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :param return_exceptions: If true, exceptions are treated the same as successful results;
        if false, the first raised exception is immediately propagated.
    :returns: Results returned by coroutines, in the order corresponding to the input sequence.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    iterator = iter(awaitables)

    tasks: List[Task] = []
    pending: Set[Task] = set()
    for _, awaitable in zip(range(concurrency), iterator):
        task = _make_task(awaitable)
        tasks.append(task)
        pending.add(task)
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            if task.cancelled():
                raise asyncio.CancelledError
            exc = task.exception()
            if exc and not return_exceptions:
                raise exc

        for _, awaitable in zip(range(len(done)), iterator):
            task = _make_task(awaitable)
            tasks.append(task)
            pending.add(task)

    return (_task_result(task) for task in tasks)


@overload
async def gather_n(
    awaitables: List[Awaitable[T]], *, concurrency: int, return_exceptions: bool = False
) -> List[T]:
    ...


@overload
async def gather_n(
    awaitables: Tuple[Awaitable[T1], Awaitable[T2]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2]:
    ...


@overload
async def gather_n(
    awaitables: Tuple[Awaitable[T1], Awaitable[T2], Awaitable[T3]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2, T3]:
    ...


@overload
async def gather_n(
    awaitables: Tuple[Awaitable[T1], Awaitable[T2], Awaitable[T3], Awaitable[T4]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Tuple[T1, T2, T3, T4]:
    ...


async def gather_n(
    awaitables: Iterable[Awaitable[T]],
    *,
    concurrency: int,
    return_exceptions: bool = False
) -> Iterable[T]:
    """
    Runs awaitable objects, with at most the specified degree of concurrency.

    :param awaitables: The coroutines to schedule and whose completion to wait for.
    :param concurrency: The maximum number of tasks that can execute concurrently.
    :param return_exceptions: If true, exceptions are treated the same as successful results;
        if false, the first raised exception is immediately propagated.
    :returns: Results returned by coroutines, in the order corresponding to the input sequence.
    :raises asyncio.CancelledError: Raised when one of the tasks in cancelled.
    """

    results = await _gather_n(
        awaitables, concurrency=concurrency, return_exceptions=return_exceptions
    )

    if isinstance(awaitables, list):
        return list(results)
    elif isinstance(awaitables, tuple):
        return tuple(results)
    else:
        return results
