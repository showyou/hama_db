# -*- coding:utf-8 -*-
import random

# 返事考える
def do(reply,session):
    sentence = ""
    for r in reply:
        if r.text == "ohayou" :
            sentence = ".@"+r.user
            l2num = 1 
            while l2num < reply.count():
                l2 = reply[l2num]
                if l2.text == "ohayou":
                    sentence += " @"+l2.user
                    session.delete(l2)
                else:
                    l2num += 1
                if len(sentence) > 100: break
            sentence += " "+random.choice((u'おはようだ！',u'おはようでござる'))
        elif r.text == 'tadaima':
            #sentence = "@"+r.user+" "+random.choice((u" おかえりだ！"))
			s = u"おかえりだ！"
			sentence = "@"+r.user+" "+s
        elif r.text == 'otukare':
            s = random.choice((u'お疲れさまだ！',u'大丈夫、明日は明日の風が吹くぞ'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'chucchu':
            s = random.choice((u'う、恥ずかしいでござる。',u'にゃ〜',u'ごろごろ'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'at':
            s = random.choice((u'ふむふむでござる',u'そういうこともあるのでござろう'))
            sentence = "@"+r.user+" "+s
        elif r.text == 'moyashi':
            s = u'だれがもやしなのだ！'
            sentence = "@"+r.user+" "+s
        else:
            s = u'ぎゃーす！！'
            sentence = "@"+r.user+" "+s
        session.delete(r)   
        if sentence != "":
            break
    session.commit()
    return sentence
