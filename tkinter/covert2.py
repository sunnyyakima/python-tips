
from tkinter import *
from tkinter.filedialog import askopenfilenames, askdirectory
from tkinter.messagebox import showerror
#import pandas as pd
from functools import partial
from utility import *
import os
import glob
import xlrd
import time


def passName_v1(fileName):  # convert file from Gene Panel Version 1 file (*.txt)  to N of 1 (*.tsv) 
    fileName = [item for sublist in fileName for item in sublist]
    for file1 in fileName:
        temp = file1.split("/")
        outpath = "/".join(temp[:-1])
        outfile = file1
        outfile = re.sub(r".tsv$", "2.tsv", outfile)  
        outfile = re.sub(r".txt$", ".tsv", outfile)  

        inData_0 = parseIn(file1)
        outData  = convert2N_of_1_v1(inData_0)
        write2file(outfile, Header_Nof1 + "\t" + Header_Additional, outData)
#    write2excel(outfile, Header_Nof1 + "\t" + Header_Additional, outData)


def passDir(inDir):     # inDir is a list
#    print(inDir[-1])
    for filename in glob.glob(os.path.join(inDir[-1], '*.tsv')):
        outfile = []
        outfile.append(filename)
    passName(outfile)

def passDir_xls(inDir):
    for filename in glob.glob(os.path.join(inDir[-1], '*.xls')):
        temp = filename.split("/")
        outpath = "/".join(temp[:-1])

        t=int(time.time())
        outfile = filename
        if(re.search("_forReview_", outfile)):
            temp =outfile.split("_forReview_")
            outfile = temp[0]
        else:
            outfile = re.sub(r".xls$", "", outfile)
        
        outfile = outfile + '_toNof1_'+str(t)+'.txt'

        wb = xlrd.open_workbook(filename)
        #wb.sheet_names()
        sh = wb.sheet_by_index(0)
#        num_cols = sh.ncols 
        my_file = open(outfile, "w")
        for row_idx in range(0, sh.nrows):
            for col_idx in range(0, 16):
                cell_obj = sh.cell(row_idx, col_idx)
                content = re.sub(r"\'", "", str(cell_obj))
                content = re.sub(r"text:", "", content)
                content = re.sub(r"empty:", "", content)
                my_file.write(content+"\t")
            my_file.write("\n")
            


class MyFrame(Frame):
    
    FileName = []
    DirName  = []

    def __init__(self):

        Frame.__init__(self)
        self.master.title("Convert to NofONE format")
        self.master.rowconfigure(5, weight=50)
        self.master.columnconfigure(5, weight=100)
        self.grid(sticky=W+E+N+S)
        self.master.minsize(width=400, height=500)
        
        self.button1 = Button(self, text=" Get variantStudio file ",   command=self.load_file1,  width=20)
        self.button1.grid(row=1, column=0, sticky=W)        
#        action_with_arg = partial(passName, self.FileName)  # pass FileName to function passName
        self.button3 = Button(self, text="submit file", command=self.passName, width=20)
        self.button3.grid(row=1, column=2, sticky=W)

#        self.button2 = Button(self, text=" Get folder with VS files ", command=self.load_folder, width=20)
#        self.button2.grid(row=2, column=0, sticky=W)
#        action_with_arg2 = partial(passDir, self.DirName)  # pass DirName to function passDir
#        self.button4 = Button(self, text="submit folder", command=action_with_arg2, width=20)
#        self.button4.grid(row=2, column=2, sticky=W)

        self.button5 = Button(self, text=" Get Version 1 file ", command=self.load_file2, width=20)
        self.button5.grid(row=3, column=0, sticky=W)
        action_with_arg3 = partial(passName_v1, self.FileName)  # pass FileName to function passName_v1
        self.button6 = Button(self, text="submit file", command=action_with_arg3, width=20)
        self.button6.grid(row=3, column=2, sticky=W)

        self.button7 = Button(self, text=" Get folder with Excel ", command=self.load_folder, width=20)
        self.button7.grid(row=5, column=0, sticky=W)
        action_with_arg4 = partial(passDir_xls, self.DirName)  # pass FileName to function passName_v1
        self.button8 = Button(self, text="submit folder", command=action_with_arg4, width=20)
        self.button8.grid(row=5, column=2, sticky=W)


    def load_file1(self):
        while len(self.FileName) > 0 : self.FileName.pop()
        fname = askopenfilenames(filetypes=(("TSV files","*.tsv"),("TXT files","*.txt"),("All files","*.*") ))

        if fname:
            try:                
                self.FileName.append(fname)      # FileName is a list
                self.FileName = [item for sublist in self.FileName for item in sublist]

                additional_window = Toplevel()   #***********HERE*******
                additional_window.geometry('500x300')
                additional_window.title("prograss")
                pathNname = fname[0].split("/")
                message_display = "First file name: "+pathNname[-1]+"\n\nQuality_threshold: "+str(Quality_threshold)+"\n\nReadDep threshold: "+str(Read_depth)+"\n\n"
                msg = Message(additional_window, text=message_display)
                msg.config(bg='lightgreen', font=('times', 14, 'italic'), justify=LEFT, aspect=500)
                msg.pack()
                button = Button(additional_window, text="Dismiss", command=additional_window.destroy)
                button.pack()
            except:                              # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def load_file2(self):  # this is for converting file from version ONE
        fname = askopenfilenames(filetypes=(("TXT files","*.txt"),("TSV files","*.tsv"),("All files","*.*") ))
        if fname:
            try:
                self.FileName.append(fname)      # FileName is a list

            except:                              # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
            return

    def load_folder(self):
        dir_opt = {}
        dir_opt['initialdir'] = '.'
        dir_opt['mustexist'] = False
        dir_opt['parent'] = self
        dir_opt['title'] = 'Please select directory'
        result = askdirectory(**dir_opt)
#        print(result)

        self.DirName.append(result)        

    def passName(self):
#        print(self.FileName)
#        fileName = [item for sublist in self.FileName for item in sublist]
#        print(fileName)
       
        for file1 in self.FileName:
            temp = file1.split("/")
            outpath = "/".join(temp[:-1])

            t=int(time.time())
            outfile = file1
            sufx = '_forReview_'+str(t)
            outfile = re.sub(r".tsv$", sufx, outfile)
            outfile = re.sub(r".txt$", sufx, outfile)

            inData_0 = parseIn(file1)
            inData_1 = filter_qual(inData_0)   ## using default: Quality=Quality_threshold, Reads=Read_depth
            inData_2 = filter_qual2(inData_1)
            inData_3 = filter_knowns(inData_2)
            outData  = convert2N_of_1(inData_3)
#    while len(self.FileName) > 0 : self.FileName.pop()
#    fileName = []
            write2excel(outfile, Header_Nof1 + "\t" + Header_Additional, outData)



        
if __name__ == "__main__":
    MyFrame().mainloop()
    
