import string, random
s = string.ascii_lowercase + string.digits
print(''.join(random.sample(s,5)))