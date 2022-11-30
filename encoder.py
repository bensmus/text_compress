import queue

codes = {'d': '0', 'c': '100', 'a': '101', 'b': '11'} # convert to array with tuples ('a', 3), ('b', 2), ('c', 3), ('d', 1)

class Node:
    def __init__(self, ch, count, left, right):
        self.ch = ch
        self.count = count
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.count < other.count

def to_string(path):
    f = open(path, 'r')
    return f.read(-1)

def charcount(string):
    counts = dict()
    for ch in string:
        if ch in counts:
            counts[ch] += 1
        else:
            counts[ch] = 1
    return counts

def to_tree(charcount):
    pq = queue.PriorityQueue()
    nodecount = len(charcount.items())
    for ch, count in charcount.items():
        pq.put(Node(ch, count, None, None))
    for _ in range(nodecount - 1):
        node_a = pq.get()
        node_b = pq.get()
        node_combined = Node(node_a.ch + node_b.ch, node_a.count + node_b.count, node_a, node_b)
        pq.put(node_combined)
    return pq.get()

def to_codes(root):
    codes = dict()
    current_node = root
    current_code = ''
    def fill_codes(node, code):
        if node:
            if len(node.ch) == 1:
                codes[node.ch] = code
            fill_codes(node.left, code + '0')
            fill_codes(node.right, code + '1')
    fill_codes(current_node, current_code)
    return codes

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
