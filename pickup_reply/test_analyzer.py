# -*- coding:utf-8 -*-
import nose
import analyzer as al
from nose.tools import ok_, eq_
import sys
import codecs

class TestAnalyzer():
    def test_select_contain_sentences(self):
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        al.main()# later, move to setUp
        s, q= al.select_contain_sentences("おはよう")
        print s
        ok_(s)
        raise

    def init_data(self):
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        self.tmp_sentences = [
        u"あぅあぅ、ご主人様おはようございますなのですよ",
        u"おはようです",
        u"あ、おはよう　ぴよんさん",
        u"おはよう、うつく！",
        u"おはようございまーす、ばんしぃさん！",
        u"おはようございました！",
        u"おはよう。朝のキミは、特に綺麗だ。"]

    def test_calc_word_count(self):
        self.init_data()
        word_cnt = al.calc_word_count(self.tmp_sentences)
        ok_(word_cnt)

    def test_pickup_reply_tweet(self):
        self.init_data()
        ok_(al.pickup_reply_tweet(reply_word, self.tmp_sentences))


    def test_pickup_top_used_word(self):
        self.init_data()
        tmp_word_total = { u"おはよう": 3, u"こんにちわ": 2, u"こんばんわ":4 }
        a = al.pickup_top_used_word(tmp_word_total, 1)
        print a
        eq_(a, u"こんばんわ")
        eq_(al.pickup_top_used_word(tmp_word_total, 2), u"こんばんわ")


    def test_pickup_reply(self):
        sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
        al.main()
        ok_(al.pickup_reply(u"おはようございます"))


if __name__ == "__main__":
    print "1"
    nose.main( True)
