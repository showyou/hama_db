#!/usr/bin/env python
# coding:utf-8
import nose
from nose import tools as nt
import reply
import readReplyTableFile

class TestArrayUsers():
    def setUp(self):
        data = [1,2,3,4,5]
        self.users = reply.ArrayUsers(data)
    
    def tearDown(self):
        pass

    @nt.with_setup(setUp, tearDown)
    def test_delete(self):
        self.users.delete(1)
        nt.eq_(self.users.data, [2,3,4,5])

    @nt.with_setup(setUp, tearDown)
    def test_ohayou(self):
        table = readReplyTableFile.read("../common/replyTable.json")
        sentence = reply.do_reply("text", table, 
            [{"user":"B", "text":"ohayou"},
             {"user":"C", "text":"tadaima"},
             {"user":"D", "text":"moyashi"}])
        print sentence

if __name__ == "__main__":
    nose.main()
