# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 13:13:11 2017

@author: Mauro
"""

import emoji_table as em

class Tag:
    
    def __init__(self, name, before_emojis, after_emojis):
        
        self.name = name
        self.emojis = (before_emojis, after_emojis)
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __ne__(self, other):
        return self.name!= other.name
        
    
    def __str__(self):
        bem = ""
        for emo in self.emojis[0]:
            bem += emo
         
        aem = ""
        for emo in self.emojis[1]:
            aem += emo
        
        return "{0} {1} {2}".format(bem, self.name, aem)

class NSFW(Tag):
    
    def __init__(self):
        super().__init__("NSFW", (em.nsfwem), (em.nsfwem))
    
class SFW(Tag):
    
    def __init__(self):
        super().__init__("SFW", (em.sfwem), (em.sfwem))

class GORE(Tag):
    
    def __init__(self):
        super().__init__("GORE", (em.goreem, em.nsfwem), (em.nsfwem, em.goreem))
        
def tag_from_string(identifier):
    
    if identifier.lower() == "nsfw":
        return NSFW()
    
    if identifier.lower() == "sfw":
        return SFW()
    
    if identifier.lower() == "gore":
        return GORE()

if __name__ == "__main__":
    
    nsfw_tag = NSFW()
    
    sfw_tag = SFW()
    
    gore_tag = GORE()
    
    print(nsfw_tag)
    print(sfw_tag)
    print(gore_tag)
    
    print(nsfw_tag == gore_tag)
    print(nsfw_tag != gore_tag)
    print(nsfw_tag == nsfw_tag)
        