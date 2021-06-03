import numpy as np
import os
import dpkt
import random
from collections import Counter

def encode(s):
    try:
        return ''.join(['{:08b}'.format(ord(c)) for c in s])
    except:
        try:
            return ''.join(['{:08b}'.format(oct(c)) for c in s])
        except:
            return ''.join(['{:08b}'.format(c) for c in s])

def decode(s, N):
    dec = []
    for i in range(0, len(s), N):
        dec.append(int(s[i:i + N], 2))
    return dec

def entropy(s):
    arr = decode(encode(s), 8)
    N = len(arr)
    ent = 0.0
    arr_freq = dict(Counter(arr))
    for w, ni in arr_freq.items():
        p = float(ni / N)
        ent -= p * np.log2(p)
    return ent

def entropy1(s):
    N = len(s)
    ent = 0.0
    arr_freq = dict(Counter(s))
    for w, ni in arr_freq.items():
        p = float(ni / N)
        ent -= p * np.log2(p)
    return ent

def entropyThreshold(N, gigantic=100):
    m = 256
    c = float(N / m)
    factorial = 1.0
    tmp = 0
    for j in range(1, gigantic):
        factorial = factorial * j
        tmp += np.power(c, j) / factorial * np.log2(j + 1)
    return np.log2(m) + np.log2(c) - tmp * np.exp(-c)

def entropy_list(s, interval=32, max_len=1504):
    threshold = entropyThreshold(interval)
    ret = []
    for i in range(max_len - len(s)):
        s += b'1'
    for i in range(int(max_len / interval)):
        # ret.append(np.abs(entropy(s[i * interval: (i + 1) * interval]) - threshold))
        ret.append(np.abs(entropy(s[i * interval: (i + 1) * interval])))
    return ret

def N_truncated_entropy_test():
    return

if __name__ == "__main__":
    f = open('D:/tls/BA0-0007.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    for ts, buf in pcap:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        tcp = ip.data
        data = tcp.data

        if len(data) != 0:
            data_value = [int(byte) for byte in data]
            print(data_value)
            N_truncated = []
            # data = decode(encode(data), 8)
            # print(data)
            for i in range(0, len(data_value), 4):
                if len(data_value[i:i+32]) == 32:
                    N_truncated.append(data_value[i:i+32])
                if i == len(data_value) -32:
                    break
            print(N_truncated)
            entropy_list = []
            for Nt in N_truncated:
                entropy_list.append(entropy1(Nt))
            print(entropy_list)
            # el = []
            # for li in N_truncated:
            #     el.append(entropy1(li))
            # # print(el)
            # print(entropy_list(data))