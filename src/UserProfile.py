# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 17:32:22 2017

@author: Mauro
"""


#==============================================================================
# Imports
#==============================================================================

# pyimports
import datetime
import random

# telepot imports
from telepot.namedtuple import (InlineKeyboardMarkup, InlineKeyboardButton)
from telepot.exception import TelegramError

# my imports
import emoji_table as em
from LanguageSupport import _

#==============================================================================
# Constants and helper functions
#==============================================================================

MAXUPLOADS = 5

def calc_rep_cost(user, rpq):
    tmp_rep = user.getReputation()
    karma = user.getKarma()
    tmp_rp = user.rep_points
    
    total_cost = 0
    for p in range(1, rpq + 1):
        cost = (tmp_rp)*2 + (tmp_rep/1000)
        tmp_rp += p
        tmp_rep = karma * tmp_rp
        total_cost += cost
        
    print("rp quantity:", rpq, "points cost:",total_cost)
    return int(total_cost)

#==============================================================================
# User Profile class
#==============================================================================

class UserProfile:
    

    def __init__(self, person):

        # ids
        self.id = person.id
        self.anonid = str(hex(person.id + random.randint(100000000, 999999999)))[2:].upper()
        
        # I don't think I really need it I will use only the ids
        #self.person = person #this needs to disappear and make a function getUser()
        
        # user status
        self.banned = False
        self.isActive = True
        self.chatid = None
        
        # temporary creations
        self.tmp_content = {} # used to create the new post
        self.tmp_nickname = None
        self.tmp_category = {}
        
        # created categories
        self.createdCategories = {}

        # daily uploads limits
        self.uploaded_content = {} # not used?
        self.dayuploads = 0
        self.firstuploadtime = datetime.datetime.now()

        # points and karma
        self.points = 0
        self.karma = None
        self.rep_points = 1

        # options
        self.dont_show_pics_id = []
        self.receive_notifications = {}
        
        # language options
        if person.language_code is not None:
            self.lang_tag = person.language_code
        else:
            self.lang_tag = "en-EN"
        



    def makeKeyboardAdminBan(self):
        # this works on the anon id, it would be better to make it work from ID
        button_ban = InlineKeyboardButton(
            text='ban',
            callback_data='ban_' + str(self.id)
            )
        button_unban = InlineKeyboardButton(
            text='unban',
            callback_data='unban_' + str(self.id)
            )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_ban, button_unban],]
            )
        return keyboard

    def getPrettyFormat(self, youtag = False):
        sdb = {}
        sdb['anonid'] = self.anonid
        sdb['karma'] = self.getKarmaStr()
        sdb['reputation'] = self.getReputationStr()
        sdb['you'] = '(you)' if youtag == True else ''
        fstr = ("{anonid} {you}:\n"
                "<code>  Rep {reputation}| Karma {karma}</code>"
                ).format(**sdb)
        return fstr

    def getChatID(self, chatsdb):
        if self.chatid == None:
            for dchat in chatsdb.values():
                chat = dchat.getData()
                if chat.type == "private" and chat.person.id == self.id:
                    print("updating chat id...")
                    self.chatid = chat.id
                    break
        return self.chatid

    def __str__(self):
        sdb = {}
        sdb['anonid'] = self.anonid
        sdb['dup'] = self.dayuploads
        sdb['pts'] = self.points
        sdb['karma'] = self.getKarma()
        sdb['rep_pts'] = self.rep_points
        sdb['rep'] = self.getReputation()
        sdb['langtag'] = self.lang_tag

        s = "{anonid:_>15}: P{pts}/K{karma}/RP{rep_pts}/R{rep}|DUps{dup}|{langtag}".format(**sdb)
        return s

    def getUploadedContent(self, categories):
        usermedia = []
        for dmedia in categories.media_vote_db.values():
            media = dmedia.getData()
            if media.getUser(categories.user_profile_db).id == self.id and not media.deleted:
                usermedia.append(media)
        return usermedia

    def countUploadedContent(self, categories):
        nmedia = 0
        for dmedia in categories.media_vote_db.values():
            media = dmedia.getData()
            if media.getUser(categories.user_profile_db).id == self.id:
                nmedia += 1
        return nmedia

    def calculateKarma(self, usermedia):
        karma = 0
        for media in usermedia:
            karma += media.getScore()
        return int(karma)

    def getKarma(self, categories = None):
        if self.karma is None and categories is not None:
            usermedia = self.getUploadedContent(categories)
            self.karma = self.calculateKarma(usermedia)
        elif self.karma is None and categories is None:
            self.karma = 0
        
        return int(self.karma)

    def getReputation(self):
        # transform reputation points into reputation
        # self.reputation * self.karma if self.karma >= 1 else 1
        if self.getKarma() is not None:
            reputation = self.rep_points * (self.getKarma() if self.getKarma() >= 1 else 1)
        else:
            reputation = 0
        return int(reputation)

    def getPointsStr(self, long = False):
        return str(em.Pstr(self.points, long))

    def getKarmaStr(self, long = False):
        return str(em.Kstr(self.getKarma(), long))
    
    def getRepPointsStr(self, long = False):
        return str(em.RPstr(self.rep_points, long))

    def getReputationStr(self, long = False):
        return str(em.Rstr(self.getReputation(), long))
    
    def sendProfileInfo(self, chatid, bot, catManager):
        
        # variable definition
        sdb = {}
        sdb['nup'] = self.countUploadedContent(catManager)
        sdb['anonid'] = self.anonid
        sdb['dup'] = self.dayuploads
        sdb['points'] = self.getPointsStr(True)
        sdb['karma'] = self.getKarmaStr(True)
        sdb['reputation'] = self.getReputationStr(True)
        sdb['rep_points'] = self.getRepPointsStr(True)
        sdb['anon_emoji'] = em.anon_emoji
        sdb['user_face'] = em.user_face
        sdb['space_shuttle'] = em.space_shuttle
        
        
        # message pattern definition
        m = "<b>- {anon_emoji} User Profile {user_face} {space_shuttle}-</b>\n"
        m += "<i>Your anonymous id is: {anonid}</i>\n"
        m += "Change nickname: /set_nickname\n"
        m += "\n"
        m += "<b>- Current Status -</b>\n"
        m += "Points: {points} | /help_points\n"
        m += "Karma: {karma} | /help_karma\n"
        m += "Reputation points: {rep_points}\n"
        m += "Reputation: {reputation}\n/help_reputation\n"
        m += "<i>To increase your reputation use</i>\n/buy_reputation\n"
        m += "\n"
        m += "<b>- My Uploads -</b>\n"
        m += "You uploaded a total of {nup} media\n"
        m += "Today you uploaded {dup} media\n"
        m += "To see your uploaded media press\n/my_uploads\n"
        m += "\n"
        m += "<b>- Create a category -</b>\n"
        m += "/add_category\n"
        m += "\n"
        m += "<b>--- Users top chart ---</b>\n"
        m += "/user_top\n"
        m += "\n"
        m += "/main_menu"
        
        
        # message translation
        mym = _(m, self.lang_tag)
        
        # assing the patterns
        mym = mym.format(**sdb)

        bot.sendMessage(chatid, mym, parse_mode= "HTML")


    def sendNotification(self, notification_tag, notification_message, bot, chatsdb):
        # notification tags:
        #  category-vote
        #  category-newmedia
        
        if notification_tag not in self.receive_notifications:
            self.receive_notifications[notification_tag] = True

        if self.receive_notifications[notification_tag] and self.isActive:            
            button = InlineKeyboardButton(
                text= _('mute notification ', self.lang_tag) + em.report_emoji,
                callback_data='mute_' + notification_tag + '_' + str(self.id)
                )

            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button,],])

            try:
                bot.sendMessage(self.getChatID(chatsdb), notification_message, parse_mode = "HTML", reply_markup= keyboard)
            except TelegramError as tge:
                print("Send notif:", tge.description)
                self.isActive = False
            except Exception as e:
                print(e)
                raise e
    
    def canUpload(self):
        time = datetime.datetime.now()
        
        diff = time - self.firstuploadtime
        if diff > datetime.timedelta(days=1):
            self.firstuploadtime = datetime.datetime.now()
            self.dayuploads = 0
            return True
        else:
            if self.dayuploads < MAXUPLOADS:
                return True
            else:
                return False

    def sendBuyReputation(self, chatid, bot, edit=False):
        
        # variable definition
        sdb = {}
        sdb['rep_points'] = self.getRepPointsStr()
        sdb['karma'] = self.getKarmaStr()
        sdb['rep'] = self.getReputationStr()
        sdb['points'] = self.getPointsStr()
        
        # message pattern definition
        msg = "<b>--- Buy reputation ---</b>\n"
        msg += "<i>Higher reputation ensures your media will be shown first, namely more reputation,  more points</i>\n"
        msg += "\n"
        msg += "You currently have {rep_points}\n"
        msg += "You a karma of {karma}\n"
        msg += "This generates a reputation of {rep}\n"
        msg += "Reputation formula:\n <code>karma * reputation points</code>\n"
        msg += "\n"
        msg += "You have {points} points\n"
        msg += "Vould you like to buy more RP?\n"
        
        # message translation        
        msg = _(msg, self.lang_tag)      
        msg = msg.format(**sdb)
        
        blist = []
        qrp = 1
        for i in range(3):
            total_cost = calc_rep_cost(self, qrp)
            
            
            #variable def 
            sdb = {}
            sdb["qrp"] =  str(em.RPstr(qrp))
            sdb["points"] = str(em.Pstr(total_cost))
            
            buyrptext = _("Buy {qrp} for {points}", self.lang_tag)
            
            buyrptext = buyrptext.format(**sdb)

            button = [InlineKeyboardButton(text= buyrptext, callback_data = "buy_rp_" + str(qrp))]
            blist.append(button)
            qrp = (i+1)*2
            
        button = [InlineKeyboardButton(text=_("Calculate media probability (not working)", self.lang_tag),
                                       callback_data = "buy_calcp"),]
        blist.append(button)
        rmk = InlineKeyboardMarkup(inline_keyboard = blist)
   
        if edit:
            assert type(chatid) == tuple and len(chatid) == 2
            bot.editMessageText(chatid, msg, parse_mode="HTML", reply_markup = rmk)
        else:
            bot.sendMessage(chatid, msg, parse_mode="HTML", reply_markup = rmk)
    
    def getMediaVoted(self, catname, categories):
        # this function gets the number of media voted in a category
        # will return the tuple (voted, total)
        
        category = categories.categories_db.getData(catname).getData()
        
        medialist = category.getMediaList(categories.media_vote_db)
        
        votedcount = 0
        
        for media in medialist:
            if self.id in media.votersids or media.id in self.dont_show_pics_id:
                votedcount += 1
        
        totmedia = len(medialist)
        
        return (votedcount, totmedia)
                
        
        
            
 

     
   