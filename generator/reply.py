# -*- coding:utf-8 -*-
import random
import os
import sys
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"
common_path = exec_path+"/common/"
sys.path.insert(0,exec_path)

from pickup_reply import analyzer

# 下二つのInterface
class BaseUsers():
    def delete(self, item):
        pass
    
    def __getitem__(i):
        pass

    def count():
        pass


# SQLAlchemy管理のユーザ
class AlchemyUsers(BaseUsers):
    def __init__(self, data, session):
        self.session = session
        self.data = data

    def delete(self, item):
        self.session.delete(item)
        #print item

    # a[hoge]なやつ
    def __getitem__(self,i):
        return self.data[i]

    def count(self):
        return self.data.count()


# 配列管理のユーザ
class ArrayUsers(BaseUsers):
    class TmpUser():
        def __init__(self, user, text):
            self.user = user
            self.text = text
        
    def __init__(self, tmpdata):
        self.data = []
        for td in tmpdata:
            self.data.append( ArrayUsers.TmpUser(td["user"], td["text"]) )
    
    # 値を持つ要素を削除じゃないの？
    def delete(self, item):
        self.data.remove(item)

    # a[hoge]なやつ
    def __getitem__(self, i):
        return self.data[i]

    def count(self):
        return len(self.data)


# data = ArrayUsers or AlchemyUsers
def pickup_same_reply(type, data, reply_id):
    sentence = ""
    l2num = 1
    print "count:", data.count()
    while l2num < data.count():
        l2 = data[l2num]
        if l2.text == type:
            sentence += "@"+l2.user + " "
            data.delete(l2)
            reply_id = -1
        else:
            l2num += 1
        if len(sentence) > 100: break
    return sentence, reply_id


def do_reply(table, replies, session):
    r = replies[0]
    sentence = "@" + r.user + " "
    sentence2 = ""
    type = r.text

    reply_id = r.reply_id
    if type.startswith(u"at"):
        if len(type) > 2:
            sentence2 = analyzer.main(type[2:], session)
        type = "at"

    print "reply:",type,
    if len(sentence2) > 0:
        sentence += sentence2
    else:

        tmp_sentence = ""
        if table[type][0]:
            tmp_sentence, reply_id = pickup_same_reply(type, replies, reply_id)
        sentence += tmp_sentence + random.choice(table[type][4])
    replies.delete(r)
    return sentence, reply_id


# do からdo_replyへの移行
# reply->data session->sessionでAlchemyArray作る
# tableはどうする？予め読み込む
def do(table, reply, session):
    replies = AlchemyUsers(reply, session)
    sentence,reply_id = do_reply(table, replies, session)
    session.commit()
    return sentence,reply_id

