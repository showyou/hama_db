#!/usr/bin/env python
# -*- coding: utf-8 -*-

exec_path = "/home/yuki/public_git/donsuke2/"
conf_path = exec_path+"./config.json"

import sys
sys.path.insert(0,exec_path)

from common import twitterscraping
import reply
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
        rep = dbSession.query(model.RetQueue)
        if( rep.count() > 0 ):
            str = reply.do(rep,dbSession)
            sendMessage(str)

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
def sendMessage(str):
    userData = LoadUserData(conf_path)
    tw = twitterscraping.Twitter(userData)
    str = string.replace(str,'yystart','')
    
    #print(str)
    tw.put(str)

quickGenerate()
