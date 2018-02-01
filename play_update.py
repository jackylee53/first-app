from lib.whitelist import Get_whitelist
#from lib.web import Handler
import sys

if __name__ == '__main__':
    play = Get_whitelist()
    if len(sys.argv) < 2:
        sys.exit(1)
    if sys.argv[1] == 'once':
        play.whitelist()
    elif sys.argv[1] == 'daemon':
        play.main()
    else:
        sys.exit(1)
