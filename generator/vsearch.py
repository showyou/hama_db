#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#sqlalchemyで深さ優先探索
import model
import simplejson

from shuffleByCount import shuffleByCount

g_depthMax = 30 # 最大探索深さ(=単語数)
exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./config.json"


def getAuthData(fileName):
	file = open(fileName,'r')
	a = simplejson.loads(file.read())
	file.close()
	return a

def depthFirstSearch(session,startWord,endWord,depthMax,reverse=False):
	if reverse: type = model.Markov.next
	else: type = model.Markov.now	
	q = session.query(model.Markov)
	node = {"text":startWord,"visit":False}
	stack =[] 
	stack.append(node)
	depth = 1 # 探索深さ
	while len(stack) != 0:
		node = stack[-1]
		if node["text"] == endWord:
			stack[-1]["visit"] = True
			break
		else:
			if node["visit"] == True or depth >= 30:
				stack.pop()
				depth -= 1
			else:
				#print (node["text"])
				stack[-1]["visit"] = True
				depth += 1
				f = q.filter(type==node["text"])
				tmpList = []
				for fq in f:
					if reverse:
						tmpList.append({"name":fq.now,"count":fq.count})
					else:
						tmpList.append({"name":fq.next,"count":fq.count})
				shuffleList = shuffleByCount(tmpList)
				for i in shuffleList:
					stack.append({"text":i["name"],"visit":False})

	#print ("ans")
	sentence = ""
	selectwordList = []
	if reverse : stack.reverse()
	for s in stack:
		if s["visit"] == True:
			sa = s["text"]
			#print s
			sentence += sa
			selectwordList.append(sa)
	return sentence,selectwordList

if __name__ == "__main__":
	u = getAuthData(conf_path) 
	session = model.startSession(u)
	fs,sl1 = depthFirstSearch(session,u"yystart",u"yyend",g_depthMax,False)
	bs,sl2 = depthFirstSearch(session,u"yyend",  u"yystart",g_depthMax,True)	
	print fs
	print bs
