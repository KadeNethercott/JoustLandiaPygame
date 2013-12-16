#!usr/bin/python

import random, time, pygame, copy, sys
from pygame.locals import *



class City:

    def __init__(self, cName, knights, citySize, joustImage):
        self.knights = knights
        self.name = cName
        self.size = citySize
        self.joustImage = joustImage
        
    
    def getKnights(self, playerProgress):
        self.defeated = []
        self.undefeated = []
        for n in range(0,playerProgress):
            self.defeated.append(self.knights[n])
            
        for n in range(playerProgress, len(self.knights)):
            self.undefeated.append(self.knights[n])
            
        self.twoLists = [self.defeated, self.undefeated]
        return self.twoLists

    def getName(self):
        return self.name
    def getSize(self):
        return self.size
    def getJoustImage(self):
        return self.joustImage
    
class Equipment:

    def __init__(self, equipoName, equipoStrength, value, equipoType):
        self.name = equipoName
        self.strength = equipoStrength
        self.purchased = False
        self.price = value
        self.type = equipoType

    def getName(self):
        return self.name
    
    def getStrength(self):
        return self.strength
    
    def getPrice(self):
        return self.price
    
    def purchase(self):
        self.purchased = True
        return self.strength

    def isPurchased(self):
        return self.purchased

    def getType(self):
        return self.type

class Lance:

    def __init__(self, name, strength, value):
        self.lanceName = name
        self.lanceStrength = strength
        self.purchased = False
        self.price = value

    def getName(self):
        return self.name
    
    def getStrength(self):
        return self.strength
    
    def getPrice(self):
        return self.price
    
    def purchase(self):
        self.purchased = True
        return self.lanceStrength
        

    def isPurchased(self):
        return self.purchased

class BlackSmith:

    def __init__(self, shields, lances):
        self.shieldList = shields
        self.lanceList = lance

    def getShields(self):
        return shields

    def getLances(self):
        return lances
    
        
    
        
class Player:
   
    def __init__(self, pName):
        self.name= pName
        self.progress = {'Isengard': 0,
                         'Yorkshire':0,
                         'Norfolk': 0}
        self.coins = 0
        self.strength = 1
        self.shield = 'high'
        self.lance = 'low'
        self.shieldList = ['Animal Hide']
        self.lanceList = ['Drift Wood']
        self.currentShield = 0
        self.currentLance = 0

    def getName(self):
        return self.name
    
    def getProgress(self, city):
        return self.progress[city]
    def getProgressList(self):
        return self.progress

    def setProgress(self, city, prog):
        self.progress[city] = prog

    def setCoins(self, newCoins):
        self.coins = newCoins + self.coins

    def getCoins(self):
        return self.coins
    
    def getStrength(self):
        return self.strength

    def setShieldPos(self, pos):
        self.shield = pos
        
    def setLancePos(self,pos):
        self.lance = pos

    def getPositions(self):
        return [self.shield, self.lance]

    def getCurrentShield(self):
        return self.shieldList[self.currentShield]
    
    def getCurrentLance(self):
        return self.lanceList[self.currentLance]
    
    def addEquipment(self, equipo):
        if(equipo.getType()=='shield'):
            self.shieldList.append(equipo.getName())
            self.strength = self.strength + equipo.getStrength()
            self.currentShield = self.currentShield + 1
        if(equipo.getType()=='lance'):
            self.lanceList.append(equipo.getName())
            self.strength = self.strength + equipo.getStrength()
            self.currentLance = self.currentLance + 1
        self.coins = self.coins - equipo.getPrice()

    def hasItem(self, name, itemType):
        if(itemType == 'shield'):
            return name in self.shieldList
        if(itemType == 'lance'):
            return name in self.lanceList
    def getLanceList(self):
        return self.lanceList
    def getShieldList(self):
        return self.shieldList

    def getCurrentShieldIndex(self):
        return self.currentShield
    def getCurrentLanceIndex(self):
        return self.currentLance

    def getEquipmentList(self):
        return self.shieldList + self.lanceList
    
    def updatePlayer(self, newPlayer):
        self.name = newPlayer.getName()
        self.progress = newPlayer.getProgressList()
        self.coins = newPlayer.getCoins()
        self.strength = newPlayer.getStrength()
        self.shieldList = newPlayer.getShieldList()
        self.lanceList = newPlayer.getLanceList()
        self.currentShield = newPlayer.getCurrentShieldIndex()
        self.currentLance = newPlayer.getCurrentLanceIndex()

    

class Knight():

    def __init__(self, kName, pShield, pLance, s, win, images):
        self.name = kName
        self.probShield = pShield
        self.probLance = pLance
        self.strength = s
        self.winnings = win
        self.images = images
        
    def getName(self):
        return self.name
    
    def getPositions(self):
        
        shieldPos=random.randint(0,10)
        lancePos=random.randint(0,10)
        if(shieldPos<self.probShield):
            self.shield = 'low'
        elif(shieldPos>=self.probShield):
            self.shield = 'high'
        if(lancePos<self.probLance):
            self.lance='low'
        elif(lancePos>=self.probLance):
            self.lance='high'
               
        return [self.shield,self.lance]

    def getStrength(self):
        return self.strength

    def getWinnings(self):
        return self.winnings

    def getImages(self):
        return self.images

def test():
    bknight = Knight('black knight',5,5,20, 30)
    kade = Player('Kade')
    castle = City('Isengard', ['Evil King', 'Black Knight', 'Green Knight'], 3)
    
   
    knightLists = castle.getKnights(kade.getProgress(castle.getName()))
    list1 = knightLists[0]
    list2 = knightLists[1]

    print "Knights Defeated"
    for n in list1:
        print n
    print "Knights Undefeated"
    for x in list2:
        print x

    print kade.getProgress('Yorkshire')

    kade.getCurrentShield()

if __name__ == '__main__':
   test()



















    
