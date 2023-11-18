from threading import Thread
import socket
from tkinter import messagebox
import json
import os
import time
from Crypto.Cipher import AES


class Peer:
# ======================================================================================================================== #
# Variable Definitions
# ======================================================================================================================== #
    

    key = b"DoMinhDucKey2003"
    nonce = b"DoMinhDucNce2003"

    cipher = AES.new(key, AES.MODE_EAX, nonce)


    IP = socket.gethostbyname(socket.gethostname()) # IP 
    ID = None
    FORMAT = "utf-8"
    peerSocket = None
    serverConnection = None
    connectSocket = None 
    listFileServer = []  # [fname1, fname2]
    listFile = {"lname": [], "fname":[]} # file name: fname, client's file system: lname
    listPeerServer = [] # [{"name": , "ID": , IP": , "port":}, ]
    listSocket = []
    allThreads = []
    endAllThread = None


# ======================================================================================================================== #
# Init A Peer
# ======================================================================================================================== #
    def __init__(self, serverIP, serverPort, name, port):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.name = name
        self.port = port
        self.ID = None

# ======================================================================================================================== #
# Set Up A Peer
# ======================================================================================================================== #
    def setUp(self):
        # Connect to server
        try:
            self.serverConnection = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket.
            self.serverConnection.connect((
                self.serverIP, self.serverPort)) # Connect to server
        except:
            self.endSystem()
            print("Fail connection !")
            return
        self.endAllThread = False
        self.listSocket.append(self.serverConnection)
        data = json.dumps({"name": self.name, "IP": self.IP, "port": self.port,
                            "action": "register", "listFile": [] })
        self.serverConnection.send(data.encode(self.FORMAT))
        # End Connect to server

        # Listen message 
        try: 
            self.peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peerSocket.bind((self.IP, self.port))
        except:
            self.endSystem()
            print("Unavailable address!")
            return
        self.listSocket.append(self.peerSocket)
        self.peerSocket.listen()
        # End Listen message

        # Create multi-thread
        receiver1 = Thread(target = self.listenServer) # From the server
        self.allThreads.append(receiver1)
        receiver1.start()
        receiver2 = Thread(target = self.listenResponse)  # Handle response
        self.allThreads.append(receiver2)
        receiver2.start()

        while (self.endAllThread == False):
            try:
                conn, addr = self.peerSocket.accept()
            except:
                break
            if (conn):
                receiver3 = Thread(target = self.listenRequest, args = (conn,))
                self.allThreads.append(receiver3)
                receiver3.start()
        # End Create multi-thread

# ======================================================================================================================== #
# Run Peer
# ======================================================================================================================== #
    def startPeer(self):
        register = Thread(target = self.setUp)
        if not os.path.isdir(self.name):
            os.mkdir(self.name)
        self.allThreads.append(register)
        register.start()


############################################################################################################################
##############                                    INTERACT WITH OTHER PEERS                               ##################
############################################################################################################################

# ======================================================================================================================== #
# Listen Peers Request
# ======================================================================================================================== #
    def listenRequest(self, conn):
        while(self.endAllThread == False):
            try:
                receiveData = conn.recv(1024).decode(self.FORMAT)
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "requestFile"):
                    #jsonData = {"name": , "action": "requestFile", "fname": }
                    peerName = jsonData["name"]
                    fname = jsonData["fname"]
                    
                    # Create a thread to send file
                    sender = Thread(target = self.sendFile, args = (conn, fname, peerName))
                    self.allThreads.append(sender)
                    sender.start()

                if (jsonData["action"] == "ping"):
                    print("\n[SERVER] Pinging from Server...")
                    mess = json.dumps({"IP": self.IP, "port": self.port, "action": "responsePing"})
                    conn.send(mess.encode(self.FORMAT))
            except:
                continue 

# ======================================================================================================================== #
# Listen Peers Response
# ======================================================================================================================== #
    def listenResponse(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.connectSocket.recv(1024).decode(self.FORMAT) 
                jsonData = json.loads(receiveData)
                if (jsonData["action"] == "responseFile"):
                    # jsonData = {"name": , "IP": , "port": , "action": "resFile", "status": , "fname": }
                    if (jsonData["status"] == "enable"):
                        self.receiveFile(jsonData["fname"], jsonData["name"], jsonData["IP"], jsonData["port"])
                    else:
                        mess = json.dumps({"name": self.name, "action": "fetch", "IP": self.IP, "port": self.port, 
                               "statusRequest": "unsuccessful", "fname": jsonData["fname"]})
                        self.serverConnection.send(mess.encode(self.FORMAT))
                        print("[CLIENT] '" + jsonData["fname"] + "' does not existed!")
                    self.connectSocket.close()
                    self.connectSocket = None
            except:   
                continue

# ======================================================================================================================== #
# Send File
# ======================================================================================================================== #
    def sendFile(self, conn, fname, peerName):
        count = 0
        lname = None
        for fileName in self.listFile["fname"]:
            if (fileName == fname):
                lname = self.listFile["lname"][count]
                break
            count += 1
        path = os.path.join(self.name, lname) # self.name\lname on Windows
        if os.path.isfile(path):
            mess = json.dumps({"name": self.name, "IP": self.IP, "port": self.port, 
                               "action": "responseFile", "status": "enable", "fname": fname})
            conn.send(mess.encode(self.FORMAT))
            time.sleep(0.1)
            print("\n  Sending " + fname + " to " + peerName + "...")
            with open(path, "rb") as file:
                while True:
                    try:
                        data = file.read(1024)
                        if (not data):
                            break
                        encrypted = self.cipher.encrypt(data)
                        conn.send(encrypted)
                    except:
                        continue
            conn.send(b"<END>")
            file.close()
            print("  Sending Successful!")
        else:
            print("File !")
            mess = json.dumps({"name": self.name, "action": "responseFile", 
                               "status": "disable", "fname": fname})
            conn.send(mess.encode(self.FORMAT))

# ======================================================================================================================== #
# Receive File
# ======================================================================================================================== #
    def receiveFile(self, fname, peerName, IP, port):
        self.connectSocket.settimeout(0.7) # Set a timeout on blocking socket operations
        if not os.path.isdir(self.name):
            os.mkdir(self.name)
        # Expands name portion of fname with numeric ' (x)' suffix to return fname that doesn't exist already.    
        path = os.path.join(self.name, fname)
        filename, extension = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = filename + "(" + str(counter) + ")" + extension
            counter += 1
        print("  Receiving " + fname + " from " + peerName + "...")
        with open(path, 'wb') as file:
            while True:
                try:
                    
                    done = False
                    file_bytes = b""

                    while not done:
                        data = self.connectSocket.recv(1024)
                        
                        if (data == b"<END>"):
                            file.write(self.cipher.decrypt(file_bytes))
                            done = True
                        elif (data[-5:] == b"<END>"):
                            file_bytes += data[:-5]
                            file.write(file_bytes)
                            file.write(self.cipher.decrypt(file_bytes))
                            done = True
                        else: 
                            file_bytes = file_bytes + data
                        
                except socket.timeout:
                    break
                file.close()
                print("  Receiving Successful!")
                mess = json.dumps({"name": self.name, "action": "fetch", "IP": self.IP, "port": self.port, 
                               "statusRequest": "successful", "fname": fname, "connName": peerName, "connIP": IP, "connPort": port})
                self.serverConnection.send(mess.encode(self.FORMAT))

                

# ======================================================================================================================== #
# Fetch File
# ======================================================================================================================== #
    def fetch(self, fname, hostname):
        if (hostname == self.name):
            print("[ERROR] Invalid Information!")
            mess = json.dumps({"name": self.name, "action": "fetch", "IP": self.IP, "port": self.port, 
                               "statusRequest": "unsuccessful", "fname": fname})
            self.serverConnection.send(mess.encode(self.FORMAT))
            return
        IP = None
        port = None
        for peerData in self.listPeerServer:
            if (hostname == peerData["name"]):
                IP = peerData["IP"]
                port = peerData["port"]
                break
        if(IP == None or port == None):
            print("[SERVER] '" +  hostname, "' does not existed in Server!")
            mess = json.dumps({"name": self.name, "action": "fetch", "IP": self.IP, "port": self.port, 
                               "statusRequest": "unsuccessful", "fname": fname})
            self.serverConnection.send(mess.encode(self.FORMAT))
            return
        connect = Thread(target = self.startConnection, args = (IP, port, fname))
        self.allThreads.append(connect)
        connect.start()

    def startConnection(self, IP, port, fname):
        self.connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connectSocket.connect((IP, port))
        self.listSocket.append(self.connectSocket)
        mess = json.dumps({"name": self.name,  "action": "requestFile", "fname": fname})
        self.connectSocket.send(mess.encode(self.FORMAT))
 


############################################################################################################################
##############                                    INTERACT WITH SERVER                                    ##################
############################################################################################################################

# ======================================================================================================================== #
# Listen Response From Server
# ======================================================================================================================== #
    def listenServer(self):
        while(self.endAllThread == False):
            try:
                receiveData = self.serverConnection.recv(
                    1024).decode(self.FORMAT) # Response from server
                
                
                jsonData = json.loads(receiveData)
                # Request to register
                if (jsonData["action"] == "responseRegister"):
                    if (jsonData["status"] == "successful"):
                        self.ID = jsonData["ID"]
                    elif (jsonData["status"] == "unsuccessfulName"):  # Check for the unique name in the server
                        print("[SERVER] '" + self.name + "' has existed!")
                        self.endSystem()
                        return
                    elif (jsonData["status"] == "unsuccessfulAddress"): # Check for the unique address in the server
                        print("[SERVER] '" + self.IP + ":" + str(self.port) + "' has existed!")
                        self.endSystem()
                        return

                # Request for list file
                elif (jsonData["action"] == "responseListFile"):
                    # jsonData = {"action": "responseListFile", "listFile": [fname1, ]}
                    self.listFileServer = []
                    for fname in jsonData["listFile"]:
                        self.listFileServer.append(fname)

                # Request for list peer
                elif (jsonData["action"] == "responseListPeer"):
                    # jsonData = {"action": "responseListPeer", "listPeer": [{"name": , "ID": , "IP": , "port":}, ]}
                    self.listPeerServer = []    # Reset list peer 
                    for peerData in jsonData["listPeer"]:
                        self.listPeerServer.append(peerData)
            except:
                continue

# ======================================================================================================================== #
# Request List Files In Server
# ======================================================================================================================== #
    def requestListFile(self):
        mess = json.dumps({"name": self.name, "IP": self.IP, "port": self.port, "action": "requestListFile"})
        self.serverConnection.send(mess.encode(self.FORMAT))

# ======================================================================================================================== #
# Show My Files
# ======================================================================================================================== #
    def showFiles(self):
        # Show upload files
        print("[SERVER] Public Files: ")
        for i in range(len(self.listFile["lname"])):
            print(" lname: ", self.listFile["lname"][i],
                  " -> ", "fname: ", self.listFile["fname"][i])
            
        # Show private files
        print("[CLIENT] Private Files: ")
        for lname in os.listdir(self.name):
            private = True
            for i in range(len(self.listFile["lname"])):
                if(lname == self.listFile["lname"][i]):
                    private = False
                    break
            if private == True:
                print(" lname: ", lname)

# ======================================================================================================================== #
# Publish File
# ======================================================================================================================== #
    def publish(self, lname, fname):
        count = 0
        # Update content in directory file without updating to server
        for name in self.listFile["lname"]:
            if (name == lname):
                print("[SERVER] File published before!")
                return
        for name in self.listFile["fname"]:
            if (name == fname):
                print("[SERVER] File published before!")
                return
        
        # Check if the file is in local repository 
        for lName in os.listdir(self.name):
            if (lname == lName):
                break
            else:
                count += 1
        if (count == len(os.listdir(self.name))):
            print("[CLIENT] File does not exist in your local repository!")
            return
        self.listFile["lname"].append(lname)
        self.listFile["fname"].append(fname)
        mess = json.dumps({"ID": self.ID, "action": "publishFile", "fname": fname})
        self.serverConnection.send(mess.encode(self.FORMAT))
        print("[SERVER] Publish '" + fname + "': SUCCESS")

# ======================================================================================================================== #
# Delete A File In Server
# ======================================================================================================================== #
    def deletePublishFile(self, fname):
        index = 0
        mess = json.dumps({"ID": self.ID, "action": "deletePublishFile", "fname": fname})
        self.serverConnection.send(mess.encode(self.FORMAT))
        for fName in self.listFile["fname"]:
            if(fName == fname):
                lName = self.listFile["lname"][index]
                print("[SERVER] Delete " + fname + '!')
                confirm = input(" Yes/No: ")
                if (confirm == "Yes" or confirm == "Y" or confirm == "yes" or confirm == "y"):
                    self.listFile["lname"].remove(lName)
                    self.listFile["fname"].remove(fName)

                    print("[SERVER] Delete '" + fname + "' : SUCCESS")
                    return
                elif (confirm == "No" or confirm == "N" or confirm == "no" or confirm == "n"): 
                    print("[SERVER] Delete '" + fname + "' : UNSUCCESS")
                    return 
                else: 
                    print("[SERVER] Delete '" + fname + "' : UNSUCCESS")
                    return
            else:
                index += 1
        print("[SERVER] '" + fname + " does not existed in Server!")
        
    def deletePublishFileUsingGUI(self, fname):
        index = 0
        mess = json.dumps({"ID": self.ID, "action": "deletePublishFile", "fname": fname})
        self.serverConnection.send(mess.encode(self.FORMAT))
        for fName in self.listFile["fname"]:
            if(fName == fname):
                lName = self.listFile["lname"][index]
                print("[SERVER] Delete " + fname + '!')
                if (messagebox.askyesno("Delete", "Are you sure?")):
                    self.listFile["lname"].remove(lName)
                    self.listFile["fname"].remove(fName)

                    print("[SERVER] Delete '" + fname + "' : SUCCESS")
                    return 
                else: 
                    print("[SERVER] Delete '" + fname + "' : UNSUCCESS")
                    return
            else:
                index += 1
        print("[SERVER] '" + fname + " does not existed in Server!")


# ======================================================================================================================== #
# Request List Peer Of A Specific File
# ======================================================================================================================== #
    def requestListPeer(self, fname):
        mess = json.dumps({"action": "requestListPeer", "fname": fname})
        self.serverConnection.send(mess.encode(self.FORMAT))

# ======================================================================================================================== #
# End Client System
# ======================================================================================================================== #
    def endSystem(self):
        if (self.ID != None):
            mess = json.dumps({"ID": self.ID, "action": "leaveNetwork"})
            self.serverConnection.send(mess.encode(self.FORMAT))
            self.ID = None
        self.endAllThread = True
        for socket in self.listSocket:
            socket.close()
            del socket
        for thread in self.allThreads:
            del thread     