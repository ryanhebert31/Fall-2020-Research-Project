import re

from tkinter import *
from tkinter import filedialog
from nltk import PorterStemmer


### Initialize window
window = Tk()
window.title("Test GUI")
window.geometry("300x300")
window.configure(bg='white')

### Initialize frames
frmTop = Frame(window)
frmButtons = Frame(window, bg = "white")
frmMidLabels = Frame(window, bg = "white")
frmSettings = Frame(window, bg = "white")

### Initialize buttons
btnSingleFile = Button()
btnDirectory = Button()

### Initialize settings
stopWords = BooleanVar()
stopWords.set(True)
stemming = BooleanVar()
stemming.set(False)
lemn = BooleanVar()
lemn.set(False)

def lemnatize(self, words):
        sw = []
        swords = open("sw.txt", 'r')
        swords = swords.read()
        
        for word in swords.split():
            word =  word.strip()
            sw.append(word)
            
        out = ''
        porter = PorterStemmer()
        
        for word in words.split():
            if word not in sw:    
                out = out + porter.stem(word) + ' '
            
        # print(sw)
        return out

def initializeProcess(directory, singleFile):
    process = 1

def correctSettings():
    if stemming == True and lemn == True:
        stemming = False
        lemn = False
    print("Here")
        ### Error message

def openSingleFile(frm): 
    sf = True
    direct = filedialog.askopenfilename(title = "Select a file", filetypes =(("txt files", "*.txt"), ("html files", "*.html")))
    if direct:
        frm.destroy()
        initializeProcess(direct, True)

def openDirectory(frm): 
    direct = filedialog.askdirectory()
    if direct:
        frm.destroy
        initializeProcess(direct, False)

lblWelcome = Label(frmTop, text = "Welcome to the Sentiganda Analyzer!\n", foreground = "#6AD4FF", background = "black").pack()

btnSingleFile = Button(frmButtons, text= "Evaluate single file", command=openSingleFile, highlightbackground = "black", fg = "#6AD4FF")
btnSingleFile['command'] = lambda frm = frmButtons: openSingleFile(frm)
btnSingleFile.pack()

btnDirectory = Button(frmButtons, text= "Evaluate contents of a directory", command=openDirectory, highlightbackground = "black", fg = "#6AD4FF")
btnDirectory['command'] = lambda frm = frmButtons: openSingleFile(frm)
btnDirectory.pack()

cbStopWord = Checkbutton(frmSettings, text = "Stop Word Removal", variable = stopWords, onvalue = 1, offvalue = 0).pack()
cbStem = Checkbutton(frmSettings, text = "Stem Tokens", variable = stemming, onvalue = 1, offvalue = 0, command = correctSettings).pack()
cbLemn = Checkbutton(frmSettings, text = "Lemnatize Tokens", variable = lemn, onvalue = 1, offvalue = 0, command = correctSettings).pack()

frmTop.pack()
frmButtons.pack(fill = X)
frmSettings.pack()


window.mainloop()