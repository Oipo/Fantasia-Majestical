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
        self._selectedProvince = None
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

            #self._provinces[dat[0]] = fmProv.Province(dat[0], img)
        #self._movement = {"Northwestia":("Southwestshire", "Northeastica"),
        #                  "Southwestshire":("Southeastland", "Northwestia"),
        #                  "Northeastica":("Southeastland", "Northwestia"),
        #                  "Southeastland":("Southwestshire", "Northeastica")}

        self.loadFromFile("province_data.txt")

        fmGlobals.glwidget.mousePress.connect(self.mapClicked)
        
    def debugInitMap(self):
        '''Moved here to prevent problems with initialization timing.'''
        self._tmpsov = fmPeople.Character(self.province("Grail"), "Test Sovereign")
        self._governments = {}

        gov = fmGov.Government(self, self.province("Grail"), self._tmpsov, self._tmpsov)
        self._governments["Empire of Grail"] = gov

        gov = fmGov.Government(self, self.province("Glimmer"), self._tmpsov, fmPeople.Character(self.province("Glimmer")))
        self._governments["Duchy of Glimmer"] = gov

        gov = fmGov.Government(self, self.province("Western Seneschals"), self._tmpsov, fmPeople.Character(self.province("Western Seneschals")))
        self._governments["Barony of Western Seneschals"] = gov

        gov = fmGov.Government(self, self.province("Eastern Seneschals"), self._tmpsov, fmPeople.Character(self.province("Eastern Seneschals")))
        self._governments["Barony of Eastern Seneschals"] = gov
        
        gov = fmGov.Government(self, self.province("Grail Coast"), self._tmpsov, fmPeople.Character(self.province("Grail Coast")))
        self._governments["Barony of Grail Coast"] = gov
        
        gov = fmGov.Government(self, self.province("Tolbank"), self._tmpsov, fmPeople.Character(self.province("Tolbank")))
        self._governments["Duchy of Tolbank"] = gov

        self._players = {"Test Player":fmPlayer.Player(self, self._tmpsov, self._governments["Empire of Grail"])}
        
    def loadFromFile(self, filename):
        '''Dubiously loads provinces from a province file.'''
        import traceback

        with open(filename) as f:
            provs = f.read().split("PROV")
            for prov in provs:
                try:
                    dat = prov.split("\n")
                    extracted = {"land":[], "sea":[]}
                    for line in dat:
                        if "$n" in line:
                            extracted["name"] = line[3:]
                        elif "$f" in line:
                            extracted["img"] = line[3:]
                        elif "$x" in line:
                            extracted["x"] = int(line[3:])
                        elif "$y" in line:
                            extracted["y"] = int(line[3:])
                        elif "$p" in line:
                            extracted["pop"] = int(line[3:])
                        elif "$g" in line:
                            extracted["goods"] = int(line[3:])
                        elif "$c" in line:
                            extracted["land"].append([int(line[3]), line[5:]])
                        elif "$s" in line:
                            extracted["sea"].append([int(line[3]), line[5:]])

                    if len(extracted.keys()) == 2:
                        continue

                    img = fmGlobals.glwidget.createImage('data/' + extracted["img"], 2, [0, 0, -1, -1], [extracted["x"], extracted["y"], -1, -1], True)

                    self._provinces[extracted["name"]] = fmProv.Province(initname = extracted["name"],
                                                                         image = img,
                                                                         initpop = extracted["pop"],
                                                                         initgoods = extracted["goods"],
                                                                         landroutes = extracted["land"],
                                                                         searoutes = extracted["sea"])
                except Exception as e:
                    print e.args
                    print traceback.format_exc()
                    pass
            
    def provinces(self):
        '''Returns a dict of all provinces on the map.'''
        return self._provinces
    
    def province(self, name):
        '''Returns the province with the given name.'''
        return self._provinces[name]
    
    #def movement(self, province):
    #    '''Returns possible targets of (land?) movement from a given province.'''
    #    return self._movement[province]

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

    def mapClicked(self, button, x, y):
        for p in self._provinces.values():
            r = p.displayOffset()

            if x >= r[0] and x <= r[0]+r[2] and y >= r[1] and y <= r[1]+r[3]:
                img = QImage(p.image().imagepath)
                if qAlpha(img.pixel(x-r[0], y-r[1])) == 0:
                    continue
                self.setSelectedProvince(p)
                fmGlobals.rsrcpanel.setSelectedProvince(p)
                break
                
    def setSelectedProvince(self, province):
        if self._selectedProvince != None:
            self._selectedProvince.image().hidden = True

        province.image().hidden = False
        self._selectedProvince = province

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
