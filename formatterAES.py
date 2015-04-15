import binascii

def main():
    Option = raw_input("Type 'F' for Format or 'D' for Decode:\n")
    if(Option == "F"):
        with open("input.txt", "w") as output:
            Input = raw_input("Enter ASCII Plaintext:\n")
            print(Input)
            print("\n")
            Input = binascii.hexlify(Input)
            print(Input)
            print("\n")
            list = []
            list += ([Input[i:i+32] for i in range(0,len(Input),32)])
            print(list)
            for words in list:
                if(len(words)!=32):
                    padding = 32-(len(words))
                    for index in range(padding):
                        words += '0'
                    words += '\n'
                    output.write(words)
                else:
                    words += '\n'
                    output.write(words)

    if(Option == "D"):
        with open("output.txt", "r") as input:
            data="".join(line.rstrip() for line in input)
            print(binascii.unhexlify(data))

if __name__ == '__main__':
    main()
