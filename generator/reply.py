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
			sentence += " "+random.choice((u'おはようございますなのよ',u'おはようなのよ'))
		elif r.text == 'tadaima':
			sentence = "@"+r.user+" "+random.choice((u"おかえりなのよ",u"おかえりなさいなのよ"))
		elif r.text == 'otukare':
			s = random.choice((u'おつかれさまなのよ',u'あともうちょっと、なのよ。',u'私が見守ってるのよ！'))
			sentence = "@"+r.user+" "+s
		elif r.text == 'chucchu':
			s = random.choice((u'にゃ〜',u'にゃん♪'))
			sentence = "@"+r.user+" "+s
		elif r.text == 'at':
			s = random.choice((u'うん、そんなところなのよ。',u'あーあ、今日もかったるいのよ',u'ありがとーなのよ♪',u'そうなのよ。',u'だ、だれもあんたのためにいったわけじゃないのよ！'))
			sentence = "@"+r.user+" "+s
		elif r.text == 'moyashi':
			s = u'だれがもやしなのよ'
			sentence = "@"+r.user+" "+s
		session.delete(r)	
		if sentence != "":
			break
	session.commit()
	return sentence 
