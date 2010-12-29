from PyQt4.QtCore import *
from PyQt4.QtGui import *

from glwidget import *
from fmMap import *
import fmGlobals

class MainWindow(QMainWindow):
    '''Wrapper class for...well, the game? Maybe this needs to be called the game engine then'''
    
    def __init__(self):
        '''
        Only initialize critical components(like opengl) here, use start() for anything else
        '''
        QMainWindow.__init__(self)
        fmGlobals.glwidget = GLWidget(self)   

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerTimeout)
        self.timer.start(13)

        self.setCentralWidget(fmGlobals.glwidget)
        fmGlobals.glwidget.makeCurrent()

    def start(self):
        fmGlobals.worldmap = WorldMap() 

    def timerTimeout(self):
        fmGlobals.glwidget.updateGL()

if __name__ == '__main__':
    app = QApplication(['Fantasia Majestical'])
    window = MainWindow()
    window.show()
    window.start()
    app.exec_()
