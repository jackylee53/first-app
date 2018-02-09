f = open(file='test', mode='r+', encoding='utf-8')
data = f.read()
new_data = data.replace('哈哈哈', 'h')
f.seek(0)
f.write(new_data)
#f.write(new_line)
f.close()



#print(data)
