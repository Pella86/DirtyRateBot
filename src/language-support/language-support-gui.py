# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 12:56:02 2017

@author: Mauro
"""

# This file will help with the translation

# create a gui that takes a file in and displays on the right the test to
# translate while on the left the translated text

from tkinter import Tk, Frame, Text, LabelFrame, Menu, Button, Label, StringVar

from tkinter.filedialog import askopenfilename


encoding = "latin-1"


class TranslationWidget:
    
    
    def __init__(self, root):
        
        self.mframe = Frame(root)
        self.mframe.pack()
        
        lframe_text = LabelFrame(self.mframe, text = "Translation window")
        lframe_text.grid(row=0, column=0, columnspan=3)
        
        lframe_org = LabelFrame(lframe_text, text="Original Text")
        lframe_org.grid(row = 0, column = 0)
        
        self.original_textbox = Text(lframe_org, height=20, width=70)
        self.original_textbox.pack()
        
        lframe_tr = LabelFrame(lframe_text, text="To be translated")
        lframe_tr.grid(row = 0, column = 1)
        
        self.translation_textbox = Text(lframe_tr, height=20, width=70)
        self.translation_textbox.pack()
        
        self.menubar = Menu(self.mframe)
        self.menubar.add_command(label="Load file", command=self.loadFile )
        self.menubar.add_command(label="Save file", command=self.saveFile )
        
        self.org_tr_str = []
        
        self.last_page = None
        self.current_page = None
        
        self.prev_button = Button(self.mframe, text = "<", command=self.prev_page)
        self.prev_button.grid(row = 1, column = 0)
        
        self.page_indicator = StringVar()
        self.page_indicator.set("default")
        self.page_indicator_l = Label(self.mframe, textvariable=self.page_indicator)
        self.page_indicator_l.grid(row=1, column=1)

        self.next_button = Button(self.mframe, text = ">", command=self.next_page)
        self.next_button.grid(row = 1, column = 2) 
        
        self.filename = None
    
    def saveFile(self):
        self.save_translation(self.current_page)
        print("saving to file:", self.filename)
        with open(self.filename, "wb") as f:
            for element in self.org_tr_str: 
                f.write("-----English String:\n".encode(encoding, "ignore"))    
                f.write(element[0].encode(encoding))
                
                f.write("\n\nTranslated String:\n".encode(encoding, "ignore"))
                f.write((element[1] + "\n\n").encode(encoding, "ignore"))
        print("File saved")
            
        
        
    def loadFile(self):
        self.org_tr_str = []
        
        self.last_page = None
        self.current_page = None
        
        # ask for the file
        filename = askopenfilename(filetypes=(("Translation files", "*.tr"), ("All files", "*.*")), initialdir="../../languages/", title="Choose a translation file")
        
        self.filename = filename
        
        dlines = []
        with open(self.filename, encoding=encoding) as f:
            for line in f:
                dlines.append(line)
        
        
        #parse the content
        line = dlines.pop(0)
        while dlines:
            org_str = ""
            tstring = ""
            if line == "-----English String:\n":
                line = dlines.pop(0)
                
                while line != "Translated String:\n":
                    org_str += line
                    line = dlines.pop(0)
                
                line = dlines.pop(0)
                
                while line != "-----English String:\n" and dlines:
                    tstring += line
                    line = dlines.pop(0)
                
                while tstring.endswith("\n"):
                    tstring = tstring[:-1]
                   
                self.org_tr_str.append([org_str[:-2],tstring])
            
            if dlines and line != "-----English String:\n":
                line = dlines.pop(0)        
    
        # display the content
        self.display_content(self.org_tr_str[0])
        
        # define the pages
        self.last_page = len(self.org_tr_str)
        
        # set the initial page
        self.current_page = 0
        
        self.update_page_indicator()
        
    def update_page_indicator(self):
        self.page_indicator.set("{}/{}".format(self.current_page, self.last_page - 1))
    
    
    def display_content(self, tr_pair):
        
        original = tr_pair[0]
        
        translated = tr_pair[1]

        self.original_textbox.delete(1.0, "end")
        self.original_textbox.insert(1.0, original)
        
        self.translation_textbox.delete(1.0, "end")
        self.translation_textbox.insert(1.0, translated)
    
    def save_translation(self, page):
        self.org_tr_str[page][1] = self.translation_textbox.get(1.0, "end")
    
    def prev_page(self):
        if self.current_page is not None:
            print(self.current_page)
            
            last_page_visited = self.current_page
            
            
            self.current_page -= 1
            
            print(self.current_page)
            
            if self.current_page >= 0:
                self.save_translation(last_page_visited)

                self.display_content(self.org_tr_str[self.current_page])
            
                self.update_page_indicator()
            else:
                self.current_page += 1
    
    def next_page(self):
        if self.current_page is not None:
            self.save_translation(self.current_page)
            
            last_page_visited = self.current_page
            
            self.current_page += 1
            
            if self.current_page < self.last_page:           
                self.save_translation(last_page_visited)
                self.display_content(self.org_tr_str[self.current_page])
                
                self.update_page_indicator()
            else:
                self.current_page -= 1
        
        

if __name__ == "__main__":
    

    root = Tk()

    tw = TranslationWidget(root)    
    
    root.config(menu=tw.menubar)
    
    root.mainloop()
