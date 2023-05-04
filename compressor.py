import sys
from math import floor
from collections import defaultdict

# calculate source from the given txt
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

# apply arithmetic encoding algorithm to the given text
def arithmetic_encode_bin(txt,k):
    src = source_fromtext(txt)
    suma = sum([x[1] for x in src])
    init_probs = [(x[0],x[1]/suma) for x in src]
    cumulative_probs = [0] + [sum(p[1] for p in init_probs[:i+1]) for i in range(len(init_probs))]
    
    alpha = '0' * k
    beta = '1' * k
    c = ""
    u = 0
    s = ""

    for i in range(0, len(txt)):
        s += txt[i]
        if not any(s in tupla for tupla in init_probs):
            continue

        delta = int(beta,2) - int(alpha,2) + 1
        current_intervals = [(int(alpha,2) + int(floor(delta * cumulative_probs[j-1])),
                              int(alpha,2) + int(floor(delta * cumulative_probs[j]) - 1)) 
                             for j in range(1, len(cumulative_probs))]
        
        pos = [x[0] for x in init_probs].index(s)
        alpha = bin(current_intervals[pos][0])[2:].zfill(k)
        beta = bin(current_intervals[pos][1])[2:].zfill(k)
        
        while alpha[0] == beta[0]:
            c += alpha[0]
            if alpha[0] == '0':
                    c += '1' * u
            else:
                    c += '0' * u
            u = 0
            alpha = alpha[1:] + '0'
            beta = beta[1:] + '1'
            
        while alpha[:2] == '01' and beta[:2] == '10':
            alpha = alpha[0] + alpha[2:] + '0'
            beta = beta[0] + beta[2:] + '1'
            u += 1
        
        s = ""
    return c + '1'

def compressor(txt):
    # encode the txt
    k = 23
    coded_txt = arithmetic_encode_bin(txt,k)

    # write the code into file
    f = open('coded_txt.txt','w')
    f.write(coded_txt)
    f.close()

    return coded_txt

def main():
    # read input file as txt
    filename = sys.argv[1]
    f = open(filename,'r',encoding='utf-8')
    txt = f.readline()
    f.close()

    # compress the input txt
    coded_txt = compressor(txt)

    # calculate the performance
    unicode_chars = len(txt)
    coded_bytes = len(coded_txt) / 8

    performance = (coded_bytes / unicode_chars) * 8

    print("Performance of the compressing algorithm:", performance)

if __name__ == "__main__":
    main()