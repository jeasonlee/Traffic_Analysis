#!/usr/bin/env python
import math
from UtilFunctions import *

def int2patt(n, m):
    pattern = list()
    for i in range(m):
        pattern.append((n >> i) & 1)
    return pattern

def countpattern(patt, bits, n):
    thecount = 0
    for i in range(n):
        match = True
        for j in range(len(patt)):
            if patt[j] != bits[i + j]:
                match = False
        if match:
            thecount += 1
    return thecount

def psi_sq_mv1(m, n, padded_bits):
    counts = [0 for i in range(2 ** m)]
    for i in range(2 ** m):
        pattern = int2patt(i, m)
        count = countpattern(pattern, padded_bits, n)
        counts.append(count)

    psi_sq_m = 0.0
    for count in counts:
        psi_sq_m += (count ** 2)
    psi_sq_m = psi_sq_m * (2 ** m) / n
    psi_sq_m -= n
    return psi_sq_m

def serial_test(bits, patternlen=None):
    bits = [int(x) for x in list(bits)]
    n = len(bits)
    if patternlen != None:
        m = patternlen
    else:
        m = int(math.floor(math.log(n, 2))) - 2

        if m < 4:
            print("Error. Not enough data for m to be 4")
            return False, 0, None
        m = 4

    # Step 1
    padded_bits = bits + bits[0:m - 1]

    # Step 2
    psi_sq_m = psi_sq_mv1(m, n, padded_bits)
    psi_sq_mm1 = psi_sq_mv1(m - 1, n, padded_bits)
    psi_sq_mm2 = psi_sq_mv1(m - 2, n, padded_bits)

    delta1 = psi_sq_m - psi_sq_mm1
    delta2 = psi_sq_m - (2 * psi_sq_mm1) + psi_sq_mm2

    P1 = gammaincc(2 ** (m - 2), delta1 / 2.0)
    P2 = gammaincc(2 ** (m - 3), delta2 / 2.0)

    # print("  psi_sq_m   = ", psi_sq_m)
    # print("  psi_sq_mm1 = ", psi_sq_mm1)
    # print("  psi_sq_mm2 = ", psi_sq_mm2)
    # print("  delta1     = ", delta1)
    # print("  delta2     = ", delta2)
    # print("  P1         = ", P1)
    # print("  P2         = ", P2)

    success = (P1 >= 0.01) and (P2 >= 0.01)
    return (success, [P1, P2])
