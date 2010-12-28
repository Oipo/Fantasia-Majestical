# -*- coding: utf-8 -*-
#
#fmMap - World map code
#
#By Doctus (kirikayuumura.noir@gmail.com)

import fmProv

class WorldMap:
    
    def __init__(self):
        self._provinces = {}
        for dat in [["Northwestia", (0, 0), 'land_topleft.png'], 
                    ["Southeastland", (0, 1000), 'land_bottomleft.png'],
                    ["Southwestshire", (1000, 1000), 'land_bottomright.png'],
                    ["Northeastica", (1000, 0), 'land_topright.png']]:
            self._provinces[dat[0]] = fmProv.Province(dat[0], dat[1], dat[2])
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