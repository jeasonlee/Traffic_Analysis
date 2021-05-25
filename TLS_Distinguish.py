import dpkt
import os

tls_path = 'D:/tls'
file_name_list = os.listdir(tls_path)
for file_name in file_name_list:
    try:
        file_path = os.path.join(tls_path, file_name)
        print(file_path)
        f = open(file_path, 'rb')
    except Exception as e:
        print(e)