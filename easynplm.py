import os
import sys
import re
import time



class CfgInfo :
	mosesdecoder_path = "/opt/translation/moses/"
	nplm = "/opt/translation/nplm/"
	corpus_path = "/home/xwshi/easymoses_workspace/corpus/giga/"
	#corpus_path = "~/corpora/nplmt/training/"
	#filename = "cht.train.en"
	nplm_path = corpus_path + "nplm_nyt/"
	#filename = "giga_nyt_eng.txt"
	#cfg_info.nplm_path = corpus_path + "nplm_cna"
	#filename = "giga_cna_eng.txt"
	#cfg_info.nplm_path = corpus_path + "nplm_wpb"
	#filename = "giga_wpb_eng.txt"
	# workspace = "/home/xwshi/easymoses_workspace/"
	source_id = "en"
	threads = "32"
	# nplm_path = corpus_path + "nplm_xin"
	filename = "giga_nyt_eng.txt"
	ngram_size = "5"
	vocab_size = "100000"
	validation_size = "500"
	num_epochs = "20"
	num_hidden = "0"
	input_embedding_dimension = "150"
	output_embedding_dimension = "750"
	num_threads = "32"



cfg = CfgInfo ()

if not os.path.exists (cfg.nplm_path) : os.system ("mkdir " + cfg_info.cfg_info.nplm_path)



######################### Training NPLM #############################
def prepare_corpus (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.source_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.nplm_path + cfg_info.filename + " > "
		+ " " + cfg_info.nplm_path + cfg_info.filename + ".tok." + cfg_info.source_id
		+ " -no-escape ")

	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/train-truecaser.perl --model " 
 		+ " " + cfg_info.nplm_path + "truecase-model." + cfg_info.source_id + " --corpus " 
		+ " " + cfg_info.nplm_path + cfg_info.filename + ".tok." + cfg_info.source_id)		


	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
		+ " " + cfg_info.nplm_path + "truecase-model." + cfg_info.source_id 
		+ " < " + cfg_info.nplm_path + cfg_info.filename + ".tok." + cfg_info.source_id 
		+ " > " + cfg_info.nplm_path + cfg_info.filename + ".true." + cfg_info.source_id)



def prepare_neural_language_model (cfg_info) :
	
	os.system (cfg_info.nplm + "bin/prepareNeuralLM " \
		+ " --train_text " + cfg_info.corpus_path + cfg_info.filename \
		+ " --ngram_size " + cfg_info.ngram_size + " " + "--vocab_size " + cfg_info.vocab_size \
		+ " --write_words_file " + cfg_info.cfg_info.nplm_path + "/words " \
		+ " --train_file " + cfg_info.cfg_info.nplm_path + "/train.ngrams " \
		+ " --validation_size " + cfg_info.validation_size \
		+ " --validation_file " + cfg_info.cfg_info.nplm_path + "/validation.ngrams " \
		+ " >& " + cfg_info.cfg_info.nplm_path + "/prepareout.out &")

def train_neural_network (cfg_info) :
	os.system (cfg_info.nplm + "bin/trainNeuralNetwork " 
		+ " --train_file " + cfg_info.cfg_info.nplm_path + "/train.ngrams " 
		+ " --validation_file " + cfg_info.cfg_info.nplm_path + "/validation.ngrams " 
		+ " --num_epochs " + cfg_info.num_epochs 
		+ " --input_words_file " + cfg_info.cfg_info.nplm_path + "/words " 
		+ " --model_prefix " + cfg_info.cfg_info.nplm_path + "/model " 
		+ " --input_embedding_dimension " + cfg_info.input_embedding_dimension 
		+ " --num_hidden " + cfg_info.num_hidden 
		+ " --output_embedding_dimension " + cfg_info.output_embedding_dimension 
 		+ " --num_threads "+ cfg_info.num_threads 
		+ " >& " +cfg_info.cfg_info.nplm_path + "/nplmtrain.out &" )



prepare_corpus (cfg)
#start = time.clock ()
print "prepare network"
#prepare_neural_language_model (cfg)
print "finish prapare network"
#end = time.clock ()
#print "prepare_neural_language_model used ", (start - end) / 1000000, "s"
#start = time.clock ()
#print "train neural network"
# train_neural_network (cfg)

#end = time.clock ()
#print "train_neural_network used ", (start - end) / 1000000, "s"
