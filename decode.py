from mpmath import *
from bisect import bisect
MAX_VALUE=32


def decompress(file):
    with open(file, "rb") as cin:
        if not cin:
            return -1

        enc_bytes = cin.read()
        cin.close()

    #начинаем распаковку с символов
    len_text = int.from_bytes(enc_bytes[0:4], byteorder='little')
    col_letters = enc_bytes[4]+1
    header = enc_bytes[5:5*col_letters + 5]
    dict_chars = dict()
    
    for i in range(col_letters):
        dict_chars[header[i*5]] = int.from_bytes(header[i*5+1:i*5+5], byteorder='little') #1

    model = dict()
    start = 0
    model.fromkeys(dict_chars)
    for ch in dict_chars.keys():
        width = dict_chars[ch]/len_text
        model[ch] = width
        start += dict_chars[ch]/len_text
    
    #parse
    col_letters = enc_bytes[4]+1
    enc_text = enc_bytes[5*col_letters + 5:]

    #в бинарь
    enc_pad = ''
    for i in enc_text:
        bin_byte = bin(i)[2:].rjust(8, '0')
        enc_pad += bin_byte


    #remove_padding
    padded_info = enc_pad[:8]
    extra_padding = int(padded_info, 2)

    enc_pad = enc_pad[8:]
    encoded_text = enc_pad[:-1*extra_padding]


    #decode
    encoded_text = [int(i) for i in enc_pad]

    dec = decode(encoded_text, model, len_text)
    
    f = open(file + ".dec", 'wb')
    f.write(dec)
    f.close()

    return 0


def decode(enc_num, model, len_text):
    precision = MAX_VALUE
    highest_value = int(2 << precision - 1)

    quarter = int(ceil(highest_value / 4))
    half = 2 * quarter
    threequarters = 3 * quarter

    alpha_bet = list(model)
    f = [0]
    for a in model:
        f.append(f[-1] + model[a])
    f.pop()

    model = list(model.values())

    enc_num.extend(precision * [0]) 
    res = len_text * [0]  

    value = int(''.join(str(a) for a in enc_num[0:precision]), 2)
    y_position = precision  
    low, hight = 0, highest_value

    res_position = 0
    while 1:
        low_hight_range = hight - low + 1
        a = bisect(f, (value - low) / low_hight_range) - 1
        res[res_position] = alpha_bet[a]

        low = low + int(ceil(f[a] * low_hight_range))
        hight = low + int(floor(model[a] * low_hight_range))

        while True:
            if hight < half:
                pass

            elif low >= half:
                low = low - half
                hight = hight - half
                value = value - half

            elif low >= quarter and hight < threequarters:
                low = low - quarter
                hight = hight - quarter
                value = value - quarter

            else:
                break

            low = 2 * low
            hight = 2 * hight + 1

            value = 2 * value + enc_num[y_position]
            y_position += 1
            
            if y_position == len(enc_num)+1:
                break

        res_position += 1
        
        if res_position == len_text or y_position == len(enc_num)+1:
            break
        
    return bytes(res)
