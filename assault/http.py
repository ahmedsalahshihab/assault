import asyncio
import time
import os
import requests

# Make the request and return the results
def fetch(url):
    print("\nI am in the fetch function")
    started_at = time.monotonic()
    response = requests.get(url)
    request_time = time.monotonic() - started_at
    print("Are you here?")
    print(str(response.status_code) + str(request_time))
    return {"status_code": response.status_code, "request_time": request_time}


# A function to take unmade requests from a queue, perform the work, and add result to the queue
async def worker(name, queue, results):
    print("I entered the function")
    loop = asyncio.get_event_loop()
    while True:
        url = await queue.get()
        if True:
            print(f"{name} - Fetching {url}")
        print("I am in the while loop")
        future_result = loop.run_in_executor(None, fetch, url)
        print(str(type(future_result)))
        result = await future_result
        print("I am in the while loop and after the future_result")
        results.append(result)
        queue.task_done()


# Divide up work into batches and collect final results
async def distribute_work(url, requests, concurrency, results):
#By adding the async keyword, distribute_work function becomes a coroutine. A coroutine can only be run by:
#It's executed by asyncio.run.
#OR
#It's "waited on" in another coroutine using the await keyword.

    queue = asyncio.Queue()			#Creates a FIFO queue
    for _ in range(requests):
        queue.put_nowait(url)		#Function put_nowait: put an item into the queue without blocking.

    print(str(queue.qsize()))
    # Create workers to match the concurrency
    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(worker(f"worker-{i+1}", queue, results))		#Tasks allows you to run coroutines concurrently.
        tasks.append(task)

    started_at = time.monotonic()
    await queue.join()		#When you call queue.join() in the main thread, all it does is block the main threads until the workers have processed everything that's in the queue. It does not stop the worker threads, which continue executing their infinite loops.
    total_time = time.monotonic() - started_at
    for task in tasks:
        task.cancel()

    print("---")
    print(f"{concurrency} workers took {total_time:.2f} seconds to complete {len(results)} requests")


# Entrypoint to making requests
def assault(url, requests, concurrency):
    results = []
    asyncio.run(distribute_work(url, requests, concurrency, results))	#To call async function, you need to use asyncio.run()
    print(results)

url = input("URL: ")
requests = input("Requests: ")
concurrency = input("Concurrency: ")

assault(url, int(requests), int(concurrency))