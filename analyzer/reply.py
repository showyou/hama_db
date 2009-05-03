#!/usr/bin/env python
#! -*- coding:utf-8 -*-

# 返信やりとりを解析する
import re
import replyModel

def analyze():
	regAt = re.compile("@(.*?) (.*)")
	session = replyModel.startSession()
	q = session.query(model.Twit)
	for i in q :
		r = regAt.search(q.text)
		if r != None: 
			print r.group(1), "+", r.group(2)
