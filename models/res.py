from flask import (
    make_response,

)


class Res(object):
    def __init__(self, form, msg='success'):
        self.code = 0
        self.msg = msg
        self.data = form

    @classmethod
    def success(cls, form={}, msg='success'):
        r = cls(form)
        r.msg = msg
        return r.__dict__

    @classmethod
    def fail(cls, form={}, msg='fail'):
        r = cls(form)
        r.code = form.get('code') or 1
        r.msg = msg

        return r.__dict__


def test():
    form = {
        'name': 'test'
    }
    h = dict(
        test1='1',
        test2='2'
    )
    s = Res.success(form)
    print('success', s)
    # e = Res.fail(form)
    # print('fail', e)


if __name__ == '__main__':
    test()
