d = {'a': 1, 'b': 2}
c = {'f': 2, 'g': 3}

f,g = c
print('f', d)
print('g', g)
# def test(*args, **kwargs):
#     print('*args', args)
#     print('**kwargs', kwargs)
#
#
# test(**c, **d)
a = None
b = None
if (a and b)is True:
    print('1')

# filterMap = {
#     'created_time':{
#         'date_type': "%Y-%m-%d %H:%M:%S",
#     },
#     'updated_time':{
#         'date_type': "%Y-%m-%d %H:%M:%S",
#     },
#     'purchase_time':{
#         'date_type': "%Y-%m-%d",
#     }
# }
filterMap = dict(
    created_time={
        'date_type': "%Y-%m-%d %H:%M:%S",
    },
    updated_time={
        'date_type': "%Y-%m-%d %H:%M:%S",
    },
    purchase_time={
        'date_type': "%Y-%m-%d",
    }
)
keyMap = filterMap.keys()
# print('keymap', filterMap['created_time'].format())
print('keymap', filterMap['created_time'].get('date_type'))
    # 格式化日期
    # for m in ms:
    #         for i in m:
    #             if i in keyMap:
    #                 # format = '%Y-%m-%d %H:%M:%S'
    #                 ct = m[i]
    #                 # d['created_time'] = '{}-{}-{} {}:{}:{}'.format(ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second)
    #                 m[i] = ct.strftime(filterMap[i]['format'])
    #                 print('m[i]', m[i])
