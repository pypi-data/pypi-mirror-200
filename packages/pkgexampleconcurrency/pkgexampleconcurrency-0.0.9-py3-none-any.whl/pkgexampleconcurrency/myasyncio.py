import asyncio
import aiosqlite
import aiohttp


class MyAsyncio:
    def __init__(self):
        pass

    def helloio(self):
        # 1
        async def hello_world1():
            print("Hello World 1!")
            await asyncio.sleep(1)

        async def hello_world2():
            print("Hello World 2!")
            await asyncio.sleep(1)

        async def main():
            await hello_world1()
            # Do more stuff
            await hello_world2()
            # Do even more stuff
            # Return results if any.

        asyncio.run(main())
        print(
            """
        # 1
        async def hello_world1():
            print("Hello World 1!")
            await asyncio.sleep(1)

        async def hello_world2():
            print("Hello World 2!")
            await asyncio.sleep(1)

        async def main():
            await hello_world1()
            # Do more stuff
            await hello_world2()
            # Do even more stuff
            # Return results if any.

        asyncio.run(main())
        
async is placed before a method/function definition to flag that is should be
treated as an asyncronous funcion.

await is placed before a called function and is used to flag that the order of 
code execution must wait for that async function to complete.

To run your async code, you must call your main function using asyncio.

asyncio.run(main())

asyncio steps in and, as long as you have appropriatly designed and flagged your 
methods/functions asyncio does all the hard work of scheduling your tasks for you.

Simple? eh?

You can define as many async main methods in your code as you like and can also 
call them sequentially in a chain.

asyncio.run(main1())
asyncio.run(main2())

You'd do this in situations for example where main2() relies on main1()
processing some data completely.
        
        """
        )

    def gather_example(self):
        # 2
        async def hello_world1():
            print("Hello World 1!")
            await asyncio.sleep(1)
            return True

        async def hello_world2():
            print("Hello World 2!")
            await asyncio.sleep(1)
            return True

        async def main():
            results = await asyncio.gather(hello_world1(), hello_world2())
            for result in results:
                print(result)

        asyncio.run(main())
        print(
            """
        
        async def hello_world1():
            print("Hello World 1!")
            await asyncio.sleep(1)
            return True

        async def hello_world2():
            print("Hello World 2!")
            await asyncio.sleep(1)
            return True

        async def main():
            results = await asyncio.gather(hello_world1(), hello_world2())
            for result in results:
                print(result)

        asyncio.run(main())

What if your methods/functions don't depend on eachother?
You can gather them all up and run them all asyncronously
using asyncio.gather()

A futures object 'results' is returned, which you don't have to return results to, or
even asign to. I only include this here to show you can return results and loop
through them. You may design tasks that don't return any results.

        """
        )
        pass

    def yeild_and_generators(self):
        # 3
        print(
            """A magical thing happens when you use the word 'yeild' in an async function/method,
it turns your function in to what is called a generator.
"""
        )

        async def my_generator():
            for i in range(5):
                yield i

        async def my_consumer():
            async for item in my_generator():
                print(f"generator ex1: {item}")

        asyncio.run(my_consumer())
        print(
            """ 
        async def my_generator():
            for i in range(10):
                await asyncio.sleep(1)
                yield i

        async def my_consumer():
            async for item in my_generator():
                print(f"generator ex1: {item}")

        asyncio.run(my_consumer()) 
        """
        )

        print(
            """ 
A generator function saves state. When the yield keyword is encountered inside 
a generator function, it suspends the execution of the generator and "yields" 
a value to the function that called it. The generator function state is saved
(this means ALL local variables), so when the generator is resumed later, it 
can continue executing from where it left off. This allows the generator to 
produce a series of values over time, without having to compute them all at once.

The following is also a valid generator.
        """
        )

        # Another valid example of a generator.
        async def my_generator2():
            yield 1
            yield 2
            yield 3
            yield 4
            yield 5

        async def my_consumer2():
            async for item in my_generator2():
                print(f"generator ex2: {item}")

        asyncio.run(my_consumer2())

        print(
            """

        #Another valid example of a generator.
        
        def my_generator2():
            yield 1
            yield 2
            yield 3
            yield 4
            yield 5

        async def my_consumer2():
            async for item in my_generator2():
                print(f"generator ex2: {item}")

        asyncio.run(my_consumer2())
        """
        )
        print(
            """
Think of functions as all or nothing executions, and generators as piecemeal executions
that pause each time it hits yield.

Note, that there is no way to reset a generator, other than creating a new instance of it."""
        )
        pass

    def sleep_example(self):
        # 4
        async def my_generator():
            for i in range(5):
                await asyncio.sleep(1)
                yield i

        async def my_consumer():
            async for item in my_generator():
                print(f"generator ex1: {item}")

        asyncio.run(my_consumer())
        print(
            """ 
        async def my_generator():
            for i in range(5):
                await asyncio.sleep(1)
                yield i

        async def my_consumer():
            async for item in my_generator():
                print(f"generator ex1: {item}")

        asyncio.run(my_consumer())

If you use time.sleep() your python interpreter will block all execution, 
including your asyncio code. 
        
If you need an async function to sleep at a point you should use await asyncio.sleep()
        """
        )
        pass

    def to_thread_example(self):
        # 5
        def blocking_function():
            # This function does some heavy work that would otherwise block the event loop
            result = 0
            for i in range(1000000):
                result += i
            return result

        async def async_function():
            # This async function calls the blocking function using asyncio.to_thread()
            print("Async function starting...")
            result = await asyncio.to_thread(blocking_function)
            print(f"Async function finished with result {result}.")

        async def main():
            # This async function calls the async function
            print("Main function starting...")
            await async_function()
            print("Main function finished.")

        asyncio.run(main())
        print(
            """ 
        def blocking_function():
            # This function does some heavy work that would otherwise block the event loop
            result = 0
            for i in range(1000000):
                result += i
            return result

        async def async_function():
            # This async function calls the blocking function using asyncio.to_thread()
            print("Async function starting...")
            result = await asyncio.to_thread(blocking_function)
            print(f"Async function finished with result {result}.")

        async def main():
            # This async function calls the async function
            print("Main function starting...")
            await async_function()
            print("Main function finished.")

        asyncio.run(main())

The to_thread() function in asyncio allows you to run a blocking function in a separate thread, 
while allowing the event loop to continue running in the main thread. 

This is useful when you need to perform some blocking I/O or CPU-bound operation that would otherwise 
block the event loop and prevent other coroutines from running.

Calls to a blocking function by using to_thread() don't necessarily run sequentially or in any particular order.
        """
        )
        pass

    def create_task_example(self):
        # 6
        async def coroutine_func(delay, task_name):
            print(f"{task_name} started")
            await asyncio.sleep(delay)
            print(f"{task_name} finished")

        async def main():
            task1 = asyncio.create_task(coroutine_func(1, "Task 1"))
            task2 = asyncio.create_task(coroutine_func(2, "Task 2"))
            task3 = asyncio.create_task(coroutine_func(3, "Task 3"))

            await task1
            await task2
            await task3

        asyncio.run(main())

        print(
            """ 
        async def coroutine_func(delay, task_name):
            print(f"{task_name} started")
            await asyncio.sleep(delay)
            print(f"{task_name} finished")

        async def main():
            task1 = asyncio.create_task(coroutine_func(1, "Task 1"))
            task2 = asyncio.create_task(coroutine_func(2, "Task 2"))
            task3 = asyncio.create_task(coroutine_func(3, "Task 3"))

            await task1
            await task2
            await task3
        """
        )
        print(
            """
When asyncio.create_task() is called, it schedules the coroutine to 
run in the event loop as soon as possible, but does not wait for it 
to complete. This means that all three tasks are started concurrently, 
and their execution overlaps in time.

We use await to wait for each task to complete in the order in which 
they were created.

You can use create_task to create a list of tasks before passing them in 
to gather,
        """
        )

        async def task1():
            print("Task 1 started")
            await asyncio.sleep(1)
            print("Task 1 finished")
            return "Task 1 result"

        async def task2():
            print("Task 2 started")
            await asyncio.sleep(2)
            print("Task 2 finished")
            return "Task 2 result"

        async def main():
            tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]
            results = await asyncio.gather(*tasks)
            print("Results:")
            for result in results:
                print(result)

        asyncio.run(main())
        print(
            """ 
        async def task1():
            print("Task 1 started")
            await asyncio.sleep(1)
            print("Task 1 finished")
            return "Task 1 result"

        async def task2():
            print("Task 2 started")
            await asyncio.sleep(2)
            print("Task 2 finished")
            return "Task 2 result"

        async def main():
            tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]
            results = await asyncio.gather(*tasks)
            print("Results:")
            for result in results:
                print(result)

        asyncio.run(main())
        """
        )
        pass

    def wait_examples(self):
        # 7

        async def task():
            await asyncio.sleep(2)
            return 1

        async def main():
            try:
                result = await asyncio.wait_for(task(), timeout=1)
            except asyncio.TimeoutError:
                print("Timed out!")
            else:
                print(result)

        asyncio.run(main())

        print(
            """ 
        async def task():
            await asyncio.sleep(2)
            return 1

        async def main():
            try:
                result = await asyncio.wait_for(task(), timeout=1)
            except asyncio.TimeoutError:
                print("Timed out!")
            else:
                print(result)

        asyncio.run(main())
        """
        )

        print(
            """
asyncio.wait() and asyncio.wait_for() are similar in that they both wait for a group of coroutines to complete, but they have different behaviors and use cases.

asyncio.wait() takes an iterable of coroutines and returns two sets of tasks: the completed tasks and the tasks that are still running. It doesn't have a timeout parameter, so it will wait indefinitely for all the tasks to complete.

asyncio.wait_for() takes a single coroutine and a timeout value and waits for the coroutine to complete within the specified timeout. If the coroutine doesn't complete within the timeout, it raises the asyncio.TimeoutError exception. wait_for() is useful when you want to set a timeout for a specific coroutine, and you don't want to wait indefinitely.

In summary, asyncio.wait() is used to wait for a group of coroutines to complete, while asyncio.wait_for() is used to wait for a single coroutine to complete within a specified timeout.
        """
        )

        async def task1():
            await asyncio.sleep(1)
            return 1

        async def task2():
            await asyncio.sleep(2)
            return 2

        async def main():
            f1 = asyncio.create_task(task1())
            f2 = asyncio.create_task(task2())

            done, pending = await asyncio.wait({f1, f2})
            for f in done:
                print(f.result())

        asyncio.run(main())
        print(
            """ 
        async def task1():
            await asyncio.sleep(1)
            return 1

        async def task2():
            await asyncio.sleep(2)
            return 2

        async def main():
            f1 = asyncio.create_task(task1())
            f2 = asyncio.create_task(task2())

            done, pending = await asyncio.wait({f1, f2})
            for f in done:
                print(f.result())

        asyncio.run(main())
        """
        )
        print(
            """ 
You may have noticed a similarity to gather().
asyncio.gather() is more suitable if you want to run a group of coroutines concurrently 
and retrieve their results as a list, whereas asyncio.wait() is more suitable if you want 
to run a group of coroutines concurrently and check when they have completed without 
retrieving their results.
        """
        )
        pass

    def as_complete_example(self):
        # 8
        print(
            """as_complete() is the "as_gather()" for the impatient. 
        """
        )

        async def task1():
            await asyncio.sleep(2)
            print("Task 1 is done")
            return True

        async def task2():
            await asyncio.sleep(1)
            print("Task 2 is done")
            return True

        async def do_all_the_tasks():
            task_list = [task1(), task2()]
            for completed_task in asyncio.as_completed(task_list):
                results = await completed_task
                print(results)
                print(f"Task completed: {results}")

        asyncio.run(do_all_the_tasks())

        print(
            """         
        async def task1():
            await asyncio.sleep(2)
            print("Task 1 is done")
            return True

        async def task2():
            await asyncio.sleep(1)
            print("Task 2 is done")
            return True

        async def do_all_the_tasks():
            task_list = [task1(), task2()]
            for completed_task in asyncio.as_completed(task_list):
                results = await completed_task
                print(f"Task completed: {results}")

        asyncio.run(do_all_the_tasks())
        """
        )

        print(
            """
as_completed() creates an iterator that yeilds futures as the tasks are completed, 
the for loop awaits for each of the futures created by each of the tasks to complete. """
        )

    # syncronization primatives

    def lock_example(self):
        # 9
        async def worker(lock, data):
            async with lock:
                # Access the shared resource
                data.append(1)
                await asyncio.sleep(1)
                data.append(2)
                await asyncio.sleep(1)
                data.append(3)

        async def main():
            lock = asyncio.Lock()
            data = []
            tasks = [asyncio.create_task(worker(lock, data)) for i in range(3)]
            await asyncio.gather(*tasks)
            print(data)

        asyncio.run(main())

        print(
            """ 
        async def worker(lock, data):
            async with lock:
                # Access the shared resource
                data.append(1)
                await asyncio.sleep(1)
                data.append(2)
                await asyncio.sleep(1)
                data.append(3)

        async def main():
            lock = asyncio.Lock()
            data = []
            tasks = [asyncio.create_task(worker(lock, data)) for i in range(3)]
            await asyncio.gather(*tasks)
            print(data)

        asyncio.run(main())
        """
        )

        print(
            """
The code given demonstrates the use of an asyncio.Lock() to synchronize access to a 
shared resource. The worker() function takes a Lock object and a list as arguments 
and appends the values 1, 2, and 3 to the list, with a 1 second pause between each append. 

The main() function creates a Lock object and an empty list, and creates a list of tasks 
using asyncio.create_task() that call the worker() function with the same Lock object and 
list. 

Finally, the main() function waits for all the tasks to complete using asyncio.gather() and 
prints the list to the console. The output demonstrates that each value is appended atomically 
and that no two coroutines append values to the list at the same time.
        """
        )
        pass

    def event_example(self):
        # 10
        async def worker(event, data):
            # Wait for the event to be set
            await event.wait()
            # Access the shared resource
            data.append(1)
            await asyncio.sleep(1)
            data.append(2)
            await asyncio.sleep(1)
            data.append(3)

        async def main():
            event = asyncio.Event()
            data = []
            tasks = [asyncio.create_task(worker(event, data)) for i in range(3)]
            await asyncio.sleep(3)  # Wait for 3 seconds
            event.set()  # Signal the event
            await asyncio.gather(*tasks)
            print(data)

        asyncio.run(main())
        print(
            """ 
        async def worker(event, data):
            # Wait for the event to be set
            await event.wait()
            # Access the shared resource
            data.append(1)
            await asyncio.sleep(1)
            data.append(2)
            await asyncio.sleep(1)
            data.append(3)

        async def main():
            event = asyncio.Event()
            data = []
            tasks = [asyncio.create_task(worker(event, data)) for i in range(3)]
            await asyncio.sleep(3)  # Wait for 3 seconds
            event.set()  # Signal the event
            await asyncio.gather(*tasks)
            print(data)

        asyncio.run(main())"""
        )

        print(
            """ 
An asyncio Event is an object in Python's asyncio library that allows multiple coroutines 
to synchronize their execution based on a common condition. The Event object has a boolean 
state, which can be set or cleared by any coroutine, and coroutines can wait for the state 
to change using the wait() method. When the state of the Event object is set, all waiting 
coroutines are woken up and allowed to proceed with their execution. This makes the Event 
object a useful tool for coordinating the execution of multiple coroutines that need to wait 
for a common condition to be met before proceeding.
        """
        )
        pass

    def conditions_examples(self):
        # 11

        async def consumer(condition, data):
            async with condition:
                while True:
                    if len(data) == 0:
                        # Wait for the producer to add data
                        await condition.wait()
                        # Check again after being woken up
                        continue
                    # Access the shared data
                    item = data.pop(0)
                    print(f"Consumer got {item}")
                    # Notify the producer that the data has been consumed
                    condition.notify()
                    # Exit the loop when there are no more items
                    if len(data) == 0:
                        break

        async def producer(condition, data):
            for i in range(5):
                # Produce some data
                item = i + 1
                print(f"Producer put {item}")
                async with condition:
                    # Add the data to the shared variable
                    data.append(item)
                    # Notify the consumer that new data is available
                    condition.notify()
                await asyncio.sleep(1)

        async def main():
            condition = asyncio.Condition()
            data = []
            consumer_task = asyncio.create_task(consumer(condition, data))
            producer_task = asyncio.create_task(producer(condition, data))
            await asyncio.gather(consumer_task, producer_task)

        asyncio.run(main())

        print(
            """ 
        async def consumer(condition, data):
            async with condition:
                while True:
                    if len(data) == 0:
                        # Wait for the producer to add data
                        await condition.wait()
                        # Check again after being woken up
                        continue
                    # Access the shared data
                    item = data.pop(0)
                    print(f"Consumer got {item}")
                    # Notify the producer that the data has been consumed
                    condition.notify()
                    # Exit the loop when there are no more items
                    if len(data) == 0:
                        break

        async def producer(condition, data):
            for i in range(5):
                # Produce some data
                item = i + 1
                print(f"Producer put {item}")
                async with condition:
                    # Add the data to the shared variable
                    data.append(item)
                    # Notify the consumer that new data is available
                    condition.notify()
                await asyncio.sleep(1)

        async def main():
            condition = asyncio.Condition()
            data = []
            consumer_task = asyncio.create_task(consumer(condition, data))
            producer_task = asyncio.create_task(producer(condition, data))
            await asyncio.gather(consumer_task, producer_task)

        asyncio.run(main())
        """
        )

        print(
            """
In a way, you could say that an asyncio.Condition is a lock that is triggered by a condition.

An asyncio.Condition consists of an asyncio.Lock and a wait queue. When a coroutine wants to 
access the shared resource protected by the condition, it first acquires the lock using the 
async with condition construct. If the lock is already held by another coroutine, the current 
coroutine is blocked until the lock is released.

However, unlike a simple lock, an asyncio.Condition also allows coroutines to wait for a particular 
condition to be satisfied before accessing the shared resource. When a coroutine waits on a condition 
using await condition.wait(), it is added to the wait queue associated with the condition. When another 
coroutine signals the condition using condition.notify() or condition.notify_all(), one or all of the 
waiting coroutines are awakened and allowed to acquire the lock and access the shared resource.

So, in summary, an asyncio.Condition is a combination of a lock and a condition variable, where the 
condition variable allows coroutines to wait for a particular condition to be satisfied before accessing 
the shared resource protected by the lock.
"""
        )

        pass

    def semaphore_example(self):
        # 12
        async def worker(semaphore):
            async with semaphore:
                # Do some work that requires access to the shared resource
                print("Worker started")
                await asyncio.sleep(1)
                print("Worker finished")

        async def main():
            # Create a semaphore with a limit of 3 concurrent tasks
            semaphore = asyncio.Semaphore(3)
            tasks = []
            # Create 5 tasks to access the shared resource
            for i in range(5):
                tasks.append(asyncio.create_task(worker(semaphore)))
            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

        asyncio.run(main())
        print(
            """ 
        async def worker(semaphore):
            async with semaphore:
                # Do some work that requires access to the shared resource
                print("Worker started")
                await asyncio.sleep(1)
                print("Worker finished")

        async def main():
            # Create a semaphore with a limit of 3 concurrent tasks
            semaphore = asyncio.Semaphore(3)
            tasks = []
            # Create 5 tasks to access the shared resource
            for i in range(5):
                tasks.append(asyncio.create_task(worker(semaphore)))
            # Wait for all tasks to complete
            await asyncio.gather(*tasks)

        asyncio.run(main())"""
        )
        print(
            """ 
In the main() coroutine, we create a semaphore with a limit of 3 concurrent tasks, and create 5 tasks to access the shared resource. 
When a task is created using asyncio.create_task(worker(semaphore)), it attempts to acquire the semaphore. If there are already 3 tasks 
running, the remaining tasks will be blocked until a running task releases the semaphore.

By using a semaphore, we can limit the number of concurrent tasks that can access the shared resource and prevent overload or contention.
        """
        )
        pass

    def queue_example(self):
        # 13
        # print("Press ctrl-c to stop this example")

        async def producer(queue):
            for i in range(10):
                await queue.put(i)
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(queue):
            while True:
                item = await queue.get()
                if item is None:
                    # print("Detected end of queue")
                    # End of jobs
                    queue.task_done()
                    break
                print(item)
                queue.task_done()

        async def main():
            queue = asyncio.Queue()
            producer_task = asyncio.create_task(producer(queue))
            consumer_task = asyncio.create_task(consumer(queue))
            await asyncio.gather(producer_task)
            await queue.join()
            consumer_task.cancel()

        asyncio.run(main())

        print(
            """ 
        async def producer(queue):
            for i in range(10):
                await queue.put(i)
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(queue):
            while True:
                item = await queue.get()
                if item is None:
                    # print("Detected end of queue")
                    # End of jobs
                    queue.task_done()
                    break
                print(item)
                queue.task_done()

        async def main():
            queue = asyncio.Queue()
            producer_task = asyncio.create_task(producer(queue))
            consumer_task = asyncio.create_task(consumer(queue))
            await asyncio.gather(producer_task)
            await queue.join()
            consumer_task.cancel()

        asyncio.run(main())
        """
        )

        print(
            """
asyncio.Queue is an asyncio primitive that provides a thread-safe way to exchange data 
between coroutines. It is designed to be used in asynchronous programming contexts and 
automatically handles synchronization internally. As a result, you don't need to use 
additional synchronization primitives like locks or conditions when using an asyncio.Queue.

The asyncio.Queue primitive automatically handles synchronization between the producer() and consumer() 
coroutines, so we don't need to use any additional synchronization primitives.

But you may need to use synchronization primitives like locks or conditions when implementing the logic 
around the asyncio.Queue. For example, if you have multiple producers and consumers accessing the queue 
concurrently, you may need to use a lock to ensure that only one producer or consumer accesses the queue at a time.
        """
        )
        pass

    def queuel_example(self):
        # 14
        # print("Press ctrl-c to stop this example")

        async def producer(queue, lock):
            for i in range(10):
                async with lock:
                    await queue.put(i)
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(queue, lock):
            while True:
                async with lock:
                    if not queue.empty():
                        item = await queue.get()
                        if item is None:
                            # print("Detected end of queue")
                            # End of jobs
                            queue.task_done()
                            break
                        print(item)
                        queue.task_done()
                await asyncio.sleep(0.1)

        async def main():
            queue = asyncio.Queue()
            lock = asyncio.Lock()
            producer_tasks = [
                asyncio.create_task(producer(queue, lock)) for i in range(3)
            ]
            consumer_tasks = [
                asyncio.create_task(consumer(queue, lock)) for i in range(3)
            ]
            await asyncio.gather(*producer_tasks, *consumer_tasks)
            await queue.join()
            for consumer_task in consumer_tasks:
                consumer_task.cancel()

        asyncio.run(main())
        print(
            """ 
        async def producer(queue, lock):
            for i in range(10):
                async with lock:
                    await queue.put(i)
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(queue, lock):
            while True:
                async with lock:
                    if not queue.empty():
                        item = await queue.get()
                        if item is None:
                            # print("Detected end of queue")
                            # End of jobs
                            queue.task_done()
                            break
                        print(item)
                        queue.task_done()
                await asyncio.sleep(0.1)

        async def main():
            queue = asyncio.Queue()
            lock = asyncio.Lock()
            producer_tasks = [
                asyncio.create_task(producer(queue, lock)) for i in range(3)
            ]
            consumer_tasks = [
                asyncio.create_task(consumer(queue, lock)) for i in range(3)
            ]
            await asyncio.gather(*producer_tasks, *consumer_tasks)
            await queue.join()
            for consumer_task in consumer_tasks:
                consumer_task.cancel()

        asyncio.run(main())
        """
        )

        pass

    def queuec_example(self):
        # 15
        # print("Press ctrl-c to stop this example")

        async def producer(condition, queue):
            for i in range(10):
                async with condition:
                    await queue.put(i)
                    condition.notify_all()
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(condition, queue):
            while True:
                async with condition:
                    if not queue.empty():
                        item = await queue.get()
                        if item is None:
                            # print("Detected end of queue")
                            # End of jobs
                            queue.task_done()
                            break
                        print(item)
                        queue.task_done()
                await asyncio.sleep(0.1)

        async def main():
            queue = asyncio.Queue()
            condition = asyncio.Condition()
            producer_tasks = [
                asyncio.create_task(producer(condition, queue)) for i in range(3)
            ]
            consumer_tasks = [
                asyncio.create_task(consumer(condition, queue)) for i in range(3)
            ]
            await asyncio.gather(*producer_tasks, *consumer_tasks)
            await queue.join()
            for consumer_task in consumer_tasks:
                consumer_task.cancel()

        asyncio.run(main())

        print(
            """
        async def producer(condition, queue):
            for i in range(10):
                async with condition:
                    await queue.put(i)
                    condition.notify_all()
                await asyncio.sleep(1)
            await queue.put(None)

        async def consumer(condition, queue):
            while True:
                async with condition:
                    if not queue.empty():
                        item = await queue.get()
                        if item is None:
                            # print("Detected end of queue")
                            # End of jobs
                            queue.task_done()
                            break
                        print(item)
                        queue.task_done()
                await asyncio.sleep(0.1)

        async def main():
            queue = asyncio.Queue()
            condition = asyncio.Condition()
            producer_tasks = [
                asyncio.create_task(producer(condition, queue)) for i in range(3)
            ]
            consumer_tasks = [
                asyncio.create_task(consumer(condition, queue)) for i in range(3)
            ]
            await asyncio.gather(*producer_tasks, *consumer_tasks)
            await queue.join()
            for consumer_task in consumer_tasks:
                consumer_task.cancel()

        asyncio.run(main())
        """
        )
        pass
