import random
iv_ints = [ random.randint( 0, (1<<16)-1 ) for _ in range( 4 ) ]
print iv_ints
IV = 0
for index, sub in enumerate( iv_ints[::-1] ):
	IV += sub<<( index*16 )
print [ bin(x) for x in iv_ints ]
print bin( IV )
print IV
iv_list = []
while( IV ):
	iv_list.append( IV % (1<<16) )
	IV = IV>>16
iv_list= iv_list[::-1]
print iv_list
