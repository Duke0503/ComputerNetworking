import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
from client import Peer
from server import Server
import time
import sys
import time

peer = None

def RunPeer():
    global peer
    serverIP = serverIPEntry.get()
    serverPort = serverPortEntry.get()
    peerName = peerNameEntry.get()
    peerPort = peerPortEntry.get()
    if ((serverIP != "") and (serverPort != "") and (peerName != "") and (peerPort != "")):
        peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
        peer.startPeer()
        while (peer.endAllThread == None):
            time.sleep(0.01)
        if (peer.endAllThread == True):
            peer = None
            return
        while (peer.ID == None):
            time.sleep(0.01)
            if (peer.endAllThread == True):
               return
        l7 = tk.Label(root, text = peer.IP, font = ("Helvetica", 11))
        l7.place(x = 180, y = 102)
        serverIPEntry.configure(state = "readonly")
        serverPortEntry.configure(state = "readonly")
        peerNameEntry.configure(state = "readonly")
        peerPortEntry.configure(state = "readonly")
        runPeerBtn.configure(state = "disable", cursor = "arrow")
    else:
        showwarning("Warning", "Missing value!")
        
def on_closing():
    if askyesno("Quit", "Are you sure"):
        global peer
        if ((peer != None) and (peer.endAllThread == False)):
            peer.endSystem()
            print("Closing connection to server...")
        root.destroy()


root = tk.Tk()
root.title("Client GUI")
root.geometry("720x503")
root.resizable(0, 0)

appTitle = tk.Label(root, text = "FILE SHARING APP", font=("Arial", 23, "bold"), width = 38, pady = 5, bg ="#ff904f", fg = "white", anchor="center")
appTitle.place(x = 0, y = 0)

label1 = tk.Label(root, text = "Connect", font=("Helvetica", 11, "bold"), width = 8, height = 5, bg ="#3399ff", fg = "white", anchor="center")
label1.place(x = 0, y = 50)

line1 = tk.Frame(root, highlightbackground = "#ddd", highlightthickness = 5, width = 720)
line1.place(x = 0, y = 145)

#
l1 = tk.Label(root, text = "Sever:", font = ("Helvetica", 11))
l2 = tk.Label(root, text = "Port", font = ("Helvetica", 11))
l3 = tk.Label(root, text = "IP", font = ("Helvetica", 11))
l1.place(x = 200, y = 65)
l2.place(x = 290, y = 65)
l3.place(x = 430, y = 65)
serverPortEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 7)
serverIPEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 14)
serverPortEntry.place(x = 350, y = 65)
serverIPEntry.place(x = 475, y = 65)

l4 = tk.Label(root, text = "Peer:", font = ("Helvetica", 11))
l5 = tk.Label(root, text = "IP", font = ("Helvetica", 11))
l6 = tk.Label(root, text = "Port", font = ("Helvetica", 11))
l7 = tk.Label(root, text = "Name", font = ("Helvetica", 11))
l4.place(x = 100, y = 102)
l5.place(x = 150, y = 102)
l6.place(x = 290, y = 102)
l7.place(x = 430, y = 102)
peerPortEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 7)
peerNameEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 14)
peerPortEntry.place(x = 350, y = 102)
peerNameEntry.place(x = 475, y = 102)
runPeerBtn = tk.Button(root, text="Connect", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunPeer)
runPeerBtn.place(x = 625, y = 82)


root.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()