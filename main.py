# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 08:58:19 2017

@author: Mauro
"""

__version__ = "0.1.0"


# import sys to access the src folder
import sys
sys.path.append("./src")


#%% imports

# py imports
import time
import pickle
import datetime
import urllib3

import random


# my imports
from LogTimes import Logger

from MessageParser import Message, Person, CbkQuery, ChatMember, VALID_MEDIA
from Databases import Database, Data
from UserProfile import UserProfile
from Category import Category
from SuperGroup import SuperGroup
from ContentVote import ContentVote
from CategoriesManager import Categories
from LanguageSupport import _

import emoji_table as em
import HelpMessages as Helpmsg
import CategoryTags as tags

# telepot imports
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import (InlineQueryResultArticle, InputTextMessageContent,
                                ForceReply)
from telepot.exception import TelegramError

#%% initialization telegram ports
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

#%% constants
# creator constants
creator_id = 183961724
creator_chatid = 183961724

# bot constants
class BotDataReader:

    def __init__(self):
        self.botfile = "./botdata/bot_data.tbot"

        with open(self.botfile, "r") as f:
            dlines = f.readlines()

        self.id = int(dlines[0].strip().split("=")[1])
        self.tag = dlines[1].strip().split("=")[1].strip(' "')
        self.token = dlines[2].strip().split("=")[1].strip(' "')

        print(self.id)
        print(self.tag)
        print(self.token)

dbot = BotDataReader()
bot_id = dbot.id
bot_tag = dbot.tag
bot_token = dbot.token


# program constants
MAXUPLOADS = 5
not_enoug_money_msg = "You don't have enough points to buy it!\n/main_menu | /help_points"
add_categories_request_msg = "Pick categories to add in the group, comma separated (cat1, cat2, cat3), by replying to this message..."

rem_categories_request_msg = "Pick categories to remove from the group, comma separated (cat1, cat2, cat3), by replying to this message..."

#%% TO DO

# create announcment class

# restructure upload
# Introduce anonymous vs. not anonymous post
#   restructure the menu so that

# create anti spam

# construct a showing interface for the media
#  example -> prev < top random > next

# make category inline

# share in group chat

# create database inspector

# !lua return sendChatAction(-1001065772922, 'typing')

#%% Helper functions

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



# %% Handle functions
#==============================================================================
# # handle function: Manage received messages
#==============================================================================

def handle(msg):

    mymsg = Message(msg, False)

    if mymsg.chat.type == "supergroup" or mymsg.chat.type == "group":

        mymsg.initOptionals()

        chatid = mymsg.chat.id
        userid = mymsg.mfrom.id

        # create a instance of supergroup
        if chatid in supergroupsdb.database:
            dspg = supergroupsdb.getData(chatid)
            spg = dspg.getData()
        else:
            lg.log("New supergroup registered " + mymsg.chat.title)
            spg = SuperGroup(chatid)
            spg.initCategories(categories.categories_db)
            dspg = Data(spg.id, spg)

            bot.sendMessage(chatid, "Hello, I'm a bot to share and rate pictures, use the command /vote, admins of this chat can /set_categories which will be shown, for more information talk to me in private.")

            supergroupsdb.addData(dspg)
            supergroupsdb.updateDb()


        # test chat member from telepot.getChatMember(chatid, personid)
        if mymsg.content is not None and mymsg.content.type == "text":

            member = ChatMember(bot.getChatMember(chatid, userid))

            if member.status == "creator" or member.status == "administrator":

                mymsg.initOptionals()

                # read the texts and use the set_category / cancel_category
                if mymsg.content.text == "/set_porngore":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("porngore set for group " + str(spg.id))
                    spg.setPornGore()

                    bot.sendMessage(chatid, "The bot will show NSFW content mainly porn and gore.")
                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()

                elif mymsg.content.text == "/rem_all":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("removed all categories for group " + str(spg.id))

                    spg.remAll()
                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()

                    bot.sendMessage(chatid, "All the categories removed, bot will be silent.")

                elif (spg.wait_category and
                      mymsg.reply is not None and
                      mymsg.reply.content is not None and
                      mymsg.reply.content.type == "text" and
                      (mymsg.reply.content.text == add_categories_request_msg or
                       mymsg.reply.content.text == rem_categories_request_msg
                       )
                   ):

                    usermsg = mymsg.content.text

                    catnames = usermsg.strip().split(",")
                    catnames = map(str.strip, catnames)
                    cs = []
                    if mymsg.reply.content.text == add_categories_request_msg:
                        cs = spg.setCategories(catnames, categories.categories_db)
                        if cs:
                            catstr = "".join([catname+" | " for catname in cs])[:-3]
                            valmsg = "The bot will show media from: " + catstr
                    elif mymsg.reply.content.text == rem_categories_request_msg:
                        cs = spg.remCategories(catnames, categories.categories_db)
                        if cs:
                            catstr = "".join([catname+" | " for catname in cs])[:-3]
                            valmsg = "The bot will NOT show media from: " + catstr

                    if not cs:
                        valmsg = "No valid category detected"

                    bot.sendMessage(chatid, valmsg)

                    spg.wait_category = False

                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()
                    lg.log("------------ NEW MESSAGE ------------")

                    lg.log("user in group: " + str(spg.id) + " tried to add " + mymsg.reply.content.text)

                elif mymsg.content.text == "/set_categories":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("called set category in group" + str(spg.id))
                    # show the avaliable categories
                    spg.sendPickCategories(categories)
                    frep = ForceReply()
                    bot.sendMessage(chatid, text=add_categories_request_msg, parse_mode="HTML", reply_markup=frep)
                    spg.wait_category = True

                elif mymsg.content.text == "/rem_categories":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("called rem category in group" + str(spg.id))
                    # show the avaliable categories
                    spg.sendPickCategories(categories)
                    frep = ForceReply()
                    bot.sendMessage(chatid, text=rem_categories_request_msg, parse_mode="HTML", reply_markup=frep)
                    spg.wait_category = True

                elif mymsg.content.text == "/set_kinky":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("called set kinky in group" + str(spg.id))
                    spg.setKinky()

                    bot.sendMessage(chatid, "The bot will show NSFW content from the categories boobs, booty, bdsm, hentai, lesbian.")

                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()

                elif mymsg.content.text == "/set_all":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("called set all in group" + str(spg.id))
                    spg.setAll()
                    bot.sendMessage(chatid, "The bot will show NSFW content from the all the categories.")

                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()

                elif mymsg.content.text == "/reset_all":
                    lg.log("------------ NEW MESSAGE ------------")
                    lg.log("called reset category in group" + str(spg.id))
                    spg.initCategories(categories.categories_db)
                    bot.sendMessage(chatid, "The bot will show content (SFW) from categories nature space and meme.")

                    dspg = Data(spg.id, spg)
                    supergroupsdb.setData(dspg)
                    supergroupsdb.updateDb()

            if mymsg.content.text.startswith("/vote"):
                lg.log("------------ NEW MESSAGE ------------")
                # just get a random media and show it
                print("vote called.")
                # get all non deleted medias
                spg.sendMedia(categories)


    # remember the files uploaded to the bot
    if mymsg.chat.type == "private":
        lg.log("------------ NEW MESSAGE ------------")
        mymsg.initOptionals()

        # is the person in the userprofiledb?
        if categories.user_profile_db.isNew(mymsg.mfrom):
            lg.log("New profile created")
            person = UserProfile(mymsg.mfrom)
            d = Data(person.id, person)
            categories.user_profile_db.addData(d)
            categories.user_profile_db.updateDb()

        user = categories.user_profile_db.getData(mymsg.mfrom.id).getData()
        user.isActive = True
        lg.log(str(user))

        # process messages
        if user.banned:
            lg.log(str(user.person) + "is banned")
            bot.sendMessage(mymsg.chat.id, _("You are banned prot!"))
        else:

            cat_req = categories.new_cat_req.get(mymsg.chat.id)
            if cat_req is not None and cat_req[0]:
                lg.log("create category: get category")
                categories.getCategoryName(mymsg)

            elif mymsg.chat.id in categories.getuploadCategory and categories.getuploadCategory[mymsg.chat.id]:
                lg.log("create MediaVote: get category")
                categories.getUploadCategory(mymsg)
                categories.sendMainMenu(mymsg.chat.id, user)

            elif mymsg.chat.id in categories.getuploadMedia and categories.getuploadMedia[mymsg.chat.id] and categories.getuploadMedia[mymsg.chat.id] != "success":
                lg.log("create MediaVote: get media")
                success = categories.getUploadMedia(mymsg)
                if success:
                    categories.sendUploadCategory(mymsg)

            elif mymsg.content_type in VALID_MEDIA:
                # set the user requests as valid
                print("got media..")
                user.tmp_content["media"] = mymsg.content
                categories.getupload[mymsg.chat.id] = True

                categories.getuploadMedia[mymsg.chat.id] = "success"

                categories.sendUploadCategory(mymsg)


            elif mymsg.content is not None and mymsg.content.type == "text":

                if mymsg.content.text == "/add_category":
                    lg.log("requested add category")
                    categories.addCategory(mymsg.chat.id)

                elif mymsg.content.text.startswith("/categories"):
                    # send the categories page
                    lg.log("requested categories")
                    categories.sendSelectCategoryMenu(mymsg.chat.id, sort=True, menu=True, user=user)

                elif mymsg.content.text == "/top_media":
                    categories.sendSelectCategoryMenu(mymsg.chat.id, sort=True, topmedia=True, user=user)

                elif mymsg.content.text == "/set_nickname":
                    user.tmp_nickname = True
                    bot.sendMessage(mymsg.chat.id, _("Please send your nickname, the nickname must be minumum 3 characters and maximum 15, it can contain only alphanumeric characters (a-z, A-Z, 0-9)", user.lang_tag))

                elif user.tmp_nickname:
                    nickname = mymsg.content.text
                    success = categories.checkNickname(mymsg.chat.id, user, nickname)

                    if success:
                        lg.log("User changed nickname " + nickname)
                    else:
                        categories.sendMainMenu(mymsg.chat.id, user)

                elif mymsg.content.text.startswith("/help"):

                    #split the content

                    command = mymsg.content.text.split('_')
                    command_length = len(command)

                    if command_length == 1:
                        lg.log("requested help")
                        #send help message

                        help_msg = Helpmsg.help_msg(__version__, user.lang_tag)
                        bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")

                    elif command_length == 2:

                        helpcat = command[1]

                        if helpcat == "karma":
                            lg.log("requested help karma")

                            help_msg = Helpmsg.help_msg_karma(user.lang_tag)
                            bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")

                        elif helpcat == "points":
                            lg.log("requested help points")
                            help_msg = Helpmsg.help_msg_points(user.lang_tag)
                            bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")

                        elif helpcat == "reputation":
                            lg.log("requested help reputation")
                            #send help reputation message
                            help_msg = Helpmsg.help_msg_reputation(user.lang_tag)

                            bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")

                        elif helpcat == "upload":
                            lg.log("requested help upload")
                            help_msg = Helpmsg.help_msg_upload(user.lang_tag)
                            bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")
                        elif helpcat == "supergroups":
                            lg.log("requested help supergroups")
                            help_msg = Helpmsg.help_msg_supergroups(user.lang_tag)
                            bot.sendMessage(mymsg.chat.id, help_msg, parse_mode = "HTML")
                        else:
                            lg.log("/help_category: bad format" + helpcat)
                            categories.sendMainMenu(mymsg.chat.id, user)
                    else:
                        lg.log("/help: bad format" + command)
                        categories.sendMainMenu(mymsg.chat.id, user)

                elif mymsg.content.text == "/upload":
                    lg.log("requested upload")
                    categories.upload(mymsg)
                    categories.sendUploadMedia(mymsg)

                elif mymsg.content.text.startswith("/my_uploads"):
                    lg.log("requested my uploads")
                    command = mymsg.content.text.split(' ')

                    nmax = 3

                    if len(command) == 2:
                        if command[1] == "all":
                            nmax = "all"
                        else:
                            try:
                                nmax = int(command[1])
                            except ValueError:
                                pass
                            except Exception as e:
                                print(e)
                        categories.sendUserUploads(mymsg.chat.id, user, nmax)
                    else:
                        categories.sendUserUploads(mymsg.chat.id, user, nmax)

                elif mymsg.content.text == "/profile":
                    lg.log("requested profile")
                    user.sendProfileInfo(mymsg.chat.id, bot, categories)

                elif mymsg.content.text.startswith("/show_top"):
                    lg.log("requested top")
                    # show_top_categoryname
                    # show_top categoryname nmax

                    categoryname = ""
                    nmax = 3

                    command = mymsg.content.text.split("_")

                    if len(command) == 3:
                        categoryname = command[2]
                    if len(command) == 2:

                        param = command[1]
                        parpar = param.split(' ')
                        print(parpar)
                        if len(parpar) >= 2:
                            categoryname = parpar[1]
                        if len(parpar) == 3:
                            if parpar[2] == "all":
                                nmax = "all"
                            else:
                                try:
                                    nmax = int(parpar[2])
                                except ValueError:
                                    nmax = 3

                    lg.log("{0} {1}".format(categoryname, nmax))
                    if categoryname:
                        categories.sendShowTop(mymsg.chat.id, categoryname, nmax)
                    else:
                        bot.sendMessage(mymsg.chat.id, "Usage: show_top [category] [number of pictures]\n/main_menu")

                elif mymsg.content.text.startswith("/show_"):
                    lg.log("requested show media")
                    commands = mymsg.content.text.split("_", maxsplit= 1)[1:]
                    if len(commands) == 1:
                        commands = commands[0]
                        param = commands.split(' ')
                        if len(param) == 1:
                            param = param[0].split('_')

                        if len(param) == 1:
                            categoryname = param[0]
                            print("requested show for: ", categoryname)
                            categories.showCategoryPrivate(mymsg.chat.id, user, categoryname, chatsdb)

                        if len(param) == 2:
                            categoryname = param[0]
                            uid = None

                            try:
                                uid = int(param[1])

                            except ValueError:
                                print("commands ", commands, "not formatted correctly")

                            if uid is not None:
                                for dmedia in categories.media_vote_db.values():
                                    media = dmedia.getData()
                                    if media.uid == uid:
                                        lg.log(str(media))
                                        media.showMediaShow(mymsg.chat.id, categories)
                                        break


                elif mymsg.content.text.startswith("/user_top"):
                    lg.log("requested top")
                    categories.sendUserTop(mymsg.chat.id, ['reputation', 'karma'], user)



                elif mymsg.content.text.startswith("/vote"):

                    if mymsg.content.text.startswith("/vote_"):
                        categoryname = "".join(mymsg.content.text.split("_")[1:])
                        lg.log("requested vote for: " + categoryname)
                        categories.voteCategoryPrivate(mymsg.chat.id, user, categoryname)
                    else:
                        # pick a random category name
                        categorylist = categories.categories_db.values()

                        # check if category contains media
                        catnameslist = []
                        for dcat in categorylist:
                            cat = dcat.getData()
                            if cat.getMediaList(categories.media_vote_db):
                                catnameslist.append(cat.name)

                        print(catnameslist)

                        if catnameslist:
                            random.shuffle(catnameslist)

                            catname = catnameslist[0]

                            while catnameslist:
                                print(catnameslist)
                                medialist = []
                                for dmedia in categories.media_vote_db.values():

                                    media = dmedia.getData()
                                    if media.catname == catname and media.id not in user.dont_show_pics_id and not media.deleted and user.id not in media.votersids:
                                        medialist.append(media)

                                nmediacat = len(medialist)
                                print(nmediacat)

                                if nmediacat == 0:
                                    catnameslist.pop(0)
                                    if catnameslist:
                                        catname = catnameslist[0]
                                    else:
                                        break
                                else:
                                    break

                            lg.log("requested vote for: " + catname)
                            categories.voteCategoryPrivate(mymsg.chat.id, user, catname)
                        else:
                            bot.sendMessage(mymsg.chat.id, "All categories have no media")
                            lg.log("All categories have no media")


                elif mymsg.content.text.startswith("/main_menu"):
                    lg.log("requested main menu")
                    categories.sendMainMenu(mymsg.chat.id, user)

                elif mymsg.content.text.startswith("/buy_reputation"):
                    print("requested buy reputation")
                    param = mymsg.content.text.split("_")[2:]
                    print(param)
                    if len(param) == 0:
                        user.sendBuyReputation(mymsg.chat.id, bot)

                elif mymsg.content.text == "/print_user_list"  and user.id == creator_id:
                    categories.printUserList()
                else:
                   lg.log("requested main menu")
                   categories.sendMainMenu(mymsg.chat.id, user)
            else:
                lg.log("requested main menu")
                categories.sendMainMenu(mymsg.chat.id, user)

        data = Data(mymsg.mfrom.id, mymsg.mfrom)
        if usersdb.isNew(data):
            lg.log("Added to userdb new user:" + str(mymsg.mfrom.id))
            usersdb.addData(data)
        # Add contents to databases
        if mymsg.content is not None and mymsg.content.file_id is not None:
            data = None

            if mymsg.content.type in ["photo", "sticker", "video", "document"]:
                data = Data(mymsg.content.file_id, mymsg.content)

            if data is not None and contentsdb.isNew(data):
                lg.log("Adding to contents db new " + str(data.getData()))
                contentsdb.addData(data)
            else:
                lg.log("content is already present")
        usersdb.updateDb()

        contentsdb.updateDb()



    data = Data(mymsg.chat.id, mymsg.chat)
    if chatsdb.isNew(data):
        chatsdb.addData(data)

    chatsdb.updateDb()




#==============================================================================
# # handle function: Manage received messages
#==============================================================================


def query(msg):

    lg.log("------------ NEW QUERY ------------")
    lg.startTimer()


    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    person = Person(msg['from'])
    dperson = Data(person.id, person)

    if usersdb.isNew(dperson):
        lg.log("Added new person:" + person.info())
        usersdb.addData(dperson)

    if query_data.startswith("v_"):
        uid = "".join(query_data.split("_")[2:])
        uid = int(uid)
        for dmedia in categories.media_vote_db.values():
            media = dmedia.getData()
            if media.uid == uid:
                print("Category", media.catname)
                print(media)
                if person.id not in media.votersids:
                    send_user_found = False
                    cbquery = CbkQuery(msg)

                    if query_data.startswith("v_like_"):
                        print(person.id, "upvoted")
                        bot.answerCallbackQuery(query_id, text="Up vote")

                        prev_media_score = media.getScore()

                        # update the media
                        media.upvote += 1

                        post_media_score = media.getScore()

                        #update the category score
                        category = media.getCategory(categories.categories_db)

                        category.score = category.score - prev_media_score + post_media_score

                        dcategory = Data(category.name, category)
                        categories.categories_db.setData(dcategory)
                        categories.categories_db.updateDb()

                        # update the uploader
                        upuser = media.getUser(categories.user_profile_db)
                        upuser.points += 1
                        upuser.karma = upuser.getKarma() - prev_media_score + post_media_score
                        nottag = media.catname + "-vote"
                        message = ("Your media got a {3} you earned 1{2}\n"
                                   "Show media (/show_{0}_{1})\n"
                                   "See /profile status").format(
                                    media.catname, media.uid, em.points_emoji, em.upvote_emoji)
                        upuser.sendNotification(nottag, message, bot, chatsdb)

                        dupuser = Data(upuser.id, upuser)
                        categories.user_profile_db.setData(dupuser)
                        categories.user_profile_db.updateDb()


                        # update the user that voted
                        if cbquery.message.chat.type == "private":
                            for duser in categories.user_profile_db.values():
                                user = duser.getData()
                                if person.id == user.id:
                                    user.points += 1
                                    categories.user_profile_db.setData(duser)
                                    categories.user_profile_db.updateDb()
                                    bot.sendMessage(user.getChatID(chatsdb), "You earned 1" + em.points_emoji + " /profile")
                                    send_user_found = True
                                    break

                    elif query_data.startswith("v_dislike_"):
                        print(person.id, "downvoted")
                        bot.answerCallbackQuery(query_id, text="Down vote")

                        prev_media_score = media.getScore()

                        # update the media
                        media.downvote += 1

                        post_media_score = media.getScore()

                        #update the category score
                        category = media.getCategory(categories.categories_db)

                        category.score = category.score - prev_media_score + post_media_score

                        dcategory = Data(category.name, category)
                        categories.categories_db.setData(dcategory)
                        categories.categories_db.updateDb()


                        # update the uploader
                        upuser = media.getUser(categories.user_profile_db)
                        upuser.points -= 1
                        upuser.karma = upuser.getKarma() + post_media_score - prev_media_score
                        nottag = media.catname + "-vote"
                        message = ("Your media got a {3} you lost 1{2}\n"
                                   "Show media (/show_{0}_{1})\n"
                                   "See /profile status").format(
                                    media.catname, media.uid, em.points_emoji, em.downvote_emoji)

                        upuser.sendNotification(nottag, message, bot, chatsdb)

                        dupuser = Data(upuser.id, upuser)
                        categories.user_profile_db.setData(dupuser)
                        categories.user_profile_db.updateDb()


                        # update the user that voted
                        if cbquery.message.chat.type == "private":
                            for duser in categories.user_profile_db.values():
                                user = duser.getData()
                                if person.id == user.id:
                                    user.points += 1
                                    categories.user_profile_db.setData(duser)
                                    categories.user_profile_db.updateDb()
                                    bot.sendMessage(user.getChatID(chatsdb), "You voted a media you earned 1" + em.points_emoji)
                                    send_user_found = True
                                    break

                    media.votersids.append(person.id)

                    dmedia.setData(media)

                    if cbquery.message.chat.type == "private":
                        keyboard = media.makeKeyboardVote()
                        bot.editMessageReplyMarkup(cbquery.getChatMsgID(), keyboard)
                    elif cbquery.message.chat.type == "supergroup" or cbquery.query_msg.chat.type == "group":
                        keyboard = media.makeKeyboardVotePublic()
                        bot.editMessageReplyMarkup(cbquery.getChatMsgID(), keyboard)

                    if send_user_found:
                        categories.voteCategoryPrivate(user.getChatID(chatsdb), user, media.catname)

                else:
                    bot.answerCallbackQuery(query_id, text='Already voted')

        categories.media_vote_db.updateDb()

    elif query_data.startswith("report_"):
        # find my chat in the database

        # get the category creator

        print("--report--")

        for dchat in chatsdb.values():
            chat = dchat.getData()
            if chat.type == "private" and chat.person.id == creator_id:
                creator_chatid = chat.id
                break

        print(query_data)

        param = query_data.split("_")

        uid = param[1]

        if uid == "cat":
            catname = param[2]
            print(catname)
            category = categories.categories_db.getData(catname).getData()
            category.sendAdmin(creator_chatid, categories)
            bot.answerCallbackQuery(query_id, text="REPORTED")

        else:
            uid = int(uid)

            for dmedia in categories.media_vote_db.values():
                media = dmedia.getData()
                if media.uid == uid:
                    if person.id in media.reported_by:
                        bot.answerCallbackQuery(query_id, text="ALREADY REPORTED")
                        print(person, "already reported this media")
                        break
                    else:
                        bot.answerCallbackQuery(query_id, text="REPORTED")

                        media.reported_by.append(person.id)
                        print(person, "reported")

                        # send to creator
                        bot.sendMessage(creator_chatid, "Report from: " + str(person))
                        media.sendAdmin(creator_chatid, bot, categories.user_profile_db, ban_keyboard=True, catManager=categories)

                        # get the category creator

                        cat = categories.categories_db.getData(media.catname).getData()
                        cat_creator_id = cat.creator
                        chatid_cat_creator = None
                        print("Category creator:", cat_creator_id)
                        if cat_creator_id is not None:
                            for dchat in chatsdb.values():
                                chat = dchat.getData()
                                if chat.type == "private" and cat_creator_id == chat.id:
                                    chatid_cat_creator = chat.id
                                    break
                            print("chat id", chatid_cat_creator)
                            if chatid_cat_creator is not None:
                                bot.sendMessage(chatid_cat_creator, "Report from: " + str(person))
                                media.sendAdmin(chatid_cat_creator, bot, categories.user_profile_db, catManager=categories)

                        break

    elif query_data.startswith("delete_"):
        bot.answerCallbackQuery(query_id, text="deleted")
        param = query_data.split("_")
        uid = param[1]

        if uid == "cat":
            catname = param[2]
            category = categories.categories_db.getData(catname).getData()
            category.deleted = True
            dcat = Data(catname, category)
            categories.categories_db.setData(dcat)
            categories.categories_db.updateDb()
            print("category", catname, "deleted")
        else:
            uid = int(uid)
            for dmedia in categories.media_vote_db.values():
                media = dmedia.getData()
                if media.uid == uid:
                    print("Media", uid, "has been flagged for delete")
                    media.deleted = True
                    dmedia.setData(media)
                    categories.media_vote_db.updateDb()
                    break

    elif query_data.startswith("noshow_"):
        bot.answerCallbackQuery(query_id, text="You will not see this picture anymore")
        uid = "".join(query_data.split("_")[1:])
        uid = int(uid)

        user = None
        if person.id in categories.user_profile_db.keys():
            duser = categories.user_profile_db.getData(person.id)
            user = duser.getData()

        if user is not None:
            for dmedia in categories.media_vote_db.values():
                media = dmedia.getData()
                if media.uid == uid:
                    print(user.id, "doesn't want to see anymore media number:", uid)
                    user.dont_show_pics_id.append(media.id)

                    duser.setData(user)

                    categories.user_profile_db.updateDb()
                    break
    elif query_data.startswith("ban_"):
        userid = "".join(query_data.split("_")[1:])
        if from_id == creator_id:
            duser = categories.user_profile_db.getData(userid)
            user = duser.getData()
            if user.id != creator_id:
                usertag = user.anonid
                if len(usertag) > 15:
                    usertag = usertag[:15]
                bot.answerCallbackQuery(query_id, text= usertag + " banned")
                print(user.anonid, "banned")
                user.banned = True

                duser.setData(user)
                categories.user_profile_db.updateDb()

    elif query_data.startswith("unban_"):
        userid = "".join(query_data.split("_")[1:])
        if from_id == creator_id:
            duser = categories.user_profile_db.getData(userid)
            user = duser.getData()
            if user.id != creator_id:
                usertag = user.anonid
                if len(usertag) > 15:
                    usertag = usertag[:15]
                bot.answerCallbackQuery(query_id, text= usertag + " unbanned")
                print(user.anonid, "unbanned")
                user.banned = False

                duser.setData(user)
                categories.user_profile_db.updateDb()

    elif query_data.startswith("mute_"):
        commands = query_data.split("_", maxsplit = 2)
        print(commands)

        nottag = commands[1]
        userid = int(commands[2])

        user = categories.user_profile_db.getData(userid).getData()

        if user.receive_notifications[nottag]:

            user.receive_notifications[nottag] = False
            bot.answerCallbackQuery(query_id, text= nottag + " muted")

            categories.user_profile_db.setData(Data(user.id, user))
            categories.user_profile_db.updateDb()
        else:
            bot.answerCallbackQuery(query_id, text= nottag + " already muted")

    elif query_data.startswith("cmp"):
        args = query_data.split("_", maxsplit = 1)[1:]
        page = int(args[0])

        cbkquery = CbkQuery(msg)

        topmedia = False
        menu = False
        user = None

        if query_data.startswith("cmps_"):
            pass
        elif query_data.startswith("cmptm_"):
            topmedia = True
            user = categories.user_profile_db.getData(cbkquery.person.id).getData()
        else:
            menu = True
            user = categories.user_profile_db.getData(cbkquery.person.id).getData()


        try:
            categories.sendSelectCategoryMenu(cbkquery.getChatMsgID(), ipage=page, sort=True, menu=menu, topmedia=topmedia, user=user )
            bot.answerCallbackQuery(query_id, text ="Page " + str(page))

        except TelegramError as e:
            if e.error_code == 400:
                if page == 1:
                    bot.answerCallbackQuery(query_id, text ="Reached first page")
                else:
                    bot.answerCallbackQuery(query_id, text ="Reached last page")
            else:
                raise e

    elif query_data.startswith("buy_"):
        param = query_data.split("_", maxsplit = 1)[1:]
        if len(param) == 0:
            print("Bad Format")
            print(query_data)
        else:
            cb_query = CbkQuery(msg)
            user = categories.user_profile_db.getData(from_id).getData()
            param = param[0].split("_", maxsplit = 1)
            print(param)
            if param[0] == "calcp":
                print("calculate the probability")
                categories.sendProbability(user.getChatID(chatsdb), user, categories.user_profile_db)
            elif param[0] == "uploads":
                param = param[1]
                is_int = False
                try:
                    points = int(param)
                    is_int = True

                except ValueError:
                    print("param is not int", param)

                except Exception as e:
                    print("Pella: Unknown error")
                    print(e)
                    raise e

                if is_int:
                    total_cost = points

                    if total_cost > user.points:
                        bot.sendMessage(user.getChatID(chatsdb), text = not_enoug_money_msg)
                        bot.answerCallbackQuery(query_id, text = "Not enough money")
                    else:

                        # update the user status
                        if user.dayuploads >= MAXUPLOADS:
                            user.points -= total_cost
                            user.dayuploads = 0
                            user.firstuploadtime = datetime.datetime.now()

                            # update user db
                            duser = Data(user.id, user)
                            categories.user_profile_db.setData(duser)
                            categories.user_profile_db.updateDb()

                            # send relative messages and callbacks / edit the previous message
                            # with the new prices
                            bot.sendMessage(user.getChatID(chatsdb), text = "You have now 5 more uploads")
                            bot.answerCallbackQuery(query_id, text = "Bough uploads, great deal!")


            elif param[0] == "rp":
                param = param[1]
                cb_query = CbkQuery(msg)
                user = categories.user_profile_db.getData(from_id).getData()
                if from_id in categories.user_profile_db.database:

                    print("points: ", user.points)
                    print("rep points:", user.rep_points)


                    is_int = False
                    try:
                        rp = int(param[0])
                        is_int = True

                    except ValueError:
                        print("param is not int", param)
                    except Exception as e:
                        print("Unknown error")
                        print(e)
                        raise e

                    if is_int:
                        total_cost = calc_rep_cost(user, rp)

                        if total_cost > user.points:
                            bot.sendMessage(user.getChatID(chatsdb), text = not_enoug_money_msg)
                            bot.answerCallbackQuery(query_id, text = "Not enough money")
                        else:
                            # update the user status
                            user.points -= total_cost
                            user.rep_points += rp

                            # update user db
                            duser = Data(user.id, user)
                            categories.user_profile_db.setData(duser)
                            categories.user_profile_db.updateDb()

                            # send relative messages and callbacks / edit the previous message
                            # with the new prices
                            bot.sendMessage(user.getChatID(chatsdb), text = "You bought " + str(em.RPstr(rp)) + "\nYou now have a reputation of " + str(user.getReputationStr()))
                            user.sendBuyReputation(cb_query.getChatMsgID(), bot, edit=True)
                            bot.answerCallbackQuery(query_id, text = "Bough reputation, great deal!")

    elif query_data.startswith("createcat_"):
        # split the query data
        catd = query_data.split("_")
        user = categories.user_profile_db.getData(from_id).getData()
        chatid = user.getChatID(chatsdb)

        catname = catd[1]

        cattag = tags.tag_from_string(catd[2])

        price = int(catd[3])

        print("New category query:", catd, catname, cattag, user)

        category = Category(catname, cattag, user.id)

        data = Data(category.name, category)
        if categories.categories_db.isNew(data):
            if user.points >= price:
                categories.categories_db.addData(data)
                categories.categories_db.updateDb()

                categories.user_profile_db.updateDb()

                categories.new_cat_req[chatid] = (False, False)

                user.points -= price
                duser = Data(user.id, user)
                categories.user_profile_db.addData(duser)
                categories.user_profile_db.updateDb()

                bot.sendMessage(chatid, _("Category successfully created\n/main_menu", user.lang_tag))
                bot.answerCallbackQuery(query_id, text = _("Category Created", user.lang_tag))
                print("category", category.name, "has been successfully created by:", user.anonid)
            else:
                categories.new_cat_req[chatid] = (False, False)
                bot.sendMessage(chatid, _("You don't have enough money, /help_points", user.lang_tag))
                bot.answerCallbackQuery(query_id, text = _("You hobo", user.lang_tag))
        else:
            categories.new_cat_req[chatid] = (False, False)
            bot.sendMessage(chatid, _("Category already present\n/main_menu", user.lang_tag))
            bot.answerCallbackQuery(query_id, text = _("Category already present", user.lang_tag))

    else:
        bot.answerCallbackQuery(query_id, text='what?')
        print("not my query")

    lg.log("- Operation done -", time_sub = True)

#%%Test message

class TestMessage:

    testfolder = "./data/testdata/"

    def __init__(self, name):
        self.name = name
        self.test_media = None
        self.test_user = None

    def dump(self):
        filename = self.testfolder + self.name + ".pickle"
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        filename = self.testfolder + self.name + ".pickle"
        with open(filename, 'rb') as f:
            loaded = pickle.load(f)
        self.name = loaded.name
        self.test_media = loaded.test_media
        self.test_user = loaded.test_user


    def sendMessage(self):

        chatid = creator_chatid

        bot.sendMessage(chatid, "Test message")

    # test

#    t = TestMessage("Test_keyboard")
#    t.load()
#    t.sendMessage()
#    t.dump()




#    print("updating users db")
#    for data in categories.user_profile_db.values():
#        user = data.getData()
#
#        newuser = UserProfile(user.person)
#
#
#
#        for attr, value in user.__dict__.items():
#            newuser.__setattr__(attr, user.__getattribute__(attr))
#
#        print(newuser)
#
#        del newuser.person
#
#        data.setData(newuser)
#
#    categories.user_profile_db.updateDb()
#
#
#    #update categories media db
#    print("updating media db")
#    for data in categories.media_vote_db.values():
#        content = data.getData()
#        newcontent = ContentVote(content.uid, content.userid, content.content, content.catname)
#
#        for attr, value in content.__dict__.items():
#            newcontent.__setattr__(attr, content.__getattribute__(attr))
#
#        del newcontent.anonymous
#        del newcontent.cmessageids
#
#        data.setData(newcontent)
#
#    categories.media_vote_db.updateDb()
#
#
#    print("updating categories db")
#    for data in categories.categories_db.values():
#        category = data.getData()
#
#
#        newcategory = Category(category.name)
#
#        for attr, value in category.__dict__.items():
#            newcategory.__setattr__(attr, category.__getattribute__(attr))
#
#        data.setData(newcategory)
#
#    categories.categories_db.updateDb()

<<<<<<< HEAD


#    # update categories media db
#    print("updating rep db")
#    for data in categories.user_profile_db.values():
#        user = data.getData()
#
#        user.rep_points = 1
#
#        data.setData(user)
#
#    categories.user_profile_db.updateDb()



#    # update categories media db
#    print("updating rep db")
#    for data in categories.user_profile_db.values():
#        user = data.getData()
#
#        user.anonid = user.anonid.upper()
#
#        data.setData(user)
#
#    categories.user_profile_db.updateDb()

=======
>>>>>>> 03628c784d71b10392b1b36a4d0a8056f6b0ec14
#%% Inline query functions

def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Inline Query:', query_id, from_id, query_string)

        articles = [InlineQueryResultArticle(
                        id='abc',
                        title=query_string,
                        input_message_content=InputTextMessageContent(
                            message_text=query_string
                        )
                   )]

        return articles

    answerer.answer(msg, compute)

def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print ('Chosen Inline Result:', result_id, from_id, query_string)


#%% Main

if __name__ == "__main__":
    from datetime import date
    timestamp = date.today().strftime("%y%m%d")
    lg = Logger("DirtyRateBot", "./logs/main_log_" + timestamp + ".txt")

    lg.log("- Loading databases -")
    lg.startTimer()

    usersdb = Database("./data/users_db/")
    print("Loading user db")
    usersdb.loadDb()

    chatsdb = Database("./data/chats_db/")
    print("Loading chats db")
    chatsdb.loadDb()

    contentsdb = Database("./data/contents_db/")
    print("Loading contents db")
    contentsdb.loadDb()

    supergroupsdb = Database("./data/supergroups_db/")
    print("Loading supergroups db")
    supergroupsdb.loadDb()


<<<<<<< HEAD

=======
>>>>>>> 03628c784d71b10392b1b36a4d0a8056f6b0ec14
    bot = telepot.Bot(bot_token)
    answerer = telepot.helper.Answerer(bot)

    categories = Categories(bot)


    lg.log("- Databases Loaded -", True)

    MessageLoop(bot, {'chat': handle,
                     'callback_query': query,
                     'chosen_inline_result': on_chosen_inline_result

                     }
                ).run_as_thread()

    print ('Listening ...')

    # Keep the program running.
    while 1:
        time.sleep(10)
