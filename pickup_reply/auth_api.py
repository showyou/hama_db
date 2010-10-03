#!/usr/bin/env python
# -*- coding:utf-8 -*-
import simplejson
import tweepy
import sys
import locale
import datetime

locale.setlocale(locale.LC_CTYPE, "")
def loadJSON(filename):
    f = open(filename)
    result = simplejson.loads(f.read())
    f.close()
    return result

def init_config(consumer_token, consumer_secret,exec_path):

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)

    try:
        redirect_url = auth.get_authorization_url()
        print redirect_url
    except tweepy.TweepError:
        print 'Error! Failed to get request token.'
        sys.exit()

    verifier = raw_input('Verifier:').strip()

    auth.get_access_token(verifier)
    access_token = auth.access_token
    user = {}
    user["key"] = key = access_token.key
    user["secret"] = secret = access_token.secret
    user["credential"] = dict(user = tweepy.API(auth).me().screen_name)

    f = open(exec_path + "/user.json", "w")
    simplejson.dump( user, f )
    f.close()
    return user

def connect(consumer_token, consumer_secret, exec_path = "."):
    try:
        user = loadJSON(exec_path+"/user.json")
    except IOError:
        user = init_config(consumer_token, consumer_secret, exec_path)

    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(user["key"], user["secret"])

    api = tweepy.API(auth)
    return api

if __name__ == "__main__":
    conf = loadJSON("config.json")
    api = connect(conf["consumer_token"], conf["consumer_secret"])
    print api.get_status(9999689822).text
