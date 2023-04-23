import os
import struct
from mpmath import *
from bisect import bisect


def get_file():
    file = input("input file:\n")
    if os.path.exists(file):
        return file

    else:
        exit("The selected file is missing!")


def compress(file):
    with open(file, "r") as cin:
        if not cin:
            return -1

        plain_text = cin.read()
        cin.close()

    precision = 32
    highest_value = int(2 << precision - 1) #<<
    
    quarter = int(ceil(highest_value / 4))
    half = 2 * quarter
    threequarters = 3 * quarter

    chars_count = dict()
    for ch in plain_text:
        chars_count[ch] = chars_count.get(ch, 0) + 1

    #вероятность
    model = dict()
    start = 0

    model.fromkeys(chars_count)
    for ch in chars_count.keys():
        width = chars_count[ch]/len(plain_text)
        model[ch] = width
        start += chars_count[ch]/len(plain_text)

    f = [0.0]
    for a in model:
        f.append(f[-1] + model[a])
    
    f.pop()
    f = dict([(a, mf) for a, mf in zip(model, f)])
        
    res = []
    low, hight = 0, highest_value
    straddle = 0

    #по тексту
    for k in range(0, len(plain_text)):
        lohi_range = hight - low + 1

        #пересчет
        low = low + ceil(lohi_range * f[plain_text[k]])
        hight = low + floor(lohi_range * model[plain_text[k]])

        while True:
            if hight < half:
                res.append(0)
                res.extend([1 for i in range(straddle)])
                straddle = 0

            elif low >= half:
                res.append(1)
                res.extend([0 for i in range(straddle)])
                straddle = 0
                low -= half
                hight -= half

            elif low >= quarter and hight < threequarters:
                straddle += 1
                low -= quarter
                hight -= quarter

            else:
                break

            low = 2 * low
            hight = 2 * hight + 1

    straddle += 1
    if low < quarter:
        res.append(0)
        res.extend([1 for i in range(straddle)])
    else:
        res.append(1)
        res.extend([0 for i in range(straddle)])

    #информация о словаре и частотах
    with open(file + '.enc',"wb") as out:
        if not out:
            return -1

        out.write(len(plain_text).to_bytes(4, byteorder='little'))
        col_letters = (len(chars_count.keys())-1).to_bytes(1, byteorder='little')
        out.write(col_letters)

        for letter, code in chars_count.items():
            out.write(ord(letter).to_bytes(2, byteorder='little'))
            out.write(code.to_bytes(4, byteorder='little'))

        res = [str(i) for i in res]
        res = ''.join(res)

        enc_out = pad_encoded_text(res)
        enc_out = get_byte_array(enc_out)
        out.write(bytes(enc_out))
        
        if out.close():
            return -1

    return 0

#добавление padding
def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8

    for _ in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text

    return encoded_text

#получение массива байтов
def get_byte_array(padded_encoded_text):
    if (len(padded_encoded_text) % 8 != 0):
        print("Encoded text not padded")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))

    return b

'''
def decompress(file):
    with open(file, "rb") as f:
        len_frequency = int.from_bytes(f.read(2), "big")
        

        def fraction_to_float(x):
            x = float(pow(10, -17) * x)
            return x
        

        
            В цикле берем первую букву и байтов , далее следующие
            4 байта отвечающие за значение. После цикла последние 
            4 байта с частотой. Перед записью в словарь делаем 
            обратную операцию возведения в степень для приведения
            к типу float

        
        frequency = dict()
        for i in range(len_frequency):
            symbol = chr(int.from_bytes(f.read(2), "big"))

            value =  int.from_bytes(f.read(32), "big")
            value = fraction_to_float(value)
            frequency[symbol] = value
        

        probability = int.from_bytes(f.read(32), "big")
        probability = float(pow(10, -17) * probability)
    
        print(frequency)
        print(probability)
        f.close()

    # Расшифровка в файл
    with open(file + ".dec", "w") as out:
     
        high = 1.0
        low = 0.0
        flag = True
        while flag:  
            interval = get_interval(frequency, low, high)
            for sym, value in interval.items():
                if value[0] <= probability < value[1]:
                    #print(interval)
                    if sym == chr(0):
                        flag = False
                        break
                    
                    #print(sym)
                    out.write(sym)

                    low = value[0]
                    high = value[1]
                    break
                elif value[0] == probability and value[1] == probability:
                    print(value[0], value[1])
                    flag = False

                else:
                    continue
                    #    flag = False
'''


def main():
    

    str2 = 'input.txt'

    compress(str2)




    return 0
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
