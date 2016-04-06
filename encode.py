#!/usr/bin/python
#

import sys
import random
import os


def collate(int_array):
	buf = []
	for b in range(8):
		for i in int_array:
			buf.append((i >> b) & 0b1)
	return buf


def invert_alternate(int_array):
	state = False
	for i in range(len(int_array)):
		if state:
			int_array[i] ^= 1
		state = not state


def chunk(int_array, size):
	if len(int_array) % size != 0:
		raise Exception("chunk(): Array length not compatible with chunk size.")
	retval = []
	for i in range(len(int_array) / size):
		retval.append(int_array[(size * i):(size * (i + 1))])
	return retval


def encode(ip):
	if len(ip) > 256:
		print "String too long."
		return
	length = collate([len(ip)])
	length.reverse()
	int_array = [ord(c) for c in ip]
	buf = collate(int_array)
	for i in range(4096 - len(buf) - len(length)):
		buf.append(0 if random.random() > 0.5 else 1)
	buf.extend(length)
	invert_alternate(buf)
	mat = chunk(buf, 64)
	return mat


def write_file(filename, matrix):
	if os.path.isfile(filename):
		raise Exception("File already exists: " + filename)
	f = open(filename + ".pbm", "w")
	f.write("P1\n")
	f.write("# Have fun!\n")
	f.write("64 64\n")
	for row in matrix:
		f.write(" ".join([str(i) for i in row]) + "\n")
	f.close()


def operate(ip, filename):
	matrix = encode(ip)
	try:
		write_file(filename, matrix)
	except Exception as e:
		print e.message


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print 'Usage: $ python encode.py "[text]" [output file name]'
		exit()
	ip = sys.argv[1]
	filename = sys.argv[2]
	operate(ip, filename)
