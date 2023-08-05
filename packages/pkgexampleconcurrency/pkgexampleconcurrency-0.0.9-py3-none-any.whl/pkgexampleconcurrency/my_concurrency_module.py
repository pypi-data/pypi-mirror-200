import argparse
from .mythreading import MyThreading
from .mymultiprocessing import MyMultiprocessing
from .myconcurrentfutures import MyThreadConcurrentfutures, MyProcessConcurrentfutures
from .myasyncio import MyAsyncio


def my_threading():
    my_threading_main_parser = argparse.ArgumentParser(
        description="Run default threading example"
    )
    my_threading_parser = my_threading_main_parser.add_mutually_exclusive_group()
    my_threading_parser.add_argument(
        "--thread-count",
        action="store_true",
        help="Max number of threads on your physical system",
    )
    my_threading_parser.add_argument(
        "--nd-concurrent",
        action="store_true",
        help="'Non daemon' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--nd-nj-concurrent",
        action="store_true",
        help="'Non daemon' 'non-join' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--nd-serial", action="store_true", help="'Non daemon' serial thread example."
    )
    my_threading_parser.add_argument(
        "--d-concurrent",
        action="store_true",
        help="'Daemon' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--d-nj-concurrent",
        action="store_true",
        help="'Daemon' 'non-join' concurrent thread example.",
    )
    my_threading_parser.add_argument(
        "--i-printalpha",
        action="store_true",
        help="Thread by inheritence example. Define own class that prints alphabet.",
    )
    my_threading_parser.add_argument(
        "--qexample",
        action="store_true",
        help="Threading queue example",
    )
    my_threading_parser.add_argument(
        "--qlexample",
        action="store_true",
        help="Threading queue with lock example",
    )
    my_threading_parser.add_argument(
        "--qjexample",
        action="store_true",
        help="Threading 'queue join' example",
    )
    my_threading_parser.add_argument(
        "--qdqexample",
        action="store_true",
        help="Threading with deque example",
    )

    my_args = my_threading_main_parser.parse_args()
    mythreadingexamples = MyThreading()
    if my_args.thread_count == True:
        mythreadingexamples.thread_count()
    if my_args.nd_concurrent == True:
        mythreadingexamples.non_daemon_concurrent_example()
    if my_args.nd_serial == True:
        mythreadingexamples.non_daemon_serial_example()
    if my_args.nd_nj_concurrent == True:
        mythreadingexamples.non_daemon_no_join_concurrent_example()
    if my_args.d_concurrent == True:
        mythreadingexamples.daemon_concurrent_example()
    if my_args.d_nj_concurrent == True:
        mythreadingexamples.daemon_no_join_concurrent_example()
    if my_args.i_printalpha == True:
        mythreadingexamples.print_alpha()
    if my_args.qexample == True:
        mythreadingexamples.threading_queue_example()
    if my_args.qlexample == True:
        mythreadingexamples.threading_queue_lock_example()
    if my_args.qjexample == True:
        mythreadingexamples.threading_queue_join_example()
    if my_args.qdqexample == True:
        mythreadingexamples.threading_using_a_deque()


def my_multiprocessing():
    my_main_multiprocessing_parser = argparse.ArgumentParser(
        description="Run default multiprocessing example"
    )
    my_multiprocessing_parser = (
        my_main_multiprocessing_parser.add_mutually_exclusive_group()
    )

    my_multiprocessing_parser.add_argument(
        "--cpu-count", action="store_true", help="What is your machine CPU count?"
    )
    my_multiprocessing_parser.add_argument(
        "--nd-concurrent",
        action="store_true",
        help="'Non Daemon' concurrent process example ",
    )
    my_multiprocessing_parser.add_argument(
        "--i-printalpha",
        action="store_true",
        help="Multiprocess by inheritence example. Define own class that prints alphabet.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolexample",
        action="store_true",
        help="Multiprocess by pool square example.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolcontextexample",
        action="store_true",
        help="Multiprocess by context pool square example.",
    )
    my_multiprocessing_parser.add_argument(
        "--poolcontextexampleadd",
        action="store_true",
        help="Multiprocess by context pool add example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qexample",
        action="store_true",
        help="Multiprocess with queue example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qlexample",
        action="store_true",
        help="Multiprocess with queue and a lock example.",
    )
    my_multiprocessing_parser.add_argument(
        "--qjexample",
        action="store_true",
        help="Multiprocess with joinable queue.",
    )
    my_multiprocessing_parser.add_argument(
        "--qdqexample",
        action="store_true",
        help="Multiprocess with a dequeue.",
    )
    my_multiprocessing_parser.add_argument(
        "--pipeexample",
        action="store_true",
        help="Multiprocess with a pipe example.",
    )

    my_args = my_main_multiprocessing_parser.parse_args()
    mymultiprocessingexamples = MyMultiprocessing()
    if my_args.cpu_count == True:
        mymultiprocessingexamples.count_cpu()
    if my_args.nd_concurrent == True:
        mymultiprocessingexamples.non_daemon_concurrent_example()
    if my_args.i_printalpha == True:
        mymultiprocessingexamples.print_alpha()
    if my_args.poolexample == True:
        mymultiprocessingexamples.pool_example_square()
    if my_args.poolcontextexample == True:
        mymultiprocessingexamples.pool_context_example_square()
    if my_args.poolcontextexampleadd == True:
        mymultiprocessingexamples.pool_context_example_add()
    if my_args.qexample == True:
        mymultiprocessingexamples.multiprocessing_queue_example()
    if my_args.qlexample == True:
        mymultiprocessingexamples.multiprocessing_queue_lock_example()
    if my_args.qjexample == True:
        mymultiprocessingexamples.multiprocessing_joinable_queue()
    if my_args.qdqexample == True:
        mymultiprocessingexamples.multiprocessing_using_a_dequeue()
    if my_args.pipeexample == True:
        mymultiprocessingexamples.pipe_example()


def my_concurrentfutures():
    my_main_concurrentfutures_parser = argparse.ArgumentParser(
        description="Run default concurrent futures example"
    )
    my_concurrentfutures_parser = (
        my_main_concurrentfutures_parser.add_mutually_exclusive_group()
    )

    my_concurrentfutures_parser.add_argument(
        "--tmap-ce",
        action="store_true",
        help="ThreadPoolExecutor map with corresponding elements",
    )
    my_concurrentfutures_parser.add_argument(
        "--tmap-tu", action="store_true", help="ThreadPoolExecutor map with tuples"
    )
    my_concurrentfutures_parser.add_argument(
        "--tsubmit", action="store_true", help="ThreadPoolExecutor submit example"
    )
    my_concurrentfutures_parser.add_argument(
        "--tresult", action="store_true", help="ThreadPoolExecutor result usage example"
    )
    my_concurrentfutures_parser.add_argument(
        "--tascomplete",
        action="store_true",
        help="ThreadPoolExecutor ascomplete example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tdone",
        action="store_true",
        help="ThreadPoolExecutor done example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tcallback",
        action="store_true",
        help="ThreadPoolExecutor callback example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tshutdown-true",
        action="store_true",
        help="ThreadPoolExecutor shutdown example wait true",
    )
    my_concurrentfutures_parser.add_argument(
        "--tshutdown-false",
        action="store_true",
        help="ThreadPoolExecutor shutdown example wait false",
    )
    my_concurrentfutures_parser.add_argument(
        "--tcancel",
        action="store_true",
        help="ThreadPoolExecutor cancel example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tcancel-ec",
        action="store_true",
        help="ThreadPoolExecutor cancel with thread event_check example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tqueueeg",
        action="store_true",
        help="ThreadPoolExecutor queue.queue() queue example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tlqueueeg",
        action="store_true",
        help="ThreadPoolExecutor queue.queue() queue example with lock",
    )
    my_concurrentfutures_parser.add_argument(
        "--tdequeueeg",
        action="store_true",
        help="ThreadPoolExecutor collections.dequeue() example",
    )
    my_concurrentfutures_parser.add_argument(
        "--tldequeueeg",
        action="store_true",
        help="ThreadPoolExecutor collections.dequeue() example with lock",
    )
    ###
    my_concurrentfutures_parser.add_argument(
        "--pmap-ce",
        action="store_true",
        help="ProcessPoolExecutor map with corresponding elements",
    )
    my_concurrentfutures_parser.add_argument(
        "--pmap-tu", action="store_true", help="ProcessPoolExecutor map with tuples"
    )
    my_concurrentfutures_parser.add_argument(
        "--psubmit", action="store_true", help="ProcessPoolExecutor submit example"
    )
    my_concurrentfutures_parser.add_argument(
        "--presult",
        action="store_true",
        help="ProcessPoolExecutor result usage example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pascomplete",
        action="store_true",
        help="ProcessPoolExecutor ascomplete example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pdone",
        action="store_true",
        help="ProcessPoolExecutor done example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pcallback",
        action="store_true",
        help="ProcessPoolExecutor callback example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pshutdown-true",
        action="store_true",
        help="ProcessPoolExecutor shutdown example wait true",
    )
    my_concurrentfutures_parser.add_argument(
        "--pshutdown-false",
        action="store_true",
        help="ProcessPoolExecutor shutdown example wait false",
    )
    my_concurrentfutures_parser.add_argument(
        "--pcancel",
        action="store_true",
        help="ProcessPoolExecutor cancel example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pcancel-ec",
        action="store_true",
        help="ProcessPoolExecutor cancel with thread event_check example",
    )
    my_concurrentfutures_parser.add_argument(
        "--pqueue",
        action="store_true",
        help="ProcessPoolExecutor multiprocessing.Queue() queue example",
    )
    my_concurrentfutures_parser.add_argument(
        "--ppipeexample",
        action="store_true",
        help="ProcessPoolExecutor pipe example",
    )

    my_args = my_main_concurrentfutures_parser.parse_args()
    mythreadfuturesexamples = MyThreadConcurrentfutures()
    myprocessfuturesexamples = MyProcessConcurrentfutures()

    if my_args.tmap_ce == True:
        mythreadfuturesexamples.map_corresponding()
    if my_args.tmap_tu == True:
        mythreadfuturesexamples.map_tuples()
    if my_args.tsubmit == True:
        mythreadfuturesexamples.submit_example()
    if my_args.tresult == True:
        mythreadfuturesexamples.result_example()
    if my_args.tascomplete == True:
        mythreadfuturesexamples.as_complete_example()
    if my_args.tdone == True:
        mythreadfuturesexamples.done_example()
    if my_args.tcallback == True:
        mythreadfuturesexamples.callback_example()
    if my_args.tshutdown_true == True:
        mythreadfuturesexamples.shutdown_wait_true_example()
    if my_args.tshutdown_false == True:
        mythreadfuturesexamples.shutdown_wait_false_example()
    if my_args.tcancel == True:
        mythreadfuturesexamples.cancel_example()
    if my_args.tcancel_ec == True:
        mythreadfuturesexamples.cancel_example_with_event()
    if my_args.tqueueeg == True:
        mythreadfuturesexamples.queue_example()
    if my_args.tlqueueeg == True:
        mythreadfuturesexamples.ldqueue_example()
    if my_args.tdequeueeg == True:
        mythreadfuturesexamples.dqueue_example()
    if my_args.tldequeueeg == True:
        mythreadfuturesexamples.ldqueue_example()
    ##
    if my_args.pmap_ce == True:
        myprocessfuturesexamples.map_corresponding()
    if my_args.pmap_tu == True:
        myprocessfuturesexamples.map_tuples()
    if my_args.psubmit == True:
        myprocessfuturesexamples.submit_example()
    if my_args.presult == True:
        myprocessfuturesexamples.result_example()
    if my_args.pascomplete == True:
        myprocessfuturesexamples.as_complete_example()
    if my_args.pdone == True:
        myprocessfuturesexamples.done_examaple()
    if my_args.pcallback == True:
        myprocessfuturesexamples.callback_example()
    if my_args.pshutdown_true == True:
        myprocessfuturesexamples.shutdown_wait_true_example()
    if my_args.pshutdown_false == True:
        myprocessfuturesexamples.shutdown_wait_false_example()
    if my_args.pcancel == True:
        myprocessfuturesexamples.cancel_example()
    if my_args.pcancel_ec == True:
        myprocessfuturesexamples.cancel_example_with_event()
    if my_args.pqueue == True:
        myprocessfuturesexamples.queue_example()
    if my_args.ppipeexample == True:
        myprocessfuturesexamples.pipe_example()


def my_asyncio():
    myasyncioexamples = MyAsyncio()
    my_asyncio_parser = argparse.ArgumentParser(
        description="Run default asyncio example"
    )
    my_asyncio_parser.add_argument(
        "--helloio", action="store_true", help="async/await hello world!"
    )
    my_asyncio_parser.add_argument(
        "--gather", action="store_true", help="gather together async functions"
    )
    my_asyncio_parser.add_argument(
        "--generator",
        action="store_true",
        help="generator example, yeild turns a function in to a generator",
    )
    my_asyncio_parser.add_argument(
        "--sleep",
        action="store_true",
        help="sleep example,",
    )
    my_asyncio_parser.add_argument(
        "--tothread",
        action="store_true",
        help="to_thread example,",
    )
    my_asyncio_parser.add_argument(
        "--createtask",
        action="store_true",
        help="createtask example,",
    )
    my_asyncio_parser.add_argument(
        "--wait",
        action="store_true",
        help="wait examples,",
    )
    my_asyncio_parser.add_argument(
        "--ascomplete",
        action="store_true",
        help="as_complete example,",
    )
    my_asyncio_parser.add_argument(
        "--lock",
        action="store_true",
        help="lock example, syncronization primative",
    )
    my_asyncio_parser.add_argument(
        "--event",
        action="store_true",
        help="event example, syncronization primative",
    )
    my_asyncio_parser.add_argument(
        "--condition",
        action="store_true",
        help="condition example, syncronization primative",
    )
    my_asyncio_parser.add_argument(
        "--semaphore",
        action="store_true",
        help="semaphore example",
    )
    my_asyncio_parser.add_argument(
        "--queue",
        action="store_true",
        help="queue example",
    )
    my_asyncio_parser.add_argument(
        "--queuel",
        action="store_true",
        help="queue example with lock",
    )
    my_asyncio_parser.add_argument(
        "--queuec",
        action="store_true",
        help="queue example with condition",
    )

    my_args = my_asyncio_parser.parse_args()

    if my_args.helloio == True:
        myasyncioexamples.helloio()

    if my_args.gather == True:
        myasyncioexamples.gather_example()

    if my_args.generator == True:
        myasyncioexamples.yeild_and_generators()

    if my_args.sleep == True:
        myasyncioexamples.sleep_example()

    if my_args.tothread == True:
        myasyncioexamples.to_thread_example()

    if my_args.createtask == True:
        myasyncioexamples.create_task_example()

    if my_args.wait == True:
        myasyncioexamples.wait_examples()

    if my_args.ascomplete == True:
        myasyncioexamples.as_complete_example()

    if my_args.lock == True:
        myasyncioexamples.lock_example()

    if my_args.event == True:
        myasyncioexamples.event_example()

    if my_args.condition == True:
        myasyncioexamples.conditions_examples()

    if my_args.semaphore == True:
        myasyncioexamples.semaphore_example()

    if my_args.queue == True:
        myasyncioexamples.queue_example()

    if my_args.queuel == True:
        myasyncioexamples.queuel_example()

    if my_args.queuec == True:
        myasyncioexamples.queuec_example()
