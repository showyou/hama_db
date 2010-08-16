# -*- coding:utf-8 -*-
import random

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

    def count():
        return len(count)


# data = ArrayUsers or AlchemyUsers
def pickup_same_reply(type, data):
    sentence = ""
    l2num = 1
    while l2num < data.count():
        l2 = data[l2num]
        if l2.text == type:
            sentence += " @"+l2.user
            data.delete(l2)
        else:
            l2num += 1
        if len(sentence) > 100: break


# 下の奴を整理する
def do_reply(table, replies):
    sentence = "@" + replies[0].user
    type = replies[0].text
    if table[type][1]:
        sentence = pickup_same_reply(type, other_replies)
    sentence += random.choice(table[type][4])   
    return sentence


# do からdo_replyへの移行
# reply->data session->sessionでAlchemyArray作る
# tableはどうする？予め読み込む
def do2(table, reply, session):
    replies = AlchemyUsers(reply, session)
    return do_reply(table, replies)


# 返事考える
def do(reply,session):
    sentence = ""
    for r in reply:
        if r.text == "ohayou" :
            sentence = "@"+r.user
            l2num = 1
            while l2num < reply.count():
                l2 = reply[l2num]
                if l2.text == "ohayou":
                    sentence += " @"+l2.user
                    session.delete(l2)
                else:
                    l2num += 1
                if len(sentence) > 100: break
            sentence += " "+random.choice((u'おはようございますー',u'おはおはー',u'おっはー',u'おはよー'))
        elif r.text == 'tadaima':
            sentence = "@"+r.user+" "+random.choice((u" おかえり～",\
            u"おかえりなさい", u"おか"))
        elif r.text == 'otukare':
            s = random.choice((u'おつかれさまです',u'あともうちょっとです',u'私が見守ってます！',u'大丈夫?',u'大丈夫,きっとなんとかなります！',u'なでなで〜'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'chucchu':
            s = random.choice((u'ちゅっちゅー<3',u'にゃ〜',u'にゃん♪',u'うふふー'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'at':
            s = \
            random.choice((u'あほか',u'ないわー',u'うんうん',u'ちゅっちゅー<3',u'なあにー？',\
            u'ずこー', u'ええええ＞＜', u'えっ'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'moyashi':
            s = u'だれがもやしですか'
            sentence = "@"+r.user+" "+s
        elif r.text == 'mukyuu':
            s = u'むきゅー'
            sentence = "@"+r.user+" "+s
        elif r.text == 'wanwan':
            s = random.choice((u'うー、わんわん',u'わんわん'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'mayuri':
            sentence = "@"+r.user+u" トゥットゥルー♪"
        elif r.text == 'baribari':
            sentence = ".@"+r.user
            l2num = 1
            while l2num < reply.count():
                l2 = reply[l2num]
                if l2.text == "baribari":
                    sentence += " @"+l2.user
                    session.delete(l2)
                else:
                    l2num += 1
                if len(sentence) > 100: break
            s = random.choice((u'やめてー！',u'やめてー＞＜'))
            sentence += " "+s
        session.delete(r)  
        if sentence != "":
            break
    session.commit()
    return sentence 
