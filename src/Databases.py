# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 11:07:51 2017

@author: Mauro
"""

# create a users database

# create a content daatabase for fast access to content

# create a chat database to keep track of new chats
import os
import pickle

#==============================================================================
# # Helper functions
#==============================================================================

def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = os.path.split(path)
    name, ext = os.path.splitext(nameext)
    return path, name, ext

#==============================================================================
# # Databases
#==============================================================================

class Data:
    
    def __init__(self, dataid, data):
        self.id = dataid
        self._data = data
        self.hasChanged = True
    
    def getData(self):
        return self._data
    
    def setData(self, data):
        self._data = data
        self.hasChanged = True
        
    def __str__(self):
        sid = ""
        if len(self.id) > 10:
            sid = self.id[:10]
        else:
            sid = self.id
        return "data id: {0} | mod {2} | data: {1}".format(sid, self._data, self.hasChanged)
    

class Database:
    
    def __init__(self, dbfolder):
        self.dbfolder = dbfolder
        self.database = {}
        
    def keys(self):
        return self.database.keys()
    
    def items(self):
        return self.database.items()
    
    def values(self):
        return self.database.values()
    
    def isNew(self, data):
        if data.id in self.database:
            return False
        print("data not in database, so is new")
        return True
    
    def getDataList(self):
        dlist = []
        for delement in self.database.values():
            element = delement.getData()
            dlist.append(element)
        return dlist

    def getDataGen(self):
        for delement in self.database.values():
            element = delement.getData()
            yield element
        
    
    def getData(self, dataid):
        return self.database[dataid]
    
    def setData(self, data):
        self.database[data.id] = data

    
    def addData(self, data):
        self.database[data.id] = data
    
    def loadDb(self):
        # for file in folder if extension is pickle load
        names = [os.path.join(self.dbfolder, f) for f in os.listdir(self.dbfolder)]
        
        tmp_db = {}
        c = 0
        for name in names:
            _ , _ , ext = get_pathname(name)
            if ext == ".pickle" and os.path.isfile(name):
                
                with open(name, 'rb') as f:
                    data = pickle.load(f)
                tmp_db[data.id] = data
                c += 1
            
        print("Loaded", c, "items")
        self.database = tmp_db
    
    def saveDb(self):
        # write the whole database again
        
        for data in self.database.values():
            filename = self.dbfolder + str(data.id) + ".pickle"
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
    
    def updateDb(self):
        # save only the ones that have changed
        for data in self.database.values():
            if data.hasChanged:
                filename = self.dbfolder + str(data.id) + ".pickle"
                with open(filename, 'wb') as f:
                    pickle.dump(data, f)
                data.hasChanged = False

    def updateDatabaseEntry(self, attributes, success_file = ""):
        if os.path.isfile(success_file):
            raise Exception("File already exist")
            
        for delement in self.database.values():
            element = delement.getData()
            for attr_name, attr_value in attributes.items():
                element.__setattr__(attr_name, attr_value(element))
            delement.setData(element)
        self.updateDb()
        
        if success_file:
            with open(success_file, "w") as f:
                f.write("success: " + self.dbfolder)
    
    
        