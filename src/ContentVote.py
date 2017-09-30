# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:52:52 2017

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import datetime

# telepot imports
from telepot.namedtuple import (InlineKeyboardMarkup, InlineKeyboardButton)

# my imports
import emoji_table as em
from LanguageSupport import _

#==============================================================================
# Content Vote class, media class
#==============================================================================

class ContentVote:

    def __init__(self, uid, userid, content, catname):
        
        # ids and stuff
        self.uid = uid
        self.userid = userid # who posted this
        self.content = content #this should stay stable
        self.id = str(self.userid) + str(self.content.file_id) # media unique id
        self.catname = catname
        
        # score
        self.upvote = 0
        self.downvote = 0
        
        # user caption
        self.caption = ""
        
        # who voted for it?
        self.votersids = []
        
#        # creation messages, change it to [chatid] = creation_message so only 
#        # the last message in the chat gets updated
#        self.cmessageids = []
        
        # is the media deleted? keep the media deleted, so that they don't get
        # uploaded again (at least pictures)
        self.deleted = False

        self.reported_by = [] # person id
        
        # date
        self.creation_date = datetime.datetime.now()

    def __str__(self):
        sdb ={}
        sdb['user'] = self.userid
        sdb['uid'] = self.uid
        sdb['content'] = self.content.type
        sdb['category'] = self.catname
        sdb['creation'] = self.creation_date.strftime("%y%m%d:%Hh")
        return"{category} | {uid} | {content} | {creation}| Uploader {user}".format(**sdb)
        
    def getCategory(self, catdb):
        return catdb.getData(self.catname).getData()

    def getUser(self, userdb):
        user = userdb.getData(self.userid).getData()
        return user

    def info(self):
        
        # variable definition
        sdb = {}
        sdb["uid"] = self.uid
        sdb["content"] = str(self.content.type)
        sdb["user"] = self.getUser().id
        sdb["karma"] = self.getKarma()
        sdb["reputation"] = self.getReputation()
        sdb["deleted"] = self.deleted
        sdb["reported by"] = len(self.reported_by)
        
        # pattern definition
        s = "-Media info-\n"
        s += "Media uploaded by {user}, {uid}, {content}\n"
        s += "Media has karma {karma} and reputation {reputation}\n"
        s += "Media is deleted {deleted} and got reported by {reported by}"
        
        # translation
        s = _(s)
        
        # pattern assignment
        s = s.format(**sdb)
        return s

    def getKarma(self):
        return self.upvote - self.downvote

    def getReputation(self):
        return self.upvote + self.downvote

    def getScore(self):
        # karma times reputation / days from upload
        dtime = datetime.datetime.now() - self.creation_date
        dtime = int(dtime.days)
        return self.getKarma() * self.getReputation() / (dtime + 1)
    
    def getScoreF(self):
        score = self.getScore()
        if score >= 1:
            return "{0:.0f}".format(score)
        else:
            return "{0:.2f}".format(score)
        
    def makeKeyboardAdminPhoto(self):
        # add a button to flag the photo for deletion
        button_delete = InlineKeyboardButton(
            text='delete',
            callback_data='delete_' + str(self.uid)
            )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_delete,]])
        return keyboard

    def sendAdmin(self, chatid, bot, userdb, catManager = None, ban_keyboard = False):
        # send the message in format
        # reported media
        # user who sent the media 
        
        # send media
        
        # variable definition
        sdb = {}
        sdb["user"] = str(self.getUser(userdb).anonid)
        sdb["category"] = self.catname
        sdb["tag"] = "not defined"
        if catManager is not None:
            sdb["tag"] = str(catManager.categories_db.getData(self.catname).getData().tag)
        sdb["score"] = self.getScoreF()
        
        # pattern definition
        cpt = "User {user} upoaded the picture\n"
        cpt += "Category: {category}\n"
        cpt += "Category tag: {tag}\n"
        cpt += "Media score: {score}\n"
        
        # get category admin
        langtag = "en-EN"
        if catManager is not None:
            creatorid = catManager.categories_db.getData(self.catname).getData().creator
            if creatorid is not None:
                creator = catManager.user_profile_db.getData(creatorid).getData()
                if creator is not None:
                    langtag = creator.lang_tag
        
        
        cpt = _(cpt, langtag)
        
        cpt = cpt.format(**sdb)
        

        rmk = self.makeKeyboardAdminPhoto()
        
        
        self.sendMedia(chatid, cpt, rmk, bot)

        # send banning options
        if ban_keyboard:
            rmkban = self.getUser(userdb).makeKeyboardAdminBan()
            bot.sendMessage(chatid, "User: " + str(self.getUser(userdb)), reply_markup = rmkban )


    def makeKeyboardVotePublic(self):
        upvstr = em.upvote_emoji + " " + str(self.upvote)
        cbstr = 'v_like_' + str(self.uid)
        button_upvote = InlineKeyboardButton(text=upvstr, callback_data=cbstr)

        downvstr = em.downvote_emoji + " " + str(self.downvote)
        cbstr = 'v_dislike_' + str(self.uid)
        button_downvote = InlineKeyboardButton(text=downvstr, callback_data=cbstr)

        reportstr = em.report_emoji + ' report ' 
        cbstr = 'report_' + str(self.uid)
        button_report = InlineKeyboardButton(text=reportstr, callback_data=cbstr)

        ld_row = [button_upvote, button_downvote, button_report]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[ld_row])  
        
        return keyboard
    
    def makeKeyboardVote(self, deleteprice = 0):
        upvstr = 'like '+ em.upvote_emoji +' - ' + str(self.upvote)
        cbstr = 'v_like_' + str(self.uid)
        button_upvote = InlineKeyboardButton(text=upvstr, callback_data=cbstr)

        downvstr = 'dislike ' + em.downvote_emoji + ' - ' + str(self.downvote)
        cbstr = 'v_dislike_' + str(self.uid)
        button_downvote = InlineKeyboardButton(text=downvstr, callback_data=cbstr)

        hidestr = 'Hide media ' + em.hidemedia_emoji
        cbstr = 'noshow_' + str(self.uid)
        button_hide = InlineKeyboardButton(text=hidestr, callback_data=cbstr)

        reportstr = 'report ' + em.report_emoji
        cbstr = 'report_' + str(self.uid)
        button_report = InlineKeyboardButton(text=reportstr, callback_data=cbstr)
        
        reportstr = 'report category ' + em.report_emoji
        cbstr = 'report_cat_' + str(self.catname)
        button_report_cat = InlineKeyboardButton(text=reportstr, callback_data=cbstr) 
        
        if deleteprice != 0:
            price = em.Pstr(deleteprice)
            deletestr = 'delete {}'.format(price)
            cbstr = 'buy_delete_' + str(deleteprice) + "_" + str(self.uid)
            button_delete_pic = InlineKeyboardButton(text=deletestr, callback_data=cbstr) 

        ld_row = [button_upvote, button_downvote]
        report_row = [button_hide, button_report]
        reportcat_row = [button_report_cat]
        if deleteprice != 0:
            deletepic_row = [button_delete_pic]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[ld_row, report_row, reportcat_row, deletepic_row])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[ld_row, report_row, reportcat_row])
            
        return keyboard

    def makeKeyboardShow(self, deleteprice = 0):
        hidestr = 'Hide media '+ em.hidemedia_emoji
        cbstr = 'noshow_' + str(self.uid)
        button_hide = InlineKeyboardButton(text=hidestr, callback_data=cbstr)

        reportstr = 'report ' + em.report_emoji
        cbstr = 'report_' + str(self.uid)
        button_report = InlineKeyboardButton(text=reportstr, callback_data=cbstr)

        reportstr = 'report category ' + em.report_emoji
        cbstr = 'report_cat_' + str(self.catname)
        button_report_cat = InlineKeyboardButton(text=reportstr, callback_data=cbstr)        


        if deleteprice != 0:
            price = em.Pstr(deleteprice)
            deletestr = 'delete {}'.format(price)
            cbstr = 'buy_delete_' + str(deleteprice) + "_" + str(self.uid)
            button_delete_pic = InlineKeyboardButton(text=deletestr, callback_data=cbstr)  

        report_row = [button_hide, button_report]
        reportcat_row = [button_report_cat]
        
        if deleteprice != 0:
            deletepic_row = [button_delete_pic]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[report_row, reportcat_row, deletepic_row])       
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[report_row, reportcat_row])       
        
        return keyboard

#    def addCreationMessage(self, msg):
#        chatmsgid = (msg.chat.id, msg.message_id)
#        self.cmessageids.append(chatmsgid)

    def createUploaderTag(self, userdb):
        user = self.getUser(userdb)
        reputation = "({})".format(user.getReputationStr())

        cpt = "Uploader: " + user.anonid + " " + reputation + "\n"
        
        return cpt
    
    def sendMedia(self, chatid, cpt, rmk, bot):
        file_id = self.content.file_id
        
        if self.content.type == "photo":
            bot.sendPhoto(chatid, file_id, caption = cpt, reply_markup = rmk)
        elif self.content.type == "video":
            bot.sendVideo(chatid, file_id, caption = cpt, reply_markup = rmk)
        elif self.content.type == "document":
            bot.sendDocument(chatid, file_id, caption = cpt, reply_markup = rmk)  
    

    def showMediaVote(self, chatid, catManager, chatsdb):
        # shows the media wit voting options
        
        cat_screen_name = self.getCategory(catManager.categories_db).screen_name
        
        cpt = ""
        
        cpt += self.createUploaderTag(catManager.user_profile_db)

        cpt += "/vote_" + cat_screen_name + " or /main_menu"
        
        # keyboard
        chattinguser = None
        for tmp_duser in catManager.user_profile_db.values():
            tmp_user = tmp_duser.getData()
            if tmp_user.getChatID(chatsdb) == chatid:
                chattinguser = tmp_user
                break        
        
        delete_price = 0
        if self.userid == chattinguser.id:
            delete_price = 100 + abs(self.getReputation())

        rmk = self.makeKeyboardVote(delete_price)
        
        # file
        self.sendMedia(chatid, cpt, rmk, catManager.bot)
        

  
    def showMediaVotePublic(self, chatid, catManager):
        # shows the media wit voting options
        
        cat_screen_name = self.getCategory(catManager.categories_db).screen_name
        
        cpt = ""
        
        cpt += self.createUploaderTag(catManager.user_profile_db)
        
        cpt += "Category: " + cat_screen_name + "\n"
        
        cpt += "Score: " + em.suffix_numbers(self.getScoreF()) + "\n"
        
        cpt += "/vote"
        
        # keyboard
 
        rmk = self.makeKeyboardVotePublic()
        
        # file
        self.sendMedia(chatid, cpt, rmk, catManager.bot)


    def showMediaShow(self, chatid, catManager, beforeinfo = None, afterinfo = None, chatdb = None):
        # just shows the media        
        
        cat_screen_name = self.getCategory(catManager.categories_db).screen_name
        
        # caption
        cpt = ""

        if beforeinfo:
            cpt += beforeinfo + "\n"
        
        cpt += self.createUploaderTag(catManager.user_profile_db)

        cpt += "Category: " + cat_screen_name + "\n"

        score = em.upvote_emoji +" {0} | {1} ".format(self.upvote, self.downvote)+em.downvote_emoji+" "
        cpt += score + "Score: " + str(self.getScoreF()) + "\n"
        
        #if the user voted all the media in a category
        
        # if chat is private, if user did not vote all pictures in the category,
        # show /vote else display /show
        
        votedall = False
        chattinguser = None
        
        if chatdb is not None:
            # find the user requesting the show vote
            chat = chatdb.getData(chatid).getData()
            if chat.type == "private":
            
                for tmp_duser in catManager.user_profile_db.values():
                    tmp_user = tmp_duser.getData()
                    if tmp_user.getChatID(chatdb) == chatid:
                        chattinguser = tmp_user
                        break

                (mediavoted, totmedia) = chattinguser.getMediaVoted(self.catname, catManager)
                if mediavoted == totmedia:
                    votedall = True
        
        if votedall:
            cpt += "/show_" + self.catname + " or /main_menu"
        else:
            cpt += "/vote_" + self.catname + " or /main_menu"
        
        if afterinfo:
            cpt += afterinfo + "\n"
        
        # Keyboard
        delete_price = 0
        
        print("user id, media userid:", chattinguser.id if chattinguser else None, self.userid)
        
        if chattinguser is not None and chattinguser.id == self.userid:
            delete_price = 100 + self.getReputation()
        rmk = self.makeKeyboardShow(delete_price)
        
        # File
        self.sendMedia(chatid, cpt, rmk, catManager.bot)