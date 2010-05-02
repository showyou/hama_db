#!/usr/bin/env python
# -*- coding: utf-8 -*-

# マルコフテーブル等定義
import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy import MetaData
from sqlalchemy import Column, MetaData, Table, types
from datetime import datetime

class Status(object):
	pass

class Collocation(object):
	pass

metadata = sqlalchemy.MetaData()

status = Table("tweet",metadata,
				Column('id', types.Integer, primary_key=True),
				Column('user', types.Unicode(32)),
				Column('text', types.Unicode(140)),
				Column('datetime', types.DateTime, default=datetime.now),
				Column('replyID', types.String(64), default=-1),
				Column('isAnalyze', types.SmallInteger, default=False),
				Column('isReplyAnalyze',types.SmallInteger, default=0),
                Column('tweetID', types.Integer),
				mysql_engine = 'InnoDB',
				mysql_charset = 'utf8'
			)

collocation = Table("collocation",metadata,
                 Column('id', types.Integer, primary_key=True),
                 Column('a',  types.Unicode(32)),
                 Column('b',  types.Unicode(32)),
                 Column('colloc_count', types.Integer,default=1),
                 Column('sentence_count',types.Integer,default=1),
                 mysql_engine = 'InnoDB',
                 mysql_charset = 'utf8'
            )

def startSession(conf):
	
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

	mapper(Status, status)
	mapper(Collocation,  collocation)
	metadata.create_all(bind=engine)
	print ("--start DB Session--")
	return dbSession
		
"""
# テスト内容
>>> a = startSession()
--start DB Session--
"""	
