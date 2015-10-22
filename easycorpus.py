import sys
import os

def files2file(path, filename, style="none"):
  print path
  files = os.listdir(path)
  outfile = open(filename, 'w')
  for afile in files:
    infile = open(os.path.join(path, afile), 'r')
    i = 0
    for line in infile.readlines():
      if style == "gale" and i < 1: 
        i += 1
        continue
      if style == "gale" and (len(line.split('\t')) != 13 or not line.split('\t')[8].isalnum()):
        #print "wrong line ", line
        continue
      if style == "gale":
        aline = line.split('\t')[7].strip()
      else:
        aline = line.strip('\n')
      i += 1
      #print aline
      outfile.write(aline+"\n")
      #if i > 10:break
  outfile.close()

def chinesetok(input, output):
  state = 0
  infile = open (input, 'r')
  outfile = open (output, 'w')
  for line in infile.readlines():
    #for c in line:print c
    words = line.decode('utf-8', 'replace')
    new_line = ""
    for word in words:
      ch = word.encode('utf-8')
      if (ch.isalnum() or ch == '.') and state == 0:
        new_line += " " + ch
        state = 1
      elif state == 1 and (ch.isalnum() or ch == '.'):
        new_line += ch
      elif ch.isspace():
        state = 0
      elif not ch.isalnum():
        state = 0
        new_line += " " + ch
    new_line = new_line.strip()
    # print new_line
    outfile.write( new_line+"\n")
  infile.close()
  outfile.close() 

def prepare_chtgiga_corpus():
  tginfile = open ('/home/xwshi/easymoses_workspace/corpus/giga/giga_wpb_eng.txt', 'r')
  tcinfile = open ('/home/xwshi/data/CHT/notok/CHT.Train.en', 'r')
  toutfile = open ('/home/xwshi/data/CHT/cht-giga2/CHT.Train.en', 'w')
  soutfile = open('/home/xwshi/data/CHT/cht-giga2/CHT.Train.zh', 'w')
  count_line = 0
  max_line = 100000
  for line in tginfile.readlines():
    # line = line.split('.,g)[0]
    line = line.strip()
    toutfile.write(line+'\n')
    soutfile.write(line+'\n')
    #ount_line += 1
    if count_line >= max_line: break
  for line in tcinfile.readlines():
    line = line.strip()
    toutfile.write(line+'\n')
    
  tginfile.close()
  tcinfile.close()
  toutfile.close()
  scinfile = open('/home/xwshi/data/CHT/notok/CHT.Train.zh', 'r')
  
  count_line = 0
  # while(True):
  #   soutfile.write("\n")
  #   count_line += 1
  #   if count_line >= max_line:break
  for line in scinfile.readlines():
    line = line.strip()
    soutfile.write(line + '\n')
  scinfile.close()
  soutfile.close()

def prepare_gale_corpus(gale_corpus_dir, out_dir, corpus_id):
  source_data_dir = os.path.join(gale_corpus_dir, "data/source")
  translation_data_dir = os.path.join(gale_corpus_dir, "data/translation")
  files2file(source_data_dir, os.path.join(out_dir, corpus_id+".source.temp"), "gale")
  files2file(translation_data_dir, os.path.join(out_dir, corpus_id+".en"), "gale")
  chinesetok(os.path.join(out_dir, corpus_id+".source.temp"), os.path.join(out_dir, corpus_id+".zh"))

def batch_untar(path, outpath):
  for tgfile in os.listdir(path):
    afile = os.path.join(path, tgfile)
    print afile
    os.system("tar zxvf "+afile+" -C "+outpath)

def batch_prepare_gale_corpus(path, outpath):
  for gale_corpus_dir in os.listdir(path):
    corpusdir = os.path.join(path, gale_corpus_dir)
    #print corpusdir
    prepare_gale_corpus(corpusdir, outpath, gale_corpus_dir)
  os.system("rm "+os.path.join(outpath,"*.temp"))

def check_corpus(path, sid, tid):
  files = os.listdir(path)
  file_dict = {}
  for afile in files:
    file_dict[afile.split('.')[0]] = 0
  count_lines = 0
  for afile in file_dict:
    len1 = len(open(os.path.join(path, afile+"."+sid),'r').read().split('\n'))
    len2 = len(open(os.path.join(path, afile+"."+tid),'r').read().split('\n'))
    if len1 == len2:
      file_dict[afile] = len1
    else:
      print "wrong corpus", afile
    count_lines += len1
    print afile+"."+sid, len1, afile+"."+tid, len2
  print "total : ", count_lines
  return file_dict

def divide_corpus(inpath, outpath, num, file_dict):
  for i in range(0,num):
    path = os.path.join(outpath, str(i))
    if not os.path.exists(path):
      os.system("mkdir "+path)
    else:
      os.system("rm "+os.path.join(path,"*"))
    print i
  files = os.listdir(inpath)
  for afile in files:
    outfiles = []
    for i in range(0,num):
      path = os.path.join(outpath, str(i))
      outfile = open(os.path.join(path, afile),'w')
      outfiles.append(outfile)
    infile = open(os.path.join(inpath, afile), 'r')
    line_num = 0
    for line in infile.readlines():
      if line_num >= num:
        line_num = 0
      #print line
      outfiles[line_num].write(line)
      line_num += 1
    for outfile in outfiles:
      outfile.close()
    infile.close()

def count_corpus_words(path):
  import re
  files = os.listdir(path)
  total_words = {'zh':0,'en':0}
  words={'zh':{},'en':{}}
  for afile in files:
    #if not afile.split('.')[0] == 'CHT':continue
    fileid=afile.split('.')[1]
    infile=open(os.path.join(path,afile), 'r')
    wordlist = re.split(r'[\s\n]\s*', infile.read())
    print afile, len(wordlist)
    #print wordlist
    #break
    total_words[fileid]+=len(wordlist)
    for word in wordlist:
      if words[fileid].has_key(word):
        words[fileid][word] += 1
      else:
        words[fileid][word] = 1
  print total_words, "zh:",len(words['zh']), "en:", len(words['en'])
  count_frq = 0
  for k,v in words['en'].items():
    if v > 1:
      count_frq += 1
  print count_frq

def batch_create_corpus(inpath,opath):
  dirs = os.listdir(inpath)
  for i in range(0,10):
    oopath = os.path.join(opath, str(i))
    osfile = open(os.path.join(oopath, "C_B.Train.zh"),'w')
    otfile = open(os.path.join(oopath, "C_B.Train.en"),'w')
    for ii in range(0, i+1):
      iipath = os.path.join(inpath, str(ii))
      files = os.listdir(iipath)
      for afile in files:
        infile = open(os.path.join(iipath, afile),'r')
        if afile.split('.')[1] == 'en':
          otfile.write(infile.read())
        elif afile.split('.')[1] == 'zh':
          osfile.write(infile.read())
        infile.close()
    osfile.close()
    otfile.close

def sampling_file(infilename, outfilename, sampling_base):
  infile = open(infilename, 'r')
  outfile = open(outfilename, 'w')
  i = 0
  for line in infile.readlines():
    if i < sampling_base:
      i += 1
    else:
      outfile.write(line)
      i = 0
  infile.close()
  outfile.close()

def main():
  print "hello polarlion"
  #prepare_gale_corpus("/home/xwshi/data/ldc-zh-en/gale_p1_ch_blog", "/home/xwshi/data/ldc-zh-en/gale", "gale_p1_ch_blog")
  #batch_untar("/home/xwshi/data/ldc-zh-en/tgz", "/home/xwshi/data/ldc-zh-en/untgz/")
  #batch_prepare_gale_corpus("/home/xwshi/data/ldc-zh-en/untgz/", "/home/xwshi/data/ldc-zh-en/gale")
  #file_dict=check_corpus("/home/xwshi/data/ldc-zh-en/gale", "zh", "en")
  #chinesetok("/home/xwshi/data/ldc-zh-en/gale/CHT.zh", "/home/xwshi/data/ldc-zh-en/gale/t.CHT.zh")
  #files2file("/home/xwshi/data/ldc-zh-en/LDC2005T10cn_en_news_magazine_parallel_text/data/source", "/home/xwshi/data/ldc-zh-en/gale/cn_en_news_magazine_parallel_text.zh.tmp")
  #chinesetok("/home/xwshi/data/ldc-zh-en/gale/cn_en_news_magazine_parallel_text.zh.tmp", "/home/xwshi/data/ldc-zh-en/gale/cn_en_news_magazine_parallel_text.zh")
  #files2file("/home/xwshi/data/ldc-zh-en/LDC2005T10cn_en_news_magazine_parallel_text/data/translation", "/home/xwshi/data/ldc-zh-en/gale/cn_en_news_magazine_parallel_text.en")
  #divide_corpus("/home/xwshi/data/ldc-zh-en/gale", "/home/xwshi/data/ldc-zh-en/gale-divide", 10, file_dict)
  #count_corpus_words("/home/xwshi/data/ldc-zh-en/gale")
  batch_create_corpus("/home/xwshi/data/ldc-zh-en/gale-divide", "/home/xwshi/data/Corpus-Bleu")
  for i in range(0,10):
    a = 0
    #check_corpus("/home/xwshi/data/ldc-zh-en/gale-divide/"+str(i), "zh", "en")
    check_corpus("/home/xwshi/data/Corpus-Bleu/"+str(i), "Train.zh", "Train.en")



if __name__=="__main__":
  import time
  print str (time.strftime('%Y-%m-%d %X',time.localtime(time.time())))
  main()

