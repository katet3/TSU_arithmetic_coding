import os

import hashlib
import encode
import decode

def get_file():
    print(" |")
    file = input(" ---> input file: ")
    if os.path.exists(file):
        return file

    else:
        exit("The selected file is missing!")



def main():
    print("|--------------------------------------------------------|")
    print("|          choose option: [c]ompress/[d]ecompress        |")
    print("|--------------------------------------------------------|")
    print("|            for test program, write \"test\"            |")
    print("|--------------------------------------------------------|")
    print(" |")
    choose = input(" ---> ")

    if 'c' == choose.lower():
        file = get_file()
        if 0 != encode.compress(file):
            print("Error")

    elif 'd' == choose.lower():
        file = get_file()
        decode.decompress(file)

    elif 'test' == choose.lower():
        file = get_file()
        if 0 != encode.compress(file):
            print("Error")
        if 0 != decode.decompress(file + ".enc"):
            print("Error")
        

        with open(file, 'rb') as f:
            file1_hash = hashlib.sha256(f.read()).hexdigest()
            f.close()
        with open(file + ".enc.dec", 'rb') as f:
            file2_hash = hashlib.sha256(f.read()).hexdigest()
            f.close()

        if file1_hash == file2_hash:
            print(" |\n ---> File hashes match!")
            print(" input:   " + file1_hash)
            print(" output:  " + file2_hash)
        else:
            print(" |\n ---> File hashes do not match!")
            print(" input:   " + file1_hash)
            print(" output:  " + file2_hash)



    else:
        exit("Unknown choose!")


if __name__ == "__main__":
    main()
