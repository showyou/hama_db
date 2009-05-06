#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#sqlalchemyで深さ優先探索
import model
<<<<<<< HEAD:searchTemp/vsearch.py

def depthFirstSearch():
	session = model.startSession()
=======
import simplejson

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
>>>>>>> a1608d1e907a6c03f0f5132705df0d50b5898ec9:searchTemp/vsearch.py
	q = session.query(model.Markov)
	node = {"text":u"A","visit":False}
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
				for fq in f:
					stack.append({"text":fq.next,"visit":False})

	print ("ans")
	for s in stack:
		if s["visit"] == True: print s
depthFirstSearch()	
