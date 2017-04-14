# coding=utf8
class Function:
    def __init__(self, name, lines):
        self.name = name
        self.lines = lines

    def __eq__(self, other):
        return self.name == other.name and \
               self.lines == other.lines