from tkinter import *
import tkinter
import tkinter.filedialog as fd

class Window:
 def __init__(self, master):
    self.filename=""
    # csvfile=Label(root, text="Load File:").grid(row=1, column=0)
    # bar=Entry(master).grid(row=1, column=1)

    #Buttons
    # self.cbutton.grid(row=15, column=3, sticky = W + E)
    self.bbutton= Button(root, text="File Browser", command=self.browsecsv) #open browser; refer to browsecsv
    self.bbutton.grid(row=1, column=2)

 def browsecsv(self):
    # filez = fd.askopenfilenames(parent=root, title='Choose a file')
    filez = fd.askopenfiles(parent=root,title='Choose a File')
    print(str(filez))

root = Tk()
window = Window(root)
root.mainloop()