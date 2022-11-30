import math

# def get_metadata(path):
#     f = open(path, 'r')
#     s = ''
#     start_encoded = 0
#     while (ch := f.read(1)) != '\n':
#         s += ch
#         start_encoded += 1
#     bitlength = int(s)
#     f.close()
#     return bitlength, start_encoded + 1 # take newline byte into account

# print(get_metadata('test.bin'))

def read(path):
    # bitlength, start_encoded = get_metadata(path)
    f = open(path, 'rb')
    header = f.readline().decode('ascii')
    assert header == 'LosslessTextComp\n'
    
    bitlength = int(f.readline().decode('ascii'))

    # read the encoded text (sequence of huffman codes)
    encoded_bytes = f.read(math.ceil(bitlength / 8))
    bitstring = encoded_bytes_to_bitstring(encoded_bytes, bitlength)

    # get the codes dictionary
    f.read(1) # newline before dictionary
    codes = {}
    codelength_max = -1
    while (line := f.readline().decode('ascii')):
        ch = line[0]
        code = line[2:]
        codes[ch] = code
        codelength_max = max(codelength_max, len(code))
    f.close()
    return bitstring, bitlength, codes, codelength_max

def encoded_bytes_to_bitstring(encoded, bitlength):
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
    assert len(bitstring) == bitlength
    return bitstring

def table_from_codes(codes, codelength_max):
    out = [None for _ in range(codelength_max)]
    start_i = 0
    # assume that dict (which is sorted by insertion order) has ascending keys, this allows index into table to be correct
    breakpoint()
    for ch, code in codes.items():
        assert codelength_max >= len(code)
        count = 2 ** (codelength_max - len(code))
        end_i = start_i + count
        out[start_i:end_i] = [(ch, len(code)) for _ in range(count)]
        start_i = end_i
    return out

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

bitstring, bitlength, codes, codelength_max = read('lorem.bin')
table = table_from_codes(codes, codelength_max)
print(table)
print(bitstring)
text = decode(bitstring, table)
print(text)
