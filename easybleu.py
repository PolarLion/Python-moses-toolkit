#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# compute Bleu scores with confidence intervals via boostrap resampling
# written by Ulrich Germann
#
# This file is part of moses.  Its use is licensed under the GNU Lesser General
# Public License version 2.1 or, at your option, any later version.

import math
import os
import sys





def corrects (translated, reference) :
    corrects = 0
    for k, v in translated.items () :
        # print k, v, reference.get(k, 0)
        corrects += min (v, reference.get (k, 0))
    return corrects


def score (translated, reference, n) :
    tl = translated
    t = {}
    for i in xrange (len (tl)) :
        k = tuple (tl [i:i+n])
        t [k] = t.get (k, 0) + 1
    # print t
    rl = reference
    r = {}
    for i in xrange (len (rl)) :
        k = tuple (rl [i:i+n])
        r [k] = r.get (k, 0) + 1
    # print r
    print "corrects ", corrects (t, r)
    precision = corrects (t, r) * 1.0 / (len (tl) -n + 1) 
    print "precision ", precision
    print "recall ", corrects (t, r) * 1.0 / (len (rl) - n + 1)
    return precision#, recall

def bleu (translated, reference, n) :
    t = translated.split (" ")
    r = reference.split (" ")
    b = {}
    bleu = 1.0
    for i in range (0, n) :
        p = score (t, r, i+1)
        bleu *= p
        print min (1, len (t) * 1.0 / len (r))
        print "bleu", bleu * min (1, len (t) * 1.0 / len (r))
        b [i] = bleu * min (1, len (t) * 1.0 / len (r))




if __name__ == "__main__":
    t1 = "You still haven 't arrived at the company ?"
    r = "Haven ’ t you arrived at the company yet ?"
    bleu (t1, r, 4)
    # bleu1 = 1.0
    # bleu2 = 1.0
    # for i in range (0, 4) :
    #     p1 = score (t1, r, i+1)
    #     p2 = score (t2, r, i+1)
    #     bleu1 *= p1
    #     bleu2 *= p2
    #     print "bleu1", bleu1 * min (1, len (t1) * 1.0 / len (r))
    #     print "bleu2", bleu2 * min (1, len (t2) * 1.0 / len (r))
