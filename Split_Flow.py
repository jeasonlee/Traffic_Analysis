import dpkt
import os
import collections
import socket

class flow:
    def __init__(self, src_ip, dst_ip, src_port, dst_port):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port

    def __eq__(self, other):
        flag_1 = self.src_ip == other.src_ip and self.dst_ip == other.dst_ip and self.src_port == other.src_port and self.dst_port == other.dst_port
        flag_2 = self.src_ip == other.dst_ip and self.dst_ip == other.src_ip and self.src_port == other.dst_port and self.dst_port == other.src_port
        return flag_1 or flag_2

    def __hash__(self):
        string_flow = str(sorted([self.src_ip, self.dst_ip]) + sorted([self.src_port, self.dst_port]))
        return hash(string_flow)

if __name__ == '__main__':
    data_path = './data_smb/'
    file_name_list = os.listdir(data_path)

    for file_name in file_name_list:
        tcp_flow_dict = dict()
        udp_flow_dict = dict()
        tcp_flow_num = 0
        udp_flow_num = 0
        try:
            f = open(os.path.join(data_path, file_name), 'rb')
            pcap = dpkt.pcap.Reader(f)

            for ts, buf in pcap:
                eth = dpkt.ethernet.Ethernet(buf)
                if not isinstance(eth.data, dpkt.ip.IP):  # 解包，网络层，判断网络层是否存在，
                    continue
                ip = eth.data
                trans_data = ip.data
                if not len(trans_data): # 无传输层数据
                    continue
                if not len(trans_data.data): # 无应用层数据
                    continue
                # print(ip)
                if ip.p == 6: # TCP
                    tcp = ip.data
                    # print("-----------------------")
                    # print(socket.inet_ntoa(ip.src))
                    # print(socket.inet_ntoa(ip.dst))
                    # print(sorted([socket.inet_ntoa(ip.src), socket.inet_ntoa(ip.dst)]))
                    new_flow = flow(ip.src, ip.dst, ip.tcp.sport, ip.tcp.dport)
                    if new_flow not in tcp_flow_dict:
                        tcp_flow_dict[new_flow] = [(ts, buf)]
                    else:
                        tcp_flow_dict[new_flow].append((ts,buf))

                elif ip.p == 17:
                    udp = ip.data
                    new_flow = flow(ip.src, ip.dst, ip.udp.sport, ip.udp.dport)
                    if new_flow not in udp_flow_dict:
                        udp_flow_dict[new_flow] = [(ts, buf)]
                    else:
                        udp_flow_dict[new_flow].append((ts, buf))
        except Exception as e:
            print("[error] {0}".format(e))

    for key, value in tcp_flow_dict.items():

        print("ip.src:{0}, ip.dst:{1}, src_port:{2}, dst_port:{3} data:{4}".format(socket.inet_ntoa(key.src_ip), socket.inet_ntoa(key.dst_ip), key.src_port, key.dst_port, len(value)))
    print("-" * 40)
    for key, value in udp_flow_dict.items():
        print("ip.src:{0}, ip.dst:{1}, src_port:{2}, dst_port:{3} data:{4}".format(socket.inet_ntoa(key.src_ip), socket.inet_ntoa(key.dst_ip), key.src_port, key.dst_port, len(value)))

    result_path = os.path.join('', "result")
    if not os.path.exists(result_path):
        os.mkdir(result_path)

    for i, value in zip(range(len(tcp_flow_dict.values())), tcp_flow_dict.values()):
        flow_new = open(os.path.join(result_path, str(i) + "_tcp.pcap"), 'wb')
        writer = dpkt.pcap.Writer(flow_new)
        value.sort(key = lambda x:x[0], reverse=False)
        for pkt in value:

            writer.writepkt(pkt = pkt[1], ts = pkt[0])
        flow_new.close()