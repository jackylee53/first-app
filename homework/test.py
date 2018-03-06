import re


# 将匹配的数字乘于 2
def double(matched):
    print(matched)
    value = int(matched.group('value'))
    return str(value * 2)


s = 'A23G4HFD567'
test = re.match('(?P<value>\d+)',s)
print(test.end(0))