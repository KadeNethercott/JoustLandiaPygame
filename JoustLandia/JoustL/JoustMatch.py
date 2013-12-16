#!usr/bin/python

import random, time, pygame, copy, sys
from pygame.locals import *


class Match():

    #returns 0 for tie, 1 for player win, 2 for opponent win
    def getResults(self, player, opponent):
        
        self.playerShield = player[0]
        self.playerLance = player[1]
        self.oppShield = opponent[0]
        self.oppLance = opponent[1]

        ##possible player win situations
        if((self.playerShield == 'low' and self.oppLance == 'low') or (self.playerShield == 'high' and self.oppLance == 'high')):
            if((self.playerLance == 'high' and self.oppShield == 'low') or (self.playerLance == 'low' and self.oppShield == 'high')):
                return 1
        #possible opponent win situations
        elif((self.playerLance == 'low' and self.oppShield == 'low') or (self.playerLance == 'high' and self.oppShield == 'high')):
            if((self.playerShield == 'high' and self.oppLance == 'low') or (self.playerShield == 'low' and self.oppLance == 'high')):
                return 2  
        else:
            return 0


def main():
    match1 = Match()
    results = match1.getResults(['low', 'low'], ['high', 'low'])
    print results
    if(not results):
        print "tie"
    elif(results==1):
        print "you win"
    else:
        print "you lose"

if __name__ == '__main__':
    main()
        
