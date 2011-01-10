# -*- coding: utf-8 -*-
#
#main - starting point of FM （゜ω゜）ｂ
#
#By Oipo (kingoipo@gmail.com)

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import *
from fmMap import *
from fmRsrcPanel import *
import fmGlobals

if fmGlobals.musicOn:
    from PyQt4.phonon import *
    from fmMusPanel import *

class MainWindow(QMainWindow):
    '''Wrapper class for...well, the game? Maybe this needs to be called the game engine then'''

    def __init__(self):
        '''
        Only initialize critical components(like opengl) here, use start() for anything else
        '''
        QMainWindow.__init__(self)

        fmGlobals.glwidget = GLWidget(self)
        self.setCentralWidget(fmGlobals.glwidget)
        fmGlobals.glwidget.makeCurrent() 
        
        if fmGlobals.musicOn:
            fmGlobals.mediaobject = Phonon.MediaObject(self)
            self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
            Phonon.createPath(fmGlobals.mediaobject, self.audioOutput)

        self.drawTimer = QTimer()
        self.drawTimer.timeout.connect(self.drawTimerTimeout)
        self.drawTimer.start(13)
        
        self.monthTimer = QTimer()
        self.monthTimer.timeout.connect(self.monthTimerTimeout)
        self.monthTimer.start(2000)

    def start(self):
        fmGlobals.worldmap = WorldMap()
        fmGlobals.rsrcpanel = RsrcPanel(self)
        if fmGlobals.musicOn:
            fmGlobals.muspanel = MusPanel(self)

    def drawTimerTimeout(self):
        fmGlobals.glwidget.updateGL()
        
    def monthTimerTimeout(self):
        fmGlobals.worldmap.advanceMonth()

if __name__ == '__main__':
    app = QApplication(['Fantasia Majestical'])
    window = MainWindow()
    window.show()
    window.start()
    app.exec_()
