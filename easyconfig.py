#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os

class CfgInfo :
	mosesdecoder_path = "/opt/translation/moses/"
	irstlm_path = "/opt/translation/irstlm/"
	giza_path = "/opt/translation/mgizapp/"

	# training_corpus_path = "/home/share/data/BOLT_Phase/Tokenized/Train/"
	# test_corpus_path = "/home/share/data/BOLT_Phase/Tokenized/Train/"
	# test_corpus_path = "/home/share/data/BOLT_Phase/Tokenized/Test/"
	# training_corpus_path = "/home/xwshi/data/double/"
	# test_corpus_path = "/home/xwshi/data/double/"
	# training_corpus_path = "/home/xwshi/data/CHT/original/"
	# test_corpus_path = "/home/xwshi/data/CHT/original/"
	# training_corpus_path = "/home/xwshi/data/wmt/europarl/"
	# test_corpus_path = "/home/xwshi/data/wmt/europarl/"
	training_corpus_path = "/home/xwshi/data/CHT/notok/"
	test_corpus_path = "/home/xwshi/data/CHT/notok/"
	# nplm_path = "/opt/translation/nplm/"
	devfilename = "CHT.Dev"
	filename = "CHT.Train"
	testfilename = "CHT.Test"
	# testfilename = "CHT.Dev"
	# filename = "europarl-v7.fr-en"
	# target_id = "fr"
	# source_id = "en1"
	source_id = "zh"
	target_id = "en"
	workspace = "/home/xwshi/easymoses_workspace/"
	threads = "32"
	sentence_length = "80"