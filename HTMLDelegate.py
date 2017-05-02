from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class HTMLDelegate(QStyledItemDelegate):
    def __init__(self):
        super(QStyledItemDelegate, self).__init__()

    def paint( self, painter, option, index ):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        painter.save()

        doc = QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        options.widget.style().drawControl(QStyle.CE_ItemViewItem, options, painter)

        painter.translate(options.rect.left(), options.rect.top())
        clip = QRectF(0, 0, options.rect.width(), options.rect.height())
        doc.drawContents(painter, clip)

        painter.restore()
    
    def sizeHint( self, option, index ):
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QSize( doc.idealWidth(), doc.size().height() )

