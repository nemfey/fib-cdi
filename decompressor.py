import sys
import time
from collections import Counter
from operator import itemgetter

#######################
### BURROWS-WHEELER ###
#######################

def decode_burrows_wheeler(last_col, pos):
    n = len(last_col)
    first_col = sorted([(i, x) for i, x in enumerate(last_col)], key=itemgetter(1))
    T = [None for i in range(n)]
    for i, y in enumerate(first_col):
        j, _ = y
        T[j] = i
    Tx = [pos]
    for i in range(1, n):
        Tx.append(T[Tx[i - 1]])
    s = [last_col[i] for i in Tx]
    s.reverse()
    return ''.join(s)


#####################
### MOVE TO FRONT ###
#####################

def decode_move_to_front(cod, alp):
    alphabet = list(alp)
    txt = ""
    for index in cod:
        char = alphabet[index]
        txt += char
        alphabet.pop(index)
        alphabet.insert(0, char)
    return txt


###############
### HUFFMAN ###
###############

def source_fromtext(txt, n=1):
    freq_packs = {}
    for i in range(len(txt) - n + 1):
        packs = txt[i:i+n]
        if packs in freq_packs:
            freq_packs[packs] += 1
        else:
            freq_packs[packs] = 1
    freq_list = [(k, v) for k, v in freq_packs.items()]
    return sorted(freq_list, key=lambda x: x[0])

def kraft_inequality(lengths, q):
    s = 0
    for l in lengths:
        s += q**-l

    return s <= 1

def format_to_alf(number, base, length, alf):
    if number == 0:
        res = alf[0]
        if length == 1:
            return res
        else:
            count = 1
            digits = []
            digits.append(res)
            while (count < length):
                digits.insert(0, alf[0])
                count +=1
            res = ''.join(str(e) for e in digits[::-1])
            return res

    digits = []
    while number > 0:
        digits.append(alf[int(number % base)])
        number //= base
    count = len(digits)
    while (count < length):
                digits.append(alf[0])
                count +=1        
    res = ''.join(str(e) for e in digits[::-1])
    return res

def canonical_code(L,q=2, alf = [0,1]):
    if not kraft_inequality(L, q):
        return 'The entry does not satisfy Kraft-McMillan inequality.'
    
    bl_count = Counter(L)
    code = 0
    bl_count[0] = 0
    next_code = {}
    maximum = max(L) + 1       
    for l in range (1, maximum):
        code = (code + bl_count[l-1])*q
        next_code[l] = code 
    def_code = []
    lengths = {}
    for l in L:
        length = l
        def_code.append(next_code[length])
        lengths[next_code[length]] = length
        next_code[length] += 1
    def_code = list(map(lambda x: format_to_alf(x,q,lengths[x], alf),def_code))
    return def_code

def huffman_code(txt, src, package_size=1):
    d_nodes = {}
    for c in src:
        d_nodes[c[0]] = 0
    
    sorted_d = sorted(src, key=lambda x: x[1]) 

    while len(sorted_d) > 1:
        new_c = sorted_d[0][0] + sorted_d[1][0]
        new_f = sorted_d[0][1] + sorted_d[1][1]
        
        for i in range(0, len(sorted_d[0][0]), package_size):
            package = sorted_d[0][0][i:i+package_size]
            d_nodes[package] += 1
            
        for i in range(0, len(sorted_d[1][0]), package_size):
            package = sorted_d[1][0][i:i+package_size]
            d_nodes[package] += 1
        
        sorted_d[1] = (new_c,new_f)
        sorted_d.pop(0);
        sorted_d = sorted(sorted_d, key=lambda x: x[1])
    
    result = [(key,value) for key, value in zip(d_nodes.keys(), canonical_code(d_nodes.values(), 2, ['0','1']))]
    return result


##############
### DECODE ###
##############

def decode(txtb,corr):
    corr = dict(corr)
    corr_keys = list(corr.keys())
    corr_values = list(corr.values())
    txt_decoded = ''
    i, j = 0, 0
    while j<=len(txtb):
        substring = txtb[i:j]
        if substring in corr_values:
            pos = corr_values.index(substring)
            txt_decoded += corr_keys[pos]
            i = j
        j += 1
        
    if i != len(txtb): # all the text could not be processed
        return 'Message could not be decoded'
    return txt_decoded


#########################
### SAVE FILE PROCESS ###
#########################

def write_decoded_text_to_file(decoded_txt):
    f = open('decoded_txt.txt','w')
    f.write(decoded_txt)
    f.close()


#######################################
### GET PARAMETERS AND ENCODED TEXT ###
#######################################

def split_txt(txt):
    alp = ""
    src = ""
    max_digits = ""
    index = ""
    coded_txt = ""

    # CODE HERE

    return alp, src, max_digits, index, coded_txt


#############################
### DECOMPRESSION PROCESS ###
#############################

def decompressor(input_txt):

    # Read encoded text and parameters
    alp, src, max_digits, index, coded_txt = split_txt(input_txt)

    # Convert from bytes to string
    # CODE HERE

    # Huffman
    huf = huffman_code(coded_txt,src,2)
    corr = dict(huf)

    # Decode
    huf_decoded = decode(coded_txt,corr)
    huf_decoded = [int((huf_decoded[i:i+max_digits])) for i in range(0, len(huf_decoded), max_digits)]

    # Move-to-Front
    mtf_decoded = decode_move_to_front(huf_decoded,alp)

    # Burrows-Wheeler
    decoded_txt = decode_burrows_wheeler(mtf_decoded,index)

    # Write decoded text to output file
    write_decoded_text_to_file(decoded_txt)


############
### MAIN ###
############

def main():
    # Start execution time
    start_time = time.time()

    # Read input file
    filename = sys.argv[1]
    input_txt = open(filename,'r',encoding='utf-8').read()

    # Decode text and write it to file
    decompressor(input_txt)

    # Execution time
    end_time = time.time()
    print('Execution time (in seconds):', end_time - start_time)

if __name__ == "__main__":
    main()