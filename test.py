import os
from pathlib import Path
from tkinter import filedialog

path = filedialog.askopenfilename()

print(path)
print(Path(path).name)