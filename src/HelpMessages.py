# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 10:31:25 2017

@author: Mauro
"""


from LanguageSupport import _

import emoji_table as em

def help_msg(version, lang_tag):
    
    # variables
    sdb = {}
    sdb["version"] = version
    sdb["pem"] = em.points_emoji
    sdb["kem"] = em.karma_emoji
    sdb["rem"] = em.reputation_emoji
    

    help_msg = "@DirtyRateBot version: {version}\n"
    help_msg += "<i>This bot allows you to upload and rate media with the rest of the bot community.\nThe media are divided into categories.</i>\n"
    help_msg += "\n"
    help_msg += "<b>- Rating pictures -</b>\n"
    help_msg += "To rate the media use /categories\n"
    help_msg += "To see the top three media use the /show_top\n"
    help_msg += "\n"
    help_msg += "<b>- Uploading pictures -</b>\n"
    help_msg += "To upload your media see /help_upload.\n"
    help_msg += "\n"
    help_msg += "<b>- Profile -</b>\n"
    help_msg += "You can check your uploads under /profile then /my_uploads.\n"
    help_msg += "You will have a profile with points {pem}, karma {kem} and reputation {rem}.\nSee /help_points, /help_karma, /help_reputation\n"
    help_msg += "\n"
    help_msg += "<b>- Super Groups -</b>\n"
    help_msg += "You can use the bot in super group, add it and press the command /vote.\n"
    help_msg += "If you are the admin you can set the categories you want to show /help_supergroups."
    
    help_msg = _(help_msg, lang_tag)
    
    help_msg = help_msg.format(**sdb)
    
    return help_msg
    
def help_msg_karma(lang_tag):
    
    sdb = {}
    sdb['kem'] = em.karma_emoji
    sdb['uem'] = em.upvote_emoji
    sdb['anonem'] = em.anon_emoji
    sdb['dem'] = em.downvote_emoji
    
    help_msg = "<b>- karma {kem} -</b>\n"
    help_msg += "The karma is calculated by the number of upvotes {uem} minus the number of downvotes {dem} and multiplied by the number of people {anonem} who voted for your media.\n"
    help_msg +=  "The karma influences the way the uploaded pictures are presented to the users.\nThe more karma you have the better visibility will get your pictures.\n"
    help_msg += "\n"
    help_msg += "- How do I earn karma?\n"
    help_msg += "Upload media to the bot by using the commnad /upload\n"

    help_msg = _(help_msg, lang_tag)
    
    help_msg = help_msg.format(**sdb)

    return help_msg

def help_msg_points(lang_tag):
    
    # variables
    sdb = {}
    sdb["pemoji"] = em.points_emoji
    sdb["1 point"] = str(em.Pstr(1))
    sdb["5 points"] = str(em.Pstr(5))
    sdb["remoji"] = em.reputation_emoji
    
    help_msg = "<b>- Points {pemoji} -</b>\n"
    help_msg += "You earn +{1 point} when you vote and +{5 points} when you /upload.\n"
    help_msg += "When somebody upvotes your content you earn +{1 point} but you lose -{1 point} if somebody downvotes.\n"
    help_msg += "Points are used to increase your reputation {remoji} (/buy_reputation), which increases the visibility of your media.\n"
    
    help_msg = _(help_msg, lang_tag)
    
    help_msg = help_msg.format(**sdb)

    return help_msg


def help_msg_reputation(lang_tag):

    sdb = {}
    sdb["remoji"] = em.reputation_emoji
    sdb["anonem"] = em.anon_emoji
    sdb["kemoji"] = em.karma_emoji
    
    help_msg = "<b>- Reputation {remoji} -</b>\n"
    help_msg += "The reputation is shown near your username (or anonymous id {anonem}).\n"
    help_msg += "The reputation is calculated by your reputation points (/buy_reputation) times your karma {kemoji} (if karma is positve).\n"
    help_msg += "\n"
    help_msg +=  "The reputation determines the media's visibility.\nWhen a person wants to vote, the media are orderd by reputation of the user.\n"
    help_msg += "\n"
    help_msg += "- How do I increase my reputation?\n"
    help_msg += "use the command /buy_reputation"

    help_msg = _(help_msg, lang_tag)
    
    help_msg = help_msg.format(**sdb)

    return help_msg

def help_msg_upload(lang_tag):
    help_msg = "<b>- Upload media -\n</b>"
    help_msg += "Use the command /upload to upload media to the bot.\n"
    help_msg += "The bot will ask for a media (can be a picture, gif, video or document)\n"
    help_msg += "The bot will ask for a category\n"
    help_msg += "If the bot says success, you made it"
    
    help_msg = _(help_msg, lang_tag)
    
    return help_msg

def help_msg_supergroups(lang_tag):
    
    help_msg = "<b>- Help supergroup -</b>\n"
    help_msg += "The users can call /vote and the bot will pick media from a set of selected categories.\n"
    help_msg += "If you are one of the admin or the creator of the supergroup, you can decide what categories will be shown.\n"
    help_msg += "By default the bot will show the safe for work (SFW) categories: meme, nature, space\n"
    help_msg += "Admin can use a series of commands to set new categories or remove them.\n"
    help_msg += "List of admin commands: (use them in group)\n"
    help_msg += "/set_all: sets all the categories\n"
    help_msg += "/rem_all: mutes all the categories\n"
    help_msg += "/set_categories: the admin can select a number of categories comma separated.\n"
    help_msg += "/rem_categories: select which categories to remove.\n"
    help_msg += "/reset_all: sets only the default categories.\n"
    help_msg += "/set_porngore: allows the porn and gore categories to be shown.\n"
    help_msg += "/set_kinky: adds the porn categories but not the gore categories, to the shown list.\n"

    help_msg = _(help_msg, lang_tag)
    
    return help_msg   

