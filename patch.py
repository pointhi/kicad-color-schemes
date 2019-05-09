#!/bin/python3.6
import sys

patch=open(sys.argv[1], "r").readlines()
orig=open(sys.argv[2],"r")
origlines = orig.readlines()

for idx,oline in enumerate(origlines):
  osubst = oline.split('=')
  for idx1,pline in enumerate(patch):
    psubst = pline.split('=')
    if osubst[0] == psubst[0]:
      origlines[idx] = pline
      patch.pop(idx1)
origlines += patch
orig.close

new=open(sys.argv[2],"w")
new.writelines(origlines)
new.close
