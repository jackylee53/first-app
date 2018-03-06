menu = [
    {
    'text': '北京',
    'children': [
        { 'text': '朝阳','children':[]},
        { 'text': '昌平','children':[
            { 'text': '沙河','children':[]},
            { 'text': '回龙观','children':[]}
        ]},
        ]
    },
    {
        'text': '上海',
        'children': [
            {'text': '宝山', 'children': []},
            {'text': '金山', 'children': []},
            {'text': '徐汇区', 'children': [{'text': '漕宝路', 'children':[]}]},
        ]
    }
]

#打印所有的text
l1 = []
def get_text(list):
    for i in list:
        l1.append(i.get('text'))
        get_text(list=i.get('children'))
    return l1
print('所有text名称：',get_text(menu))

#输入节点名字，遍历找到了就打印，并返回true。
str = input('请输入节点名称：').strip()
def get_text(list):
    for i in list:
        if str == i.get('text'):
            print(i.get('text'))
            return True
        else:
            get_text(list=i.get('children'))

print(get_text(menu))