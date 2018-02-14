f = open(file='test', mode='r+', encoding='utf-8')
data = f.read()
f.seek(0)
new_data = data.replace('jenry', 'henry')  # 将文件中jenry字符替换为ham
f.write(new_data)
f.close()