#!/usr/bin/python

infile  = open("/Users/aamiraziz/include_list.txt", 'r')  # open file for appending
outfile = open("/Users/aamiraziz/include_list_2.txt","a") # open file for appending

for line in infile.readlines():
  outfile.write("\"-I" + line.strip("\n") + "\",\n")

infile.close()
outfile.close()