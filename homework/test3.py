# -*-coding: utf-8 -*-
import hashlib
test = '123213sdfdsfd123123sf'
md5 = hashlib.md5(test.encode('utf-8'))
print(md5.hexdigest())
#md5.update(test.encode('utf-8'))
#md5.he