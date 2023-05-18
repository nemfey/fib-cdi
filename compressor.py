import sys
from collections import Counter
from operator import itemgetter

#######################
### BURROWS-WHEELER ###
#######################

def compare_idx(x, y, txt):
    if txt[x] != txt[y]:
        return txt[x] < txt[y]
    
    return compare_idx((x+1)%len(txt), (y+1)%len(txt), txt)

def merge_sort(arr, txt):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]

    left = merge_sort(left, txt)
    right = merge_sort(right, txt)

    return merge(left, right, txt)


def merge(left, right, txt):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if compare_idx(left[i], right[j], txt):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result

def sorted_permutations(txt):
    perms = list(range(len(txt)))
    perms = merge_sort(perms, txt)
    return perms

def encode_burrows_wheeler_merge(txt):
    sorted_perms = sorted_permutations(txt)
    last_col = ''.join(txt[x-1] for x in sorted_perms)
    pos = sorted_perms.index(0)

    return last_col, pos


#####################
### MOVE TO FRONT ###
#####################

def encode_move_to_front(txt):
    alphabet = list(set(txt))
    alphabet.sort()
    q = len(alphabet)
    sequence = []
    for char in txt:
        index = alphabet.index(char)
        sequence.append(index)
        alphabet.pop(index)
        alphabet.insert(0, char)
    return sequence


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
        sorted_d.pop(0)
        sorted_d = sorted(sorted_d, key=lambda x: x[1])
    
    result = [(key,value) for key, value in zip(d_nodes.keys(), canonical_code(d_nodes.values(), 2, ['0','1']))]
    return result


##############
### ENCODE ###
##############

def encode(txta,corr):
    corr = dict(corr)
    txt_encoded = ''
    i, j = 0, 0
    while j<=len(txta):
        substring = txta[i:j]
        if substring in corr:
            txt_encoded += corr[substring]
            i = j
        j += 1
        
    if i != len(txta): # all the text could not be processed
        return 'Message could not be encoded'
    return txt_encoded


#########################
### SAVE FILE PROCESS ###
#########################

def write_coded_text_to_file(alp, src, max_digits, index, coded_txt):

    f = open('coded_txt.txt','wb')

    # Encode and write alp
    # CODE HERE

    # Encode and write src
    # CODE HERE

    # Encode and write max digits
    # CODE HERE

    # Encode and write index
    # CODE HERE
    
    # Write coded text
    f.write(coded_txt)
    f.close()
    #Hacer tantos writes como parámetros necesitemos que se guarden
    #linea1 = "Linea1"
    #linea1 = linea1 + '\n'
    #linea2 = "Linea2"
    #linea2 = linea2 + '\n'
    #f.write(linea1)
    #f.write(linea2)
    #Importante añandir '\n' al final de cada uno pq si no, no se guarda en cada línea. Todo tiene que ser en string
    #return coded_txt #Retorna el código para después calcular el rendimiento

    '''Segunda opción, con esta no se añade explicitamente el '\n'
    #Hace cosas
    with open('coded_txt.txt','w') as f:
        print("Linea 1", file=f)
        print("Linea 2", file=f)
    '''


###########################
### COMPRESSION PROCESS ###
###########################

def compressor(txt):

    # Alphabet of text
    alp = sorted(list(set(txt)))

    # Burrows-Wheeler transform
    bw = encode_burrows_wheeler_merge(txt)
    bw_code = bw[0]
    index = bw[1]

    # Move-to-Front
    mtf_code = encode_move_to_front(bw_code)

    max_digits = len(str(max(mtf_code)))

    mtf_code = [str(x).zfill(max_digits) for x in mtf_code]
    mtf_code = ''.join(mtf_code)

    # Huffman
    src = source_fromtext(mtf_code,2)
    huf = huffman_code(mtf_code, src, 2)
    corr = dict(huf)

    # Encoding
    huf_code = encode(mtf_code,corr)
    coded_txt = int(huf_code, 2).to_bytes((len(huf_code) + 7) // 8, byteorder='big')

    # Write paramteres and coded text to file
    write_coded_text_to_file(alp, src, max_digits, index, coded_txt)

    return coded_txt

############
### MAIN ###
############

def main():
    # Read input file
    filename = sys.argv[1]
    f = open(filename,'r',encoding='utf-8')
    txt = f.readline()
    f.close()

    # Encode text and write it to file
    coded_txt = compressor(txt)

    # Calculate encoding performance
    unicode_chars = len(txt)
    coded_bytes = len(coded_txt)
    performance = (coded_bytes / unicode_chars) * 8
    print('performance:',performance)

if __name__ == "__main__":
    main()