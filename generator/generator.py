#!/usr/bin/env python
# -*- coding: utf-8 -*-


exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"

import sys
sys.path.insert(0,exec_path)

from common import twitterscraping
import vsearch
# 解析結果に基づいて文章生成(または行動を起こす)
import model
#import scheduler
import datetime
#from sqlalchemy import and_
import random
import string
import sys
import simplejson


def generator():
	#sched = scheduler.Scheduler()
	#sched.schedule()
	u = LoadUserData(conf_path)
	dbSession = model.startSession(u)
	if False:
	#if( sched.has_schedule() ):
		str = doSchedule(sched)
	else:
		reply = dbSession.query(model.RetQueue)
		if( reply.count() > 0 ):
			str = DoReply(reply,dbSession)
		else:
			try:
				# 予定もreplyもないならhotでも取り出してマルコフ連鎖する
				str = CreateMarkovSentenceWithHot(dbSession)
			except:
				str,sl = vsearch.depthFirstSearch(dbSession,"yystart","yyend")
			SendMessage(str)


def CreateMarkovSentenceWithHot(session):
	w = SelectHotWord(session)
	fw,sl1 = vsearch.depthFirstSearch(session,w,"yyend")
	bw,sl2 = vsearch.depthFirstSearch(session,"yystart",w,True)
	str =bw+fw
	return str

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
	str = string.replace(str,'yyend','')
	#print(str)
	tw.put(str)

def SortWordCnt(wordcnt):
    words = wordcnt.keys()
    words.sort(key=lambda x: wordcnt[x], reverse=True)
    return words

def TopN(wordcnt,n):
	wordRank = sortWordCnt(wordcnt)
	i = 0
	lst = []
	for w in wordRank:
		#print_d(w),
		#print "x" + str(wordcnt[w])
		lst.append(w)
		i+=1
		if i >= n : break
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

	hotNArray = TopN(hotWord,10)
	w = random.choice(hotNArray)
	print ("hot"+w)	
	return w 

# 返事考える
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
		elif r.text == 'at':
			s = random.choice((u'あほか',u'ないわー',u'うんうん',u'ちゅっちゅー<3',u'ずこー'))
			sentence = "@"+r.user+" "+s
		elif r.text == 'moyashi':
			s = u'だれがもやしですか'
			sentence = "@"+r.user+" "+s
		sendMessage(sentence)
		session.delete(r)	
		if sentence != "":
			break
	session.commit()
	return sentence 

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


#session = model.startSession()
generator()
#CreateMarkovSentenceWithHot(session)

