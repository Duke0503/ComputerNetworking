from client import Peer
import time

peer = None

serverPort = input("Server port: ")
serverIP = input("Server IP: ")
peerName = input("Peer name: ")
peerPort = input("Peer port: ")
peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))

print("Peer is running...\n")
peer.startPeer()
time.sleep(0.1)

while (peer.endAllThread == None):
    time.sleep(0.01)

while (peer.endAllThread == False):

    command = input("Please specify a command: ")
    if (len(command) > 0):
        arr = command.split(' ')
        if (arr[0] == "help"):
            print("[CLIENT] Available Commands: fetch")
            print("[SERVER] Available Commands: files, publish, delete, exit")
        elif (arr[0] == "publish" and len(arr) == 3):
            peer.publish(arr[1], arr[2])
        elif (arr[0] == "files" and len(arr) == 2):
            if (arr[1] == "server"):
                peer.requestListFile()
                time.sleep(0.1)
                if (peer.listFileServer == []):
                    print("[SERVER] Empty!")
                else:
                    for fname in peer.listFileServer:
                        print(' ', fname)
                peer.listFileServer = []
            elif (arr[1] == "local"):
                peer.showFiles()
            else:
                peer.requestListFile()
                time.sleep(0.1)
                check = False
                for fname in peer.listFileServer:
                    if (fname == arr[1]):
                        check = True
                        break
                if (check == True):
                    peer.requestListPeer(fname)
                    time.sleep(0.1)
                    if (peer.listPeerServer == []):
                        print("[SERVER] Empty!")
                    else:
                        for peerName in peer.listPeerServer:
                            print(' ', peerName["name"])
                else:
                    print("[SERVER] '" + arr[1] + "' does not existed in server!")
        elif (arr[0] == "delete" and len(arr) == 2):
                peer.deletePublishFile(arr[1])
        elif (arr[0] == "fetch" and len(arr) == 2):
            peer.requestListPeer(arr[1])
            time.sleep(0.1)
            inputPeer = input(" You want to fetch from: ")
            peer.fetch(arr[1], inputPeer)
            time.sleep(0.5)
        elif (arr[0] == "exit" and len(arr) == 1):
            print("Closing connection to server...")
            peer.endSystem()
        else: 
            print("[ERROR] Wrong command!")
    else:
        print("[ERROR] Wrong command!")

    
peer.endSystem()