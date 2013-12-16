#!usr/bin/python


import random, time, pygame, copy, sys, os
from pygame.locals import *

GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
WHITE       = (255, 255, 255, 100)

class TextBox:

    def __init__(self):
        
        self.string = ''

    def startUp(self, width, height, surf, message):
        
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        FPSCLOCK = pygame.time.Clock()
    
        COLOR1 = RED
        COLOR2 = RED
        COLOR3 = BLACK

        
        
        addToString = ''
        self.string=''
        blinkWaitTime = 0
        blinkXPos = width/2-250
        
        ##create fonts
        font = pygame.font.Font(os.path.join('graphics','FancyText.ttf'),55)
        font2 = pygame.font.Font(os.path.join('graphics','FancyText3.ttf'),40)
        nameSurfaceObj = font.render(message, True, RED)
        nameRectObj =nameSurfaceObj.get_rect()

        ## sound for button clicking
        BUTTONCLICKSOUND = pygame.mixer.Sound(os.path.join('sounds', 'buttonClick.wav'))

        
        closeRectObj =nameSurfaceObj.get_rect()
        
        ## Images and locations
        paper = pygame.image.load(os.path.join('graphics','oldPaperFullShadow.png'))
        paperRectObj = paper.get_rect()
        
        paperRectObj.center = (width/2, height/2)
        nameRectObj.center = (width/2, (height/2)-55)

        errorSurfaceObj = font.render("Not A Valid Key", True, RED)
        errorRectObj =errorSurfaceObj.get_rect()
        errorRectObj.center = (width/2, (height/2))

        nameErrorSurfaceObj = font.render('Please Enter a Name', True, COLOR1)
        nameErrorRectObj = nameErrorSurfaceObj.get_rect()
        nameErrorRectObj.center = ((width/2),( (height/2)))
        
        while(True): ## textbox loop

            ##images that change based on user input
            submitSurfaceObj = font.render('Submit', True, COLOR1)
            submitRectObj = submitSurfaceObj.get_rect()
            submitRectObj.center = ((width/2),( (height/2) +40))

            closeSurfaceObj = font.render('X', True, COLOR2)    
            closeRectObj =closeSurfaceObj.get_rect()
            closeRectObj.center = ( ((width/2)+285), ((height/2)-45))

            blinkLineSurfaceObj = font2.render('|', True, COLOR3)    
            blinkLineRectObj =blinkLineSurfaceObj.get_rect()
            blinkLineRectObj.center = ( blinkXPos, ((height/2)+5))

            stringSurfaceObj = font2.render(self.string, True, BLACK)    
            stringRectObj =stringSurfaceObj.get_rect()
            stringRectObj.topleft = ( ((width/2)-250), ((height/2)-34))

            
            surf.blit(paper, paperRectObj)
            surf.blit(nameSurfaceObj, nameRectObj)
            
            surf.blit(closeSurfaceObj, closeRectObj)
            surf.blit(submitSurfaceObj, submitRectObj)
            surf.blit(blinkLineSurfaceObj, stringRectObj.topright)
            surf.blit(stringSurfaceObj, stringRectObj)

                                        
            ##highlight buttons
            mouseX, mouseY = pygame.mouse.get_pos()
            if(submitRectObj.collidepoint((mouseX, mouseY))):
                COLOR1 = BLACK
            else:
                COLOR1 = RED
            if(closeRectObj.collidepoint((mouseX, mouseY))):
                COLOR2 = BLACK
            else:
                COLOR2 = RED
                
            for event in pygame.event.get(): ## event loop
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    if submitRectObj.collidepoint( (mousex, mousey) ):
                        
                        if(len(self.string)>0): ## if the player entered a string then return it
                            BUTTONCLICKSOUND.play()
                            pygame.time.wait(500)
                            return self.string
                        else: ## if nothing entered but still sumbited then show error
                            BUTTONCLICKSOUND.play()
                            pygame.time.wait(500)
                            surf.blit(nameErrorSurfaceObj, nameErrorRectObj)
                            pygame.display.update()
                            pygame.time.wait(1000)
                           
                    elif closeRectObj.collidepoint( (mousex, mousey) ): ## if player clicks the x button, exits with false
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        return False
                if event.type == KEYUP:
                    key = pygame.key.name(event.key) ## allow for upper case letters
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        self.string+=key.upper()
                       
                    elif(key == 'backspace' or key == 'delete'): ## allow deletion of characters
                        if(len(self.string)):
                            lastKey = self.string[-1]
                            self.string = self.string[:-1]
                    elif(key == 'return'): ## return works as submit
                        if(len(self.string)>0):
                            BUTTONCLICKSOUND.play()
                            pygame.time.wait(500)
                            return self.string
                        else:
                           surf.blit(nameErrorSurfaceObj, nameErrorRectObj)
                           pygame.display.update()
                           pygame.time.wait(1000)
                    
                    elif(key == 'tab' or key == 'space'): ## don't allow tab or space keys
                        surf.blit(errorSurfaceObj, errorRectObj)
                        pygame.display.update()
                        pygame.time.wait(400)
                        print "not a valid key"
                    elif(key == "right shift" or key == "left shift"): ## don't throw an error on shift keys
                        pass
                    else:
                        try:
                            self.string+= chr(event.key) ## add characters to the string
                        
                        except:## show error if key not allowed as input
                            surf.blit(errorSurfaceObj, errorRectObj)
                            pygame.display.update()
                            pygame.time.wait(400)
                            print 'not a valid key'
                    
                    
  
                    
            blinkWaitTime = blinkWaitTime + FPSCLOCK.get_time()  
            if(blinkWaitTime > 360):
                if(COLOR3 == WHITE):
                    COLOR3 = BLACK
                else:
                    COLOR3=WHITE
                blinkWaitTime = 0
    
            
            pygame.display.update()
            FPSCLOCK.tick(25)
            

        
        
    
    def getInput(self):
        return self.string





def test():
    
    pygame.init()
    surf = pygame.display.set_mode((1100, 700))
    surf.fill(GRAY)

    myBox = TextBox()

    myBox.startUp(800, 700, surf, 'Enter Name')
    surf.fill(GRAY)
    
    pygame.display.update()
    while(True):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()



    
if __name__ == '__main__':
   test()


        
        
