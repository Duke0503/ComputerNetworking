from threading import Thread 
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
import socket
import json
import copy 

class Server:
# ======================================================================================================================== #
# Variable Definitions
# ======================================================================================================================== #
    FORMAT = "utf8"
    IP = socket.gethostbyname(socket.gethostname()) 
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
            print("[ERROR] Fail binding address!")
            self.endSystem()
            return
        self.endAllThread = False
        self.listSocket.append(self.serverSocket)
        self.serverSocket.listen()
        print("Server is running... \n")
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

                if (jsonData["action"] == "fetch"):
                    print("[DEBUG] Command: fetch")
                    # jsonData = {"name":, "action": "fetch", "IP": "port":, 
                    #           "statusRequest": "unsuccessful", "fname":, "connName":, "connIP":, "connPort":}
                    if (jsonData["statusRequest"] == "unsuccessful"):
                        print("[CLIENT]: [" + jsonData["name"] + ":" + jsonData["IP"] + ":" 
                              + str(jsonData["port"]) + "] fetch '" + jsonData["fname"] +"' : UNSUCCESS")
                    else:
                        print("[CLIENT]: [" + jsonData["name"] + ":" + jsonData["IP"] + ":" + str(jsonData["port"]) + "] fetch '" + 
                              jsonData["fname"] + "from [" + jsonData["connName"] + ":" + jsonData["connIP"] + ":" + str(jsonData["connPort"]) +"' : SUCCESS") 
                elif (jsonData["action"] == "register"):
                    # jsonData = {"name": , "IP": , "port": , "action": "register", "listFile": [] }
                    self.handleRegister(conn, jsonData)

                elif (jsonData["action"] == "publishFile"):
                    # jsonData = {"ID": , "action": "publishFile", "fname":}
                    self.handlePublish(jsonData)

                elif (jsonData["action"] == "deletePublishFile"):
                    # jsonData = {"name": , "ID": , "action": "publishFile", "fname": }
                    self.handleDelete(jsonData)

                elif (jsonData["action"] == "requestListFile"):
                    # jsonData = {"name" : , "IP" : , "port" : , "action": , "requestListFile"}
                    print("[DEBUG] Command: files")
                    print("[CLIENT] [" + jsonData["name"] + ":" + jsonData["IP"] + ":" + str(jsonData["port"]) + "]")
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
                mess = json.dumps({"action": "responseRegister", "status": "unsuccessfulName"})
                conn.send(mess.encode(self.FORMAT))
                return
            # Check if address has existed
            elif (peerData["IP"] == jsonData["IP"] and peerData["port"] == jsonData["port"]):
                mess = json.dumps({"action": "responseRegister", "status": "unsuccessfulAddress"})
                conn.send(mess.encode(self.FORMAT))
                return
        # Valid name and address
        print("[SERVER] Incoming client connection from " + "[" + jsonData["name"] + ":" + 
                                        jsonData["IP"] + ":" + str(jsonData["port"]) + "]")
        jsonData["ID"] = self.peerID
        self.jsonPeerDatas.append(jsonData)
        mess = json.dumps({"ID": self.peerID, "action": "responseRegister", "status": "successful"})
        conn.send(mess.encode(self.FORMAT))
        self.peerID += 1

# ======================================================================================================================== #
# Publish File In Server
# ======================================================================================================================== #    
    def handlePublish(self, jsonData):
        # jsonData = {"ID": , "action": "publishFile", "fname": }
        index = 0
        for peerData in self.jsonPeerDatas:
            if (peerData["ID"] == jsonData["ID"]):
                break
            index += 1
        fname = jsonData["fname"]
        print("[DEBUG] Command: publish")
        print("[CLIENT] [" + self.jsonPeerDatas[index]["name"] + ":" + self.jsonPeerDatas[index]["IP"] 
              + ":" + str(self.jsonPeerDatas[index]["port"]) + "] : " + fname)
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
        for peerData in self.jsonPeerDatas:
            if(peerData["ID"] == jsonData["ID"]):
                break
            index += 1
        fname = jsonData["fname"]
        print("[DEBUG] Command: delete")
        print("[CLIENT] [" + self.jsonPeerDatas[index]["name"] + ":" + 
                self.jsonPeerDatas[index]["IP"] + ":" + str(self.jsonPeerDatas[index]["port"]) + "]: " + fname)
        self.jsonPeerDatas[index]["listFile"].remove(fname)
        for data in self.jsonPeerDatas:
            if fname in data["listFile"]:
                return
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
        print("[DEBUG] Command: ping")
        for peerData in self.jsonPeerDatas:
            if (peerData["name"] == hostname):
                peerIP = peerData["IP"]
                peerPort = peerData["port"]
                break
        if (peerIP == None or peerPort == None):
            print("[SERVER] '" + hostname + "' does not existed in Server!")
            showerror("Error", "[SERVER] '" + hostname + "' does not existed in Server!")
            return
        try: 
            pingSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            pingSocket.connect((peerIP, peerPort))
        except:
            print("[ERROR] Fail connection!")
            showerror("Error", "[ERROR] Fail connection!")
            return
        print("[SERVER] [" + hostname + ":" + peerIP + ":" + str(peerPort) + "]: Pinging...")
        showinfo("Info", "[SERVER] [" + hostname + ":" + peerIP + ":" + str(peerPort) + "]: Pinging...")
        mess = json.dumps({"action": "ping"})
        pingSocket.send(mess.encode(self.FORMAT))
        receiveData = pingSocket.recv(1024).decode(self.FORMAT)
        jsonData = json.loads(receiveData)
        if (jsonData["action"] == "responsePing"):
            print("[CLIENT] [" + hostname + ":" + peerIP + ":" + str(peerPort) + "]: OK")
            showinfo("Success", "[CLIENT] [" + hostname + ":" + peerIP + ":" + str(peerPort) + "]: OK")

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
        print("[SERVER] Closing connection for client [" +  self.jsonPeerDatas[index]["name"] + ":"
              + self.jsonPeerDatas[index]["IP"] + ":" + str(self.jsonPeerDatas[index]["port"]) + "]")
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
        
