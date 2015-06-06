#!/usr/bin/env python
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
    print t
    rl = reference
    r = {}
    for i in xrange (len (rl)) :
        k = tuple (rl [i:i+n])
        r [k] = r.get (k, 0) + 1
    print r
    print "corrects ", corrects (t, r)
    precision = corrects (t, r) * 1.0 / (len (tl) -n + 1) 
    print "precision ", precision
    print "recall ", corrects (t, r) * 1.0 / (len (rl) - n + 1)
    return precision#, recall



if __name__ == "__main__":
    t1 = "Israeli officials responsibility of airport safely".split (' ')
    t2 = "airport security Israeli officials are responsible".split (' ')
    r = "Israeli officials are responsible for airport security".split (' ')
    bleu1 = 1.0
    bleu2 = 1.0
    for i in range (0, 4) :
        p1 = score (t1, r, i+1)
        p2 = score (t2, r, i+1)
        bleu1 *= p1
        bleu2 *= p2
        print "bleu1", bleu1 * min (1, len (t1) * 1.0 / len (r))
        print "bleu2", bleu2 * min (1, len (t2) * 1.0 / len (r))
