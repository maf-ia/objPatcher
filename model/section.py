class Section:
    def __init__(self, name, functions):
        self.name = name
        self.functions = functions

    def __eq__(self, other):
        return self.name == other.name and \
        self.functions == other.functions