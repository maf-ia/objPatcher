import os

class Line:
    def __init__( self, value ):
        self.value = value
        self.addr = ""
        self.hexa = ""
        self.code = ""
        self.comment = ""
        
        elts = value[2:].split( "\t" )
        if len(elts) > 0:
            self.addr = elts[0][:-1]
            
        if len(elts) > 1:
            self.hexa = elts[1]
            
        if len(elts) > 2:
            codeElts = elts[2].split( "#" )
            self.code = codeElts[0]    
            if len(codeElts) > 1:
                self.comment = codeElts[1]

class Block:
    def __init__( self, title ):
        self.title = title
        self.lines = []
        
    def addLine( self, line ):
        self.lines.append( Line(line) )

class Section:
    def __init__( self, title ):
        self.title = title
        self.blocks = []
        
    def addBlock( self, title ):
        self.blocks.append( Block( title ) )
        
    def addBlockLine( self, line ):
        self.blocks[-1].addLine( line )

class TreeDump:
    def __init__( self ):
        self.title = ""
        self.sections = []
    
    def load( self, data ):
        for line in data:
            if line != "":
                if self.title == "":
                    self.title = line
                else:
                    if line[0] == " ":
                        self.currentSection.addBlockLine( line )
                    elif line[0] == "0":
                        self.currentSection.addBlock( line )
                    else:
                        self.addSection( line )
    
    def addSection( self, sectionTitle ):
        s = Section( sectionTitle )
        self.currentSection = s
        self.sections.append( s )
        

def buildDump():
    os.system( "objdump -d step1.bin > code.txt" )
    
def readDump():
    with open( "./test/code.txt", "r" ) as fic:
        data = fic.read().split( "\n" )
        
    tree = TreeDump()
    tree.load( data )
    return tree
        
        
