# -*- coding: utf-8 -*-
from ctypes import *

def sparse_all(s,mecabpath):
	# ライブラリの場所を指定
	# ライブラリを ctypes を使って読み込み
	lib = cdll.LoadLibrary(mecabpath)

	# 解析器初期化用の引数を指定（第二引数無しで普通の解析)
	argc = c_int(2)
	argv = (c_char_p * 2)("mecab", "")

	# 解析器のオブジェクトを作る
	tagger = lib.mecab_new(argc, argv)

	""" 指定された文字列を品詞など調べて返す。 """
	s = lib.mecab_sparse_tostr(tagger, s)
	ret = c_char_p(s).value

	# 終わったら、一応、殺しておく 
	lib.mecab_destroy(tagger)
	return ret

"""
テスト内容
sparse_all("本日は晴天なり","/usr/hoge/libmecab.so")
>> 本日 は 晴天 なり
"""
