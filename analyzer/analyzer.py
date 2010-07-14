#!/usr/bin/env python
# -*- coding: utf-8 -*-

# crawlerで入手したテキストを解析する
# 1.マルコフ連鎖テーブル
# 2.最近10min間のホットな単語リスト
# 3.ればreplyリストに入れる
import sys
import mecab
import datetime
import re
from sqlalchemy import and_

import model
import simplejson

from collections import defaultdict
#import psyco
#psyco.full()

mecabPath = "/usr/lib/libmecab.so.1"
g_mecabencode = g_systemencode = "utf-8"
g_outencode = g_systemencode
_debug = False 
exec_path = "/home/yuki/public_git/hama_db"
conf_path = exec_path+"/common/config.json"
common_path = exec_path+"/common/"

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

    # ToDo:ここ、1000件ずつ取って、一定件数溜まったらDBに書き込むように変えられないか？

    insertData = defaultdict(int)
    while(True):
        tq = q.filter(model.Twit.isAnalyze == 1)[:1000]
        i = 0
        if len(tq) == 0: break
        for t in tq:
            #1発言毎
            t.text = removeCharacter(t.text)
            t.isAnalyze = 2 
            t_enc = t.text.encode(g_mecabencode,'ignore')
            sarray = mecab.sparse_all(t_enc,mecabPath).split("\n")
            sarray2 = connectUnderScore(sarray)
            markovWordList,topNWordList = takeWordList(sarray2)
            print len(markovWordList)
            
            #最近出た名詞貯める
            """for tn in topNWordList:
                hot = model.Hot()
                hot.word = unicode(tn,g_systemencode)
                dbSession.save(hot)
            """
            dbSession.update(t)
            appendMarkov(markovWordList, dbSession, insertData)
            #appendCollocation(markovWordList,dbSession)
            i+= 1
            if i >= 1000:
                insertMarkovData2DB(dbSession, insertData)
                dbSession.commit()
                insertData = defaultdict(int)
                i = 0

    if len(insertData) > 0:
        insertMarkovData2DB(dbSession, insertData)
        dbSession.commit()


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
	#print i
	if(i < len(array)):retArray.append(array[i])
	if(i+1 < len(array)):retArray.append(array[i+1])
	return retArray		


# 分解した品詞列から単語群と重要単語を抜き出す
def takeWordList(sarray):	
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



replacePattern = [
    ['http://\S+\s*', '', 'http'],
    ['\[.*\]', '', 'tag'],
    ['\*.*\*', '', 'tag2'],
    ['(B|b)rowsing:.*', '', 'browsing'],
    ['(RT|QT)\s.*:.*', '', 'RT'],
    ['#\S*', '', 'hashtag']
]

for rp in replacePattern:
    rp[0] = re.compile(rp[0])


# test内容
# しかしこれcrawlerでやるべきだよなぁ
def removeCharacter(str):
    #余計な記号(http://とか、[hoge]とか)
    for rp in replacePattern:
        if rp[0].search(str):
            print_d2(rp[2] + " cut")
            str = rp[0].sub(rp[1], str)
    
    return str


import datetime
def appendMarkov(markovWordList, session, insertData):
    #マルコフテーブル追加
    #DBに直接入れるんじゃなくて、一旦メモリにでも保管
    # pw = previous word cw = current word nw = next word
    pw = ""
    cw = "yystart"
    markovWordList.append("yyend")
    q = session.query(model.Markov)
    for nw in markovWordList:
        nw = unicode(nw,g_systemencode)
        insertData[(pw, cw, nw)]+=1
        # もしnow = pw, next=cwがあったらそれに1足す
        pw = cw
        cw = nw
        

import pytc
import pickle
import struct
def insertMarkovData2DB(dbSession, insertData):
    #matope風に一旦ファイル書き出し 一括書き込みの方が早いかも
    #ベンチ必要

    db = pytc.BDB(common_path + 'markov.bdb', pytc.BDBOWRITER | pytc.BDBOCREAT)
    invertIndex = {}
    #今回はprev, nowに対するnextのテーブルだけど、now,nextに対してprevを得る奴も必要かも
    for gram, count in insertData.iteritems():
        #print gram, count
        
        indexKeyGram = (gram[0], gram[1])

        key = pickle.dumps(gram)
        print key
        indexKey = pickle.dumps(indexKeyGram)
        #print "iKG", indexKeyGram, indexKey
        value = gram[2]
        if not (db.has_key(key)):
            db[key] = struct.pack('i', 1)
        else:
            db.addint(key,insertData[gram])
        print struct.unpack('i', db[key])[0]
        if not (invertIndex.has_key(indexKey)):
            invertIndex[indexKey] = set(value)
        else:
            invertIndex[indexKey].add(value)
       
        """
        try:
            #pass

            dbSession.execute(u'call replace_markov("%s","%s","%s","%s")'\
                           % (gram +(count,) ) )
        except:
            print gram
            print "Unexpected error:", sys.exc_info()
        #
            q2 = q.filter(and_(model.Markov.now == pw,
            model.Markov.next == cw))
           if q2.count() > 0:
            markov = q2.one()
            markov.count += 1
        else:
            markov = model.Markov()
            markov.now =  pw
            markov.next = cw
        session.save_or_update(markov)"""
    db.close()
    

    # 転置インデックス書き込む
    db = pytc.BDB(common_path + 'invertIndex.bdb', pytc.BDBOWRITER | pytc.BDBOCREAT)
    for key, value in invertIndex.iteritems():
        if db.has_key(key):
            tmpValue = pickle.loads(db[key])
            tmpValue.update(value)
        else:
            tmpValue = value
        
        db[key] = pickle.dumps( tmpValue )
    db.close()
    

# 共起テーブルに追加
# l : わかち書きした単語のリスト
def appendCollocation(l,session):
	q = session.query(model.Collocation)
	for i in range(len(l)-1):
		a = unicode(l[i],g_systemencode,'ignore')
		for j in range(i+1,len(l)):
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

