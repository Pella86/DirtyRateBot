# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 10:32:39 2017

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================

# pyimports
import datetime
import random
import string
import math

# telepot imports
from telepot.namedtuple import (InlineKeyboardMarkup, InlineKeyboardButton)

# my imports
from Databases import Database, Data
import emoji_table as em
from LanguageSupport import _

from Category import Category
from ContentVote import ContentVote

import CategoryTags as cattag

#==============================================================================
# Helper functions & constants
#==============================================================================

def linear_map(inx, x0, y0, x1, y1):
    return y0 + (inx - x0)*(y1-y0)/(x1 - x0)

creator_id = 183961724

#==============================================================================
# # Class Categories: Main Managemnet
#==============================================================================


class Categories:

    base_path = "./data/categories/"

    def __init__(self, bot):
        # databases
        # categoires database
        self.categories_db = Database(self.base_path + "categoriesdb/")
        print("Loading categories db")
        self.categories_db.loadDb()
        
        # medias database
        self.media_vote_db = Database(self.base_path + "mediadb/")
        print("Loading media db")
        self.media_vote_db.loadDb()
        
        #   short unique identifier for media, based on number of files in the folder
        
        # generate the list containing the uids
        dmedialist = list(self.media_vote_db.values())
        uidlist = []
        for k in dmedialist:
            uidlist.append(k.getData().uid)
        
        self.uid = max(uidlist) if uidlist else 0
        
        # user database
        self.user_profile_db = Database(self.base_path + "usersprofiledb/")
        print("Loading users_profiles db")
        self.user_profile_db.loadDb()
        
        # the bot
        self.bot = bot
        
        # needed for adding categories
        self.new_cat_req = {}
        
        # needed for adding medias
        self.getupload = {}
        self.getuploadMedia = {}
        self.getuploadCategory = {}

    def sendMainMenu(self, chatid, user):
        # create the main menu

        m = "<b> prot --- Main Menu --- prot </b>\n"
        m += "<i>Choose a category to see or vote the pictures, media, belonging to it</i>\n"
        m += "\n"
        m += "<b>--- Category ---</b>\n"
        m += "START HERE!!\n"
        m += "/categories\n"
        m += "\n"
        m += "<b>--- Top media ---</b>\n"
        m += "/top_media\n"
        m += "\n"
        m += "<b>--- Profile ---</b>\n"
        m += "/profile\n"
        m += "\n"
        m += "<b>--- Upload your content ---</b>\n"
        m += "/upload\n"
        m += "\n"
        m += "<b>--- HELP ---</b>\n"
        m += "/help\n"
        m += "\n"
        
        m = _(m, user.lang_tag)

        self.bot.sendMessage(chatid, m, parse_mode = "HTML")
    

    def addCategory(self, chatid):
        # chatid must be private, checked in the handle
        self.sendSelectCategoryMenu(chatid, sort=True)
        
        m = "Send a category name\n"
        m += "<i>The name must be maximum 15 characters long and can contain only alphanumeric characters (a-b and 1-10)</i>"
        
        self.bot.sendMessage(chatid, m, parse_mode="HTML")
        self.new_cat_req[chatid] = (True, False)

    def getCategoryName(self, msg):
        chatid = msg.chat.id
        user = self.user_profile_db.getData(msg.mfrom.id).getData()
        
        if self.new_cat_req[chatid][0]:
            if (msg.content is not None and
                msg.content.type == "text" and not
                msg.content.text.startswith("/")
                ):
                
                # check validity of category name
                # a category must be max 15 character long
                categoryname = msg.content.text.lower()
                
                is_valid_name = True
                if len(categoryname) > 15:
                    is_valid_name = False
                    
                validcharset = string.ascii_lowercase + string.digits
                
                if is_valid_name:
                    for c in categoryname:
                        if c not in validcharset:
                            is_valid_name = False
                            break
                # if the name is valid
                # create a message where the buttons displays the possible tags
                if is_valid_name:
                    # create message
                    
                    #price = 1000 + int(user.getReputation() / 1000)
                    price = 0
                    
                    sdb = {}
                    sdb["catname"] = categoryname
                    sdb["price"] = em.Pstr(price, long=True)
                    m = "Select a tag for the category\n"
                    m += "<i>Your category will be banned if you have for example porn in a safe for work (SFW-tag category</i>\nThis action will cost you {price}\n\n"
                    m += "category: {catname}"
                    
                    m = _(m, user.lang_tag)
                    
                    m = m.format(**sdb)
                    
                    # create keyboard
                    
                    strtag = "nsfw"
                    cbstr = 'createcat_' + categoryname + "_" + strtag + "_" + str(price)
                    button_nsfw = InlineKeyboardButton(text=strtag, callback_data=cbstr)

                    strtag = "sfw"
                    cbstr = 'createcat_' + categoryname + "_" + strtag + "_" + str(price)
                    button_sfw = InlineKeyboardButton(text=strtag, callback_data=cbstr)
                        
                    strtag = "gore"
                    cbstr = 'createcat_' + categoryname + "_" + strtag + "_" + str(price)
                    button_gore = InlineKeyboardButton(text=strtag, callback_data=cbstr)

                    ld_row = [button_nsfw, button_sfw, button_gore]

                    keyboard = InlineKeyboardMarkup(inline_keyboard=[ld_row])

                    self.bot.sendMessage(chatid, m, parse_mode="HTML", reply_markup = keyboard)                    
                    
                    self.new_cat_req[chatid] = (True, True)
                    
                    
                else:
                    self.bot.sendMessage(chatid,_("Name not valid /add_category again", user.lang_tag))
                    self.new_cat_req[chatid] = (False, False)
            else:
                self.bot.sendMessage(chatid, _("Operation aborted (must be text and not a command) /add_category again", user.lang_tag))
                self.new_cat_req[chatid] = (False, False)



    def upload(self, msg):
        chatid = msg.chat.id
        person = msg.mfrom
        user = self.user_profile_db.getData(person.id).getData()

        if user.canUpload():
            self.getupload[chatid] = True
            self.getuploadMedia[chatid] = False
            self.getuploadCategory[chatid] = False
        else:
            self.getupload[chatid] = False
            self.getuploadMedia[chatid] = False
            self.getuploadCategory[chatid] = False

            dtime = datetime.timedelta(days = 1) - (datetime.datetime.now() - user.firstuploadtime)
            print(dtime, "\n")
            
            minutes, seconds = divmod(dtime.seconds, 60)
            hours, minutes = divmod(minutes, 60)
            
            cost = int(100 + user.getReputation()/1000)
            button_buyups = InlineKeyboardButton(
                    
            text='buy 5 uploads for' + str(em.Pstr(cost)),
            callback_data='buy_uploads_' + str(cost)
            )
            keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[button_buyups],]
            )
            rmk = keyboard

            self.bot.sendMessage(chatid, "Max upload reached! Missing {0}h and {1}m\nYou currently have {2}".format(hours, minutes, user.getPointsStr()), reply_markup = rmk)
            print("max upload reached")

    def sendUploadMedia(self, msg):
        chatid = msg.chat.id
        if self.getupload[chatid] == True:
           self.bot.sendMessage(chatid, "Send a media (picture, gif, video, ...)")
           self.getuploadMedia[chatid] = True

    def getUploadMedia(self, msg):
        chatid = msg.chat.id
        if self.getupload[chatid] and self.getuploadMedia[chatid] == True:
            if msg.content is not None:
                if msg.content.type in ["photo", "video", "document"]:
                    print("received media", msg.content.info())
                    person = msg.mfrom

                    user = self.user_profile_db.getData(person.id).getData()

                    user.tmp_content["media"] = msg.content

                    self.getuploadMedia[chatid] = "success"

                    return True
            print("Something went wrong")
            self.bot.sendMessage(chatid, "Media: Something went wrong use /upload again")
            self.getupload[chatid] = False
            self.getuploadMedia[chatid] = False
            self.getuploadCategory[chatid] = False
    
    def getCategoriesList(self):
        catlist = []
        for dcat in self.categories_db.values():
            cat = dcat.getData()
            if not cat.deleted:
                catlist.append(cat) 
        return catlist
    
    def getCategoriesNamesList(self):
        catnamelist = []
        for dcat in self.categories_db.values():
            cat = dcat.getData()
            if not cat.deleted:
                catnamelist.append(cat.name) 
        return catnamelist        
    
    def sendSelectCategoryMenu(self, chatid, ipage = None, sort = False, menu = False, topmedia=False, user = None):

        catlist = self.getCategoriesList()
        
        if sort:
            catlist = sorted(catlist, key=lambda x : x.score, reverse = True)
            
        if menu:
            querytag = "cmp"
            maxcatperpage = 3
        elif topmedia:
            querytag = "cmptm"
            maxcatperpage = 3
        else:
            querytag = "cmps"
            maxcatperpage = 5
        
        cll = len(catlist)
        maxpage = math.ceil(cll / maxcatperpage)
        
        page = 1 if ipage is None else ipage
        
        # set min value 1
        page = 1 if page < 1 else page
        
        # set max value to be max page        
        page = maxpage if page >= maxpage else page
        
        # slice the category list
        offsetmin = (page - 1) * maxcatperpage      
        offsetmax = page * maxcatperpage

        catinpage = catlist[offsetmin:offsetmax]
        
        # build the string
        m = "- Categories -\n"
        for cat in catinpage:
            if menu:
                m += self.getCategoryPage(cat, user)
            elif topmedia:
                m += self.getTopMediaPage(cat, user)
            else:
                m += "- <b>{0}</b> ({1})\nScore: {2}\n".format(cat.name, cat.tag.name, cat.score) 

        m += "Page: {0}/{1} | /main_menu".format(page, maxpage)
        
        # create keyboard
        prevpage = 1
        if page > 1:
            prevpage = page - 1
        cbprevpage = querytag + "_" + str(prevpage)
        
        bprev = InlineKeyboardButton(
                text = "< previous",
                callback_data=cbprevpage
                )
        
        nextpage = maxpage
        if page < maxpage:
            nextpage = page + 1
        cbnextpage = querytag + "_" + str(nextpage)
        
        bnext = InlineKeyboardButton(
                text = "next >",
                callback_data=cbnextpage
                ) 
        
        rmk = InlineKeyboardMarkup(inline_keyboard=[[bprev,bnext],])        
        

        if ipage is None:
            self.bot.sendMessage(chatid, m, parse_mode = "HTML", reply_markup = rmk)
        else:
            self.bot.editMessageText(chatid, m, parse_mode = "HTML", reply_markup = rmk)        
        

    def sendUploadCategory(self, msg):
        chatid = msg.chat.id
        user = self.user_profile_db.getData(msg.mfrom.id).getData()
        print("-sendUploadCategory-")
        print(self.getupload[chatid], self.getuploadMedia[chatid])

        if self.getupload[chatid] and self.getuploadMedia[chatid] == "success":
            # show categories
            self.sendSelectCategoryMenu(chatid, sort=True)
            self.bot.sendMessage(chatid, _("The media will be uploaded underthe category you chose:\nSend category name:", user.lang_tag))
            
            # set categories to be accepted
            self.getuploadCategory[chatid] = True

    def getUploadCategory(self, msg):
        chatid = msg.chat.id

        if self.getuploadCategory[chatid] == True and self.getuploadMedia[chatid] == "success":
            # get the category message categories
            
            duser = self.user_profile_db.getData(msg.mfrom.id)
            user = duser.getData() 
            
            if msg.content.type == "text":
                usercatname = msg.content.text.lower()
                # check if category is a real category
                catnamelist = self.getCategoriesNamesList()
                if usercatname in catnamelist:
                    # get the user


                    user.tmp_content["cateogry"] = usercatname
                    # preventively
                    
                    # change this might create error
                    print("try to create media")

                    # temporarily assign none to the short id
                    mediavote = ContentVote(None, user.id, user.tmp_content["media"], user.tmp_content["cateogry"])

                    # if the picture is already present
                    isoc = True
                    for media in self.media_vote_db.values():
                        if media.getData().content.file_id == mediavote.content.file_id:
                            isoc = False

                    if isoc:
                        dmediavote = Data(mediavote.id, mediavote)
                        if self.media_vote_db.isNew(dmediavote):
                            # assign here the uid
                            self.uid += 1
                            dmediavote.getData().uid = self.uid
                            
                            # add the data to the database
                            self.media_vote_db.addData(dmediavote)
                            self.media_vote_db.updateDb()
                            
                            # mange the users data
                            user.dayuploads += 1
                            user.points += 5
                            
                            # update the user data
                            duser.setData(user)
                            self.user_profile_db.updateDb()

                            # reset the upload media switches
                            self.getuploadCategory[chatid] = False
                            self.getuploadMedia[chatid] = False
                            self.getupload[chatid] = False

                            self.bot.sendMessage(chatid, _("Content uploaded successfully", user.lang_tag))
                            self.bot.sendMessage(chatid, "You earned " + str(em.Pstr(5)) + " /profile")
                            print(dmediavote.getData(), "added successfully")
                            return True
                    else:
                        self.bot.sendMessage(chatid, _("Media already in database", user.lang_tag))
                else:
                    self.bot.sendMessage(chatid, _("Category not found\nYou can add the category using /add_category", user.lang_tag))
            else:
                self.bot.sendMessage(chatid, _("Message must be text", user.lang_tag))
            self.bot.sendMessage(chatid, "Category: Something went wrong use /upload again")
            self.getuploadCategory[chatid] = False
            self.getuploadMedia[chatid] = False
            self.getupload[chatid] = False

    def showCategoryPrivate(self, chatid, user, categoryname, chatdb):
        # upon a request to show a media -> send a random media
        # construct a paging interface
        
        medialist = []
        catnamelist = self.getCategoriesNamesList()
        if categoryname in catnamelist:
            for dmedia in self.media_vote_db.values():
                media = dmedia.getData()
                if media.catname == categoryname and media.id not in user.dont_show_pics_id and not media.deleted:
                    medialist.append(media)

        nmediacat = len(medialist)
        print("category:", categoryname, "has:", nmediacat)

        if nmediacat > 0:
            media = random.choice(medialist)
            media.showMediaShow(chatid, self, chatdb=chatdb)
        else:
            self.bot.sendMessage(chatid, _("No media in this category", user.lang_tag))
            self.sendMainMenu(chatid, user)
            print("no media in this category")

    def sendProbability(self, chatid, user, userdb):
        msg = "<b> Media Probability </b>\nYour media will have the indicated probability to be shown when a person uses the command /vote_[category_name]\n\n"
        
        cat_medialist = {}
        for dmedia in self.media_vote_db.values():
            catlist = self.getCategoriesList()
            for cat in catlist:
                cat_medialist[cat.name] = []
        
        
        for dmedia in self.media_vote_db.values():
            media = dmedia.getData()
            
            if media.deleted:
                pass
            else:
                cat_medialist[media.catname].append(media)
        
        for catname, mlist in cat_medialist.items():
            print(catname, len(mlist))
            
        for catname in cat_medialist.keys():
            allprobs = []
            
            if cat_medialist[catname]:
                def getrep(x):
                     return x.getUser(userdb).getReputation() if x.id != creator_id else 0.001
                    
                maxrep = max(cat_medialist[catname], key=lambda x :getrep(x)).getUser().getReputation() 
            else:
                maxrep = 0

            totmedia = len(cat_medialist[catname])
            
            uprob = 0
            for media in cat_medialist[catname]:
                mediauser = media.getUser()
                rep =  0.001 if creator_id == mediauser.id else mediauser.getReputation()
                nmedia = sum([1 if m.getUser().id == mediauser.id else 0 for m in cat_medialist[catname]])
                
                if nmedia != 0 and math.log2(maxrep) != 0:
                    prob = math.log2(rep) / math.log2(maxrep) * 0.9 * (nmedia/totmedia)   
                else:
                    prob = 0
                allprobs.append(prob)
                if user.id == mediauser.id:
                    uprob = prob
                    
            if allprobs:
                repmax = max(allprobs)
            else:
                repmax = 1
            
            repmax = repmax if repmax else 1
             
            s = 0
            for p in allprobs:
                s += p/repmax
                
            s = s if s != 0 else 1
            

            sdb = {}

            sdb["prob"] = uprob/repmax/s * 100
            sdb["catname"] = catname
            
            msg += "-*- <b>{catname}</b> -*-\n".format(**sdb)
            msg += "Probability: <b>{prob:.0f}%</b>\n ".format(**sdb)
            msg += "\n"
        
        self.bot.sendMessage(chatid, msg, parse_mode="HTML")
        
            

    def pickMedia(self, medialist):
        usermedia = []
        reps = []
        for media in medialist:
            usermedia.append(media)
            
            user = media.getUser(self.user_profile_db)
            if user.id == creator_id:
                rep = 0.001
            else:
                rep = math.log2(user.getReputation() + 0.001)
            reps.append(rep)    
     
        rep_max = max(reps)  
        
        # choose randomly a picture
        
        # construct a weight for the probability to be shown from
        # 0 .. 0.9 
        reps_norm = []
        for rep, media in zip(reps, medialist):        
            repnew = linear_map(rep/rep_max, 0, 0, 1, 0.9)
            reps_norm.append(repnew)
        
        # chose the random media
        remix = list(zip(reps_norm, usermedia))
        random.shuffle(remix) 
        for rep, media in remix:
            test_n = random.uniform(0, 1)
            if test_n <= rep:
                # return the weighted choice
                return media 
        
        chosen_media = random.choice(usermedia) # the default media is random   
        return chosen_media
    

    def getTopMediaPage(self, category, user):
        # check if is a valid category
        m = ""

        # build the string containg the catecogry
        cattitle = "<b> " + category.getTitleStr() + " </b>"
        m  = "{0:~^30}\n".format(cattitle)
        m += "Category score: {0}\n".format(category.score)
        v, t = user.getMediaVoted(category.name, self)
        m += "<i>Voted: {0} / Total: {1}</i>\n".format(v, t)
        m += "\n"
        
        sdb = {}
        sdb["uv"] = em.upvote_emoji
        sdb["dv"] = em.downvote_emoji
        sdb["catname"] = category.name
        sdb["trophy"] = em.trophy
        
 
        m += ("{trophy} /show_top_{catname} {trophy}\n\n").format(**sdb)
        
        return m        

    def voteCategoryPrivate(self, chatid, user, categoryname):
        medialist = []
        for dmedia in self.media_vote_db.values():
            media = dmedia.getData()
            if media.catname == categoryname and media.id not in user.dont_show_pics_id and not media.deleted:
                medialist.append(media)

        nmediacat = len(medialist)
        print("category: ", categoryname, "has :", nmediacat)

        if nmediacat > 0:

            # count all the picture the user didnt vote and get the
            # reputation of each user that uploaded the media
            
            usermedia = []
            for media in medialist:
                if user.id not in media.votersids:
                    usermedia.append(media)                  

            nusermedia = len(usermedia)
            print("in this category user", user.id, "voted", nmediacat - nusermedia)

            if nusermedia > 0:
                chosen_media = self.pickMedia(usermedia)
                print("The user will vote: ", chosen_media)

                # propose picture
                chosen_media.showMediaVote(chatid, self)
            else:
                self.bot.sendMessage(chatid, _("You voted all the pictures in this category use", user.lang_tag))
                self.sendMainMenu(chatid, user)
                print("All pictures have been voted")
        else:
            self.bot.sendMessage(chatid, _("No media in this category", user.lang_tag))
            self.sendMainMenu(chatid, user)
            print("no media in this category")
        
    def getCategoryPage(self, category, user):
        # check if is a valid category
        m = ""

        # build the string containg the catecogry
        cattitle = "<b> " + category.getTitleStr() + " </b>"
        m  = "{0:~^30}\n".format(cattitle)
        m += "Category score: {0}\n".format(category.score)
        v, t = user.getMediaVoted(category.name, self)
        m += "<i>Voted: {0} / Total: {1}</i>\n".format(v, t)
        m += "\n"
        
        sdb = {}
        sdb["uv"] = em.upvote_emoji
        sdb["dv"] = em.downvote_emoji
        sdb["catname"] = category.name
        sdb["trophy"] = em.trophy
        
        if v < t: 
            m += ("{uv} /vote_{catname} {dv}\n").format(**sdb)
        else:
            m += ("{uv} /show_{catname} {dv}\n").format(**sdb)                
        m += "\n"
            

        return m

    def createMediaList(self, categoryname):
        medialist = []
        catlist = self.getCategoriesNamesList()
        if categoryname in catlist:
            category = self.categories_db.getData(categoryname).getData()
            medialist = []
            for dmedia in self.media_vote_db.values():
                media = dmedia.getData()
                if media.catname == category.name and not media.deleted:
                    medialist.append(media)
        return medialist

    def sortMediaListScore(self, medialist, nmax = None):
        mediasorted = sorted(medialist, key = ContentVote.getScore, reverse = True)

        nmax = len(mediasorted) if nmax == "all" else nmax
        
        if nmax is not None and nmax >= 0 and nmax <= len(mediasorted):
            mediasorted = mediasorted[:nmax]
        return mediasorted

    def sendShowTop(self, chatid, categoryname, nmax = None):
        # first
        catnamelist = self.getCategoriesNamesList()
        if categoryname in catnamelist:
            category = self.categories_db.getData(categoryname).getData()
            medialist = self.createMediaList(category.name)
            smedia = self.sortMediaListScore(medialist, nmax)
            for i, media in enumerate(smedia):
                beforeinfo = None
                if i == 0:
                    beforeinfo = (em.first_medal + em.trophy + em.gold_medal + " First " +
                                  em.gold_medal + em.trophy + em.first_medal)
                if i == 1:
                    beforeinfo = em.second_medal + " Second " + em.second_medal
                if i == 2:
                    beforeinfo = em.third_medal + " Third " + em.third_medal
                    
                media.showMediaShow(chatid, self, beforeinfo)
        else:
            self.bot.sendMessage(chatid, "ShowTop: Category not found")

    def sendUserUploads(self, chatid, user, nmax = None):
        usermedia = user.getUploadedContent(self)
        usermediasort = self.sortMediaListScore(usermedia, nmax)
        for media in usermediasort:
            media.showMediaShow(chatid, self)

    def generateUserList(self, sort = None, nmax = None, excluded_ids = []):

        # get the whole users list
        userlist = []
        for duser in self.user_profile_db.values():
            user = duser.getData()
            if user.id not in excluded_ids:
                userlist.append(user)

        if type(sort) == str:
            sort = [sort]

        sort = sort[::-1]

        for element in sort:
            print("sort for:", element)
            if element == "points":
                userlist.sort(key = lambda x : x.points, reverse = True)
            if element == "karma":
                userlist.sort(key = lambda x : 0 if x.getKarma() is None else x.getKarma(), reverse = True)
            if element == "rep_points":
                userlist.sort(key = lambda x : x.rep_points, reverse = True)
            if element == "reputation":
                userlist.sort(key = lambda x : 0 if x.getReputation() is None else x.getReputation(), reverse = True)

        if nmax is not None and nmax <= len(userlist) and nmax >= 0:
            userlist = userlist[:nmax]

        return userlist

    def printUserList(self, nmax = None, file = None):
        userlist = self.generateUserList(sort=["reputation", "karma", "points"],nmax=nmax)
        for user in userlist:
            print(user)
        if file is not None:
            with open(file, 'r') as f:
                for user in userlist:
                    f.write(str(user) + '\n')

    def sendUserTop(self,chatid, sort, requser, nmax = None):
        userlist = self.generateUserList(sort=sort, nmax=nmax, excluded_ids=[creator_id])
        # generate the message
        # 1. 2. 3. 4. 5. ... user ... totusers
        # make pages?
        s = '<b>--- Top 5 User Chart ---</b>\n'
        s += "\n"
        c = 0
        for i, user in enumerate(userlist):
            c += 1
            if i < 5:
                s += str(c) + ". "
                if user.id == requser.id:
                    s += "User " + user.getPrettyFormat(True)
                    print(user)
                else:
                    s += "User " + user.getPrettyFormat()
                    print(user)
                s += "\n"
                s += "\n"
            else:
                if user.id == requser.id:
                    s += "...\n"
                    s += str(c) + ". " + "User " +  user.getPrettyFormat(True) + "\n"
                    s += "\n"
                    print(user)
        s += "<i>Total Users: " + str(c) + "</i>\n"

        s += "/main_menu"

        self.bot.sendMessage(chatid, s, parse_mode = "HTML")
        
    
    def checkNickname(self, chatid, user, nickname):
        # the nickname can be min 3 char long and max 15 char long
        # the nickname must be in the alphanumeric set
        # the lowercase representation of the nickname must not be repeated
        
        is_valid = False
        if type(nickname) is str:
            if len(nickname) > 3 and len(nickname) < 15:
                is_valid = True
            else:
                self.bot.sendMessage(chatid, _("Nickname must be over 3 char and below 15 char", user.lang_tag)) 
                user.tmp_nickname = ""
        else:
            self.bot.sendMessage(chatid, _("Nickname must be string", user.lang_tag)) 
            user.tmp_nickname = ""
        
        if is_valid:
            is_ascii = True
            for c in nickname:
                if c not in string.ascii_letters + string.digits:
                    is_ascii = False
                    
                    # define variabbles
                    sdb = {}
                    sdb["character"] = c
                    
                    # define message 
                    
                    m = "This [{character}] symbol cannot be used in name\n /main_menu"
                    
                    # translate
                    m = _(m, user.lang_tag)
                    
                    # assign variables
                    
                    m = m.format(**sdb)
                    
                    
                    self.bot.sendMessage(chatid,m)
                    break
            
            if is_ascii:
                is_unique = True
                for dcuser in self.user_profile_db.values():
                    cuser = dcuser.getData()
                    if cuser.anonid.lower() == nickname.lower():
                        is_unique = False
                        self.bot.sendMessage(chatid, _("Nickname already in database\n /main_menu", user.lang_tag))
                        break
                
                if is_unique:
                    user.anonid = nickname
                    duser = Data(user.id, user)
                    user.tmp_nickname = ""
                    self.user_profile_db.setData(duser)
                    self.user_profile_db.updateDb()
                    
                    self.bot.sendMessage(chatid, _("Nickname changed successfully\n /main_menu", user.lang_tag))
                    
                    return True
                else:
                    user.tmp_nickname = ""
                    return False
            else:
                user.tmp_nickname = ""
                return False
        else:
            user.tmp_nickname = ""
            return False
                        
                        
            
