# -*- coding: utf-8 -*-
#
#fmMap - World map code
#
#By Doctus (kirikayuumura.noir@gmail.com)

import fmProv, fmGlobals, fmPeople, fmGov, fmPlayer

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class WorldMap(QObject):

    updateSlot = pyqtSignal()
    
    def __init__(self):
        QObject.__init__(self)
        self._provinces = {}
        self._month = 0

        for dat in [["oceantopleft", (0, 0), 'oceantopleft.png'], 
                    ["oceanbottomleft", (0, 1000), 'oceanbottomleft.png'],
                    ["oceanbottomright", (1000, 1000), 'oceanbottomright.png'],
                    ["oceantopright", (1000, 0), 'oceantopright.png']]:
            qimg = QImage('data/' + dat[2])
            img = fmGlobals.glwidget.createImage(qimg, -2, (0, 0, qimg.width(), qimg.height()), (dat[1][0], dat[1][1], qimg.width(), qimg.height()))

        for dat in [["Northwestia", (0, 0), 'landtopleft.png'], 
                    ["Southeastland", (0, 1000), 'landbottomleft.png'],
                    ["Southwestshire", (1000, 1000), 'landbottomright.png'],
                    ["Northeastica", (1000, 0), 'landtopright.png']]:
            qimg = QImage('data/' + dat[2])
            img = fmGlobals.glwidget.createImage(qimg, -1, (0, 0, qimg.width(), qimg.height()), (dat[1][0], dat[1][1], qimg.width(), qimg.height()))
            self._provinces[dat[0]] = fmProv.Province(dat[0], img)
        self._movement = {"Northwestia":("Southwestshire", "Northeastica"),
                          "Southwestshire":("Southeastland", "Northwestia"),
                          "Northeastica":("Southeastland", "Northwestia"),
                          "Southeastland":("Southwestshire", "Northeastica")}

        #semi-debug stuff----
        self._tmpsov = fmPeople.Character("Test Sovereign")
        self._governments = {"Duchy of Northwestia":fmGov.Government(self, "Northwestia", self._tmpsov)}                  
        self._players = {"Test Player":fmPlayer.Player(self, self._tmpsov, self._governments["Duchy of Northwestia"])}
        #--------------------
                          
    def provinces(self):
        '''Returns a dict of all provinces on the map.'''
        return self._provinces
    
    def province(self, name):
        '''Returns the province with the given name.'''
        return self._provinces[name]
    
    def movement(self, province):
        '''Returns possible targets of (land?) movement from a given province.'''
        return self._movement[province]
    
    def canMove(self, provinceone, provincetwo):
        '''Returns whether movement is possible from a first province to a second.'''
        return provincetwo in self._movement[provinceone]

    def advanceMonth(self):
        '''Advances the entire world one month of game time.'''
        self._month += 1
        for gov in self._governments.values():
            gov.collectTax()
            gov.collectProduction()
        for prov in self._provinces.values():
            prov.advanceMonth()
        
        print "Month " + str(self._month)
        self._players["Test Player"].debugPrint()
        self.province("Northwestia").debugPrint()

        self.updateSlot.emit()
