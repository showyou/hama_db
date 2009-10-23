#!/usr/bin/env python
# -*- coding: utf-8 -*-

# マルコフテーブル等定義
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy import MetaData
from sqlalchemy import Column, MetaData, Table, types
from datetime import datetime

class OhayouTime(object):
	pass

class Markov(object):
	pass

class Twit(object):
	pass

class RetQueue(object):
	pass

class Hot(object):
	pass

class Collocation(object):
	pass

init = False
metadata = sqlalchemy.MetaData()

ohayouTime = Table("ohayouTime",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('type', types.Unicode(32)),
				Column('datetime', types.DateTime, default=datetime.now),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
				)
	
markovOneColumn = Table("markov",metadata,
					Column('id', types.Integer, primary_key=True),
					Column('now', types.Unicode(32)),
					Column('next', types.Unicode(32)),
					Column('count', types.Float,default=1),
					mysql_engine = 'MyISAM',
					mysql_charset= 'utf8'
					)

# 応答キュー。順番固定
retQueue = Table("retQueue",metadata,
					Column('id', types.Integer, primary_key=True),
					Column('user', types.Unicode(32)),
					Column('text', types.Unicode(140)),
					mysql_engine = 'MyISAM',
					mysql_charset = 'utf8'
			)

# hotな単語一覧
hot = Table("hot",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('word', types.Unicode(140)),
				Column('datetime',types.DateTime, default=datetime.now),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
			)

twit = Table("twit",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('text', types.Unicode(140)),
				Column('datetime', types.DateTime, default=datetime.now),
				Column('isAnalyze', types.SmallInteger, default=False),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
			)

collocation = Table("collocation",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('a',  types.Unicode(32)),
				Column('b',  types.Unicode(32)),
				Column('colloc_count', types.Integer,default=1),
				Column('sentence_count',types.Integer,default=1),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
			)

def startSession(conf):
	global init
	config = {"sqlalchemy.url":
			"mysql://"+conf["dbuser"]+":"+conf["dbpass"]+"@"+conf["dbhost"]+"/"+conf["db"]+"?charset=utf8","sqlalchemy.echo":"False"}
	engine = sqlalchemy.engine_from_config(config)

	dbSession = scoped_session(
					sessionmaker(
						autoflush = True,
						transactional = True,
						bind = engine
					)
				)

	if init == False:
		mapper(Twit, twit)
		mapper(Hot,  hot)
		mapper(Markov,markovOneColumn)
		mapper(RetQueue, retQueue)
		mapper(OhayouTime, ohayouTime)
		mapper(Collocation, collocation)
		init = True
	metadata.create_all(bind=engine)
	print ("--start DB Session--")
	return dbSession
		
"""
# テスト内容
a = startSession()
>>> --start DB Session--
"""	
