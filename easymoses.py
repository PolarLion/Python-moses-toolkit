import sys
import os
import re
import ConfigInfo

######################### corpus preparation  ###########################

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

def truecasing (cfg_info) :
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

######################### corpus preparation  ###########################



#########################  language model traning #######################
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

#########################  language model traning #######################



#########################  training ranslation system ###########################################

def training_translation_system (cfg_info) :
	print "training translation system"
	os.system ("nohup nice " + cfg_info.mosesdecoder_path + "scripts/training/train-model.perl " \
		+ "-mgiza -mgiza-cpus 16 -cores 2 -root-dir " + cfg_info.working_path + "train -corpus " \
		+ cfg_info.training_path + "../" + cfg_info.filename + ".clean " \
		+ "-f " + cfg_info.source_id + " -e " + cfg_info.target_id + " -alignment grow-diag-final-and " \
		+ "-reordering msd-bidirectional-fe -lm 0:3:" + cfg_info.lm_path + cfg_info.filename + ".blm." \
		+ cfg_info.target_id + ":8 " \
		+ "-external-bin-dir " + cfg_info.giza_path + "bin " \
		+ " >& " + cfg_info.working_path + "training.out &" )
	print "finish training translation system"

def tuning_tokenizer (cfg_info) :
	print "tuning tokenizer"
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " \
		+ cfg_info.target_id + " < " + cfg_info.tuning_path + cfg_info.tuning_file + "." + cfg_info.target_id + " > " \
		+ cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".tok." + cfg_info.target_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " \
		+ cfg_info.source_id + " < " + cfg_info.tuning_path + cfg_info.tuning_file + "." + cfg_info.source_id + " > " \
		+ cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".tok." + cfg_info.source_id)

def tuning_truecase (cfg_info) :
	print "tuning truecase"
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " \
		+ cfg_info.tuning_path + "../truecase-model." + cfg_info.target_id \
		+ " < " + cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".tok." + cfg_info.target_id \
		+ " > " + cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".true." + cfg_info.target_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " \
		+ cfg_info.tuning_path + "../truecase-model." + cfg_info.source_id \
		+ " < " + cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".tok." + cfg_info.source_id \
		+ " > " + cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".true." + cfg_info.source_id)

def tuning_process (cfg_info) :
	print "tuning process"
	os.system ("nohup nice " + cfg_info.mosesdecoder_path + "scripts/training/mert-moses.pl " \
	  + "-threads 32 " \
		+ "-working-dir " + cfg_info.working_path + " " \
		+ cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".true." + cfg_info.source_id + " " \
		+ cfg_info.tuning_path + "../" + cfg_info.tuning_file + ".true." + cfg_info.target_id + " " \
		+ cfg_info.mosesdecoder_path + "bin/moses " + cfg_info.working_path + "train/model/moses.ini " \
		+ "--mertdir " + cfg_info.mosesdecoder_path + "bin/ &> " + cfg_info.working_path + "mert.out &")

#########################  training ranslation system ###########################################



def corpus_preparation (cfg_info) :
	print "corpus preparation"
	tokenisation (cfg_info)
	truecaser (cfg_info)
	truecasing (cfg_info)
	limiting_sentence_length (cfg_info)
	print "finish corpus preparation"

def tuning (cfg_info) :
	print "tuning"
	#tuning_tokenizer (cfg_info)
	#tuning_truecase (cfg_info)
	tuning_process (cfg_info)
	print "finish tuning"

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
	#language_model_training (cfg_info)
	#training_translation_system (cfg_info)
	tuning (cfg_info)

