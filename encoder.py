# f = open('test.bin', 'wb')
# f.write(bytes([0, 33, 255])) # f is now 0021ff (in hex). list elements must be between 0, 255 (inclusive)
# f.close()
# f = open('test.bin', 'rb')
# print(f.read(-1))

# s = '101011'
# print(int(s, 2))

# %%

codes = {'d': '0', 'c': '100', 'a': '101', 'b': '11'} # convert to array with tuples ('a', 3), ('b', 2), ('c', 3), ('d', 1)

def to_table(codes, depth):
    out = [None for _ in range(depth)]
    start_i = 0
    # assume that dict (which is sorted by insertion order) has ascending keys
    for ch, code in codes.items():
        count = 2 ** (depth - len(code))
        end_i = start_i + count
        out[start_i:end_i] = [(ch, len(code)) for _ in range(count)]
        start_i = end_i
    return out

def to_tablestring(table):
    s = '\n'
    for tup in table:
        ch, count = tup
        s += ch + str(count) + '\n'
    return s.encode('ascii')

def encode(text, codes):
    bitstring = ''
    for ch in text:
        code = codes[ch]
        bitstring += code
    nums = []
    for i in range(0, len(bitstring), 8):
        bitstring_slice = bitstring[i:i+8]
        nums.append(int(bitstring_slice, 2))
    print(bitstring)
    return bytes(nums), len(bitstring)

def write_bin(path, encoded, bitlength, tablestring):
    # encoded and tablestring are both in byte form already
    f = open(path, 'wb') # wb necessary to write bytes, have to put .encode(blah) everywhere
    f.write(f'{bitlength}\n'.encode('ascii'))
    f.write(encoded)
    f.write(tablestring)
    f.close()

encoded, bitlength = encode('adcaaaaaaaaaaaaaaadddddddddddddccccccccccccccc', codes)
write_bin('test.bin', encoded, bitlength, to_tablestring(to_table(codes, 3)))

# %%
