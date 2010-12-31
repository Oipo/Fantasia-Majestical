# -*- coding: utf-8 -*-
#
#fmPeople - Characters, personae, etc
#
#By Doctus (kirikayuumura.noir@gmail.com)

import fmNameGen, random

def _rstat():
    return min(100, max(0, random.gauss(50, 12)))

class Relationship:
    
    def __init__(self, origin, target, affection=None, loyalty=None):
        self._origin = origin
        self._target = target
        if affection:
            self._affection = affection
        else:
            self._affection = 50
        if loyalty:
            self._loyalty = loyalty
        else:
            self._loyalty = 50

        #debug
        import sys

        if not isinstance(origin, Character):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

        if not isinstance(target, Character):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)
        
    def origin(self):
        '''The source of the thoughts and feelings.'''
        return self._origin
    
    def target(self):
        '''The one about whom the thoughts and feelings are.'''
        return self._target
    
    def affection(self):
        '''Returns affection on a scale of 0 (hate) to 100 (love).'''
        return self._affection
    
    def loyalty(self):
        '''Returns loyalty on a scale of 0 (none) to 100 (devotion).'''
        return self._loyalty
    
    def setAffection(self, new):
        self._affection = new
        
    def setLoyalty(self, new):
        self._loyalty = new
        
    def changeAffection(self, amount):
        self._affection = min(100, max(0, self._affection + amount))
        
    def changeLoyalty(self, amount):
        self._loyalty = min(100, max(0, self._loyalty + amount))
        
    def setFeelings(self, affection=None, loyalty=None):
        if affection: self.setAffection(affection)
        if loyalty: self.setLoyalty(loyalty)

    def changeFeelings(self, affection=None, loyalty=None):
        if affection: self.changeAffection(affection)
        if loyalty: self.changeLoyalty(loyalty)

class Character:
    
    def __init__(self, name="random"):
        if name == "random":
            self._name = fmNameGen.getName("japanese")
        else:
            self._name = name
        self._mainPersona = Persona(self._name, {self._name:self})
        self._currentPersona = self._mainPersona
        self._alts = {self._name:self._mainPersona}
        self._relationships = {}
        self._stats = {}
        for stat in ["courage", "temperance", "fortitude", "compassion",
                     "piety", "industriousness", "pride", "charm",
                     "cleverness", "analysis", "intuition", "determination",
                     "combat", "stealth", "etiquette", "refinement",
                     "morality", "tolerance", "cooking", "constitution",
                     "magic", "musicality", "administration", "perspicacity",
                     "wheedling", "disguise", "strategy", "tactics",
                     "history", "language", "accounting", "gravity",
                     "greed", "irascibility", "introspection", "ambition",
                     "curiousity", "cheerfulness", "humour", "foresight",
                     "poisons", "lockpicking", "equestrian", "sociability",
                     "crafting", "misdirection", "mining", "architecture",
                     "lying", "lore", "gluttony", "patience", "wit",
                     "narcissism", "leadership"]:
                         self._stats[stat] = _rstat()
        
    def name(self):
        '''Returns the character's actual internal name.'''
        return self._name
    
    def stat(self, statname):
        '''Returns the character's value in a given statistic.'''
        return self._stats[statname]
    
    def hasPersona(self, name):
        '''Returns whether the passed name is one of the character's.'''
        return self._alts.has_key(name)
    
    def createPersona(self, name):
        '''Creates an entirely new persona for this character.'''
        self._alts[name] = Persona(name, {self._name:self})
        
    def addPersona(self, persona):
        '''Adds an existing persona to the list of this character's alts.'''
        self._alts[persona.name()] = persona
        persona.addOwner(self)
        
    def setPersona(self, name):
        '''Sets the character's persona to the one with the specified name.'''
        self._currentPersona = self._alts[name]
        
    def currentPersona(self):
        '''Gets the character's currently portrayed persona.'''
        return self._currentPesona
    
    def setRelationship(self, target, affection=None, loyalty=None):
        '''Sets the relationship with the target persona to the specified value(s).'''
        if not self._relationships.has_key(target.name()):
            self._relationships[target.name()] = Relationship(self.name(), target.name(), affection, loyalty)
        else:
            self._relationships[target.name()].setFeelings(affection, loyalty)
            
    def modRelationship(self, target, affection=None, loyalty=None):
        '''Alters the relationship with the target persona by the specified value(s).'''
        if not self._relationships.has_key(target.name()):
            self._relationships[target.name()] = Relationship(self.name(), target.name())
        self._relationships[target.name()].changeFeelings(affection, loyalty)
        
    def getRelationship(self, name):
        '''Returns the relationship object matching the name provided.'''
        return self._relationships[name]

    def manageGovernment(self, gov):
        if gov.getGovernor() != self:
            return

        p = gov.province()

        if p.getUnrestDescList().index(p.getUnrestDescriptor()) <= p.getUnrestDescList().index(gov.order().unrest.lower()):
            if p.taxRate() < gov.order().tax:
                p.changeTaxRate(0.4)
            elif p.taxRate() > gov.order().tax:
                p.changeTaxRate(-0.4)
                
        
class Persona:
    
    def __init__(self, name="random", owner={}):
        if name == "random":
            self._name = fmNameGen.getName("japanese")
        else:
            self._name = name
        self._owners = owner
            
    def name(self):
        '''Returns the persona's name.'''
        return self._name
    
    def isOwner(self, name):
        '''Returns whether the given name is a character associated with this persona.'''
        return self._owners.has_key(name)
    
    def addOwner(self, owner):
        '''Adds an owner to this persona.'''
        self.owners[owner.name()] = owner
