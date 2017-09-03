# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 09:36:05 2017

@author: Mauro
"""

import random

class SuperGroup:

    def __init__(self, chatid):
        self.id = chatid

        # default categories
        self.catsettings = {}
        self.wait_category = False

    def initCategories(self, catdb):
        for catname in catdb.keys():
            self.catsettings[catname] = False

        # set the defaults
        self.catsettings["nature"] = True
        self.catsettings["meme"] = True
        self.catsettings["space"] = True

    def addCategory(self, catname, catdb):
        if catname in catdb.database:
            cat = catdb.getData(catname).getData()
            if not cat.deleted:
                self.catsettings[catname] = True
            return catname

    def delCategory(self, catname, catdb):
        if catname in catdb.database:
            self.catsettings[catname] = False
            return catname

    def setCategories(self, catnames, catdb):
        switchedon = []
        for name in catnames:
            cn = self.addCategory(name, catdb)
            if cn is not None:
                switchedon.append(cn)
        return switchedon

    def remCategories(self, catnames, catdb):
        switchedoff = []
        for name in catnames:
            cn = self.delCategory(name, catdb)
            if cn is not None:
                switchedoff.append(cn)
        return switchedoff

    def getChat(self, chatdb):
        dchat = chatdb.getData(self.id)
        return dchat.getData()

    def sendPickCategories(self, categories):
        categories.sendSelectCategoryMenu(self.id, sort=True)

    def setKinky(self):
        self.catsettings["boobs"] = True
        self.catsettings["booty"] = True
        self.catsettings["bdsm"] = True
        self.catsettings["hentai"] = True
        self.catsettings["lesbian"] = True

    def setPornGore(self):
        self.catsettings["nature"] = False
        self.catsettings["meme"] = False
        self.catsettings["space"] = False
        self.catsettings["dicks"] = False
        self.catsettings["gay"] = False
        self.catsettings["random"] = False
        self.catsettings["boobs"] = True
        self.catsettings["booty"] = True
        self.catsettings["bdsm"] = True
        self.catsettings["hentai"] = True
        self.catsettings["lesbian"] = True
        self.catsettings["gore"] = True

    def setAll(self):
        for key, value in self.catsettings.items():
            self.catsettings[key] = True

    def remAll(self):
        for key, value in self.catsettings.items():
            self.catsettings[key] = False

    def sendMedia(self, catManager):
        medialist = []
        for dmedia in catManager.media_vote_db.values():
            media = dmedia.getData()
            category = catManager.categories_db.getData(media.catname).getData()
            try:
                if not media.deleted and self.catsettings[media.catname] and not category.deleted:
                    medialist.append(media)
            except KeyError:
                self.catsettings[media.catname] = False
                if not media.deleted and self.catsettings[media.catname] and not category.deleted:
                    medialist.append(media)
            except Exception as e:
                raise e

        if medialist:
            cmedia = random.choice(medialist)
            cmedia.showMediaVotePublic(self.id, catManager)