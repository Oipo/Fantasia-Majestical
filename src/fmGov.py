# -*- coding: utf-8 -*-
#
#fmGov - Provincial governments
#
#By Doctus (kirikayuumura.noir@gmail.com)

class Order:

    def __init__(self, tax, unrest):
        self.tax = tax
        self.unrest = unrest

class OrderRequest:

    def __init__(self, originatinggovernment, targetgovernment, order):
        self.origin = originatinggovernment
        self.target = targetgovernment
        self.current = originatinggovernment
        self.order = order
        self.route = []

        self.calculateRoute()

        #debug
        import sys

        if not isinstance(originatinggovernment, Government):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(targetgovernment, Government):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(order, Order):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

    def calculateRoute(self):
        self.route = [self.target, self.origin] #this list is in reverse order. That is, [0] is the end, [len(self)] is the start

    def advanceMonth(self):
        self.current = self.route.pop()

        if self.current == self.target:
            self.target.setOrder(self.order)
            
    def done(self):
        '''So that outside classes can determine whether to garbage collect this class'''
        return (self.current == self.target)

class Government:
    
    def __init__(self, mappe, startingprovince, leader, governor, order = None, startingtreasury=500):
        self._world = mappe
        self._province = startingprovince
        self._leader = leader
        self._governor = governor
        self._treasury = startingtreasury
        self._province.setGovernment(self)
        self._order = order

        if order == None:
            self._order = Order(5, "Calm")

        #debug
        import sys
        from fmMap import WorldMap
        from fmPeople import Character
        from fmPlayer import Player
        from fmProv import Province

        if not isinstance(mappe, WorldMap):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(leader, Character):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(governor, Character):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(startingprovince, Province):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(self._order, Order):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)
        
    def treasury(self):
        '''Returns the current treasury value.'''
        return self._treasury
    
    def province(self):
        '''Returns the province name of which this is currently the government.'''
        return self._province

    def order(self):
        '''Returns the currently set Order for this government'''
        return self._order
    
    def getLeader(self):
        '''Returns the character who leads the provincial government.'''
        return self._leader

    def getGovernor(self):
        '''Returns the managing governer. Can be the same as leader.'''
        return self._governor
        
    def changeTreasury(self, amount):
        '''Change the treasury by amount.'''
        self._treasury += amount
        
    def collectTax(self):
        '''Collect current monthly tax in the province.'''
        self.changeTreasury(self._province.getTax())
            
    def collectProduction(self):
        '''Collect current monthly goods value in the province.'''
        self.changeTreasury(self._province.goodsValue())
        
    def changeProvince(self, newprov):
        '''Moves the government to a new province.'''
        if self._province:
            self._province.setGovernment(None)
        self._province = newprovname
        self._province.setGovernment(self)

    def setOrder(self, order):
        self._order = order
