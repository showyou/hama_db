#!/usr/bin/env python
# -*- coding: utf-8 -*-

exec_path = "/Users/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"

import sys
sys.path.insert(0,exec_path)

from common import twitterscraping
import simplejson
import model
import datetime
import toDate
from   sqlalchemy import and_


#ログに入れない人のリスト
g_ngUser = [ 
	"ha_ma", "donsuke", "yuka_" 
]



dbSession = None

def getAuthData(fileName):
	file = open(fileName,'r')
	a = simplejson.loads(file.read())
	file.close()
	return a

# NGUserならTrue そうでないならFalse 
def isNGUser(user):
	for u in g_ngUser:
		if u == user: return True
	return False

# twitterから発言を取ってきてDBに格納する
userdata = getAuthData(conf_path)
tw = twitterscraping.Twitter(userdata)
l = tw.get("yuka_")
dbSession = model.startSession(userdata)

#for u in l:
	#twList = tw.getWithUser(u) # lastTime以降の発言全部取得

for td in l:
	if td[0] == userdata["user"]:continue
	d = toDate.toDate(td[2],"%a %b %d %H:%M:%S +0000 %Y")
	query = dbSession.query(model.Twit).filter(and_(model.Twit.datetime==d,model.Twit.user==td[0]))
	if( query.count() > 0 ): continue
	if( isNGUser(td[0]) ): continue
	t = model.Twit()
	t.user = td[0]
	t.text = td[1]
	t.datetime = d
	if td[5] != None:
		t.replyID = td[5]
	dbSession.save(t)
	dbSession.commit()


