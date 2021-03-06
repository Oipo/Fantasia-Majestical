﻿# -*- coding: utf-8 -*-
#
#fmPlayer - Players! Human ones, maybe.
#
#By Doctus (kirikayuumura.noir@gmail.com)

class Player:
    
    def __init__(self, mappe, sovereign, startinggov, startingvassals = []):
        self._world = mappe
        self._sovereign = sovereign
        self._gov = startinggov
        self._vassals = startingvassals

        #debug
        from fmMap import WorldMap
        from fmPeople import Character
        from fmGov import Government

        if not isinstance(mappe, WorldMap):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(sovereign, Character):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(startinggov, Government):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)
        
    def treasury(self):
        '''Returns the player's government's treasury.'''
        return self._gov.treasury()
    
    def sovereign(self):
        '''Returns the player's sovereign.'''
        return self._sovereign
    
    def governedProvince(self):
        '''Returns the province name over which the player is exerting direct control.'''
        return self._gov.province()
    
    def vassals(self):
        '''Returns a list of the player's vassal governments.'''
        return self._vassals
    
    def addVassal(self, vass):
        '''Grants the player a new vassal.'''
        if vass not in self._vassals:
            self._vassals.append(vass)
            
    def removeVassal(self, vass):
        '''Removes one of the player's vassals from his or her dominion.'''
        if vass in self._vassals:
            self._vassals.remove(vass)
        
    def changeTreasury(self, amount):
        '''Change the player's government's treasury by amount.'''
        self._gov.changeTreasury(amount)
        
    def debugPrint(self):
        print "Player Treasury: " + str(self.treasury())
