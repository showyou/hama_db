#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import re
import os
import simplejson
from collections import defaultdict
import codecs
import random

session = None
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"
common_path = exec_path+"/common/"
sys.path.insert(0,exec_path)
from common import auth_api, model, mecab


def getAuthData(fileName):
    file = open(fileName,'r')
    a = simplejson.loads(file.read())
    file.close()
    return a


def remove_at(session):
    # reply_wordを含む文章を返す
    query = session.query(model.Reply).filter(\
            model.Reply.reply_text.like('%@%'))[0:100000]
    for q in query:
        print q.reply_text
        try:
            q.reply_text = re.sub("([^@]*)@\S+ ", "\1", q.reply_text)
            q.reply_text = re.sub("([^@]*)@.*", "\1", q.reply_text)
            q.src_text = re.sub("([^@]*)@\S+ ", "\1", q.src_text)
            q.src_text = re.sub("([^@]*)@.*", "\1", q.src_text)

            session.add(q)
        except:
            print "error"
        session.flush()
    session.commit()
    
    # reply_wordを含む文章を返す
    query = session.query(model.Reply).filter(\
            model.Reply.src_text.like('%@%'))[0:10000]
    for q in query:
        print q.src_text
        q.reply_text = re.sub("([^@]*)@\S+ ", "\1", q.reply_text)
        q.src_text = re.sub("([^@]*)@\S+ ", "\1", q.src_text)
        q.reply_text = re.sub("([^@]*)@.*", "\1", q.reply_text)
        q.src_text = re.sub("([^@]*)@.*", "\1", q.src_text)
        session.add(q)
        session.flush()
    session.commit()

    query = session.query(model.Reply)[0:10000]
    for q in query:
        print len(q.reply_text)
        if len(q.reply_text) == 0 or len(q.src_text) ==0:
            session.delete(q)
    session.commit()
    return
    #raise


def main():
    #sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    user = getAuthData(conf_path)
    session = model.startSession(user)

    api = auth_api.connect(user["consumer_token"], user["consumer_secret"])
    #api = tweepy_connect.connect()

    remove_at(session)


if __name__ == "__main__":
    main()

