import sys

try:
	name = sys.argv[1]
except IndexError:
	sys.exit( "No input file." )

with open( name, "rb") as input_stream, open( name + ".encrypted", "wb") as output_stream:
	while( 1 ):
		f_char = input_stream.read( 1 )
		if( f_char == "" ):
			sys.exit( "Done" )
		f_int = ord( f_char )
		o_char = chr( f_int )
		output_stream.write( o_char )

	input_stream.close()
	output_stream.close()
