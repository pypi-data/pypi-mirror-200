import threading
import time
import queue
import random
from collections import deque
import os


class OutputAlpha(threading.Thread):
    def __init__(self, daemon: bool, sleeptime: int):
        threading.Thread.__init__(self)
        self.sleeptime = sleeptime
        self.daemon = daemon

    def run(self):
        for char in "abcdefg":
            time.sleep(self.sleeptime)
            print(char)


class MyThreading:
    def __init__(self):
        pass

    def print_evens(self):
        max_num = 6
        for i in range(0, max_num + 1, 2):
            time.sleep(max_num + 1 - i)
            print(i)

    def print_odds(self):
        max_num = 6
        for i in range(1, max_num + 1, 2):
            time.sleep(i + 1)
            print(i)

    def item_producer(self, builtin_queue_class):
        for i in range(10):
            time.sleep(1)
            print(f"Produced item {i}")
            builtin_queue_class.put(i)

    def item_consumer(self, builtin_queue_class):
        while True:
            try:
                time.sleep(2)
                item = builtin_queue_class.get()
                if item is None:
                    break
                print(f"Consuming item {item}")
            except queue.Empty:
                break

    def thread_count(self):
        k = 5
        max_threads = k * os.cpu_count()
        print(
            f"""If you at anypoint use the concurrent futures module,
This would be your maxium number of concurrent threads.

    ThreadPoolExecutor(max_workers={max_threads})
    
Of course, you could double the number, but half of your threads 
won't be executing concurrently

This was estimated using a rule of thumb multiplication,

  max_threads = k * os.cpu_count()

Your code task *might* suffer performance issues if you load your system 
with too many threads.  Experimentation per hardware is recomended.

Of course, systems and OS can have many threads.

cat /proc/sys/kernel/threads-max 
125998

The /proc/sys/kernel/threads-max file is a system file on Linux systems that specifies the maximum number
of threads that can be created system-wide. This value represents the absolute upper limit on the number 
of threads that can be created on the system, regardless of the number of available CPUs or the amount of 
available memory.

When you create a ThreadPoolExecutor object and specify the max_workers parameter, the executor will create 
a pool of worker threads with the specified maximum number of threads. However, this maximum number of 
threads is subject to various limits and constraints such as the amount of available memory and system 
resources, as well as the value of /proc/sys/kernel/threads-max.

In general, the number of threads created by the ThreadPoolExecutor should be less than or equal to the value 
of /proc/sys/kernel/threads-max to avoid resource exhaustion and system instability. If you attempt to create 
more threads than allowed by the system's threads-max limit, the thread creation will fail and you will receive 
an error.

Therefore, when working with ThreadPoolExecutor or any other multithreaded program on a Linux system, it's 
important to keep in mind the system's threads-max limit and design your program to stay within this limit 
to ensure stable and reliable operation.

"""
        )

    def item_consumer_taskdone(self, builtin_queue_class):
        while True:
            try:
                time.sleep(2)
                item = builtin_queue_class.get()
                if item is None:
                    ##If using queue.join() remember, NONE is still an item in the queue and you must call .task_done()
                    builtin_queue_class.task_done()
                    break
                print(f"Consuming item {item}")
                builtin_queue_class.task_done()
            except queue.Empty:
                break

    def item_producer_with_lock(self, builtin_queue_class, threading_lock):
        for i in range(10):
            with threading_lock:
                print(f"Produced item {i}")
                builtin_queue_class.put(i)
            time.sleep(random.random())

    def item_consumer_with_lock(self, builtin_queue_class, threading_lock):
        while True:
            try:
                with threading_lock:
                    # You must check if the queue is empty or not
                    # when using threading locks.  If you don't
                    # you should jam your worker methods.
                    if not builtin_queue_class.empty():
                        item = builtin_queue_class.get()
                        if item is None:
                            break
                        print(f"Consuming item {item}")
                time.sleep(2 * random.random())
            except queue.Empty:
                break

    def item_producer_with_deque(self, my_deque):
        for i in range(10):
            time.sleep(1)
            print(f"Produced item {i}")
            my_deque.append(i)

    def item_consumer_with_deque(self, my_deque):
        while True:
            time.sleep(2)
            if my_deque:
                item = my_deque.popleft()
                if item is None:
                    break
                print(f"Consuming item {item}")

    def print_alpha(self):
        print(
            """#We define a class that inherits the Thread base class,

class OutputAlpha(threading.Thread):

     #Notice we have to overide the base constructor if we want to
     #pass in our own variables.
    def __init__(self, daemon: bool, sleeptime: int):
        threading.Thread.__init__(self)
        self.sleeptime = sleeptime
        self.daemon = daemon

     #We overide the run() method to carry out a task of our choice.
    def run(self):
        for char in "abcdefg":
            time.sleep(self.sleeptime)
            print(char)


     #and then call it from within another class method,
class MyThreading:
    def __init__(self):
        pass

    def print_alpha(self)
        output_alpha = OutputAlpha(daemon=True, sleeptime=1)
        output_alpha.start()
        output_alpha.join()

             """
        )
        output_alpha = OutputAlpha(daemon=True, sleeptime=1)
        output_alpha.start()
        output_alpha.join()

        print(
            """

We ran our thread class as a daemon thread class with joins,
so the main thread waited for the worker thread to finish. """
        )

    def non_daemon_concurrent_example(self):
        t1 = threading.Thread(target=self.print_evens)
        t2 = threading.Thread(target=self.print_odds)

        print(
            """
#This is a non daemon CONCURRENT thread example.
#You will see that odd and even numbers will print
#in mixed order as the threads run concurrently.
#This configuration of the use of .start(), and .join()
#will run your threads concurrently.

----
t1 = threading.Thread(target=self.print_evens)
t2 = threading.Thread(target=self.print_odds)

t1.start()
t2.start()

t1.join()
t2.join()
----

"""
        )

        # This configuration of .start() and .join() will run threads concurrently
        t1.start()
        t2.start()

        t1.join()
        t2.join()
        print(
            """This print statement is called at the end of the main thread, notice 
that when calling .join() on a worker thread this blocks the main thread until
the worker thread has finished its task.  This print statement is the last executed
code in the main thread"""
        )

    def non_daemon_no_join_concurrent_example(self):
        t1 = threading.Thread(target=self.print_evens)
        t2 = threading.Thread(target=self.print_odds)

        print(
            """
#This is a non daemon CONCURRENT thread example
#that does not call .join() on its worker threads.
#You will see that odd and even numbers will print
#in mixed order as the threads run concurrently.
#You will also see that non daemon threads, even when
#not having called join() will hold the main thread open
#untill their tasks complete.

----
t1 = threading.Thread(target=self.print_evens)
t2 = threading.Thread(target=self.print_odds)

t1.start()
t2.start()


----

"""
        )

        # This configuration of .start() and .join() will run threads concurrently
        t1.start()
        t2.start()

        print(
            """This print statement is called at the end of the main thread, notice 
that when NOT calling .join() on a worker thread this does not block the main thread
which is why you are seeing this print statement. However, a running non-daemon worker thread will
keep the main thread open until it finishes its work... which is why you are about to see
the worker threads continue to output numbers.  This main thread will exit when the worker thread is done.

"""
        )

    def non_daemon_serial_example(self):
        t1 = threading.Thread(target=self.print_evens)
        t2 = threading.Thread(target=self.print_odds)

        print(
            """
#This is a non daemon SERIAL thread example.
#You will see that odd and even numbers will print
#at diffent steps as the threads run SERIALY.
#This configuration of the use of .start(), and .join()
#will run your threads SERIALY.

----
t1 = threading.Thread(target=self.print_evens)
t2 = threading.Thread(target=self.print_odds)

t1.start()
t1.join()

t2.start()
t2.join()
----"""
        )

        # This configuration of .start() and .join() will run threads concurrently
        t1.start()
        t1.join()

        t2.start()
        t2.join()
        print(
            """This print statement is called at the end of the main thread, notice 
that when calling .join() on a worker thread this blocks the main thread until
the worker thread has finished its task.  It is this blocking property that enables this configuration
of threads to run SERIALLY. This print statement is the last executed code in the main thread"""
        )

    def daemon_concurrent_example(self):
        t1 = threading.Thread(daemon=True, target=self.print_evens)
        t2 = threading.Thread(daemon=True, target=self.print_odds)

        print(
            """
#This is a DAEMON CONCURRENT thread example.
#You will see that odd and even numbers will print
#in mixed order as the threads run concurrently.
#This configuration of the use of .start(), and .join()
#will run your threads concurrently.

----
t1 = threading.Thread(daemon=True,target=self.print_evens)
t2 = threading.Thread(daemon=True,target=self.print_odds)

t1.start()
t2.start()

t1.join()
t2.join()
----

"""
        )

        # This configuration of .start() and .join() will run threads concurrently
        t1.start()
        t2.start()

        t1.join()
        t2.join()
        print(
            """This print statement is called at the end of the main thread, notice 
that just as in the 'non-daemon' worker thread case, when calling .join() on a worker 
thread this blocks the main thread until the worker thread has finished its task.  
This print statement is the last executed code in the main thread.

Run the non .join() 'Daemon' example to find a difference between 'Daemon' and 'Non-Daemon' worker threads. """
        )

    def daemon_no_join_concurrent_example(self):
        t1 = threading.Thread(daemon=True, target=self.print_evens)
        t2 = threading.Thread(daemon=True, target=self.print_odds)

        print(
            """
#This is a DAEMON CONCURRENT 'no .join()' thread example.
#You might expect that odd and even numbers will print concurrently...

----
t1 = threading.Thread(daemon=True,target=self.print_evens)
t2 = threading.Thread(daemon=True,target=self.print_odds)

t1.start()
t2.start()

----

"""
        )

        # This configuration of .start() will run threads concurrently if your main thread doesn't exit.
        t1.start()
        t2.start()

        print(
            """This print statement is called at the end of the main thread, notice 
that in this 'daemon' worker thread case example no numbers are output.  This is because
a daemon thread without a call to .join() will not be waited for by the main thread.
The main thread printed this statement, exited, and the worker thread didn't
get a chance to complete its job.  Ofcourse, if the main thread is kept alive
by some other task your daemon threads might stand a chance at doing their jobs concurrently.
"""
        )

    # def <> threading queue example using built in queue module
    def threading_queue_example(self):
        print("threading_queue_example")
        print(
            """ 
#This is a THREADING WITH QUEUE example. Using the built in threading, and 
#built in queue class. We create a producer and and consumer method.


def item_producer(self, args):
    builtin_queue_class = args
    for i in range(10):
        time.sleep(1)
        print(f"Produced item {i}")
        builtin_queue_class.put(i)

def item_consumer(self, args):
    builtin_queue_class = args
    while True:
        time.sleep(2)
        item = builtin_queue_class.get()
        if item is None:
            break
        print(f"Consuming item {item}")
        builtin_queue_class.task_done()

#We create a queue object of type builtin queue.Queue()
#Create a thread for the producer, and consumer and pass
#in the queue as a tuple set to an args variable. The args
#variable is unpacked by the methods.

builtin_queue = queue.Queue()
thread1 = threading.Thread(target=self.item_producer, args=(builtin_queue,))
thread2 = threading.Thread(target=self.item_consumer, args=(builtin_queue,))

#We then start the threads in the concurrent configuration.
#Note we add a None item to the queue as an indicator that the 
#end of the queue has been reached.

thread1.start()
thread2.start()

thread1.join()
builtin_queue.put(None)
thread2.join()

            """
        )

        builtin_queue = queue.Queue()
        thread1 = threading.Thread(target=self.item_producer, args=(builtin_queue,))
        thread2 = threading.Thread(target=self.item_consumer, args=(builtin_queue,))

        thread1.start()
        thread2.start()

        thread1.join()
        builtin_queue.put(None)
        thread2.join()

        print(
            """This is a print satement that you should only see after the threads have finished their work."""
        )

    # def <> threading queue example using built in queue module and threading.lock()
    def threading_queue_lock_example(self):
        print(
            """ 
# This is a THREADING WITH QUEUE and LOCK example.
# We create a produducer and a consumer that accept
# a queue and a threading lock.

def item_producer_with_lock(self, builtin_queue_class, threading_lock):
    for i in range(10):
        with threading_lock:
            print(f"Produced item {i}")
            builtin_queue_class.put(i)
        time.sleep(random.random())

def item_consumer_with_lock(self, builtin_queue_class, threading_lock):
    while True:
        try:
            with threading_lock:
                #You must check if the queue is empty or not
                #when using threading locks.  If you don't
                #you should jam your worker methods.
                if not builtin_queue_class.empty():
                    item = builtin_queue_class.get()
                    if item is None:
                        break
                    print(f"Consuming item {item}")
            time.sleep(2 * random.random())
        except queue.Empty:
            break

# We then create a queue, and a threading lock.
            
builtin_queue = queue.Queue()
threading_lock = threading.Lock()

# We create two threads targeting our consumer and producer
# and pass in our queue and lock.

thread1 = threading.Thread(
    target=self.item_producer_with_lock,
    args=(builtin_queue, threading_lock),
)
thread2 = threading.Thread(
    target=self.item_consumer_with_lock,
    args=(builtin_queue, threading_lock),
)

# We then start the threads in a concurrent configuration.

thread1.start()
thread2.start()

thread1.join()
# Remember to pass in the end of queue indicator.
builtin_queue.put(None)
thread2.join()
            
            """
        )

        builtin_queue = queue.Queue()
        threading_lock = threading.Lock()
        thread1 = threading.Thread(
            target=self.item_producer_with_lock,
            args=(builtin_queue, threading_lock),
        )
        thread2 = threading.Thread(
            target=self.item_consumer_with_lock,
            args=(builtin_queue, threading_lock),
        )

        thread1.start()
        thread2.start()

        thread1.join()
        builtin_queue.put(None)
        thread2.join()

        print(
            """This is a print satement that you should only see after the threads have finished their work."""
        )

    # def <> threading queue example with queue.join()
    def threading_queue_join_example(self):
        print("threading_queue_example")
        print(
            """ 
# This is a THREADING WITH QUEUE, with QUEUE.JOIN() example.
# Queue.join() blocks the main thread from exiting until all 
# the items in the queue have been processed by the worker 
# threads and their associated task_done() method has been called.
# Queue.join() should be called once, in the main thread, after all 
# worker threads have been started and before the program exits.

# First we create the producer and consumer threads.

def item_producer(self, builtin_queue_class):
    for i in range(10):
        time.sleep(1)
        print(f"Produced item {i}")
        builtin_queue_class.put(i)

def item_consumer_taskdone(self, builtin_queue_class):
    while True:
        try:
            time.sleep(2)
            item = builtin_queue_class.get()
            if item is None:
                ##If using queue.join() remember, NONE is still an item in the queue and you must call .task_done()
                builtin_queue_class.task_done()
                break
            print(f"Consuming item {item}")
            builtin_queue_class.task_done()
        except queue.Empty:
            break

# We create a queue
builtin_queue = queue.Queue()

# Then create threads targeting our producer and consumer and
# feedin our queue.

thread1 = threading.Thread(target=self.item_producer, args=(builtin_queue,))
thread2 = threading.Thread(
    target=self.item_consumer_taskdone, args=(builtin_queue,)
)

# We start the threads in a concurrent configuration.

thread1.start()
thread2.start()

# And call join on our queue.
builtin_queue.join()

thread1.join()
# Don't forget to indicate the end of the list by adding None to the end of the queue.
builtin_queue.put(None)
thread2.join()


            """
        )

        builtin_queue = queue.Queue()
        thread1 = threading.Thread(target=self.item_producer, args=(builtin_queue,))
        thread2 = threading.Thread(
            target=self.item_consumer_taskdone, args=(builtin_queue,)
        )

        thread1.start()
        thread2.start()

        builtin_queue.join()

        thread1.join()
        builtin_queue.put(None)
        thread2.join()

    ##------ Does dequeue work with threading? If so give an example
    def threading_using_a_deque(self):
        print("threading using a deque")
        print(
            """
# This is a THREADING example using DEQUE
# deque is thread safe and has some extra commands over queue.Queue
#
# For example,
#
#append(item) and appendleft(item):         add an item to the right or left side of the deque, respectively.
#pop() and popleft():                       remove and return an item from the right or left side of the deque, respectively.
#extend(iterable) and extendleft(iterable): extend the deque on the right or left side with the items from an iterable, respectively.
#rotate(n):                                 rotate the deque n steps to the right (positive n) or left (negative n).
#
# A deque queue does not have .join()

# First we create a producer and consumer,
            

def item_producer_with_deque(self, my_deque):
    for i in range(10):
        time.sleep(1)
        print(f"Produced item {i}")
        my_deque.append(i)

def item_consumer_with_deque(self, my_deque):
    while True:
        time.sleep(2)
        if my_deque:
            item = my_deque.popleft()
            if item is None:
                break
            print(f"Consuming item {item}")

# We create a deque Queue, 

my_deque = deque()

# Pass it to a couple of threads targeting our producer and consumer.

thread1 = threading.Thread(
    target=self.item_producer_with_deque, args=(my_deque,)
)
thread2 = threading.Thread(
    target=self.item_consumer_with_deque, args=(my_deque,)
)

# We start the threads in a concurrent configuration,

thread1.start()
thread2.start()

thread1.join()
# We then add None to the queue to indicate the end of the queue.
# Note, we do this after our process that adds tasks to the queue joins.
my_deque.append(None)
thread2.join()

        """
        )

        my_deque = deque()

        thread1 = threading.Thread(
            target=self.item_producer_with_deque, args=(my_deque,)
        )
        thread2 = threading.Thread(
            target=self.item_consumer_with_deque, args=(my_deque,)
        )

        thread1.start()
        thread2.start()

        thread1.join()
        my_deque.append(None)
        thread2.join()
        print(
            "This print statement is shown after the producer and consumer have joined allowing the main thread to exit."
        )
