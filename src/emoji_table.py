# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 11:59:25 2017

@author: Mauro
"""

karma_emoji = "🌀"
points_emoji = " ₽"
reputation_emoji = "⚜️"
upvote_emoji = "👍"
downvote_emoji = "👎"
people_emoji = "👥"
anon_emoji = "👤"
reputation_points_emoji = "🔰"
user_face = "👩‍"
space_shuttle = "🚀"
report_emoji = "❌"
hidemedia_emoji ="📵"
first_medal = "🥇"
trophy = "🏆"
gold_medal = "🏅"
second_medal = "🥈"
third_medal = "🥉"

nsfwem = "🔞"
sfwem = "❇"
goreem = "🗡"



def suffix_numbers(num):
    magnitude = 0
    onum = num
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
        if magnitude >= 5:
            break

    if onum <= 999:
        return '{0}'.format(num)
    else:
        suffix_list = ('', 'K', 'M', 'G', 'T', 'P')
        return '{0:.1f}{1}'.format(num, suffix_list[magnitude])


class NEM:
    
    def __init__(self, n, emoji, long = False):
        self.n = n
        self.emoji = emoji
        self.long = long
    
    def __str__(self):
        if self.long:
            return "{0}{1}".format(self.n, self.emoji)
        else:
            return "{0}{1}".format(suffix_numbers(self.n), self.emoji)
    
class Pstr(NEM):
    
    def __init__(self, n, long = False):
        super().__init__(n, points_emoji)
    
class Kstr(NEM):
 
    def __init__(self, n, long = False):
        super().__init__(n, karma_emoji)   

class Rstr(NEM):

    def __init__(self, n, long = False):
        super().__init__(n, reputation_emoji)  

class RPstr(NEM):
    
    def __init__(self, n, long = False):
        super().__init__(n, reputation_points_emoji)      

if __name__ == "__main__":
    print(Kstr(19))