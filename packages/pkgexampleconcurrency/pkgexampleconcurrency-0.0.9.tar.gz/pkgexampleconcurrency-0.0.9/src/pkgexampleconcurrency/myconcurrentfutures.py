import concurrent.futures
import time
import threading
import queue
import random

from collections import deque
import multiprocessing
from multiprocessing import Manager


class MyThreadConcurrentfutures:
    def __init__(self):
        pass

    def some_task(self, n):
        return n * n

    def sleep_task(self, n):
        sleep_time = random.randint(1, 5)
        time.sleep(sleep_time)
        return n

    def worker(self, n):
        print(f"Starting worker {n}")
        time.sleep(n * 2)
        print(f"Finishing worker {n}")
        return n

    def add(self, x, y):
        return x + y

    def map_corresponding(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add, [1, 2, 3], [4, 5, 6])
            for result in results:
                print(result)

        print(
            """
    def add(self, x, y):
        return x + y

    def map_corresponding(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add, [1, 2, 3], [4, 5, 6])
            for result in results:
                print(result)

    # ThreadPoolExecutor Example


    # def map_corresponding(self): creates a thread pool and apply
    # the add method to corresponding elements in the two lists
    # [1, 2, 3] and [4, 5, 6]. The map() method returns an iterator
    # that yields the results of each function call in the order that
    # they were submitted.
                
        """
        )

    # def map_corresponding(self): creates a thread pool and apply
    # the add method to corresponding elements in the two lists
    # [1, 2, 3] and [4, 5, 6]. The map() method returns an iterator
    # that yields the results of each function call in the order that
    # they were submitted.

    def add_tups(self, args):
        x, y = args
        return x + y

    def map_tuples(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

        print(
            """ 
    def add_tups(self, args):
        x, y = args
        return x + y

    def map_tuples(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

    # ThreadPoolExecutor Example

    # def map_tuples(self): uses the map() creates a thread pool
    # and applies the add_tups method to each tuple in the list
    # [(1, 4), (2, 5), (3, 6)]. The map() method returns an iterator
    # that yields the results of each function call in the order
    # that they were submitted.                    
    """
        )

    # def map_tuples(self): uses the map() creates a thread pool
    # and applies the add_tups method to each tuple in the list
    # [(1, 4), (2, 5), (3, 6)]. The map() method returns an iterator
    # that yields the results of each function call in the order
    # that they were submitted.

    def submit_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        print(
            """ 
    def some_task(self, n):
        return n * n

    def submit_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

    # ThreadPoolExecutor Example

    # def submit_example(self): creates a thread pool and submit a single
    # task to it using the submit() method. The submit() method returns
    # a Future object that represents the result of the task when it completes.

        """
        )

    # def submit_example(self): creates a thread pool and submit a single
    # task to it using the submit() method. The submit() method returns
    # a Future object that represents the result of the task when it completes.

    def result_example(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

        print(
            """
    def some_task(self, n):
        return n * n

    def add_tups(self, args):
        x, y = args
        return x + y

    def result_example(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

        # ThreadPoolExecutor Example


        # A future object can return one result, or an itterable of many results
        # depending on which methods you call. For example,

        # The submit() method returns a Future object, which represents the result
        # of a single task that is submitted to the executor. Calling the result()
        # method on this Future object will block until the result of the single task
        # is available, at which point it returns the result.

        # The map() method returns an iterator that yields the results of multiple tasks
        # submitted to the executor. When you call map() with a function and one or more
        # iterable arguments, it will apply the function to the corresponding elements
        # of the iterables, and yield the results as they become available.
        
           """
        )

        # A future object can return one result, or an itterable of many results
        # depending on which methods you call. For example,

        # The submit() method returns a Future object, which represents the result
        # of a single task that is submitted to the executor. Calling the result()
        # method on this Future object will block until the result of the single task
        # is available, at which point it returns the result.

        # The map() method returns an iterator that yields the results of multiple tasks
        # submitted to the executor. When you call map() with a function and one or more
        # iterable arguments, it will apply the function to the corresponding elements
        # of the iterables, and yield the results as they become available.

    def as_complete_example(self):
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

        print(
            """ 
    def some_task(self, n):
        return n * n

    def as_complete_example(self):
        futures = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

        # ThreadPoolExecutor Example


        # as_complete_example(self): creates a thread pool and submit multiple tasks to it
        # using the submit() method. The submit() method returns a Future object that
        # represents the result of the task when it completes.
        # The as_completed() function is then used to iterate over the completed futures
        # in the order they completed, yielding each future as it completes.

        # Notice that the tasks are returned in the order they are completed, not submitted.
        # If you need to ensure that the results are returned in the order in which the jobs
        # were submitted, you can use the map() method instead of submit() and as_completed().
        # The map() method applies the specified function to each element of one or more input
        # iterables in order, and returns an iterator that yields the results in the same order
        # as the input iterables.

        """
        )

        # as_complete_example(self): creates a thread pool and submit multiple tasks to it
        # using the submit() method. The submit() method returns a Future object that
        # represents the result of the task when it completes.
        # The as_completed() function is then used to iterate over the completed futures
        # in the order they completed, yielding each future as it completes.

        # Notice that the tasks are returned in the order they are completed, not submitted.
        # If you need to ensure that the results are returned in the order in which the jobs
        # were submitted, you can use the map() method instead of submit() and as_completed().
        # The map() method applies the specified function to each element of one or more input
        # iterables in order, and returns an iterator that yields the results in the same order
        # as the input iterables.

    def done_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        while futures:
            for future in futures:
                if future.done():
                    try:
                        result = future.result()
                        print(f"Task {result} has completed.")
                    except Exception as e:
                        print(f"Task {result} raised an exception: {e}")
                    futures.remove(future)
                else:
                    print("Task is still running")

        print(
            """ 

    def some_task(self, n):
        return n * n

    def done_examaple(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        while futures:
            for future in futures:
                if future.done():
                    try:
                        result = future.result()
                        print(f"Task \{result\} has completed.")
                    except Exception as e:
                        print(f"Task \{result\} raised an exception: \{e\}")
                    futures.remove(future)
                else:
                    print("Task is still running")

        # ThreadPoolExecutor Example


        # def done_examaple(self): Sumbits multiple tasks using submit(). It then
        # continuously monitors the returned futures using the future.done() method.
        # When a future is done, it prints the result and removes the future from
        # the list of futures. It then continues monitoring the futures until all
        # of them are complete.

        """
        )

        # def done_examaple(self): Sumbits multiple tasks using submit(). It then
        # continuously monitors the returned futures using the future.done() method.
        # When a future is done, it prints the result and removes the future from
        # the list of futures. It then continues monitoring the futures until all
        # of them are complete.

    def print_result(self, future):
        result = future.result()
        print(result)

    def callback_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            future.add_done_callback(self.print_result)

        print(
            """ 
    def some_task(self, n):
        return n * n

    def print_result(self, future):
        result = future.result()
        print(result)

    def callback_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            future.add_done_callback(self.print_result)

    # ThreadPoolExecutor Example


    # In this example, we submit a job method some_task() with an argument of 5, which
    # returns one Future object representing the result of the task. We then register the
    # print_result() method to be called when the task is complete using the add_done_callback()
    # method. When the task completes, the print_result() method is called with the Future object as
    # its argument, and it prints the result of the task.
    # This is an alternative to checking each task using .done() and then running a method.

        """
        )

        # In this example, we submit a job method some_task() with an argument of 5, which
        # returns one Future object representing the result of the task. We then register the
        # print_result() method to be called when the task is complete using the add_done_callback()
        # method. When the task completes, the print_result() method is called with the Future object as
        # its argument, and it prints the result of the task.
        # This is an alternative to checking each task using .done() and then running a method.

    def shutdown_wait_true_example(self):
        print("Submitting jobs")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=True)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

        print(
            """ 

    def worker(self, n):
        print(f"Starting worker \{n\}")
        time.sleep(n * 2)
        print(f"Finishing worker \{n\}")
        return n
        
    def shutdown_wait_true_example(self):
        print("Submitting jobs")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=True)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task \{result\} has completed.")
                        except Exception as e:
                            print(f"Task \{result\} raised an exception: \{e\}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

       # ThreadPoolExecutor Example


        # def shutdown_wait_true_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=True) to wait for all the
        # submitted tasks to complete before shutting down the executor.
        # Finally, the method prints the result of all the futures.
        #
        # When you run this example, the ThreadPoolExecutor will wait for
        # all the tasks to complete before shutting down and printing the results.

        """
        )

        # def shutdown_wait_true_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=True) to wait for all the
        # submitted tasks to complete before shutting down the executor.
        # Finally, the method prints the result of all the futures.
        #
        # When you run this example, the ThreadPoolExecutor will wait for
        # all the tasks to complete before shutting down and printing the results.

    def shutdown_wait_false_example(self):
        print("Submitting jobs")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=False)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)
        print(
            """ 
    def worker(self, n):
        print(f"Starting worker \{n\}")
        time.sleep(n * 2)
        print(f"Finishing worker \{n\}")
        return n
        
    def shutdown_wait_false_example(self):
        print("Submitting jobs")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=False)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

      # ThreadPoolExecutor Example


        # def shutdown_wait_false_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=False) to signal that the
        # executor should not accept any new tasks and should shut down immediately,
        # without waiting for the tasks that are currently running to complete.
        # The wait parameter is set to False, which means that the shutdown method
        # returns immediately without blocking, allowing the program to continue running
        # while the tasks are still executing. This can be useful if you want to perform
        # other actions while the tasks are running, or if you want to terminate the
        # program quickly without waiting for the tasks to finish.
                
        """
        )

        # def shutdown_wait_false_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=False) to signal that the
        # executor should not accept any new tasks and should shut down immediately,
        # without waiting for the tasks that are currently running to complete.
        # The wait parameter is set to False, which means that the shutdown method
        # returns immediately without blocking, allowing the program to continue running
        # while the tasks are still executing. This can be useful if you want to perform
        # other actions while the tasks are running, or if you want to terminate the
        # program quickly without waiting for the tasks to finish.

    def count_down(self, n):
        for i in range(n, 0, -1):
            print(f"{i} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.count_down, 10)
            time.sleep(5)
            if not future.done():
                future.cancel()
                print("Task cancelled!")

        print(
            """ 

    def count_down(self, n):
        for i in range(n, 0, -1):
            print(f"\{i\} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.count_down, 10)
            time.sleep(5)
            if not future.done():
                future.cancel()
                print("Task cancelled!")

    # ThreadPoolExecutor Example

    # def cancel_example(self): submits the count_down() method to run in a
    # separate thread with an argument of 10. It then waits for 5 seconds
    # and checks if the future returned by executor.submit() is done by
    # calling the done() method. If the future is not done, it cancels the
    # future using the cancel() method and prints a message indicating that
    # the task was cancelled. This is a demonstration on how to cancel a running
    # thread using the cancel() method.

    # WARNING: If a task is already executing it won't stop, you'll need to
    # pass an event, see example --tcancel-ec
        
        """
        )

    # def cancel_example(self): submits the count_down() method to run in a
    # separate thread with an argument of 10. It then waits for 5 seconds
    # and checks if the future returned by executor.submit() is done by
    # calling the done() method. If the future is not done, it cancels the
    # future using the cancel() method and prints a message indicating that
    # the task was cancelled. This is a demonstration on how to cancel a running
    # thread using the cancel() method.
    # WARNING: If a task is already executing it won't stop, you'll need to
    # pass an event, see example --tcancel-ec

    def count_down_ccheck(self, n, cancel_event):
        for i in range(n, 0, -1):
            if cancel_event.is_set():
                return
            print(f"{i} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example_with_event(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            cancel_event = threading.Event()
            future = executor.submit(self.count_down_ccheck, 10, cancel_event)
            time.sleep(5)
            if not future.done():
                cancel_event.set()
                print("Task cancelled!")

        print(
            """ 
        
    def count_down_ccheck(self, n, cancel_event):
        for i in range(n, 0, -1):
            if cancel_event.is_set():
                return
            print(f"\{i\} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example_with_event(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            cancel_event = threading.Event()
            future = executor.submit(self.count_down_ccheck, 10, cancel_event)
            time.sleep(5)
            if not future.done():
                cancel_event.set()
                print("Task cancelled!")

    # ThreadPoolExecutor Example

    # def cancel_example_with_event(self): is another example on how to cancel
    # a task. It's very similar to def cancel_example(self):, but explicitly
    # sends a threading 'cancel_event' Event.  Not as clean, but it does allow
    # you to cancel a task that is already in progress. Threads share the same
    # memory space so you can share states between tasks. Most of these example
    # can be copied code for code for a ProcessPoolExecutor() but not this.
    # You need to use Managers to share states between processes ( which do
    # not share memory space).
        """
        )

    # ThreadPoolExecutor Example

    # def cancel_example_with_event(self): is another example on how to cancel
    # a task. It's very similar to def cancel_example(self):, but explicitly
    # sends a threading 'cancel_event' Event.  Not as clean, but it does allow
    # you to cancel a task that is already in progress. Threads share the same
    # memory space so you can share states between tasks. Most of these example
    # can be copied code for code for a ProcessPoolExecutor() but not this.
    # You need to use Managers to share states between processes ( which do
    # not share memory space).
    def qworker(self, queue):
        while True:
            item = queue.get()
            if item is None:
                break
            # Do some work on the item
            print(f"Processing item {item}")
            # Mark the item as done
            queue.task_done()

    def queue_example(self):
        # Create a queue and fill it with some items
        my_queue = queue.Queue()
        for i in range(10):
            my_queue.put(i)

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            futures = []
            for _ in range(3):
                future = executor.submit(self.qworker, my_queue)
                futures.append(future)
            # Wait for all tasks to be processed
            my_queue.join()

            # Signal the worker threads to exit
            for _ in range(3):
                my_queue.put(None)

            # Wait for the worker threads to finish
            for future in futures:
                future.result()

        print(
            """ 

    def qworker(self, queue):
        while True:
            item = queue.get()
            if item is None:
                break
            # Do some work on the item
            print(f"Processing item \{item\}")
            # Mark the item as done
            queue.task_done()

    def queue_example(self):
        # Create a queue and fill it with some items
        my_queue = queue.Queue()
        for i in range(10):
            my_queue.put(i)

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            futures = []
            for _ in range(3):
                future = executor.submit(self.qworker, my_queue)
                futures.append(future)
            # Wait for all tasks to be processed
            my_queue.join()

            # Signal the worker threads to exit
            for _ in range(3):
                my_queue.put(None)

            # Wait for the worker threads to finish
            for future in futures:
                future.result()
        """
        )

    def lqworker(self, q, lock):
        with lock:
            q.put("Hello from thread")

    def lqueue_example(self):
        q = queue.Queue()
        lock = threading.Lock()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.lqworker, q, lock)
        with lock:
            print(q.get())
        print(
            """ 
    def lqworker(self,q, lock):
        with lock:
            q.put("Hello from thread")

    def lqueue_example(self):
        q = queue.Queue()
        lock = threading.Lock()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.lqworker, q, lock)
        with lock:
            print(q.get())
        """
        )

    def dqworker(self, queue):
        while True:
            try:
                item = queue.popleft()
            except IndexError:
                # Queue is empty, exit worker loop
                break
            # Do some work on the item
            print(f"Processing item {item}")

    def dqueue_example(self):
        # Create a queue and fill it with some items
        my_queue = deque(range(10))

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            num_tasks = len(my_queue)
            futures = []
            for _ in range(3):
                future = executor.submit(self.dqworker, my_queue)
                futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Verify that all tasks were processed
            if my_queue:
                raise ValueError("Not all tasks were processed")
        print(
            """ 
    
    def dqworker(self, queue):
        while True:
            try:
                item = queue.popleft()
            except IndexError:
                # Queue is empty, exit worker loop
                break
            # Do some work on the item
            print(f"Processing item \{item\}")

    def dqueue_example(self):
        # Create a queue and fill it with some items
        my_queue = deque(range(10))

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            num_tasks = len(my_queue)
            futures = []
            for _ in range(3):
                future = executor.submit(self.dqworker, my_queue)
                futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Verify that all tasks were processed
            if my_queue:
                raise ValueError("Not all tasks were processed")
        """
        )

    def ldqworker(self, queue, lock):
        while True:
            try:
                with lock:
                    item = queue.popleft()
            except IndexError:
                # Queue is empty, exit worker loop
                break
            # Do some work on the item
            print(f"Processing item {item}")

    def ldqueue_example(self):
        # Create a queue and fill it with some items
        my_queue = deque(range(10))
        my_lock = threading.Lock()

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            num_tasks = len(my_queue)
            futures = []
            for _ in range(3):
                future = executor.submit(self.ldqworker, my_queue, my_lock)
                futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Verify that all tasks were processed
            if my_queue:
                raise ValueError("Not all tasks were processed")
        print(
            """ 
    def ldqworker(self, queue, lock):
        while True:
            try:
                with lock:
                    item = queue.popleft()
            except IndexError:
                # Queue is empty, exit worker loop
                break
            # Do some work on the item
            print(f"Processing item {item}")

    def ldqueue_example(self):
        # Create a queue and fill it with some items
        my_queue = deque(range(10))
        my_lock = threading.Lock()

        # Create a thread pool executor with 3 worker threads
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            num_tasks = len(my_queue)
            futures = []
            for _ in range(3):
                future = executor.submit(self.ldqworker, my_queue, my_lock)
                futures.append(future)

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)

            # Verify that all tasks were processed
            if my_queue:
                raise ValueError("Not all tasks were processed")
        """
        )


class MyProcessConcurrentfutures:
    def __init__(self):
        pass

    def some_task(self, n):
        return n * n

    def sleep_task(self, n):
        sleep_time = random.randint(1, 5)
        time.sleep(sleep_time)
        return n

    def worker(self, n):
        print(f"Starting worker {n}")
        time.sleep(n * 2)
        print(f"Finishing worker {n}")
        return n

    def add(self, x, y):
        return x + y

    def map_corresponding(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add, [1, 2, 3], [4, 5, 6])
            for result in results:
                print(result)

        print(
            """
    def add(self, x, y):
        return x + y

    def map_corresponding(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add, [1, 2, 3], [4, 5, 6])
            for result in results:
                print(result)

    # ProcessPoolExecutor Example


    # def map_corresponding(self): creates a process pool and apply
    # the add method to corresponding elements in the two lists
    # [1, 2, 3] and [4, 5, 6]. The map() method returns an iterator
    # that yields the results of each function call in the order that
    # they were submitted.
                
        """
        )

    # def map_corresponding(self): creates a thread pool and apply
    # the add method to corresponding elements in the two lists
    # [1, 2, 3] and [4, 5, 6]. The map() method returns an iterator
    # that yields the results of each function call in the order that
    # they were submitted.

    def add_tups(self, args):
        x, y = args
        return x + y

    def map_tuples(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)
        print(
            """ 
    def add_tups(self, args):
        x, y = args
        return x + y

    def map_tuples(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

    # ProcessPoolExecutor Example

    # def map_tuples(self): uses the map() creates a process pool
    # and applies the add_tups method to each tuple in the list
    # [(1, 4), (2, 5), (3, 6)]. The map() method returns an iterator
    # that yields the results of each function call in the order
    # that they were submitted.                    
    """
        )

    # def map_tuples(self): uses the map() creates a thread pool
    # and applies the add_tups method to each tuple in the list
    # [(1, 4), (2, 5), (3, 6)]. The map() method returns an iterator
    # that yields the results of each function call in the order
    # that they were submitted.

    def submit_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        print(
            """ 
    def some_task(self, n):
        return n * n

    def submit_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

    # ProcessPoolExecutor Example

    # def submit_example(self): creates a process pool and submit a single
    # task to it using the submit() method. The submit() method returns
    # a Future object that represents the result of the task when it completes.
        
        """
        )

    # def submit_example(self): creates a thread pool and submit a single
    # task to it using the submit() method. The submit() method returns
    # a Future object that represents the result of the task when it completes.

    def result_example(self):

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

        print(
            """
    def some_task(self, n):
        return n * n

    def add_tups(self, args):
        x, y = args
        return x + y

    def result_example(self):

        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            print(future.result())

        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.add_tups, [(1, 4), (2, 5), (3, 6)])
            for result in results:
                print(result)

        # ProcessPoolExecutor Example


        # A future object can return one result, or an itterable of many results
        # depending on which methods you call. For example,

        # The submit() method returns a Future object, which represents the result
        # of a single task that is submitted to the executor. Calling the result()
        # method on this Future object will block until the result of the single task
        # is available, at which point it returns the result.

        # The map() method returns an iterator that yields the results of multiple tasks
        # submitted to the executor. When you call map() with a function and one or more
        # iterable arguments, it will apply the function to the corresponding elements
        # of the iterables, and yield the results as they become available.
        
           """
        )

        # A future object can return one result, or an itterable of many results
        # depending on which methods you call. For example,

        # The submit() method returns a Future object, which represents the result
        # of a single task that is submitted to the executor. Calling the result()
        # method on this Future object will block until the result of the single task
        # is available, at which point it returns the result.

        # The map() method returns an iterator that yields the results of multiple tasks
        # submitted to the executor. When you call map() with a function and one or more
        # iterable arguments, it will apply the function to the corresponding elements
        # of the iterables, and yield the results as they become available.

    def as_complete_example(self):
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

        print(
            """ 
    def some_task(self, n):
        return n * n

    def as_complete_example(self):
        futures = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            print(future.result())

        # ProcessPoolExecutor Example


        # as_complete_example(self): creates a process pool and submits multiple tasks to it
        # using the submit() method. The submit() method returns a Future object that
        # represents the result of the task when it completes.
        # The as_completed() function is then used to iterate over the completed futures
        # in the order they completed, yielding each future as it completes.

        # Notice that the tasks are returned in the order they are completed, not submitted.
        # If you need to ensure that the results are returned in the order in which the jobs
        # were submitted, you can use the map() method instead of submit() and as_completed().
        # The map() method applies the specified function to each element of one or more input
        # iterables in order, and returns an iterator that yields the results in the same order
        # as the input iterables.

        """
        )
        # as_complete_example(self): creates a thread pool and submit multiple tasks to it
        # using the submit() method. The submit() method returns a Future object that
        # represents the result of the task when it completes.
        # The as_completed() function is then used to iterate over the completed futures
        # in the order they completed, yielding each future as it completes.

        # Notice that the tasks are returned in the order they are completed, not submitted.
        # If you need to ensure that the results are returned in the order in which the jobs
        # were submitted, you can use the map() method instead of submit() and as_completed().
        # The map() method applies the specified function to each element of one or more input
        # iterables in order, and returns an iterator that yields the results in the same order
        # as the input iterables.

    def done_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        while futures:
            for future in futures:
                if future.done():
                    try:
                        result = future.result()
                        print(f"Task {result} has completed.")
                    except Exception as e:
                        print(f"Task {result} raised an exception: {e}")
                    futures.remove(future)
                else:
                    print("Task is still running")
        print(
            """ 

    def some_task(self, n):
        return n * n

    def done_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.some_task, i)
                futures.append(future)

        while futures:
            for future in futures:
                if future.done():
                    try:
                        result = future.result()
                        print(f"Task \{result\} has completed.")
                    except Exception as e:
                        print(f"Task \{result\} raised an exception: \{e\}")
                    futures.remove(future)
                else:
                    print("Task is still running")

        # ProcessPoolExecutor Example


        # def done_examaple(self): Sumbits multiple tasks using submit(). It then
        # continuously monitors the returned futures using the future.done() method.
        # When a future is done, it prints the result and removes the future from
        # the list of futures. It then continues monitoring the futures until all
        # of them are complete.

        """
        )
        # def done_examaple(self): Sumbits multiple tasks using submit(). It then
        # continuously monitors the returned futures using the future.done() method.
        # When a future is done, it prints the result and removes the future from
        # the list of futures. It then continues monitoring the futures until all
        # of them are complete.

    def print_result(self, future):
        result = future.result()
        print(result)

    def callback_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            future.add_done_callback(self.print_result)

        print(
            """ 
    def some_task(self, n):
        return n * n

    def print_result(self, future):
        result = future.result()
        print(result)

    def callback_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.some_task, 5)
            future.add_done_callback(self.print_result)

    # ProcessPoolExecutor Example


    # In this example, we submit a job method some_task() with an argument of 5, which
    # returns one Future object representing the result of the task. We then register the
    # print_result() method to be called when the task is complete using the add_done_callback()
    # method. When the task completes, the print_result() method is called with the Future object as
    # its argument, and it prints the result of the task.
    # This is an alternative to checking each task using .done() and then running a method.

        """
        )

        # In this example, we submit a job method some_task() with an argument of 5, which
        # returns one Future object representing the result of the task. We then register the
        # print_result() method to be called when the task is complete using the add_done_callback()
        # method. When the task completes, the print_result() method is called with the Future object as
        # its argument, and it prints the result of the task.
        # This is an alternative to checking each task using .done() and then running a method.

    def shutdown_wait_true_example(self):
        print("Submitting jobs")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=True)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

        print(
            """ 

    def worker(self, n):
        print(f"Starting worker \{n\}")
        time.sleep(n * 2)
        print(f"Finishing worker \{n\}")
        return n
        
    def shutdown_wait_true_example(self):
        print("Submitting jobs")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=True)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task \{result\} has completed.")
                        except Exception as e:
                            print(f"Task \{result\} raised an exception: \{e\}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

       # ProcessPoolExecutor Example


        # def shutdown_wait_true_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=True) to wait for all the
        # submitted tasks to complete before shutting down the executor.
        # Finally, the method prints the result of all the futures.
        #
        # When you run this example, the ProcessPoolExecutor will wait for
        # all the tasks to complete before shutting down and printing the results.

        """
        )

        # def shutdown_wait_true_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=True) to wait for all the
        # submitted tasks to complete before shutting down the executor.
        # Finally, the method prints the result of all the futures.
        #
        # When you run this example, the ThreadPoolExecutor will wait for
        # all the tasks to complete before shutting down and printing the results.

    def shutdown_wait_false_example(self):
        print("Submitting jobs")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=False)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)
        print(
            """ 
    def worker(self, n):
        print(f"Starting worker \{n\}")
        time.sleep(n * 2)
        print(f"Finishing worker \{n\}")
        return n
        
    def shutdown_wait_false_example(self):
        print("Submitting jobs")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for i in range(5):
                future = executor.submit(self.worker, i)
                futures.append(future)

            executor.shutdown(wait=False)
            print("Main thread continues executing...")

            while futures:
                for future in futures:
                    if future.done():
                        try:
                            result = future.result()
                            print(f"Task {result} has completed.")
                        except Exception as e:
                            print(f"Task {result} raised an exception: {e}")
                        futures.remove(future)
                    else:
                        print("Task is still running")
                # wait a second before rechecking futures
                time.sleep(2)

        # ProcessPoolExecutor Example


        # def shutdown_wait_false_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=False) to signal that the
        # executor should not accept any new tasks and should shut down immediately,
        # without waiting for the tasks that are currently running to complete.
        # The wait parameter is set to False, which means that the shutdown method
        # returns immediately without blocking, allowing the program to continue running
        # while the tasks are still executing. This can be useful if you want to perform
        # other actions while the tasks are running, or if you want to terminate the
        # program quickly without waiting for the tasks to finish.
                
        """
        )

        # def shutdown_wait_true_example(self): submits a range of jobs,
        # it then calls executor.shutdown(wait=False) to signal that the
        # executor should not accept any new tasks and should shut down immediately,
        # without waiting for the tasks that are currently running to complete.
        # The wait parameter is set to False, which means that the shutdown method
        # returns immediately without blocking, allowing the program to continue running
        # while the tasks are still executing. This can be useful if you want to perform
        # other actions while the tasks are running, or if you want to terminate the
        # program quickly without waiting for the tasks to finish.

    def count_down(self, n):
        for i in range(n, 0, -1):
            print(f"{i} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.count_down, 10)
            time.sleep(5)
            if not future.done():
                future.cancel()
                print("Task cancelled!")

        print(
            """ 

    def count_down(self, n):
        for i in range(n, 0, -1):
            print(f"\{i\} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future = executor.submit(self.count_down, 10)
            time.sleep(5)
            if not future.done():
                future.cancel()
                print("Task cancelled!")

    # ProcessPoolExecutor Example

    # def cancel_example(self): submits the count_down() method to run in a
    # separate thread with an argument of 10. It then waits for 5 seconds
    # and checks if the future returned by executor.submit() is done by
    # calling the done() method. If the future is not done, it cancels the
    # future using the cancel() method and prints a message indicating that
    # the task was cancelled. This is a demonstration on how to cancel a running
    # thread using the cancel() method.

    # WARNING: If a task is already executing it won't stop, you'll need to
    # pass an event, see example --tcancel-ec
        
        """
        )

    # def cancel_example(self): submits the count_down() method to run in a
    # separate thread with an argument of 10. It then waits for 5 seconds
    # and checks if the future returned by executor.submit() is done by
    # calling the done() method. If the future is not done, it cancels the
    # future using the cancel() method and prints a message indicating that
    # the task was cancelled. This is a demonstration on how to cancel a running
    # thread using the cancel() method.
    # WARNING: If a task is already executing it won't stop, you'll need to
    # pass an event, see example --tcancel-ec

    def count_down_ccheck(self, n, cancel_event):
        for i in range(n, 0, -1):
            if cancel_event.is_set():
                return
            print(f"{i} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example_with_event(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            with Manager() as manager:
                cancel_event = manager.Event()
                future = executor.submit(self.count_down_ccheck, 10, cancel_event)
                time.sleep(5)
                if not future.done():
                    cancel_event.set()
                    print("Task cancelled!")
                manager.shutdown
        print(
            """ 
    def count_down_ccheck(self, n, cancel_event):
        for i in range(n, 0, -1):
            if cancel_event.is_set():
                return
            print(f"\{i\} seconds left...")
            time.sleep(1)
        print("Time's up!")

    def cancel_example_with_event(self):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            with Manager() as manager:
                cancel_event = manager.Event()
                future = executor.submit(self.count_down_ccheck, 10, cancel_event)
                time.sleep(5)
                if not future.done():
                    cancel_event.set()
                    print("Task cancelled!")
                manager.shutdown

    # ProcessPoolExecutor Example

    # def cancel_example_with_event(self): is another example on how to cancel
    # a task. It's very similar to def cancel_example(self):, but explicitly
    # sends a threading 'cancel_event' Event.  Not as clean, but it does allow
    # you to cancel a task that is already in progress. Processes do not share
    # share the same memory space so you must use a Manager to share states 
    # between processes.
    # Please note the slightly different implementation to the ThreadPoolExecutor
    # example.    
        """
        )

    def qworker(self, queue):
        while True:
            item = queue.get()
            if item is None:
                print("Process exiting")
                break
            # Do some work on the item
            print(f"Processing item {item}")

    def queue_example(self):
        # Create a queue and fill it with some items
        my_queue = multiprocessing.Queue()
        for i in range(10):
            my_queue.put(i)

        # Create a thread pool executor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            futures = []
            for _ in range(3):
                future = executor.submit(self.qworker, my_queue)
                futures.append(future)

            # Signal the workers to exit
            for _ in range(3):
                my_queue.put(None)

            # Wait for the worker to finish
            for future in futures:
                future.result()

        print(
            """ 

    def qworker(self, queue):
        while True:
            item = queue.get()
            if item is None:
                print("Process exiting")
                break
            # Do some work on the item
            print(f"Processing item \{item\}")

    def queue_example(self):
        # Create a queue and fill it with some items
        my_queue = multiprocessing.Queue()
        for i in range(10):
            my_queue.put(i)

        # Create a thread pool executor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the worker function to the executor
            futures = []
            for _ in range(3):
                future = executor.submit(self.qworker, my_queue)
                futures.append(future)

            # Signal the workers to exit
            for _ in range(3):
                my_queue.put(None)

            # Wait for the worker to finish
            for future in futures:
                future.result()
        """
        )

    def pipe_worker(self, pipe, data):
        result = data**2
        pipe.send(result)

    def pipe_example(self):
        # Create a pipe for communication between threads
        parent_conn, child_conn = multiprocessing.Pipe()

        # Create a thread pool
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit two tasks to the thread pool
            futures = []
            for i in range(2):
                future = executor.submit(self.pipe_worker, child_conn, i)
                futures.append(future)

            # Wait for the tasks to complete
            concurrent.futures.wait(futures)

            # Get the results from the pipe
            results = []
            while parent_conn.poll():
                result = parent_conn.recv()
                results.append(result)

        # Print the results
        print(results)
        print(
            """ 
    def pipe_worker(self, pipe, data):
        result = data**2
        pipe.send(result)

    def pipe_example(self):
        # Create a pipe for communication between threads
        parent_conn, child_conn = multiprocessing.Pipe()

        # Create a thread pool
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit two tasks to the thread pool
            futures = []
            for i in range(2):
                future = executor.submit(self.pipe_worker, child_conn, i)
                futures.append(future)

            # Wait for the tasks to complete
            concurrent.futures.wait(futures)

            # Get the results from the pipe
            results = []
            while parent_conn.poll():
                result = parent_conn.recv()
                results.append(result)

        # Print the results
        print(results)
        """
        )
