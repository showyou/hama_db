#!/usr/bin/env python
#! -*- coding: utf-8 -*-
# 人工無脳の一日のスケジュールを決める
import random
import datetime

scheduleTable = {
	"morning":7,
	"lanch":12,
	"dinner":18,
	"bath":21,
}

def Generate():
	genSchedule = {};
	genSchedule["morning"] = scheduleTable["morning"] + random.gauss(0,0.5);#+-0.5
	genSchedule["lanch"] = scheduleTable["lanch"] + random.gauss(0,0.5);
	genSchedule["dinner"] = scheduleTable["dinner"] + random.gauss(0,1.5);
	genSchedule["bath"] = scheduleTable["bath"] + random.gauss(0,0.5);

	return genSchedule;

g = Generate()
print g
now = datetime.datetime.today() 
print now.hour
min = 0 
max = 0 
for sc in g.keys():
	if now.hour > g[sc] and max < g[sc]:
		print sc,g[sc]
		label = sc
		max = g[sc] 
print label
