#!/usr/bin/env python
import dpkt
import os
import time
import CumulativeSumsTest as CuST
import NTruncatedEntropyTest as NTEn
import ApproximateEntropyTest as ApEn
import FrequencyWithinBlockTest as FrWB
# import LinearComplexityTest as LiCT
# import BinaryMatrixRankTest as BMRT
# import RandomExcursionVariantTest as REVT
# import OverlappingTemplateMatchingTest as OTMT
import MonobitTest as MbT

# 第0字节
RECORD_TYPES = {
    0x14: "TLS_ChangeCipherSpec", # 20
    0x15: "TLS_Alert", # 21
    0x16: "TLS_Handshake",# 22
    0x17: "TLS_ApplicationData",# 23
}
# 第1、2字节
TLS_VERSION = {
    '0300': "SSL3",
    '0301': "TLS 1.0",
    '0302': "TLS 1.1",
    '0303': "TLS 1.2",
    '0304': "TLS 1.3"
}
# 第3、4字节为后续字节个数
# 第5字节
HANDSHAKE_TYPES = {
    0: 'HelloRequest',
    1: 'ClientHello',
    2: 'ServerHello',
    11: 'Certificate',
    12: 'ServerKeyExchange',
    13: 'CertificateRequest',
    14: 'ServerHelloDone',
    15: 'CertificateVerify',
    16: 'ClientKeyExchange',
    20: 'Finished',
}

def tls_detection(data):
    if data[0] in RECORD_TYPES.keys(): #data[0]字节ASCII编码
        print(RECORD_TYPES.get(data[0]) + '/ ', end='')
        if data[1:3].hex() in TLS_VERSION.keys(): #data[1:3].hex()转换为十六进制字符串
            print(TLS_VERSION.get(data[1:3].hex()) + '/ ', end='')
            if data[5] in HANDSHAKE_TYPES.keys() and data[0] != 23:
                print(HANDSHAKE_TYPES.get(data[5]) + '/ ', end='')
            return True
    else:
        return False

def tls_applicationdata_test(data):
    if data[1:3].hex() in TLS_VERSION.keys():  # data[1:3].hex()转换为十六进制字符串
        if data[0] in RECORD_TYPES.keys() and data[0] == 23:
            return True
    else:
        return False

def data_to_bitsequence(data):
    try:
        return ''.join(['{:08b}'.format(ord(byte)) for byte in data])
    except:
        try:
            return ''.join(['{:08b}'.format(oct(byte)) for byte in data])
        except:
            return ''.join(['{:08b}'.format(byte) for byte in data])
    # for byte in data:
    #     print("{:08b}".format(byte))
    # bit_sequence = ''
    # bit_sequence = bit_sequence + ''.join(['{:08b}'.format(byte) for byte in data]) # 字节转换为二进制bit流
    # return bit_sequence

tls_path = './data_tls1.2'
file_name_list = os.listdir(tls_path)
# [low, high] = NTEn.generate_random_range()
# start = time.time()
for file_name in file_name_list:
    TLS_data = []
    file_path = os.path.join(tls_path, file_name)
    print(file_path)
    try:
        f = open(file_path, 'rb')
        pcap = dpkt.pcap.Reader(f)
        num = 0
        for ts, buf in pcap:
            num = num + 1
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            data = tcp.data
            if len(data) != 0:
                print("pktnum{0}: ".format(num), end='')
                tls_detection(data)
                TLS_data.append(data)
                # NTEn_result, NTEn_value = NTEn.N_truncated_entropy_test(data, low, high)
                # CuST_result, CuST_value = CuST.cumulative_sums_test(data_to_bitsequence(data))
                # ApEn_result, ApEn_value = ApEn.fast_approximate_entropy_test(data_to_bitsequence(data))
                # FrWB_result, FrWB_value = FrWB.frequency_within_block_test(data_to_bitsequence(data))
                # LiCT_result, LiCT_value = LiCT.linear_complexity_test(data_to_bitsequence(data))
                # REVT_result, REVT_value = REVT.random_excursion_variant_test(data_to_bitsequence(data))
                # OTMT_result, OTMT_value = OTMT.overlapping_template_matching_test(data_to_bitsequence(data))
                MbT_result, MbT_value = MbT.monobit_test(data_to_bitsequence(data))


                # if NTEn_result:
                #     print("\nNTEn: True pass.")
                # else:
                #     print("\nNTEn: False.")
                #
                # if CuST_result:
                #     print("CuST: True pass.")
                # else:
                #     print("CuST: False.")
                #
                # if ApEn_result:
                #     print("ApEn: True pass.")
                # else:
                #     print("ApEn: False.")
                #
                # if FrWB_result:
                #     print("FrWB: True pass.")
                # else:
                #     print("FrWB: False.")
                #
                if MbT_result:
                    print("MbT: True pass.")
                else:
                    print("MbT: False.")

                # if NTEnT_result and CuST_result:
                #     print("True")
                #     print("PASS")
                # # elif tls_applicationdata_test(data):
                # #     print("True")
                # #     print("PASS")
                # else:
                #     print("False")
                #     print("FAIL: Data not random")

            else:
                print("pktnum{0}: TCP linkage no Application data".format(num))

    except Exception as e:
        print(e)