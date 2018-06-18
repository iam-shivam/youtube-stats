from tkinter import *
import configparser
import os

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.browser = IntVar()
        self.init_window()

    def init_window(self):
        self.master.title("Choose Browser")
        self.pack(fill=BOTH)
        root.resizable(False, False)
        try:
            config.read(configfile)
            selectedbrowser = int(config.get('Browser', 'selected'))
            self.browser.set(selectedbrowser)
        except:
            self.browser.set(1)

        Label(root, text= "Choose Default Web Browser To Use.\n").pack(anchor=W,fill=BOTH,padx=40,pady=5)
        Radiobutton(root, text="Google Chrome (Recommended)", variable=self.browser, value=1, command = self.save_config).pack(anchor=W,fill=BOTH,padx=10,pady=5)
        Radiobutton(root, text="Mozilla Firefox", variable=self.browser, value=2, command = self.save_config).pack(anchor=W,fill=BOTH,padx=10,pady=5)
        Radiobutton(root, text="Microsoft Edge (Not Recommended)", variable=self.browser, value=3, command = self.save_config).pack(anchor=W,fill=BOTH,padx=10,pady=5)

    def save_config(self):
        cfgfile = open(configfile, 'w+')
        try:
            config.add_section('Browser')
        except:
            print('Updating INI File')
        config.set('Browser', 'Selected', str(self.browser.get()))
        config.write(cfgfile)
        cfgfile.close()
        exit()

		
currentDirectory = os.path.dirname(os.path.realpath(__file__)).replace("\\\\","\\")
configfile = os.path.join(currentDirectory,"config.ini")
config = configparser.ConfigParser()
root = Tk()
root.geometry("300x180")
app = Window(root)
root.mainloop()
