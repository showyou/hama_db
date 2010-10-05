#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

import os
import simplejson
from collections import defaultdict
import codecs
import random

session = None
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"
common_path = exec_path+"/common/"
sys.path.insert(0,exec_path)
from common import auth_api, model, mecab

def getAuthData(fileName):
    file = open(fileName,'r')
    a = simplejson.loads(file.read())
    file.close()
    return a


def select_contain_sentences(word):
    #sqlalchemyに与える文字列は(utf-8)
    global session
    #print "word",word
    q = session.query(model.Reply)
    sentences = q.filter( 
        model.Reply.src_text.like('%'+word.encode("utf-8")+'%'))[0:100]
    result = []
    for s in sentences:
        #print s.reply_text
        result.append(s.reply_text)
    return result
    #raise


def pickup_reply_tweet(reply_word, word):
    global session
    # reply_wordを含む文章を返す
    print u"入力基準単語:返信基準単語",
    print word,reply_word
    q = session.query(model.Reply.reply_text).filter( \
        model.Reply.src_text.like('%'+word.encode("utf-8")+'%'))
    sentences =\
    q.filter(model.Reply.reply_text.like('%'+reply_word.encode("utf-8")+'%'))[0]
    #print "sent",
    #print sentences[0]
    return sentences[0]
    #raise


def pickup_top_used_word(word_total, number):
    # word_total: [単語名:数]
    # number: 取り出す数。1なら1個。nならn個
    if len(word_total) == 0: return ""
    sort_item= sorted(word_total.items(), key=lambda x:x[1],reverse=True)[0:number]
    if number > 1:
        l = []
        for si in sort_item:
            l.append(si[0])
        #print "len", len(l),sort_item,number
        result = random.choice(l)
    else: result = sort_item[0][0]
    #print "result",result
    return result
    raise


def sparse_sentence(s):
    #print s
    s_sparse =\
    mecab.sparse_all(s.encode("utf-8"),"/usr/lib/libmecab.so.1").split("\n")[:-2]
    candidate = set()
    for s2 in s_sparse: # この時点で単語レベルのハズ(ただしs2=単語 品詞
                        # とかかなぁ
        #print "s2",
        s3 = s2.decode("utf-8").split("\t")
        s4 = s3[1].split(",")
        #print s3[0],s4[0]
        if s4[0] != u"記号" and s4[0] != u"助動詞" \
            and s4[0] != u"助詞":#数が集まったら名詞のみにしたい
            candidate.add(s3[0])
    return candidate


def calc_word_count(sentences):
    word_total = defaultdict(float)
    for s in sentences:
        #print s
        word_onesentence_set = sparse_sentence(s)

        for w in word_onesentence_set:
            word_total[w] += 1.0
    #for k,w in word_total.iteritems():
    #    print k, w
    cnt = 0.0
    for i in word_total.values():
        cnt += i
    for k in word_total.keys():
        word_total[k] /= cnt
    return word_total
    raise


def pickup_reply_one_word(word):
    sentences = select_contain_sentences( word )
    word_total = calc_word_count(sentences)
    return word_total


"""
    "あつい"と入れると
    1.あつい を含むtweetを列挙
    2.tweetを単語レベルに分解
    3.あつい 以外の単語の出現数を数え上げる(ただし1文につき一回)
"""
def pickup_reply(input_sentence):
    
    word_total = defaultdict(int)
    word_head  = {} #topになったreplyが出る転置インデックス
    words = sparse_sentence(input_sentence)

    if len(words) == 1: words.add("eof")
    for word in words:
        #print "w1",
        #print word
        if word == "eof": continue
    
        tmp_total = pickup_reply_one_word(word)
        for k,v in tmp_total.iteritems():
            word_total[k]+=v
            if word_head.has_key(k) ==  False:
                word_head[k] = set([word])
            else:
                word_head[k].add(word)
    
    
    reply_word = pickup_top_used_word(word_total,5) # 1はTop1だけ取ってくる。
                                       # 2以上ならTop2個とってあとはランダム
    if reply_word == "": return ""
    a = word_head[reply_word]
    #print a
    if len(a) > 1:
        src_word = random.choice(list(a))
    else:
        src_word = list(a)[0]
    #print "a",src_word
    reply_text = pickup_reply_tweet(reply_word, src_word)
    return reply_text


def main(str, newSession=None):
    global session
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    #print "conf_path", conf_path
    user = getAuthData(conf_path)
    if session == None:
        if newSession == None:
            session = model.startSession(user)
        else:
            session = newSession
    api = auth_api.connect(user["consumer_token"], user["consumer_secret"],\
        common_path)
    #api = tweepy_connect.connect()
    return pickup_reply(str)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input = sys.argv[1].decode("utf-8")
    else:
        input = u"帰宅"
    print main(input)
