#!/usr/bin/env python
import math

def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes, ones)

def monobit_test(bits):
    bits = [int(x) for x in list(bits)]
    n = len(bits)

    zeroes, ones = count_ones_zeroes(bits)
    s = abs(ones - zeroes)
    # print("  Ones count   = %d" % ones)
    # print("  Zeroes count = %d" % zeroes)

    p = math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0)))

    success = (p >= 0.01)
    return (success, p)