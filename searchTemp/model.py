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

metadata = sqlalchemy.MetaData()

markovOneColumn = Table("markovVsearchTemp",metadata,
					Column('id', types.Integer, primary_key=True),
					Column('now', types.Unicode(32)),
					Column('next', types.Unicode(32)),
					Column('count', types.Integer,default=1),
					mysql_engine = 'MyISAM',
					mysql_charset= 'utf8'
					)

def startSession(conf):

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

	mapper(Markov,markovOneColumn)
	metadata.create_all(bind=engine)
	print ("--start DB Session--")
	return dbSession
		
"""
# テスト内容
a = startSession()
>>> --start DB Session--
"""	
