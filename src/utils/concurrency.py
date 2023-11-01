import asyncio
from concurrent.futures import ThreadPoolExecutor

thread_pool_executor = ThreadPoolExecutor(max_workers=8)


def execute_asyncio_task(async_task):
    local_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(local_loop)
    try:
        local_loop.run_until_complete(async_task)
    except Exception as error:
        print(f"An error occurred while running the task: {error}")
    finally:
        local_loop.close()

    try:
        task_exception = async_task.exception()
        if task_exception:
            raise task_exception
        else:
            print("no exception found")
    except asyncio.CancelledError:
        pass


def go(target_function, *arguments, **keyword_arguments):
    thread_pool_executor.submit(
        execute_asyncio_task, target_function(*arguments, **keyword_arguments)
    )


def go_and_wait(target_function, *arguments, **keyword_arguments):
    future = thread_pool_executor.submit(
        execute_asyncio_task, target_function(*arguments, **keyword_arguments)
    )
    return future.result()
