#!usr/bin/python

import random, time, pygame, copy, sys, os, pickle
from pygame.locals import *
from JoustL import JoustObjects
from JoustL import JoustMatch
from JoustL import TextBox
from JoustL import JoustSprites

FPS = 25
### Screen size ##
WINDOWWIDTH = 1100
WINDOWHEIGHT = 700

#   Colors      R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (255, 255, 10)
LIGHTYELLOW = (175, 175,  20)
PURPLE      = (76, 0, 153)

############## Knight images ##############
kingImages = ['kingShieldLanceDown.png', 'kingShieldDownLanceUp.png', 'kingShieldUpLanceDown.png', 'kingShieldLanceUp.png', 'blackLegsClosed.png', 'blackLegsOpen.png']

knightImages = ['greenShieldLanceDown.png', 'greenShieldDownLanceUp.png', 'greenShieldUpLanceDown.png', 'greenShieldLanceUp.png', 'darkBrownLegsClosed.png', 'darkBrownLegsOpen.png']
ladyImages = ['pinkShieldLanceDown.png', 'pinkShieldDownLanceUp.png', 'pinkShieldUpLanceDown.png', 'pinkShieldLanceUp.png', 'grayLegsClosed.png', 'grayLegsOpen.png']


############ Knights and Ladies (Name, probability high, probability low, strength, coins, images)###############
evilKing = JoustObjects.Knight('Evil King', 5, 5, 39, 1000, kingImages )
sirVladimir= JoustObjects.Knight('Sir Vladimir', 2, 2, 35, 100, knightImages)
blackKnight= JoustObjects.Knight('Black Knight', 3, 4, 30, 50, knightImages)
sirRobin = JoustObjects.Knight('Sir Robin', 3,8,25, 40, knightImages)
sirLancelot = JoustObjects.Knight('Sir Lancelot', 2,4,20, 35, knightImages)
joanOfArc = JoustObjects.Knight('Joan of Arc', 1, 3, 15, 30, ladyImages)
sirWilliam = JoustObjects.Knight('Sir William', 6, 8, 10, 25, knightImages)

sirConstantine = JoustObjects.Knight('Constantine', 3,9,10, 35, knightImages)
greenKnight = JoustObjects.Knight('Green Knight', 8, 8, 9, 20, knightImages)
sirKahedin = JoustObjects.Knight('Sir Kahedin', 2, 2, 5, 15, knightImages)
sirDuke = JoustObjects.Knight('Sir Duke', 6, 4, 4, 10, knightImages)

sirLeonidas = JoustObjects.Knight('Sir Leonidas', 8, 3, 7, 30, knightImages)
sirTroy = JoustObjects.Knight('Sir Troy', 6,9,5, 15, knightImages)
sirMark = JoustObjects.Knight('Sir Mark', 9, 1, 3, 10, knightImages)
ladyTristan = JoustObjects.Knight('Lady Tristan', 9, 9, 1, 5, ladyImages)

############## Player object ###########
PLAYER= JoustObjects.Player('')

############ Cities     (name, knights list, number of knights, image) ##################
castle = JoustObjects.City('Isengard', [sirWilliam, joanOfArc, sirLancelot, sirRobin, blackKnight, sirVladimir, evilKing], 7, 'kingslair.png')
yorkshire = JoustObjects.City('Yorkshire', [sirDuke, sirKahedin, greenKnight, sirConstantine], 4, 'smallcastlescene.png')
norfolk  = JoustObjects.City('Norfolk', [ladyTristan, sirMark, sirTroy, sirLeonidas], 4, 'townscene.png')

######### Lances (Name, Strength, Cost, Type) ##############
blessedLance = JoustObjects.Equipment('Blessed Bronze', 2, 10, 'lance')
blackIronLance = JoustObjects.Equipment('Black Iron', 3, 30, 'lance')
heroLance = JoustObjects.Equipment('Hero Maker', 5, 65, 'lance')
legendLance = JoustObjects.Equipment('Legend Slayer', 10, 95, 'lance')

############## Shields (Name, Strength, Cost, Type)  ############
barbarianShield = JoustObjects.Equipment('Barbarians', 2, 15, 'shield')
crusadersShield = JoustObjects.Equipment('Crusaders',3, 25, 'shield')
lionShield = JoustObjects.Equipment('Lion Heart', 5, 55, 'shield')
dragonShield = JoustObjects.Equipment('Dragon Scales', 10, 100, 'shield')



def main():
    ####### Global Variables ########
    global FPSCLOCK, DISPLAYSURF, BGIMAGE, FANCYFONTLARGE, FANCYFONTMEDIUM, FANCYFONTSMALLMED, FANCYFONTSMALL
    global GOTHFONTLARGE, GOTHFONTMEDIUM, GOTHFONTSMALL
    global PLAYERHASHTABLE, BUTTONCLICKSOUND, PLAYERCLOCK, STARTTIMER
    
    print "Game Loading....."

    ###### Center the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    ### initialize sounds and pygame  
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
   
    STARTTIMER = 0
    PLAYERHASHTABLE  = {}
    ############################## Load the Saved Games #############################
    try:
        savedGameFile = open(os.path.join('SavedGames','SavedGames.pkl'), 'rb')
    
        PLAYERHASHTABLE = pickle.load(savedGameFile)
    
        
        savedGameFile.close()
    except IOError:
        print "No saved games file, creating one now...."
        output = open(os.path.join('savedGames','SavedGames.pkl'), 'wb')
        pickle.dump(PLAYERHASHTABLE, output)
        output.close()

    
    BUTTONCLICKSOUND = pygame.mixer.Sound(os.path.join('sounds', 'buttonClick.wav'))

    ############ create the different fonts for the text images ##################   
    FANCYFONTLARGE = pygame.font.Font(os.path.join('graphics', 'FancyText.ttf'), 150)
    FANCYFONTMEDIUM = pygame.font.Font(os.path.join('graphics', 'FancyText.ttf'), 100)
    FANCYFONTSMALLMED = pygame.font.Font(os.path.join('graphics', 'FancyText.ttf'), 75)
    FANCYFONTSMALL = pygame.font.Font(os.path.join('graphics', 'FancyText.ttf'), 50)

    GOTHFONTLARGE = pygame.font.Font(os.path.join('graphics', 'AGothiqueTime.ttf'),150)
    GOTHFONTMEDIUM = pygame.font.Font(os.path.join('graphics', 'AGothiqueTime.ttf'),100)
    GOTHFONTSMALL = pygame.font.Font(os.path.join('graphics', 'AGothiqueTime.ttf'),80)
    logoImg = pygame.image.load(os.path.join('graphics','joustlandia.png'))

    logoRectObj = logoImg.get_rect()
    logoRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    
    FPSCLOCK = pygame.time.Clock()
    PLAYERCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('JoustLandia!')

    ######################### create the text sprites #########################
    #bannerText = JoustSprites.TextSprite(FANCYFONTLARGE, (WINDOWWIDTH/2, 150), YELLOW, 'J o u s t L a n d i a')
    newText = JoustSprites.TextSprite(FANCYFONTLARGE, (WINDOWWIDTH/2, 400), PURPLE, "New Game")
    loadText = JoustSprites.TextSprite(FANCYFONTLARGE, (WINDOWWIDTH/2, 575), PURPLE, "Load Game")

    ####################### create the text sprite groups #####################
    textSprites = pygame.sprite.Group((newText, loadText))
    
    while True: ####### Main Game Loop #######
             
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(logoImg,logoRectObj)
        
        textSprites.update(YELLOW)
        textSprites.draw(DISPLAYSURF)

        for event in pygame.event.get(): ##Events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if newText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    newGame()
                if loadText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    loadGame()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def helpInfo():
    
    ### Sprites and Sprite Groups
    saveText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (300,650), BLACK, 'Save')
    backText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (100, 650), BLACK, 'Back')
    textSpriteGroup = pygame.sprite.Group((saveText, backText))
    helpImg = pygame.image.load(os.path.join('graphics','helpInfo.png'))
    
    helpRectObj = helpImg.get_rect()
    
    helpRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    
    
    while(True): #### Help screen loop
        
        DISPLAYSURF.fill(GRAY)
        DISPLAYSURF.blit(helpImg, helpRectObj)

        textSpriteGroup.update(YELLOW)
        textSpriteGroup.draw(DISPLAYSURF)
        
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
    
                if saveText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    saveGame()
                    
                elif backText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    return 0
                
        pygame.display.update()
        
def newGame():
    
    DISPLAYSURF.fill(GRAY)
    logoSmallImg = pygame.image.load(os.path.join('graphics','logoSmall.png'))
    introImg = pygame.image.load(os.path.join('graphics','intro.png'))
    
    logoSmallRectObj = logoSmallImg.get_rect()
    introRectObj = introImg.get_rect()
    
    logoSmallRectObj.center = (WINDOWWIDTH/2, 130)
    introRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    
    DISPLAYSURF.blit(logoSmallImg, logoSmallRectObj)
    DISPLAYSURF.blit(introImg, introRectObj)
    
    nameTextBox = TextBox.TextBox()
    playerName = ''
    ## get player name input using the textbox, return to previous menu if x button is pressed
    newPlayerName = nameTextBox.startUp(WINDOWWIDTH, WINDOWHEIGHT+560, DISPLAYSURF, 'Enter a Name')
    
    if newPlayerName == False:
        return 0
    else:
        ##create the new player
        newPlayer = JoustObjects.Player(newPlayerName)
        ##insert into hash table to allow saving
        PLAYERHASHTABLE[newPlayer.getName()] = newPlayer
        #Change the global player object to the newPlayer info
        PLAYER.updatePlayer(newPlayer)
        saveGame()
        STARTTIMER = pygame.time.get_ticks()
        drawWorldMap()
        return 0


def loadGame():
    DISPLAYSURF.fill(GRAY)
    keys = PLAYERHASHTABLE.keys()  ## get the names of all of the players from the saved games hash table
    nameTextBox = TextBox.TextBox()
    column =150
    row = 130
    
    nameErrorSurfaceObj = FANCYFONTLARGE.render('Player Not Found', True, BLACK)
    nameErrorRectObj = nameErrorSurfaceObj.get_rect()
    nameErrorRectObj.center = ((WINDOWWIDTH/2),( (WINDOWHEIGHT/2)))

    currentPlayersSurfaceObj = FANCYFONTMEDIUM.render('* Player Names *', True, RED)
    currentPlayersRectObj = currentPlayersSurfaceObj.get_rect()
    currentPlayersRectObj.center = ((WINDOWWIDTH/2),50)

    DISPLAYSURF.blit(currentPlayersSurfaceObj, currentPlayersRectObj)

    largestName = 0  ## keep track of the longest name so we know how far over to start the next row

    for key in PLAYERHASHTABLE.keys(): ##loop through the has table and print each players name to the screen
        playerNamesSurfaceObj = FANCYFONTSMALL.render('{ ' + key, True, YELLOW)
        playerNamesRectObj = playerNamesSurfaceObj.get_rect()
        playerNamesRectObj.midleft = (column,row)
        nameSizeX, nameSizeY = playerNamesRectObj.midright
        
        if(largestName < nameSizeX ):
            largestName = nameSizeX ## keep track of longest name so we know where to start the next row
        DISPLAYSURF.blit(playerNamesSurfaceObj, playerNamesRectObj)
        row = row +50 ## move down to start the next row of player names
        if(row > 500): ## if hit the bottom then move over to the next column
            row =130
            column = largestName +10
    pygame.display.update()

    ##get the name entered in the textbox
    loadPlayerName = nameTextBox.startUp(WINDOWWIDTH, WINDOWHEIGHT+500, DISPLAYSURF, 'Enter Existing Name')
    if(PLAYERHASHTABLE.has_key(loadPlayerName)):## if found the start the game
        PLAYER.updatePlayer(PLAYERHASHTABLE[loadPlayerName])
        STARTTIMER = pygame.time.get_ticks()
        drawWorldMap()
        return 0
    if(loadPlayerName == False): 
        return 0
    else: ## if player doesn't exist then exit to previous screen
        DISPLAYSURF.blit(nameErrorSurfaceObj, nameErrorRectObj) 
        pygame.display.update()
        pygame.time.wait(1000)
        return 0
    

def saveGame():

        saveSurfaceObj = FANCYFONTLARGE.render('Saving...', True, RED)
        saveRectObj = saveSurfaceObj.get_rect()
        saveRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

        ##enter the player into the hash table
        PLAYERHASHTABLE[PLAYER.getName()]= PLAYER
        DISPLAYSURF.blit(saveSurfaceObj, saveRectObj)
        
        
        print "Saving Content...."
        try: ##save the updated hash table to the saved games file
            output = open(os.path.join('SavedGames','SavedGames.pkl'), 'wb')
            pickle.dump(PLAYERHASHTABLE, output)
            output.close()
        except IOError:
            print "Failed to Save"
            
        pygame.display.update()
        pygame.time.wait(1000)
        

def drawWorldMap():

    STARTTIMER
    

    ######## Set up the background image.
    townImage = pygame.image.load(os.path.join('graphics','town.png'))
    smallCastleImage = pygame.image.load(os.path.join('graphics','smallcastle.png'))
    castleImage = pygame.image.load(os.path.join('graphics','bigcastle.png'))
    mapImg = pygame.image.load(os.path.join('graphics','mapColored.png'))

    lockedSurfaceObj = FANCYFONTMEDIUM.render('Locked', True, YELLOW)
    lockedRectObj = lockedSurfaceObj.get_rect()
    lockedRectObj.center = (WINDOWWIDTH/4, 250)

    ### create sprites for the buttons ####
    saveText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (300,650), BLACK, 'Save')
    backText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (100, 650), BLACK, 'Back')
    helpText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (480, 650), BLACK, 'Help')
    ## creat sprites for the city names ###
    norfolkNameSprite = JoustSprites.CityNameSprite(FANCYFONTMEDIUM, (850,250), PURPLE , 'Yorkshire', smallCastleImage)
    yorkshireNameSprite = JoustSprites.CityNameSprite(FANCYFONTMEDIUM, (865,560), PURPLE , 'Norfolk', townImage)
    isengardNameSprite = JoustSprites.CityNameSprite(FANCYFONTMEDIUM, (215,230), PURPLE , 'Isengard', castleImage)

    ## sprite groups for buttons and city names ##
    textSpriteGroup = pygame.sprite.Group((saveText, backText, helpText))
    cityNameSpriteGroup = pygame.sprite.Group( (norfolkNameSprite, yorkshireNameSprite, isengardNameSprite))

    
    while(True):

        
    
        playerClockSurfaceObj = FANCYFONTSMALL.render(str((pygame.time.get_ticks()-STARTTIMER)/1000), True, LIGHTBLUE)
        playerClockRectObj = playerClockSurfaceObj.get_rect()
        playerClockRectObj.topright = (WINDOWWIDTH-10, 10)

        ## create the rectangles and their positions for the images
        townImageRect = townImage.get_rect()
        smallCastleImageRect = smallCastleImage.get_rect()
        castleImageRect = castleImage.get_rect()
        townImageRect.center = (865, 560)
        smallCastleImageRect.center = (900, 250)
        castleImageRect.center = (215, 230)

        ## blit to the screen
        BGIMAGE = mapImg
        BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
        DISPLAYSURF.blit(townImage, townImageRect)
        DISPLAYSURF.blit(smallCastleImage, smallCastleImageRect)
        DISPLAYSURF.blit(castleImage, castleImageRect)
        DISPLAYSURF.blit(playerClockSurfaceObj, playerClockRectObj)


        DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

        ## update and draw sprites
        textSpriteGroup.update(YELLOW)
        textSpriteGroup.draw(DISPLAYSURF)
        cityNameSpriteGroup.update()
        cityNameSpriteGroup.draw(DISPLAYSURF)
    
        checkForQuit()
        for event in pygame.event.get(): #### World Map game loop
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if castleImageRect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    if(PLAYER.getProgress('Norfolk') == 4 and PLAYER.getProgress('Yorkshire') == 4):
                        drawCity(castle)
                    else:
                        DISPLAYSURF.blit(lockedSurfaceObj, lockedRectObj)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        
                elif townImageRect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    drawCity(norfolk)
                elif smallCastleImageRect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    drawCity(yorkshire)
                elif saveText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    saveGame()
                elif backText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    return 0
                elif helpText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    helpInfo()
        pygame.display.update()

        
        
def drawCity(city):

    ### Text images  
    completedSurfaceObj = FANCYFONTMEDIUM.render('City Completed', True, LIGHTBLUE)
    completedRectObj = completedSurfaceObj.get_rect()
    completedRectObj.center = (WINDOWWIDTH-275, 200)


    nameSurfaceObj = FANCYFONTLARGE.render(city.getName(), True, PURPLE)
    nameRectObj = nameSurfaceObj.get_rect()
    nameRectObj.center = (WINDOWWIDTH/4, 75)

    coinsSurfaceObj = FANCYFONTMEDIUM.render('Coins: ', True, YELLOW)
    coinsRectObj = coinsSurfaceObj.get_rect()
    coinsRectObj.center = (250, 600)

    
    defeatedSurfaceObj = FANCYFONTSMALL.render('Defeated ', True, BLACK)
    defeatedRectObj = defeatedSurfaceObj.get_rect()
    defeatedRectObj.center = (125, 200)

    undefeatedSurfaceObj = FANCYFONTSMALL.render('Undefeated ', True, BLACK) 
    undefeatedRectObj = undefeatedSurfaceObj.get_rect()
    undefeatedRectObj.center = (425, 200)
    
    pCoinsFontObj = pygame.font.Font(os.path.join('graphics','FancyText.ttf'), 75)

    ### Sprites for the buttons
    saveText = JoustSprites.TextSprite(FANCYFONTMEDIUM,(WINDOWWIDTH-275, 450), BLACK, 'Save')
    mapText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (WINDOWWIDTH-275, 350), BLACK, 'Map')
    bSmithText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (WINDOWWIDTH-275, 250), BLACK, 'Blacksmith')
    joustText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (WINDOWWIDTH-275, 150), BLACK, 'Joust')
    inventoryText = JoustSprites.TextSprite(FANCYFONTMEDIUM, (WINDOWWIDTH-275, 530), BLACK, 'Inventory')

    ### buttons sprite group
    textSpriteGroup = pygame.sprite.Group((saveText, mapText, bSmithText, joustText, inventoryText))
    

    paperImg = pygame.image.load(os.path.join('graphics','bookPaper.png')).convert()

    
    while(True):

        ### draw the images to the screen
        strengthSurfaceObj = FANCYFONTMEDIUM.render('Strength: ' + str(PLAYER.getStrength()), True, RED)
        strengthRectObj = strengthSurfaceObj.get_rect()
        strengthRectObj.center = (WINDOWWIDTH-275, 625)
        
        pCoinsSurfaceObj = pCoinsFontObj.render(str(PLAYER.getCoins()), True, YELLOW)
        pCoinsRectObj = pCoinsSurfaceObj.get_rect()
        pCoinsRectObj.topleft = (350, 570)
        
        BGIMAGE = paperImg
        BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
 
        BGIMAGE.blit(nameSurfaceObj, nameRectObj)
        BGIMAGE.blit(coinsSurfaceObj, coinsRectObj)
        BGIMAGE.blit(pCoinsSurfaceObj, pCoinsRectObj)
        BGIMAGE.blit(defeatedSurfaceObj, defeatedRectObj)
        BGIMAGE.blit(undefeatedSurfaceObj, undefeatedRectObj)
        BGIMAGE.blit(strengthSurfaceObj, strengthRectObj)

        ## get the 2 list of knights for the current city
        knightLists = city.getKnights(PLAYER.getProgress(city.getName()))

        ## Get the defeated and undefeated knights 
        defeated = knightLists[0]
        undefeated = knightLists[1]
        
        yLoc = 230

        ## draw the defeated knights to the screen
        for n in defeated:  
            knightSurfaceObj = FANCYFONTSMALL.render(n.getName(), True, LIGHTBLUE)
            knightRectObj = knightSurfaceObj.get_rect()
            knightRectObj.topleft = (40, yLoc)
            BGIMAGE.blit(knightSurfaceObj, knightRectObj)
            yLoc = yLoc + 35

        ## reset the y position
        yLoc = 230
        
        ##draw the undefeated knights
        for n in undefeated:      
            knightSurfaceObj = FANCYFONTSMALL.render(n.getName(), True, LIGHTBLUE)
            knightRectObj = knightSurfaceObj.get_rect()
            knightRectObj.topleft = (325, yLoc)
            BGIMAGE.blit(knightSurfaceObj, knightRectObj)
            yLoc = yLoc + 45                                 
    
        DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

        ##update and draw the sprite group
        textSpriteGroup.update(YELLOW)
        textSpriteGroup.draw(DISPLAYSURF)

            
        checkForQuit()
        for event in pygame.event.get(): ## city game loop 
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if bSmithText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    drawBlackSmith(city)
                elif joustText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    if(len(undefeated)==0): ## if all the knights have been defeated then can't joust any more in the city
                        DISPLAYSURF.blit(completedSurfaceObj, completedRectObj)
                        pygame.display.update()
                        pygame.time.wait(500)
                    else:
                        if(drawMatch(undefeated[0], city)): ## if the player wins the match, then update progress and winnings
                            updateProg = PLAYER.getProgress(city.getName())
                            updateProg = updateProg +1
                            PLAYER.setProgress(city.getName(), updateProg)
                            PLAYER.setCoins(undefeated[0].getWinnings())
                        if(city.getName()=='Isengard' and PLAYER.getProgress(city.getName()) == 7): ## if player completed Isengard then won the game
                            gameCompleted()
                elif mapText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    return 1
                elif saveText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    saveGame()
                elif inventoryText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    drawInventory()
        pygame.display.update()
        
def drawMatch(knight, city):

    playerWins = 0
    knightWins = 0
    joustMatch = JoustMatch.Match()
    playerScore =0
    oppScore = 0

    shieldStr = 'High'
    lanceStr = 'Low'
    shieldPos = 550
    lancePos = 600

    ## colors for the joust and back buttons
    CURRENTCOLOR1 = GRAY
    CURRENTCOLOR2 = GRAY
    
    
#############set up all of the text graphics and positions #######################
    shieldPosSurfaceObj = FANCYFONTSMALL.render('Shield:', True, BLUE)
    shieldPosRectObj = shieldPosSurfaceObj.get_rect()
    shieldPosRectObj.center = (WINDOWWIDTH-300, 500)

    shieldHighSurfaceObj = FANCYFONTSMALL.render('High', True, BLACK)
    shieldHighRectObj = shieldHighSurfaceObj.get_rect()
    shieldHighRectObj.center = (WINDOWWIDTH-300, 550)

    shieldLowSurfaceObj = FANCYFONTSMALL.render('Low', True, BLACK)
    shieldLowRectObj = shieldLowSurfaceObj.get_rect()
    shieldLowRectObj.center = (WINDOWWIDTH-300, 600)
    
    lancePosSurfaceObj = FANCYFONTSMALL.render('Lance: ', True, BLUE)
    lancePosRectObj = lancePosSurfaceObj.get_rect()
    lancePosRectObj.center = (WINDOWWIDTH-150, 500)

    lanceHighSurfaceObj = FANCYFONTSMALL.render('High', True, BLACK)
    lanceHighRectObj = lanceHighSurfaceObj.get_rect()
    lanceHighRectObj.center = (WINDOWWIDTH-150, 550)

    lanceLowSurfaceObj = FANCYFONTSMALL.render('Low', True, BLACK)
    lanceLowRectObj = lanceLowSurfaceObj.get_rect()
    lanceLowRectObj.center = (WINDOWWIDTH-150, 600)
    
    tieSurfaceObj = FANCYFONTMEDIUM.render('Tie', True, PURPLE)
    tieRectObj = tieSurfaceObj.get_rect()
    tieRectObj.center = (WINDOWWIDTH/2, 350)

    winSurfaceObj = FANCYFONTMEDIUM.render('You Won!', True, PURPLE)
    winRectObj = winSurfaceObj.get_rect()
    winRectObj.center = (WINDOWWIDTH/2, 450)

    winMatchSurfaceObj = FANCYFONTMEDIUM.render('You Won the Joust Match!!!', True, PURPLE)
    winMatchRectObj = winMatchSurfaceObj.get_rect()
    winMatchRectObj.center = (WINDOWWIDTH/2, 150)

    winningsMatchSurfaceObj = FANCYFONTMEDIUM.render('Coins: ' + str(knight.getWinnings()), True, PURPLE)
    winningsMatchRectObj = winningsMatchSurfaceObj.get_rect()
    winningsMatchRectObj.center = (WINDOWWIDTH/2, 250)

    loseSurfaceObj = FANCYFONTMEDIUM.render('You Lost', True, PURPLE)
    loseRectObj = loseSurfaceObj.get_rect()
    loseRectObj.center = (WINDOWWIDTH/2, 450)

    loseMatchSurfaceObj = FANCYFONTMEDIUM.render('You Lost the Joust Match', True, PURPLE)
    loseMatchRectObj = loseMatchSurfaceObj.get_rect()
    loseMatchRectObj.center = (WINDOWWIDTH/2, 150)

    playerNameSurfaceObj = FANCYFONTSMALLMED.render(PLAYER.getName(), True, BLUE)
    playerNameRectObj = playerNameSurfaceObj.get_rect()
    playerNameRectObj.topright = (WINDOWWIDTH-10, 10)
    
    knightNameSurfaceObj = FANCYFONTSMALLMED.render(knight.getName(), True, RED)
    knightNameRectObj = knightNameSurfaceObj.get_rect()
    knightNameRectObj.topleft = (10, 10)

#######################load the images #######################
    fenceImage = pygame.image.load(os.path.join('graphics','fence.png'))
    fenceRectObj = fenceImage.get_rect()
    fenceRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    cloudImage = pygame.image.load(os.path.join('graphics','cloud.png'))
    cloudRectObj = cloudImage.get_rect()
    cloudRectObj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)

    #### images for the knight ####
    knightImages = knight.getImages()
    leftShieldLanceDownImage = pygame.image.load(os.path.join('graphics',knightImages[0]))
    leftShieldDownLanceUpImage = pygame.image.load(os.path.join('graphics', knightImages[1]))
    leftShieldUpLanceDownImage = pygame.image.load(os.path.join('graphics', knightImages[2]))
    leftShieldLanceUpImage = pygame.image.load(os.path.join('graphics', knightImages[3]))
    
    ### images for the player ###
    rightShieldLanceDownImage = pygame.image.load(os.path.join('graphics','rightShieldLanceDown.png'))
    rightShieldDownLanceUpImage = pygame.image.load(os.path.join('graphics','rightShieldDownLanceUp.png'))
    rightShieldUpLanceDownImage = pygame.image.load(os.path.join('graphics','rightShieldUpLanceDown.png'))
    rightShieldLanceUpImage = pygame.image.load(os.path.join('graphics','rightShieldLanceUp.png'))

    ## create sprites
    playerSprite = JoustSprites.KnightSprite([WINDOWWIDTH-100, 350], rightShieldLanceDownImage, rightShieldDownLanceUpImage, rightShieldUpLanceDownImage, rightShieldLanceUpImage)
    opponentSprite = JoustSprites.KnightSprite([100, 335], leftShieldLanceDownImage,leftShieldDownLanceUpImage,leftShieldUpLanceDownImage, leftShieldLanceUpImage   )

    ## sprite groups
    playerSpriteGroup = pygame.sprite.Group(playerSprite)
    opponentSpriteGroup = pygame.sprite.Group(opponentSprite)

    ##images and sprites for the horses legs so they can run with the horses
    rightLegsClosedImg = pygame.image.load(os.path.join('graphics','lightBrownLegsClosed.png'))
    rightLegsOpenImg = pygame.image.load(os.path.join('graphics','lightBrownLegsOpen.png'))

    rightLegsSprite = JoustSprites.LegsSprite([WINDOWWIDTH-100, 350], rightLegsClosedImg, rightLegsOpenImg)
    rightLegsSpriteGroup = pygame.sprite.Group(rightLegsSprite)
    
    leftLegsClosedImg = pygame.image.load(os.path.join('graphics',knightImages[4]))
    leftLegsOpenImg = pygame.image.load(os.path.join('graphics',knightImages[5]))

    leftLegsSprite = JoustSprites.LegsSprite([100,335], leftLegsClosedImg, leftLegsOpenImg)
    leftLegsSpriteGroup = pygame.sprite.Group(leftLegsSprite)
    
    highlightFontObj = pygame.font.Font(os.path.join('graphics','FancyText.ttf'), 53)
    highlightFontObj.set_underline(True)

    ## jousting city background image
    cityJoustImage = pygame.image.load(os.path.join('graphics',city.getJoustImage())).convert()

    ### Jousting match sounds ##
    horsesRunningSound = pygame.mixer.Sound(os.path.join('sounds', 'horsesRunning.wav'))
    horseSound = pygame.mixer.Sound(os.path.join('sounds', 'horseSound.wav'))
    crashSound = pygame.mixer.Sound(os.path.join('sounds', 'CRASH.wav'))


    while(True): ##  match game loop
        
        #### graphics that change depending on user input
        backSurfaceObj = FANCYFONTMEDIUM.render('Back', True, CURRENTCOLOR2)
        backRectObj = backSurfaceObj.get_rect()
        backRectObj.center = (100, 650)
    
        joustSurfaceObj = FANCYFONTMEDIUM.render('Start Joust', True, CURRENTCOLOR1)
        joustRectObj = joustSurfaceObj.get_rect()
        joustRectObj.center = (WINDOWWIDTH/2, 350)
       
        highlightLanceSurfaceObj = highlightFontObj.render(lanceStr, True, PURPLE)
        highlightLanceRectObj = highlightLanceSurfaceObj.get_rect()
        highlightLanceRectObj.center = (WINDOWWIDTH-150, lancePos)

       
        highlightShieldSurfaceObj = highlightFontObj.render(shieldStr, True, PURPLE)
        highlightShieldRectObj = highlightShieldSurfaceObj.get_rect()
        highlightShieldRectObj.center = (WINDOWWIDTH-300, shieldPos)
    
        oppScoreSurfaceObj = FANCYFONTSMALLMED.render(str(oppScore), True, RED)
        oppScoreRectObj = oppScoreSurfaceObj.get_rect()
        oppScoreRectObj.center = (100, 150)

        playerScoreSurfaceObj = FANCYFONTSMALLMED.render(str(playerScore), True, BLUE)
        playerScoreRectObj = playerScoreSurfaceObj.get_rect()
        playerScoreRectObj.center = (WINDOWWIDTH-100, 150)
        


##############  Draw all of the graphics to the screen
        BGIMAGE = cityJoustImage
        BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
        
        BGIMAGE.blit(backSurfaceObj, backRectObj)
        BGIMAGE.blit(joustSurfaceObj, joustRectObj)
        
        BGIMAGE.blit(shieldPosSurfaceObj, shieldPosRectObj)
        BGIMAGE.blit(shieldHighSurfaceObj, shieldHighRectObj)
        BGIMAGE.blit(shieldLowSurfaceObj, shieldLowRectObj)
        BGIMAGE.blit(lancePosSurfaceObj, lancePosRectObj)
        BGIMAGE.blit(lanceHighSurfaceObj, lanceHighRectObj)
        BGIMAGE.blit(lanceLowSurfaceObj, lanceLowRectObj)
        BGIMAGE.blit(oppScoreSurfaceObj, oppScoreRectObj)
        BGIMAGE.blit(playerScoreSurfaceObj,playerScoreRectObj)
        BGIMAGE.blit(playerNameSurfaceObj, playerNameRectObj)
        BGIMAGE.blit(knightNameSurfaceObj, knightNameRectObj)
        BGIMAGE.blit(highlightShieldSurfaceObj, highlightShieldRectObj)
        BGIMAGE.blit(highlightLanceSurfaceObj, highlightLanceRectObj)
        
        DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())

        playerPos = PLAYER.getPositions()

        ##update sprite groups
        playerSpriteGroup.update((WINDOWWIDTH-100), playerPos)
        opponentSpriteGroup.update(100, ['low','low'])
        
        rightLegsSpriteGroup.update((WINDOWWIDTH-100), 4)
        leftLegsSpriteGroup.update((100), 4)

        
        ### draw sprite groups
        opponentSpriteGroup.draw(DISPLAYSURF)
        leftLegsSpriteGroup.draw(DISPLAYSURF)
        
        DISPLAYSURF.blit(fenceImage, fenceRectObj)
        
        playerSpriteGroup.draw(DISPLAYSURF)
        
        rightLegsSpriteGroup.draw(DISPLAYSURF)

        ## change color of the buttons if mouse if over them
        mouseX, mouseY = pygame.mouse.get_pos()
        if joustRectObj.collidepoint( (mouseX, mouseY) ):
            CURRENTCOLOR1 = YELLOW
        else:
            CURRENTCOLOR1 = GRAY
        if backRectObj.collidepoint( (mouseX, mouseY) ):
            CURRENTCOLOR2 = YELLOW
        else:
            CURRENTCOLOR2 = GRAY
            
########### Event Loop   ##############
        for event in pygame.event.get(): 
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == KEYUP: ## get the positions of the lance and shield
                shieldStr, lanceStr, shieldPos, lancePos = changePositions(event, shieldStr, lanceStr, shieldPos, lancePos, shieldLowRectObj, shieldHighRectObj, lanceLowRectObj, lanceHighRectObj)
                 
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if backRectObj.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    
                    pygame.time.wait(500)
                    return 0
                elif joustRectObj.collidepoint( (mousex, mousey) ): ## start the joust sequence
                    horseSound.play()
                    pygame.time.wait(500)
                    
                    xPosLeft = 101 ## move the left knight
                    xPosRight = WINDOWWIDTH-101 ## move the player knight
                    
                    BGIMAGE = cityJoustImage
                    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))

                    
                    prevOppPos = knight.getPositions()

                    legsPos = 0
                    horsesRunningSound.play()

                    ## loop until the knights collide
                    while(not playerSprite.smallRect.colliderect(opponentSprite.smallRect)): 
                        DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
                        
                        
                        if xPosLeft % 9 == 0:## limit the frequency that the knight changes lance and shiel positions
                            oppPos = knight.getPositions()
                            prevOppPos = oppPos
                            
                        ## update shield/lance positions
                        oppPos=prevOppPos
                        playerPos = PLAYER.getPositions()

                        ##update sprites
                        playerSpriteGroup.update(xPosRight, playerPos)
                        opponentSpriteGroup.update(xPosLeft, oppPos)
                        rightLegsSpriteGroup.update(xPosRight, legsPos)
                        leftLegsSpriteGroup.update(xPosLeft, legsPos)

                        ## draw sprites and graphics
                        opponentSpriteGroup.draw(DISPLAYSURF)
                        leftLegsSpriteGroup.draw(DISPLAYSURF)
                        DISPLAYSURF.blit(fenceImage, fenceRectObj)
                        
                        playerSpriteGroup.draw(DISPLAYSURF)
                        rightLegsSpriteGroup.draw(DISPLAYSURF)
                        
                            
                        for event in pygame.event.get():   ## get the new positions                      
                            shieldStr, lanceStr, shieldPos, lancePos =changePositions(event, shieldStr, lanceStr, shieldPos, lancePos, shieldLowRectObj, shieldHighRectObj, lanceLowRectObj, lanceHighRectObj)

                        ##highlight the positions for lance and shield
                        highlightLanceSurfaceObj = highlightFontObj.render(lanceStr, True, PURPLE)
                        highlightLanceRectObj = highlightLanceSurfaceObj.get_rect()
                        highlightLanceRectObj.center = (WINDOWWIDTH-150, lancePos)

       
                        highlightShieldSurfaceObj = highlightFontObj.render(shieldStr, True, PURPLE)
                        highlightShieldRectObj = highlightShieldSurfaceObj.get_rect()
                        highlightShieldRectObj.center = (WINDOWWIDTH-300, shieldPos)

                        
                        DISPLAYSURF.blit(shieldPosSurfaceObj, shieldPosRectObj)
                        DISPLAYSURF.blit(shieldHighSurfaceObj, shieldHighRectObj)
                        DISPLAYSURF.blit(shieldLowSurfaceObj, shieldLowRectObj)
                        DISPLAYSURF.blit(lancePosSurfaceObj, lancePosRectObj)
                        DISPLAYSURF.blit(lanceHighSurfaceObj, lanceHighRectObj)
                        DISPLAYSURF.blit(lanceLowSurfaceObj, lanceLowRectObj)
                        DISPLAYSURF.blit(highlightShieldSurfaceObj, highlightShieldRectObj)
                        DISPLAYSURF.blit(highlightLanceSurfaceObj, highlightLanceRectObj)
                        
                        ## change knight and player positions
                        xPosLeft = xPosLeft + 4
                        xPosRight = xPosRight - 4
                        legsPos = legsPos + 1
                        
                        pygame.display.update()
                        

                    horsesRunningSound.stop()
                    crashSound.play()
                    pygame.time.wait(100)
                    
                    ## get the final positions of the player and opposing knight
                    oppPositions = oppPos
                    print "Opponent: ", oppPositions
                    
                    playerPositions = PLAYER.getPositions()
                    print PLAYER.getName(), ": ", playerPositions

    ##################Check the results of each jousting round
                    results = joustMatch.getResults(playerPositions, oppPositions)
                    DISPLAYSURF.blit(cloudImage, cloudRectObj)
                    if(not results): ## if a tie then check player and opponent strength to see if there is a tie breaker
                        if(knight.getStrength()-5 > PLAYER.getStrength()):
                            results =2
                            DISPLAYSURF.blit(tieSurfaceObj, tieRectObj)
                            pygame.display.update()
                            pygame.time.wait(1500)
                            print "You tied but the opponent is stronger so he won"
                        elif(knight.getStrength() < PLAYER.getStrength()-5):
                            print "You tied but the your're stronger so you won"
                            results =1
                            DISPLAYSURF.blit(tieSurfaceObj, tieRectObj)
                            pygame.display.update()
                            pygame.time.wait(1500)
                        else:
                            DISPLAYSURF.blit(tieSurfaceObj, tieRectObj)
                            pygame.display.update()
                            pygame.time.wait(2000)
                    ## if the player won
                    if(results ==1):
                        DISPLAYSURF.blit(winSurfaceObj, winRectObj)
                        playerScore = playerScore + 1
                        pygame.display.update()
                        pygame.time.wait(2000)
                    ## if the player lost
                    if(results ==2):
                        DISPLAYSURF.blit(loseSurfaceObj, loseRectObj)
                        pygame.display.update()
                        oppScore = oppScore +1
                        pygame.time.wait(2000)
                    ## if the player won 3 rounds
                    if(playerScore == 3):
                        DISPLAYSURF.blit(winMatchSurfaceObj, winMatchRectObj)
                        DISPLAYSURF.blit(winningsMatchSurfaceObj, winningsMatchRectObj)
                        
                        pygame.display.update()
                        pygame.time.wait(2000)
                        return 1
                    elif(oppScore == 3): ## if opponent won 3 rounds
                        DISPLAYSURF.blit(loseMatchSurfaceObj, loseMatchRectObj)
                        pygame.display.update()
                        pygame.time.wait(2000)
                        return 0
            
                else: ## get new positions
                    shieldStr, lanceStr, shieldPos, lancePos = changePositions(event, shieldStr, lanceStr, shieldPos, lancePos, shieldLowRectObj, shieldHighRectObj, lanceLowRectObj, lanceHighRectObj)
                
        ##update players shield/lance positions before starting to joust
        crashSound.stop()
        ## update sprites with new positions
        playerPos = PLAYER.getPositions()
        playerSpriteGroup.update((WINDOWWIDTH-100), playerPos)
        playerSpriteGroup.draw(DISPLAYSURF)
                    
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def changePositions(event, shieldStr, lanceStr, shieldPos, lancePos, shieldLowRectObj, shieldHighRectObj, lanceLowRectObj, lanceHighRectObj):
    ## get the user input for the new positions
    if event.type == KEYUP:
        if event.key == K_d:
            shieldStr = 'Low'
            shieldPos = 600
            PLAYER.setShieldPos('low')
        elif event.key == K_e:
            shieldStr = 'High'
            shieldPos = 550
            PLAYER.setShieldPos('high')
        elif event.key == K_k:
            lanceStr = 'Low'
            lancePos = 600
            PLAYER.setLancePos('low')
        elif event.key == K_i:
            lanceStr = 'High'
            lancePos = 550
            PLAYER.setLancePos('high')
                 
    if event.type == MOUSEBUTTONDOWN:
        mousex, mousey = event.pos
        if shieldLowRectObj.collidepoint( (mousex, mousey) ):
            BUTTONCLICKSOUND.play()
            shieldStr = 'Low'
            shieldPos = 600
            PLAYER.setShieldPos('low')
        elif shieldHighRectObj.collidepoint( (mousex, mousey) ):
            BUTTONCLICKSOUND.play()
            shieldStr = 'High'
            shieldPos = 550
            PLAYER.setShieldPos('high')
        elif lanceLowRectObj.collidepoint( (mousex, mousey) ):
            BUTTONCLICKSOUND.play()
            lanceStr = 'Low'
            lancePos = 600
            PLAYER.setLancePos('low')
        elif lanceHighRectObj.collidepoint( (mousex, mousey) ):
            BUTTONCLICKSOUND.play()
            lanceStr = 'High'
            lancePos = 550
            PLAYER.setLancePos('high')
    return [shieldStr, lanceStr, shieldPos, lancePos]        

def drawInventory():

    ## button color
    CURRENTCOLOR1 = GRAY
    
    ## text images 
    inventorySurfaceObj = FANCYFONTLARGE.render('Inventory', True, RED)
    inventoryRectObj = inventorySurfaceObj.get_rect()
    inventoryRectObj.center = (WINDOWWIDTH/2, 75)

    shieldsSurfaceObj = FANCYFONTMEDIUM.render('Shields', True, LIGHTBLUE)
    shieldsRectObj = shieldsSurfaceObj.get_rect()
    shieldsRectObj.center = (250, 200)

    lancesSurfaceObj = FANCYFONTMEDIUM.render('Lances', True, LIGHTBLUE)
    lancesRectObj = lancesSurfaceObj.get_rect()
    lancesRectObj.center = (800, 200)

    coinsSurfaceObj = FANCYFONTMEDIUM.render('Coins: ', True, YELLOW)
    coinsRectObj = coinsSurfaceObj.get_rect()
    coinsRectObj.center = (WINDOWWIDTH-275, 650)

    pCoinsSurfaceObj = FANCYFONTMEDIUM.render(str(PLAYER.getCoins()), True, YELLOW)
    pCoinsRectObj = pCoinsSurfaceObj.get_rect()
    pCoinsRectObj.topleft = (WINDOWWIDTH-175, 600)
 
    ## get inventory from player 
    shieldList = PLAYER.getShieldList()
    lanceList = PLAYER.getLanceList()
    shieldYPos = 250
    lanceYPos = 250

    while(True): ## inventory game loop
        
        DISPLAYSURF.fill(BLACK)
        
        backSurfaceObj = FANCYFONTMEDIUM.render('Back', True, CURRENTCOLOR1)
        backRectObj = backSurfaceObj.get_rect()
        backRectObj.center = (100, 650)
        
        for shield in shieldList:
            shieldNameSurfaceObj = FANCYFONTSMALL.render(shield, True, GRAY)
            shieldNameRectObj = shieldNameSurfaceObj.get_rect()
            shieldNameRectObj.topleft = (150, shieldYPos)
            DISPLAYSURF.blit(shieldNameSurfaceObj, shieldNameRectObj)
            shieldYPos = shieldYPos + 65

        shieldYPos=250       
        for lance in lanceList:
            lanceNameSurfaceObj = FANCYFONTSMALL.render(lance, True, GRAY)
            lanceNameRectObj = lanceNameSurfaceObj.get_rect()
            lanceNameRectObj.topleft = (700, lanceYPos)
            DISPLAYSURF.blit(lanceNameSurfaceObj, lanceNameRectObj)
            lanceYPos = lanceYPos + 65
        lanceYPos = 250

        DISPLAYSURF.blit(inventorySurfaceObj, inventoryRectObj)
        DISPLAYSURF.blit(shieldsSurfaceObj, shieldsRectObj)
        DISPLAYSURF.blit(lancesSurfaceObj, lancesRectObj)
        DISPLAYSURF.blit(coinsSurfaceObj, coinsRectObj)

        DISPLAYSURF.blit(pCoinsSurfaceObj, pCoinsRectObj)
   
        DISPLAYSURF.blit(backSurfaceObj, backRectObj)

        checkForQuit()
        mouseX, mouseY = pygame.mouse.get_pos()
        if backRectObj.collidepoint( (mouseX, mouseY) ):
            CURRENTCOLOR1 = YELLOW
        else:
            CURRENTCOLOR1 = GRAY
            
        for event in pygame.event.get():## event loop
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if backRectObj.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    return 0

        pygame.display.update()

        
def drawBlackSmith(city):
    ##Text images
    blackSmithSurfaceObj = FANCYFONTLARGE.render('Blacksmith Shop', True, RED)
    blackSmithRectObj = blackSmithSurfaceObj.get_rect()
    blackSmithRectObj.center = (WINDOWWIDTH/2, 75)

    newShieldSurfaceObj = FANCYFONTMEDIUM.render('New Shield', True, LIGHTBLUE)
    newShieldRectObj = newShieldSurfaceObj.get_rect()
    newShieldRectObj.center = (250, 250)

    newLanceSurfaceObj = FANCYFONTMEDIUM.render('New Lance', True, LIGHTBLUE)
    newLanceRectObj = newLanceSurfaceObj.get_rect()
    newLanceRectObj.center = (800, 250)

    purchasedShieldSurfaceObj = FANCYFONTSMALLMED.render('X', True, RED)
    purchasedShieldRectObj = purchasedShieldSurfaceObj.get_rect()
    purchasedShieldRectObj.center = (250, 250)

    purchasedLanceSurfaceObj = FANCYFONTSMALLMED.render('X', True, RED)
    purchasedLanceRectObj = purchasedLanceSurfaceObj.get_rect()
    purchasedLanceRectObj.center = (800, 250)    

    coinsSurfaceObj = FANCYFONTMEDIUM.render('Coins: ', True, YELLOW)
    coinsRectObj = coinsSurfaceObj.get_rect()
    coinsRectObj.center = (WINDOWWIDTH-275, 650)

    ## sprites for shields and lances
    backText = JoustSprites.TextSprite(FANCYFONTMEDIUM,(100, 650), GRAY, 'Back')
    barbarianText = JoustSprites.TextSprite(FANCYFONTSMALL,(250, 325), GRAY, 'Barbarian $15')
    crusaderText = JoustSprites.TextSprite(FANCYFONTSMALL, (250, 400), GRAY, 'Crusader $25')
    lionText = JoustSprites.TextSprite(FANCYFONTSMALL, (250, 475), GRAY, 'Lion Heart $55')
    dragonText = JoustSprites.TextSprite(FANCYFONTSMALL, (250, 550), GRAY, 'Dragon Scales $100')
    blessedText = JoustSprites.TextSprite(FANCYFONTSMALL, (800, 325), GRAY, 'Blessed Bronze $10')
    blackIronText = JoustSprites.TextSprite(FANCYFONTSMALL, (800, 400), GRAY, 'Black Iron $30')
    heroText = JoustSprites.TextSprite(FANCYFONTSMALL, (800, 475), GRAY, 'Hero Maker $65')
    legendText = JoustSprites.TextSprite(FANCYFONTSMALL, (800, 550), GRAY, 'Legend Slayer $95')

    ## show only the equipment found in that city
    if(city.getName() == 'Isengard'):
        textSpriteGroup = pygame.sprite.Group((backText, lionText, dragonText, heroText, legendText))

    if(city.getName() == 'Yorkshire'):
        textSpriteGroup = pygame.sprite.Group((backText, crusaderText, blackIronText))

    if(city.getName() == 'Norfolk'):
        textSpriteGroup = pygame.sprite.Group((barbarianText, backText, blessedText))


    while True: ## blacksmith game loop
    
        #### draw the lances and shields
        DISPLAYSURF.fill(BLACK)   
        DISPLAYSURF.blit(blackSmithSurfaceObj, blackSmithRectObj)
        DISPLAYSURF.blit(newShieldSurfaceObj, newShieldRectObj)
        DISPLAYSURF.blit(newLanceSurfaceObj, newLanceRectObj)
        DISPLAYSURF.blit(coinsSurfaceObj, coinsRectObj)

        textSpriteGroup.update(YELLOW)
        textSpriteGroup.draw(DISPLAYSURF)
        
        playerShields = PLAYER.getShieldList()
        playerLances = PLAYER.getLanceList()

        ## draw the equipmen in that city and check if it has already been purchased
        if(city.getName() == 'Norfolk'):
            if(barbarianShield.getName() in playerShields):
                DISPLAYSURF.blit(purchasedShieldSurfaceObj, barbarianText.rect)
            if(blessedLance.getName() in playerLances):
                DISPLAYSURF.blit(purchasedLanceSurfaceObj, blessedText.rect)
            
        if(city.getName() == 'Yorkshire'):
            if(crusadersShield.getName() in playerShields):  
                DISPLAYSURF.blit(purchasedShieldSurfaceObj, crusaderText.rect)
            if(blackIronLance.getName() in playerLances):
                DISPLAYSURF.blit(purchasedLanceSurfaceObj, blackIronText.rect)

        if(city.getName() == 'Isengard'):
            if(lionShield.getName() in playerShields):  
                DISPLAYSURF.blit(purchasedShieldSurfaceObj, lionText.rect)
        
            if(dragonShield.getName() in playerShields):  
                DISPLAYSURF.blit(purchasedShieldSurfaceObj, dragonText.rect)
        
            if(heroLance.getName() in playerLances):
                DISPLAYSURF.blit(purchasedLanceSurfaceObj, heroText.rect)

            if(legendLance.getName() in playerLances):
                DISPLAYSURF.blit(purchasedLanceSurfaceObj, legendText.rect)


        ## update player coins
        pCoinsSurfaceObj = FANCYFONTMEDIUM.render(str(PLAYER.getCoins()), True, YELLOW)
        pCoinsRectObj = pCoinsSurfaceObj.get_rect()
        pCoinsRectObj.topleft = (WINDOWWIDTH-175, 600)
        DISPLAYSURF.blit(pCoinsSurfaceObj, pCoinsRectObj)

          
        checkForQuit()
        for event in pygame.event.get(): ## event loop
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if backText.rect.collidepoint( (mousex, mousey) ):
                    BUTTONCLICKSOUND.play()
                    pygame.time.wait(500)
                    return 0
                
                if(city.getName() == 'Norfolk'):
                    if barbarianText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(barbarianShield)
                    elif blessedText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(blessedLance)
                        
                if(city.getName() == 'Yorkshire'):
                    if crusaderText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(crusadersShield)
                    elif blackIronText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(blackIronLance)
                        
                if(city.getName() == 'Isengard'):
                    if lionText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(lionShield)
                    elif dragonText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(dragonShield)
                    elif heroText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(heroLance)
                    elif legendText.rect.collidepoint( (mousex, mousey) ):
                        BUTTONCLICKSOUND.play()
                        pygame.time.wait(500)
                        purchase(legendLance)
                
    
        pygame.display.update()

        
def purchase(equipment):

    ## text images
    outOfStockSurfaceObj = FANCYFONTSMALLMED.render('Out of Stock', True, YELLOW)
    outOfStockRectObj = outOfStockSurfaceObj.get_rect()
    outOfStockRectObj.center = (WINDOWWIDTH/2, 175)

    tooExpensiveSurfaceObj = FANCYFONTSMALLMED.render('Need More Coins', True, YELLOW)
    tooExpensiveRectObj = tooExpensiveSurfaceObj.get_rect()
    tooExpensiveRectObj.center = (WINDOWWIDTH/2, 175)

    #String to display the strength added
    strength = str(equipment.getStrength())
    addedStrength = '+ '
    addedStrength += strength
    addedStrength += ' Strength'
    
    strengthSurfaceObj = FANCYFONTMEDIUM.render(addedStrength, True, LIGHTRED)
    strengthRectObj = strengthSurfaceObj.get_rect()
    strengthRectObj.center = (WINDOWWIDTH/2, 450)

    ## get what the player already has
    playerEquipment = PLAYER.getEquipmentList()

    ## check that the player has enough money and that they don't already have the equipment
    if((equipment.getPrice() > PLAYER.getCoins()) and (not equipment.getName() in playerEquipment)):
        DISPLAYSURF.blit(tooExpensiveSurfaceObj, tooExpensiveRectObj)
        pygame.display.update()
        pygame.time.wait(1200)
        
    
    elif(equipment.getName() in playerEquipment):
        DISPLAYSURF.blit(outOfStockSurfaceObj, outOfStockRectObj)
        pygame.display.update()
        pygame.time.wait(1200)
    
    else:
        equipment.purchase()
        PLAYER.addEquipment(equipment)
        DISPLAYSURF.blit(strengthSurfaceObj, strengthRectObj)
        pygame.display.update()
        pygame.time.wait(1200)

        
    
    
def gameCompleted():

    ##text images
    congratsSurfaceObj = FANCYFONTMEDIUM.render('Congrats You Beat the Game!!', True, LIGHTBLUE)
    congratsRectObj = congratsSurfaceObj.get_rect()
    congratsRectObj.center = (WINDOWWIDTH/2, 350)

    freeSurfaceObj = FANCYFONTMEDIUM.render('JoustLandia is Now Free!!', True, LIGHTBLUE)
    freeRectObj = freeSurfaceObj.get_rect()
    freeRectObj.center = (WINDOWWIDTH/2, 550)

    logoSmallImg = pygame.image.load(os.path.join('graphics','logoSmall.png'))
    logoSmallRectObj = logoSmallImg.get_rect()
    logoSmallRectObj.center = (WINDOWWIDTH/2, 130) 

    ## game completed music
    beatGame = pygame.mixer.Sound(os.path.join('sounds', 'beatGame.wav'))

    beatGame.play()
 
    while True: ## game completed loop
        
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(logoSmallImg, logoSmallRectObj)
        DISPLAYSURF.blit(congratsSurfaceObj, congratsRectObj)
        DISPLAYSURF.blit(freeSurfaceObj, freeRectObj)
        
        for event in pygame.event.get((QUIT,KEYUP)):
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        pygame.display.update()
        
def checkForQuit():
    #event handling loop
    for event in pygame.event.get((QUIT,KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()





































    
