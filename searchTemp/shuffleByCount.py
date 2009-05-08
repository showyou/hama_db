#!/usr/bin/env python
#! -*- coding:utf-8 -*-
#test
def shuffleByCount(list):
	""" 
	入力されたリストをアイテムの個数に応じて適当に並べ変えます
	リストからランダム選択->キューに入れる->元リストに入れるの繰り返し
	>>> shuffleByCount(list)
	ng	
	"""
	
	tmpList = []
	# まず元リストを作る
	for item in list:
		tmpList.append(item)

	result = []
	# 次にリストの中身が空になるまで、GetQueryByCountを実行する
	while tmpList:
		i = GetQueryByCount(tmpList)
		result.append(i)
		tmpList.remove(i)

	print("ok")
	return result

# 数量に応じて結果を返す
# ex: [a:5, b:3, c:2] なら aが5割、bが3割、cが2割の確率
def GetQueryByCount(filter):
	import random
	total = 0
	for q in filter:
		total += q['count']

	t = random.randint(1,total)
	total2 = 0
	for q in filter:
		total2 += q['count']
		if t <= total2: 
			result = q
			break
	# ここまででresultにはなにか入ってるはず 
	return result

def _test():
	import doctest

	ha = {'name':'a','count':1}
	hb = {'name':'b','count':2}
	hc = {'name':'c','count':3}
	list = [ ha, hb, hc ]
	
	result = shuffleByCount(list)
	for i in result:
		print( i["name"] )
	#doctest.testmod()

if __name__ == "__main__":
	_test()
 
