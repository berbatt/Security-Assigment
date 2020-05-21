# start the virus
import sys
import random

virusLines = []

thisFile = sys.argv[0]
virusFile = open(thisFile,"r")
lines = virusFile.readlines();
virusFile.close()


stringLines = "".join(lines)


def get_random_key(l):
    result = bin(random.getrandbits(l))[2:].zfill(l)
    return result

def xor(plain,key):
    r = []
    for i, j in zip(plain, key):
        r.append(str(int(i) ^ int(j)))  # xor between bits i and j
    return "".join(r)

def encrypt(plain,key):
    return xor(plain,key)

def decrypt(cipher,key):
    return xor(cipher,key)

def convertToBits(message):
    byte_array = message.encode()
    binary_int = int.from_bytes(byte_array,"big")
    binary_string = bin(binary_int)
    return binary_string[2:]

def frombits(bits):
    binary_int = int(bits, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text

# convert lines to bits
bit_lines = convertToBits(stringLines)

# generate a key
key = get_random_key(len(bit_lines))

# encryption part
encrypted = encrypt(bit_lines,key)

# decryption part
decrypted = decrypt(encrypted,key)

print(frombits(decrypted))


#exec(stringLines