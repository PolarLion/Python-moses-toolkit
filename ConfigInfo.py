#!/usr/bin/python
#ConfigInfo.py

import re


class ConfigInfo :
	filename = ""
	training_path = ""
	tuning_path = ""
	lm_path = ""
	working_path = ""
	source_id = ""
	target_id = ""
	mosesdecoder_path = ""
	irstlm_path = ""
	giza_path = ""
	sentence_length = ""


	def read_config (self, filename) :
		config = open (filename, 'r')
		i = 0
		for line in config :
			if  re.match (r'filename( *)=( *)".*"', line) : 
				print line.split('\"')[1]
				self.filename = line.split('\"')[1]

			elif  re.match (r'training_path( *)=( *)".*"', line) : 
				print line.split('\"')[1]
				self.training_path = line.split('\"')[1]

			elif re.match (r'tuning_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.tuning_path = line.split('\"')[1]

			elif re.match (r'source_id( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.source_id = line.split('\"')[1]

			elif re.match (r'lm_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.lm_path = line.split('\"')[1]

			elif re.match (r'working_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.working_path = line.split('\"')[1]

			elif re.match (r'target_id( *)=( *)".*"', line) :
				print "target_id = ", line.split('\"')[1]
				self.target_id = line.split('\"')[1]

			elif re.match (r'mosesdecoder_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.mosesdecoder_path = line.split('\"')[1]

			elif re.match (r'irstlm_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.irstlm_path = line.split('\"')[1]
			elif re.match (r'giza_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.giza_path = line.split('\"')[1]
			elif re.match (r'sentence_length( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.sentence_length = line.split('\"')[1]
			
		
	def __init__ (self, filename) :
		self.read_config (filename)

