import socket

import tqdm
from Crypto.Cipher import AES

class Receiver:

    key = b"DoMinhDucKey2003"
    nonce = b"DoMinhDucNce2003"

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path
    
    def receiveFileData(self):

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.IP, self.port))
        server.listen()

        client, addr = server.accept()

        

        # file_size = client.recv(1024).decode()
        # print(file_size)
        count = 0
        file = open(self.path, "wb")

        done = False

        file_bytes = b""

        #progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000)

        while not done:
            #count += 1
            print("Count::: ", count)
            data = client.recv(1024)
            print(data)
            count += 1
            if file_bytes[-5:] == b"<END>":
                done = True
            else:
                file_bytes += data
                #print(file_bytes)
            #progress.update(1024)

        print("data: ")
        print(file_bytes)

        file.write(self.cipher.decrypt(file_bytes[:-5]))

        file.close()
        print("Count: ", count)
        client.close()

        server.close()