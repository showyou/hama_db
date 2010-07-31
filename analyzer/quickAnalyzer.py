#!/usr/bin/env python
# -*- coding: utf-8 -*-

# analyzerのうちの単純応答だけ高速に出す
# 1min程度cronで
# 最初過去時間は1min固定->lastUpdateに
import mecab
import model
import datetime
import re
import sys
from sqlalchemy import and_

import picklefile
import simplejson
mecabPath = "/usr/lib/libmecab.so.1"
g_mecabencode = g_systemencode = "utf-8"
g_outencode = g_systemencode
_debug = False 
homepath = "/home/yuki/public_git/hama_db"
exec_path = "/home/yuki/public_git/hama_db"
conf_path = exec_path+"/common/config.json"

dbSession = None
regOhayou = re.compile(u'おはよう|起床|オハヨウ')
regTadaima = re.compile(u'ただいま|帰宅($|。|し(まし)*た($|。))')
regTukareta = re.compile(u'(疲|つか)れた|タスケテ|助けて')
regChucchu = re.compile(u'甘えたい|ちゅっ')
regMoyashi = re.compile(u'もやし')
regAthama = re.compile(u'(@yuka_|@ゆうか|@ゆーか)(.*)')
regWanwan = re.compile(u'わんわん')
regMukyu = re.compile(u'むきゅー')
regBaribari = re.compile(u'ﾊﾞﾘﾊﾞﾘ|ばりばり|バリバリ|マジックテープ')
regGohan = re.compile(u'(@yuka_|@ゆうか|@ゆーか)(.*)(ご飯|ごはん|めし)(あげる|やる|どぞ|どうぞ)')
regMayuri = re.compile(u'トゥットゥルー')

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


def quickAnalyze():
	# dbからデータを読み込む
	u = LoadUserData(conf_path)
	dbSession = model.startSession(u)
	# 前回の更新時間から現在までのデータを入手する

	q = dbSession.query(model.Twit)
	tq = q.filter(model.Twit.isAnalyze == 0)[:10000]
	for t in tq:
		#1発言毎
		t.text = RemoveCharacter(t.text)
		#print_d2(t.text)
		analyzeReply(t,dbSession)
		t.isAnalyze = 1 
		t_enc = t.text.encode(g_mecabencode,'ignore')
		sarray = mecab.sparse_all(t_enc,mecabPath).split("\n")
		sarray2 = connectUnderScore(sarray)
		markovWordList,topNWordList = TakeWordList(sarray)
		
		#最近出た名詞貯める
		for tn in topNWordList:
			hot = model.Hot()
			hot.word = unicode(tn,g_systemencode)
			dbSession.save(hot)
        dbSession.save_or_update(t)
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
        #markovWordList.append(sa2[0])
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


def print_d2(str):
	if _debug:
		print unicode(str,g_systemencode,'ignore').encode(g_outencode,'ignore'),


def CheckTime(type,timespan,x,d,session):
	
	replyFlag = False
	ot = None
	q = session.query(model.OhayouTime).filter(and_(model.OhayouTime.user == x.user,model.OhayouTime.type == type))
	if q.count() > 0:
		ot = q[0]
		if datetime.datetime.today() - ot.datetime > timespan:
			replyFlag = True
		else:
			pass
	else:
		replyFlag = True

	if replyFlag:
		d.user = x.user
		d.text = type
		if ot == None:
			ot = model.OhayouTime()
			ot.user = d.user
			ot.type = d.text
		ot.datetime=datetime.datetime.today()
		session.save_or_update(ot)
	return d


#所謂「おはようなのよ」
def analyzeReply(x,session):

    d = model.RetQueue()
    d.user = ""
         
    if regOhayou.search(x.text):
        print_d2("ohayou hit")
        CheckTime("ohayou",datetime.timedelta(hours=10),x,d,session)

    elif regTadaima.search(x.text):
        print_d2("tadaima hit")
        CheckTime("tadaima",datetime.timedelta(minutes=30),x,d,session)
    elif regGohan.search(x.text):
        print_d2("gohan hit")
        d.user = x.user
        d.text = "gohan"
    elif regTukareta.search(x.text): 
        print_d2("otukare hit")
        d.user = x.user
        d.text = "otukare"
    elif regChucchu.search(x.text):
        print_d2("chucchu hit")
        d.user = x.user
        d.text = "chucchu"
    elif regMoyashi.search(x.text):
        print_d2("moyashi hit")
        d.user = x.user
        d.text = "moyashi"
    elif regMayuri.search(x.text):
        print_d2("mayuri hit")
        d.user = x.user
        d.text = "mayuri"
    elif regBaribari.search(x.text):
        print_d2("baribari hit")
        CheckTime("baribari",datetime.timedelta(minutes=10),x,d,session)
    else:
        match2 = regAthama.match(x.text)
        if match2:
            d.user = x.user
            text = match2.group(2)

            d.text = 'at'#text
    	    print "at:",
		
    # @(英数字)空白 -> user
    # この辺も直す必要ありそうだなぁ。っていうかin_reply_status_idとれるし、そっち使った方が早そう
    """
    reg2 = re.compile('@(\S+)\s')
    match2 = reg2.match(x.text)
    if match2:
        replyUser = match2.group(1)
        d.user = x.user
        d.text = "at"
    
    print "match:",print replyUser
        try:
            b = tw.getWithUser("showyou",replyUser)
            for y in b:
                if toDate.toDate(x[2]) - toDate.toDate(y[2]) >\
                    datetime.timedelta(days =0) :
                l = {}
                l["reply"] = {"user":x[0],"text":x[1].encode("utf-8")}
                l["src"] = {"user":y[0],"text":y[1].encode("utf-8")}
                retList.append(l)
                break
        except:
            pass
    """

    if( d.user != "" ):
        session.save(d)
    session.commit()

if __name__ == "__main__":
	quickAnalyze()
