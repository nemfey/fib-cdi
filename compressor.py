import sys

def compressor(f):
    print(f.readline())

def main():
    filename = sys.argv[1]
    # file to compress
    f = open(filename,'r',encoding='utf-8')
    compressor(f)

if __name__ == "__main__":
    main()