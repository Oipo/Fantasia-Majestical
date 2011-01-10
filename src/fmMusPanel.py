import os, random

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *

import fmGlobals

class fileItem(QListWidgetItem):

    def __init__(self, file, dir, panel):
        QListWidgetItem.__init__(self)
        self.file = file
        self.dir = dir
        
        self.setText(file[5:len(file)-3])
        
class musicListWidget(QListWidget):

    def __init__(self, panel):
        QListWidget.__init__(self)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.panel = panel

class MusPanel(QDockWidget):
    '''Music Panel, shows the available music and allows the player to control it'''

    def __init__(self, mainWindow):
        super(QDockWidget, self).__init__(mainWindow)

        self.next = None
        self.contents = QWidget(self)
        self.musicList = musicListWidget(self)
        self.play = QPushButton("Play")
        self.stop = QPushButton("Stop")
        self.pause = QPushButton("Pause")
        self.shuffle = QCheckBox("Shuffle")
        
        self.addFilesInDir("music")
        
        x = 0
        grid = QGridLayout()

        grid.addWidget(self.musicList, x, 0, 1, 3)
        x += 1
        
        grid.addWidget(Phonon.SeekSlider(fmGlobals.mediaobject), x, 0, 1, 3)
        x += 1
        
        grid.addWidget(self.play, x, 0)
        grid.addWidget(self.stop, x, 1)
        grid.addWidget(self.pause, x, 2)
        x += 1
        
        grid.addWidget(self.shuffle, x, 0)
        x += 1

        self.contents.setLayout(grid)
        
        self.play.clicked.connect(self.playClicked)
        self.stop.clicked.connect(self.stopClicked)
        self.pause.clicked.connect(self.pauseClicked)
        fmGlobals.mediaobject.aboutToFinish.connect(self.enqueueNext)
        fmGlobals.mediaobject.currentSourceChanged.connect(self.updateList)
        
        self.setWindowTitle("Music Panel")
        self.setWidget(self.contents)
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

    def addFilesInDir(self, dir):
        fdir = os.listdir(dir)
        
        for file in fdir:
            if os.path.isdir(dir + '/' + file):
                self.addFilesInDir(dir + '/' + file)

        for file in fdir:
            if file[-3:] == "mp3":
                self.musicList.addItem(fileItem(file, dir, self))

    def updateList(self):
        if self.next != None:
            self.musicList.setCurrentItem(self.next)
        
    def enqueueNext(self):
        if self.shuffle.isChecked():
            rand = self.musicList.currentRow()
            count = self.musicList.count()
            
            while rand == self.musicList.currentRow() and count > 1:
                rand = random.randint(0, count-1)

            item = self.musicList.item(rand)
            fmGlobals.mediaobject.enqueue(Phonon.MediaSource(item.dir + '/' + item.file))
        else:
            count = self.musicList.count()
            currentrow = self.musicList.currentRow()
            next = 0
            
            if currentrow + 1 < count:
                next = currentrow + 1
            
            item = self.musicList.item(next)
            fmGlobals.mediaobject.enqueue(Phonon.MediaSource(item.dir + '/' + item.file))
            
        self.next = item
            
    def playClicked(self, checked):
        item = self.musicList.item(self.musicList.currentRow())
        
        if fmGlobals.mediaobject.state() == Phonon.PausedState:
            fmGlobals.mediaobject.play()
            return
        
        fmGlobals.mediaobject.setCurrentSource(Phonon.MediaSource(item.dir + '/' + item.file))
        
        if fmGlobals.mediaobject.state() != Phonon.PlayingState:
            fmGlobals.mediaobject.play()
            
    def stopClicked(self, checked):
        fmGlobals.mediaobject.stop()
    
    def pauseClicked(self, checked):
        if fmGlobals.mediaobject.state() == Phonon.PausedState:
            fmGlobals.mediaobject.play()
        if fmGlobals.mediaobject.state() == Phonon.PlayingState:
            fmGlobals.mediaobject.pause()