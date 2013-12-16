#!usr/bin/python

import random, time, pygame, copy, sys
from pygame.locals import *

class TextSprite(pygame.sprite.Sprite):


    
    def __init__(self, font, location, color, description):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.color = color
        self.description = description
        self.image = font.render(description, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = location
        
        
    def update(self, newColor=None, description=None):
        mouseX, mouseY = pygame.mouse.get_pos()
        ## highlight if mouse is over the button, and change text if included
        if not newColor and not description:
            self.image = self.font.render(self.description, True, self.color)
        elif not description and newColor:
            if self.rect.collidepoint( (mouseX, mouseY) ):
                self.image = self.font.render(self.description, True, newColor)
            else:
                self.image = self.font.render(self.description, True, self.color)
        elif not newColor and description:
            self.image = self.font.render(description, True, self.color)
                

class CityNameSprite(pygame.sprite.Sprite):

    def __init__(self, font, location, color, description, image):

        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.color = color
        self.description = description
        self.image = font.render(description, True, color)
        self.rect = image.get_rect()
        self.rect.center = location

    def update(self):
        mouseX, mouseY = pygame.mouse.get_pos()  
        if self.rect.collidepoint( (mouseX, mouseY) ):
            self.image = self.font.render(self.description, True, self.color)
        else:
            self.image = self.font.render('', True, self.color)

class KnightSprite(pygame.sprite.Sprite):
    
    def __init__(self, location, shieldLanceDownImg, shieldDownLanceUpImg, shieldUpLanceDownImg, shieldLanceUpImg):

        pygame.sprite.Sprite.__init__(self)
        self.shieldLanceDownImg = shieldLanceDownImg
        self.shieldDownLanceUpImg = shieldDownLanceUpImg
        self.shieldUpLanceDownImg = shieldUpLanceDownImg
        self.shieldLanceUpImg = shieldLanceUpImg
        
        self.image = shieldUpLanceDownImg
        self.rect = shieldUpLanceDownImg.get_rect()
        self.smallRect = self.rect.inflate(-190,-190)
        self.xLocation = location[0]
        self.yLocation = location[1]
        self.rect.center = (location[0], location[1])
        self.smallRect.center = (location[0], location[1])
        
    
    def update(self, xPos, equipmentPositions):
    
        knightPos = equipmentPositions
    
        if(knightPos[0] == 'low' and knightPos[1] == 'low'):
            self.image = self.shieldLanceDownImg
            self.rect.center = (xPos, self.yLocation)
            self.smallRect.center = (xPos, self.yLocation)
                           
        elif(knightPos[0] == 'high' and knightPos[1] == 'low'):
            self.image = self.shieldUpLanceDownImg
            self.rect.center = (xPos, self.yLocation)
            self.smallRect.center = (xPos, self.yLocation)
                           
        elif(knightPos[0] == 'low' and knightPos[1] == 'high'):
            self.image = self.shieldDownLanceUpImg
            self.rect.center = (xPos, self.yLocation)
            self.smallRect.center = (xPos, self.yLocation)
            
        elif(knightPos[0] == 'high' and knightPos[1] == 'high'):
            self.image = self.shieldLanceUpImg
            self.rect.center = (xPos, self.yLocation)
            self.smallRect.center = (xPos, self.yLocation)

class LegsSprite(pygame.sprite.Sprite):
    
    def __init__(self, location, legsClosed, legsOpen):

        pygame.sprite.Sprite.__init__(self)
        self.legsOpenImg = legsOpen
        self.legsClosedImg = legsClosed
        
        self.image = legsOpen
        self.rect = legsOpen.get_rect()
        self.xLocation = location[0]
        self.yLocation = location [1]
        self.rect.center = (location[0], location[1])
      
        
    
    def update(self, xPos, legsPos):
        if((legsPos % 4) == 0):
            self.image = self.legsOpenImg
        elif((legsPos %3) == 0):
            self.image = self.legsClosedImg
        self.rect.center = (xPos, self.yLocation)
            



def test():
    print "Testing..."

if __name__ == '__main__':
   test()


