"""Multiprocessing demonstration in Python 3

This is a short code snippet for demonstrating the multiprocessing module in python 3. It enables to run multiple
computations on multiple processor cores in parallel. Thus speeding up the process approximately by the factor of
number of cores.

In this example the compute(n) method runs a loop for 2 to the power of n times and returns the amount of time it took
to execute the method. The compute(n) method is called by multiprocessing_test() method to execute it using
multiprocessing module and running the code in parallel. The single_process_test() method executes the compute(n)
method in serial. Both tests are run in the main() method and does a comparison in the end.

This script also takes arguments. So check their declarations in the main section or call
python3 multiprocessing_demo.py -h
"""

import multiprocessing
import time
import argparse


def compute(n=26):
    """ Computes 2 to the power of n and returns elapsed time"""
    start = time.time()
    res = 0
    for i in range(2**n):
        res += 1
    end = time.time()
    dt = end - start
    print(f'Result {res} in {dt} seconds!')
    return dt


def multiprocessing_test(i, n):
    """
    Calls the compute() method i times and executes in parallel on multiple cores. In the end returns total executed
    time, as well as the time per method call and sum of all method calls.
    """
    start = time.time()
    pool = multiprocessing.Pool(processes=i)
    # total_time = pool.starmap(compute, [() for _ in range(i)])  # Can be used for no argument function
    total_time = pool.starmap(compute, ([(n,)]*i))
    end = time.time()
    dt = end - start
    return dt, sum(total_time), total_time


def single_process_test(i, n):
    """
    Calls the compute() method i times and executes serially on a single core. In the end returns total executed
    time, as well as the time per method call and sum of all method calls.
    """
    start = time.time()
    total_time = []
    for x in range(i):
        total_time.append(compute(n))
    end = time.time()
    dt = end - start
    return dt, sum(total_time), total_time


def main(args):
    i = args.instances
    n = args.loops
    ret_multi = multiprocessing_test(i, n)
    print(ret_multi)
    ret_single = single_process_test(i, n)
    print(f'Multiprocessing: {ret_multi}')
    print(f'Single core processing: {ret_single}')
    # print(ret_single)
    print(f'Difference {ret_single[0] - ret_multi[0]}')


if __name__ == '__main__':

    p = argparse.ArgumentParser()

    p.add_argument('-i', '--instances', type=int, help='number of computations', default=4)
    p.add_argument('-n', '--loops', type=int, help='2^n number of iterations per computation', default=26)

    args = p.parse_args()
    main(args)

