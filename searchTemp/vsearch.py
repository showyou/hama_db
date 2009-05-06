#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#sqlalchemyで深さ優先探索
import model
import simplejson

from shuffleByCount import shuffleByCount

exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"


def getAuthData(fileName):
	file = open(fileName,'r')
	a = simplejson.loads(file.read())
	file.close()
	return a

def depthFirstSearch():
	u = getAuthData(conf_path) 
	session = model.startSession(u)
	q = session.query(model.Markov)
	node = {"text":u"yystart","visit":False}
	stack =[] 
	stack.append(node)
	while len(stack) != 0:
		node = stack[-1]
		if node["text"] == u"yyend":
			stack[-1]["visit"] = True
			break
		else:
			if node["visit"] == True:
				stack.pop()
			else:
				print (node["text"])
				stack[-1]["visit"] = True	
				f = q.filter(model.Markov.now==node["text"])
				# 一旦ランダムに並べ替えたほうがいいかも
				tmpList = []
				for fq in f:
					tmpList.append({"name":fq.next,"count":fq.count})
				shuffleList = shuffleByCount(tmpList)
				for i in shuffleList:
					stack.append({"text":i["name"],"visit":False})

	print ("ans")
	for s in stack:
		if s["visit"] == True: 
			#print s
			print s["text"],

depthFirstSearch()	
