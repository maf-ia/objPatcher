import os
import subprocess
import sys

from PyQt4.QtGui import *

class LineItem(QStandardItem):
    def __init__( self, data, col ):
        super(QStandardItem, self).__init__()
        self.data = data
        if col == 0:
            self.setText( data.addr )
        elif col == 1:
            self.setText( data.hexa )
        elif col == 2:
            self.setText( data.code )
        else:
            self.setText( data.comment )


class Line:
    def __init__( self, value ):
        self.value = value
        self.addr = ""
        self.hexa = ""
        self.code = ""
        self.comment = ""
        self.binData = ""
        self.newData = ""
        
        elts = value[2:].split( "\t" )
        if len(elts) > 0:
            self.addr = elts[0][:-1]
            
        if len(elts) > 1:
            self.hexa = elts[1]
            data = self.hexa
            data = data.replace( " ", "" )
            self.binData = "".join([ chr(int(data[2*i:2*(i+1)],16)) for i in range( int( len(data) / 2 ) )] )
            self.newData = self.binData
            
        if len(elts) > 2:
            codeElts = elts[2].split( "#" )
            self.code = codeElts[0]    
            if len(codeElts) > 1:
                self.comment = codeElts[1]

    def setNewData( self, data ):
        self.newData = data	
        self.hexa = ""
        for old,new in zip(self.binData,self.newData):
            if old == new:
                self.hexa += ('0'+hex(ord(new))[2:])[-2:]+ " "
            else:
                self.hexa += "<b>" + ('0'+hex(ord(new))[2:])[-2:]+ "</b> "

    def buildItems( self ):
        return [ LineItem(self,0), LineItem(self,1), LineItem(self,2), LineItem(self,3) ]


class Block(QStandardItem):
    def __init__( self, title ):
        super(QStandardItem, self).__init__(title)
        self.title = title
        self.lines = []
        self.offset = -1
        
    def addLine( self, line ):
        newLine = Line(line)
        self.lines.append( newLine )
        self.appendRow( newLine.buildItems() )
        
    def getData( self ):
        return "".join( [ l.binData for l in self.lines] )
		

class Section(QStandardItem):
    def __init__( self, title ):
        super(QStandardItem, self).__init__(title)
        self.title = title
        self.blocks = []
        
    def addBlock( self, title ):
        newBlock = Block( title )
        self.blocks.append( newBlock )
        self.appendRow( newBlock )
        
    def addBlockLine( self, line ):
        self.blocks[-1].addLine( line )

class TreeDump(QStandardItemModel):
    def __init__( self ):
        super(QStandardItemModel, self).__init__()
        self.title = ""
        self.sections = []
    
    def loadFile( self, filename ):
        self.clear()
        self.setHorizontalHeaderLabels(['Address', 'Hexa', 'Code', 'Comment'])
        self.sections = []
        
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
        self.appendRow( s )

        
        
