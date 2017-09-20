# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 13:52:52 2017

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================


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

    def __str__(self):
        sdb ={}
        sdb['user'] = self.userid
        sdb['uid'] = self.uid
        sdb['content'] = self.content.type
        sdb['category'] = self.catname
        return"{category} | {uid} | {content} | Uploader {user}".format(**sdb)
        
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
        return self.getKarma() * self.getReputation()

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
        sdb["score"] = self.getScore()
        
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
    
    def makeKeyboardVote(self):
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

        ld_row = [button_upvote, button_downvote]
        report_row = [button_hide, button_report]
        reportcat_row = [button_report_cat]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[ld_row, report_row, reportcat_row])
        return keyboard

    def makeKeyboardShow(self):
        hidestr = 'Hide media '+ em.hidemedia_emoji
        cbstr = 'noshow_' + str(self.uid)
        button_hide = InlineKeyboardButton(text=hidestr, callback_data=cbstr)

        reportstr = 'report ' + em.report_emoji
        cbstr = 'report_' + str(self.uid)
        button_report = InlineKeyboardButton(text=reportstr, callback_data=cbstr)

        reportstr = 'report category ' + em.report_emoji
        cbstr = 'report_cat_' + str(self.catname)
        button_report_cat = InlineKeyboardButton(text=reportstr, callback_data=cbstr)        

        report_row = [button_hide, button_report]
        reportcat_row = [button_report_cat]
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


    def showMediaVote(self, chatid, catManager):
        # shows the media wit voting options
        
        cpt = ""
        
        cpt += self.createUploaderTag(catManager.user_profile_db)

        cpt += "/vote_" + self.catname + " or /main_menu"
        
        # keyboard
        rmk = self.makeKeyboardVote()
        
        # file
        self.sendMedia(chatid, cpt, rmk, catManager.bot)
        

  
    def showMediaVotePublic(self, chatid, catManager):
        # shows the media wit voting options
        
        cpt = ""
        
        cpt += self.createUploaderTag(catManager.user_profile_db)
        
        cpt += "Category: " + self.catname + "\n"
        
        cpt += "Score: " + em.suffix_numbers(self.getScore()) + "\n"
        
        cpt += "/vote"
        
        # keyboard
 
        rmk = self.makeKeyboardVotePublic()
        
        # file
        self.sendMedia(chatid, cpt, rmk, catManager.bot)


    def showMediaShow(self, chatid, catManager, beforeinfo = None, afterinfo = None, chatdb = None):
        # just shows the media        

        # caption
        cpt = ""

        if beforeinfo:
            cpt += beforeinfo + "\n"
        
        cpt += self.createUploaderTag(catManager.user_profile_db)

        cpt += "Category: " + self.catname + "\n"

        score = em.upvote_emoji +" {0} | {1} ".format(self.upvote, self.downvote)+em.downvote_emoji+" "
        cpt += score + "Score: " + str(self.getScore()) + "\n"
        
        #if the user voted all the media in a category
        
        # if chat is private, if user did not vote all pictures in the category,
        # show /vote else display /show
        
        votedall = False
        
        if chatdb is not None:
            chat = chatdb.getData(chatid).getData()
            if chat.type == "private":
                user = catManager.user_profile_db.getData(chat.person.id).getData()
                (mediavoted, totmedia) = user.getMediaVoted(self.catname, catManager)
                if mediavoted == totmedia:
                    votedall = True
        
        if votedall:
            cpt += "/show_" + self.catname + " or /main_menu"
        else:
            cpt += "/vote_" + self.catname + " or /main_menu"
        
        if afterinfo:
            cpt += afterinfo + "\n"
        
        # Keyboard
        rmk = self.makeKeyboardShow()
        
        # File
        self.sendMedia(chatid, cpt, rmk, catManager.bot)