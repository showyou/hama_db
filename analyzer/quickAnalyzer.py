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
import simplejson
import picklefile

g_systemencode = "utf-8"
g_outencode = g_systemencode
_debug = True
exec_path = "/home/yuki/gitrep/project/hama_db/"
conf_path = exec_path+"config.json"

dbSession = None
regOhayou = re.compile(u'おはよう')
regTadaima = re.compile(u'ただいま|帰宅')
regTukareta = re.compile(u'(疲|つか)れた|タスケテ|助けて')
regChucchu = re.compile(u'甘えたい|ちゅっ')
regMoyashi = re.compile(u'もやし')
regAthama = re.compile(u'(@yuka_|@ゆーか|@ゆうか)(.*)')
#regAthama = re.compile(u'(@yuka_|@ゆーか|@ゆうか)')


def LoadUserData(fileName):
	#ファイルを開いて、データを読み込んで変換する
 	#データ形式は(user,password)
	try:
		file = open(fileName,'r')
		a = simplejson.loads(file.read())
		file.close()
	except:
		print ("IO Error",fileName)
		sys.exit(1)
	return a

def quickAnalyze():
	# dbからデータを読み込む
	u = LoadUserData(conf_path)
	dbSession = model.startSession(u)
	# 前回の更新時間から現在までのデータを入手する

	q = dbSession.query(model.Twit)
	tq = q.filter(model.Twit.isAnalyze == False)
	for t in tq:
		#1発言毎
		t.text = RemoveCharacter(t.text)
		print (t.text)
		AnalyzeReply(t,dbSession)
		t.isAnalyze = True
		#dbSession.save(t)
	dbSession.commit()

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
def AnalyzeReply(x,session):

    d = model.RetQueue()
    d.user = ""
         
    if regOhayou.search(x.text):
        print_d2("ohayou hit")
        CheckTime("ohayou",datetime.timedelta(hours=10),x,d,session)

    elif regTadaima.search(x.text):
        print_d2("tadaima hit")
        CheckTime("tadaima",datetime.timedelta(minutes=30),x,d,session)
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
    else:
        match2 = regAthama.match(x.text)
        if match2:
            d.user = x.user
            d.text = match2.group(2)
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

quickAnalyze()
