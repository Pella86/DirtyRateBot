# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 07:06:41 2017

@author: Mauro
"""

# impoorts

# py imports

import time
import datetime

# Timing utils

class Logger:
    ''' This class will manage the logging '''
    
    def __init__(self, title = None, pathfile = None, debug_mode = True, debug_level = 0):
        self.path_file = pathfile
        self.debug_mode = debug_mode
        
        self.starttime = time.perf_counter()
        
        self.nowtime = time.perf_counter()
        
        self.lastcall = time.perf_counter() 
        self.debug_level = debug_level
        
        if title is not None:
            today = datetime.datetime.now()   
            s = title + " program started the " + today.strftime("%d of %b %Y at %H:%M")
            self.log("=============================================================\n" +
                     s +
                     "\n=============================================================")           


    def convert_in_ddhhss(self, seconds):
        hh = 0
        mm = 0
        ss = 0
        
        ms = str(seconds % 1)[1:5]
        
        mm, ss = divmod(int(seconds), 60)
        hh, mm = divmod(mm, 60)    
        
        return "{0:0>2}:{1:0>2}:{2:0>2}{3}".format(hh, mm, ss, ms)

    def startTimer(self):
        self.lastcall = time.perf_counter()
    
    
    def getSubTimerStr(self):
        nowtime = time.perf_counter()
        subtime =  nowtime - self.lastcall
        subtimestr = self.convert_in_ddhhss(subtime)
        s  = "Elapsed time for subprocess: {0}\n".format(subtimestr)
        return s
    
    def getTotTimeStr(self):
        nowtime = time.perf_counter()
        totaltime = nowtime - self.starttime
        totaltimestr = self.convert_in_ddhhss(totaltime)
        s = "Total elapsed time: {0}".format(totaltimestr)  
        return s             
    
    def gettimestr(self):
        self.nowtime = time.perf_counter()
        subtime =  self.nowtime - self.lastcall
        subtime = self.convert_in_ddhhss(subtime)
        s  = "Elapsed time for subprocess: {0}\n".format(subtime)
        
        totaltime = self.nowtime - self.starttime
        totaltime = self.convert_in_ddhhss(totaltime)
        s += "Total elapsed time: {0}".format(totaltime)
        
        self.lastcall = time.perf_counter()
        return s
    

    
    def log(self, title, time_sub = False, time_tot = False):
        title = title.encode('ascii', errors='replace').decode('utf-8')
        
        s = title
        if time_sub or time_tot:
            s += '\n'
        if time_sub:
            s += self.getSubTimerStr() + '\n'
        if time_tot:
            s += self.getTotTimeStr() + '\n'
        if not time_sub and not time_tot:
            s += '\n'

        if self.path_file is not None:
            with open(self.path_file, 'a') as f:
                f.write(s)
                
        if self.debug_mode:
            print(s[:-1])

