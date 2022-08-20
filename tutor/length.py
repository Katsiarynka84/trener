def length(a, b, c, d):
    from math import sqrt
    pif = sqrt(((x2 - x1)**2+(y2 - y1)**2))
    return pif

# считываем данные
x1, y1, x2, y2 = float(input('введите 4 числа:\n')),float(input()),float(input()),float(input())

# вызываем функцию
print(length(x1, y1, x2, y2))



