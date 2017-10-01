# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 14:06:57 2017

@author: Mauro
"""

import threading
from telepot.exception import BotWasBlockedError
from Databases import Data

import os
import datetime
import time

creator_id = 183961724

class Announcement:
    
    def __init__(self, bot, catdb, chatsdb):
        self.bot = bot
        self.catdb = catdb
        self.chatsdb = chatsdb
        
        self.success = {}
        self.success_daily = {}
        
        # open the directory
        succssessdir = "./data/announcements/"
        if not os.path.isdir(succssessdir):
            os.mkdir(succssessdir)
        
        # create a log file for the custom announcments
        self.successfile = "./data/announcements/main_success_log.txt"
        if os.path.isfile(self.successfile):
            with open(self.successfile, 'r') as f:
                lines = f.readlines()
                
            if lines:
                for line in lines:
                    userid = int(line)
                    self.success[userid] = True
        
        
        # create a log file for the custom announcments
        self.success_daily_file = "./data/announcements/success_daily_log.txt"
        self.daily_announcement_done = "./data/announcements/daily_announcement_done.txt"
        self.star_timer_file = "./data/announcements/start_timer.txt"
        if os.path.isfile(self.success_daily_file):
            
            lines = []
            
            with open(self.success_daily_file, 'r') as f:
                lines = f.readlines()
                
            if lines:
                for line in lines:
                    userid = int(line)
                    self.success_daily[userid] = True
        
        self.writeStartTimer()
        
    def writeStartTimer(self):
        with open(self.star_timer_file, "w") as f:
            tnowprec = datetime.datetime.now()
            year = tnowprec.year
            month = tnowprec.month
            day = tnowprec.day
            tnow = datetime.datetime(year, month, day, 0, 0, 0)
            f.write(str(tnow.timestamp())+"\n")
    
    def getStartTimer(self):
        timestamp = None
        with open(self.star_timer_file, "r") as f:
            line = f.readline()
            line = line.strip()
            timestamp = float(line)
        
        return datetime.datetime.fromtimestamp(timestamp)
    
    def announce_text(self, user, text):
        text = text if len(text) > 10 else "{0: >10}".format(text)
        print("Sending (", text[0:10], ")to", user.anonid)        
        user.sendNotification("main-announcement", text, self.bot, self.chatsdb)
        self.success[user.id] = True
        
        # write a file containing the id of the users
        with open(self.successfile, 'a') as f:
            f.write(str(user.id) + '\n')
        return    
    
    def announce_all_users(self, text):
        # the api limit is 30 in a second
        tele_api_limit = 1 / 25.0
        
        # yet is better to announce the users over a day.
        userlist = self.catdb.user_profile_db.values()
        # get the total users
        totusers = len(userlist)
        print("tot users", totusers)
        
        # calculate the interval, if above below api limit the message will be
        # spread over more days
        apilimit = 60 * 60 * 24 / totusers
        if apilimit <= tele_api_limit:
            apilimit = tele_api_limit
        
        secs = 0
        usercount = 0
        
        for duser in userlist:
            user = duser.getData()
            if user.id in self.success:
                pass
            else:
                self.success[user.id] = False
            
            if not self.success[user.id]:
                # start a timer thread for each user
                t = threading.Timer(secs, self.announce_text, args=(user, text))
            
                t.start()
                
                print("Announcement for", user.anonid, "starts in", secs,"seconds, users announced", usercount)
                
            secs += apilimit
                
            usercount += 1
                
                
        
        self.catdb.user_profile_db.updateDb()
    
    def daily_announcement_text(self, user, last, day_cat, day_media):
        # The daily announcment should bring 
        # position 
        # added categories from last visit
        # added media from last visit
        
        userlist = self.catdb.generateUserList(sort=['reputation', 'karma'], nmax=None, excluded_ids=[creator_id])
        
        position = 0
        ouser = userlist[position]
        while user.id != ouser.id:
            position += 1
            if position >= len(userlist):
                break
            ouser = userlist[position]
            
        

        sdb = {}
        sdb["position"] = position
        
        text = "<b>---- Daily Summary ----</b>\n"
        text += "You are in position {position}\n"

        text += "\n"
        
        text += "---- New categories today ----\n"

        if day_cat:
            for cat in day_cat:
                text += cat.getTitleStr() + "\n /vote_{}\n".format(cat.name)
        else:
            text += "No new categories\n"
        
        text += "\n"
        
        text += "--- New media today ----\n"
        
        if day_media:
            
            cat_media = {}
            
            for media in day_media:
                if media.catname in cat_media:
                    cat_media[media.catname] += 1
                else:
                    cat_media[media.catname] = 1
            
            for catname, nmedia in cat_media.items():
                text += "{catname} has {nmedia} new media\n/vote_{catname}\n".format(catname=catname, nmedia=nmedia)
            
        else:
            text += "No new media\n"

        text = text.format(**sdb)

        print("send daily message to user", user.id)
        user.sendNotification("daily-announcement", text, self.bot, self.chatsdb)
        
        with open(self.success_daily_file, 'a') as f:
            f.write(str(user.id) + "\n")
        
        
        if last:
            print("Deleting file...")
            # delete the file
            os.remove(self.success_daily_file)
            self.success_daily_success = True
            
            # create also a success file that will be deleted if the time is
            # passed
            with open(self.daily_announcement_done, "w") as f:
                f.write("success\n")
        return
        
    def announce_daily(self, catManager):
        print("Daily routine work")
        catManager.maintenence()
        
        print("Try sending announcement", datetime.datetime.now())
        nowtime = datetime.datetime.now()
        timedelta = datetime.timedelta(days=1)

        timediff = nowtime - self.getStartTimer()
        
        is_day_passed = (timediff > timedelta)
        
        print("is it time", is_day_passed)
        
        if is_day_passed:
            # delete the done file
            if os.path.isfile(self.daily_announcement_done):
                os.remove(self.daily_announcement_done)
            
            
        
        is_done = os.path.isfile(self.daily_announcement_done)
        is_pending = os.path.isfile(self.success_daily_file)
        
        if not is_done and (is_pending or is_day_passed):
            
            tele_api_limit = 1 / 25.0
            
            # yet is better to announce the users over a day.
            userlist = list(self.catdb.user_profile_db.values())
            # get the total users
            totusers = len(userlist)
            
            # calculate the interval, if above below api limit the message will be
            # spread over more days
            apilimit = 60 * 60 * 24 / totusers
            if apilimit <= tele_api_limit:
                apilimit = tele_api_limit
            
            apilimit = 1
            
            secs = 0
            usercount = 0
            
            # gather the newly added categories and media
            day_media = []
            for media in catManager.media_vote_db.getDataList():
                if nowtime - media.creation_date < datetime.timedelta(days=1):
                    day_media.append(media)
            
            day_cat = []
            for category in catManager.categories_db.getDataList():
                if nowtime - category.creation_date < datetime.timedelta(days=1):
                    day_cat.append(category)
            
            for duser in userlist:
                user = duser.getData()
                if user.id not in self.success_daily:
                    self.success_daily[user.id] = False
                
                if not self.success_daily[user.id]:
                    # start a timer thread for each user
                    last = False
                    if user.id == userlist[-1].getData().id:
                        last = True
                        
                    
                    
                    print("is last", last)
                    t = threading.Timer(secs, self.daily_announcement_text, args=(user, last, day_cat, day_media))
                
                    t.start()
                    
                    print("Daily for", user.anonid, "starts in", secs,"seconds, users announced", usercount)
                    
                secs += apilimit
                    
                usercount += 1
                    
                
            
            self.catdb.user_profile_db.updateDb() 
            
            self.writeStartTimer()
        return
    
    def run_daily(self, catManager):
        while 1:
            print("start thread")
            t = threading.Thread(target=self.announce_daily, args=(catManager,))
            t.start()
            time.sleep(2*60*60)
            
  
    