import tkinter as tk
import tkinter.ttk as ttk 
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
from client import Peer
from server import Server
import time
import sys
import time
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

def updateListFile():
  global peer
  if (peer == None):
    return
  peer.requestListFile()
  time.sleep(0.1)
  listFile = peer.listFileServer
  fileListbox.delete(0, "end")
  if (len(listFile) > 0):
      fileListbox.configure(state = "normal") 
      for i in range(len(listFile)):
          fileListbox.insert(i, " " + listFile[i])
  peer.listFileServer = []  
  
def no_selection(index):
  try:
    str = peerListBox.get(peerListBox.curselection())
  except:
    return
  peerName = str.replace(" ", "")
  if peerName == peer.name:
    peerListBox.itemconfig(0, fg='gray')
    peerListBox.select_clear(0)

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
      if peer.ID == listPeer[i]["ID"]:
        peerListBox.itemconfig(i, fg='gray')
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
  peerListBox.delete(0, "end")
  

def OpenFile():
  path = filedialog.askopenfilename()
  path = Path(path).name
  lnameEntry.configure(state="normal")  
  lnameEntry.delete(0, "end")
  lnameEntry.insert(0, path)
  lnameEntry.configure(state="readonly") 
  pass

def publishFile():
  global peer
  if (peer == None):
    showwarning("Warning", "Connect to server!")
    return
  lname = lnameEntry.get()
  fname = fnameEntry.get()
  if (lname != "" and fname != ""):
    peer.publish(lname, fname)
    lnameEntry.configure(state="normal")  
    lnameEntry.delete(0, "end")
    lnameEntry.insert(0, "")
    lnameEntry.configure(state="readonly")
    fnameEntry.delete(0, tk.END)
    fnameEntry.insert(0, "")
    updateListFile()
  else:
    showwarning("Warning", "Missing value!")
    
def fetchFile():
  try:
    str1 = fileListbox.get(fileListbox.curselection())
    str2 = peerListBox.get(peerListBox.curselection())
  except:
    return
  fname = str1.replace(" ", "")
  hostname = str2.replace(" ", "")
  peer.fetch(fname, hostname)
  showinfo("Complete", "Fetch Successful")
        
def on_closing():
    if askyesno("Quit", "Are you sure"):
        global peer
        if ((peer != None) and (peer.endAllThread == False)):
            peer.endSystem()
            print("Closing connection to server...")
        root.destroy()


root = tk.Tk()
root.title("Client GUI")
root.geometry("720x720")
root.resizable(0, 0)

appTitle = tk.Label(root, text = "FILE SHARING APP", font=("Arial", 23, "bold"), width = 60, pady = 5, bg ="#ff904f", fg = "white", anchor="center")
appTitle.place(x = 0, y = 0)

label1 = tk.Label(root, text = "Connect", font=("Helvetica", 11, "bold"), width = 8, height = 8, bg ="#3399ff", fg = "white", anchor="center")
label2 = tk.Label(root, text = "Download", font=("Helvetica", 11, "bold"), width = 8, height = 40, bg ="#3399ff", fg = "white", anchor="center")
label3 = tk.Label(root, text = "Publish", font=("Helvetica", 11, "bold"), width = 8, height = 9, bg ="#3399ff", fg = "white", anchor="center")
label1.place(x = 0, y = 40)
label2.place(x = 0, y = 140)
label3.place(x = 0, y = 610)

line1 = tk.Frame(root, highlightbackground = "#ddd", highlightthickness = 5, width = 720)
line2 = tk.Frame(root, highlightbackground = "#ddd", highlightthickness = 5, width = 720)
line1.place(x = 0, y = 145)
line2.place(x = 0, y = 610)

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

l8 = tk.Label(root, text = "List file", font = ("Helvetica", 11))
l8.place(x = 90, y = 170)
showListFile = tk.Button(root, text="Refresh", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = updateListFile)
showListFile.place(x = 90, y = 340)
deleteFile = tk.Button(root, text="Delete", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = deleteFile)
deleteFile.place(x = 200, y = 340)

fileArea = tk.Frame(root, background="white")
fileArea.place(x = 90, y = 195)
scroll = ttk.Scrollbar(fileArea)
fileListbox = tk.Listbox(fileArea, yscrollcommand = scroll.set, font = ("Helvetica", 14), width = 25, height = 7, 
                     bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                     highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled")
fileListbox.bind("<<ListboxSelect>>", showListPeer)
scroll.pack(side = "right", fill = "y")
fileListbox.pack(side = "left", padx = 5, pady = 5)

l9 = tk.Label(root, text = "Users has the file", font = ("Helvetica", 11))
l9.place(x = 450, y = 166)

peerArea = tk.Frame(root, background="white")
peerArea.place(x = 450, y = 195)
scroll = ttk.Scrollbar(peerArea)
peerListBox = tk.Listbox(peerArea, yscrollcommand = scroll.set, font = ("Helvetica", 14), width = 25, height = 7, 
                     bg = "white", selectbackground = "#ff904f", selectforeground = "white", activestyle = "none", 
                     highlightthickness = 0, borderwidth = 0, selectmode = "single", cursor = "hand2", state = "disabled")
peerListBox.bind("<<ListboxSelect>>", no_selection)
scroll.pack(side = "right", fill = "y")
peerListBox.pack(side = "left", padx = 5, pady = 5)
fetchBtn = tk.Button(root, text="Fetch", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = fetchFile)
fetchBtn.place(x = 450, y = 340)

#
l11 = tk.Label(root, text = "lname", font = ("Helvetica", 11))
l11.place(x = 90, y = 630)
lnameEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 20)
lnameEntry.place(x = 145, y = 630)
browseFileBtn = tk.Button(root, text = "Browse", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = OpenFile)
browseFileBtn.place(x = 350, y = 630)

l12 = tk.Label(root, text = "fname", font = ("Helvetica", 11))
l12.place(x = 90, y = 685)
fnameEntry = ttk.Entry(root, font = ("Helvetica", 11), width = 20)
fnameEntry.place(x = 145, y = 685)

publishBtn = tk.Button(root, text="Publish", border = 0, borderwidth = 0, relief = "sunken", cursor = "hand2", command = publishFile)
publishBtn.place(x = 350, y = 685)

root.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()