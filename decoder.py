import math

def get_metadata(path):
    f = open(path, 'r')
    s = ''
    start_encoded = 1 # take newline byte into account
    while (ch := f.read(1)) != '\n':
        s += ch
        start_encoded += 1
    bitlength = int(s)
    f.close()
    return bitlength, start_encoded

# print(get_metadata('test.bin'))

def split(path):
    bitlength, start_encoded = get_metadata(path)
    f = open(path, 'rb')
    f.read(start_encoded)
    encoded = f.read(math.ceil(bitlength / 8))
    f.read(1) # there's a newline before the table
    table = f.read(-1)
    return encoded, bitlength, table

def encoded_to_bitstring(encoded, bitlength):
    bitstring = ''
    bitlength_last = bitlength - (bitlength // 8) * 8
    for i, b in enumerate(encoded):
        s = bin(b)[2:]
        # encoder split a binary string into groups of 8, so bin(b) does not capture leading 0's
        if i < len(encoded) - 1:
            s = '0' * (8 - len(s)) + s
        else:
            s = '0' * (bitlength_last - len(s)) + s
        bitstring += s
    return bitstring

def tablestring_to_table(tablestring):
    s_to_tup = lambda s: (s[0], int(s[1]))
    return list(map(s_to_tup, tablestring.split('\n')[:-1]))

def decode(bitstring, table):
    read_size = int(math.log2(len(table)))
    bitstring_index = 0
    text = ''
    while (bitstring_index < len(bitstring)):
        bitstring_slice = bitstring[bitstring_index : bitstring_index + read_size]
        tup = table[int(bitstring_slice, 2)]
        text += tup[0]
        bitstring_index += tup[1]
    return text

encoded, bitlength, tablebytes = split('test.bin')
table = tablestring_to_table(tablebytes.decode('ascii'))
print(table)
bitstring = encoded_to_bitstring(encoded, bitlength)
print(bitstring)
text = decode(bitstring, table)
print(text)
