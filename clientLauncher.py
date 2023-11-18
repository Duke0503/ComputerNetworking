import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from client2 import Peer
from server import Server
import time
import sys
import threading
import os

peer = None

# def runPeer():
#   global peer
#   serverPort = serverPortEntry.get()
#   serverIP = serverIPEntry.get()
#   peerName = peerNameEntry.get()
#   peerPort = peerPortEntry.get()
  
#   if ((serverPort != "") and (serverIP != "") and (peerName != "") and (peerPort != "")):
#     peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
#     print("Peer is running...\n")
#     submitButton.config(state="disabled")
#     peer.startPeer()
    

#   else:
#     messagebox.showwarning("Warning", "Missing value!")

# def onFetch():
#   return
    
# def startRunPeer():
#   t1 = threading.Thread(target=runPeer).start()
  
# def handler():
#   if messagebox.askyesno("Quit?", "Are you sure?"):
#     root.destroy()
#     # os._exit(os.EX_OK)

# root = Tk()
# root.protocol("WM_DELETE_WINDOW", handler)
# root.title("Client GUI")

# infoFrame = Frame(root)
# infoFrame.grid(row=0, column=0)
# Label(infoFrame, text='Client Info').grid()
# serverPortEntry = Entry(infoFrame)
# serverPortEntry.grid(row=1, column=1)
# Label(infoFrame, text='Server Port').grid(row=1, column=0)
# serverIPEntry = Entry(infoFrame)
# serverIPEntry.grid(row=2, column=1)
# Label(infoFrame, text='Server IP').grid(row=2, column=0)
# peerNameEntry = Entry(infoFrame)
# peerNameEntry.grid(row=3, column=1)
# Label(infoFrame, text='Peer Name').grid(row=3, column=0)
# peerPortEntry = Entry(infoFrame)
# peerPortEntry.grid(row=4, column=1)
# Label(infoFrame, text='Peer Port').grid(row=4, column=0)
# submitButton = Button(infoFrame, text="Submit", command=startRunPeer)
# submitButton.grid(row=5)

# # Create Filename List Frame
# fileFrame = Frame(root)
# fileFrame.grid(row=1, column=0, padx=10, sticky=N)
# Label(fileFrame, text='Available Files').grid()
# fileListFrame = Frame(fileFrame)
# fileListFrame.grid(row=1, column=0)
# fileScroll = Scrollbar(fileListFrame, orient=VERTICAL)
# fileScroll.grid(row=0, column=1, sticky=N+S)
# root.fileList = Listbox(fileListFrame, height=5, yscrollcommand=fileScroll.set)
# root.fileList.grid(row=0, column=0)
# fileScroll["command"] = root.fileList.yview

# # Create Peer List Frame
# peerFrame = Frame(root)
# peerFrame.grid(row=1, column=1, padx=10, sticky=N)
# Label(peerFrame, text='Peer List').grid()
# peerListFrame = Frame(peerFrame)
# peerListFrame.grid(row=1, column=0)
# peerScroll = Scrollbar(peerListFrame, orient=VERTICAL)
# peerScroll.grid(row=0, column=1, sticky=N+S)
# root.peerList = Listbox(peerListFrame, height=5, yscrollcommand=peerScroll.set)
# root.peerList.grid(row=0, column=0)
# peerScroll["command"] = root.peerList.yview

# root.fetchButton = Button(fileFrame, text='Fetch', command=onFetch)
# root.fetchButton.grid(row=2, column=0)

# root.mainloop()

def RunPeer():
  global peer
  serverIP = serverIPEntry.get()
  serverPort = serverPortEntry.get()
  peerName = peerNameEntry.get()
  peerPort = peerPortEntry.get()
  if ((serverIP != "") and (serverPort != "") and (peerName != "") and (peerPort != "")):
    peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
    print("Peer is running...\n")
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
    l7.place(x = 475, y = 102)
    serverIPEntry.configure(state = "readonly")
    serverPortEntry.configure(state = "readonly")
    peerNameEntry.configure(state = "readonly")
    peerPortEntry.configure(state = "readonly")
    runPeerBtn.configure(state = "disable", cursor = "arrow")
  else:
    showwarning("Warning", "  Missing value !  ")

def on_closing():
  global peer
  print("Peer off.")
  if ((peer != None) and (peer.endAllThread == False)):
      peer.endSystem()
  root.destroy()

root = tk.Tk()
root.title("Client GUI")
root.geometry("720x500")
root.tk_setPalette(background='#f8f8f8')
root.resizable(0, 0)

#
# appTitle = tk.Label(root, text = "FILE SHARING APP", font=("Helvetica", 23, "bold"), width = 38, pady = 5, bg ="#ff904f", fg = "white", anchor="center")
# appTitle.place(x = 0, y = 0)

label1 = tk.Label(root, text = "Register", font=("Helvetica", 11, "bold"), width = 8, height = 5, bg ="#3399ff", fg = "white", anchor="center")
# label2 = tk.Label(root, text = "Download", font=("Helvetica", 11, "bold"), width = 8, height = 14, bg ="#3399ff", fg = "white", anchor="center")
# label3 = tk.Label(root, text = "Publish", font=("Helvetica", 11, "bold"), width = 8, height = 6, bg ="#3399ff", fg = "white", anchor="center")
label1.place(x = 0, y = 50)
# label2.place(x = 0, y = 140)
# label3.place(x = 0, y = 390)
line1 = tk.Frame(root, highlightbackground = "#ddd", highlightthickness = 1, width = 720)
line2 = tk.Frame(root, highlightbackground = "#ddd", highlightthickness = 1, width = 720)
line1.place(x = 0, y = 145)
line2.place(x = 0, y = 390)

#
l1 = tk.Label(root, text = "Sever:", font = ("Helvetica", 11))
l2 = tk.Label(root, text = "Port", font = ("Helvetica", 11))
l3 = tk.Label(root, text = "IP", font = ("Helvetica", 11))
l1.place(x = 220, y = 65)
l2.place(x = 310, y = 65)
l3.place(x = 450, y = 65)
serverPortEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 7)
serverIPEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 14)
serverPortEntry.place(x = 350, y = 65)
serverIPEntry.place(x = 475, y = 65)

l4 = tk.Label(root, text = "Peer:", font = ("Helvetica", 11))
l5 = tk.Label(root, text = "Port", font = ("Helvetica", 11))
l6 = tk.Label(root, text = "Name", font = ("Helvetica", 11))
l4.place(x = 220, y = 102)
l5.place(x = 310, y = 102)
l6.place(x = 430, y = 102)
peerPortEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 7)
peerNameEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 14)
peerPortEntry.place(x = 350, y = 102)
peerNameEntry.place(x = 475, y = 102)
path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

runPeerBtn = tk.Button(root, text="Enter", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command=RunPeer)
runPeerBtn.place(x = 625, y = 82)

tk.mainloop()