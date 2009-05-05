#!/usr/bin/python
# -*- coding: utf-8 -*-
import cPickle as pickle

#pickle
def read(filename):
	file = open(filename,'r')
	data = pickle.load(file)
	file.close()
	return data

def write(filename,data):
	file = open(filename,'w')
	pickle.dump( data,file )
	file.close()
