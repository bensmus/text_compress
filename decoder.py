import math
import sys


def read_encoded(path):
    f = open(path, 'rb')
    header = f.readline().decode('ascii')
    assert header[:-1] == 'LosslessTextComp'
    
    # read the encoded text (sequence of huffman codes)
    bitlength = int(f.readline().decode('ascii'))
    encoded_bytes = f.read(math.ceil(bitlength / 8))
    bitstring = encoded_bytes_to_bitstring(encoded_bytes, bitlength)
    
    # get the codes dictionary
    f.read(1) # newline before dictionary
    codes = {}
    codelength_max = -1
    while (ch := f.read(1).decode('ascii')): # we can't just readlines because we can encode newline characters
        f.read(1) # space
        code = f.readline()[:-1].decode('ascii')
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
    for ch, code in codes.items():
        assert codelength_max >= len(code)
        count = 2 ** (codelength_max - len(code))
        end_i = start_i + count
        out[start_i:end_i] = [(ch, len(code)) for _ in range(count)]
        start_i = end_i
    return out


def decode(bitstring, table, codelength_max):
    read_size = int(math.log2(len(table)))
    bitstring_index = 0
    text = ''
    def padzeros(s, l): return s + (l - len(s)) * '0'
    while (bitstring_index < len(bitstring)):
        bitstring_slice = bitstring[bitstring_index : bitstring_index + read_size]
        print(bitstring_slice)
        tup = table[int(padzeros(bitstring_slice, codelength_max), 2)]
        text += tup[0]
        bitstring_index += tup[1]
    return text


def write_decoded(path_encoded, path_decoded):
    bitstring, bitlength, codes, codelength_max = read_encoded(path_encoded)
    table = table_from_codes(codes, codelength_max)
    text = decode(bitstring, table, codelength_max)
    f = open(path_decoded, 'w')
    f.write(text)


def main():
    assert len(sys.argv) == 3
    write_decoded(sys.argv[1], sys.argv[2])

main()
