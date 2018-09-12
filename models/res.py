class Res(object):
    def __init__(self, form, msg):
        self.code = 0
        self.data = form
        self.msg = msg 
    @classmethod
    def success(cls, form):
        r = cls(form)
        return r.__dict__
    
    @classmethod
    def fail(cls, form):
        r = cls(form)
        r.code = 1
        r.msg = 'fail'
        return r.__dict__

def test():
    form = {
        'name': 'test'
    }
    s = Res.success(form)
    print('success', s)    
    e = Res.fail(form)
    print('fail', e)

if __name__ == '__main__':
    test()
