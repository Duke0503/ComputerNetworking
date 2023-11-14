from threading import Thread 
import socket
import json
import copy 

class Server:
# ======================================================================================================================== #
# Variable Definitions
# ======================================================================================================================== #
    IP = socket.gethostbyname(socket.gethostname()) 
    FORMAT = "utf8"
    listFile = []   # [fname1, fname2]
    jsonPeerDatas = []  # [{"ID": , "name": , "IP", "port": , "action": , "listFile": [fname, ]}, ]
    peerID = 1
    serverSocket = None
    listSocket = []
    allThreads = []
    endAllThread = None

# ======================================================================================================================== #
# Init Server
# ======================================================================================================================== #
    def __init__(self, port):
        self.port = port
    
# ======================================================================================================================== #
# Init Server
# ======================================================================================================================== #
    def startServer(self):
        binder = Thread(target = self.listenMessage)
        self.allThreads.append(binder)
        binder.start()
    
# ======================================================================================================================== #
# Listen Message From Peers
# ======================================================================================================================== #
    def listenMessage(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.IP, self.port))
        except:
            print("Fail binding address!")
            self.endSystem()
            return
        self.endAllThread = False
        self.listSocket.append(self.serverSocket)
        self.serverSocket.listen()
        print("Server is running...")
        while (self.endAllThread == False):
            try:
                conn, addr = self.serverSocket.accept()
            except:
                break
            if (conn):
                receiver = Thread(target = self.receiveMessage, args = (conn,))
                self.allThreads.append(receiver)
                receiver.start()

# ======================================================================================================================== #
# Message
# ======================================================================================================================== #
    def receiveMessage(self, conn):
        while (self.endAllThread == False):
            try:
                receiveData = conn.recv(1024).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "register"):
                    # jsonData = {"name": , "IP": , "port": , "action": "register", "listFile": [] }
                    self.handleRegister(conn, jsonData)

                elif (jsonData["action"] == "publishFile"):
                    # jsonData = {"name": , "ID": , "action": "publishFile", "fname": }
                    self.handlePublish(jsonData)

                elif (jsonData["action"] == "deletePublishFile"):
                    # jsonData = {"name": , "ID": , "action": "publishFile", "fname": }
                    self.handleDelete(jsonData)

                elif (jsonData["action"] == "requestListFile"):
                    # jsonData = {"name": , "action": , "requestListFile"}
                    print(jsonData["name"] + " request list file.")
                    self.sendListFile(conn)

                elif (jsonData["action"] == "requestListPeer"):
                    # jsonData = {"action": "requestListPeer", "fname": }
                    self.sendListPeer(conn, jsonData["fname"])

                elif (jsonData["action"] == "leaveNetwork"):
                    # jsonData = {"ID": , "action": "leaveNetwork"}
                    self.handleLeave(conn, jsonData["ID"])
            except:
                continue
    
# ======================================================================================================================== #
# Server Function
# ======================================================================================================================== #
    
# ======================================================================================================================== #
# Register For Peer Join Server
# ======================================================================================================================== #    
    def handleRegister(self, conn, jsonData):
        # Check if nameInput has existed
        for peerData in self.jsonPeerDatas:
            if (peerData["name"] == jsonData["name"]):
                print("Invalid name input!")
                mess = "Invalid name!"
                conn.send(mess.encode(self.FORMAT))
                return
            # Check if address has existed
            elif (peerData["IP"] == jsonData["IP"] and peerData["port"] == jsonData["port"]):
                print("Invalid address input!")
                mess = "Invalid address!"
                conn.send(mess.encode(self.FORMAT))
                return
        # Valid name and address
        print(jsonData["name"] + " joined.")
        jsonData["ID"] = self.peerID
        self.jsonPeerDatas.append(jsonData)
        mess = json.dumps({"ID": self.peerID, "action": "responseRegister"})
        conn.send(mess.encode(self.FORMAT))
        self.peerID += 1

# ======================================================================================================================== #
# Publish File In Server
# ======================================================================================================================== #    
    def handlePublish(self, jsonData):
        index = 0
        for peerData in self.jsonPeerDatas:
            if (peerData["ID"] == jsonData["ID"]):
                break
            index += 1
        fname = jsonData["fname"]
        print(self.jsonPeerDatas[index]["name"] + " published " + fname)
        self.jsonPeerDatas[index]["listFile"].append(fname)
        for fileName in self.listFile:
            if (fname == fileName):
                return
        self.listFile.append(fname)

# ======================================================================================================================== #
# Delete File In Server
# ======================================================================================================================== #    
    def handleDelete(self, jsonData):
        index = 0
        peerListFile = None
        for peerData in self.jsonPeerDatas:
            if(peerData["ID"] == jsonData["ID"]):
                break
            index += 1
        fname = jsonData["fname"]
        print(self.jsonPeerDatas[index]["name"] + " deleted " + fname)
        self.jsonPeerDatas[index]["listFile"].remove(fname)
        dataString = json.dumps(self.jsonPeerDatas)
        if (fname not in dataString):
            self.listFile.remove(fname)

# ======================================================================================================================== #
# List Peer Of A Specific File
# ======================================================================================================================== #
    def sendListPeer(self, conn, fname):
        listPeer = []
        for peerData in self.jsonPeerDatas:
            for fileName in peerData["listFile"]:
                if(fileName == fname):
                    data = {"name": peerData["name"], "ID": peerData["ID"], "IP": peerData["IP"], "port": peerData["port"]}
                    listPeer.append(data)
            sendData = json.dumps({"action": "responseListPeer", "listPeer": listPeer})
            conn.send(sendData.encode(self.FORMAT))

# ======================================================================================================================== #
# List File In Server
# ======================================================================================================================== #
    def sendListFile(self, conn):
        #listFile = copy.deepcopy(self.listFile)
        sendData = json.dumps({"action": "responseListFile", "listFile": self.listFile})
        conn.send(sendData.encode(self.FORMAT))

# ======================================================================================================================== #
# Ping To Peer
# ======================================================================================================================== #
    def ping(self, hostname):
        peerIP = None
        peerPort = None
        for peerData in self.jsonPeerDatas:
            if (peerData["name"] == hostname):
                peerIP = peerData["IP"]
                peerPort = peerData["port"]
                break
        if (peerIP == None or peerPort == None):
            print(hostname, " not found!")
            return
        try: 
            pingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pingSocket.connect((peerIP, peerPort))
        except:
            print("Fail connection!")
            return
        print("Pinging " + hostname + ' [' + peerIP + ', ' + str(peerPort) + '] ...')
        mess = json.dumps({"action": "ping"})
        pingSocket.send(mess.encode(self.FORMAT))
        receiveData = pingSocket.recv(1024).decode(self.FORMAT)
        jsonData = json.loads(receiveData)
        if (jsonData["action"] == "responsePing"):
            print("Reply from [" + jsonData["IP"] + ', ' + str(jsonData["port"]) + "] : OK")

# ======================================================================================================================== #
# Peer Leave Server
# ======================================================================================================================== #
    def handleLeave(self, conn, ID):
        index = 0
        peerListFile = None
        for peerData in self.jsonPeerDatas:
            if(peerData["ID"] == ID):
                peerListFile = copy.deepcopy(peerData["listFile"])
                break
            index += 1
        print(self.jsonPeerDatas[index]["name"] + " leave.")
        self.jsonPeerDatas.pop(index)
        dataString = json.dumps(self.jsonPeerDatas)
        for peerFname in peerListFile:
            if (peerFname not in dataString):
                self.listFile.remove(peerFname)
        conn.close()

# ======================================================================================================================== #
# End Server System
# ======================================================================================================================== #
    def endSystem(self):
        self.endAllThread = True
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread
        