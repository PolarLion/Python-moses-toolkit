#!/usr/bin/env python
# -*- coding: utf-8 -*-  

import os

class CfgInfo :
	mosesdecoder_path = "/opt/translation/moses/"
	irstlm_path = "/opt/translation/irstlm/"
	giza_path = "/opt/translation/mgizapp/"

	training_corpus_path = "/home/share/data/BOLT_Phase/Tokenized/Train/"
	test_corpus_path = "/home/share/data/BOLT_Phase/Tokenized/Test/"
	nplm_path = "/opt/translation/nplm/"
	devfilename = "CHT.Dev"
	filename = "CHT.Train"
	testfilename = "CHT.Test"
	target_id = "en"
	source_id = "zh"
	workspace = "/home/xwshi/easymoses_workspace/"
	threads = "32"
	sentence_length = "80"