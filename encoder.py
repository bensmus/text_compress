import queue
import sys

class Node:
    def __init__(self, ch, count, left, right):
        self.ch = ch
        self.count = count
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.count < other.count

def read(path):
    f = open(path, 'r')
    s = f.read(-1)
    f.close()
    return s

def charcount(string):
    counts = dict()
    for ch in string:
        if ch in counts:
            counts[ch] += 1
        else:
            counts[ch] = 1
    return counts

def huff_tree(charcount):
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

def codes_from_tree(root):
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

def get_codes_bytes(codes):
    s = '\n'
    for key, value in codes.items():
        s += key + ' ' + value + '\n'
    return s.encode('ascii')

def encode(text, codes):
    bitstring = ''
    for ch in text:
        code = codes[ch]
        bitstring += code
    nums = []
    for i in range(0, len(bitstring), 8):
        bitstring_slice = bitstring[i : i + 8]
        nums.append(int(bitstring_slice, 2))
    return bytes(nums), len(bitstring)

def write(path, encoded_bitlength, encoded_bytes, codes_bytes):
    f = open(path, 'wb') # wb necessary to write bytes, have to put .encode(blah) everywhere
    f.write('LosslessTextComp\n'.encode('ascii'))
    f.write(f'{encoded_bitlength}\n'.encode('ascii'))
    f.write(encoded_bytes)
    f.write(codes_bytes)
    f.close()

def main():
    assert len(sys.argv) == 3
    path_in = sys.argv[1]
    path_out = sys.argv[2]
    text = read(path_in)
    codes = codes_from_tree(huff_tree(charcount(text)))
    codes_bytes = get_codes_bytes(codes)
    encoded_bytes, encoded_bitlength = encode(text, codes)
    write(path_out, encoded_bitlength, encoded_bytes, codes_bytes)

main()
