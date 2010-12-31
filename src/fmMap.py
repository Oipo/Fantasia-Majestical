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
        self._orders = []

        for dat in [["oceantopleft", (0, 0), 'oceantopleft.png'], 
                    ["oceanbottomleft", (0, 1000), 'oceanbottomleft.png'],
                    ["oceanbottomright", (1000, 1000), 'oceanbottomright.png'],
                    ["oceantopright", (1000, 0), 'oceantopright.png']]:
            qimg = 'data/' + dat[2]
            img = fmGlobals.glwidget.createImage(qimg, -2, (0, 0, 1000, 1000), (dat[1][0], dat[1][1], 1000, 1000))

        for dat in [["Northwestia", (0, 0), 'landtopleft.png'], 
                    ["Southeastland", (0, 1000), 'landbottomleft.png'],
                    ["Southwestshire", (1000, 1000), 'landbottomright.png'],
                    ["Northeastica", (1000, 0), 'landtopright.png']]:
            qimg = 'data/' + dat[2]
            img = fmGlobals.glwidget.createImage(qimg, -1, (0, 0, 1000, 1000), (dat[1][0], dat[1][1], 1000, 1000))
            self._provinces[dat[0]] = fmProv.Province(dat[0], img)
        self._movement = {"Northwestia":("Southwestshire", "Northeastica"),
                          "Southwestshire":("Southeastland", "Northwestia"),
                          "Northeastica":("Southeastland", "Northwestia"),
                          "Southeastland":("Southwestshire", "Northeastica")}

        #semi-debug stuff----
        self._tmpsov = fmPeople.Character("Test Sovereign")
        self._AIsov = fmPeople.Character("AI Sovereign")
        self._governments = {}

        gov = fmGov.Government(self, self.province("Northwestia"), self._tmpsov, self._tmpsov)
        self._governments["Duchy of Northwestia"] = gov

        gov = fmGov.Government(self, self.province("Southwestshire"), self._tmpsov, self._AIsov)
        self._governments["Duchy of Southwestshire"] = gov

        gov = fmGov.Government(self, self.province("Northeastica"), self._tmpsov, self._AIsov)
        self._governments["Duchy of Northeastica"] = gov

        gov = fmGov.Government(self, self.province("Southeastland"), self._tmpsov, self._AIsov)
        self._governments["Duchy of Southeastland"] = gov

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

    def getHumanPlayer(self):
        '''Obviously this needs to be done properly.'''
        return self._players["Test Player"]

    def getPlayerProvinces(self, player):
        '''Returns all provinces which directly or indirectly are owned by player'''
        provinces = []

        for province in self._provinces:
            if province.getLeader() == player:
                provinces.append(province)

        return provinces

    def getCharacterProvince(self, character):
        '''Returns the province which is directly governed by character'''
        for province in self._provinces.values():
            gov = province.government()
            if gov and gov.getGovernor() == character:
                return province

    def canMove(self, provinceone, provincetwo):
        '''Returns whether movement is possible from a first province to a second.'''
        return provincetwo in self._movement[provinceone]

    def addOrderRequestToQueue(self, order):
        '''Add an order to the list of orders which are yet to arrive at their destination.
           That is not to say that these could be corrupted, and their routes changed. No one knows!'''
        self._orders.append(order)

    def advanceMonth(self):
        '''Advances the entire world one month of game time.'''
        self._month += 1

        deletedOrders = []
        for order in self._orders:
            order.advanceMonth()
            if order.done():
                deletedOrders.append(order)

        while len(deletedOrders) > 0:
            self._orders.remove(deletedOrders.pop())

        for gov in self._governments.values():
            gov.collectTax()
            gov.collectProduction()

            gov.getGovernor().manageGovernment(gov)
        for prov in self._provinces.values():
            prov.advanceMonth()

        self.updateSlot.emit()
