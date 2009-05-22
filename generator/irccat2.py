#! /usr/bin/env python
# -*- coding:utf-8 -*-
import irclib
import sys

class IRCCat(irclib.SimpleIRCClient):
    def __init__(self, target,message):
        irclib.SimpleIRCClient.__init__(self)
        self.target = target
        self.message = message
    def on_welcome(self, connection, event):
        if irclib.is_channel(self.target):
            connection.join(self.target)
        else:
            self.send_it()

    def on_join(self, connection, event):
        self.send_it()

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def send_it(self):
        self.connection.privmsg(self.target, self.message.encode("iso-2022-jp",'ignore'))
        self.connection.quit("Using irclib.py")

def main(message):
    server = "irc.media.kyoto-u.ac.jp"
    port = 6667
    nickname = "shIRC"
    target = "#hama" 

    c = IRCCat(target,message)
    try:
        c.connect(server, port, nickname)
    except irclib.ServerConnectionError, x:
        print x
        sys.exit(1)
    c.start()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        message = sys.argv[1]
    else: message = u"てすてす"
    main(message)
