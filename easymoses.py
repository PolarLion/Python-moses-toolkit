import sys
import os
import re
import ConfigInfo


def tokenisation (cfg_info) :
	print "tokenisation"
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.target_id 
			+ " < " + cfg_info.training_path + cfg_info.filename + "." + cfg_info.target_id + " > "
			+ cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.target_id)
	print "finish 1"
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.source_id 
			+ " < " + cfg_info.training_path + cfg_info.filename + "." + cfg_info.source_id + " > "
			+ cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.source_id)
	print "finish 2"


def truecaser (cfg_info) :
	print "truecaser"
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/train-truecaser.perl --model " \
		+ cfg_info.training_path + "../truecase-model." + cfg_info.target_id + " --corpus " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.target_id)		
	print "finish 1"
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/train-truecaser.perl --model " \
		+ cfg_info.training_path + "../truecase-model." + cfg_info.source_id + " --corpus " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.source_id)		
	print "finish 2"

def Truecasing (cfg_info) :
	print "truecasing"
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " \
		+ cfg_info.training_path + "../truecase-model." + cfg_info.target_id \
		+ " < " + cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.target_id \
		+ " > " + cfg_info.training_path + "../" + cfg_info.filename + ".true." + cfg_info.target_id)
	print "finish 1"
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " \
		+ cfg_info.training_path + "../truecase-model." + cfg_info.target_id \
		+ " < " + cfg_info.training_path + "../" + cfg_info.filename + ".tok." + cfg_info.source_id \
		+ " > " + cfg_info.training_path + "../" + cfg_info.filename + ".true." + cfg_info.source_id)
	print "finish 2"

def limiting_sentence_length (cfg_info) :
	print "limiting sentence length to sentence length " + cfg_info.sentence_length
	os.system (cfg_info.mosesdecoder_path + "scripts/training/clean-corpus-n.perl " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".true " + cfg_info.source_id + " " + cfg_info.target_id + " " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".clean  1 " + cfg_info.sentence_length)
	print "finish 1"


#def language_model_training (cfg_info) :
	
def corpus_preparation (cfg_info) :
	#tokenisation (cfg_info)
	#truecaser (cfg_info)
	#truecasing (cfg_info)
	limiting_sentence_length (cfg_info)


def easymoses ():
	cfg_info = ConfigInfo.ConfigInfo("config")
	corpus_preparation (cfg_info)

