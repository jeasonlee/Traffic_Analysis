import numpy as np
import sympy
import random
from collections import Counter

# def encode(s):
#     try:
#         return ''.join(['{:08b}'.format(ord(c)) for c in s])
#     except:
#         try:
#             return ''.join(['{:08b}'.format(oct(c)) for c in s])
#         except:
#             return ''.join(['{:08b}'.format(c) for c in s])

def decode(s, N):
    dec = []
    for i in range(0, len(s), N):
        dec.append(int(s[i:i + N], 2))
    return dec

# def entropy_hu(s):
#     arr = decode(encode(s), 8)
#     N = len(arr)
#     ent = 0.0
#     arr_freq = dict(Counter(arr))
#     for w, ni in arr_freq.items():
#         p = float(ni / N)
#         ent -= p * np.log2(p)
#     return ent

def entropy(s):
    N = len(s)
    ent = 0.0
    arr_freq = dict(Counter(s))
    for w, ni in arr_freq.items():
        p = float(ni / N)
        ent -= p * np.log2(p)
    return ent

def entropyThreshold(len = 32 ,N = 8):
    # len 截断长度，字节
    # N 一字节八位，取值空间
    m = 2 ** N
    c = float(len / m)
    j = sympy.symbols("j", integer = True)
    fun = ((c ** (j-1)) / (sympy.factorial(j-1))) * sympy.log(j, 2)
    temp = sympy.summation(fun , (j, 1, sympy.oo))
    # print(temp)
    return float(sympy.log(m, 2) + sympy.log(c, 2) - (sympy.E ** (-c)) * temp)

def generate_random_range(len = 32):
    N = 8 # 一字节八位bit
    entr_arr = []
    random.seed()
    for n in range(0, 100000): # 生成100000个随机序列
        random_str = ''
        for i in range(len * N): # 32字节，32*8位bit
            random_str += str(random.randint(0, 1))
        # print(random_str)
        entr_arr.append(entropy(decode(random_str, N)))

    u = np.mean(entr_arr)
    v = np.std(entr_arr, ddof=1)
    low = u - 4*v
    high = u + 4*v
    return [low, high]

# def entr_thr_hu(Len, N):
#     m = 2 ** (N)
#     c = float(Len / m)
#     n = sympy.symbols("n", integer=True)
#     s = sympy.summation(- ((c ** (n - 1)) / (sympy.factorial(n - 1))) * (sympy.log(n) / sympy.log(2)), (n, 1, 1000))
#     ent = float(s.doit()) * math.exp((-c)) + np.log2(Len)
#     # print(ent)
#     return ent

# def entropy_list(s, interval=32, max_len=1504):
#     threshold = entropyThreshold(interval)
#     ret = []
#     for i in range(max_len - len(s)):
#         s += b'1'
#     for i in range(int(max_len / interval)):
#         # ret.append(np.abs(entropy(s[i * interval: (i + 1) * interval]) - threshold))
#         ret.append(np.abs(entropy(s[i * interval: (i + 1) * interval])))
#     return ret

def N_truncated_entropy_test(data, low, high):
    # [low, high] = generate_random_range()
    # print([low, high])

    data_value = [int(byte) for byte in data]
    N_truncated = []
    for i in range(0, len(data_value) - 32, 16):
        N_truncated.append(data_value[i:i + 32])
        # if i == len(data_value) -32:
        #     break
    # print(N_truncated)
    entropy_list = []
    for Nt in N_truncated:
        entropy_list.append(entropy(Nt))
    # print(entropy_list)
    u = np.mean(entropy_list)
    success = (u > low)
    # if u > low:
    #     # print("True")
    # else:
    #     # print("False")
    return (success, u)

# if __name__ == "__main__":
#     f = open('D:/tls/BA0-0007.pcap', 'rb')
#     # start = time.time()
#
#     print("-------")
#     # end = time.time()
#     # print((end-start))
#     # print(entropyThreshold(32))