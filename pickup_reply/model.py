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

class Reply(object):
    pass

class Analyze(object):
    pass

metadata = sqlalchemy.MetaData()

status = Table("buffer_20100605",metadata,
                Column('id_autoinc', types.BigInteger(20), primary_key=True),
                Column('id', types.BigInteger(20)),
                Column('user', types.String(20)),
                Column('content', types.Text),
                Column('source', types.Text),
                Column('time', types.DateTime, default=datetime.now),
                #Column('isAnalyze', types.SmallInteger, default=False),
                #Column('isReplyAnalyze',types.SmallInteger, default=0),
                mysql_engine = 'InnoDB',
                mysql_charset = 'utf8'
            )


reply = Table("reply",metadata,
                Column('id', types.Integer, primary_key=True),
                Column('tweet_id', types.BigInteger(20)),
                Column('reply_text', types.Text),
                Column('src_id', types.BigInteger(20)),
                Column('src_text', types.Text),
                Column('is_analyze', types.SmallInteger, default=False),
                mysql_engine = 'InnoDB',
                mysql_charset = 'utf8'
            )


analyze = Table("analyze",metadata,
                Column('buffer_id', types.BigInteger(20), primary_key=True),
                Column('is_reply_analyze', types.SmallInteger, default=False),
                mysql_engine = 'InnoDB',
                mysql_charset = 'utf8'
            )

"""
status_reply = Table("status_reply", metadata,
                    Column('id', types.Integer, primary_key=True),
                    Column('status_id', types.Integer, ForeignKey('twit.id')),
                    Column('reply_id', types.Integer, ForeignKey('twit2.id')),
                    mysql_engine = 'MyISAM',
                    mysql_charset = 'utf8'
                    )
"""
def startSession(conf):
    
    config = {"sqlalchemy.url":
            "mysql://"+conf["dbuser"]+":"+conf["dbpass"]+"@"+conf["dbhost"]+"/"+conf["db"]+"?charset=utf8",
            "sqlalchemy.echo":"False"}
    engine = sqlalchemy.engine_from_config(config)

    dbSession = scoped_session(
                    sessionmaker(
                        autoflush = True,
                        autocommit = False,
                        bind = engine
                    )
                )

    mapper(Status, status)
    mapper(Reply,  reply)
    mapper(Analyze, analyze)
    """mapper(Status, status, properties = {
                'Replys' : relation(Reply, secondary = status_reply),
           })"""
    metadata.create_all(bind=engine)
    print ("--start DB Session--")
    return dbSession
        
"""
# テスト内容
>>> a = startSession()
--start DB Session--
"""    
