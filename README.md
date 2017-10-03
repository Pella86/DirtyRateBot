# DirtyRateBot 
##### _(v. 0.1.0)_
Telegram bot that allows people to share pictures, gifs and videos and other people can rate them.

https://t.me/DirtyRateBot

## Introduction
The bot is very simple, users can upload media and chose the uploading category. The media will be then presented to the other users with the possibility to rate them. The user is presented with a private interface
The users can rate like (👍) or dislike (👎) this will then give a score to the media.
The user earns reputation depending on the score of its media, and earns also points that can spend to adjust his reputation or buy categories.

## Bot mechanics
The next section is dedicated to explain the bot fundamental mechanics from a Telegram user point of view

### The user menu (private interface)
![main menu](/README_data/main_menu.png)

When the user opens the bot, the user is presented with several choices.
* /categories: gives access to the rating interface
* /top_media: shows the first three media of a given category
* /profile: will give access to the profile page
* /upload: will allow the user to upload a media
* /help: the main help menu


### Categories
![categories menu](/README_data/Screenshot_1.png)

The bot has several categories ordered by score (the sum of the score of the media) and they are displayed to the user in pages.
The lower the category score the farther the page will be.
The user will be able to rate pictures only once (a vote is forever).

### The media
![categories menu](/README_data/Screenshot_5.png)

The media is presented to the user with 5 options.
* like (👍): gives one point to the media and gives a point to the user (₽), the uploader gains a point (₽) 
* dislike (👎): adds a negative point to the media and give one point to the user (₽), the uploader loses a point (₽)
* hide media: the media will not be shown again to the user
* report media: in case that illegal content or material non pertinent to the category gets uploaded
* report category: since is user based some categories might be attracting illegal material, so they will be deleted

The top media menu is the same as the categories but will show the 3 best rated pictures per category.

### Profile Menu
![categories menu](/README_data/Screenshot_3.png)

The profile menu allows a customization of the user profile.

* Username: each user get a randomly generated unique username, which can be changed with the command /set_nickname
* The points system: The user receives different points from the media, and in this subsection he can manage them
* The upload menu: It is a summary of the user uploaded media and the user can also access to its uploaded media
* Add category: the user, given enough points, can buy a new category
* The user top chart: users are listed in order of reputation and karma

### The top chart
![categories menu](/README_data/photo_2017-09-21_00-05-36.jpg)

The users are presented in order of reputation, the reputation can be gained in the profile section, karma and reputation points help to reach the top

