import sys
import re
import os
import easybleu



bleun = 1
threshold = {1:0.3, 2:0.2, 3:0, 4:0}


def count_sentences_len(filename):
  sl={}
  infile = open(filename,'r')
  count_s = 0.0
  for line in infile.readlines():
    count_s += 1.0
    l = len(line.split(r' ')) 
    #if l > 100:print line
    if sl.has_key(l):
      sl[l] += 1
    else:
      sl[l] = 1
  count = 0
  for k in sorted(sl):
    #print type(a)
    count += sl[k]
    print str(k) + "\t" + str(sl[k])+"\t"+str( count/count_s)
  return filename, sl

def truel2fakel(l):
  if l <= 43:
    return l
  else:
    return 45
  # if l <= 7:
  #   return l
  # elif l <=9 :
  #   return 9
  # elif l <= 14:
  #   return 14
  # elif l <= 20:
  #   return 20
  # elif l <= 30:
  #   return 30
  # elif l <= 40:
  #   return 40
  # else:
  #   return 50

def trueb2fakeb(b):
  if b <= 0.0001:
    return 0.0
  elif b <= 0.0288:
    return 0.01
  # elif b <= 0.0483:
    # return 0.0483
  elif b <= 0.067:
    return 0.04
  # elif b <= 0.12:
    # return 0.09
  elif b <= 0.3444:
    return 0.20
  # elif b <= 0.9:
  #   return 0.9
  else:
    return 1.0

def analyze_len_bleu(filename):
  if not os.path.exists("/home/xwshi/data/ana-len/"):
    os.system("mkdir /home/xwshi/data/ana-len/")
  else:
    os.system("rm  /home/xwshi/data/ana-len/*")
  if not os.path.exists("/home/xwshi/data/ana-bleu/"):
    os.system("mkdir /home/xwshi/data/ana-bleu/")
  else:
    os.system("rm  /home/xwshi/data/ana-bleu/*.dict")

  prefix = filename.split('/')
  # print type(prefix)
  lower_than_threshold = open("/home/xwshi/data/ana-bleu/"+prefix[len(prefix)-2]+".lower_than_threshold.txt",'w')
  infile = open(filename,'r')
  slb = {}
  for i in range(1, 100):
    slb[truel2fakel(i)] = {}
  avelenbleu = {}
  bsl = {}
  sld = {}
  trb = {}
  state = 0
  line1 = ""
  line2 = ""
  line3 = ""
  id_dict = {}
  for line in infile.readlines():
    if state == 0:
      line1 = line
      source = re.match(r"(?:\[.*?\])(.*)", line).groups()[0].strip()
      source_id = re.match(r"\[#(.*?)\]", line).groups()[0].strip()
      sl = truel2fakel(len(source.split(' ')))
      #print line, source, sl
      if sld.has_key(sl):
        sld[sl] += 1
      else:
        sld[sl] = 1
      state += 1
    elif state == 1:
      line2 = line
      # bleu = trueb2fakeb(float(re.match(r"\[(.*?)\]", line).groups()[0].strip()))
      bleu = float(re.match(r"\[(.*?)\]", line).groups()[0].strip())
      trans = re.match(r"(?:\[.*?\])(.*)", line).groups()[0].strip()
      # trl = truel2fakel(len(trans.split(' ')))
      trl = len(trans.split(' '))
      #print bleu, trans, trl
      state += 1
    elif state == 2:
      line3 = line
      id_dict[source_id] = line1+line2+line3
      ref = re.match(r"(?:\[.*?\])(.*)", line).groups()[0].strip()
      rfl = len(ref.split(' '))
      if rfl < bleun:
        state = 0 
        continue
      bleu_n = easybleu.bleu_n(trans, ref, 4)
      # print bleu_n
      # print bleu, trans, ref, source_id
      if not bleu_n.has_key(bleun): bleu = 0
      else: bleu = bleu_n[bleun]
      if bleu < threshold[bleun] and sl > 1:
        print source_id
        lower_than_threshold.write(line1)
        lower_than_threshold.write(line2)
        lower_than_threshold.write(line3)
      if slb[sl].has_key(bleu):
        slb[sl][bleu] += 1
      else:
        slb[sl][bleu] = 1
      if avelenbleu.has_key(sl):
        avelenbleu[sl] += bleu
      else:
        avelenbleu[sl] = bleu
      state = 0
      # break
  lower_than_threshold.close()
  #print slb
  
  for k in slb:
    outfile = open("/home/xwshi/data/ana-len/"+str(k), "w")
    for kk in slb[k]:
      if trb.has_key(kk):
        trb[kk] += slb[k][kk]
      else :
        trb[kk] = slb[k][kk] 
      if bsl.has_key(kk):
        if bsl[kk].has_key(k):
          bsl[kk][k] += slb[k][kk]
        else:
          bsl[kk][k] = slb[k][kk]
      else:
        bsl[kk]={}
        bsl[kk][k] = slb[k][kk]
      outfile.write(str(kk)+"\t"+str(slb[k][kk])+"\n")
    outfile.close()

  all_outfile = open("/home/xwshi/data/ana-bleu/all.txt", 'w')
  for k in sorted(bsl):
    outfile = open("/home/xwshi/data/ana-bleu/"+str(k)+".dict", "w")
    for kk in sorted(bsl[k]):
      outfile.write(str(kk)+"\t"+str(bsl[k][kk])+"\t"+str(bsl[k][kk]/(1.0*sld[kk]))+"\n")
      # for i in range(0,bsl[k][kk]):
      all_outfile.write(str(k)+"\t"+str(kk)+"\t"+str(bsl[k][kk])+"\t"+str(bsl[k][kk]/(1.0*sld[kk]))+"\n")
    outfile.close()
  #print bsl
  all_outfile.close()
  cb = 0
  for k in sorted(trb) :
    cb += trb[k]
    # print str(k)+"\t"+str(trb[k])+"\t"+str(cb/4977.0)
  all_bleu = 0.0
  for k in sorted(avelenbleu):
    all_bleu += avelenbleu[k]
    # print str(k) + "\t" + str(avelenbleu[k]/(sld[k]*1.0))
  # print "all ", all_bleu / 4977
  return id_dict

def comparesmtnmt1(smtfilename, nmtfilename, id_dict, comm_filename):
  smtfile = open(smtfilename, 'r')
  nmtfile = open(nmtfilename, 'r')
  smtdict={}
  nmtdict={}
  for line in smtfile.readlines():
    smtdict[int(line)] = 1
  for line in nmtfile.readlines():
    nmtdict[int(line)] = 1
  print "smt number: ", len(smtdict)
  print "nmt number: ", len(nmtdict)
  count = 0
  comm_list = []
  for k in nmtdict:
    if smtdict.has_key(k):
      count += 1
      comm_list.append(k)
  print count
  comm_file = open(comm_filename, 'w')
  for k in comm_list:
    comm_file.write(id_dict[str(k)])
  comm_file.close()

def main():
  # print "hello polarlion"
  #print count_sentences_len("/home/xwshi/easymoses_workspace/evaluation/16/CHT.Test.true.zh") 
  #print count_sentences_len("/home/xwshi/easymoses_workspace/corpus/16/CHT.Train.true.zh") 
  #print count_sentences_len("/home/xwshi/easymoses_workspace/corpus/16/CHT.Train.true.en") 
  #print count_sentences_len("/home/xwshi/easymoses_workspace/evaluation/16/CHT.Test.true.en") 
  # id_dict = analyze_len_bleu("/home/xwshi/easymoses_workspace/evaluation/16/translation_result.txt.918")
  # id_dict = analyze_len_bleu("/home/xwshi/easymoses_workspace/evaluation/17/translation_result.txt")
  # comparesmtnmt1("out17.txt","out16.txt", id_dict, "comm-16.txt")
  count_sentences_len("/home/xwshi/data/Corpus-Bleu/7/C_B.Train.zh")

if __name__=="__main__":
  main()
