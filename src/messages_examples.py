# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 12:59:41 2017

@author: Mauro
"""

#Photo message        
photo_message = {'message_id': 105,
 'from': {'id': 407215805, 'first_name': 'PellaTestBot', 'username': 'PellaTestBot'},
 'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle','type': 'private'},
 'date': 1500659777,
 'photo': [{'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABPYNX-pwoGJGmj0AAgI', 'file_size': 1602, 'file_path': 'photos/6021404288133212413.jpg', 'width': 72, 'height': 90},
           {'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABN4OWXpwmBx0mz0AAgI', 'file_size': 30789, 'width': 256, 'height': 320},
           {'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABI2KDwIoYNEbnD0AAgI', 'file_size': 70238,'width': 400, 'height': 500}]
 }        


# Entry message
entry_message = {'message_id': 105,
 'from': {'id': 407215805, 'first_name': 'PellaTestBot', 'username': 'PellaTestBot'},
 'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
 'date': 1500659777, 
 'photo': [{'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABPYNX-pwoGJGmj0AAgI', 'file_size': 1602, 'file_path': 'photos/6021404288133212413.jpg', 'width': 72, 'height': 90
},{'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABN4OWXpwmBx0mz0AAgI', 'file_size': 30789, 'width': 256, 'height': 320}, {'file_id': 'AgADBAAD_agxG0xTkFNPT4XB2UXINu1y4BkABI2KDwIoYNEbnD0AAgI', 'file_size': 70238,'width': 400, 'height': 500}]
}
 
# chat message
new_member_message = {'message_id': 310026,
 'from': {'id': 75583542, 'first_name': 'A'},
 'chat': {'id': -1001055364781, 'title':'?? illuminaughty. ??', 'type': 'supergroup'},
 'date': 1500661484, 
 'new_chat_participant': {'id':75583542, 'first_name': 'A'},
 'new_chat_member': {'id': 75583542, 'first_name': 'A'},
 'new_chat_members':[{'id':75583542, 'first_name': 'A'}]}

# from chat group
chat_message = {'message_id': 310034, 
 'from': {'id': 183961724, 'first_name': 'Pella Jiraiya','username': 'Pellostyle','language_code': 'it-IT'},
 'chat': {'id': -1001055364781, 'title': '?? illuminaughty. ??','type': 'supergroup'}, 
 'date': 1500662990,
 'text': 'it werks'}

# reply

reply_message = {'message_id': 310056,
 'from': {'id': 167778740, 'first_name': 'Carla', 'username': 'Rosinda'},
 'chat':{'id':-1001055364781, 'title': '?? illuminaughty. ??','type': 'supergroup'},
 'date': 1500666749,
 'reply_to_message': {'message_id': 310052, 'from': {'id': 407215805, 'first_name': 'PellaTestBot','username': 'PellaTestBot'},'chat': {'id': -1001055364781, 'title': '?? illuminaughty. ??','type': 'supergroup'}, 'date': 1500666623, 'text': "HELLO I'm a goddamn fucking bot"},
 'text': 'With no manners ??????'}

# leaving group
leaving_group_message ={'message_id': 310108,
 'from': {'id': 183961724, 'first_name': 'Pella Jiraiya','username': 'Pellostyle', 'language_code': 'it-IT'},
 'chat': {'id': -1001055364781, 'title': '?? illuminaughty. ??', 'type': 'supergroup'},
 'date': 1500681944,
 'left_chat_participant': {'id': 407215805, 'first_name':'PellaTestBot','username':'PellaTestBot'},
 'left_chat_member': {'id': 407215805, 'first_name': 'PellaTestBot', 'username':'PellaTestBot'}
 }



# creation of a message
cretion_message = {'message_id': 1297,
 'from': {'id': 407215805, 'first_name': 'PellaTestBot', 'username': 'PellaTestBot'},
 'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type':'private'},
 'date': 1500724360,
 'photo': [{'file_id':'AgADBAADNKkxG09ymVPOsa5DrBOBOWMFvRkABGSGs9TBAdi51owDAAEC',
            'file_size': 1448, 'file_path':'photos/6023971660668971316.jpg',
            'width': 90,
            'height':60},
           {'file_id':'AgADBAADNKkxG09ymVPOsa5DrBOBOWMFvRkABMPW-igwr0ve2IwDAAEC',
            'file_size': 16387,
            'width': 320,
            'height': 213},
           {'file_id': 'AgADBAADNKkxG09ymVPOsa5DrBOBOWMFvRkABAv-YyJLuAmY2YwDAAEC',
            'file_size':61615,'width': 800, 'height': 533},
           {'file_id': 'AgADBAADNKkxG09ymVPOsa5DrBOBOWMFvRkABC7JNDcdC66x2owDAAEC',
            'file_size': 130189, 'width': 1280, 'height': 853},
           {'file_id': 'AgADBAADNKkxG09ymVPOsa5DrBOBOWMFvRkABBX0F-NIC36l14wDAAEC',
            'file_size': 239864, 'width': 1920, 'height': 1280}
           ]
 }


# sticker
sticker_message = {
    'message_id': 17,
    'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username':'Pellostyle', 'language_code': 'it-IT'},
    'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya','username': 'Pellostyle', 'type': 'private'},
    'date':1500796477,
    'sticker': {'width': 512,
                'height':512,
                'emoji': '?',
                'set_name': 'SarcasticPolarBear',
                'thumb': {'file_id':'AAQCABMUSUsNAAQaRjCrpWPrmx6fAQABAg',
                          'file_size': 5738,
                          'width': 128,
                          'height': 128},
                'file_id':'CAADAgADVQADECECEKCWjDbNyTMbAg',
                'file_size': 32730
                }
    }
                
                
# Video Message
video_message = {
    'message_id': 20,
    'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
    'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
    'date':1500797072, 
    'video': {'duration': 10,
              'width': 640,
              'height': 640,
              'mime_type':'video/mp4',
              'thumb': {'file_id': 'AAQEABP9y94ZAASXiwwocvu4UQw1AAIC',
                        'file_size': 2140,
                        'width': 90,
                        'height': 90
                        },
              'file_id': 'BAADBAAD1AADe8ahU1Zt3VZvLj6dAg',
              'file_size': 930381
              }
    }


# GIF message
document_message = {
    'message_id': 21,
    'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
    'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
    'date':1500798073,
    'document': {'file_name': 'jenna-haze-blowjob.gif.mp4',
                 'mime_type': 'video/mp4',
                 'thumb': {'file_id': 'AAQEABNwk1gZAAQRFiFM1-7wOEInAAIC', 'file_size': 2336, 'width': 90, 'height': 51},
                 'file_id': 'CgADBAAD2AADe8ahUw1mbPghFKFmAg',
                 'file_size': 37225}
    }
    
# Forwarded message
fw_message = {
    'message_id': 35,
    'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
    'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
    'date':1500800149,
    'forward_from': {'id': 143604624, 'first_name': 'Vale', 'username':'HellCat0'},
    'forward_date': 1500755580,
    'text': 'Ma qua non stavamo parlando delle tette di Memi'
    }
        
# Reply to forwarded message
replyfw_message = {
    'message_id': 36,
    'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
    'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
    'date':1500800533,
    'reply_to_message': {'message_id': 33,
                         'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
                         'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'},
                         'date': 1500800099,
                         'forward_from': {'id': 139719748, 'first_name': 'Cactus?®', 'username': 'Teknocasa'},
                         'forward_date': 1500755582,
                         'text': 'So serio, sono indeciso tra un paio di posti ahahah'},
    'text': 'Hello fuckers'
    }
    
    
# Query message
query_message = {'id': '790109589471336783',
 'from': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'language_code': 'it-IT'},
 'message': {'message_id': 8854, 'from': {'id': 311499977,'first_name': 'Dirty rate bot', 'username': 'DirtyRateBot'},'chat': {'id': 183961724, 'first_name': 'Pella Jiraiya', 'username': 'Pellostyle', 'type': 'private'}, 'date': 1501131446, 'document': {'file_name': 'AGlgfaZ.mp4', 'mime_type': 'video/mp4', 'thumb': {'file_id': 'AAQEABOJaN0ZAATWSxfjtjKZaXtRAAIC', 'file_size': 3262, 'file_path': 'thumbnails/20859.jpg', 'width': 90, 'height': 67}, 'file_id': 'CgADBAADpQADjKnRU7XiOEl5smbQAg', 'file_size': 766649}, 'caption': 'Uploader AnonID: 0x177ced0d (0??)\n/vote_random or /main_menu'}, 
 'chat_instance': '-8860907535132224251',
 'data': 'v_like_89'}


# Query message dummy for question
query_message_dummy = {'id': '000000000000000000',
 'from': {'id': 000000000, 'first_name': 'AAAAAAAAAAAAA', 'username': 'AAAAAAAAAA', 'language_code': 'aa-AA'},
 'message': {'message_id': 0000, 'from': {'id': 000000000,'first_name': 'AAAAAAAAAAAAAA', 'username': 'AAAAAAAAAAAA'},'chat': {'id': 000000000, 'first_name': 'AAAAAAAAAAAAA', 'username': 'AAAAAAAAAA', 'type': 'private'}, 'date': 1501131446, 'document': {'file_name': 'AAAAAAA.mp4', 'mime_type': 'video/mp4', 'thumb': {'file_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'file_size': 3262, 'file_path': 'thumbnails/20859.jpg', 'width': 90, 'height': 67}, 'file_id': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', 'file_size': 766649}, 'caption': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}, 
 'chat_instance': 'AAAAAAAAAAAAAAAAAAAA',
 'data': 'AAAAAAAAA'}
        
#mystr = '''🥇🏆🏅 First 🏅🏆🎖
#Uploader AnonID: 0x177ced0d (0⚜️)
#Category: boobs
#Score: 👍 5 | 2 👎 
#/show_boobs or /main_menu
#User caption:
#The Milky Way burning bright and rising over Lake Heron, New Zealand
#'''        