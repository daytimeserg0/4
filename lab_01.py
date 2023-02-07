a, b, c = map(float, input().split())
d = b ** 2 - 4 * a * c
if d > 0:
    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b - d ** 0.5) / (2 * a)
    print(f'Первый корень {x1}, Второй корень {x2}')
elif d == 0:
    x = (-b) / (2 * a)
    print(f'Единственный кoрень {x}')
else:
    print("Нет корней")