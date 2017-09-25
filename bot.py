# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 23:54:27 2017

@author: userpv
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to send timed Telegram messages
# This program is dedicated to the public domain under the CC0 license.


from telegram.ext import Updater, CommandHandler, Job
import logging
import telegram
import re
from difflib import SequenceMatcher
from bs4 import BeautifulSoup, NavigableString, Tag

import requests


import pandas as pd

# Enable logging


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi! Use /singlish to find a word meaning')


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
        
def ReadEdmw():
        
    url = r"http://forums.hardwarezone.com.sg/eat-drink-man-woman-16/acronyms-lingo-peculiar-edmw-1738415.html"
    
    r  = requests.get(url)
    
    data = r.text
    
    soup = BeautifulSoup(data, features="lxml")
    
    Text = []
    for a in soup.findAll('b'):
        c = str(a.nextSibling)
        a2 = re.sub('\n|\s|\t|<.*?>','',str(a))
        c = re.sub('\n|\r|\t|:',' ',c)
        b = [a2,c.strip()]    
        Text.append(b)
        
    return(Text)


def ReadWiki():
    url = r"https://en.wikipedia.org/wiki/Singlish_vocabulary"
    
    r  = requests.get(url)
    
    data = r.text
    
    soup = BeautifulSoup(data, features="lxml")
    
    Text = []
    for a in soup.findAll('tr'):
        c = a.findAll('td')
        Text2 = []
        for d in c:
            b = re.sub('<.*?>',' ',str(d)).strip()
            Text2.append(b)
        if len(Text2) > 0:
            Text.append(Text2)
    return(Text)



Wiki = ReadWiki()
Edmw = ReadEdmw()

def singlish(bot,update,args):
    String = " ".join(args)
    
    for i in Edmw:
        if String.lower() == i[0].lower():
            Ans = i
        
    for i in Wiki:
        if String.lower() == i[0].lower():
            Ans = i
    
    try: 
        Reply = ('\n\n'.join(Ans))
    except:
        sim = 0
        for i in Edmw:
             sim2 = similar(String.lower(),i[0].lower())
             if sim < sim2:
                 sim = sim2
                 Ans = i
        
        for i in Wiki:
             sim2 = similar(String.lower(),i[0].lower())
             if sim < sim2:
                 sim = sim2
                 Ans = i
        Reply = ('Did you mean?\n\n' + '\n\n'.join(Ans))             
    
    update.message.reply_text(Reply)



def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))



def main():
    updater = Updater("355993039:AAFkJmcjKgQLWz3IWBGz1niXLFq8zq1vH6M")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("singlish", singlish,
                                  pass_args=True
                                  ))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
