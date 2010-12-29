from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import *
from fmMap import *
import fmGlobals

class MainWindow(QMainWindow):
    ''' Example class for using SpiralWidget'''
    
    def __init__(self):
        QMainWindow.__init__(self)
        fmGlobals.glwidget = GLWidget(self)   

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerTimeout)
        self.timer.start(13)
        
        self.monthTimer = QTimer()
        self.monthTimer.timeout.connect(self.monthTimerTimeout)
        self.monthTimer.start(2000)

        self.setCentralWidget(fmGlobals.glwidget)
        fmGlobals.glwidget.makeCurrent()

    def start(self):

        fmGlobals.worldmap = WorldMap() 

    def timerTimeout(self):
        fmGlobals.glwidget.updateGL()
        
    def monthTimerTimeout(self):
        fmGlobals.worldmap.advanceMonth()

if __name__ == '__main__':
    app = QApplication(['Fantasia Majestical'])
    window = MainWindow()
    window.show()
    window.start()
    app.exec_()
