#写一个可以执行的脚步，指定文件的内容进行全局替换
# python your_script.py old_str new_str filename
import sys
import chardet


def change_context(old_context, new_context, filename='sdfsdf.txt'):
    with open(filename, 'rb') as f:
        code = chardet.detect(f.read())['encoding']
    print('你的文件编码是：%s。我们将以这个编码处理文件。' % code)
    with open(filename, 'r', encoding=code) as f:
        for line in f:
            if old_context in line:
                new_line = line.replace(old_context, new_context)
            else:
                new_line = line



def main():
    change_context(old_context='123', new_context='321')


if __name__ == '__main__':
    main()
