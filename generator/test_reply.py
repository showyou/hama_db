#!/usr/bin/env python
# coding:utf-8
import nose
from nose import tools as nt
import reply
import readReplyTableFile
import model
import simplejson
import os
exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
conf_path = exec_path+"/common/config.json"

class TestArrayUsers():
    def setUp(self):
        data = [{"user":"A", "text":"ohayou"},
                {"user":"B", "text":"ohayou"},
                {"user":"C", "text":"tadaima"},
                {"user":"D", "text":"moyashi"}]
        self.users = reply.ArrayUsers(data)
    
    def tearDown(self):
        pass

    @nt.with_setup(setUp, tearDown)
    def test_delete(self):
        user = self.users[0]
        self.users.delete(user)
        nt.eq_(self.users.data, [2,3,4,5])

    @nt.with_setup(setUp, tearDown)
    def test_ohayou(self):
        table = readReplyTableFile.read("../common/replyTable.json")
        sentence = reply.do_reply(table, 
            reply.ArrayUsers([{"user":"A", "text":"ohayou"},
             {"user":"B", "text":"ohayou"},
             {"user":"C", "text":"tadaima"},
             {"user":"D", "text":"moyashi"}
             ]
             )
            )
        print sentence


class TestAlchemyUsers():
    def test_query(self):
        u = LoadUserData(conf_path)
        table = readReplyTableFile.read("../common/replyTable.json")
        session = model.startSession(u)
        rep = session.query(model.RetQueue)
        print reply.do2(table, rep, session)
        

def LoadUserData(fileName):
    #ファイルを開いて、データを読み込んで変換する
    #データ形式は(user,password)
    try:
        file = open(fileName,'r')
        a = simplejson.loads(file.read())
        file.close()
    except IOError:
        print "LoadUserData error" 
        sys.exit(1)
    return a


if __name__ == "__main__":
    TestAlchemyUsers().test_query()
    nose.main()
