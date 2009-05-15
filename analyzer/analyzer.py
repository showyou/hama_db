#!/usr/bin/env python
# -*- coding: utf-8 -*-

# crawlerで入手したテキストを解析する
# 1.マルコフ連鎖テーブル
# 2.最近10min間のホットな単語リスト
# 3.ればreplyリストに入れる

import mecab
import datetime
import re
from sqlalchemy import and_

import model
import simplejson
mecabPath = "/usr/lib/libmecab.so"
g_mecabencode = "euc-jp"
g_systemencode = "utf-8"
g_outencode = g_systemencode
_debug = False 
exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"

dbSession = None

def getAuthData(fileName):
	file = open(fileName,'r')
	a = simplejson.loads(file.read())
	file.close()
	return a

def analyze():
	# dbからデータを読み込む
	userdata = getAuthData(conf_path)
	dbSession = model.startSession(userdata)
	# 前回の更新時間から現在までのデータを入手する
	q = dbSession.query(model.Twit)
	tq = q.filter(model.Twit.isAnalyze == 1) 
	for t in tq:
		#1発言毎
		t.text = RemoveCharacter(t.text)
		t.isAnalyze = 2 
		t_enc = t.text.encode(g_mecabencode,'ignore')
		sarray = mecab.sparse_all(t_enc,mecabPath).split("\n")
		sarray2 = connectUnderScore(sarray)
		markovWordList,topNWordList = TakeWordList(sarray)
		
		#最近出た名詞貯める
		"""for tn in topNWordList:
			hot = model.Hot()
			hot.word = unicode(tn,g_systemencode)
			dbSession.save(hot)
		"""
		#dbSession.save(t)
		dbSession.commit()
		
		AppendMarkov(markovWordList,dbSession)
		AppendCollocation(markovWordList,dbSession)

# A,_,B->A_Bに直す
def connectUnderScore(array):
	retArray = []
	i = 0
	while(i < len(array)-2):
		if array[i+1] == "_":
			retArray.append(array[i] + "_" + array[i+2])
			i+=3
		else:
			retArray.append(array[i])
		i+=1
	print i
	if(i < len(array)):retArray.append(array[i])
	if(i+1 < len(array)):retArray.append(array[i+1])
	return retArray		

# 分解した品詞列から単語群と重要単語を抜き出す
def TakeWordList(sarray):	
    markovWordList = []
    topNWordList = []
    for sa in sarray:
        if sa.startswith("EOS") : break
        sa2 = sa.split("\t")
        sa2[0] = unicode(sa2[0],g_mecabencode,'ignore').encode(g_systemencode,'ignore')
        print_d2(sa2[0])
        markovWordList.append(sa2[0])
        sa3 = sa2[1].split(",")
        if unicode(sa3[0],g_mecabencode) == u"名詞" :
            if unicode(sa3[1],g_mecabencode) == u"固有名詞" or \
                unicode(sa3[1],g_mecabencode) == u"一般":
                if sa2[0] != "yystart" and sa2[0] != "yyend":
                    topNWordList.append(sa2[0])
    return markovWordList,topNWordList

# test内容
# RemoveCharacter("検索サイト http://www.google.com")->検索サイト
# RemoveCharacter("検索サイト [mb]")->検索サイト
# RemoveCharacter("検索サイト *Tw*")->検索サイト
# しかしこれcrawlerでやるべきだよなぁ
def RemoveCharacter(str):
	#余計な記号(http://とか、[hoge]とか)
	reg = re.compile('http://\S+\s*')
	regTag = re.compile('[.*]')
	regTag2 = re.compile('\*.*\*')

	if reg.search(str):
		print_d2("http cut")
		str = reg.sub(' ',str)
	
	if regTag.search(str):
		print_d2("tag cut")
		str = regTag.sub(' ',str)

	if regTag2.search(str):
		print_d2("tag2 cut")
		str = regTag2.sub(' ',str)

	return str

def AppendMarkov(markovWordList,session):
	#マルコフテーブル追加
	pw = "yystart"
	markovWordList.append("yyend")
	q = session.query(model.Markov)
	for cw in markovWordList:
		cw = unicode(cw,g_systemencode)
		# もしnow = pw, next=cwがあったらそれに1足す
		q2 = q.filter(and_(model.Markov.now == pw,
			 model.Markov.next == cw))
		if q2.count() > 0:
			markov = q2[0]
			markov.count += 1
		else:
			markov = model.Markov()
			markov.now =  pw
			markov.next = cw
		
		session.save_or_update(markov)
		pw = cw
	session.commit()

# 共起テーブルに追加
# l : わかち書きした単語のリスト
def AppendCollocation(l,session):
	q = session.query(model.Collocation)
	# yyendだけ無視
	for i in range(len(l)-1):
		a = unicode(l[i],g_systemencode,'ignore')
		for j in range(i+1,len(l)-1):
			b = unicode(l[j],g_systemencode,'ignore')
			# もしa = a, b=bがあったらそれに1足す
			q2 = q.filter(and_(model.Collocation.a == a ,
				 	model.Collocation.b == b))
			if q2.count() > 0:
				c = q2[0]
				c.colloc_count += 1
				#c.sentence_count += 1 
			else:
				c = model.Collocation()
				c.a = a
				c.b = b

			session.save_or_update(c)
	session.commit()

def print_d2(str):
	if _debug:
		print unicode(str,g_systemencode,'ignore').encode(g_outencode,'ignore'),

if __name__ == "__main__":
	analyze()

