# -*- coding:utf-8 -*-
import analyzer
#from nose.tools import assert_equal

class Test_removeCharacter():
    def testHTTP(self):
        assert self._rc(u"検索サイト http://www.google.com"), u"検索サイト "
 
    def testTag1(self): #[]カット
        assert self._rc(u"検索サイト [mb]") == u"検索サイト "

    def testTag2(self): #**カット
        assert self._rc(u"検索サイト *Tw*") == u"検索サイト "
  
    def testBrowsing(self):
        assert self._rc(u"Browsing:ほげほげ") == u""
        assert self._rc(u"browsing: ふがふが")== u""

    def testRT(self): #RT:カット
        assert self._rc(u"あああああ RT @hoge: abcde") == u"あああああ "

    def testHashtag(self): #カット
        assert self._rc(u"あああああ #test") == u"あああああ "
    
    """ todo: __でメソッドが外部非公開かどうか確認 """
    def _rc(self,input):
        return analyzer.RemoveCharacter(input)

if __name__ == '__main__':
    nose.main()
