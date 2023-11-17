from tkinter import *
from tkinter import messagebox
from client import Peer
import time
from server import Server
import sys

class ClientGUI(Frame):
  def __init__(self, master, serverPort, serverIP, peerName, peerPort):
    self.master = master
    self.serverPort = serverPort
    self.serverIP = serverIP
    self.peerName = peerName
    self.peerPort = peerPort
    self.master.protocol("WM_DELETE_WINDOW", self.handler)
    self.createGUI()

  def createGUI(self):
    infoFrame = Frame(self.master)
    infoFrame.grid(row=0, column=0)
    Label(infoFrame, text='Client Info').grid()
    self.serverPort = Label(infoFrame, text=self.serverPort)
    self.serverPort.grid(row=1, column=1)
    Label(infoFrame, text='Server Port').grid(row=1, column=0)
    self.serverIP = Label(infoFrame, text=self.serverIP)
    self.serverIP.grid(row=2, column=1)
    Label(infoFrame, text='Server IP').grid(row=2, column=0)
    self.peerName = Label(infoFrame, text=self.peerName)
    self.peerName.grid(row=3, column=1)
    Label(infoFrame, text='Peer Name').grid(row=3, column=0)
    self.peerPort = Label(infoFrame, text=self.peerPort)
    self.peerPort.grid(row=4, column=1)
    Label(infoFrame, text='Peer Port').grid(row=4, column=0)
    
    # Create Filename List Frame
    fileFrame = Frame(self.master)
    fileFrame.grid(row=1, column=0, padx=10, sticky=N)
    Label(fileFrame, text='Available Files').grid()
    fileListFrame = Frame(fileFrame)
    fileListFrame.grid(row=1, column=0)
    fileScroll = Scrollbar(fileListFrame, orient=VERTICAL)
    fileScroll.grid(row=0, column=1, sticky=N+S)
    self.master.fileList = Listbox(fileListFrame, height=5, yscrollcommand=fileScroll.set)
    self.master.fileList.grid(row=0, column=0)
    fileScroll["command"] = self.master.fileList.yview

    # Create Peer List Frame
    peerFrame = Frame(self.master)
    peerFrame.grid(row=1, column=1, padx=10, sticky=N)
    Label(peerFrame, text='Peer List').grid()
    peerListFrame = Frame(peerFrame)
    peerListFrame.grid(row=1, column=0)
    peerScroll = Scrollbar(peerListFrame, orient=VERTICAL)
    peerScroll.grid(row=0, column=1, sticky=N+S)
    self.master.peerList = Listbox(peerListFrame, height=5, yscrollcommand=peerScroll.set)
    self.master.peerList.grid(row=0, column=0)
    peerScroll["command"] = self.master.peerList.yview
    
    self.master.fetchButton = Button(fileFrame, text='Fetch', command=self.onFetch)
    self.master.fetchButton.grid(row=2, column=0)
    
  def onFetch(self):
    sels = self.peerList.curselection()
    return

  def handler(self):
    if messagebox.askyesno("Quit?", "Are you sure?"):
      self.master.destroy()
      
  def runTerminal(self):
    return
    
if __name__ == "__main__":
  try:
    serverPort = sys.argv[1]
    serverIP = sys.argv[2]
    peerName = sys.argv[3]
    peerPort = sys.argv[4]
    
    peer = None
    peer = Peer(serverIP, int(serverPort), peerName, int(peerPort))
    print("Peer is running...\n")
    peer.startPeer()
    time.sleep(0.1)
    
  except:
    print("[Usage: clientLauncher.py serverPort serverIP peerName peerPort]\n")