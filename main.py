import os

def get_file():
    file = input("input file:\n")

    if os.path.exists(file):
        return file

    else:
        exit("The selected file is missing!")


def compress():
	pass


def decompress():
	pass


def main():
    print("|--------------------------------------------------------|")
    print("|          choose option: [c]ompress/[d]ecompress        |")
    print("|--------------------------------------------------------|")
    choose = input()

    if choose == 'c':
        file = get_file()
        compress(file)
    
    elif choose == 'd':
        file = get_file()
        decompress(file)
	
    else:
        exit("Unknown choose!")
		

if __name__ == "__main__":
	main()