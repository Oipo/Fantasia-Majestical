# -*- coding: utf-8 -*-
#
#fmMil - Military stuff
#
#By Doctus (kirikayuumura.noir@gmail.com)

import random

class Regiment:
    
    def __init__(self, size, commander, initlocname, morale=20, training=5):
        self._size = size
        self._commander = commander
        self._morale = morale
        self._training = training
        self._province = initlocname
        
    def commander(self):
        '''Returns the commander of the regiment.'''
        return self._commander
    
    def size(self):
        '''Returns the number of soldiers in the regiment.'''
        return self._size
    
    def morale(self):
        '''Returns the internal representation of regimental morale.'''
        return self._morale
    
    def training(self):
        '''Returns the internal representation of regimental training.'''
        return self._training
    
    def location(self):
        '''Returns the name of the unit's current location.'''
        return self._province
    
    def getMoraleDescriptor(self):
        '''Returns a one-word description of the regiment's morale suitable for display to the player.'''
        if self._morale <= 0:
            return "broken"
        elif self._morale <= 5:
            return "near breaking"
        elif self._morale <= 10:
            return "demoralized"
        elif self._morale <= 15:
            return "disgruntled"
        elif self._morale <= 25:
            return "typical"
        elif self._morale <= 35:
            return "contented"
        elif self._morale <= 55:
            return "motivated"
        elif self._morale <= 75:
            return "zealous"
        return "fervent"
    
    def getTrainingDescriptor(self):
        '''Returns a one-word description of the regiment's training suitable for display to the player.'''
        if self._training <= 10:
            return "green"
        elif self._training <= 20:
            return "disciplined"
        elif self._training <= 35:
            return "regular"
        elif self._training <= 50:
            return "veteran"
        elif self._training <= 70:
            return "exceptional"
        return "elite"
    
    def move(self, newname):
        '''Moves the unit to a new province.'''
        self._province = newname
    
    def changeSize(self, amount):
        '''Changes the number of soldiers in the unit *without* affecting training/morale.'''
        self._size += amount
    
    def addTroops(self, amount, recruitsmorale=20, recruitstraining=5):
        '''Changes the number of soldiers in the unit, *affecting* training/morale.'''
        relsize = self._size / amount
        self._morale = ((self._morale * relsize) + recruitsmorale) / (1+relsize)
        self._training = ((self._training * relsize) + recruitstraining) / (1+relsize)
        self._size += amount
        
    def changeMorale(self, amount):
        '''Changes the unit's morale by the specified amount.'''
        self._morale += amount
        
    def changeTraining(self, amount):
        '''Changes the unit's training by the specified amount.'''
        self._training += amount
        
    def changeCommander(self, new):
        '''Gives the unit a new commander.'''
        self._commander = new
        
    def drill(self):
        '''Gives the unit the benefits of one month of drilling.'''
        #Not yet fully implemented
        self._training += (random.randint(0, 4)# +
                            #self._commander.relevant_military_skill
                            #self._province.relevant_bonuses
                            #self._other_misc_bonuses
                            )
        self._morale += (random.randint(0, 4)# +
                            #self._commander.relevant_military_skill
                            #self._province.relevant_bonuses
                            #self._other_misc_bonuses
                            )