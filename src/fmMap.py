# -*- coding: utf-8 -*-
#
#fmMap - World map code
#
#By Doctus (kirikayuumura.noir@gmail.com)

import fmProv
import fmGlobals

from PyQt4.QtGui import *

class WorldMap:
    
    def __init__(self):
        self._provinces = {}
        for dat in [["Northwestia", (0, 0), 'landtopleft.png'], 
                    ["Southeastland", (0, 1000), 'landbottomleft.png'],
                    ["Southwestshire", (1000, 1000), 'landbottomright.png'],
                    ["Northeastica", (1000, 0), 'landtopright.png']]:
            qimg = QImage('data/' + dat[2])
            img = fmGlobals.glwidget.createImage(qimg, (0, 0, qimg.width(), qimg.height()), (dat[1][0], dat[1][1], qimg.width(), qimg.height()))
            self._provinces[dat[0]] = fmProv.Province(dat[0], img)
        self._movement = {"Northwestia":("Southwestshire", "Northeastica"),
                          "Southwestshire":("Southeastland", "Northwestia"),
                          "Northeastica":("Southeastland", "Northwestia"),
                          "Southeastland":("Southwestshire", "Northeastica")}
                          
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
