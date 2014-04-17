import Tkinter as tk
import tkFileDialog
import tkMessageBox
import createIndex
import test
import time
from threading import Thread
#import _tkinter # with underscore, and lowercase 't'

from whoosh import index
from whoosh.qparser import QueryParser
from whoosh import scoring
from subprocess import call

class Window:
    def __init__(self, master=None):
        self.form = tk.Tk()
        self.layout();
        self.searchButton["command"] = self.search
        #keep main loop
        self.form.mainloop()
    def layout(self):
        # The grid setting
        self.form.columnconfigure(0, weight=0)
        self.form.columnconfigure(1, weight=1)
        self.form.columnconfigure(2, weight=0)
        self.form.columnconfigure(3, weight=0)
        self.form.rowconfigure(0, weight=0)
        self.form.rowconfigure(1, weight=1)
        self.form.rowconfigure(2, weight=1)
        
        #UIs layout
        self.searchText = tk.Label(self.form)
        self.searchText["text"] = "Search:"
        self.searchText.grid(row=0, column=0,sticky=tk.W)
        
        self.searchField = tk.Entry(self.form)
        self.searchField.grid(row=0, column=1, sticky= "WE")
        
        self.searchButton = tk.Button(self.form, text='search')
        self.searchButton.grid(row=0,column = 3)

        self.buildIndexButton = tk.Button(self.form, text='buildIndex')
        self.buildIndexButton.grid(row=1,column = 3,sticky="N")
        self.buildIndexButton["command"] = self.buildIndex
        
        self.buildIndexButton = tk.Button(self.form, text='CleanIndex')
        self.buildIndexButton.grid(row=3,column = 3,sticky="N")
        self.buildIndexButton["command"] = self.cleanIndex

        self.outputBox = tk.Text(self.form, state="disabled")
        self.outputBox.grid(row=1,column = 0, columnspan=3,rowspan=3, sticky= "NEWS")
        
        self.entryScroll = tk.Scrollbar(self.form, orient=tk.VERTICAL,command=self.outputBox.yview)
        self.entryScroll.grid(row=1,column = 2,rowspan=3, sticky="NEWS")
        self.outputBox.config(yscrollcommand=self.entryScroll.set)
        
    def search(self):
        #clean all text and wait hint
        self.cleanAndLine("Wait...")
        try:
            myindex = index.open_dir("index")
            #the TF_IDF searching strategy setting
            searcher = myindex.searcher(weighting=scoring.TF_IDF())
            #search target and set schema
            qp = QueryParser("content", schema=myindex.schema)
            #set search text
            q = qp.parse(self.searchField.get())
            results = searcher.search(q, limit=None)
            #output
            self.line("Get %r data" %(len(results)))
            self.line("Query : %r" %(q))
            for x in results:
                self.line("docId = %5r , score = %r" %(x['docId'], x.score))
        except:
            self.clean()
            self.line("ERROR!! May be don't have index!\n press buildIndex first!")
    def buildIndex(self):
        self.cleanAndLine("Wait...")
        #open a file dialog to get the file
        file_path = tkFileDialog.askopenfilename()
        if file_path == "":
            print "Cancel BuildIndex"
            return
        #reset the index file
        createIndex.deleteIndex(u"index")
        createIndex.createIndex(u"index")
        
        #open file thread
        t = Thread(target=self.buildIndexThread, args=(file_path,))
        time.sleep(1)
        t.start()
            
    def line(self,string):
        self.outputBox.config(state="normal")
        self.outputBox.insert(tk.END, string)
        self.outputBox.insert(tk.END, "\n")
        self.outputBox.config(state="disabled")
    def clean(self):
        self.outputBox.config(state="normal")
        self.outputBox.delete(1.0, tk.END)
        self.outputBox.config(state="disabled")
    def cleanAndLine(self,string):
        self.outputBox.config(state="normal")
        self.outputBox.delete(1.0, tk.END)
        self.outputBox.insert(tk.END, string)
        self.outputBox.insert(tk.END, "\n")
        self.outputBox.config(state="disabled")
    def cleanIndex(self):
        createIndex.deleteIndex(u"index")
        tkMessageBox.showinfo("Index", "Cleaned!")
    def buildIndexThread(self,path):
        try:
            test.run(path)
        except:
            self.clean()
            self.line("Build Index error!!\n Please select current file!!")
    

if __name__ == '__main__':
    window = Window()

    
