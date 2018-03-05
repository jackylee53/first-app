'''
作业题目（一）：三级菜单
作业需求：
可依次选择进入各子菜单
可从任意一层往回退到上一层
可从任意一层退出程序
所需新知识点：列表、字典
'''
menu = {
    '北京': {
        '海淀': {
            '五道口': {
                'soho': {},
                '网易': {},
                'google': {}
            },
            '中关村': {
                '爱奇艺': {},
                '汽车之家': {},
                'youku': {},
            },
            '上地': {
                '百度': {},
            },
        },
        '昌平': {
            '沙河': {
                '老男孩': {},
                '北航': {},
            },
            '天通苑': {},
            '回龙观': {},
        },
        '朝阳': {},
        '东城': {},
    },
    '上海': {
        '闵行': {
            "人民广场": {
                '炸鸡店': {}
            }
        },
        '闸北': {
            '火车战': {
                '携程': {}
            }
        },
        '浦东': {},
    },
    '山东': {},
}

currert_level = menu
list = []
while True:
    for key in currert_level:
        print(key)
    location = input('请输入,b为返回上一层，q为退出>').strip()
    if not location:continue

    if location in currert_level:
        list.append(currert_level)
        currert_level = currert_level[location]

    elif location == 'b':
        if len(list) != 0:
            currert_level = list.pop() #将删除的上一层层级重新赋值给currert_level变量
        else:
            print('已在顶级目录')

    elif location == 'q':
        exit()


