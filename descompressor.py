import sys

def descompressor(f):
    print(f.readline())

def main():
    filename = sys.argv[1]
    # file to descompress
    f = open(filename,'r',encoding='utf-8')
    descompressor(f)

if __name__ == "__main__":
    main()