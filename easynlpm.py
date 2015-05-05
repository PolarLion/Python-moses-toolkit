import os
import sys
import re



class CfgInfo :
	nplm = "/opt/translation/nplm/"
	corpus_path = "~/corpora/nplmt/training/"
	filename = "cht.train.zh-cn.txt"
	ngram_size = "5"
	vocab_size = "50000"
	validation_size = "500"
	num_epochs = "10"
	num_hidden = "0"
	input_embedding_dimension = "150"
	output_embedding_dimension = "750"
	num_threads = "32"



cfg = CfgInfo ()

######################### Training NPLM #############################

def prepare_neural_language_model (cfg_info) :
	os.system (cfg_info.nplm + "bin/prepareNeuralLM --train_text " + cfg_info.corpus_path + cfg_info.filename + " " \
		+ " --ngram_size " + cfg_info.ngram_size + " " + "--vocab_size " + cfg_info.vocab_size + \
		+ " --write_words_file " + cfg_info.corpus_path + "../words " \
		+ " --train_file " + cfg_info.corpus_path + "../train.ngrams " \
		+ " --validation_size " + cfg_info.validation_size \
		+ " --validation_file " + cfg_info.corpus_path + "../validation.ngrams " \
		+ " >& " +cfg_info.corpus_path + "../prepareout.out &")

def train_neural_network (cfg_info) :
	os.system (cfg_info.nplm + "bin/trainNeuralNetwork " \
		+ " --train_file " + cfg_info.corpus_path + "../train.ngrams " \
		+ " --validation_file " + cfg_info.corpus_path + "../validation.ngrams " \
		+ " --num_epochs " + cfg_info.num_epochs \
		+ " --input_words_file " + cfg_info.corpus_path + "../words " \
		+ " --model_prefix " + cfg_info.corpus_path + "../model " \
		+ " --input_embedding_dimension " + cfg_info.input_embedding_dimension \
		+ " --num_hidden " + cfg_info.num_hidden \
		+ " --output_embedding_dimension " + cfg_info.output_embedding_dimension \
 		+ " --num_threads "+ cfg_info.num_threads \
		+ " >& " +cfg_info.corpus_path + "../nplmtrain.out &" )




#prepare_neural_language_model (cfg)
train_neural_network (cfg)
