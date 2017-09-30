# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 15:09:58 2017

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

# pyimports
import datetime

# telepot imports
from telepot.namedtuple import (InlineKeyboardMarkup, InlineKeyboardButton)

# my imports
import emoji_table as em


#==============================================================================
# # Class Category
#==============================================================================

class Category:

    def __init__(self, name, tag = None, creator = None):
        self.name = name.lower() # string max 15 characters in the ascii set
        
        self.screen_name = name
        
        self.creation_date = datetime.datetime.now()
        
        self.description = ""
        
        self.tag = tag # SFW | NSFW | GORE 
        
        self.default = False
        
        self.score = 0
        
        self.deleted = False
        
        self.creator = creator
        
        self.reported_by = []
    
    def __str__(self):
        
        sdb = {}
        
        sdb["name"] = self.name
        sdb["tag"] = str(self.tag)
        sdb["default"] = self.default
        sdb["score"] = self.score
        
        strf = "{name:^15}|{tag:^8}|def:{default}|{score}".format(**sdb)
        
        return strf
    
    def getTitleStr(self):
        sdb = {}
        
        sdb["name"] = self.screen_name
        sdb["tag"] = str(self.tag)
        
        strf = "{name} ({tag})".format(**sdb)
        return strf
    
    def getScoreStr(self):
        s = "Score: {}".format(em.suffix_numbers(self.score))
        return s
    
    def calculateScore(self, mediadb):
        score = 0
        for dmedia in mediadb.values():
            media = dmedia.getData()
            if media.catname == self.name:
                score += media.getScore()
        self.score = score  
    
    def getScore(self):
        return self.score
    
    def getMediaList(self, mediadb):
        medialist = []
        for dmedia in mediadb.values():
            media = dmedia.getData()
            if media.catname == self.name and not media.deleted:
                medialist.append(media)
        return medialist
    
    def getTotMedia(self, mediadb):
        l = self.getMediaList(mediadb)
        return len(l)

    def getVotedCount(self, mediadb, user):
        ccvoted = 0
        ccmedia = 0
        for dmedia in mediadb.values():
            media = dmedia.getData()

            if not media.deleted and media.catname == self.name and media.id not in user.dont_show_pics_id:
                ccmedia += 1

                if user.id in media.votersids:
                    ccvoted += 1 

        return (ccvoted, ccmedia)  

    def sendAdmin(self, chatid, catManager):
        # variable definition
        sdb = {}
        sdb["cat_creator"] = str(self.creator)
        sdb["category"] = self.name
        sdb["nmedia"] = len(self.getMediaList(catManager.media_vote_db))
        sdb["tag"] = str(self.tag)

        
        # pattern definition
        cpt =  "Category creator: {cat_creator}\n"
        cpt += "Category        : {category}\n"
        cpt += "Number of media : {nmedia}\n"
        cpt += "Tag             : {tag}\n"

        
        cpt = cpt.format(**sdb)

        button_delete = InlineKeyboardButton(
            text='delete category',
            callback_data='delete_cat_' + str(self.name)
            )
        rmk = InlineKeyboardMarkup(inline_keyboard=[[button_delete,]])
        
        catManager.bot.sendMessage(chatid, cpt, reply_markup=rmk)
        
        # send banning options
        if self.creator is not None:
            creator = catManager.user_profile_db.getData(self.creator).getData()
            rmkban = creator.makeKeyboardAdminBan()
            
            catManager.bot.sendMessage(chatid, "Category creator: " + str(creator), reply_markup = rmkban )
        
