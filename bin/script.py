#!/usr/bin/env python
import os
import sys
if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Format: ./script pm_file image_file vm_type"
		exit(1)
	os.chdir("../src/")
	os.system("python main_mini.py " + sys.argv[1] + " " +sys.argv[2] + " " +sys.argv[3])

