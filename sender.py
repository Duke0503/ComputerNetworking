import os
import socket

from Crypto.Cipher import AES

class Sender:
    key = b"DoMinhDucKey2003"
    nonce = b"DoMinhDucNce2003"

    cipher = AES.new(key, AES.MODE_EAX, nonce)

    def __init__(self, IP, port, path):
        self.IP = IP
        self.port = port
        self.path = path

    def sendFileData(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.IP, self.port))

        #file_size = os.path.getsize("file")

        with open(self.path, "rb") as f:
            data = f.read()

        encrypted = self.cipher.encrypt(data)

        client.sendall(encrypted)
        client.send(b"<END>")

        client.close()