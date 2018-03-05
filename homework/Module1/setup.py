import sys
from homework.Module1 import Module1_homework2_cart as Cart


def main():
    argv = sys.argv[1]
    if argv == 'install':
        Cart.setup()
    elif argv == 'run':
        Cart.main()
    else:
        print('您输入的选项不正确')


if __name__ == '__main__':
    main()
