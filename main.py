import os
import random



def get_file():
    file = input("input file:\n")
    if os.path.exists(file):
        return file

    else:
        exit("The selected file is missing!")


def get_interval(_frequency, _low, _high):
    intervals = {str(): [0.0, 1.0]}
    intervals.clear() 

    full_stretch = _high - _low
    for i in _frequency:
        percent_stretch = _frequency[i] * full_stretch
        intervals[i] = [_low, percent_stretch + _low]

        _low = percent_stretch + _low

    return intervals


def compress(file):
    # Получение количества каждого символа

    with open(file, "r") as f:
        frequency = dict()

        size = 0
        for line in f:
            for sym in line:
                if sym in frequency.keys():
                    frequency[sym] += 1
                else:
                    frequency[sym] = 1
                size += 1
        f.close()
    # Получение вероятности
    for sym in frequency:
        frequency[sym] /= size

    # Построение интервалов и get вероятность
    with open(file, "r") as f:
        high = 1.0
        low = 0.0
        probability = 0.0

        for line in f:
            for sym in line:
                interval = get_interval(frequency, low, high)
                print(interval[sym])

                for i in interval:
                    if i == sym:
                        low = interval[i][0]
                        high = interval[i][1]
                        probability = random.triangular(low, high)
        f.close()
    
    # 8 цифр после запятой
    probability = int(pow(10, 9) * probability)
    #print(probability)

    def get_fraction(x):
        x = int(pow(10, 9) * x)
        return x

    frequency = dict(zip(frequency.keys(),[get_fraction(i) for i in frequency.values()]))
    print(frequency)

    print(len(frequency))
    # Запись результата в файл
    with open(file + '.enc', "wb") as out:
        out.write(len(frequency).to_bytes(2, 'big'))

        for sym, value in frequency.items():
            out.write(int(sym).to_bytes(2, "big"))
            out.write(value.to_bytes(4, "big"))
        
        out.write(probability.to_bytes(4, 'big'))
        out.close()    


def decompress(file):
    with open(file, "rb") as f:
        len_frequency = int.from_bytes(f.read(2), "big")
        

        def fraction_to_float(x):
            x = float(pow(10, -8) * x)
            return x
        

        '''
            В цикле берем первую букву и байтов , далее следующие
            4 байта отвечающие за значение. После цикла последние 
            4 байта с частотой. Перед записью в словарь делаем 
            обратную операцию возведения в степень для приведения
            к типу float

        '''
        frequency = dict()
        for i in range(len_frequency):
            symbol = chr(int.from_bytes(f.read(1), "big"))

            value =  int.from_bytes(f.read(4), "big")
            value = fraction_to_float(value)
            frequency[symbol] = value
        

        probability = int.from_bytes(f.read(4), "big")
        probability = float(pow(10, -9) * probability)

        print(frequency)
        print(probability)

        
        # print(chr(int.from_bytes(f.read(1), "big")))
        # print(int.from_bytes(f.read(4), "big"))
        # for j in f:
        #     print(j)
            #print(int(i, 10))
            #print(i)


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
