# International Data Encryption Algorithm
# developed by Xuejia Lai and James L. Massey published in 1991

# Encrypts a 64 bit block of plaintext into a 64 bit block of ciphertext using a 128 bit key

# 2**16 + 1 is prime so all mod that has an inverse
# multiplication mod 2**16 + 1
# 2**16 == 0

def key_expansion(master_key):
    "Expects a list of bits"
    # The 128 bit key is expanded into 52 16-bit keys.
    # print master_key
    twice = master_key*2
    # print twice
    # for y in [4,2]:
        # for x in master_key:
            # twice += x
    temp_key = []
    start = 0
    # starting at 0, generate eight 16-bit chunks
    while len(temp_key) < 52:
        temp_key += [twice[x:x+16] for x in range(start,start+8*16,16)]
        start += 25
        start = start % 128
    # chop off the end of temp_key, it will be longer than 52 because I add 8 at a
    # time and only 4 need to be added on the last go
    temp_key = temp_key[:52]
    key = [int("".join(bits),2) for bits in temp_key]
    # print key
    # keys 50 and 51 are swapped
    # temp = key[49]
    # key[49] = key[50]
    # key[50] = temp
    key[49], key[50] = key[50], key[49]
    return key

def hex_to_bits(hx):
    "length is how many bytes it is, 2 chars of hex"
    length = len(hx)
    # int() can take a string and a base and will return an integer
    # bin() can take an integer and returns a string of 0b followed by 0s and 1s
    b = bin(int(hx,16))
    # cut off the 0b
    b = b[2:]
    # length * 4 because each character represents 4 bits
    padlen = length*4-len(b)
    # pad = [0 for x in range(padlen)]
    pad = "0"*padlen
    # pad = [0 for x in range(len(length*8-len(b)))]
    # return pad + [0 if x=="0" else 1 for x in b]
    return list(pad + b)

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

def odd_round(X, K):
    mult = lambda x,y: ((x if x != 0 else 2**16)*(y if y != 0 else 2**16)) % (2**16+1)
    add = lambda x,y: (x+y) % (2**16)
    # print mult(X[0], K[0]), "=", X[0], "*", K[0]
    # print add(X[2], K[2]), "=", X[2], "+", K[2]
    # print add(X[1], K[1]), "=", X[1], "+", K[1]
    # print mult(X[3], K[3]), "=", X[3], "*", K[3]
    return [mult(X[0], K[0]), add(X[2], K[2]), add(X[1], K[1]), mult(X[3], K[3])]

def even_round(X, K):
    "This is it's own inverse. f(f(x)) = x"
    mult = lambda x,y: ((x if x != 0 else 2**16)*(y if y != 0 else 2**16)) % (2**16+1)
    add = lambda x,y: (x+y) % (2**16)
    Yin = X[0] ^ X[1]
    Zin = X[2] ^ X[3]
    Yout = mult(add(mult(Yin, K[0]), Zin), K[1])
    Zout = add(mult(Yin, K[0]), Yout)
    return [X[0] ^ Yout, X[1] ^ Yout, X[2] ^ Zout, X[3] ^ Zout]

def encrypt(M,K):
    "encrypts one block of 64 bits (4, 16-bit chunks)"
    ki = 0
    for rnd in range(1,18):
        if rnd % 2 == 0:
            M = even_round(M, K[ki:ki+2])
            ki += 2
        else:
            M = odd_round(M, K[ki:ki+4])
            ki += 4
    return M

def decrypt(M,K):
    "same as encrypt but pass in inverse of the keys for the odd round"
    # if p is prime
    # y = x**(p-2) mod p
    inverse = lambda x: pow(x, 2**16-1, 2**16+1)
    ki = 52
    for rnd in range(1,18):
        if rnd % 2 == 0:
            ki -= 2
            M = even_round(M, K[ki:ki+2])
        else:
            ki -= 4
            # print "round", rnd
            # print "inv of", hex(K[ki]), "is", hex(inverse(K[ki]))
            # print "inv of", hex(K[ki+1]), "is", hex(2**16-1-K[ki+1])
            # print "inv of", hex(K[ki+2]), "is", hex(2**16-1-K[ki+2])
            # print "inv of", hex(K[ki+3]), "is", hex(inverse(K[ki+3]))
            M = odd_round(M, [inverse(K[ki]), 2**16-1-K[ki+1], 2**16-1-K[ki+2], inverse(K[ki+3])])
    return M

def main(block, key_input):
    "block and key_input are strings of hex characters"
    if len(block) != 16:
        print "error, from main: block size must be 16 hex chars"
    if len(key_input) != 32:
        print "error, from main: key input must be 32 hex chars"
    key = key_expansion(hex_to_bits(key_input))
    q = len(block)/4
    M = [int(block[hi:hi+q],16) for hi in range(0,len(block), q)]
    print "message", M
    print "after encrypt", encrypt(M,key)
    return decrypt(encrypt(M,key), key)

master_key = "0123456789abcdef0123456789abcdef"
block_input = "0123456789abcdef"
# print "what i want after encrypt", bits_to_int(hex_to_bits("e06300a677ba7854"), 16)
# print bin(int(master_key,16))
# print key_expansion(hex_to_bits(master_key, 16))[0]

# after = main(block_input, master_key)
# print "after decrypt", after



# for i in range(1000):
#     ran = random.random()
#     num = int(ran*(2**16-1))
#     inver = inverse(num)
#     invmo = invmod(num)
#     if inver != invmo:
#         print "wrong"
#     print inver, invmo
#     print 
# # print random.random()







# r = int(random.random()*2**16)
# print r
# print key_expansion(r)
