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
        ''' The function shows the user the main menu of the bot'''

        m = "<b> prot --- Main Menu --- prot </b>\n"
        m += "<i>Choose a category to see or vote the pictures, media, belonging to it</i>\n"
        m += "\n"
        m += "<b>--- Category ---</b>\n"
        m += "START HERE!!\n"
        m += "/categories\n"
        m += "\n"
        m += "<b>--- Top users and media ---</b>\n"
        m += "<i>The top chart of media and users by category</i>\n"
        m += "/top_media\n"
        m += "\n"
        m += "<b>--- Profile ---</b>\n"
        m += "<i>Your profile containing the information about points </i>\n"
        m += "/profile\n"
        m += "\n"
        m += "<b>--- Upload ---</b>\n"
        m += "<i>Upload your media to the bot</i>\n"
        m += "/upload\n"
        m += "\n"
        m += "<b>--- HELP ---</b>\n"
        m += "/help\n"
        m += "\n"

        m = _(m, user.lang_tag)

        self.bot.sendMessage(chatid, m, parse_mode = "HTML")
    
    def categoryPrice(self, user):
        ''' The price to create a category'''
        return (500 + int(user.getReputation() / 1000))
                
    def addCategory(self, chatid, user):
        ''' This function is called when a user wants to create a category
        chatid must be private and is checked in the handle function
        user is te requesting user
        '''
        
        # first send the available categories
        self.sendSelectCategoryMenu(chatid, sort=True)
        
        # create the message to purchase a category
        sdb = {}
        sdb["price"] = em.Pstr(self.categoryPrice(user), True)
        sdb["points"] = user.getPointsStr(True)

        m = "Send a category name\n"
        m += "<i>The name must be maximum 15 characters long and can contain only alphanumeric characters (a-z and A-Z and 1-10)</i>\n"

        m += "\n"
        m += "Create a category will cost {price} you have {points}\n"
        m += "/cancel\n"

        m = _(m, user.lang_tag)

        m = m.format(**sdb)

        self.bot.sendMessage(chatid, m, parse_mode="HTML")
        self.new_cat_req[chatid] = (True, False)

    def getCategoryName(self, chatid, user, content):
        ''' this function gets the name from the chat once the user wants to 
        add a category
        '''
        
        # check if the user requested a "add category"        
        if self.new_cat_req[chatid][0]:
            if (content is not None 
                and content.type == "text" 
                and not content.text.startswith("/")
                ):

                # check validity of category name
                # a category must be max 15 character long
                categoryname = content.text

                is_valid_name = True
                if len(categoryname) > 15:
                    is_valid_name = False

                validcharset = string.ascii_lowercase + string.ascii_uppercase + string.digits
                
                for c in categoryname:
                    if c not in validcharset:
                        is_valid_name = False
                        break

                if (is_valid_name
                    and categoryname.lower() in map(lambda s : s.lower(), list(self.categories_db.keys()))
                    and categoryname.lower() != "top"
                    ):
                    is_valid_name = False
                
                # if the name is valid
                # create a message where the buttons displays the possible tags
                if is_valid_name:
                    # create message
                    price = self.categoryPrice(user)

                    sdb = {}
                    sdb["catname"] = categoryname
                    sdb["price"] = em.Pstr(price, long=True)
                    m = "Select a tag for the category\n"
                    m += "<i>Your category will be banned if you have for example porn in a safe for work (SFW-tag category</i>\nThis action will cost you {price}\n\n"
                    m += "category: {catname}\n\n/main_menu"

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
                    self.bot.sendMessage(chatid,_("Name not valid (either character or category already present) /add_category again or /main_menu", user.lang_tag))
                    self.new_cat_req[chatid] = (False, False)
            else:
                self.bot.sendMessage(chatid, _("Operation aborted (must be text and not a command) /add_category again or /main_menu", user.lang_tag))
                self.new_cat_req[chatid] = (False, False)

    def sendMaxUploadMessage(self, chatid, user):
        ''' This function governs the max upload reached message'''
        #Calculate the time difference
        dtime = datetime.timedelta(days = 1) - (datetime.datetime.now() - user.firstuploadtime)

        minutes, seconds = divmod(dtime.seconds, 60)
        hours, minutes = divmod(minutes, 60)

        cost = int(40 + user.getReputation()/1000)
        
        button_buyups = InlineKeyboardButton(
                text='buy 5 uploads for' + str(em.Pstr(cost)),
            callback_data='buy_uploads_' + str(cost)
            )
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_buyups],])
        
        rmk = keyboard

        self.bot.sendMessage(chatid, "Max upload reached! Missing {0}h and {1}m\nYou currently have {2}".format(hours, minutes, user.getPointsStr(True)), reply_markup = rmk)
        print("max upload reached")

    def upload(self, chatid, user):
        '''This function is called when a person calls the command /upload'''

        if user.canUpload():
            self.getupload[chatid] = True
            self.getuploadMedia[chatid] = False
            self.getuploadCategory[chatid] = False
        else:
            self.getupload[chatid] = False
            self.getuploadMedia[chatid] = False
            self.getuploadCategory[chatid] = False

            self.sendMaxUploadMessage(chatid, user)

        if self.getupload[chatid] == True:
           self.bot.sendMessage(chatid, "Send a media (picture, gif, video, ...)")
           self.getuploadMedia[chatid] = True

    def getUploadMedia(self, msg):
        ''' get the media when the user posts the message ater uploading
        The next step will determine the category and the media and the 
        category will be checked
        '''
        
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
                catnamelist.append(cat.name.lower())
        return catnamelist 

    def sendSelectCategoryMenu(self, chatid, ipage = None, sort = False, menu = False, topmedia=False, user = None):
        ''' This function is sent when a person need to select from different 
        categories, different formats are given, like if it is for a menu or a
        top media menu.
        '''
        
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
            
        catinpage, page, maxpage = self.sliceListForPage(catlist, ipage, maxcatperpage)

        # build the string
        m = "<b>- Categories -</b>\n\n"
        for cat in catinpage:
            if menu:
                m += self.getCategoryPage(cat, user)
            elif topmedia:
                m += self.getTopMediaPage(cat, user)
            else:
                m += "- <b>{0}</b> ({1})\nScore: {2}\n\n".format(cat.name, cat.tag.name, cat.score)

        self.sendPage(chatid, maxpage, maxcatperpage, m, page, ipage, querytag)


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
        ''' This function is the core function of the uploading process
        the function checks if the media can be created, the function is activated only
        if the user requested an upload (either by direct posting or command /upload)
        and the user provided a category name
        
        categoryname: must be the lowercase representation of one of the category
        
        if the user chosed a valid category
        the program will try to create a media
        '''
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
                    user.tmp_content["cateogry"] = usercatname.lower()
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
        
        m += "{trophy} /user_top_{catname} {trophy}\n\n".format(**sdb)

        return m

    def voteCategoryPrivate(self, chatid, user, categoryname, chatsdb):
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
                chosen_media.showMediaVote(chatid, self, chatsdb)
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
        m += "Category score: {0}\n".format(em.suffix_numbers(category.score))
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

    def sendShowTop(self, chatid, categoryname, chatsdb, nmax = None):
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
                media.showMediaShow(chatid, self, beforeinfo, chatdb=chatsdb)
        else:
            self.bot.sendMessage(chatid, "ShowTop: Category not found")
            
    def sliceListForPage(self, the_list, ipage, max_elements_per_page):
        ''' This function prepares a list to be displayed to in pages'''
        
        cll = len(the_list)
        maxpage = math.ceil(cll / max_elements_per_page)
        
        # set minimal value
        page = 1 if ipage is None or ipage < 1 else ipage

        # set max value to be max page
        page = maxpage if page >= maxpage else page

        # slice the upload list
        offsetmin = (page - 1) * max_elements_per_page
        offsetmax = page * max_elements_per_page

        rlist = the_list[offsetmin:offsetmax]

        return rlist, page, maxpage
    
        
    
    def sendUserUploadsPage(self, chatid, user, chatdb, ipage = None):
        usermedia = user.getUploadedContent(self)
        usermediasort = self.sortMediaListScore(usermedia, "all")
        
        maxupsperpage = 5
        
        upinpage, page, maxpage = self.sliceListForPage(usermediasort, ipage, maxupsperpage)

        # build the string
        s = "----- MY UPLOADS-----\n"
        postion = (page - 1) * maxpage
        for media in upinpage:
            
            # number | mediatype | category | upvotes | downvotes | Score
            sdb = {}
            sdb["number"] = postion
            sdb["uid"] = media.uid
            sdb["mediatype"] = media.content.type
            sdb["category"] = media.catname
            sdb["upvotes"] = media.upvote
            sdb["downvotes"] = media.downvote
            sdb["score"] = media.getScore()
            sdb["upem"] = em.upvote_emoji
            sdb["doem"] = em.downvote_emoji
            
            s += "{number}. | {mediatype} | {category}\n{upvotes}{upem}{doem}{downvotes} | score: {score} \n /show_{category}_{uid}\n\n".format(**sdb)
            
            postion += 1
            

        # create keyboard
        querytag = "cmpuu"
        
        self.sendPage(chatid, maxpage, maxupsperpage, s, page, ipage, querytag)
    
    def sendPage(self, chatid, maxpage, max_elements_per_page, message, page, ipage, querytag, args = []):

        message += "/main_menu | Page: {page}/{maxpage}".format(page=page, maxpage=maxpage)
        
        # institute the previous button table
        
        
        
        m = 1
        
        bprev_list = []
        
        
        print("creation back button")
        while page / m > 1:
            
            print(page, m, page-m)
            
            if page > m:
                prevpage = page - m
                
                cb_prev = querytag + "_" + str(prevpage)
                for arg in args:
                    cb_prev += "_" + str(arg)
                
                bl_str = "<< -{}".format(m)
                
                bprev = InlineKeyboardButton(text=bl_str, callback_data=cb_prev)
                
                bprev_list.append(bprev)
            
            m *= 10
        
        
        m = 1
        
        bnext_list = []
        
        print("creation next button")
        while maxpage / m >= 1:
            
            print(page, m, page-m)
            
            if page + m <= maxpage:
                nextpage = page + m
            
                cb_next = querytag + "_" + str(nextpage)
                for arg in args:
                    cb_next += "_" + str(arg)            
        
                bl_str = "+{} >>".format(m)
                
                bnext= InlineKeyboardButton(text=bl_str, callback_data=cb_next)
                
                bnext_list.append(bnext)            
         
            m *= 10
            
        i = 0  
        in_key = []
        while i < max(len(bprev_list), len(bnext_list)):
            row = []
            if i < len(bprev_list):
                row.append(bprev_list[i])
            
            if i < len(bnext_list):
                row.append(bnext_list[i])
            
            
            i += 1
            print(" ".join(b.text for b in row))
            in_key.append(row)
            
        
        rmk = InlineKeyboardMarkup(inline_keyboard=in_key)

        if ipage is None:
            self.bot.sendMessage(chatid, message, parse_mode = "HTML", reply_markup = rmk)
        else:
            self.bot.editMessageText(chatid, message, parse_mode = "HTML", reply_markup = rmk)        


    def generateUserList(self, sort = None, nmax = None, excluded_ids = [], catnames = []):
        ''' This function generate a user list, if all the parameters are defaulted 
        the function will return the whole user list
        '''
    
        # get the whole users list
        userlist = []
        for duser in self.user_profile_db.values():
            user = duser.getData()
            
            add_user = False
            if catnames:
                usermedialist = user.getUploadedContent(self)
                for media in usermedialist:
                    if media.catname in catnames:
                        add_user = True
                 
            if user.id not in excluded_ids:
                if catnames and add_user:
                    userlist.append(user)
                if not catnames:
                    userlist.append(user)
        
        if not userlist:
            return userlist

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
    
    def sendUserTopCategory(self, chatid, requser, catnames, ipage=None):
        
        userlist = self.generateUserList(sort=["reputation", "karma"], excluded_ids=[creator_id], catnames=catnames)
        
        if userlist:
            
            maxperpage = 10
        
            ulistpage, page, maxpage = self.sliceListForPage(userlist, ipage, maxperpage)
            
            categories = [cat for cat in self.categories_db.getDataGen() if cat.name in catnames]
            

            sdb = {}
            sdb["ipos"] = (page - 1) * maxpage + 1
            sdb["endpos"] = sdb["ipos"] + maxpage
            sdb["catnames"] = "|".join(cat.screen_name for cat in categories)
                        
            s = '<b>--- For the categories: {catnames} ---</b>\n'.format(**sdb)
            s += 'Form {ipos} to {endpos} User Chart\n'.format(**sdb)
            s += "\n"   
            
            position = (page-1) * maxpage + 1
            is_user_in_page = False
            fillcharposition = "0"

            for user in ulistpage:
                # prepare the variables to be printed such position and reputation
                sdb = {}
                sdb["position"] = position
                sdb["anonid"] = user.anonid
                sdb["reputation"] = user.getReputationStr()
                sdb["karma"] = user.getKarmaStr()
                
                # if the user is in this page it gets a (you) tag and is not displayed
                # at the chart bottom
                if user.id == requser.id:
                    is_user_in_page = True
                    sdb["you"] = "(you)"
                else:
                    sdb["you"] = "" 
                   
                if  position ==  (page-1) * maxperpage + 1:
                    fillcharposition = len(str(position + maxperpage))
 
                sdb["fposition"] = "{position: <{0}}".format(fillcharposition, position=sdb["position"])
                s += "<code>{fposition}.{anonid:_^15}{you}|{reputation}|{karma}</code>\n".format(**sdb)
                
                position += 1    
        
            if not is_user_in_page:
                # find the requser position
                position = 0
                for user in userlist:
                    position += 1
                    if user.id == requser.id:
                        break
                    
                sdb = {}
                sdb["position"] = position
                sdb["anonid"] = requser.anonid
                sdb["reputation"] = requser.getReputationStr()
                sdb["karma"] = requser.getKarmaStr()
                sdb["you"] = "(you)"
                s += "...\n{position}. {anonid}{you}|R{reputation}|K{karma}\n...\n".format(**sdb)
            
            s += "\n"
            tot_users = len(userlist)
            s += "<i>Users in this category: " + str(tot_users) + "</i>\n"

            self.sendPage(chatid, maxpage, maxperpage, s, page, ipage, "cmputc") 
        else:
            self.bot.sendMessage(chatid, _("No media in this category", requser.lang_tag))
            
            


    def sendUserTop(self, chatid, requser, ipage=None):
        '''' This function sends the users topcharts 
        The first 5 users are represented in a nice page
        the subsequent in a table format
        '''
        
        userlist = self.generateUserList(sort=["reputation", "karma"], excluded_ids=[creator_id])
        
        maxperpage = 10
        ulistpage, page, maxpage = self.sliceListForPage(userlist, ipage, maxperpage)
        
        if ipage == None or ipage == 1:
            s = '<b>---{0} Top Ten User Chart {0}---</b>\n'.format(em.trophy)
            position = 1
        else:
            position =(page-1) * maxperpage + 1
            s = '<b>--- Form {} to {} User Chart ---</b>\n'.format(position, position + maxperpage)   
            
        s += "\n"

        # prepare the display of the chart 
        is_user_in_page = False
        fillcharposition = "0"
        for user in ulistpage:
            print(user)
            # prepare the variables to be printed such position and reputation
            sdb = {}
            sdb["position"] = position
            sdb["anonid"] = user.anonid
            sdb["reputation"] = user.getReputationStr()
            sdb["karma"] = user.getKarmaStr()
            
            # if the user is in this page it gets a (you) tag and is not displayed
            # at the chart bottom
            if user.id == requser.id:
                is_user_in_page = True
                sdb["you"] = "(you)"
            else:
                sdb["you"] = "" 
            
            if page == 1:
                s += "{position}. <b>{anonid}{you}</b>\n<code> R:{reputation}  K:{karma}</code> \n".format(**sdb)
            else:
                # prepare the spaces for the numbers
                fillcharposition = len(str(position + maxperpage))
                
                # set the number aligned to the left    
                sdb["fposition"] = "{position: <{0}}".format(fillcharposition, position=sdb["position"])
                
                s += "<code>{fposition}.{anonid:_^15}{you}|{reputation}|{karma}</code>\n".format(**sdb)
            
            position += 1
        
        # insert an new line if in table representation
        if page != 1:
            s += "\n"
        
        if not is_user_in_page:
            # find the requser position
            position = 0
            for user in userlist:
                position += 1
                if user.id == requser.id:
                    break
                
            sdb = {}
            sdb["position"] = position
            sdb["anonid"] = requser.anonid
            sdb["reputation"] = requser.getReputationStr()
            sdb["karma"] = requser.getKarmaStr()
            sdb["you"] = "(you)"
            s += "...\n{position}. {anonid}{you}|R{reputation}|K{karma}\n...\n".format(**sdb)
        
        # add the number of users
        s += "\n"
        tot_users = len(userlist)
        s += "<i>Total Users: " + str(tot_users) + "</i>\n"
        
        # format the page
        self.sendPage(chatid, maxpage, maxperpage, s, page, ipage, "cmput")

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

    def maintenence(self):
        # update the user and categories karma
        
        print("Updating karma...")
        for user in self.user_profile_db.getDataList():
            # get media list
            medialist = user.getUploadedContent(self)
            karma = user.calculateKarma(medialist)
            user.karma = karma
            
            self.user_profile_db.setData(Data(user.id, user))
            self.user_profile_db.updateDb()
       
        print("Updating categories db...")
        for category in self.categories_db.getDataList():
            category.calculateScore(self.media_vote_db)
            
            self.categories_db.setData(Data(category.name, category))
            self.categories_db.updateDb()
        
        
        print("Maintenence done.")