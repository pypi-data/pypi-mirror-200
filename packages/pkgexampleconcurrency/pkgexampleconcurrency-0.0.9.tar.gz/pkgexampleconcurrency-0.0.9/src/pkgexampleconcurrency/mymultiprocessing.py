import multiprocessing
from multiprocessing import Pool
from collections import deque
import random
import time


class OutputAlpha(multiprocessing.Process):
    def __init__(self, daemon: bool, sleeptime: int):
        multiprocessing.Process.__init__(self)
        self.sleeptime = sleeptime
        self.daemon = daemon

    def run(self):
        for char in "abcdefg":
            time.sleep(self.sleeptime)
            print(char)


class MyMultiprocessing:
    def __init__(self):
        pass

    def count_cpu(self):
        cpu_count = multiprocessing.cpu_count()
        print("CPU Count : ", cpu_count)
        print(
            f"""If you at anypoint use the concurrent futures module,
This would be your maxium number of concurrent workers.

    ProcessPoolExecutor(max_workers={cpu_count})
    
Of course, you could double the number, but half of your processes 
won't be executing concurrently and the job will take twice the time"""
        )

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

    def square_number(self, x):
        return x**2

    def add_numbers(self, args):
        x, y = args
        return x + y

    def item_producer(self, my_multiprocessing_queue):
        for i in range(0, 5):
            print(f"Produce item {i}")
            my_multiprocessing_queue.put(i)
            time.sleep(random.random())

    def item_consumer(self, my_multiprocessing_queue):
        while True:
            item = my_multiprocessing_queue.get()
            if item is None:
                break
            print(f"Item found {item}")
            time.sleep(2 * random.random())

    def item_producer_with_lock(
        self, my_multiprocessing_queue, my_multiprocessing_lock
    ):
        for i in range(10):
            time.sleep(random.random())
            with my_multiprocessing_lock:
                my_multiprocessing_queue.put(i)
                print(f"Produced {i}")

        # We ad an indicator value of None to mark the end of the queue stream.
        with my_multiprocessing_lock:
            my_multiprocessing_queue.put(None)

        # You can also capture locks without using it in a context statement
        # by manually aquireing and releasing a lock.
        #
        # my_multiprocessing_lock.acquire()
        #
        # {Do stuff here.}
        #
        # my_multiprocessing_lock.release()

    def item_consumer_with_lock(
        self, my_multiprocessing_queue, my_multiprocessing_lock
    ):
        while True:
            with my_multiprocessing_lock:
                if not my_multiprocessing_queue.empty():
                    item = my_multiprocessing_queue.get()
                    if item is None:
                        # End of queued items
                        break
                    print(f"Consumed {item}")

            time.sleep(2 * random.random())

    def item_consumer_taskdone(self, my_multiprocessing_queue):
        # We actually pass in a joinable queue, let's assign it a different name.
        my_multiprocessing_joinable_queue = my_multiprocessing_queue
        while True:
            try:
                item = my_multiprocessing_joinable_queue.get()
                if item is None:
                    ##If using multiprocessing_joinable_queue.join() remember, NONE is still an item in the queue and you must call .task_done()
                    my_multiprocessing_joinable_queue.task_done()
                    break
                print(f"Consuming item {item}")
                my_multiprocessing_joinable_queue.task_done()
            except my_multiprocessing_joinable_queue.Empty:
                break
            time.sleep(2 * random.random())

    def non_daemon_concurrent_example(self):
        print(
            """The non-daemon and daemon, concurrent and serial configurations 
covered in the 'threading' module examples also apply to processes in 'multiprocessing' module.

This is the only configuration I will reproduce just to show you how it is done.

Here the main process stays alive until all non-daemon processes finish their tasks.

The processes are distributed between your processor cores.  The multiprocessor module
takes care of the scheduling

"""
        )
        print(
            """

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

    process1 = multiprocessing.Process(daemon=False, target=self.print_evens)
    process2 = multiprocessing.Process(daemon=False, target=self.print_odds)

    process1.start()
    process2.start()

    process1.join()
    process2.join()

          """
        )

        process1 = multiprocessing.Process(daemon=False, target=self.print_evens)
        process2 = multiprocessing.Process(daemon=False, target=self.print_odds)

        process1.start()
        process2.start()

        process1.join()
        process2.join()

    def print_alpha(self):
        print(
            """#We define a class that inherits the multiprocessing base class,

class OutputAlpha(multiprocessing.Process):

     #Notice we have to overide the base constructor if we want to
     #pass in our own variables.
    def __init__(self, daemon: bool, sleeptime: int):
        multiprocessing.Process.__init__(self)
        self.sleeptime = sleeptime
        self.daemon = daemon

     #We overide the run() method to carry out a task of our choice.
    def run(self):
        for char in "abcdefg":
            time.sleep(self.sleeptime)
            print(char)

     #and then call it from within another class method,

class MyMultiprocessing:
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

We ran our multiprocessing.Process class as a daemon thread class with joins,
so the main process waited for the worker process to finish. """
        )

    def pool_example_square(self):
        print(
            """ 
    from multiprocessing import Pool

    def square_number(self, x):
        return x**2

    pool = Pool(processes=4)

    inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    results = pool.map(self.square_number, inputs)

    pool.close()
    pool.join()
        """
        )
        pool = Pool(processes=4)

        inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        results = pool.map(self.square_number, inputs)

        pool.close()
        pool.join()

        print(results)

    def pool_context_example_square(self):
        print(
            """ 
    from multiprocessing import Pool

    def square_number(self, x):
        return x**2

    with Pool(processes=4) as pool:
        inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        results = pool.map(self.square_number, inputs)
    print(results)

        """
        )
        with Pool(processes=4) as pool:
            inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            results = pool.map(self.square_number, inputs)
        print(results)

    def pool_context_example_add(self):
        print(
            """ 
    def add_numbers(self, args):
        x, y = args
        return x + y

    with Pool(processes=4) as pool:
        inputs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
        results = pool.map(self.add_numbers, inputs)
    print(results)

        """
        )
        with Pool(processes=4) as pool:
            inputs = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)]
            results = pool.map(self.add_numbers, inputs)
        print(results)

    # def <>  multiprocessing queue example using multiprocessing.Queue

    def multiprocessing_queue_example(self):

        print(
            """
#This is an example of multi processing using the multiprocessing module
#and the multiprocessing.Queue class. This is a specific queue class 
#designed for multiprocessing.

#We create an item producer, and an item consumer,

def item_producer(self, my_multiprocessing_queue):
    for i in range(0, 5):
        print(f"Produce item {i}")
        my_multiprocessing_queue.put(i)
        time.sleep(random.random())

def item_consumer(my_multiprocessing_queue):
    while True:
        item = my_multiprocessing_queue.get()
        if item is None:
            break
        print(f"Item found {item}")
        time.sleep(2 * random.random())

#We then create a multiprocessing queue
my_mp_queue = multiprocessing.Queue()

#Then feed this queue to the item producer
#and consumer.

process1 = multiprocessing.Process(
    target=self.item_producer, args=(my_mp_queue,)
)
process2 = multiprocessing.Process(
    target=self.item_consumer, args=(my_mp_queue,)
)

#And start the processes

process1.start()
process2.start()
process1.join()

# Just before we "join()" the process that comsumes the queue
# we use 'None' as an indicator to stop our item_consumer
# process (as we have implemented it that way).
# This allowed the main thread to exit as it's waiting 
# for the multiprocess to finish.
# At this point 'None' is placed at the end of the queue
# after all items

my_mp_queue.put(None)
process2.join()

#These processes will run concurently, and you
#should see the queue is filled, then emptied,
#then printed to the screen.
"""
        )

        my_mp_queue = multiprocessing.Queue()

        process1 = multiprocessing.Process(
            target=self.item_producer, args=(my_mp_queue,)
        )
        process2 = multiprocessing.Process(
            target=self.item_consumer, args=(my_mp_queue,)
        )

        process1.start()
        process2.start()
        process1.join()
        my_mp_queue.put(None)
        process2.join()

    # def <>  multiprocessing queue example using multiprocessing.Queue, and lock

    def multiprocessing_queue_lock_example(self):
        print(
            """

#This is an example of multi processing using the multiprocessing module
#and the multiprocessing.Queue() class with multiprocessing.Lock() class. 
#This is a specific queue and lock class designed for multiprocessing.

#This example has one queue, and one lock.
#The producer and consumer methods lock and unlock a multiprocessing.Lock()
#and control who has access to the queue.

#You can have more than one lock controling access to more than one shared resource.

def item_producer_with_lock(self, my_multiprocessing_queue, my_multiprocessing_lock):
    for i in range(10):
        time.sleep(random.random())
            with my_multiprocessing_lock:
                my_multiprocessing_queue.put(i)
                print(f"Produced {i}")

        # We add an indicator value of None to mark the end of the queue stream.
        with my_multiprocessing_lock:
            my_multiprocessing_queue.put(None)

def item_consumer_with_lock(self, my_multiprocessing_queue, my_multiprocessing_lock):
    while True:
        with my_multiprocessing_lock:
            if not my_multiprocessing_queue.empty():
                item = my_multiprocessing_queue.get()
                if item is None:
                    # End of queued items
                    break
                print(f"Consumed {item}")
            time.sleep(2 * random.random())

# We create a multiprocessing queue and lock

my_multiprocessing_queue = multiprocessing.Queue()
my_multiprocessing_lock = multiprocessing.Lock()

# We then create two processes targeting the producer
# and consumer. We pass in the shared resource, in
# this case the queue, and the lock controling access to
# that resource.

process1 = multiprocessing.Process(
    target=self.item_producer_with_lock,
    args=(my_multiprocessing_queue, my_multiprocessing_lock),
        )
process2 = multiprocessing.Process(
    target=self.item_consumer_with_lock,
    args=(my_multiprocessing_queue, my_multiprocessing_lock),
        )

# Notice the following configuration of .start() and .join()
# is the concurrent config.

process1.start()
process2.start()

process1.join()
process2.join()

# The random sleep timer in each process will create
# a random output of Consumed and Produced statements.


            """
        )
        my_multiprocessing_queue = multiprocessing.Queue()
        my_multiprocessing_lock = multiprocessing.Lock()

        process1 = multiprocessing.Process(
            target=self.item_producer_with_lock,
            args=(my_multiprocessing_queue, my_multiprocessing_lock),
        )
        process2 = multiprocessing.Process(
            target=self.item_consumer_with_lock,
            args=(my_multiprocessing_queue, my_multiprocessing_lock),
        )

        process1.start()
        process2.start()

        process1.join()
        process2.join()

    # def <> multiprocessing queue example with multiprocessing.JoinableQueue.join()

    def multiprocessing_joinable_queue(self):
        print(
            """ 
# This is a MULTIPROCESSING WITH QUEUE, with JOINABLE QUEUE example.
# JoinableQueue.join() blocks the main process from exiting until all 
# the items in the queue have been processed by the worker 
# processes and their associated task_done() method has been called.
# JoinableQueue.join() should be called once, in the main thread, after all 
# worker processes have been started and before the program exits.

def item_producer(self, my_multiprocessing_queue):
    for i in range(0, 5):
        print(f"Produce item {i}")
        my_multiprocessing_queue.put(i)
        time.sleep(random.random())

def item_consumer_taskdone(self, my_multiprocessing_queue):
    # We actually pass in a joinable queue, let's assign it a different name.
    my_multiprocessing_joinable_queue = my_multiprocessing_queue
    while True:
        try:
            item = my_multiprocessing_joinable_queue.get()
            if item is None:
                ##If using multiprocessing_joinable_queue.join() remember, NONE is still an item in the queue and you must call .task_done()
                my_multiprocessing_joinable_queue.task_done()
                break
            print(f"Consuming item {item}")
            my_multiprocessing_joinable_queue.task_done()
        except my_multiprocessing_joinable_queue.Empty:
            break
        time.sleep(2 * random.random())

# We create a joinable queue.
my_multiprocessing_joinable_queue = multiprocessing.JoinableQueue()

# Pass the joinable queue into our producer and consumer processes,

process1 = multiprocessing.Process(
    target=self.item_producer,
    args=(my_multiprocessing_joinable_queue,),
)
process2 = multiprocessing.Process(
    target=self.item_consumer_taskdone,
    args=(my_multiprocessing_joinable_queue,),
)

# We start the processes in a concurrent formation.

process1.start()
process2.start()

# We call join on our joinable queue.
my_multiprocessing_joinable_queue.join()

process1.join()
# We place the NONE item as an indicator that it is the end of the queue.
my_multiprocessing_joinable_queue.put(None)
# If you want to call join_thread() on the queue later,
# you must formally close the queue by calling .close()
my_multiprocessing_joinable_queue.close()
process2.join()

# Call join_thread to not only wait for the queue to be empty,
# but also wait for processes to finish processing the items.
# This is optional, but depends on your design. Ideally, you 
# would think that your would want each item in a queue to be processed.
my_multiprocessing_joinable_queue.join_thread()

#Note, calling .join() on processes processing a joinable queue that has
#join_thread() called would be redundant as join_thread() will call
#.join() on all processes for you.  (Not the case when processing a non-joinable queue)

        """
        )

        my_multiprocessing_joinable_queue = multiprocessing.JoinableQueue()

        process1 = multiprocessing.Process(
            target=self.item_producer,
            args=(my_multiprocessing_joinable_queue,),
        )
        process2 = multiprocessing.Process(
            target=self.item_consumer_taskdone,
            args=(my_multiprocessing_joinable_queue,),
        )

        process1.start()
        process2.start()

        my_multiprocessing_joinable_queue.join()

        process1.join()
        my_multiprocessing_joinable_queue.put(None)
        my_multiprocessing_joinable_queue.close()
        process2.join()

        my_multiprocessing_joinable_queue.join_thread()

        print(
            """
You should see this printout once all processes and queue have joined, the main process should exit straight after this message.

The difference between join_thread() and join() for a multiprocessing JoinableQueue 
is that join_thread() is used to wait for the worker threads to finish, while join() 
is used to wait for all items in the queue to be processed.

When you call join_thread(), the main process will wait for all worker processes to 
complete their work and terminate.  Specifically, it waits for the worker processes 
to call task_done() on the queue for every item they get from the queue, and then it 
calls join() on each worker process to wait for them to finish. This ensures that 
all the data in the queue has been processed by the worker processes.

On the other hand, when you call join(), the main process will wait until all items 
in the queue have been processed, but it does not wait for the worker processes to 
terminate. This means that if there are any worker processes that have not completed 
their work yet, the main process will still exit, and those worker processes will 
continue to run in the background.

In short, join_thread() waits for worker processes to finish, while join() only waits 
for the queue to be empty.
"""
        )

    ##------ Does dequeue work with multiuprocessing? If so give an example
    def multiprocessing_using_a_dequeue(self):
        print(
            """ 
Unfortunately multiprocessing DOES NOT support deque.

If you want to share objects between processes
Look in to https://docs.python.org/3/library/multiprocessing.html#managers

A manager returned by Manager() will support types list, dict, Namespace, 
Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, 
Value and Array. 

If you need a queue, stick with multiprocessing.Queue() and 
multiprocessing.JoinableQueue()


            """
        )

    def sender(self, conn):
        conn.send("Hello from sender!")
        conn.close()

    def receiver(self, conn):
        message = conn.recv()
        conn.close()
        print(f"Received message: {message}")

    def pipe_example(self):
        parent_conn, child_conn = multiprocessing.Pipe()
        p1 = multiprocessing.Process(target=self.sender, args=(child_conn,))
        p2 = multiprocessing.Process(target=self.receiver, args=(parent_conn,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        print(
            """
    def sender(self,conn):
        conn.send("Hello from sender!")
        conn.close()

    def receiver(self,conn):
        message = conn.recv()
        conn.close()
        print(f"Received message: {message}")

    def pipe_example(self):
        parent_conn, child_conn = multiprocessing.Pipe()
        p1 = multiprocessing.Process(target=self.sender, args=(child_conn,))
        p2 = multiprocessing.Process(target=self.receiver, args=(parent_conn,))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        # Both the parent and child processes can use the send and recv methods 
        # to send and receive data through the connection objects. The choice of 
        # which end of the pipe to use for sending and which to use for receiving 
        # is up to the specific implementation of the communication protocol.
        
                              """
        )
