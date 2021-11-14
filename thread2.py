from Tkinter import *
from ttk import *
import threading
import time
import sys

#this runs successfully

def fmtTime(timeStamp):
    timeArray = time.localtime(timeStamp)
    dateTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return dateTime

class re_Text():

    def __init__(self, widget):

        self.widget = widget

    def write(self, content):

        self.widget.insert(INSERT, content)
        self.widget.see(END)

class GUI():

    def __init__(self, root):

        self.initGUI(root)

    def initGUI(self, root):

        root.title("test")
        root.geometry("400x200+700+500")
        root.resizable = False

        self.button = Button(root, text="click", width=10, command=self.show)
        self.button.pack(side="top")

        self.scrollBar = Scrollbar(root)
        self.scrollBar.pack(side="right", fill="y")

        self.text = Text(root, height=10, width=45, yscrollcommand=self.scrollBar.set)
        self.text.pack(side="top", fill=BOTH, padx=10, pady=10)
        self.scrollBar.config(command=self.text.yview)

        sys.stdout = re_Text(self.text)    #what is sys??
        root.mainloop()

    def __show(self):

        i = 0
        while i < 3:
            print (fmtTime(time.time()))
            time.sleep(1)
            i += 1

    def show(self):
        T = threading.Thread(target=self.__show, args=())
        T.start()


if __name__ == "__main__":

    root = Tk()
    myGUI = GUI(root)