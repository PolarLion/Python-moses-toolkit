import sys
import os

def chinesetok(input, output):
  state = 0
  infile = open (input, 'r')
  outfile = open (output, 'w')
  for line in infile.readlines():
    words = line.decode('utf-8')
    new_line = ""
    for word in words:
      ch = word.encode('utf-8')
      if (ch.isalnum() or ch == '.') and state == 0:
        new_line += " " + ch
        state = 1
      elif state == 1 and (ch.isalnum() or ch == '.'):
        new_line += ch
      elif ch.isspace():
        a = 0
      elif not ch.isalnum():
        state = 0
        new_line += " " + ch
    new_line = new_line.strip()
    # print new_line
    outfile.write(new_line+"\n")
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

