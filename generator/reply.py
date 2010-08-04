# -*- coding:utf-8 -*-
import random

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
            sentence = "@"+r.user+" "+random.choice((u" おかえり～",u" おかえりなさい"))
        elif r.text == 'otukare':
            s = random.choice((u'おつかれさまです',u'あともうちょっとです',u'私が見守ってます！',u'大丈夫?',u'大丈夫,きっとなんとかなります！',u'なでなで〜'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'chucchu':
            s = random.choice((u'ちゅっちゅー<3',u'にゃ〜',u'にゃん♪',u'うふふー'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'at':
            s = \
            random.choice((u'あほか',u'ないわー',u'うんうん',u'ちゅっちゅー<3',u'なあにー？', u'ずこー'))
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
        elif r.text == 'gohan':
            sentence = ".@"+r.user
            l2num = 1
            while l2num < reply.count():
                l2 = reply[l2num]
                if l2.text == "gohan":
                    sentence += " @"+l2.user
                    session.delete(l2)
                else:
                    l2num += 1
                if len(sentence) > 100: break
            s = random.choice((u'ありがとー、おいしー',u'いっただっきまーす',
                            u'ありがと、でも今はいいやー'))
            sentence += " "+s
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
