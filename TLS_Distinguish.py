import dpkt
import os

tls_path = 'D:/tls'
file_name_list = os.listdir(tls_path)
for file_name in file_name_list:
    file_path = os.path.join(tls_path, file_name)
    print(file_path)
    try:
        f = open(file_path, 'rb')
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            data = tcp.data
            if len(data) != 0:
                if data[0] == 22:
                    print(len(data))
                    if data[5] == 1:
                        print("Client Hello!")
                    elif data[5] == 2:
                        print("Server Hello!")
                    elif data[5] == 11:
                        print("Certificate!")
                elif data[0] == 23:
                    print("Application Data!")

    except Exception as e:
        print(e)