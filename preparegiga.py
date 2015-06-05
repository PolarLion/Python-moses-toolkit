import os
import sys
import re
import gzip

#giga_path = "/home/share/data/LDC/LDC2011T07/gigaword_eng_5_d2/data/nyt_eng/"
##giga_path = "/home/share/data/LDC/LDC2011T07/gigaword_eng_5_d2/data/cna_eng/"
#giga_path = "/home/share/data/LDC/LDC2011T07/gigaword_eng_5_d2/data/wpb_eng/"
giga_path = "/home/share/data/LDC/LDC2011T07/gigaword_eng_5_d3/data/xin_eng/"
filename = "/home/xwshi/corpora/giga/giga_xin_eng.txt"






if __name__ == "__main__":
	print "preapare giga"
	pattern = re.compile (r'<P>.*?</P>')
	outfile = open (filename, 'w')
	files = os.listdir (giga_path)
	i = 0
	for afile in files :
		afile = os.path.join (giga_path, afile)
		print "processing " + afile
		g_file = gzip.GzipFile (afile)
		f = g_file.read ().replace ('\n', ' ')
		#outfile.write (f)
		for content in pattern.finditer (f) :
			outfile.write (content.group ().replace ('<P>', '').replace ('</P>', '') + '\n')
		g_file.close ()
		i += 1
		print i
		#if i > 0 : break
	print (i)
	outfile.close ()


