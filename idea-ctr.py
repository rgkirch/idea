# Richard Kirchofer

# International Data Encryption Algorithm
# developed by Xuejia Lai and James L. Massey published in 1991

# Encrypts a 64 bit block of plaintext into a 64 bit block of ciphertext using a 128 bit key

# 2**16 + 1 is prime so all mod that has an inverse
# multiplication mod 2**16 + 1
# 2**16 == 0

# any files listed after the invocation ie
# $ python program.py file1 file2
# may be iterated though as in
# for line in fileinput.input():
#		do stuf on line
import fileinput

# it's sys
import sys
import os

# We must expand the 128 bit input to provide 56, 16 bit keys
# start at index 0, grab 8 and wrap around if you walk off the end
# start +25 from last time, grab 8 moar of 'em
def key_expansion(master_key):
	# "Expands the '1010...' 128 bit string input into a list of 52 integers in the range 0-2**16 (16bits), [1,3,5,9,...]"
	"""Expands the ['1','0','1'] 128 bit list of strings into a list of 52 integers in the range 0-2**16 (16bits), [1,3,5,9,...]"""
	# The 128 bit key is expanded into 52 16-bit keys.

	# double the string so we can walk off and wrap around
	twice = master_key*2
	temp_key = []
	start = 0
	# starting at 0, generate eight 16-bit chunks
	while len(temp_key) < 52:
		# add 8 keys to the list
		temp_key += [twice[x:x+16] for x in range(start,start+8*16,16)]
		start += 25
		start = start % 128
	# chop off the end of temp_key, it will be longer than 52 because I add 8 at a
	# time and only 4 need to be added on the last go
	temp_key = temp_key[:52]
	# joins the bits together into a string of bits ['1','0'] -> '10'
	# converts it to an int, reading it as a base 2 number
	key = [int("".join(bits),2) for bits in temp_key]
	# keys 50 and 51 are swapped
	key[49], key[50] = key[50], key[49]
	return key

def hex_to_bits(hx):
	"""ab -> ['1', '0', '1', '0', '1', '0', '1', '1']"""
	length = len(hx)
	# int() can take a string and a base and will return an integer
	# bin() can take an integer and returns a string of 0b followed by 0s and 
	b = bin(int(hx,16))
	# cut off the 0b
	b = b[2:]
	# length * 4 because each character represents 4 bits
	# bin() does not display leading 0s
	padlen = length*4-len(b)
	pad = "0"*padlen
	# list('strng') returns ['s','t','r','n','g']
	return list(pad + b)

"""
def bits_to_int(bits, length=4):
	if len(bits)%length != 0:
	   print "error, in func 'bit_to_int' input must be multiple of", length
	nibs = [bits[x:x+length] for x in range(0,len(bits),length)]
	data = []
	for nib in nibs:
	   s = "".join(str(x) for x in nib)
	   i = int(s,2)
	   data.append(i)
	return data
"""

def odd_round(X, K):
	"""Half multiply, half add, 100% switcheroo."""
	# replace 0 with 2 to the power of 16
	# multiply then mod 2**16+1
	mult = lambda x,y: ((x if x != 0 else 2**16)*(y if y != 0 else 2**16)) % (2**16+1)
	# 2**16 maps to 0
	add = lambda x,y: (x+y) % (2**16)
	# print mult(X[0], K[0]), "=", X[0], "*", K[0]
	# print add(X[2], K[2]), "=", X[2], "+", K[2]
	# print add(X[1], K[1]), "=", X[1], "+", K[1]
	# print mult(X[3], K[3]), "=", X[3], "*", K[3]
	return [mult(X[0], K[0]), add(X[2], K[2]), add(X[1], K[1]), mult(X[3], K[3])]

def even_round(X, K):
	"""This is it's own inverse. f(f(x)) = x"""
	# see diagram not attached
	mult = lambda x,y: ((x if x != 0 else 2**16)*(y if y != 0 else 2**16)) % (2**16+1)
	add = lambda x,y: (x+y) % (2**16)
	Yin = X[0] ^ X[1]
	Zin = X[2] ^ X[3]
	Yout = mult(add(mult(Yin, K[0]), Zin), K[1])
	Zout = add(mult(Yin, K[0]), Yout)
	return [X[0] ^ Yout, X[1] ^ Yout, X[2] ^ Zout, X[3] ^ Zout]

def encrypt(M,K):
	"""encrypts one block of 64 bits (4, 16-bit chunks)"""
	# M = [int, int, int, int]
	# K = [int, int, int, int, int, int, int, int...]
	# key undex
	ki = 0
	for rnd in range(1,18):
		if rnd % 2 == 0:
			M = even_round(M, K[ki:ki+2])
			ki += 2
		else:
			M = odd_round(M, K[ki:ki+4])
			ki += 4
	return M

def read_data(f):
	"""This function yields the next 16 chars of the file with each iteration."""
	hex_chars = '0123456789abcdef'
	while 1:
		d = f.read(16)
		d = filter(lambda x: x in hex_chars, d)
		if not d:
			break
		if len(d) < 16:
			d = d + '0'*(16-len(d))
		### INPUT_VALIDATION ###
		# if filter(lambda x: x not in hex_chars, d):
			# print >> sys.stderr, "fileinput not all hex chars"
			# print >> sys.stderr, filter(lambda x: x not in hex_chars, d)
			# print >> sys.stderr, "see non hex chars above"
		yield d

def encrypt_main():
	hex_chars = '0123456789abcdef'
	# prepend is now a function that prepends 0s to the input up to a length of y
	prepend = lambda x, y: '0'*(y-len(x)) + x
	is_hex_char = lambda x: x in '0123456789abcdef'

	# mk is 32 hex
	if 'key.txt' in os.listdir(os.getcwd()):
		# open
		temp = open('key.txt', 'rb')
		#read
		MK = temp.readline().strip()
		iv_hex = temp.readline().strip()
		# filter
		MK = filter(is_hex_char, MK)
		iv_hex = filter(is_hex_char, iv_hex)
		#close
		temp.close()
	else:
		MK = raw_input("key:\n").strip()
		MK = filter(is_hex_char, MK)

	### INPUT_VALIDATION ###
	if len(MK) != 32:
		print >> sys.stderr, "key needs to be 32 long not " + str(len(MK))
	# if filter(lambda x: x not in hex_chars, MK):
		# print >> sys.stderr, "key not all hex chars"
		# print >> sys.stderr, filter(lambda x: x not in hex_chars, MK)
		# print >> sys.stderr, "see non hex chars above"

	master_key = key_expansion(hex_to_bits(MK))
		
	if 'key.txt' in os.listdir(os.getcwd()):
		pass
	else:
		iv_hex = raw_input("initialization vector:\n").strip()
		iv_hex = filter(is_hex_char, iv_hex)

	### INPUT_VALIDATION ###
	if len(iv_hex) != 16:
		print >> sys.stderr, "iv needs to be 16 long not " + str(len(iv_hex))
	# if filter(lambda x: x not in hex_chars, iv_hex):
		# print >> sys.stderr, "iv not all hex chars:"
		# print >> sys.stderr, filter(lambda x: x not in hex_chars, iv_hex)
		# print >> sys.stderr, "see non hex chars above"


	# iv is 16 hex
	iv_int = int(iv_hex, 16)
	# the first argument after the name of this file is used as input
	# if no argument is provided then the program will read from stdin
	try:
		input_stream = open(sys.argv[1], "rb")
	except IndexError:
		input_stream = sys.stdin
	# the second argument after the name of this file is used as output
	# if no argument is provided then the program will print to stdout
	try:
		output_stream = open(sys.argv[2], "w")
	except IndexError:
		output_stream = sys.stdout
	# that is totally the most impressive part of this code (to me (right now))

	data = input_stream.read()
	data = filter(is_hex_char, data)


	# read chunks of 16 hex from generator
	# FOR CHUNK IN [DATA[X:X+16] FOR X IN RANGE(0,LEN(DATA), 16)]:
	# read_data is a generator and so is iterable
	# read_data returns chunks of 16 for each call of next()
	# for text in read_data(input_stream):
	for text in [data[x:x+16] for x in range(0,len(data),16)]:
		# if we got to the last one, pad it
		if len(text) != 16:
			text = text + '0'*(16-len(text))
		# convert int to hex, cut off leading '0x', prepend leading 0s
		IV = hex(iv_int)[2:]
		# a when hex is called on a large number, the output can look like 0xffL
		# we have to cut out the L
		IV = filter(is_hex_char, IV)
		IV = prepend(IV,16)
		# convert iv from int to hex, break into quarters, convert each quarter to int
		iv_list = [int(IV[y:y+4],16) for y in range(0,16,4)]
		# same for text_list
		text_list = [int(text[y:y+4],16) for y in range(0,16,4)]
		# encrypting the iv and key creates the otp_list (One Time Pad)
		# opt_list is a list of four ints
		otp_list = encrypt(iv_list, master_key)
		# xor the input block and the otp_list
		for bitstream, plaintext in zip(otp_list, text_list):
			output_stream.write(prepend(hex(int(bitstream ^ plaintext))[2:],4))
		# increment the iv and mod it
		iv_int = int((iv_int + 1) % 2**16)
	# cleaning up
	# if input_stream is not stdin then we opened a file and need to close it
	if input_stream != sys.stdin:
		input_stream.close()
	# if output_stream is not stdout then we opened a file and need to close it
	if output_stream != sys.stdout:
		output_stream.close()

"""
try:
	input_stream = open(sys.argv[1], "rb")
except IndexError:
	input_stream = sys.stdin
try:
	output_stream = open(sys.argv[2], "w")
except IndexError:
	output_stream = sys.stdout
"""

encrypt_main()


# master_key = "0123456789abcdef0123456789abcdef"
# key = key_expansion(hex_to_bits(master_key))

# block_input = "0123456789abcdef"


