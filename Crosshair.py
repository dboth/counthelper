from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class Crosshair(QLabel):
    def __init__(self, parent,name,position,relative=False):
        super(Crosshair, self).__init__(parent)
        self.name = name
        self.makeUI(position,relative)
		
    def makeUI(self, position,relative):
        self.setStyleSheet("border: none; background-color: none")
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setPixmap(QPixmap("images/kreis.png").scaled(self.size(), Qt.KeepAspectRatio ,Qt.SmoothTransformation))
        self.show()
        if not relative:
            ownSize = self.size()
            self.move(position.x()-ownSize.width()/2,position.y()-ownSize.height()/2)
            self.updatePosition()
        else:
            self.position = position
            self.refreshPosition()

    def delete(self):
        self.deleteLater()

    def sizeHint(self):
        return QSize(50,50)

    def mousePressEvent(self,event):
        self.parent().deleteMe(self.name)

    def getPoint(self):
        if not self.parent().pixmap:
            return None
        imageSize = self.parent().pixmap.size()
        return [self.position[0]*imageSize.width(),self.position[1]*imageSize.height()]

    def refreshPosition(self):
        if not self.parent().pixmap:
            return
        parentSize = self.parent().size()
        imageSize = self.parent().pixmap.size()
        ownSize = self.size()
        imageAspectRatio = imageSize.width()/imageSize.height()
        if (parentSize.width()/parentSize.height()) >= imageAspectRatio:
            realImageHeight = parentSize.height()
            realImageWidth = realImageHeight * imageAspectRatio
            imageX = (parentSize.width()-realImageWidth)/2
            imageY = 0
        else:
            realImageWidth = parentSize.width()
            realImageHeight = realImageWidth / imageAspectRatio
            imageX = 0
            imageY = (parentSize.height()-realImageHeight)/2
        self.move(int(imageX+self.position[0]*realImageWidth-ownSize.width()/2),int(imageY+self.position[1]*realImageHeight-ownSize.height()/2))
        

    def updatePosition(self):
        ownSize = self.size()
        parentSize = self.parent().size()
        imageSize = self.parent().pixmap.size()
        imageAspectRatio = imageSize.width()/imageSize.height()
        if (parentSize.width()/parentSize.height()) >= imageAspectRatio:
            realImageHeight = parentSize.height()
            realImageWidth = realImageHeight * imageAspectRatio
            imageX = (parentSize.width()-realImageWidth)/2
            imageY = 0
        else:
            realImageWidth = parentSize.width()
            realImageHeight = realImageWidth / imageAspectRatio
            imageX = 0
            imageY = (parentSize.height()-realImageHeight)/2
        x = max(0,min(1,(self.x()+ownSize.width()/2-imageX)/realImageWidth))
        y = max(0,min(1,(self.y()+ownSize.height()/2-imageY)/realImageHeight))
        self.position = (x,y)
        
