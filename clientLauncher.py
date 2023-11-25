from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
from client import Peer
import time
import os
from pathlib import Path

peer = None
btnFrames = []
peerBtns = []

def RunPeer():
  global peer
  serverIP = serverIPEntry.get()
  serverPort = serverPortEntry.get()
  peerName = peerNameEntry.get()
  peerPort = peerPortEntry.get()
  if (serverIP != "" and serverPort != "" and peerName != "" and peerPort != ""):
    peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
    print("Peer is running...")
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
    Label(peerInfo, text = peer.IP, font = ("Helvetica", 11)).grid(row=3, column=1, sticky=W)
    serverIPEntry.configure(state = "readonly")
    serverPortEntry.configure(state = "readonly")
    peerNameEntry.configure(state = "readonly")
    peerPortEntry.configure(state = "readonly")
    runPeerBtn.configure(state = "disable", cursor = "arrow")
    connectSuccess()
    # updateListLocalFile()
  else:
    showwarning("Warning", "Missing Value")
        
def onClosing():
  if askyesno("Quit", "Are you sure"):
    global peer
    if ((peer != None) and (peer.endAllThread == False)):
      peer.endSystem()
      print("Closing connection to server...")
    root.destroy()

# Create Screen
root = Tk()
root.title("Client GUI")
# root.geometry("500x800")
root.resizable(0, 0)

# Create Client Info Frame
infoFrame = Frame(root)
Label(infoFrame, text="Client Info", font = ("Helvetica", 18)).grid(row=0, sticky=W+E)
infoFrame.grid(row=0, padx=10, pady=10)

# Server Info
serverInfo = Frame(infoFrame)
serverInfo.grid(row=1, column=0, padx=10, pady=10, sticky=N+W)
Label(serverInfo, text="Server:", font = ("Helvetica", 14)).grid(row=0, column=0, sticky=W, padx=10, pady= 10)
Label(serverInfo, text="Port:").grid(row=1, column=0, sticky=W)
Label(serverInfo, text="IP:").grid(row=2, column=0, sticky=W)
serverPortEntry = Entry(serverInfo, font = ("Helvetica", 11), width = 7)
serverPortEntry.grid(row=1, column=1, sticky=W)
serverIPEntry = Entry(serverInfo, font = ("Helvetica", 11), width = 14)
serverIPEntry.grid(row=2, column=1, sticky=W)

# Peer Info
peerInfo = Frame(infoFrame)
peerInfo.grid(row=1, column=1, padx=10, pady=10, sticky=N)
Label(peerInfo, text="Peer:", font = ("Helvetica", 14)).grid(row=0, column=0, sticky=W, padx=10, pady= 10)
Label(peerInfo, text="Port:").grid(row=1, column=0, sticky=W)
Label(peerInfo, text="Name:").grid(row=2, column=0, sticky=W)
Label(peerInfo, text="IP:").grid(row=3, column=0, sticky=W)
peerPortEntry = Entry(peerInfo, font = ("Helvetica", 11), width = 7)
peerPortEntry.grid(row=1, column=1, sticky=W)
peerNameEntry = Entry(peerInfo, font = ("Helvetica", 11), width = 14)
peerNameEntry.grid(row=2, column=1, sticky=W)
runPeerBtn = Button(infoFrame, text="Connect", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = RunPeer)
runPeerBtn.grid(row=1, column=2)

Frame(root, highlightbackground = "#252525", highlightthickness = 5, width = 500).grid(row=1)

def connectSuccess():
  global deleteFile
  
  def updateListLocalFile():
    global peer
    name = peer.name
    listFile = peer.listFile
    index = 0
    localFileListBox.delete(0, "end")
    localFileListBox.configure(state = "normal")
    for lname in os.listdir(name):
      private = True
      for i in range(len(listFile["lname"])):
        if(lname == listFile["lname"][i]):
          private = False
          break
      if private == True:
        localFileListBox.insert(index, " " + lname)
        index = index + 1
  
  def publishFile():
    global peer
    if (peer == None):
      showwarning("Warning", "Connect to server!")
      return
    try:
      str = localFileListBox.get(localFileListBox.curselection())
    except:
      return
    lname = str.replace(" ", "")
    fname = fnameEntry.get()
    if (lname != "" and fname != ""):
      peer.publish(lname, fname)
      fnameEntry.delete(0, "end")
      fnameEntry.insert(0, "")
    else:
      showwarning("Warning", "Missing value!")
    updateListFile()
    updateListLocalFile()
    peerListBox.delete(0, "end")
  
  def updateListFile():
    peer.requestListFile()
    time.sleep(0.1)
    listFile = peer.listFileServer
    fileListbox.delete(0, "end")
    if (len(listFile) > 0):
      fileListbox.configure(state = "normal") 
      for i in range(len(listFile)):
        fileListbox.insert(i, " " + listFile[i])
    else:
      peerListBox.delete(0, "end")  
    peer.listFileServer = []
  
  def showListPeer(var):
    global peer
    try:
      str = fileListbox.get(fileListbox.curselection())
    except:
      return
    fname = str.replace(" ", "")
    peer.requestListPeer(fname)
    time.sleep(0.1)
    listPeer = peer.listPeerServer
    peerListBox.delete(0, "end")
    if (len(listPeer) > 0):
      peerListBox.configure(state = "normal")
      for i in range(len(listPeer)):
        peerListBox.insert(i, " " + listPeer[i]["name"])
        if peer.name == listPeer[i]["name"]:
          peerListBox.itemconfig(i, fg="gray")
    peer.listPeerServer = []

  def deleteFile():
    global peer
    try:
      str = fileListbox.get(fileListbox.curselection())
    except:
      return
    fname = str.replace(" ", "")
    peer.deletePublishFileUsingGUI(fname)
    time.sleep(0.1)
    updateListFile()
    var = None
    showListPeer(var)
      
  def fetchFile():
    try:
      str1 = fileListbox.get(fileListbox.curselection())
      str2 = peerListBox.get(peerListBox.curselection())  
    except:
      return
    fname = str1.replace(" ", "")
    hostname = str2.replace(" ", "")
    peer.requestListPeer(fname)
    time.sleep(0.1)
    peer.fetch(fname, hostname)
    time.sleep(0.1)
    peer.listPeerServer = []
  
  # Create List Frame
  listFrame = Frame(root)
  listFrame.grid(row=2, sticky=W+E)
  Label(listFrame, text="List", font = ("Helvetica", 18)).grid(row=0, padx=10, pady=10, sticky=W)

  # File List Frame
  listFileFrame = Frame(listFrame)
  listFileFrame.grid(row=1, column=0, padx=10, pady=10, sticky=W)
  Label(listFileFrame, text = "List file", font = ("Helvetica", 14)).grid(row=0)
  fileArea = Frame(listFileFrame, background="white")
  fileArea.grid(row=1, padx=10, pady= 10)
  scroll = Scrollbar(fileArea)
  fileListbox = Listbox(fileArea, yscrollcommand = scroll.set, font = ("Helvetica", 11), width = 25, height = 7, 
                      bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                      highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled", exportselection=0)
  fileListbox.bind("<<ListboxSelect>>", showListPeer)
  scroll.pack(side = "right", fill = "y")
  fileListbox.pack(side = "left", padx = 5, pady = 5)
  showListFile = Button(listFileFrame, text="Refresh", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListFile)
  showListFile.grid(row=2, column=0, sticky=W, padx=10, pady= 10)
  deleteFile = Button(listFileFrame, text="Delete", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = deleteFile)
  deleteFile.grid(row=2, column=0, sticky=E, padx=10, pady= 10)

  # Peer List Frame
  listPeerFrame = Frame(listFrame)
  listPeerFrame.grid(row=1, column=1, padx=10, pady=10, sticky=S)
  Label(listPeerFrame, text = "Users has the file", font = ("Helvetica", 14)).grid(row=0)
  peerArea = Frame(listPeerFrame, background="white")
  peerArea.grid(row=1, padx=10, pady= 10)
  scroll = Scrollbar(peerArea)
  peerListBox = Listbox(peerArea, yscrollcommand = scroll.set, font = ("Helvetica", 11), width = 25, height = 7, 
                      bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                      highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled", exportselection=0)
  scroll.pack(side = "right", fill = "y")
  peerListBox.pack(side = "left", padx = 5, pady = 5)
  fetchBtn = Button(listPeerFrame, text="Fetch", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = fetchFile)
  fetchBtn.grid(row=2, padx=10, pady= 10)

  # Local File Frame
  localFileFrame = Frame(listFrame)
  localFileFrame.grid(row=2, column=0, padx=10, pady=10)
  Label(localFileFrame, text = "Local File", font = ("Helvetica", 14)).grid(row=0, column=0)
  localFileArea = Frame(localFileFrame, background="white")
  localFileArea.grid(row=1, column=0, padx=10, pady= 10)
  scroll = Scrollbar(localFileArea)
  localFileListBox = Listbox(localFileArea, yscrollcommand = scroll.set, font = ("Helvetica", 11), width = 25, height = 7, 
                      bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                      highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled", exportselection=0)
  scroll.pack(side = "right", fill = "y")
  localFileListBox.pack(side = "left", padx = 5, pady = 5)
  showListLocalFile = Button(localFileFrame, text="Refresh", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListLocalFile)
  showListLocalFile.grid(row=2, column=0, sticky=W, padx=10, pady= 10)
  
  publishFrame = Frame(listFrame)
  publishFrame.grid(row=2, column=1, padx=10, pady= 10, sticky=W+E)
  Label(publishFrame, text="fname", font=("Helvetica", 18)).grid(row=0, padx=10, pady=10, sticky=W)
  fnameEntry = Entry(publishFrame, font = ("Helvetica", 11), width = 20)
  fnameEntry.grid(row=1, column=0, sticky=W, padx=10, pady= 10)
  publishBtn = Button(publishFrame, text="Publish", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = publishFile)
  publishBtn.grid(row=2, column=0, sticky=W, padx=10, pady= 10)

root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()