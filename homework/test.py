def flatten(nested):
    try:
        # 如果是字符串，那么手动抛出TypeError。
        if isinstance(nested, str):
            raise TypeError
        for sublist in nested:
            for element in flatten(sublist):
                print('got:', element)
    except TypeError:
        yield nested


L = ['aaadf', [1, 2, 3], 2, 4, [5, [6, [8, [9]], 'ddf'], 7]]
for num in flatten(L):
    print(num)

print(isinstance(L, str))