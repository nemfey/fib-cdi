import sys
from math import floor

def arithmetic_decode_bin(code, k, src, l):
    suma = sum([x[1] for x in src])
    init_probs = [(x[0],x[1]/suma) for x in src]
    cumulative_probs = [0] + [sum(p[1] for p in init_probs[:i+1]) for i in range(len(init_probs))]
    
    alpha = '0' * k
    beta = '1' * k
    gamma = code[:k]
    used = k
    x = ''
    
    while len(x) != l:
        delta = int(beta,2) - int(alpha,2) + 1
        current_intervals = [(int(alpha,2) + int(floor(delta * cumulative_probs[j-1])),
                              int(alpha,2) + int(floor(delta * cumulative_probs[j]) - 1)) 
                             for j in range(1, len(cumulative_probs))]
        
        for pos, subinterval in enumerate(current_intervals):
            if subinterval[0] <= int(gamma,2) <= subinterval[1]:
                x += init_probs[pos][0]
                alpha = bin(subinterval[0])[2:].zfill(k)
                beta = bin(subinterval[1])[2:].zfill(k)
               
        if len(x) >= l:
            break
            
        while alpha[0] == beta[0]:
            alpha = alpha[1:] + '0'
            beta = beta[1:] + '1'
            if used == len(code):
                gamma = gamma[1:] + '0'
            else:
                gamma = gamma[1:] + code[used]
                used += 1
                
        while alpha[:2] == '01' and beta[:2] == '10':
            alpha = alpha[0] + alpha[2:] + '0'
            beta = beta[0] + beta[2:] + '1'
            if used == len(code):
                gamma = gamma[0] + gamma[2:] + '0'
            else:
                gamma = gamma[0] + gamma[2:] + code[used]
                used += 1
    return x

def descompressor(txt):
    # decode the txt
    k = 23
    src = [(' ', 1867), ('!', 1), ("'", 4), (',', 212), ('-', 5), ('.', 37), (':', 6), (';', 21), ('?', 1), ('A', 10), ('B', 4), ('C', 8), ('D', 6), ('E', 7), ('F', 4), ('G', 6), ('H', 2), ('I', 2), ('L', 6), ('M', 8), ('N', 2), ('O', 1), ('P', 6), ('Q', 9), ('R', 5), ('S', 3), ('T', 6), ('U', 1), ('Y', 6), ('\\', 10), ('a', 1017), ('b', 175), ('c', 302), ('d', 427), ('e', 1067), ('f', 46), ('g', 80), ('h', 92), ('i', 358), ('j', 34), ('l', 498), ('m', 230), ('n', 560), ('o', 734), ('p', 149), ('q', 132), ('r', 508), ('s', 571), ('t', 267), ('u', 391), ('v', 68), ('x', 2), ('y', 122), ('z', 34), ('¡', 1), ('¿', 1), ('á', 31), ('é', 29), ('í', 95), ('ñ', 18), ('ó', 62), ('ú', 7), ('ü', 1)]
    l = 10375 # size of original text
    decoded_txt = arithmetic_decode_bin(txt,k,src,l)

    # write the decoded text into file
    f = open('decoded_txt.txt','w')
    f.write(decoded_txt)
    f.close()

    #return decoded_txt

def main():
    # read input file as txt
    filename = sys.argv[1]
    f = open(filename,'r',encoding='utf-8')
    txt = f.readline()
    f.close()

    # compress the input txt
    descompressor(txt)

if __name__ == "__main__":
    main()