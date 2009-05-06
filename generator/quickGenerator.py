#!/usr/bin/env python
# -*- coding: utf-8 -*-

exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"

import sys
sys.path.insert(0,exec_path)

from common import twitterscraping
# 解析結果に基づいて文章生成(または行動を起こす)
import model
#import scheduler
import datetime
#from sqlalchemy import and_
import random
import string
import sys
import simplejson

def quickGenerate():
    #sched = scheduler.Scheduler()
    #sched.schedule()
    u = LoadUserData(conf_path)
    dbSession = model.startSession(u)
    if False:
        if( sched.has_schedule() ):
            str = doSchedule(sched)
    else:
        reply = dbSession.query(model.RetQueue)
        if( reply.count() > 0 ):
            str = DoReply(reply,dbSession)


def LoadUserData(fileName):
    #ファイルを開いて、データを読み込んで変換する
    #データ形式は(user,password)
    try:
        file = open(fileName,'r')
        a = simplejson.loads(file.read())
        file.close()
    except:
        sys.exit(1)
    return a


# Twitterにメッセージ投げる
def SendMessage(str):
    userData = LoadUserData(conf_path)
    tw = twitterscraping.Twitter(userData)
    str = string.replace(str,'yystart','')
    
    #print(str)
    tw.put(str)

#返事考える
def DoReply(reply,session):
    sentence = ""
    for r in reply:
        if r.text == "ohayou" :
            sentence = ".@"+r.user
            l2num = 1 
            while l2num < reply.count():
                l2 = reply[l2num]
                if l2.text == "ohayou":
                    sentence += " @"+l2.user
                    session.delete(l2)
                else:
                    l2num += 1
                if len(sentence) > 100: break
            sentence += " "+random.choice((u'おはようございますー',u'おはおはー',u'おっはー'))
        elif r.text == 'tadaima':
            sentence = "@"+r.user+" "+random.choice((u" おかえり～",u" おかえりなさい"))
        elif r.text == 'otukare':
            s = random.choice((u'おつかれさま～',u'あともうちょっとよ',u'私が見守っているのよ！',u'大丈夫?',u'大丈夫,きっとなんとかなるわよ！',u'なでなで〜'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'chucchu':
            s = random.choice((u'ちゅっちゅー<3',u'にゃ〜',u'にゃん♪',u'うふふー'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'moyashi':
            s = u'だれがもやしですか'
            sentence = "@"+r.user+" "+s
        else:
            s = random.choice((u'はい',u'にゃん♪',u'うんうん',u'ちゅっちゅー<3',u'ずこー'))
            sentence = "@"+r.user+" "+s
        SendMessage(sentence)
        session.delete(r)   
        if sentence != "":
            break
    session.commit()
    return sentence 

quickGenerate()
