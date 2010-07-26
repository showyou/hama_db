#! -*- coding:utf-8 -*-
import nose
import nose.tools as t
import quickAnalyzer as qa

def testRegKitaku():
    """ 帰宅がちゃんとヒットするか確認 """
    def isKitaku(str):
        if qa.regTadaima.search(str):
            return True
        else: return False
    
    t.eq_(isKitaku(u"帰宅した"), True)
    t.eq_(isKitaku(u"帰宅中"), True)


    t.eq_(isKitaku(u"帰宅したら"), True)
    t.eq_(isKitaku(u"帰宅しても"), False)



if __name__ == "__main__":
    nose.main()


