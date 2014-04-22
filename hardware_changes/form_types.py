class Type(object):
    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return self.value == other

    def __str__(self):
        return "<Type {}>".format(self.value)

class Boolean(Type):
    def __init__(self, value):
        self.value = value == '1'

class Integer(Type):
    def __init__(self, value):
        self.value = int(value)
