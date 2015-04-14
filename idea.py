# International Data Encryption Algorithm
# developed by Xuejia Lai and James L. Massey published in 1991

# Encrypts a 64 bit block of plaintext into a 64 bit block of ciphertext using a 128 bit key

def key_expansion(master_key):
    "The 128 bit key is expanded into 52 16-bit keys."
    # print master_key
    twice = master_key*2
    # print twice
    # for y in [4,2]:
        # for x in master_key:
            # twice += x
    key = []
    start = 0
    while len(key) < 52:
        key += [twice[x:x+16] for x in range(start,start+8*16,16)]
        start += 25
        start = start % 128
    key = key[:52]
    # for i,each in enumerate(key):
        # print i,each
    # keys 50 and 51 are swapped
    temp = key[49]
    key[49] = key[50]
    key[50] = temp
    return key

def plus(one,two):
    "returns the bitwise sum modulo 2*8"
    half = map(lambda x,y: x^y,x and y,one,two)





test = []
for i in range(64):
    test.append(True)
    test.append(False)
print len(test)
# test = range(128)
round_keys = key_expansion(test)
