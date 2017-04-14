class Line:
    def __init__(self, address, hexa, code, comment):
        self.address = address
        self.hexa = hexa
        self.code = code
        self.comment = comment
        
    def __eq__(self, other):
        return self.address == other.address and \
               self.hexa == other.hexa and \
               self.code == other.code and \
               self.comment == other.comment