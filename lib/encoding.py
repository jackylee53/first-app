import sys
class Encoding():
    def __init__(self):
        pass;

    def encoding_app(self, encode):
        self.encode = encode
        reload(sys)
        sys.setdefaultencoding(self.encode)