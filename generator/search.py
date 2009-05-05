#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#sqlalchemyで深さ優先探索
import random
import model

# 深さ優先探索
# reverse = true で文の初めに向かって探索
def depthFirstSearch(reverse,start=u"yystart",end=u"yyend"):
	session = model.startSession()
	q = session.query(model.Markov)
	node = {"text":start,"visit":False,"count":0}
	stack =[] 
	stack.append(node)
	while len(stack) != 0:
		node = stack[-1]
		if node["text"] == end:
			stack[-1]["visit"] = True
			break
		else:
			if node["visit"] == True:
				stack.pop()
			else:
				print (node["text"])
				stack[-1]["visit"] = True
				if reverse:
					f = q.filter(model.Markov.next==node["text"])
				else:	
					f = q.filter(model.Markov.now==node["text"])

				tmpStack = [] # マルコフ的選択前の仮スタック
				for fq in f:
					if reverse:	text = fq.now
					else:		text = fq.next
					tmpStack.append(
						{"text":text,"visit":False,"count":fq.count} )

				stack += markovSort(tmpStack)

	print ("ans")
	result = []
	sentence = ""
	for s in stack:
		if s["visit"] == True: 
			if reverse:
				result.insert(0,s["text"])
				sentence = s["text"] + sentence
			else:
				result.append(s["text"])
				sentence += s["text"]

	return sentence,result

# マルコフ的に一個ずつランダムに選択していき並び替える
# in [ a b c d ] / out [ d a c b ]
def markovSort(tmpStack):
	ansStack = []

	while len(tmpStack) != 0:
		q = getQueryByCount(tmpStack)
		ansStack.insert(0,q)
		tmpStack.remove(q)
	return ansStack

def getQueryByCount(tmpStack):

	total = 0
	for q in tmpStack:
		total += q["count"]

	t = random.randint(1,total)
	total2 = 0
	for q in tmpStack:
		total2 += q["count"]
		if t <= total2: 
			result = q
			break
	return result	

if __name__ == "__main__":
	
	s,l = depthFirstSearch(False,u"yystart")	
	print s
