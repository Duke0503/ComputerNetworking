from server import Server
import copy
import time

server = None

port = input("Server port: ")
server = Server(int(port))
print("Server IP: ", server.IP)
server.startServer()

while (server.endAllThread == None):
    time.sleep(0.01)
    
while (server.endAllThread == False):
    try:
        command = input("")
    except:
        break
    arr = command.split(' ')
    if (len(arr) == 2):
        if (arr[0] == "ping"):
            server.ping(arr[1])
        elif (arr[0] == "discover"):
            peerDatas = copy.deepcopy(server.jsonPeerDatas)
            if (peerDatas == []):
                print("[SERVER] '" + arr[1] + "' does not existed in Server!")
            else:
                for i in range(len(peerDatas)):
                    if (peerDatas[i]["name"] == arr[1]):
                        print("[SERVER] [" + peerDatas[i]["name"] + ":" + peerDatas[i]["IP"] 
                              + ":" + str(peerDatas[i]["port"]) + "]:", 'list file:', peerDatas[i]["listFile"])
                        break
                    elif (i == len(peerDatas) - 1):
                        print("[SERVER] '" + arr[1] + "' does not existed in Server!")
        elif (arr[0] == "list"):    
            peerDatas = copy.deepcopy(server.jsonPeerDatas)
            if (peerDatas == []):
                print("[SERVER]: Empty!")
            else:
                if (arr[1] == "peer"):
                    print("[SERVER] List Of Peer In Server:")
                    for i in range(len(peerDatas)):
                        print(' ',"[ID:" + str(peerDatas[i]["ID"]) + "] [" + peerDatas[i]["name"] + ":" + peerDatas[i]["IP"] 
                              + ":" + str(peerDatas[i]["port"]) + "]", 'list file:', peerDatas[i]["listFile"])
                elif (arr[1] == "file"):
                    if (server.listFile == ""):
                        print("[SERVER]: Empty!")
                    else:
                        print("[SERVER] List Of File In Server:")
                        for fname in server.listFile:
                            print(' ',fname)
                else: 
                    print("[ERROR] Wrong command!")
        else:
            print("[ERROR] Wrong command!")
    elif (len(arr) == 1):
        if (arr[0] == "exit"):
            print("Shutting down the server..")
            server.endSystem()
        else:
            print("[ERROR]: Wrong command!")
            
    else:
        print("[ERROR] Wrong command!")

server.endSystem()