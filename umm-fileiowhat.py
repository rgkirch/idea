import sys

try:
	name = sys.argv[1]
except IndexError:
	sys.exit( "No input file." )

try:
	with open( name , "rb") as input_stream:
		other = name + ".encrypted"
		try:
			with open( other, "wb") as output_stream:
				while( 1 ):
					f_char = input_stream.read( 1 )
					f_int = ord( f_char )
					o_char = chr( f_int )
					output_stream.write( o_char )

				input_stream.close()
				output_stream.close()
		except IOError:
			sys.exit( "Could not open file for writing." )
except IOError:
	sys.exit( "Could not find file named '" + name + "'." )

