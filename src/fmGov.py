# -*- coding: utf-8 -*-
#
#fmGov - Provincial governments
#
#By Doctus (kirikayuumura.noir@gmail.com)

class Government:
    
    def __init__(self, mappe, startingprovincename, leader, startingtreasury=500):
        self._world = mappe
        self._province = startingprovincename
        self._leader = leader
        self._treasury = startingtreasury
        self._world.province(self._province).setGovernment(self)
        
    def treasury(self):
        '''Returns the current treasury value.'''
        return self._treasury
    
    def province(self):
        '''Returns the province name of which this is currently the government.'''
        return self._province
    
    def getLeader(self):
        '''Returns the character who leads the provincial government.'''
        return self._leader
        
    def changeTreasury(self, amount):
        '''Change the treasury by amount.'''
        self._treasury += amount
        
    def collectTax(self):
        '''Collect current monthly tax in the province.'''
        self.changeTreasury(self._world.province(self._province).getTax())
            
    def collectProduction(self):
        '''Collect current monthly goods value in the province.'''
        self.changeTreasury(self._world.province(self._province).goodsValue())
        
    def changeProvince(self, newprovname):
        '''Moves the government to a new province.'''
        if self._province:
            self._province.setGovernment(None)
        self._province = newprovname
        self._world.province(self._province).setGovernment(self)