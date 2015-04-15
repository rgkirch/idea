import sys

try:
	with open( "key.txt", "rb" ) as f:
		key = f.read( 16 )
		iv = f.read (8)
except EnvironmentError:
	sys.exit( "Could not open key.txt\nMake sure it's in this dir" )
print [bin(ord(x)) for x in list(key)]

