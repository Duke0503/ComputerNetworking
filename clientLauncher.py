from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Client Launcher")
root.geometry("450x400")

def onFetch():
  return

def handler():
  if messagebox.askyesno("Quit?", "Are you sure?"):
    root.destroy()

root.protocol("WM_DELETE_WINDOW", handler)

# Create Filename List Frame
fileFrame = Frame(root)
fileFrame.grid(row=0, column=0, padx=10)
Label(fileFrame, text='Available Files').grid()
fileListFrame = Frame(fileFrame)
fileListFrame.grid(row=1, column=0)
fileScroll = Scrollbar(fileListFrame, orient=VERTICAL)
fileScroll.grid(row=0, column=1, sticky=N+S)
root.fileList = Listbox(fileListFrame, height=5, 
                        yscrollcommand=fileScroll.set)
root.fileList.grid(row=0, column=0)
fileScroll["command"] = root.fileList.yview

root.fetchButton = Button(fileFrame, text='Fetch',
                           command=onFetch)
root.fetchButton.grid()

# Create Peer List Frame
peerFrame = Frame(root)
peerFrame.grid(row=0, column=1, padx=10)
Label(peerFrame, text='Peer List').grid()
peerListFrame = Frame(peerFrame)
peerListFrame.grid(row=1, column=0)
peerScroll = Scrollbar(peerListFrame, orient=VERTICAL)
peerScroll.grid(row=0, column=1, sticky=N+S)
root.peerList = Listbox(peerListFrame, height=5, 
                        yscrollcommand=peerScroll.set)
root.peerList.grid(row=0, column=0)
peerScroll["command"] = root.peerList.yview


root.mainloop()