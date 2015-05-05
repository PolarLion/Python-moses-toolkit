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


	
def corpus_preparation (cfg_info) :
	#tokenisation (cfg_info)
	#truecaser (cfg_info)
	#truecasing (cfg_info)
	limiting_sentence_length (cfg_info)


def generate_sb (cfg_info) :
	print "generate .sb. "
	os.system (cfg_info.irstlm_path + "bin/add-start-end.sh < " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".true." + cfg_info.target_id + " > "\
		+ cfg_info.lm_path + cfg_info.filename + ".sb." + cfg_info.target_id)

def generate_lm (cfg_info) :
	print "generate lm"
	os.system ("export IRSTLM=" + cfg_info.irstlm_path + "; " + cfg_info.irstlm_path + "bin/build-lm.sh " \
		+ "-i " + cfg_info.lm_path + cfg_info.filename + ".sb." + cfg_info.target_id + " -t ./tmp -p -s " \
		+ "improved-kneser-ney -o " + cfg_info.lm_path + cfg_info.filename + ".lm." + cfg_info.target_id)

def generate_arpa (cfg_info) :
	print "generate arpa"
	os.system (cfg_info.irstlm_path + "bin/compile-lm --text=yes " \
		+ cfg_info.lm_path + cfg_info.filename + ".lm." + cfg_info.target_id + ".gz " \
		+ cfg_info.lm_path + cfg_info.filename + ".arpa." + cfg_info.target_id)

def generate_blm (cfg_info) :
	print "generate blm"
	os.system (cfg_info.mosesdecoder_path + "bin/build_binary " \
		+ cfg_info.lm_path + cfg_info.filename + ".arpa." + cfg_info.target_id + " " \
		+ cfg_info.lm_path + cfg_info.filename + ".blm." + cfg_info.target_id)

def language_model_training (cfg_info) :
	print "language model training"
	generate_sb (cfg_info)
	generate_lm (cfg_info) 
	generate_arpa (cfg_info)
	generate_blm (cfg_info) 
	print "finsih language model training"





def easymoses ():
	cfg_info = ConfigInfo.ConfigInfo("config")
	#corpus_preparation (cfg_info)
	language_model_training (cfg_info)

