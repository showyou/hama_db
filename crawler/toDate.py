#! /usr/bin/env python
# -*- coding:utf-8 -*-
import datetime

"""
地域に応じた時差を返す
日本だと+9時間(JST)
GSTなら0かしら？
ニューヨークなら9-14 = -5?
サンフランシスコ 9-17 = -8?
"""
def getLocalTime(timezoneName):
	if timezoneName == "JP":
		return 9
	else:
		return 0

# 自作strptime
"""
strpTable = [ "a":0, "b":0, "d":0, "H":0, "M":0, "S":0, "Y":0 ]
strpWeek = [ "Sun", "Mon", "Thu", "Wen", "Thi", "Fri", "Sut" ]
def mystrptime(str, format, assign):
	import re
	m = re.search(str, format)
	if !m:
		print ("Value error: bad format"+str+":"+format)
	else:
			
		for a in assign:
			if a == "a":
				result
"""				 
# sample %a %b %d %H:%M:%S +0000 %Y 	
def toDate(date,str):
	dates = datetime.datetime.strptime(date,str)
	dt = dates+datetime.timedelta(hours=getLocalTime("JP"))
	
	return dt

