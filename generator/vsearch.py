#!/usr/bin/env python
#! -*- coding:utf-8 -*-

#sqlalchemyで深さ優先探索
import model
import simplejson
from sqlalchemy import and_
from shuffleByCount import shuffleByCount
import pytc
import pickle
import sys

g_depthMax = 30 # 最大探索深さ(=単語数)
exec_path = "/home/yuki/public_git/hama_db/"
conf_path = exec_path+"./common/config.json"
common_path = exec_path+"./common/"

def getAuthData(fileName):
    file = open(fileName,'r')
    a = simplejson.loads(file.read())
    file.close()
    return a


def dfs2(db, index_db, prevWord, startWord, endWord, depthMax):
    node = {"text":startWord,"prev":prevWord, "visit":False}
    print node
    stack =[] 
    depth = 1 # 探索深さ
    
    if node["text"] == endWord:
        return [ node["text"] ]
    elif 2 >= depthMax:
        return []
    else:
        depth += 1
        query = pickle.dumps((node["prev"], node["text"]))
        print query
        f = pickle.loads(index_db[query])
        print "a"
        #逆にとって、最後にreverseするやり方はダメな気がする
        #f = q.filter(and_(type1==node["text"],type2==node["prev"]))
        tmpList = []
        for fq in f:
            #if reverse:
            #    tmpList.append({"name":fq.now,"count":fq.count})
            #else:

            query = pickle.dumps((node["prev"], node["text"], fq))
            try:
                count = db.addint(query, 0) + INT_MAX
                print "count",count
                tmpList.append({"name":fq,"count":count})
            except:
                print "Unexpected error:", sys.exc_info()
                print node["prev"], node["text"], "fq",fq,
        shuffleList = shuffleByCount(tmpList)
        for i in shuffleList:
            print "i", i["name"]
            resultList = dfs2(db, index_db, node["text"], i["name"], endWord,
                            depthMax-1 )
            if resultList != []:
                resultList.insert(0, node["text"])
                return resultList
        else: return []


def depthFirstSearch2( startWord, endWord, depthMax, reverse=False):
    #print ("ans")
    sentence = ""
    selectwordList = []
    
    # 探索用DBを開く
    data_db = pytc.BDB(common_path + "markov.bdb", 
        pytc.BDBOREADER)
    index_db = pytc.BDB(common_path + "invertIndex.bdb",
        pytc.BDBOREADER)
    for k, v in index_db.iteritems():
        if pickle.loads(k)[1] == 'yystart' :print k
     
    print "start dfs"
    if reverse:
        pass
        #stack = dfs2(db, "", startWord, endWord, depthMax)
    else:
        stack = dfs2(data_db, index_db, "", startWord, endWord, depthMax)
    
    if reverse : 
        stack.reverse()
        stack.pop()

    for s in stack:
        sentence += s
        selectwordList.append(s)
    return sentence,selectwordList

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
			if node["visit"] == True: 
				stack.pop()
				depth -= 1
			elif depth >= depthMax:
				stack.pop()
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
	if reverse : 
		stack.reverse()
		stack.pop()

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
	fs,sl1 = depthFirstSearch(session,"yystart","yyend",g_depthMax,False)
	bs,sl2 = depthFirstSearch(session,"yyend",  "yystart",g_depthMax,True)	
	print fs
	print bs
