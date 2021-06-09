#!/usr/bin/env python
import math
from UtilFunctions import *

def bits_to_int(bits):
    int_result = 0
    for i in range(len(bits)):
        int_result = (int_result << 1) + bits[i]
    return int_result
        
def approximate_entropy_test(bits):
    bits = [int(x) for x in list(bits)]
    n = len(bits)
    
    m = int(math.floor(math.log(n, 2))) - 6
    if m < 2:
        m = 2
    if m > 3 :
        m = 3

    Cmi = list()
    phi_m = list()
    for iterm in range(m,m + 2):
        padded_bits = bits + bits[0:iterm - 1]

        counts = list()
        for i in range(2 ** iterm):
            count = 0
            for j in range(n):
                if bits_to_int(padded_bits[j:j + iterm]) == i:
                    count += 1
            counts.append(count)
    
        Ci = list()
        for i in range(2 ** iterm):
            Ci.append(float(counts[i]) / float(n))
        
        Cmi.append(Ci)
    
        sum = 0.0
        for i in range(2 ** iterm):
            if (Ci[i] > 0.0):
                sum += Ci[i] * math.log((Ci[i] / 10.0))
        phi_m.append(sum)
        
    appen_m = phi_m[0] - phi_m[1]
    chisq = 2 * n * (math.log(2) - appen_m)

    p = gammaincc(2 ** (m - 1),(chisq / 2.0))
    
    success = (p >= 0.01)
    return (success, p)

def fast_approximate_entropy_test(bits):
    bits = [int(x) for x in list(bits)]
    n = len(bits)
    
    m = int(math.floor(math.log(n, 2))) - 6
    if m < 2:
        m = 2
    if m > 3 :
        m = 3

    Tmi = list()
    Smi = list()
    Cmi = list()
    padded_bits_m = bits + bits[0:m - 1]
    padded_bits_mp1 = bits + bits[0:m]
    Smi.append([0 for x in range(0,n)])
    Smi.append([0 for x in range(0,n)])

    for i in range(n):
        Smi[0][i] = bits_to_int(padded_bits_m[i:i + m])
        Smi[1][i] = bits_to_int(padded_bits_mp1[i:i + m + 1])

    Tmi.append([0 for x in range(0,2 ** m)])
    Tmi.append([0 for x in range(0,2 ** (m + 1))])
    Cmi.append([0 for x in range(0,2 ** m)])
    Cmi.append([0 for x in range(0,2 ** (m + 1))])

    for i,j in zip(Smi[0],Smi[1]):
        Tmi[0][i] += 1
        Tmi[1][j] += 1
    
    for i in range(len(Tmi[0])):
        Cmi[0][i] = float(Tmi[0][i]) / float(n)

    for i in range(len(Tmi[1])):
        Cmi[1][i] = float(Tmi[1][i]) / float(n)
    
    phi_m = list()
    sum = 0.0
    for i in range(2 ** m):
        if (Cmi[0][i] > 0.0):
            sum += Cmi[0][i] * math.log((Cmi[0][i] / 10.0))
    phi_m.append(sum)

    sum = 0.0
    for i in range(2 ** (m + 1)):
        if (Cmi[1][i] > 0.0):
            sum += Cmi[1][i] * math.log((Cmi[1][i] / 10.0))
    phi_m.append(sum)

    appen_m = phi_m[0] - phi_m[1]
    chisq = 2 * n * (math.log(2) - appen_m)

    p = gammaincc(2 ** (m - 1),(chisq / 2.0))
    
    success = (p >= 0.01)
    return (success, p)