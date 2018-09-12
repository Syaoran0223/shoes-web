class My_Response():
    def __init__(self, form):
        self.code = 0
        self.data = form
        self.msg = '请求成功'

    @classmethod
    def success(cls, form):
        r = cls(form)
        return r.__dict__

    @classmethod
    def fail(cls):
        r = cls({})
        r.code = 1
        r.msg = '请求失败'
        return r.__dict__
    #  缺少参数
    @classmethod
    def errorRequire(cls):
        pass

def two_sum(numbers, target):
    result = {}
    for index, n in enumerate(numbers):
        result[n] = index
    for n in numbers:
        temp = target - n
        if temp in numbers:
            nIndex = result[n]
            tempIndex = result[temp]
            break
    return [nIndex, tempIndex]

if __name__ == '__main__':
    form = dict(
        username='feng'
    )
    r = My_Response.success(form)
    print('成功', r)
    r = My_Response.fail()
    print('失败', r)

