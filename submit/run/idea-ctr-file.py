# Richard Kirchofer

# call this on foo, it will use foo.key to make foo.encrypted
# if there is no foo.key, it will make one
# call this on foo.encrypted, it will use foo.key to make foo
# if there is no foo.key, it will error

# International Data Encryption Algorithm
# developed by Xuejia Lai and James L. Massey published in 1991

# 2**16 + 1 is prime so all mod that has an inverse
# multiplication mod 2**16 + 1
# 2**16 == 0

# use sys to check extra arguments for
import sys
# create random keys
import random
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

def encrypt_main():
	hex_chars = '0123456789abcdef'
	# prepend is now a function that prepends 0s to the input up to a length of y
	prepend = lambda x, y: '0'*(y-len(x)) + x
	is_hex_char = lambda x: x in '0123456789abcdef'
	decimal_to_binary = lambda x: '0'*(8-len(bin(x)[2:])) + bin(x)[2:]

	# check that a file(name) to encrypt was provided
	try:
		input_file = sys.argv[1]
	except IndexError:
		sys.exit( "error: no input file" )
	# try to open the key file to read from
	try:
		key_file = sys.argv[2]
		with open( key_file, "rb" ) as f:
			key_ints = [ ord( x ) for x in list( f.read( 16 ) ) ]
			iv_ints = [ ord( x ) for x in list( f.read( 8 ) ) ]
			# error if too few bytes in key
			if len( key_ints ) + len( iv_ints ) < 16 + 8:
				sys.exit( "error: key file too small" )
	# if key file not provided, make one
	except IndexError:
		# this fills key and the iv with bytes
		key_ints = [ random.randint( 0, (1<<8)-1 ) for _ in range( 16 ) ]
		iv_ints = [ random.randint( 0, (1<<8)-1 ) for _ in range( 8 ) ]
		# both the key and the iv have bytes written to them because the data
		# is saved to the file one byte at a time as characters
		# the data in key_ints is later expanded into the master key
		# the data from iv_ints is modified, each pair is combined to make four 16 bit chunks
		with open( input_file + ".key", "wb" ) as key_file:
			key_file.write( "".join( [ chr( x ) for x in key_ints ] ) )
			key_file.write( "".join( [ chr( x ) for x in iv_ints ] ) )
	# we have a key and iv whether we read it or made it
	# open the file to read from and the file to write to
	# the output file may be either the encrypted or decrypted data, add suffix of .idea
	with open( input_file, "rb") as input_stream, open( input_file + ".idea", "wb") as output_stream:
		# convert key_ints from a list of bytes into a list of bits
		# master_key = key_expansion(reduce(lambda x,y: x+y, [decimal_to_binary(x) for x in key_ints],[]))
		master_key = key_expansion(list("".join([decimal_to_binary(x) for x in key_ints])))
		#master_key = key_expansion( [ decimal_to_binary( x ) for x in key_ints ] )

		# convert iv_ints to a single integer
		IV = 0
		for index, sub in enumerate( iv_ints[::-1] ):
			IV += sub<<( index*8 )
		# begin main loop
		#for _ in range ( 1 ):
		while( 1 ):
			iv_list = []
			IV_temp = IV
			# better than while(IV) because I get leading 0s
			for _ in range( 4 ):
				# mod to chop off last 16 bits of iv
				iv_list.append( IV_temp % (1<<16) )
				# shift iv over to get different bits next time
				IV_temp = IV_temp>>16
			# reverse the list
			iv_list = iv_list[::-1]
			# encrypting the iv and key creates the otp_list (One Time Pad)
			# opt_list is a list of four ints
			otp_list = encrypt(iv_list, master_key)
			# convert otp_list to single bytes instead of pairs
			otp_byte_sized = [ f(x) for x in otp_list for f in [ lambda z: (z>>8)%(1<<8), lambda z: z%(1<<8) ] ]
			for pad_byte in otp_byte_sized:
				l = input_stream.read( 1 )
				if l == '':
					sys.exit( "" )
				output_stream.write( chr( pad_byte ^ ord( l ) % 256 ) )
			# xor the input block and the otp_list

				#output_stream.write(prepend(hex(int(bitstream ^ plaintext))[2:],4))
			# increment the iv and mod it
			IV = (IV + 1) % (2**64)

encrypt_main()

