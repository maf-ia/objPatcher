import os
import subprocess
import sys

class Line:
    def __init__( self, value ):
        self.value = value
        self.addr = ""
        self.hexa = ""
        self.code = ""
        self.comment = ""
        self.binData = ""
        
        elts = value[2:].split( "\t" )
        if len(elts) > 0:
            self.addr = elts[0][:-1]
            
        if len(elts) > 1:
            self.hexa = elts[1]
            data = self.hexa
            data = data.replace( " ", "" )
            self.binData = "".join([ chr(int(data[2*i:2*(i+1)],16)) for i in range( int( len(data) / 2 ) )] )
            
        if len(elts) > 2:
            codeElts = elts[2].split( "#" )
            self.code = codeElts[0]    
            if len(codeElts) > 1:
                self.comment = codeElts[1]


class Block:
    def __init__( self, title ):
        self.title = title
        self.lines = []
        self.offset = -1
        
    def addLine( self, line ):
        self.lines.append( Line(line) )
        
    def getData( self ):
        return "".join( [ l.binData for l in self.lines] )
		

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
    
    def loadFile( self, filename ):
        with open( filename, "rb" ) as fic:
            if sys.version_info.major == 3:
                self.binData = "".join([chr(e) for e in fic.read()])
            else:
                self.binData = fic.read()
            
        #data = subprocess.check_output("objdump -d -M intel " + filename, shell=True ).split( "\n" )
        os.system( "objdump -d " + str(filename) + " > /tmp/tmp.txt" )
        
        with open( "/tmp/tmp.txt", "r" ) as fic:
            data = fic.read().split( "\n" )
        
        os.system( "rm /tmp/tmp.txt" )
        self.load( data )
        self.findOffsets()
    
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
    
    def findOffsets(self):
        curOffset = 0
        for s in self.sections:
            for b in s.blocks:
                curOffset = self.findOffset( curOffset, b.getData() )
                b.offset = curOffset
                #print(b.offset, len(b.getData()))
    
    def findOffset(self, offset, data ):
        return self.binData.find( str(data), offset )
    
    def addSection( self, sectionTitle ):
        s = Section( sectionTitle )
        self.currentSection = s
        self.sections.append( s )
        

        
        
