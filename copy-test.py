with open( "image.jpg", "rb" ) as f, open( "copy.jpg", "wb" ) as o:
	print len( f.read() )
