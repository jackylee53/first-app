class China:
    company = 'BAIDU'
    def __init__(self,card, balance, amount):
        self.card = card
        self.balance = balance
        self.amount = amount


    def transaction(self, another):
        another.balance -= self.amount

class American:
    company = 'IBM'
    def __init__(self, card, balance, amount):
        self.card = card
        self.balance = balance
        self.amount = amount

    def transaction(self, another):
        another.balance -= self.amount


baidu = China('123456', 23, 10)
ibm = American('654321', 23, 10)

