# -*- coding: utf-8 -*-
#
#fmProv - Province code
#
#By Doctus (kirikayuumura.noir@gmail.com)

import random

class Province:
    
    def __init__(self, initname="Defaultaria", image=None, initpop=1000, inittax=5, initgoods=20, initunrest = 5, inittoltax = 5):
        self._name = initname
        self._population = initpop
        self._tax = inittax
        self._growthrate = 0.004
        self._growthvariance = [-0.001, 0, 0, 0.001]
        self._goodsvalue = initgoods
        self._unrest = initunrest
        self._toltax = inittoltax
        self._img = image
        
        #Even for a temporary militia, roughly 25% are too young to fight, 10% are too old, and 15% are otherwise physically incapable
        self._fightpop = initpop * 0.60
        
        #No more than around 6% of a typical medieval society can serve for an extended period without resulting in famine
        self._maxlevy = initpop * 0.06
        
        #Something like 2% can be raised for an army without significant difficulty (this one is rather variable though)
        self._normallevy = initpop * 0.02
        
    def name(self):
        '''Returns the province's name.'''
        return self._name
    
    def displayOffset(self):
        '''Returns the x, y coordinates of the province's image.'''
        return self._displayloc
    
    def image(self):
        '''Returns the filename of the province's map image.'''
        return self._img
        
    def population(self):
        '''Returns the province's current population.'''
        return int(self._population)
    
    def changePopulation(self, amount):
        '''For -1 < x < 1, changes province population by that percent. For other numbers, changes by that raw number.'''
        if amount > 1 or amount < -1:
            self._population += amount
        else:
            self._population += self._population * amount
    
    def taxRate(self):
        '''Returns the current tax rate (1 = 1%)'''
        return self._tax
    
    def setTaxRate(self, target):
        '''Sets the province tax rate (1 = 1%)'''
        self._tax = target
        
    def changeTaxRate(self, amount):
        '''Changes the province tax rate by amount (1 = 1%)'''
        self._tax += amount
    
    def fightingPopulation(self):
        '''Returns the number of people physically capable of fighting.'''
        return int(self._fightpop)
    
    def maxLevy(self):
        '''Returns the number of people capable of joining an army for some time without raising severe logistical problems.'''
        return int(self._maxlevy)
    
    def normalLevy(self):
        '''Returns the number of people capable of being recruited for the army with relative ease.'''
        return int(self._normallevy)
    
    def getTax(self):
        '''Returns the monthly tax amount.'''
        return int(self._population * self._tax / 100)
    
    def goodsValue(self):
        '''Returns the monthly value of goods produced in the province.'''
        return self._goodsvalue
    
    def recruit(self, number):
        '''Deducts an appropriate number of people from the province for military recruitment.'''
        self._population = max(0, self._population - number)
        self._fightpop = max(0, self._fightpop - number)
        self._maxlevy = max(0, self._maxlevy - number)
        self._normallevy = max(0, self._normallevy - number)
    
    def advanceMonth(self):
        '''Advances the province one month of game time.'''
        self._population += self._population*(self._growthrate+random.choice(self._growthvariance))
        
        #Let's be charitable for the sake of gameplay on these
        self._fightpop = min((self._fightpop + self._population * 0.01), self._population * 0.60)
        self._maxlevy = min((self._maxlevy + self._population * 0.001), self._population * 0.06)
        self._normallevy = min((self._normallevy + self._population * 0.00033), self._population * 0.02)
        
        if abs(self._tax - self._toltax) > 0.5:
            if self._tax > self._toltax:
                self._toltax += 0.05
                self._unrest += 0.25 + ((self._tax - self._toltax) * 0.25)
            elif self._tax < self._toltax:
                self._toltax -= 0.1
                self._unrest -= 0.125 + ((self._tax - self._toltax) * 0.125)
        else:
            self._toltax = self._tax
            if self._unrest > 10: self._unrest -= 0.1
        
    def getUnrestDescriptor(self):
        '''Returns a one-word description of the amount of unrest suitable for display to the player.'''
        if self._unrest <= 0:
            return "placid"
        elif self._unrest <= 10:
            return "calm"
        elif self._unrest <= 20:
            return "uneasy"
        elif self._unrest <= 40:
            return "troubled"
        elif self._unrest <= 70:
            return "violent"
        return "rebellious"
        
    def debugPrint(self):
        print "Data for Province " + self._name
        print "Population: " + str(self.population())
        print "Fighting Population: " + str(self.fightingPopulation())
        print "Maximum Levy: " + str(self.maxLevy())
        print "Normal Levy: " + str(self.normalLevy())
        print "Tax Rate: " + str(self.taxRate()) + "%"
        print "Monthly Tax: " + str(self.getTax())
        print "Monthly Goods Income: " + str(self.goodsValue())
        print "Unrest: " + self.getUnrestDescriptor() + " [" + str(self._unrest) + "]"
        print "[Tolerated Tax " + str(self._toltax) + "]"
        
    def debugAdvanceYear(self):
        for x in range(0, 12):
            self.advanceMonth()

