import sys

try:
	name = sys.argv[1]
except IndexError:
	sys.exit( "No input file." )

input_stream = open( name , "rb")
other = name + ".encrypted"
output_stream = open( other, "w")

while( input_stream ):
	f_char = input_stream.read( 1 )
	f_int = ord( f_char )
	o_char = chr( f_int )
	output_stream.write( o_char )

input_stream.close()
output_stream.close()
