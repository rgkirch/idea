import random
iv_ints = [ random.randint( 0, 255 ) for _ in range( 2 ) ]
IV = 0
for index, sub in enumerate( iv_ints[::-1] ):
	IV += sub<<( index*8 )
print [ bin(x) for x in iv_ints ]
print bin( IV )
