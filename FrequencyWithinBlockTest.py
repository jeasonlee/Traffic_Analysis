#!/usr/bin/env python
import math
from fractions import Fraction
from UtilFunctions import *

#ones_table = [bin(i)[2:].count('1') for i in range(256)]
def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes,ones)


def frequency_within_block_test(bits):
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    # miniumum block size 20 bits, most blocks 100
    bits = [int(x) for x in list(bits)]
    n = len(bits)
    M = 20
    N = int(math.floor(n / M))
    if N > 99:
        N = 99
        M = int(math.floor(n / N))

    if len(bits) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return False, -1

    num_of_blocks = N
    block_size = M

    proportions = list()
    for i in range(num_of_blocks):
        block = bits[i * (block_size):((i + 1) * (block_size))]
        zeroes, ones = count_ones_zeroes(block)
        proportions.append(Fraction(ones, block_size))

    chisq = 0.0
    for prop in proportions:
        chisq += 4.0 * block_size * ((prop - Fraction(1, 2)) ** 2)

    p = gammaincc((num_of_blocks / 2.0), float(chisq) / 2.0)
    success = (p >= 0.01)
    return (success, p)