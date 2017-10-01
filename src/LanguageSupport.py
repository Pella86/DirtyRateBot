# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 17:56:25 2017

@author: Mauro
"""


# translation class
# is trying to make what gettext does with internationalization and localization
# using IEFT language tag
# 'it-IT' example

from os.path import isfile
import os

encoding = "latin-1"

class Translator:
    pass
    # the class will receive strings form the program
    # will check if the strings exists and return a translation of the string in the requested language
    # will compose a text file where the first string is the english version
    # or bot version, while the second is the translation
    # the bot will take the strings as soon as they are called, check for the 
    # translation and select the user language option
    
    def __init__(self):
        
        # define a file where one stores the tags
        # it is in the folder /data/language_tags
        
        self.lang_folder = "./languages/"
        
        if not os.path.isdir(self.lang_folder):
            os.mkdir(self.lang_folder)
        
        self.p = self.lang_folder + "language_tags.txt"
        
        self.tags = []
        
        self.langtostr = {} # key is (language-tag, string)
        
        if isfile(self.p):
            with open(self.p, 'r') as f:
                dlines = f.readlines()
            
            for line in dlines:
                if not line.startswith("#") and line.strip():
                    self.tags.append(line.strip())
        else:
            #initialize a empty file
            with open(self.p, 'w') as f:
                f.write("\n")
        
        #read the blocks
        for tag in self.tags:
            print("tag:", tag)
            dlines = []
            with open(self.getLangFileName(tag), "rb") as f:
                for line in f:
                    dlines.append(line.decode(encoding))
                    
            
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
                       
                    self.langtostr[(tag, org_str[:-2])] = tstring
                
                if dlines and line != "-----English String:\n":
                    line = dlines.pop(0)
                    

    
    def getTagFolderName(self, tag):
        return self.lang_folder + "language_" + tag + "/"
    
    def getLangFileName(self, tag):
        return self.getTagFolderName(tag) + "translation_file_" + tag + ".tr"
    
    def updateTags(self, tag):
        self.tags.append(tag)
        # write to file
        with open(self.p, "a") as f:
            f.write(tag + "\n")
            
        # open a folder with name "language_XX-XX"
        os.mkdir(self.getTagFolderName(tag))
        
        with open(self.getLangFileName(tag), 'wb') as f:
            f.write("\n".encode(encoding))
        
    def addTranslationBlock(self, string, tag):
        with open(self.getLangFileName(tag), "ab") as f:
            f.write("-----English String:\n".encode(encoding))    
            f.write(string.encode(encoding))
            
            f.write("\n\nTranslated String:\n".encode(encoding))
            f.write("\n\n".encode(encoding))


mytr = Translator()                
    
def _(string, language_tag):
    if language_tag not in mytr.tags:
        mytr.updateTags(language_tag)
    
    
    if (language_tag, string) not in mytr.langtostr:
        # append to the translation file in the folder the string
        mytr.addTranslationBlock(string, language_tag)
        mytr.langtostr[(language_tag, string)] = ""
    
    # get the translated string
    langstr = mytr.langtostr[(language_tag, string)]
    if langstr:
        return langstr
    else:
        return string
            

if __name__ == "__main__":
    print("Hello")   

    mylang = _("Hello my name is Ciao", "it-IT")    

    print(mylang)     
    
    mylang = _("Hello my name is Ciao", "de-CH")
    
    print(mylang)
    
    mylang = _("We have good news", "de-CH")
    
    print(mylang)
            
            