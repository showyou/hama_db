#!/usr/bin/env python
# -*- coding: utf-8 -*-

# マルコフテーブル等定義
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy import MetaData
from sqlalchemy import Column, MetaData, Table, types
from datetime import datetime

class Markov(object):
	pass

class Twit(object):
	pass

init = False
metadata = sqlalchemy.MetaData()
markovOneColumn = Table("markov",metadata,
					Column('id', types.Integer, primary_key=True),
					Column('now', types.Unicode(32)),
					Column('next', types.Unicode(32)),
					Column('count', types.Integer),
					mysql_engine = 'MyISAM',
					mysql_charset= 'utf8'
					)

twit = Table("twit",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('text', types.Unicode(140)),
				Column('datetime', types.DateTime, default=datetime.now),
				Column('replyID', types.String(64), default=-1),
				Column('isAnalyze', types.SmallInteger, default=False),
				Column('isReplyAnalyze',types.SmallInteger, default=0),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
			)


twit2 = Table("twit2",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('text', types.Unicode(140)),
				Column('in_reply_to', types.Unicode(64)),
				Column('datetime', types.DateTime, default=datetime.now),
				Column('isAnalyze', types.SmallInteger, default=False),
				mysql_engine = 'MyISAM',
				mysql_charset = 'utf8'
			)

def startSession(conf):
	global init
	config = {"sqlalchemy.url":
			"mysql://"+conf["dbuser"]+":"+conf["dbpass"]+"@"+conf["dbhost"]+"/"+conf["db"]}

	engine = sqlalchemy.engine_from_config(config)

	dbSession = scoped_session(
					sessionmaker(
						autoflush = True,
						transactional = True,
						bind = engine
					)
				)
	if init == False:
		mapper(Markov, markovOneColumn)
		mapper(Twit, twit)
		init = True
	metadata.create_all(bind=engine)
	print ("--start DB Session--")
	return dbSession
		
"""
# テスト内容
>>> a = startSession()
--start DB Session--
"""	
