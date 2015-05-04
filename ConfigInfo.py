#!/usr/bin/python
#ConfigInfo.py

import re


class ConfigInfo :
	training_path = ""
	tuning_path = ""
	lm_path = ""
	working_path = ""
	source_id = ""
	target_id = ""
	mosesdecoder_path = ""
	irstlm_path = ""
	giza_path = ""


	def read_config (self, filename) :
		config = open (filename, 'r')
		i = 0
		for line in config :
			if  re.match (r'training_path( *)=( *)".*"', line) : 
				print line.split('\"')[1]
				self.set_training_path (line.split('\"')[1])
			elif re.match (r'tuning_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_tuning_path(line.split('\"')[1])
			elif re.match (r'source_id( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_source_id(line.split('\"')[1])
			elif re.match (r'lm_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_lm_path(line.split('\"')[1])
			elif re.match (r'working_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_working_path(line.split('\"')[1])
			elif re.match (r'target_id( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_target_id(line.split('\"')[1])
			elif re.match (r'mosesdecoder_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_mosesdecoder_path(line.split('\"')[1])
			elif re.match (r'irstlm_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_irstlm_path(line.split('\"')[1])
			elif re.match (r'giza_path( *)=( *)".*"', line) :
				print line.split('\"')[1]
				self.set_giza_path(line.split('\"')[1])
			i += 1
	
	def set_lm_path (self, s) :
		lm_path = s
	
	def set_working_path (self, s) :
		working_path = s

	def set_training_path (self, s) :
		training_path = s
	
	def set_tuning_path (self, s) :
		tuning_path = s
	
	def set_source_id (self, s) :
		source_id = s
	
	def set_target_id (self, s) :
		target_id = s
	
	def set_mosesdecoder_path (self, s) :
		mosesdecorder_path = s
	
	def set_irstlm_path (self, s) :
		irstlm_path = s

	def set_giza_path (self, s) :
		giza_path = s
		
	def __init__ (self, filename) :
		self.read_config (filename)

