import os
import subprocess
import sys
import tempfile

from PyQt5.QtGui import *

def updateString( chaine, pos, car ):
    if pos == 0:
        return car + chaine[1:]
    elif pos == len(chaine) - 1:
        return chaine[:-1] + car
    else:
        return chaine[:pos] + car + chaine[pos+1:]

class LineItem(QStandardItem):
    def __init__( self, data, col ):
        super(QStandardItem, self).__init__()
        self.data = data
        self.col = col
        if col == 0:
            self.setText( data.addr )
        elif col == 1:
            self.setText( data.hexa )
        elif col == 2:
            result = data.code.replace("<", "&lt;" )
            self.setText( result )
        else:
            result = data.comment.replace("<", "&lt;" )
            self.setText( result )

    def updateLine( self ):
        if self.col == 0:
            self.setText( self.data.addr )
        elif self.col == 1:
            self.setText( self.data.hexa )
        elif self.col == 2:
            self.setText( self.data.code )
        else:
            self.setText( self.data.comment )

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
        isDiff = False
        for old,new in zip(self.binData,self.newData):
            if old == new:
                self.hexa += ('0'+hex(ord(new))[2:])[-2:]+ " "
            else:
                self.hexa += "<b>" + ('0'+hex(ord(new))[2:])[-2:]+ "</b> "
                isDiff = True
        if isDiff:
            self.code = "<i>" + self.code + "</i>"
        for item in self.items:
            item.updateLine()

    def getRawHexa( self ):
        ret = ""
        for elt in self.newData:
            ret  += ('0'+hex(ord(elt))[2:])[-2:]+ " "
        return ret

    def buildItems( self ):
        self.items = [ LineItem(self,0), LineItem(self,1), LineItem(self,2), LineItem(self,3) ]
        return self.items
        
    def isModified( self ):
        return self.newData != self.binData


class Block(QStandardItem):
    def __init__( self, title ):
        result = title.replace("<", "&lt;" )
        super(QStandardItem, self).__init__(result)
        self.title = result
        self.lines = []
        self.offset = -1
        
    def addLine( self, line ):
        newLine = Line(line)
        self.lines.append( newLine )
        self.appendRow( newLine.buildItems() )
        
    def getData( self ):
        return "".join( [ l.binData for l in self.lines] )
        
    def getCurrentData( self ):
        return "".join( [ l.newData for l in self.lines] )
        
    def isModified( self ):
        for line in self.lines:
            if line.isModified():
                return True
        return False
		

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
    def __init__( self, commandBuilder ):
        super(QStandardItemModel, self).__init__()
        self.title = ""
        self.sections = []
        self.commandBuilder = commandBuilder
    
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
        tempFilename = tempfile.mktemp()
        os.system( self.commandBuilder.getParseCommand(filename) + " > " + tempFilename )
        
        
        with open( tempFilename, "r" ) as fic:
            data = fic.read().split( "\n" )
        
        os.system( "rm " + tempFilename )
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
                        
    def saveFile( self, filename ):
        self.updateBinaryData()
        with open( filename, "wb" ) as fic:
            if sys.version_info.major == 3:
                fic.write( self.binData.encode('ISO-8859-1') )
            else:
                fic.write( self.binData )
    
    def updateBinaryData( self ):
        for section in self.sections:
            for block in section.blocks:
                if block.isModified():
                    for pos,car in enumerate(block.getCurrentData()):
                        self.binData = updateString( self.binData, block.offset + pos, car )
    
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

        
        
