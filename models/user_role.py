import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()

    @classmethod
    def get_enum_labels(cls):
        print('cls', cls)
        for k,v in cls:
            print('c', k, v)
        return [i.value for i in cls]

    def translate(self, _escape_table):
        return self.name


class GuaEncoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def gua_decode(d):
    if GuaEncoder.prefix in d:
        name = d[GuaEncoder.prefix]
        return UserRole[name]
    else:
        return d
if __name__ == '__main__':
    l = UserRole.get_enum_labels()
    print('l', l)
    # i = UserRole.guest
    # print('i' ,i)
    # print("UserRole['guest']", UserRole['guest'])
    # print('pjdr', i == 'guest')
    # print('pjdr1', i == UserRole.guest)
    # print('type', type(i))


