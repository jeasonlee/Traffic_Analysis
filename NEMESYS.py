import dpkt
import os
from math import log

def calculate(a, b):
    def a2b(num):
        bit = list(bin(num)[2:])
        if len(bit) != 8:
            tem = 8 - len(bit)
            while tem > 0:
                bit.insert(0, '0')
                tem -= 1
            return bit
        else:
            return bit

    byte_a = a2b(a)
    byte_b = a2b(b)

    same_num = 0
    for i in range(0, 8):
        if byte_a[i] == byte_b[i]:
            same_num += 1
        else:
            continue
    return same_num/8

datapath = './result/'
file_name_list = os.listdir(datapath)
for file_name in file_name_list:
    try:
        f = open(os.path.join(datapath, file_name), 'rb')
        pcap = dpkt.pcap.Reader(f)

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            data = tcp.data
            # print(data)

            BC = []
            for j in range(0, len(data)-1):
                BC.append(calculate(data[j], data[j+1]))
            print(BC)

            deltaBC = []
            for j in range(0, len(BC)-1):
                deltaBC.append((BC[j+1] - BC[j]))
            print(deltaBC)

            vote = [0]*len(data)
            for j in range(len(deltaBC)-1):
                if j == 0:
                    vote[j] += 1
                elif deltaBC[j] < deltaBC[j-1] and deltaBC[j] < deltaBC[j+1]:
                    vote[j+1] += 1

            # j = 0
            # temp_data = b''
            # while j < len(data):
            #     if vote[j] == 1 and data[j] == 32:
            #         temp_data += b'^'
            #     else:
            #         temp_data += chr(data[j]).encode()
            #     j += 1

            # delimiters = [' ', ':', '\r', '\n']
            # for j in range(len(data)):
            #     if chr(data[j]) in delimiters:
            #         vote[j] += 3

            print(data)
            print(vote)
    except Exception as exception:
        print("\n[error] Process break abnormally.")
        print(exception)
        break