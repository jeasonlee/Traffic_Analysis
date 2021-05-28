import dpkt
import os
import CumulativeSumsTest as CuST
import NTruncatedEntropy as NTEn
# 第0字节
RECORD_TYPES = {
    0x14: "TLSChangeCipherSpec", # 20
    0x15: "TLSAlert", # 21
    0x16: "TLSHandshake",# 22
    0x17: "TLSAppData",# 23
}
# 第1、2字节
TLS_VERSION = {
    '0300': "SSL3",
    '0301': "TLS 1.0",
    '0302': "TLS 1.1",
    '0303': "TLS 1.2",
    '0304': 'TLS 1.3'
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

def TLS_Detection(data):
    if data[0] in RECORD_TYPES.keys(): #data[0]字节ASCII编码
        print(RECORD_TYPES.get(data[0]))
        if data[1:3].hex() in TLS_VERSION.keys(): #data[1:3].hex()转换为十六进制字符串
            # print(TLS_VERSION.get(data[1:3].hex()) + '/ ', end='')
            # if data[5] in HANDSHAKE_TYPES.keys():
            #     print(HANDSHAKE_TYPES.get(data[5]) + '/ ', end='')
            return True
    else:
        return False

tls_path = 'D:/tls'
file_name_list = os.listdir(tls_path)
for file_name in file_name_list:
    TLS_data = []
    file_path = os.path.join(tls_path, file_name)
    print(file_path)
    try:
        f = open(file_path, 'rb')
        pcap = dpkt.pcap.Reader(f)
        num = 0
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            data = tcp.data
            num = num + 1
            if len(data) != 0:
                TLS_data.append(data)
                print("pktnum{0}: ".format(num), end='')
                if TLS_Detection(data):
                    CuST.cumulative_sums_test(data)
            else:
                print("pktnum{0}: TCP linkage no Application data".format(num))

    except Exception as e:
        print(e)