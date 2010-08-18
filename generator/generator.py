#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"

import sys
sys.path.insert(0,exec_path)

from common import auth_api
from common import readReplyTable
import vsearch
import reply
# 解析結果に基づいて文章生成(または行動を起こす)
import model
#import scheduler
import datetime
#from sqlalchemy import and_
import random
import string
import simplejson
g_debug = False


def generator():
    #sched = scheduler.Scheduler()
    #sched.schedule()
    u = LoadUserData(conf_path)
    table, footer= readReplyTable.read(exec_path+"/common/replyTable.json")
    dbSession = model.startSession(u)
    if False:
    #if( sched.has_schedule() ):
        str = doSchedule(sched)
    else:
        rep = dbSession.query(model.RetQueue)
        if( rep.count() > 0 ):
            sentence = reply.do(table, rep, dbSession)
        else:
            #try:
                # 予定もreplyもないならhotでも取り出してマルコフ連鎖する
            #    str,sl = CreateMarkovSentenceWithHot(dbSession)
            #except:
            #    print "Unexpected error:", sys.exc_info()[0]
            str,sl = vsearch.depthFirstSearch2("yystart","yyend",15)
            print_d(str)
            print_d(len(sl))
            asl = afterEffect(sl,footer)
            sentence = ""
            for i in asl:
                sentence += i
        sendMessage(sentence)

# 文章生成後の後処理(口癖とか)
# >>> afterEffect([u"りんご",u"は",u"青い",u"。"])
# [u"りんご",u"は",u"青い,u"です。"]
def afterEffect(sl,footer):
    asl = []
    if len(sl) < 3: return []

    for i in range(0,len(sl)):
        appendFlag = True
        if i > 0:
            i2 = i-1
            footer_maru = footer + u"。"
            if sl[i] == u"。" :
                if(sl[i2] != footer and sl[i2] != footer_maru \
                    and sl[i2] != u"。"):
                    asl.append(footer_maru)
                    appendFlag = False
            elif sl[i2] != u"。" and sl[i2] != footer_maru and sl[i2] != footer \
                and i ==len(sl)-1:
                asl.append(footer_maru)
                appendFlag = False
            else:
                asl.append(wstrcat(sl[i-1],sl[i]))
                appendFlag = False

        if appendFlag :
            asl.append(sl[i])
    return asl

"""
    アルファベットが並んだら空白開ける
"""
def wstrcat(a,b):
    if (a == u"@"): result = b + " "
    else:    result = b
    return result


def CreateMarkovSentenceWithHot(session):
    w = SelectHotWord(session)
    fw,sl1 = vsearch.depthFirstSearch(session,w,u"yyend",8)
    bw,sl2 = vsearch.depthFirstSearch(session,w,u"yystart",8,True)
    q3 = model.SelectedHotWord()
    q3.word = w
    session.save(q3)
    session.commit()
    print_d(len(sl1))
    print_d(len(sl2))
    str =bw+fw
    sl = sl2+sl1
    return str,sl


def LoadUserData(fileName):
    #ファイルを開いて、データを読み込んで変換する
    #データ形式は(user,password)
    try:
        file = open(fileName,'r')
        a = simplejson.loads(file.read())
        file.close()
    except IOError:
        print "LoadUserData error" 
        sys.exit(1)
    return a


# Twitterにメッセージ投げる
def sendMessage(str):
    userdata = LoadUserData(conf_path)
    tw = auth_api.connect(userdata["consumer_token"],
        userdata["consumer_secret"], exec_path+"/common/")
    str = string.replace(str,'yystart','')
    str = string.replace(str,'yyend','')
    if g_debug :
        print(str)
    else:
        tw.update_status(str)


def SortWordCnt(wordcnt):
    words = wordcnt.keys()
    words.sort(key=lambda x: wordcnt[x], reverse=True)
    return words

def TopN(session, wordcnt,n):
    wordRank = SortWordCnt(wordcnt)
    i = 0
    lst = []
    for w in wordRank:
        #print_d(w),
        #print "x" + str(wordcnt[w])
        lst.append(w)
        tw = model.Top10Words()
        tw.word = w
        session.save(tw)
        i+=1
        if i >= n : break
    session.commit()
    return lst


# 最近人気の単語から一つ抜き出す
def SelectHotWord(session):
    q = session.query(model.Hot)
    q2 = q.filter(model.Hot.datetime > datetime.datetime.now() - datetime.timedelta(minutes=10))
    
    # ランダムに一つ選択する(重み付けなし)
    hotWord = {}
    for hot in q2:
        h = hot.word
        if hotWord.has_key(h):
            hotWord[h]+=1
        else:
            hotWord[h]=1

    hotNArray = TopN(session,hotWord,10)
    w = random.choice(hotNArray)
    print_d("hot"+w)    
    return w 


# 数量に応じて結果を返す
# ex: [a:5, b:3, c:2] なら aが5割、bが3割、cが2割の確率
def GetQueryByCount(filter):
    total = 0
    for q in filter:
        total += q.count

    t = random.randint(1,total)
    total2 = 0
    for q in filter:
        total2 += q.count
        if t <= total2: 
            result = q
            break
    # ここまででresultにはなにか入ってるはず 
    return result 

def print_d(str):
    if g_debug:
        print(str)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            print "debug mode"
            g_debug = True
    #generator()
generator()

