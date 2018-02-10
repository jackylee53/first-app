#写一个可以执行的脚步，指定文件的内容进行全局替换
# python your_script.py old_str new_str filename
import sys
import chardet


def change_context(old_context, new_context, filename):
    print()
    o_f = open(filename, 'r')
    sys.argv