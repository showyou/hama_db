#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# /home/*/hama_dbとかが返ってくる
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"
sys.path.insert(0,exec_path)
from common import auth_api

import simplejson
import model
import datetime
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


def main():

    # twitterから発言を取ってきてDBに格納する
    userdata = getAuthData(conf_path)
    tw = auth_api.connect(userdata["consumer_token"],
        userdata["consumer_secret"], exec_path+"/common/")

    dbSession = model.startSession(userdata)

    page_number = 0
    update_flag = True
    while update_flag:
        update_flag = False
        l = tw.home_timeline(page = page_number)
        page_number += 1
        if page_number > 10: break
        for s in l:
            #if s.author.screen_name == userdata["user"]:continue
            jTime = s.created_at + datetime.timedelta(hours = 9)
            name = unicode(s.user.screen_name)
            query = dbSession.query(model.Status).filter(
                and_(model.Status.datetime== jTime, 
                        model.Status.user==name ))
            if( query.count() > 0 ): continue
            if( isNGUser(name) ): continue
            update_flag = True

            t = model.Status()
            t.user = name
            t.text = s.text
            t.datetime = jTime
            t.replyID = s.in_reply_to_status_id
            t.tweetID = s.id
            #print s.id
            dbSession.add(t)
            dbSession.commit()

if __name__ == "__main__":
    main()
