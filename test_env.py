# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 11:26:26 2017

@author: Mauro
"""

import sys
sys.path.append("./src")

import random
from matplotlib import pyplot as plt
import math

random.seed(5)

class User:
    
    def __init__(self, uid, points, karma, rep_points):
        self.id = uid
        self.points = points
        self.karma = karma
        self.rep_points = rep_points
        
        self.media_uploaded = []
    
    def addMedia(self, media):
        self.media_uploaded.append(media)
        
    def calcKarma(self):
        self.karma = 0
        for media in self.media_uploaded:
            self.karma += media.getScore()
    
    def getReputation(self):
        # transform reputation points into reputation
        # self.reputation * self.karma if self.karma >= 1 else 1
        reputation = self.rep_points * (self.karma if self.karma >= 1 else 1) #/ float(len(self.media_uploaded))

        return reputation   
    
    def __str__(self):
        return "ID{5}| P{0}| K{1}| RP{2}| R{3}| N{4}".format(self.points, self.karma, self.rep_points, self.getReputation(), len(self.media_uploaded), self.id)


class Media:
    
    def __init__(self, upvote, downvote, user):
        self.upvote = upvote
        self.downvote = downvote
        self.user = user
    
    def getKarma(self):
        return self.upvote - self.downvote
    
    def getImpact(self):
        return self.upvote + self.downvote
    
    def getScore(self):
        if self.getImpact() == 0:
            return 0
        return self.getKarma() * self.getImpact()
    
    def __str__(self):
        s = "User: {}|Up: {}| down: {}| karma: {}| impact: {}| score {}".format(self.user.id, self.upvote, self.downvote, self.getKarma(), self.getImpact(), self.getScore())
        return s


def linear_map(inx, x0, y0, x1, y1):
    return y0 + (inx - x0)*(y1-y0)/(x1 - x0)

#
## variables
#NUSERS = 10
#NMEDIA = 100
#
#
## build users
#userslist = []
#for i in range(NUSERS):
#    user = User(i, 0, 0, random.randint(1,20))
#    
#    userslist.append(user)
#
## add media
#for user in userslist:
#    mediaperuser =random.randint(1, int(NMEDIA / NUSERS))
#    
#    for i in range(mediaperuser):
#        media = Media(random.randint(0,10), random.randint(0,10), user)
#        user.addMedia(media)
#    user.calcKarma()
#        
#
#
#def pick_media(medialist):
#    usermedia = []
#    reps = []
#    for media in medialist:
#        usermedia.append(media)
#        user = media.user
#        rep = math.log2(user.getReputation())
#        reps.append(rep)    
# 
#    rep_max = max(reps)  
#    
#    # choose randomly a picture
#    
#    # construct a weight for the probability to be shown from
#    # 0 .. 0.9 
#    reps_norm = []
#    for rep, media in zip(reps, medialist):        
#        repnew = linear_map(rep/rep_max, 0, 0, 1, 0.9)
#        reps_norm.append(repnew)
#    
#    # chose the random media
#    chosen_media = random.choice(usermedia) # the default media is random
#    remix = list(zip(reps_norm, usermedia))
#    random.shuffle(remix) 
#    for rep, media in remix:
#        test_n = random.uniform(0, 1)
#        if test_n <= rep:
#            chosen_media = media 
#            break  
#    return chosen_media
#
#
#userslist = [0 for i in range(5)]
#
#userslist[0] = User("Anna", 0, 1, 1000)
#for i in range(10):
#    userslist[0].addMedia(Media(0,0, userslist[0]))
#    
#userslist[1] = User("Piero", 0, 1, 5)
#for i in range(3):
#    userslist[1].addMedia(Media(0,0, userslist[1]))
#    
#userslist[2] = User("Miai", 0, 1, 5000)
#for i in range(6):
#    userslist[2].addMedia(Media(0,0, userslist[2]))
#    
#userslist[3] = User("Nur", 0, 1, 2)
#for i in range(100):
#    userslist[3].addMedia(Media(0,0, userslist[3]))
#    
#userslist[4] = User("Pella", 0, 1, 1)
#for i in range(1):
#    userslist[4].addMedia(Media(0,0, userslist[4]))
#
#
#medialist = []
#for user in userslist:
#    medialist += user.media_uploaded
#    
#  
#
#
#print("--------- MEDIA ---------")
#for media in medialist:
#    print(media)
#
#print("--------- USERS ---------")
#for user in userslist:
#    print(user)


mydict = {}
mydict["pear"] = 1

try:
     a = mydict["apple"]
     a = 1/0
except KeyError as e:
    print("key not found")
    print(e)
