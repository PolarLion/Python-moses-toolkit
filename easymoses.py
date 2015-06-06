import sys
import os
import re
import time
import ConfigInfo


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


cfg_info = CfgInfo()

easy_experiment_id = 1
easy_corpus = ""
easy_truecaser = ""
easy_logs = "" 
easy_lm = ""
easy_working = ""
easy_train = ""
easy_tuning = ""
easy_evaluation = ""
easy_blm = ""

def read_state (cfg_info) :
	global easy_experiment_id
	if os.path.isfile (cfg_info.workspace + ".easystate") :
		infile = open (cfg_info.workspace + ".easystate", 'r')
		for line in infile :
			if  re.match (r'last-num( *)=( *)".*"', line) :
				# print "******************************  ", line.split('\"')[1]
				easy_experiment_id = int (line.split('\"')[1])
				print easy_experiment_id
	else :
		outfile = open (cfg_info.workspace + ".easystate", 'w')
		easy_experiment_id = 0
		outfile.write ("last-num=\"" + str (easy_experiment_id) + "\"")
		outfile.close ()

	outfile = open (cfg_info.workspace + ".easystate", 'w')
	outfile.write ("last-num=\"" + str (easy_experiment_id + 1) + "\"")
	outfile.close ()

######################### preparation #####################
def preparation (cfg_info) :
	global easy_corpus
	global easy_truecaser
	global easy_logs
	global easy_lm
	global easy_working
	global easy_train
	global easy_tuning
	global easy_evaluation
	global easy_blm
	# read_state (cfg_info)

	print "experiment id: ", easy_experiment_id
	easy_corpus = cfg_info.workspace + "corpus/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_corpus) : os.system ("mkdir " + easy_corpus)
	easy_truecaser = cfg_info.workspace + "truecaser/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_truecaser) : os.system ("mkdir " + easy_truecaser)
	easy_logs = cfg_info.workspace + "logs/" 
	if not os.path.exists (easy_logs) : os.system ("mkdir " + easy_logs)
	easy_lm = cfg_info.workspace + "lm/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_lm) : os.system ("mkdir " + easy_lm)
	easy_working = cfg_info.workspace + "working/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_working) : os.system ("mkdir " + easy_working)
	easy_train = cfg_info.workspace + "train/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_train) : os.system ("mkdir " + easy_train)
	easy_tuning = cfg_info.workspace + "tuning/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_tuning) : os.system ("mkdir " + easy_tuning)
	easy_evaluation = cfg_info.workspace + "evaluation/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_evaluation) : os.system ("mkdir " + easy_evaluation)
	easy_blm = cfg_info.workspace + "blm/" + str (easy_experiment_id) + "/"
	if not os.path.exists (easy_blm) : os.system ("mkdir " + easy_blm)

	outfile = open (easy_logs + str (easy_experiment_id) + ".log", 'w')
	outfile.write (str (time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time())) ))
	outfile.close ()


######################### corpus preparation  ###########################
def tokenisation (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.source_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.training_corpus_path + cfg_info.filename + "." + cfg_info.source_id + " > "
		+ " " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.source_id
		+ " -no-escape ")

	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.target_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.training_corpus_path + cfg_info.filename + "." + cfg_info.target_id + " > "
		+ " " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.target_id)

def truecaser (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/train-truecaser.perl --model " 
 		+ " " + easy_truecaser + "truecase-model." + cfg_info.source_id + " --corpus " 
		+ " " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.source_id)		

	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/train-truecaser.perl --model " 
 		+ " " + easy_truecaser + "truecase-model." + cfg_info.target_id + " --corpus " 
		+ " " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.target_id)		

def truecasing (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
		+ " " + easy_truecaser + "truecase-model." + cfg_info.source_id 
		+ " < " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.source_id 
		+ " > " + easy_corpus + cfg_info.filename + ".true." + cfg_info.source_id)

	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
		+ " " + easy_truecaser + "truecase-model." + cfg_info.target_id 
		+ " < " + easy_corpus + cfg_info.filename + ".tok." + cfg_info.target_id 
		+ " > " + easy_corpus + cfg_info.filename + ".true." + cfg_info.target_id)

def limiting_sentence_length (cfg_info) :
	print "limiting sentence length to sentence length " + cfg_info.sentence_length
	os.system (cfg_info.mosesdecoder_path + "scripts/training/clean-corpus-n.perl " 
		+ " " + easy_corpus + cfg_info.filename + ".true " + cfg_info.source_id + " " + cfg_info.target_id + " " 
		+ " " + easy_corpus + cfg_info.filename + ".clean  1 " + cfg_info.sentence_length)

######################### corpus preparation  ###########################

#########################  language model traning #######################
def generate_sb (cfg_info) :
	print "generate .sb. "
	os.system (cfg_info.irstlm_path + "bin/add-start-end.sh < " \
		+ " " + easy_corpus + cfg_info.filename + ".true." + cfg_info.target_id + " > "\
		+ " " + easy_lm + cfg_info.filename + ".sb." + cfg_info.target_id)

def generate_lm (cfg_info) :
	print "generate lm"
	os.system ("export IRSTLM=" + cfg_info.irstlm_path + "; " + cfg_info.irstlm_path + "bin/build-lm.sh " \
		+ " -i " + easy_lm + cfg_info.filename + ".sb." + cfg_info.target_id + " -t ./tmp -p -s " \
		+ " improved-kneser-ney -o " + easy_lm + cfg_info.filename + ".lm." + cfg_info.target_id)

def generate_arpa (cfg_info) :
	print "generate arpa"
	os.system (cfg_info.irstlm_path + "bin/compile-lm --text=yes " \
		+ " " + easy_lm + cfg_info.filename + ".lm." + cfg_info.target_id + ".gz " \
		+ " " + easy_lm + cfg_info.filename + ".arpa." + cfg_info.target_id)

def generate_blm (cfg_info) :
	print "generate blm"
	os.system (cfg_info.mosesdecoder_path + "bin/build_binary " \
		+ " " + easy_lm + cfg_info.filename + ".arpa." + cfg_info.target_id + " " \
		+ " " + easy_lm + cfg_info.filename + ".blm." + cfg_info.target_id)

#########################  language model traning #######################

#########################  training ranslation system ###########################################
def training_translation_system (cfg_info) :
	os.system ("nohup nice " + cfg_info.mosesdecoder_path + "scripts/training/train-model.perl " 
		+ " -mgiza -mgiza-cpus 16 -cores 2 "
		+ " -root-dir " + easy_train 
		+ " -corpus " + " " + easy_corpus + cfg_info.filename + ".clean " 
		+ " -f " + cfg_info.source_id + " -e " + cfg_info.target_id 
		+ " -alignment grow-diag-final-and " 
		+ " -reordering msd-bidirectional-fe -lm 0:3:" + easy_lm + cfg_info.filename + ".blm." + cfg_info.target_id + ":8 " 
		# + " -reordering msd-bidirectional-fe -lm 0:4:" + "" + ":8 " 
		+ " -external-bin-dir " + cfg_info.giza_path + "bin " 
		+ " >& " + easy_working + "training.out &" )
	print "finish training translation system"

def tuning_tokenizer (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.source_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.training_corpus_path + cfg_info.devfilename + "." + cfg_info.source_id + " > " 
		+ " " + easy_tuning + cfg_info.devfilename + ".tok." + cfg_info.source_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.target_id
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.training_corpus_path + cfg_info.devfilename + "." + cfg_info.target_id + " > " 
		+ " " + easy_tuning + cfg_info.devfilename + ".tok." + cfg_info.target_id)

def tuning_truecase (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
		+ " " + easy_truecaser + "truecase-model." + cfg_info.source_id 
		+ " < " + easy_tuning + cfg_info.devfilename + ".tok." + cfg_info.source_id 
		+ " > " + easy_tuning + cfg_info.devfilename + ".true." + cfg_info.source_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
		+ " " + easy_truecaser + "truecase-model." + cfg_info.target_id 
		+ " < " + easy_tuning + cfg_info.devfilename + ".tok." + cfg_info.target_id 
		+ " > " + easy_tuning + cfg_info.devfilename + ".true." + cfg_info.target_id)

def tuning_process (cfg_info) :
	print "tuning process"
	os.system ("nohup nice " + cfg_info.mosesdecoder_path + "scripts/training/mert-moses.pl " 
	 	+ " -threads " + cfg_info.threads
		+ " -working-dir " + easy_tuning 
		+ " " + easy_tuning + cfg_info.devfilename + ".true." + cfg_info.source_id 
		+ " " + easy_tuning + cfg_info.devfilename + ".true." + cfg_info.target_id 
		+ " " + cfg_info.mosesdecoder_path + "bin/moses " + easy_train + "model/moses.ini " 
		+ " --mertdir " + cfg_info.mosesdecoder_path + "bin/ &> " + easy_tuning + "mert.out &")

	#########################  training translation system ###########################################

def corpus_preparation (cfg_info) :
	print "corpus preparation"
	tokenisation (cfg_info)
	truecaser (cfg_info)
	truecasing (cfg_info)
	limiting_sentence_length (cfg_info)
	print "finish corpus preparation"

def tuning (cfg_info) :
	print "tuning"
	tuning_tokenizer (cfg_info)
	tuning_truecase (cfg_info)
	tuning_process (cfg_info)
	print "finish tuning"

def language_model_training (cfg_info) :
	generate_sb (cfg_info)
	generate_lm (cfg_info)
	generate_arpa (cfg_info)
	generate_blm (cfg_info)

######################## nplm ##########################################

# path_to_nplm = "/opt/translation/nplm/"

# input_model = "~/corpora/giga/nplm_cna/model.10"
output_model = "/home/xwshi/corpora/giga/nplm_cna/output_model.nnlm"
train_ngrams = "~/corpora/giga/nplm_cna/train.ngrams"

def averageNullEmbedding (cfg_info) :
	print "averageNullEmbedding"
	os.system (cfg_info.mosesdecoder_path + "scripts/training/bilingual-lm/averageNullEmbedding.py " \
		+ " -p " + path_to_nplm + "python " \
		+ " -i " + input_model \
		+ " -o " + output_model )
		# + " -n 0 " \
		# + " -t " + train_ngrams)
	print "finish averageNullEmbedding"


def nplm (cfg_info) :
	print "nplm"
	averageNullEmbedding (cfg_info)

######################   bnplm #############################################


# output_bplm_model = bplm_working + "train.10k.model.nplm.out"
# input_bplm_model = bplm_working + "train.10k.model.nplm.40"
# train_bplm_ngrams = bplm_working + "cht.train.clean.ngrams"

def extract_training (cfg_info) :
	print "extract training"
	#os.system (cfg_info.mosesdecoder_path + "scripts/training/bilingual-lm/extract_training.py " 
	os.system (cfg_info.mosesdecoder_path + "/scripts/training/bilingual-lm/extract_training.py "
		+ " --working-dir " + easy_blm
		+ " --corpus " + easy_corpus + cfg_info.filename + ".clean " 
		+ " --source-language " + cfg_info.source_id  #+ cfg_info.training_path + "../" + cfg_info.filename + ".true." + cfg_info.source_id \
		+ " --target-language " + cfg_info.target_id # + cfg_info.training_path + "../" + cfg_info.filename + ".true." + cfg_info.target_id \
		+ " --align " + easy_train + "/model/aligned.grow-diag-final-and " \
		+ " --prune-target-vocab 20000 " 
		+ " --prune-source-vocab 20000 " 
		+ " --target-context 3 " 
		+ " --source-context 2 ")
	print "finish extract training"

def train_nplm (cfg_info) : 
	print "train nplm"
	#os.system (cfg_info.mosesdecoder_path + "scripts/training/bilingual-lm/train_nplm.py " \
	os.system ( cfg_info.mosesdecoder_path + "/scripts/training/bilingual-lm/train_nplm.py "
 		+ " --working-dir " + easy_blm 
		+ " --corpus " + easy_corpus + cfg_info.filename + ".clean " 
		+ " --nplm-home " + cfg_info.nplm_path 
		+ " --ngram-size 8 " 
		+ " --epochs 40 " 
		+ " --learning-rate 1 "
		# + " --input_vocab_size 20000 " 
		# + " --output_vocab_size 20000 " 
		+ " --hidden 512 "
		+ " --input-embedding 150 "
		+ " --output-embedding 150 " 
		+ " --threads " + cfg_info.threads
		+ " & ")
	print "finish train nplm"

def averagebNullEmbedding (cfg_info) :
	print "averagebplmNullEmbedding"
	os.system (cfg_info.mosesdecoder_path + "scripts/training/bilingual-lm/averageNullEmbedding.py " 
		+ " -p " + path_to_nplm + "python " 
		+ " -i " + input_bplm_model 
		+ " -o " + output_bplm_model 
		+ " -t " + train_bplm_ngrams)
	print "finish averagebplmNullEmbedding"

def bnplm (cfg_info) :
	extract_training (cfg_info)
	train_nplm (cfg_info)
	# averagebNullEmbedding (cfg_info)


####################### testing #############################################
def t_start (cfg_info) :
	os.system (cfg_info.mosesdecoder_path + "bin/moses -f " 
		+ cfg_info.working_path + "moses.ini")
	os.system ("mkdir " + cfg_info.working_path + "binarised-model ")
	os.system (cfg_info.mosesdecoder_path + "bin/processPhraseTableMin " 
		+ " -in " + cfg_info.working_path + "train/model/phrase-table.gz -nscores 4 " 
		+ " -out " + cfg_info.working_path + "binarised-model/phrase-table " )
	os.system (cfg_info.mosesdecoder_path + "bin/processLexicalTableMin " 
		+ " -in " + cfg_info.working_path + "train/model/reordering-table.wbe-msd-bidirectional-fe.gz " 
		+ " -out " + cfg_info.working_path + "binarised-model/reordering-table")

def t_tokenisation (cfg_info) :
	print "tokenisation"
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.source_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.test_corpus_path + cfg_info.testfilename + "." + cfg_info.source_id 
		+ " > " + easy_evaluation + cfg_info.testfilename + ".tok." + cfg_info.source_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/tokenizer/tokenizer.perl -l " + cfg_info.target_id 
		+ " -threads " + cfg_info.threads
		+ " -no-escape 1 "
		+ " < " + cfg_info.test_corpus_path + cfg_info.testfilename + "." + cfg_info.target_id 
		+ " > " + easy_evaluation + cfg_info.testfilename + ".tok." + cfg_info.target_id)
	
def t_truecasing (cfg_info) :
	print "truecasing" 
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
	 	+ " " + easy_truecaser + "truecase-model." + cfg_info.source_id 
		+ " < " + easy_evaluation + cfg_info.testfilename  + ".tok." + cfg_info.source_id 
		+ " > " + easy_evaluation + cfg_info.testfilename  + ".true." + cfg_info.source_id)
	os.system (cfg_info.mosesdecoder_path + "scripts/recaser/truecase.perl --model " 
	 	+ " " + easy_truecaser + "truecase-model." + cfg_info.target_id 
		+ " < " + easy_evaluation + cfg_info.testfilename  + ".tok." + cfg_info.target_id 
		+ " > " + easy_evaluation + cfg_info.testfilename  + ".true." + cfg_info.target_id)
 
def t_filter_model_given_input (cfg_info) :
	print "filter model given input"
	os.system (cfg_info.mosesdecoder_path + "scripts/training/filter-model-given-input.pl " \
			+ easy_evaluation + "filtered-" + cfg_info.testfilename +  " " + cfg_info.working_path + "moses.ini " \
		+ test_corpus_path + test_filename + ".true." + cfg_info.source_id \
		+ " -Binarizer " + cfg_info.mosesdecoder_path + "bin/processPhraseTableMin" )
	print "finish filter model given input"

def run_test (cfg_info) :
	print "start run moses"
	os.system ( "nohup nice " + cfg_info.mosesdecoder_path + "bin/moses "
		+ " -threads " + cfg_info.threads
		+ " -f " + easy_tuning + "moses.ini " 
		#+ cfg_info.working_path + "filtered-" + test_filename + "/moses.ini " \
		#+ " -i " + cfg_info.working_path + "filtered-" + test_filename + "/input.115575 " \
		+ " < " + easy_evaluation + cfg_info.testfilename + ".true." + cfg_info.source_id 
		+ " > " + easy_evaluation + cfg_info.testfilename + ".translated." + cfg_info.target_id 
		+ " 2> " + easy_evaluation + cfg_info.testfilename + ".out ")
	os.system (cfg_info.mosesdecoder_path + "scripts/generic/multi-bleu.perl " 
		+ " -lc " + easy_evaluation + cfg_info.testfilename + ".true." + cfg_info.target_id 
		+ " < " + easy_evaluation + cfg_info.testfilename + ".translated." + cfg_info.target_id)

def view_result (cfg_info) :
	translation_result = open (easy_evaluation + "translation_result.txt", 'w')
	translated = open (easy_evaluation + cfg_info.testfilename + ".translated." + cfg_info.target_id, 'r')
	source = open (easy_evaluation + cfg_info.testfilename + ".true." + cfg_info.source_id, 'r')
	target = open (easy_evaluation + cfg_info.testfilename + ".true." + cfg_info.target_id, 'r')
	count = 0
	for tran_line in translated :
		source_line = source.readline ()
		if source_line : translation_result.write ("[#" + str(count) + "] " + source_line)
		else : 
			print "eeeeeeeeeerror  " + str (count)
			break
		translation_result.write ("[" + str(count) + "] " + tran_line)
		target_line = target.readline ()
		if target_line : translation_result.write ("[ref] " + target_line) 
		else :
			print "errrrrrrrrrrror" + str (count)
			break
		count += 1


def testing (cfg_info) :
	print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	#t_start (cfg_info)
	print "******************************************************************"
	# t_tokenisation (cfg_info)
	# t_truecasing (cfg_info)
	#t_filter_model_given_input (cfg_info)
	# run_test (cfg_info)
	view_result (cfg_info)

#########################  test  ###########################


def easymoses ():
	# cfg_info = ConfigInfo.ConfigInfo("moses.conf")
	preparation (cfg_info)
	# corpus_preparation (cfg_info)
	# language_model_training (cfg_info)
	# training_translation_system (cfg_info)
	# tuning (cfg_info)
	testing (cfg_info)
	#nplm (cfg_info)
	
	# bnplm (cfg_info)
	# tuning_process (cfg_info)



if __name__ == "__main__" :
	easymoses ()
	print str (time.strftime('%Y-%m-%d-%X',time.localtime(time.time())))