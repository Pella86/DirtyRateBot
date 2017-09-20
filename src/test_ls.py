# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 13:56:59 2017

@author: Mauro
"""

from LanguageSupport import _

class TestLS:
    
    def __init__(self):
        
        self.mypoints = 10
        
    
    def showPoints(self):
        
        sdb = {}
        sdb["points"] = self.mypoints
        
        msg = "My points = {points}"
        
        msg = _(msg,  "it-IT")
        
        msg = msg.format(**sdb)
        
        return msg