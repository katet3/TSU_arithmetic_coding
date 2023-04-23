from mpmath import *
MAX_VALUE=32


def compress(file):
    with open(file, "rb") as cin:
        if not cin:
            return -1

        input_text = cin.read()
        cin.close()

    precision = MAX_VALUE
    highest_value = int(2 ** precision - 1) #<<
    
    quarter = int(ceil(highest_value / 4))
    half = 2 * quarter
    threequarters = 3 * quarter

    #chars_count = getCharscount(plain_text)
    #model = getModel(chars_count, len(plain_text))

    dict_chars = dict()
    for ch in input_text:
        dict_chars[ch] = dict_chars.get(ch, 0) + 1

    # вероятность
    model = dict()
    index = 0

    model.fromkeys(dict_chars)
    for ch in dict_chars.keys():
        width = dict_chars[ch]/len(input_text)
        model[ch] = width
        index += dict_chars[ch]/len(input_text)

    f = [0.0]
    for a in model:
        f.append(f[-1] + model[a])
    
    f.pop()
    f = dict([(a, mf) for a, mf in zip(model, f)])
        
    result = []
    low, hight = 0, highest_value
    straddle = 0

    #по тексту
    for k in range(0, len(input_text)):
        low_hight_range = hight - low + 1

        #пересчет
        low = low + ceil(low_hight_range * f[input_text[k]])
        hight = low + floor(low_hight_range * model[input_text[k]])

        while True:
            if hight < half:
                result.append(0)
                result.extend([1 for i in range(straddle)])
                straddle = 0

            elif low >= half:
                result.append(1)
                result.extend([0 for i in range(straddle)])
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
        result.append(0)
        result.extend([1 for i in range(straddle)])
    else:
        result.append(1)
        result.extend([0 for i in range(straddle)])


    #информация о словаре и частотах
    with open(file + '.enc',"wb") as out:
        if not out:
            return -1

        out.write(len(input_text).to_bytes(4, byteorder='little'))
        col_letters = (len(dict_chars.keys())-1).to_bytes(1, byteorder='little')
        out.write(col_letters)

        
        for letter, code in dict_chars.items():
            out.write(letter.to_bytes(1, byteorder='little'))
            out.write(code.to_bytes(4, byteorder='little'))

        result = [str(i) for i in result]
        result = ''.join(result)

        enc_out = pad_encoded_text(result)
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
        print("Padding is unnecessary")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))

    return b