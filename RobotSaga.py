# Copyright SAGA 2019
# Not to be duplicated without express consent of
# original members. Not for release.
#
# Note: Layer 0 is for loading screens, layer 1 is for menu text/sprites, layer 2 is for menus, 3-5 for sprites, 6 for background
#
#
#
#
#
#
#
#
#
#
#
#
#.


import random
import gui
import time
import thread
import os




        ####################
        #                  #
        #     CONSTANTS    #
        #                  #
        #    (MIGHT BE     #
        #     MOVED TO     #
        #  STARTUP CLASS)  #
        #                  #
        #                  #
        ####################


        # used for movement animations. Lowest stable is .12
moveAnimationSleep = .12  # any lower and coords get messed up


#BITS is how many pixels are in each texture
BITS = 32
#how many tiles there are wide
WIDTH_TILES = 32
#how many tiles there are tall
HEIGHT_TILES = 18
MAX_BEINGS = 6
MAX_INVENTORY = 10
TOWN_AREA = None
E_FIELD_AREA = None
NE_FIELD_AREA = None
N_FIELD_AREA = None
DUNGEON_AREA = None
CURRENT_AREA = None
CURRENT_BG = None
bot1 = None



# Basic class for turn counter instances.

class TurnCounter():
  def __init__(self):
        self.turn = 0


# Main turn counter for game turns

counter = TurnCounter()


    #CONTAINERS
#beings
currentBeingList = []
#interactable objects
objectList = []
#gore pieces
gibList = []
#animated sprites
animatedSpriteList = []
#light sources
lightSources = []


##class CoreGame():   experimented with a class to hold game data. could be addressed later
#    def __init__(self):
        #add select game folder (to allow more portable loading of assets to path)
try:
           path #test to see if path exists
except NameError: #if path does not exist make new path
           printNow("Please select your game install folder")
           path = pickAFolder()
else: printNow("Welcome Back") #welcome the player back to the game







# Sprite paths for beings. Arrays in form [back, front, left, right,
# moving left, moving right, moving front, moving back]

userSpritePaths = [path + "RobotSprites/botBlueBack.gif",
               path + "RobotSprites/botBlueFront.gif",
               path + "RobotSprites/botBlueSideLeft.gif",
               path + "RobotSprites/botBlueSideRight.gif",
               path + "RobotSprites/botBlueMovingLeft.gif",
               path + "RobotSprites/botBlueMovingRight.gif",
               path + "RobotSprites/botBlueMovingFront.gif",
               path + "RobotSprites/botBlueMovingBack.gif",]
friendlyGreenSpritePaths = [path + "RobotSprites/botGreenBack.gif",
               path + "RobotSprites/botGreenFront.gif",
               path + "RobotSprites/botGreenSideLeft.gif",
               path + "RobotSprites/botGreenSideRight.gif",
               path + "RobotSprites/botGreenMovingLeft.gif",
               path + "RobotSprites/botGreenMovingRight.gif",
               path + "RobotSprites/botGreenMovingFront.gif",
               path + "RobotSprites/botGreenMovingBack.gif",]
friendlyOrangeSpritePaths = [path + "RobotSprites/botOrangeBack.gif",
               path + "RobotSprites/botOrangeFront.gif",
               path + "RobotSprites/botOrangeSideLeft.gif",
               path + "RobotSprites/botOrangeSideRight.gif",
               path + "RobotSprites/botOrangeMovingLeft.gif",
               path + "RobotSprites/botOrangeMovingRight.gif",
               path + "RobotSprites/botOrangeFront.gif",
               path + "RobotSprites/botOrangeBack.gif",]
friendlyPinkSpritePaths = [path + "RobotSprites/botPinkBack.gif",
               path + "RobotSprites/botPinkFront.gif",
               path + "RobotSprites/botPinkSideLeft.gif",
               path + "RobotSprites/botPinkSideRight.gif",
               path + "RobotSprites/botPinkMovingLeft.gif",
               path + "RobotSprites/botPinkMovingRight.gif",
               path + "RobotSprites/botPinkFront.gif",
               path + "RobotSprites/botPinkBack.gif",]
friendlyYellowSpritePaths = [path + "RobotSprites/botYellowBack.gif",
               path + "RobotSprites/botYellowFront.gif",
               path + "RobotSprites/botYellowSideLeft.gif",
               path + "RobotSprites/botYellowSideRight.gif",
               path + "RobotSprites/botYellowMovingLeft.gif",
               path + "RobotSprites/botYellowMovingRight.gif",
               path + "RobotSprites/botYellowFront.gif",
               path + "RobotSprites/botYellowBack.gif",]
blueEnemySpritePaths = [path + "RobotSprites/blueRobotBack.gif",
               path + "RobotSprites/blueRobotFront.gif",
               path + "RobotSprites/BlueRobotSideLeft.gif",
               path + "RobotSprites/BlueRobotSideRight.gif",
               path + "RobotSprites/BlueRobotMovingLeft.gif",
               path + "RobotSprites/BlueRobotMovingRight.gif",
               path + "RobotSprites/BlueRobotMovingFront.gif",
               path + "RobotSprites/BlueRobotMovingBack.gif",]
greenEnemySpritePaths = [path + "RobotSprites/GreenRobotBack.gif",
               path + "RobotSprites/GreenRobotFront.gif",
               path + "RobotSprites/GreenRobotSideLeft.gif",
               path + "RobotSprites/GreenRobotSideRight.gif",
               path + "RobotSprites/GreenRobotMovingLeft.gif",
               path + "RobotSprites/GreenRobotMovingRight.gif",
               path + "RobotSprites/GreenRobotFront.gif",
               path + "RobotSprites/GreenRobotBack.gif",]
redEnemySpritePaths = [path + "RobotSprites/RedRobotBack.gif",
               path + "RobotSprites/RedRobotFront.gif",
               path + "RobotSprites/RedRobotSideLeft.gif",
               path + "RobotSprites/RedRobotSideRight.gif",
               path + "RobotSprites/RedRobotMovingLeft.gif",
               path + "RobotSprites/RedRobotMovingRight.gif",
               path + "RobotSprites/RedRobotFront.gif",
               path + "RobotSprites/RedRobotBack.gif",]
purpleEnemySpritePaths = [path + "RobotSprites/PurpleRobotBack.gif",
               path + "RobotSprites/PurpleRobotFront.gif",
               path + "RobotSprites/PurpleRobotSideLeft.gif",
               path + "RobotSprites/PurpleRobotSideRight.gif",
               path + "RobotSprites/PurpleRobotMovingLeft.gif",
               path + "RobotSprites/PurpleRobotMovingRight.gif",
               path + "RobotSprites/PurpleRobotFront.gif",
               path + "RobotSprites/PurpleRobotBack.gif",]
yellowEnemySpritePaths = [path + "RobotSprites/YellowRobotBack.gif",
               path + "RobotSprites/YellowRobotFront.gif",
               path + "RobotSprites/YellowRobotSideLeft.gif",
               path + "RobotSprites/YellowRobotSideRight.gif",
               path + "RobotSprites/YellowRobotMovingLeft.gif",
               path + "RobotSprites/YellowRobotMovingRight.gif",
               path + "RobotSprites/YellowRobotFront.gif",
               path + "RobotSprites/YellowRobotBack.gif",]
shopKeeperSpritePaths = [path + "RobotSprites/ShopkeeperbotBack.gif",
                         path + "RobotSprites/ShopkeeperbotFront.gif",
                         path + "RobotSprites/ShopkeeperbotLeft.gif",
                         path + "RobotSprites/ShopkeeperbotRight.gif",
                         path + "RobotSprites/ShopkeeperbotMovingLeft.gif",
                         path + "RobotSprites/ShopkeeperbotMovingRight.gif",
                         path + "RobotSprites/ShopkeeperbotMovingFront.gif",
                         path + "RobotSprites/ShopkeeperbotMovingBack.gif",
                         path + "RobotSprites/ShopkeeperbotCloseup.gif",]



# Sprites for light sources.  Arrays in form [off, on, bright]
lightpostSpritePaths = [path + "ObjectSprites/lampOff.gif",
                        path + "ObjectSprites/lampOn.gif",
                        path + "ObjectSprites/lampBright.gif"]
torchSpritePaths = [path + "ObjectSprites/metalTorchOff.gif",
                        path + "ObjectSprites/metalTorchOn1.gif.gif",
                        path + "ObjectSprites/metalTorchOn2.gif.gif"]

bigTorchSpritePaths = [path + "ObjectSprites/metalBigTorchOff.gif",
                        path + "ObjectSprites/metalBigTorchOn1.gif",
                        path + "ObjectSprites/metalBigTorchOn2.gif"]
healingStationSpritePaths = [path + "ObjectSprites/rechargeStation1.gif",
                        path + "ObjectSprites/rechargeStation2.gif",
                        path + "ObjectSprites/rechargeStation3.gif",
                        path + "ObjectSprites/rechargeStation4.gif"]

#Not sure if needed, might delete
menuSpritePaths = [path + "Menu/menuDefault.png",
                    path + "Menu/menuItem.png",
                    path + "Menu/menuStatus.png",
                    path + "Menu/menuEquip.png"]

# Dictionaries for items
# Numbers correspond to stats


# Weapon dictionary. Array in form [attack power, weaponSprites[], burnable, flamingWeaponSprites[], range, currencyValue]
# weaponSprites and flamingWeaponSprites arrays in form [first up frame, first down frame, first left frame,
# first right frame, repeat for frames two and three]
weaponStatsList = {
    "Stick": [1, [path + "WeaponSprites/Stick/stickUp1.gif",
                  path + "WeaponSprites/Stick/stickDown1.gif",
                  path + "WeaponSprites/Stick/stickLeft1.gif",
                  path + "WeaponSprites/Stick/stickRight1.gif",
                  path + "WeaponSprites/Stick/stickUp2.gif",
                  path + "WeaponSprites/Stick/stickDown2.gif",
                  path + "WeaponSprites/Stick/stickLeft2.gif",
                  path + "WeaponSprites/Stick/stickRight2.gif",
                  path + "WeaponSprites/Stick/stickUp3.gif",
                  path + "WeaponSprites/Stick/stickDown3.gif",
                  path + "WeaponSprites/Stick/stickLeft3.gif",
                  path + "WeaponSprites/Stick/stickRight3.gif",], true, [path + "WeaponSprites/Stick/stickFireUp1.gif",
                  path + "WeaponSprites/Stick/stickFireDown1.gif",
                  path + "WeaponSprites/Stick/stickFireLeft1.gif",
                  path + "WeaponSprites/Stick/stickFireRight1.gif",
                  path + "WeaponSprites/Stick/stickFireUp2.gif",
                  path + "WeaponSprites/Stick/stickFireDown2.gif",
                  path + "WeaponSprites/Stick/stickFireLeft2.gif",
                  path + "WeaponSprites/Stick/stickFireRight2.gif",
                  path + "WeaponSprites/Stick/stickFireUp3.gif",
                  path + "WeaponSprites/Stick/stickFireDown3.gif",
                  path + "WeaponSprites/Stick/stickFireLeft3.gif",
                  path + "WeaponSprites/Stick/stickFireRight3.gif"], 1, 0],
    "Rock": [2, [path + "WeaponSprites/Rock/rockUp1.gif",
                  path + "WeaponSprites/Rock/rockDown1.gif",
                  path + "WeaponSprites/Rock/rockLeft1.gif",
                  path + "WeaponSprites/Rock/rockRight1.gif",
                  path + "WeaponSprites/Rock/rockUp2.gif",
                  path + "WeaponSprites/Rock/rockDown2.gif",
                  path + "WeaponSprites/Rock/rockLeft2.gif",
                  path + "WeaponSprites/Rock/rockRight2.gif",
                  path + "WeaponSprites/Rock/rockUp3.gif",
                  path + "WeaponSprites/Rock/rockDown3.gif",
                  path + "WeaponSprites/Rock/rockLeft3.gif",
                  path + "WeaponSprites/Rock/rockRight3.gif",], false, None, 1, 200],
    "Sword": [5, [path + "WeaponSprites/Sword/swordUp1.gif",
                  path + "WeaponSprites/Sword/swordDown1.gif",
                  path + "WeaponSprites/Sword/swordLeft1.gif",
                  path + "WeaponSprites/Sword/swordRight1.gif",
                  path + "WeaponSprites/Sword/swordUp2.gif",
                  path + "WeaponSprites/Sword/swordDown2.gif",
                  path + "WeaponSprites/Sword/swordLeft2.gif",
                  path + "WeaponSprites/Sword/swordRight2.gif",
                  path + "WeaponSprites/Sword/swordUp3.gif",
                  path + "WeaponSprites/Sword/swordDown3.gif",
                  path + "WeaponSprites/Sword/swordLeft3.gif",
                  path + "WeaponSprites/Sword/swordRight3.gif"], false, None, 1, 1000],
    "Botsmasher": [12, [path + "WeaponSprites/Botsmasher/botsmasherUp1.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherDown1.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherLeft1.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherRight1.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherUp2.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherDown2.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherLeft2.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherRight2.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherUp3.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherDown3.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherLeft3.gif",
                  path + "WeaponSprites/Botsmasher/botsmasherRight3.gif"], false, None, 1, 10000]
   }

# Helmet dict. Array in form [def power, spritePath(currently Unused)]
helmStatsList = {
    "Hair": [0, "spritePath"],
    "Leaf": [1, "spritePath"]
    }

# Helmet dict. Array in form [def power, spritePath(currently Unused)]
chestStatsList = {
    "BDaySuit": [0, "spritePath"],
    "Fur Coat": [1, "spritePath"]
    }

# Helmet dict. Array in form [def power, spritePath(currently Unused)]
legsStatsList = {
    "Shame": [0, "spritePath"],
    "Fur Pants": [1, "spritePath"]
    }

# Helmet dict. Array in form [def power, spritePath(currently Unused)]
feetStatsList = {
    "Toes": [0, "spritePath"],
    "Fur Boots": [1, "spritePath"]
    }

# Helmet dict. Array in form [def power, spritePath(currently Unused)]
handStatsList = {
    "Digits": [0, "spritePath"],
    "Fur Gloves": [1, "spritePath"]
    }

#item array. (currently unused)
itemsList = {}  #potions, etc.

#loot table (currently unused)
lootTable = {}


# Direction dict for reference with arrays
directionList = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3
    }

mapNameList = ["town", "dungeon", "path"]




        ####################
        #                  #
        #    FUNCTIONS     #
        #                  #
        ####################




# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Converts the given rawText to a Label object to be added to the
# display, then adds at coordsX, coordsY.



def showText(rawText, coordsX = 1280 * (2/5), coordsY = 0):
    label = gui.Label(rawText)
    label.position = (coordsX, coordsY)
    display.add(rawText, coordsX, coordsY)







# Takes an array of animatable objects and animates them all.
# All sprites in the list must have an animate() member function to call.

def animateSpriteSet(stationaryAnimatedSpriteSet):
    for sprite in stationaryAnimatedSpriteSet:
      sprite.animate()



# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Adds the given gui.Label to the display at the Label's coords (default 0, 0)

def showLabel(label):
    display.add(label, 1280*(2/5), 0)
def removeLabel(label):
    display.remove(label)




# All actions that depend on the turn counter go here. All actions/functions within
# will occur with the passing of each turn (e.g., attack, player-directed movement)

def turnPass():
    global counter
    global currentBeingList
    counter.turn += 1
    if  CURRENT_AREA != TOWN_AREA and len(currentBeingList)< MAX_BEINGS:
      if counter.turn % 100 == 0 and bot1.level > 40:
        spawnThreat5()
      elif counter.turn % 80 == 0 and bot1.level >= 28:
        spawnThreat4()
      elif counter.turn % 40 == 0 and bot1.level >= 19:
        if bot1.level >= 19:
          spawnThreat3()
        elif bot1.level >= 10:
          spawnThreat2()
      elif counter.turn % 20 == 0:
        spawnEnemy()

    for person in currentBeingList:
        if person.hostile == true:
            person.simpleHostileAI()
    if bot1.hp <= 0:
        bot1.coords.x = 0
        bot1.coords.y = 0
        bot1.sprite.spawnSprite()
    clearBadSprites()

    #total action counter to affect shop/store stock


def inventoryFull():
    label = gui.Label("Not enough inventory space!")
    showLabel(label)
    delayRemoveObject(label, 2)


# slides an object to the right one pixel at a time until the object's coords.x == targetXBig.
# parameters:
# object        - object to be moved (must have a sprite)
# targetXBig    - x coord target (must be greater than object.coords.x)

def slideRight(toBeMoved, targetXBig):
    time.sleep(.005)
    toBeMoved.coords.x += 1
    toBeMoved.forwardCoords.x += 1
    display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.x < targetXBig:
        thread.start_new_thread(slideRight, (toBeMoved, targetXBig, sprite))

def slideSpriteDown(toBeMoved, targetYBig):
    time.sleep(.005)
    toBeMoved.coords.y += 1
    display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.y < targetYBig:
        thread.start_new_thread(slideSpriteDown, (toBeMoved, targetYBig))




# Checks player coords to determine if a load is necessary.
# may call loadNewArea
# double calls for garbage sprite cleanup

def loadAreaCheck(player):
    global CURRENT_AREA

    maxAceptableWidth = 960
    maxAceptableHeight = 512
    if CURRENT_AREA.otherAreas:
        currCoord = coordToTileCoord(bot1.coords)
        currSpot = tileCoordToSpot(currCoord)
        if currentMap.getTileDesc(currSpot) == "hole":
            #enter the dungeon!
            coordY = (HEIGHT_TILES/2) * BITS
            coordX = (WIDTH_TILES/2) * BITS
            bot1.coords.y = coordY
            bot1.coords.x = coordX
            loadNewArea(CURRENT_AREA.otherAreas[0])
        elif currentMap.getTileDesc(currSpot) == "door":
            coordY = (HEIGHT_TILES/2) * BITS
            coordX = (WIDTH_TILES/2) * BITS
            bot1.coords.y = coordY
            bot1.coords.x = coordX
            loadNewArea(CURRENT_AREA.otherAreas[0])
    if player.coords.y <= 0:
        bot1.coords.y = maxAceptableHeight
        loadNewArea(CURRENT_AREA.northArea)
        CURRENT_AREA.spawnCoords = Coords(bot1.coords.x, bot1.coords.y)

    elif player.coords.y > maxAceptableHeight:
        bot1.coords.y = BITS #place user one in from the edge
        loadNewArea(CURRENT_AREA.southArea)
        CURRENT_AREA.spawnCoords = Coords(bot1.coords.x, bot1.coords.y)
    elif player.coords.x <= 0:
        bot1.coords.x = maxAceptableWidth
        loadNewArea(CURRENT_AREA.westArea)
        CURRENT_AREA.spawnCoords = Coords(bot1.coords.x, bot1.coords.y)
    elif player.coords.x > maxAceptableWidth:
        bot1.coords.x = BITS #place user one in from the edge
        loadNewArea(CURRENT_AREA.eastArea)
        CURRENT_AREA.spawnCoords = Coords(bot1.coords.x, bot1.coords.y)





# Joins area objects by placing both in the opposite area's opposite
# area attribute.  Used when loading new areas. Arguments should be passed
# as parameters are described (e.g., northArea should be the area to the north).

def joinNorthSouthAreas(northArea, southArea):
    northArea.southArea = southArea
    southArea.northArea = northArea
def joinEastWestAreas(eastArea, westArea):
    eastArea.westArea = westArea
    westArea.eastArea = eastArea
def joinOtherAreas(target, area):
    target.otherAreas.append(area)




# Spawns the passed enemy object. If none is passed, the default spawned enemy is a blue enemy, lv 1,
# with a stick as a weapon

def spawnEnemy(toSpawn = None):
    if toSpawn == None:
      toSpawn = Enemy(None, "Stick", blueEnemySpritePaths, random.randint(0, 10)*32, random.randint(0, 10)*32, 1)
    if toSpawn.name == None:
      global counter
      toSpawn.name = ("EnemyBorn" + str(counter.turn)+str(len(CURRENT_AREA.beingList)))
    if len(CURRENT_AREA.beingList) < MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()


      # Quick spawn commands for higher level enemies
def spawnThreat2():
    global counter
    toSpawn = Threat2Enemy("EnemyBorn" + str(counter.turn)+str(len(CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(CURRENT_AREA.beingList) < MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat3():
    global counter
    toSpawn = Threat3Enemy("EnemyBorn" + str(counter.turn)+str(len(CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(CURRENT_AREA.beingList) < MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat4():
    global counter
    toSpawn = Threat4Enemy("EnemyBorn" + str(counter.turn)+str(len(CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(CURRENT_AREA.beingList) < MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat5():
    global counter
    toSpawn = Threat5Enemy("EnemyBorn" + str(counter.turn)+str(len(CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(CURRENT_AREA.beingList) < MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()




# Spawns a friendly with the given parameters.  Default is green friendly with stick at random location.

def spawnFriendly(name = None, weap = "Stick", spritePaths = friendlyGreenSpritePaths,  x = random.randint(0, 10)*32, y =  random.randint(0, 10)*32):
    if name == None:
      global counter
      name = ("FriendlyBorn" + str(counter.turn))
    while not isTraversable(x, y):
        x = random.randint(0, 10)*32
        y =  random.randint(0, 10)*32
    friendly = Friendly(name, weap, spritePaths, x, y)
    friendly.sprite.spawnSprite()


# Used to remove objects (labels, sprites, etc.) from the display after a delay.
# only call delayRemoveObject.  threadDelayRemoveObject() is not meant to be called
# directly.
# Parameters:
#   object          - An object on the displays self.items list
#   delay           - the amount of time in seconds to delay the removal

def delayRemoveObject(object, delay):
    thread.start_new_thread(threadDelayRemoveObject, (object, delay))
def threadDelayRemoveObject(object, delay):
    time.sleep(delay)
    display.remove(object)






# cleanup for duplicate sprites created when input is given
# too quickly

def clearBadSprites():
    goodSprites = []
    for being in currentBeingList:
        goodSprites.append(being.sprite)
    stop = time.time() + .5
    for sprite in display.items:
      if sprite not in goodSprites and type(sprite) == BeingSprite :
          display.remove(sprite)
      if time.time() >= stop:
          break







# clears giblets from the display()

def clearGibList():
    for sprite in gibList:
        display.remove(sprite)
        gibList.remove(sprite)
        del sprite






# used with thread.start_new_thread(threadRemoveSprite, (timeToWait, sprite))
# in order to despawn a sprite after a delay. For use with animations.
# parameters:
#   timeToWait      - time in seconds to delay the sprite removal
#   sprite          - sprite to be removed

def threadRemoveSprite(timeToWait, sprite):
    time.sleep(timeToWait)
    display.remove(sprite)






#helper Functions
def spotToCoord(spot):
    #if low set to 0d
    if spot < 0: spot = 0
    #if high set to max (should probably just throw error
    if spot > WIDTH_TILES * HEIGHT_TILES: spot = WIDTH_TILES * HEIGHT_TILES - 1
    return Coords(spot % WIDTH_TILES, spot / WIDTH_TILES)


#given tile Coords give tile Spot in 1d array
def tileCoordToSpot(coord):
    return coord.x + coord.y * WIDTH_TILES


#Goes from pixel coords to tile Coords
def coordToTileCoord(coord):
    return Coords(coord.x/BITS, coord.y/BITS)

PIXEL_WIDTH = WIDTH_TILES * BITS
PIXEL_HEIGHT = HEIGHT_TILES * BITS
#Goes from tile spot to pixel coords
def tileSpotToCoord(spot):
    return Coords((spot * BITS)%PIXEL_WIDTH, (spot / WIDTH_TILES)*BITS)

#probably bad?
def coordToTile(coord):
    return coord.x/BITS + (coord.y/BITS) * WIDTH_TILES

#takes pixel coordanates and returns if the tile at that location is
def isTraversable(x, y):
    spot = coordToTile(Coords(x,y))
    return currentMap.isTraversable(spot)


#depricated can Delete
def placeTex(tex, spot, back):
    startx = (spot * BITS) % backWidth;
    starty = ((spot * BITS) / backWidth) * BITS;
    for x in range(0, BITS):
        for y in range(0, BITS):
            setColor(getPixel(back, startx + x, starty + y), getColor(getPixel(tex, x, y)))



# Converts pixel coordinates to "spot" coordinates
def textCoordToSpot(x, y):
  col = texWidth/32
  row = texHeight/32
  return x + y*col

#LEGACY can delete
def getTexture(spot):
    texture = makeEmptyPicture(BITS,BITS)
    #spot to coord conversion
    startx = (spot * BITS) % texWidth;
    starty = ((spot * BITS) / texWidth) * BITS;
    for x in range(0, BITS):
        for y in range(0, BITS):
            setColor(getPixel(texture, x, y), getColor(getPixel(textureMap, x + startx, y + starty)))
    return texture






# intro credits, adjust to add fade, etc.

def loadIntro():
    global loading
    global title
    global startScreen
    global text
    loading.spawnSprite()
    time.sleep(1.5)
    startScreen.spawnSprite()
    loading.removeSprite()
    title.spawnSprite()
    slideSpriteDown(title, 104)
    time.sleep(1.5)
    text.onKeyType(mainMenuAction)
    text.grabFocus()



# Clears the display, sets up layers for use, and displays
# the SAGA logo

def loadingScreen():
    display.removeAll()
    setUpLayers()
    loading.spawnSprite()





# Compacts and stores information about the current area and
# loads the next. The player will be spawned on the opposite side
# of the screen they exited from.
# Parameters:
#     Area      - The area to be loaded

def loadNewArea(area):
    loadingScreen()
    setUpLayers()
    global currentBeingList
    global gibList
    global animatedSpriteList
    global lightSources
    global objectList
    global text
    global display
    global CURRENT_BG
    global currentMap
    global CURRENT_AREA
    global bot1
    #global background_music
    #thread.start_new_thread(music.loop2, (background_music,))
    #background_music = false
    #thread.start_new_thread(music.Stop, (background_music,))
    

    for light in lightSources:
      if light.isOn:
        light.turnOff()
        CURRENT_AREA.wasOn.append(light)
    currentMap = area.mapObject
    CURRENT_BG = area.mapSprite
    CURRENT_AREA = area
    CURRENT_BG.spawnSprite()
    display.add(text)
    try:
      currentBeingList.remove(bot1)
    except:
      None
    currentBeingList = area.beingList
    currentBeingList.append(bot1)
    bot1.area = CURRENT_AREA
    objectList = area.objectList
    gibList = area.gibList
    animatedSpriteList = area.animatedSpriteList
    lightSources = area.lightSources
    for being in currentBeingList:
      being.sprite.spawnSprite()
    for thing in area.objectList:
        thing.sprite.spawnSprite()
    for gib in gibList:
        display.add(gib)
    loading.removeSprite()

    for light in CURRENT_AREA.wasOn:
        light.turnOn()
    for sprite in CURRENT_AREA.persistentAnimations:
        sprite.animate()
    text.grabFocus()
    bot1.hpBar.updateBar()
    bot1.wallet.updateWalletDisplay()
    turnPass()
  



 # Adds 7 sprites as placeholders to create layers
 # for use with future sprites

def setUpLayers():
    layer0.spawnSprite()
    layer1.spawnSprite()
    layer2.spawnSprite()
    layer3.spawnSprite()
    layer4.spawnSprite()
    layer5.spawnSprite()
    layer6.spawnSprite()







# Default keybindings/controls

def keyAction(a):
  bot1Ready = (bot1.weapon.displayed == false and bot1.isMoving == false)
  if a == "w":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveUp()
        turnPass()
  elif a == "s":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveDown()
        turnPass()
  elif a == "a":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveLeft()
        turnPass()
  elif a == "d":
    if bot1Ready:
        bot1.isMoving = true
        bot1.moveRight()
        turnPass()
  elif a == "W":
        bot1.faceUp()
  elif a == "A":
        bot1.faceLeft()
  elif a == "S":
        bot1.faceDown()
  elif a == "D":
        bot1.faceRight()

  elif a == "f": #attack
    if bot1Ready:
        bot1.meleeAtk()
        turnPass()
  elif a == "g": #steal
    if bot1Ready:
        bot1.steal(bot1.getFrontTarget())
        turnPass()
  elif a == "q":
    print("NotImplementedAtAll")
  elif a == "t":
    print("not implemented")
  elif a == "v":
    bot1.talk()
  elif a == " ":
      bot1.activateTarget()

     #Menu Logic

  elif a == "m": #Activates menu, switches to menu controls
    if bot1Ready:
        defaultMenu.sprite.spawnSprite()
        text.onKeyType(menuAction)


def menuAction(menuInput):
  bot1Ready = (bot1.weapon.displayed == false and bot1.isMoving == false)
  if menuInput == "u":
    if bot1Ready:
        statusMenu.sprite.spawnSprite()
        stats = Menu()
        stats= stats.Menu.statusItems
        stats.Menu.showLabels


  elif menuInput == "i":
    if bot1Ready:
        # textBox.sprite.spawnSprite()
        itemMenu.sprite.spawnSprite()


#Not in use, placeholder
  elif menuInput == "q":
    if bot1Ready:
      print "When this works, it will quit game."

  elif menuInput == "m":
    if bot1Ready:
      statusMenu.sprite.removeSprite()
      itemMenu.sprite.removeSprite()
      defaultMenu.sprite.removeSprite()
      text.onKeyType(keyAction)


"""
defaultMenu.sprite.spawnSprite()
itemMenu.sprite.spawnSprite()
equipMenu.sprite.spawnSprite()
statusMenu.sprite.spawnSprite()
"""





def mainMenuAction(input):
  global title
  global startScreen
  global text
  text.onKeyType(blockKeys)
  title.removeSprite()
  startScreen.removeSprite()
  if input == "1":
    loadBot()
  else:
    newBot()
  startGame()

# To pass to getKeyTyped in order to block inputs
# (e.g., during animations or delays)

def blockKeys(a):
    None






# Currently not in use

def initialSetup():
    for item in weaponStatsList:
        lootTable[item] = weaponStatsList[item]
    for item in helmStatsList:
        lootTable[item] = helmStatsList[item]
    for item in chestStatsList:
        lootTable[item] = chestStatsList[item]
    for item in legsStatsList:
        lootTable[item] = legsStatsList[item]
    for item in feetStatsList:
        lootTable[item] = feetStatsList[item]






def damageCalculation(target, damage):
  if target != bot1:
    target.hostile = true
  target.changeHp(damage*(-1))
  target.displayDamage()
  if target.hp <= 0:
    self.changeXp(target.xpValue)
    global friendlyGreen
    global friendlyOrange
    global shopKeeper
    if target == friendlyGreen:
      del friendlyGreen
    elif target == friendlyOrange:
      del friendlyOrange
    elif target == shopKeeper:
      del shopKeeper

def threadDamageCalculation(self, target, damage, delay):
  time.sleep(delay)
  if target != bot1:
    target.hostile = true
  target.changeHp(damage*(-1))
  target.displayDamage()
  if target.hp <= 0:
    self.changeXp(target.xpValue)
    global friendlyGreen
    global friendlyOrange
    global shopKeeper
    if target == friendlyGreen:
      del friendlyGreen
    elif target == friendlyOrange:
      del friendlyOrange
    elif target == shopKeeper:
      del shopKeeper

def startGame():
  loading.spawnSprite()
  global CURRENT_AREA
  global TOWN_AREA
  global CURRENT_BG
  global currentBeingList
  global objectList
  global gibList
  global animatedSpriteList
  global lightSources
  CURRENT_AREA = TOWN_AREA
  CURRENT_BG = TOWN_AREA.mapSprite
  CURRENT_BG.spawnSprite()
  currentBeingList = TOWN_AREA.beingList
  objectList = TOWN_AREA.objectList
  gibList = TOWN_AREA.gibList
  animatedSpriteList = TOWN_AREA.animatedSpriteList
  lightSources = TOWN_AREA.lightSources
  bot1Spawn = Coords(13*BITS, 1*BITS)
  shopKeeper = ShopKeeper("shopKeep", "Stick", shopKeeperSpritePaths, 3*BITS, 6*BITS)
  shopKeeper.sprite.spawnSprite()
  friendlyOrange = Friendly("orange", "Stick", friendlyOrangeSpritePaths, 8*BITS, 10*BITS)
  friendlyGreen = Friendly("green", "Stick", friendlyGreenSpritePaths, 10*BITS, 10*BITS)
  friendlyOrange.sprite.spawnSprite()
  friendlyGreen.sprite.spawnSprite()
  loadNewArea(TOWN_AREA)#refresh screen, start animations
  loading.removeSprite()
  text.grabFocus()
  text.onKeyType(keyAction)

def newBot():
  global bot1
  bot1 = User("bot1", "Stick", userSpritePaths, TOWN_AREA)
  bot1.area = CURRENT_AREA

def loadBot():
  global bot1
  bot1 = User("bot1", "Stick", userSpritePaths, TOWN_AREA)
  fin = open(path + "SaveData.txt")
  for line in fin:
    if "CharName:" in line:
      bot1.name = line[len("Name:"):line.index('\n')]
    elif "Weapon:" in line:
      bot1.weapon = Weapon(line[len("Weapon:"):line.index('\n')])
    elif "Level:" in line:
      bot1.level = int(line[len("Level:"):line.index('\n')])
    elif "MaxHp:" in line:
      bot1.maxHp = int(line[len("MaxHp:"):line.index('\n')])
    elif "CurrentHp:" in line:
      bot1.maxHp = int(line[len("CurrentHp:"):line.index('\n')])
    elif "Xp:" in line:
      bot1.xp = int(line[len("Xp:"):line.index('\n')])
    elif "Atk:" in line:
      bot1.atk = int(line[len("Atk:"):line.index('\n')])
    elif "Def" in line:
      bot1.df = int(line[len("Def:"):line.index('\n')])
    elif "Wallet" in line:
      bot1.changeWallet(int(line[len("Wallet:"):line.index('\n')]))
  fin.close()

def saveBot():
  global bot1
  fout = open(path + "SaveData.txt", 'w')
  fout.write("CharName:"+str(bot1.name)+"\n")
  fout.write("Weapon:"+str(bot1.weapon.name)+"\n")
  fout.write("Level:"+str(bot1.level)+"\n")
  fout.write("MaxHp:"+str(bot1.maxHp)+"\n")
  fout.write("CurrentHp:"+str(bot1.hp)+"\n")
  fout.write("Xp:"+str(bot1.xp)+"\n")
  fout.write("Atk:"+str(bot1.atk)+"\n")
  fout.write("Def:"+str(bot1.df)+"\n")
  fout.write("Wallet:"+str(bot1.wallet.value)+"\n")
  fout.close()


        ####################
        #                  #
        #      CLASSES     #
        #                  #
        ####################


    # A custom class created to override gui.Display's default destructor.

class CustomDisplay(gui.Display):


  def __init__(self, title = "", width = 600, height = 400, x=0, y=0, color = None):
    gui.Display.__init__(self, title, width, height, x, y, color)
  def __del__(self):
    #insert stop music logic here
    music.Stop(move)
    music.Stop(dead_sound)
    music.Stop(quieter_music)
    music.Stop(background_music1)
    music.Stop(dungeon_sound)


    gui.display.__del__(self)













    # The following class holds area-specific information for use in tracking
    # and loading.
    # Constructor Parameters:
    #    mapSprite            - Sprite object containing the map image
    #    mapObject            - Map object containing the collision/grid info
    #    persistantAnimations - Any persistant animated objects for the map
    #
    # Members:
    #    beingList            - List of all beings within the area
    #    objectList           - List of all objects within the area
    #    gibList              - List of all giblets within the area
    #    animatedSpriteList   - List of all animated sprites within the area
    #    lightSources         - List of all lightSources in the area
    #    mapSprite            - Sprite object containing the map image
    #    mapObject            - Map object containing the collision/grid info
    #    spawnCoords          - Coords object containing the areas player-spawn area
    #    persistantAnimations - Any persistant animated objects for the map
    #    wasOn                - List of lightSources that are on (turn on these when loading area)
    #    northArea            - Area connected to the north of the area
    #    sourth/east/westArea - See above

class Area():
    def __init__(self, mapSprite, mapObject, persistantAnimations = []):
        self.beingList = [] #beings
        self.objectList = [] #lootbags, chests, doodads, etc.
        self.gibList = [] # gore pieces
        self.animatedSpriteList = [] # may be removed
        self.lightSources = [] #lightSources class objects
        self.mapSprite = mapSprite #sprite for maps
        self.mapObject = mapObject #corresponding Map class object
        self.spawnCoords = None #desired spawn location as coords class object
        self.persistentAnimations = persistantAnimations #stationaryAnimatedSprites
        self.wasOn = [] #to keep track of light sources that were on when loading new area
        self.northArea = None #connected area to the north
        self.southArea = None
        self.eastArea = None
        self.westArea = None
        self.otherAreas = []

    def isTraversable(self, being, spot):
        if self.mapObject.isTraversable(spot):
            testCoords = tileSpotToCoord(spot)
            #printNow("TARGET")
            #printNow(str(testCoords.x) + "," + str(testCoords.y))
            #printNow("CURRENT")
            #printNow(str(being.coords.x) + "," + str(being.coords.y))
            for thing in self.beingList:
                #printNow(thing.name)
                if thing.name == being.name:
                    continue
                #printNow(str(thing.coords.x) + "," + str(thing.coords.y))
                #printNow(str(being.coords.x) + "," + str(being.coords.y))
                if testCoords.x == thing.coords.x and testCoords.y == thing.coords.y:
                    #printNow("Thing in spot")
                    return false
            return true
        return false

    def activateAnimations(self):
        for animatedSprite in self.persistentAnimations:
          animatedSprite.animate()












# universal coordinates object. Coords in pixels.

class Coords():
  def __init__(self, x, y):
    self.x = x
    self.y = y












    # Object that holds collision/terrain information

class Tile():
  def __init__(self, isTraversable, isPassable, isTough, desc):
    self.desc = desc
    #self.tileImg = tile
    #can a being walk over
    self.isTraversable = isTraversable
    #can a projectile go over
    self.isPassable = isPassable
    #ai gets 2 turns if player is on this tile
    self.isTough = isTough
    self.beings = {} #array of beings in that tile

  def getTraversable(self):
    return self.isTraversable

  def addBeing(self, being):
    self.beings.append(being)

  def getDesc(self):
    return self.desc












    # Object that holds collision/terrain information

class Map():
    def __init__(self, tileMap):
        #self.map = back
        self.tileMap = {} #change to make map
        self.beings = {} #master holder for all of the beings
        self.updateMap(tileMap)

    def placeTex(self, tex, spot):
        self.tileMap.update({spot: tex})

    def getTileDesc(self, spot):
        printNow(spot)
        printNow(self.tileMap[spot].desc)
        return self.tileMap[spot].desc


    def placeStruct(self, struct, spot, desc):
        startx = (spot * BITS) % backWidth
        starty = ((spot * BITS) / backWidth) * BITS
        if desc == "tree":
            printNow("Tree at: " + str(startx) + " " + str(starty))


    def updateMap(self, tiles):
        for spot in range(0, len(tiles)):
            if tiles[spot] == "g": self.placeTex(grass, spot)
            elif tiles[spot] == "l": self.placeTex(lavaRock, spot)
            elif tiles[spot] == "s": self.placeTex(stone, spot)
            elif tiles[spot] == "S": self.placeTex(stoneWall, spot)
            elif tiles[spot] == "d": self.placeTex(dirt, spot)
            elif tiles[spot] == "D": self.placeTex(dirtWall, spot)
            elif tiles[spot] == "w": self.placeTex(water, spot)
            elif tiles[spot] == "f": self.placeTex(fence, spot)
            elif tiles[spot] == "L": self.placeTex(lava, spot)
            elif tiles[spot] == "H": self.placeTex(hole, spot)
            elif tiles[spot] == ".": self.placeTex(blank, spot)
            elif tiles[spot] == ",": self.placeTex(blank, spot)
            elif tiles[spot] == "o": self.placeTex(door, spot)
            elif tiles[spot] == "h": self.placeStruct(house, spot, "house")
            elif tiles[spot] == "t": self.placeStruct(tree1, spot, "tree")
            elif tiles[spot] == "c": self.placeStruct(chest, spot, "chest")


    def isTraversable(self, spot):
        printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1:
            return false
        return self.tileMap[spot].getTraversable()





    # class for placeable objects (torches, trees, blocks, tc.)
    # Constructor Parameters:
    #    filepaths            - List of image filepaths in form [stationary, animate1, animate2]
    #    x                    - x coords in pixels
    #    y                    - y coords in pixels
    #    layer                - layer in relation to other objects (layer 0 is closest to the screen/front
    #
    # Members:
    #    destructible         - bool indicating whether or not the object can be destroyed
    #    coords               - Coords object holding location
    #    layer                - layer in relation to other objects (layer 0 is closest to the screen/front
    #    spriteList           - List of image filepaths in form [stationary, animate1, animate2]
    #    sprite               - Sprite object holding the default sprite
    #    animatedSprite       - StationaryAnimatedSprite object holding the animation for the doodad
    #    isAnimating          - bool indicating animation activity

class Doodad():
    def __init__(self, filepaths, x, y, layer = 3):
        self.destructible = false
        self.coords = Coords(x, y)
        self.layer = layer
        self.spriteList = filepaths
        self.sprite = Sprite(filepaths[0], self, layer)
        self.isAnimating = false
        self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], x, y, self.layer)
        self.sprite.spawnSprite()
        self.type = "doodad"
        objectList.append(self)


class Activatable(Doodad):
    def __init__(self, filepaths, x, y, onActivateFunction, layer = 3):
      Doodad.__init(self, filepaths, x, y, layer)

    def activate(self):
      onActivateFunction()


class HealingStation(Doodad):
    def __init__(self, filepaths, x, y, layer = 2):
      Doodad.__init__(self, filepaths, x, y, layer)
      self.animatedSprite = ThreeStageAnimationCycle(self.spriteList[1], self.spriteList[2], self.spriteList[3], self.coords.x, self.coords.y, .2, 2)
      self.type = "healingStation"
    def activate(self, activator):
      activator.hp = activator.maxHp
      activator.hpBar.updateBar()
      for files in activator.bloodySprites:
          try:
            os.remove(files)
          except:
            None
      activator.booodySprites = []
      activator.spritePaths = activator.unchangedSpritePaths
      self.animatedSprite.animateOnce()


# special animated doodad that emits light within 3 tiles. if is burnable, attacking
# with an onFire weapon will turnOn the light source

class LightSource(Doodad):
    def __init__(self, filepaths, x, y, burnable = false, layer = 3):
        Doodad.__init__(self, filepaths, x, y, layer)
        self.isOn = false
        self.type = "light"
        self.isBurnable = burnable
        lightSources.append(self)

    def activate(self):
        if self.isOn == true:
            self.turnOff()
        else:
            self.turnOn()

    def turnOn(self):
        if self.isOn == false:
            self.isOn = true
            self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], self.coords.x, self.coords.y, self.layer)
            self.animatedSprite.animate()
            for being in currentBeingList:
                if distanceX <= BITS*3 and distanceY <= range:
                    being.lightenDarken()
            #self.sprite.removeSprite()
    def turnOff(self):
        if self.isOn == true:
            self.isOn = false
            animatedSpriteList.remove(self.animatedSprite)
            for being in currentBeingList:
                distanceX = abs(being.coords.x - self.coords.x)
                distanceY = abs(being.coords.y - self.coords.y)
                if distanceX <= BITS*3 and distanceY <= range:
                    being.lightenDarken()








        # Class  "buy/sell" transaction




class Transaction():
    def __init__(self, buyer, seller):
      global bot1
      self.buyer = buyer
      self.seller = seller
      #self.buyingWindowSprite = Sprite()
      #self.sellingWindowSprite = Sprite()
      if seller is bot1:
        self.sellingMode()
      else:
        if len(bot1.inv) < MAX_INVENTORY:
          self.buyingMode()
        else:
          inventoryFull()


    def sellingMode(self):
      #self.sellingWindowSprite.spawnSprite()
      for item in seller.inv:
        None
        #Add item to display, selling price, assign selling key
        #set selling price to item.value
        #set keyaction


    def buyingMode(self):
      #self.buyingWindowSprite.spawnSprite()
      for item in buyer.inv:
        None
        #Add item to display, add price to display, assign a buying key
        #set buying price to int(item.value * (1.5))


    def buy(self, item):
      global bot1
      cost = item.value * (1)
      if buyer is bot1:
        cost = int(item.value * (1.5))
      if len(self.buyer.inv) < MAX_INVENTORY:
        self.buyer.changeWallet(cost* (-1))
        self.buyer.inventoryAdd(item)
        self.seller.changeWallet(cost)
        self.seller.inventoryRemove(item)







        # An object used for holding/transporting/tracking currency for beings.
        # Constructor Parameters:
        #   parental              - Owner object
        #   amount                - Initial currency within
        #
        # Members:
        #   value                 - Current currency value
        #   parental              - Owner

class Wallet():
    def __init__(self, parental, amount):
      self.value = amount


      # User-exclusive wallet class.
      # Expansions:
      #   coords                - coords for the HUD icon (User only)
      #   sprite                - sprite for the HUD icon (User only)
      #   label                 - currency amount display for HUD (User only)

class UserWallet(Wallet):
    def __init__(self, parental, amount):
      Wallet.__init__(self, parental, amount)
      self.coords = Coords(960, 16)
      self.sprite = Sprite(path + r"EffectSprites/walletSprite.gif", self, 1)
      self.label = gui.Label(str(self.value), gui.RIGHT)
      self.sprite.spawnSprite()
      display.add(self.label, 1000, 24)



    def updateWalletDisplay(self):
      self.sprite.spawnSprite()
      try:
        removeLabel(self.label)
      except:
        None
      self.label = gui.Label(str(self.value), gui.RIGHT)
      display.add(self.label, 1000, 24)




    # Container object for obtainable items. Often dropped by enemies.
    # Animates in a new thread
    # Constructor Parameters:
    #    itemList             - list of items held by the Lootbag
    #    coords               - coords object holding location
    #    spriteList           - images used for animation
    #    sprite               - current spryte
    #    type                 - used for certain logic checks

class Lootbag():
    def __init__(self, itemList, coords):
        self.contents = itemList
        self.coords = coords
        self.spriteList = [Sprite(path + r"EffectSprites/lootBag.gif", self),
                           Sprite(path + r"EffectSprites/lootBag2.gif", self)]
        self.sprite = self.spriteList[0]
        self.type = "lootbag"

        self.spawnSprite()
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






    def spawnSprite(self):
        display.place(self.sprite, self.coords.x, self.coords.y, 1)
    def removeSprite(self):
        display.remove(self.sprite)



    def threadAnimate(self, x):
        while self in objectList:
            time.sleep(.5)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in objectList:
            self.removeSprite()
            del self










    # Class used when an ownerless sprite is needed

class RawSprite():
    def __init__(self, filename, x, y, layer = 4):
        self.coords = Coords(x, y)
        self.sprite = Sprite(filename, self, layer)
    def spawnSprite(self):
        self.sprite.spawnSprite()
    def spawnSpriteFront(self):
        self.sprite.spawnSpriteFront()
    def spawnSpriteBack(self):
        self.sprite.spawnSpriteBack()
    def removeSprite(self):
        self.sprite.removeSprite()












    # general class for sprites.
    # to display on the main screen.
    # parameters:
    #   filename    - filename in string format
    #   parental      - object that owns this instance. must have it's own coords
    #   layer       - screen layer of sprite, 0 closest to front
    # Members inherited from gui.icon

class Sprite(gui.Icon):

  def __init__(self, filename, parental, layer = 4):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM- LEGACY, NOT SURE OF NECESSITY
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, NOT SURE OF NECESSITY
      self.position = (0,0)              # assume placement at a Display's origin- LEGACY, NOT SURE OF NECESSITY
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, NOT SURE OF NECESSITY
      self.layer = layer
      self.parental = parental

      printNow(filename)
      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality)- LEGACY, NOT SURE OF NECESSITY
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)

      # adds the sprite to the display in the foreground (closest to the user)

  def spawnSpriteFront(self):
      self.layer = 3
      self.spawnSprite()


      # adds the sprite to the display in the background (closest to the map, just in front of it)
      # order number of 3 spawns behind the background

  def spawnSpriteBack(self):
      self.layer = 5
      self.spawnSprite()

      # removes the sprite from the display

  def removeSprite(self):
        display.remove(self)












  # inherits from Sprite. Separated to give
  # ownership to sub-sprites (e.g., weapon)
  #   See sprite for function exacts.

class BeingSprite(Sprite):
  def __init__(self, filename, parental, layer = 4):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM - LEGACY, UNUSED FOR NOW
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, UNUSED FOR NOW
      self.position = (0,0)              # assume placement at a Display's origin - LEGACY, UNUSED FOR NOW
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, UNUSED FOR NOW
      self.icon = gui.ImageIO.read(File(filename))
      self.parental = parental
      self.layer = layer
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality) - LEGACY, UNUSED FOR NOW
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)






      # removes the sprite

  def removeSprite(self):
        display.remove(self)





      # not a huge fan of the weaponOut flag, but it works for now.
      # without the check in putAwayWeap, JES complains

  def displayWeapon(self, sprite, coords):
    display.add(sprite, coords.x, coords.y)






      # hides the weapon. may be unnecessary if we get
      # animations figured out

  def hideWeapon(self):
      display.remove(self.weap)






      #moves sprite to location given

  def moveTo(self, x, y):
      self.parental.coords.x = x
      self.parental.coords.y = y
      display.addOrder(self, 4, x, y)












    # Class for weapon objects. weapName must correspond to a weapon
    # in the weaponList. Contains stats and sprites.
    # Constructor Parameters:
    #    weapName             - string corresponding to a weapon in the weapon dict
    #
    # Members:
    #    name                 - string corresponding to a weapon in the weapon dict
    #    power                - attack power
    #    originalSprites      - default weapon sprites (used with burnable weapons)
    #    isBurnable           - bool that determines whether or not a weapon can burn
    #    range                - weapon range in tiles
    #    coords               - location object. mostly unused
    #    sprites              - current sprite list
    #    sprite               - current sprite
    #    onFire               - bool holding the onFire weapon status
    #    displayed            - bool signifying whether or not the weapon is in use
    #    currentAnimation     - current animation to be used upon attacking
    #    animationUp/Down/etc.- ThreeStageAnimationCycle object holding the corresponding animation
    #    burningAnimationUp...- ThreeStageAnimationCycle object holding the corresponding animation when burning
    #
    #spritePaths should be array of order [up, down, left, right]


class Weapon():
    def __init__(self, weapName):
        self.name = weapName
        if self.name != None:
          self.power = weaponStatsList[self.name][0]
          self.originalSprites = weaponStatsList[self.name][1]
          self.isBurnable = weaponStatsList[self.name][2]
          self.burningSprites = weaponStatsList[self.name][3]
          self.range = weaponStatsList[self.name][4]
          self.coords = Coords(0, 0)
          self.sprites = self.originalSprites
          self.sprite = Sprite(self.sprites[3], self)
          self.onFire = false
          self.value = weaponStatsList[self.name][5]
          self.displayed = false
          self.currentAnimation = None
          self.animationDelay = .15
          self.animationUp = ThreeStageAnimationCycle(self.sprites[0], self.sprites[4], self.sprites[8], 0, 0, self.animationDelay)
          self.animationDown = ThreeStageAnimationCycle(self.sprites[1], self.sprites[5], self.sprites[9], 0, 0, self.animationDelay)
          self.animationLeft = ThreeStageAnimationCycle(self.sprites[2], self.sprites[6], self.sprites[10], 0, 0, self.animationDelay)
          self.animationRight = ThreeStageAnimationCycle(self.sprites[3], self.sprites[7], self.sprites[11], 0, 0, self.animationDelay)
          try:
            self.burningAnimationUp = ThreeStageAnimationCycle(self.burningSprites[0], self.burningSprites[4], self.burningSprites[8], 0, 0, animationDelay)
            self.burningAnimationDown = ThreeStageAnimationCycle(self.burningSprites[1], self.burningSprites[5], self.burningSprites[9], 0, 0, animationDelay)
            self.burningAnimationLeft = ThreeStageAnimationCycle(self.burningSprites[2], self.burningSprites[6], self.burningSprites[10], 0, 0, animationDelay)
            self.burningAnimationRight = ThreeStageAnimationCycle(self.burningSprites[3], self.burningSprites[7], self.burningSprites[11], 0, 0, animationDelay)
          except:
            None




      # sets the weapon on fire. Starts a new thread for a count down to put out fire

    def burn(self):
        x = None
        self.onFire = true
        thread.start_new_thread(self.threadFireCountdown, (x, ))

    def threadFireCountdown(self, x):
        start = counter.turn
        finish = start + 15
        while counter.turn < finish:
            None
        self.onFire = false
        self.sprites = self.originalSprites






        # Displays the weapon's "up/down/left/right" sprite at the coords.
        # For use with being's "self.forwardCoords.x/y"

    def displayUp(self, x, y):
        if self.displayed == false:
          self.displayed = true
          if self.onFire == true:
            self.currentAnimation = self.burningAnimationUp
          else:
            self.currentAnimation = self.animationUp
          self.currentAnimation.coords = Coords(x, y)
          self.currentAnimation.animate()


    def displayDown(self, x, y):
       if self.displayed == false:
          self.displayed = true
          if self.onFire == true:
            self.currentAnimation = self.burningAnimationDown            
          else:
            self.currentAnimation = self.animationDown
          self.currentAnimation.coords = Coords(x, y)
          self.currentAnimation.animate()

    def displayLeft(self, x, y):
       if self.displayed == false:
          self.displayed = true
          if self.onFire == true:
            self.currentAnimation = self.burningAnimationLeft            
          else:
            self.currentAnimation = self.animationLeft
          self.currentAnimation.coords = Coords(x, y)
          self.currentAnimation.animate()
          self.displayed = true


    def displayRight(self, x, y):       
        if self.displayed == false:
          if self.onFire == true:
            self.currentAnimation = self.burningAnimationRight            
          else:
            self.currentAnimation = self.animationRight
          self.currentAnimation.coords = Coords(x, y)
          self.currentAnimation.animate()
          self.displayed = true







        # removes the weapon from the display

    def hide(self):
        display.remove(self.sprite)
        self.displayed = false












    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove, upMove, downMove]
    # All beings are added to the currentBeingList[]
    # Constructor Parameters:
    #    name                 - Being's name as a string
    #    weapName             - Being's starting weapon as a string - must correlate with weaponList
    #    spritePaths          - list containing the filePaths of the Being's sprites
    #    xSpawn               - initial x location
    #    ySpawn               - initial y location
    #    itemList             - default inventory items
    #
    # Members:
    #    name                 - name as a string
    #    level                - combat level
    #    hp                   - current hp
    #    maxHp                - maximum hp
    #    xp                   - current xp for levelling
    #    atk                  - innate attack power
    #    df                   - innate defense
    #    lootValue            - calculated value to determine value of loot dropped
    #    xpValue              - calculated value to determine xp awarded upon defeat
    #    hostile              - bool indicating whether the being is under hostile cpu control
    #    inv                  - inventory items
    #    coords               - Coords object indicating location
    #    forwardCoords        - Coords object indicating forward-1-tile location
    #    unchangedSpritePaths - Original sprites before modification with gore/lighting
    #    spritePaths          - current sprite paths
    #    sprite               - BeingSprite object holding the Being's sprite
    #    weapon               - Weapon object for the currently equipped weapon
    #    wallet               - in value indicating wealth in currency
    #    facing               - current direction the Being is facing
    #    isMoving             - bool indicating movement status
    #    talkingLines         - default talking lines when spoken to
    #    bloodySprites        - altered BeingSprites used when injured
    #    lightSprites         - altered BeingSprites when within range of LightSource that is on
    #    darkSprites          - placeholder for darkened BeingSprites

class Being():
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        self.name = name
        self.level = 0
        self.hp = 10
        self.maxHp = 10
        self.xp = 0
        self.atk = 5
        self.df = 5
        self.lootValue = self.maxHp + self.atk + self.df
        self.xpValue = self.lootValue/2
        self.hostile = false
        self.inv = []
        self.coords = Coords(xSpawn, ySpawn)
        self.forwardCoords = Coords(self.coords.x + BITS, self.coords.y)
        self.unchangedSpritePaths = spritePaths
        self.spritePaths = spritePaths
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.weapon = Weapon(weapName)
        self.wallet = Wallet(self, self.lootValue)
        self.facing = directionList["down"]
        self.isMoving = false
        self.talkingLines = ["Hello!",
                             "Yes?",
                             "Can I Help you?"]
        self.bloodySprites = []
        self.lightSprites = []
        self.darkSprites = []
        if itemList != None:
            self.inv += itemList
        currentBeingList.append(self)



        # use this moveTo when moving beings around

    def moveTo(self, x, y):
        self.sprite.moveTo(x, y)
        self.coords.x = x
        self.coords.y = y


        # activates an activatable object directly in front

    def activateTarget(self):
      target = self.getFrontTarget()
      try:
        target.activate(self)
      except:
        target.activate()

        # Updates wallet by amount

    def changeWallet(self, amount):
        self.wallet.value += amount
        if self.wallet <= 0:
            self.wallet == 0
        self.wallet.updateWalletDisplay()






        # Adds/removes item to/from inventory list

    def inventoryAdd(self, item):
        if len(self.inv) < MAX_INVENTORY:
          self.inv.append(item)
        else:
          inventoryFull()
    def inventoryRemove(self, item):
        self.inv.remove(item)



        # returns the Being's level

    def getLevel(self):
        return self.level






        # level-up logic. Semi-randomly increases max HP, Atk, df

    def levelUp(self):
        self.xp = 0
        self.level += 1
        self.changeMaxHP(random.randint(0, 8))
        self.changeAtk(random.randint(0, 4))
        self.changeDf(random.randint(0, 4))
        self.hp = self.maxHp
        try:
          self.hpBar.updateBar()
        except:
          None





        # returns the Being's name

    def getName(self):
        return self.name






        # returns the Being's current hp

    def getCurrentHP(self):
        return int(self.hp)






        # returns the Being's max hp

    def getMaxHP(self):
        return int(self.maxHp)






        # returns the Being's current xp

    def getXp(self):
        return int(self.xp)






        # returns the Being's ATK

    def getAtk(self):
        return int(self.atk)






        # returns the Being's DF

    def getDf(self):
        return int(self.df)






        # increases xp by the amount given.
        # negative amounts will reduce xp
        # contains built in "barrier" formula
        # for levelling up

    def changeXp(self, amount):
        for i in range(1, amount):
            self.xp +=1
            if self.xp>=(self.level**1.2)*1.5:
                self.levelUp()






        # changes ATK by the amount given

    def changeAtk(self, amount):
        self.atk += amount






        # changes DF by the amount given


    def changeDf(self, amount):
        self.df += amount






        # changes max HP by the amount given

    def changeMaxHP(self, amount):
        self.maxHp += amount






        # changes current HP by amount given.
        # negative values reduce.
        # if hp falls below 0, calls dead()

    def changeHp(self, amount):
        self.hp = int(self.hp + amount)
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        elif self.hp <= 0:
            self.dead()
        else:
            self.bloodify()
        try:
          self.hpBar.updateBar()
        except:
          None






        # Basic enemy AI. Enemy moves in a random direction and attacks if
        # the player is directly in front.

    def simpleHostileAI(self):
        distanceX = self.coords.x - bot1.coords.x
        distanceY = self.coords.y - bot1.coords.y
        closeProximity = BITS * 3
        if self.forwardCoords.x == bot1.coords.x and self.forwardCoords.y == bot1.coords.y:
            self.meleeAtk()
        elif self.coords.x-BITS == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceLeft()
            self.meleeAtk()
        elif self.coords.x+BITS == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceRight()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y+BITS == bot1.coords.y:
            self.faceDown()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y-BITS == bot1.coords.y:
            self.faceUp()
            self.meleeAtk()
        elif abs(self.coords.x - bot1.coords.x) < BITS and abs(self.coords.y - bot1.coords.y) < BITS:
            self.moveRandom()
        elif abs(self.coords.x - bot1.coords.x) <= closeProximity and abs(self.coords.y - bot1.coords.y) <= closeProximity:
            self.moveTowardsPlayer(distanceX, distanceY)
        else:
            self.moveRandom()






        # Moves towards bot1. Distances should be passed in form self.x - bot1.x, same for y

    def moveTowardsPlayer(self, distanceX, distanceY):
        if abs(distanceX) > abs(distanceY):
            if distanceX < 0:
                self.moveRight()
            else:
                self.moveLeft()
        else:
            if distanceY < 0:
                self.moveDown()
            else:
                self.moveUp()


        # Moves a being in a random direction

    def moveRandom(self):
        randNum = random.randint(0, 3)
        if randNum == 0:
            self.moveUp()
        elif randNum == 1:
            self.moveDown()
        elif randNum == 2:
            self.moveLeft()
        else:
            self.moveRight()







        # returns a random item from the inv list

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]







        # drops all contents of the inv list in a lootbag object

    def dropLoot(self):
        newWallet = Wallet(None, self.wallet.value)
        self.inv.append(newWallet)
        loot = Lootbag(self.inv, self.coords)
        objectList.append(loot)






        # Actions to be taken on hp <= 0

    def dead(self):
        self.inv.append(self.weapon)
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        del self
        global dead_sound
        thread.start_new_thread(music.Play, (dead_sound,))

        # Handles lighting of sprites. If a valid light object is within the range
        # currently set to BITS * 3, a new set of sprites will be created and applied
        # to simulate lighting.
        # Starts a new thread.

    def lightenDarken(self):
        bright = self.lightWithinRange(BITS * 3)
        if self.spritePaths != self.lightSprites and bright:
            self.lightenPixels()
        elif self.spritePaths == self.lightSprites and not bright:
            self.resumePixels()
            deletePath = path + "RobotSprites"
            deleteKey = self.name + str(currentBeingList.index(self)) + "lightSprite"
            x = None
            thread.start_new_thread(self.threadDeleteLightSprites, (x,))




        # Helper for lightenDarken(). Separated to allow for early returns. Determins if
        # a valid light source is within the range passed

    def lightWithinRange(self, range):
        for light in lightSources:
            distanceX = abs(self.coords.x - light.coords.x)
            distanceY = abs(self.coords.y - light.coords.y)
            if distanceX <= range and distanceY <= range and light.isOn:
                return true
        return false

        # Deletes lightened sprites when no longer in use
    def threadDeleteLightSprites(self, x):
        for sprite in self.lightSprites:
            os.remove(sprite)
        self.lightSprites = []

        # Returns being's BeingSprites to normal-nonlightened sprites
    def resumePixels(self):
        self.spritePaths = self.darkSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[self.facing], self)
        self.sprite.spawnSprite()

        # Lightens the BeingSprites
    def lightenPixels(self):
        self.darkSprites = self.spritePaths
        spriteNum = 0
        for sprites in range(0, len(self.spritePaths)):
            pic = makePicture(self.spritePaths[sprites])
            for x in range(0, getWidth(pic)-1):
                for y in range(0, getHeight(pic)-1):
                    p = getPixel(pic, x, y)
                    color = getColor(p)
                    if color != makeColor(0, 0, 0):
                        setColor(p, makeColor(getRed(p)*1.5, getGreen(p)*1.5, getBlue(p)*1.5))
            newPicPath = path + "RobotSprites/" + self.name + str(currentBeingList.index(self)) + "lightSprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.lightSprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.lightSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.lightSprites[self.facing], self)
        self.sprite.spawnSprite()

        # Adds an oil effect to the BeingSprites at varied intensity depending
        # on being.hp (higher effect at lower hp)
    def bloodify(self):
        spriteNum = 0

        self.bloodySprites = []
        for sprites in range(0, len(self.spritePaths)):
            pic = makePicture(self.spritePaths[sprites])
            for x in range(0, getWidth(pic)-1):
                for y in range(0, getHeight(pic)-1):
                    p = getPixel(pic, x, y)
                    if getColor(p) != makeColor(0, 0, 0):
                        if random.randint(0, 100) > (self.hp*100)/self.maxHp:
                          setRed(p, (getRed(p)+228)/3)
                          setGreen(p, (getGreen(p)+174)/3)
                          setBlue(p, (getBlue(p)+14)/3)
            newPicPath = path + "RobotSprites/" + self.name + str(currentBeingList.index(self)) + "bloodySprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.bloodySprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.bloodySprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.bloodySprites[self.facing], self)
        self.sprite.spawnSprite()





        # For use with actions that can target more than one target (e.g., attacks)

    def getFrontTargetList(self):
        bigList = currentBeingList + objectList
        targetList = []
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                targetList.append(target)
        return targetList







        #for use with actions that can only target one target (e.g., talking)

    def getFrontTarget(self):
        bigList = currentBeingList + objectList
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                return target





        #needs to be reworked for better decomp
        #
        # activates the melee attack action.
        # displays the weapon animation at the being's forward coord
        # and activates a damage calculation if any being is there
        # Friendly fire is enabled. Attacking a friendly turns them hostile
        # if the target is killed, exp is calculated.  If the player is killed,
        # the player loses all levels/items and respawns as a new instance of the
        # User class.
        #
        # Damage logic is delayed with a thread to occur around the time the third weapon
        # display animation activates

    def meleeAtk(self):
        global hit_sound
        thread.start_new_thread(music.Play, (hit_sound,))
        self.displayWeapon()
        x = None
        thread.start_new_thread(self.threadHideWeapon, (None,))
        for target in self.getFrontTargetList():
            if isinstance(target, LightSource):
              if target.isBurnable and target.isOn and self.weapon.isBurnable:
                self.weapon.burn()
              elif target.isBurnable and not target.isOn and self.weapon.onFire:
                target.turnOn()
            elif isinstance(target, Being) or isinstance(target, Enemy):
              damage = self.atk
              if damage <= 0:
                damage = 1
              thread.start_new_thread(threadDamageCalculation, (self, target, damage, self.weapon.animationDelay*2))
              





        # Display's the "damage splash" sprite at
        # the given location. Uses multithreading.

    def displayDamage(self):
        damage = Sprite(path + r"EffectSprites/damage.gif", self)
        display.add(damage, self.coords.x, self.coords.y)
        thread.start_new_thread(threadRemoveSprite, (.25, damage))






        # For use with meleeAtk and thread.start_new_thread().
        # may be removed and have functionality replaced by
        # more general function

    def threadHideWeapon(self, x):
        time.sleep(self.weapon.currentAnimation.secondsBetween*4)
        self.weapon.currentAnimation.stopAnimating()
        self.weapon.displayed = false





        # displays the being's weapon at the being's forward coords
        # note that the weapon sprite is not despawned

    def displayWeapon(self):
        if self.facing == directionList["up"]:
            self.weapon.displayUp(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == directionList["down"]:
            self.weapon.displayDown(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == directionList["left"]:
            self.weapon.displayLeft(self.forwardCoords.x, self.forwardCoords.y)
        else:  #right
            self.weapon.displayRight(self.forwardCoords.x, self.forwardCoords.y)


        # picks up any LootBag objects at the coords given

    def pickUpLoot(self, coords):
        for item in objectList:
            if item.type == "lootbag" and item.coords.x == coords.x and item.coords.y == coords.y:
                if len(self.inv) + len(item.contents) < MAX_INVENTORY:
                  self.inv += item.contents
                  item.removeSprite()
                  objectList.remove(item)
                  del item
                  for item in self.inv:
                    if isinstance(item, Wallet):
                      self.changeWallet(item.value)
                      self.inv.remove(item)
                else:
                  inventoryFull()



                    # MOVEMENT CLUSTER
        # Moves the being up/down/left/right one unit in two steps.
        # the first step is instant/halfstep, the second
        # is through a delayed call to thread moveDirection
        # in order to give the illusion of animation.
        # faceDirection is called first
        # threadMoveDirection is not meant to be called directly.
        # pickUpLoot() is called in the threadMovefunctions
        #
        # may be streamlined by using a single moveForward function
        # that interacts with direction facing




    def moveUp(self):
        global move
        self.faceUp()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y >= 0 and CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.y -= BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[7], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveUp, (x,))
            if self.facing == directionList["up"]:
              self.forwardCoords.y = self.coords.y - BITS - BITS/2
              self.forwardCoords.x = self.coords.x
              thread.start_new_thread(music.Play, (move,))

        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (move,))


    def threadMoveUp(self, x):
        time.sleep(.15)
        self.coords.y -= BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[0], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.y%32 != 0:
          self.coords.y = (self.coords.y/32)*32


    def moveDown(self):
        global move2
        self.faceDown()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y < backHeight and CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.y += BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[6], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveDown, (x,))
            self.sprite.moveTo(self.coords.x, self.coords.y)
            if self.facing == directionList["down"]:
              self.forwardCoords.y = self.coords.y + BITS + BITS/2
              self.forwardCoords.x = self.coords.x
              thread.start_new_thread(music.Play, (move2,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (move2,))


    def threadMoveDown(self, x):
        time.sleep(.15)
        self.coords.y += BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.y%32 != 0:
          self.coords.y = (self.coords.y/32)*32


    def moveLeft(self):
        global move3
        self.faceLeft()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x >= 0 and CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.x -= BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[4], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveLeft, (x,))
            if self.facing == directionList["left"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x - BITS - BITS/2
              thread.start_new_thread(music.Play, (move3,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (move3,))

    def threadMoveLeft(self, x):
        time.sleep(.15)
        self.coords.x -= BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[2], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.x%32 != 0:
          self.coords.x = (self.coords.x/32)*32

    def moveRight(self):
        global move
        self.faceRight()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x < backWidth and CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.x += BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[5], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveRight, (x,))
            if self.facing == directionList["right"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x + BITS+ BITS/2
              thread.start_new_thread(music.Play, (move4,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (move4,))


    def threadMoveRight(self, x):
        time.sleep(.1)
        self.coords.x += BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[3], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.x%32 != 0:
          self.coords.x = (self.coords.x/32)*32


        # changes the being's sprite to one facing the corresponding
        # direction. If a weapon is displayed, it is first hidden.
        # adjusts forwardCoords accordingly

    def faceUp(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["up"]:
          self.facing = directionList["up"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[0], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y - BITS
          self.forwardCoords.x = self.coords.x

    def faceDown(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["down"]:
          self.facing = directionList["down"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[1], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y + BITS
          self.forwardCoords.x = self.coords.x

    def faceLeft(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["left"]:
          self.facing = directionList["left"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[2], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x - BITS
          self.forwardCoords.y = self.coords.y

    def faceRight(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["right"]:
          self.facing = directionList["right"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[3], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x + BITS
          self.forwardCoords.y = self.coords.y












        # Custom being instance for friendlies. Slightly different giblets/giblet logic
class Friendly(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [RawSprite(path + r"RobotSprites/friendlyBigGib1.gif", self.coords.x, self.coords.y),
                              RawSprite(path + r"RobotSprites/friendlyBigGib2.gif", self.coords.x, self.coords.y),
                              RawSprite(path + r"RobotSprites/friendlyHead.gif", self.coords.x, self.coords.y),
                              ]


    def gibSpawn(self, gibSprite, x, y):
        gibList.append(gibSprite.sprite)
        display.add(gibSprite.sprite, x, y)

    def giblets(self):
        x = random.randint(self.coords.x - BITS, self.coords.x + BITS)
        y = random.randint(self.coords.y - BITS, self.coords.y + BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(path + r"RobotSprites/friendlyBigGib1.gif", path + r"RobotSprites/friendlyBigGib2.gif", x, y)
          animatedGib.animate()
        possibilities = random.randint(0, 3)
        if possibilities == 3:
          for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - BITS, self.coords.x + BITS)
            y = random.randint(self.coords.y - BITS, self.coords.y + BITS)
            if isTraversable(x, y):
              self.gibSpawn(self.gibSpriteList[2], x, y)

        # Actions to be taken on hp <= 0

    def dead(self):
        global dead_sound2
        self.giblets()
        self.inventoryAdd(self.weapon)
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
          try:
            os.remove(files)
          except:
            None
        currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (dead_sound2,))














        # Custom being instance for friendlies. Slightly different giblets/giblet logic
class ShopKeeper(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [Sprite(path + r"RobotSprites/shopKeeperGib1.gif", self),
                              Sprite(path + r"RobotSprites/shopKeeperGib2.gif", self)
                              ]






        # Displays gore effects

    def giblets(self):
        x = random.randint(self.coords.x - BITS, self.coords.x + BITS)
        y = random.randint(self.coords.y - BITS, self.coords.y + BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(path + r"RobotSprites/shopKeeperGib1.gif", path + r"RobotSprites/shopKeeperGib2.gif", x, y)
          animatedGib.animate()



    def dead(self):
        #play animation
        #delete coordinate data from grid
        global dead_sound4
        self.giblets()
        self.inventoryAdd(self.weapon)
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (dead_sound4,))








    # Custom being for enemies. Slightly different logic

class Enemy(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, level):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        for num in range(0, level):
            self.levelUp()
        self.gibSpriteList = [Sprite(path + r"RobotSprites/enemyArmGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyLegGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyLegGib2.gif", self),
                              Sprite(path + r"RobotSprites/enemyBodyGib.gif", self),
                              Sprite(path + r"RobotSprites/enemyHeadGib.gif", self),
                              ]
        self.hostile = true







        # Drops a Lootbag instance with a random inv item

    def dropLoot(self):
        items = []
        items.append(self.randomInvItem())
        items.append(self.wallet)
        loot = Lootbag(items, self.coords)
        objectList.append(loot)



        # adds a sprite to the gibList and display at the pixel coords given

    def gibSpawn(self, gibSprite, x, y):
        gibList.append(gibSprite)
        display.add(gibSprite, x, y)

        # Gore effect for enemies

    def giblets(self):
        gibIndex = 0
        for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - BITS, self.coords.x + BITS)
            y = random.randint(self.coords.y - BITS, self.coords.y + BITS)
            if isTraversable(x, y):
                self.gibSpawn(self.gibSpriteList[gibIndex], x, y)
                print(gibIndex)
                gibIndex += 1



        # Calls functions related to hp==0 logic

    def dead(self):
        #play animation
        #delete coordinate data from grid
        self.giblets()
        self.inventoryAdd(self.weapon)
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
          os.remove(files)
        currentBeingList.remove(self)
        del self
        music.Play(dead_sound3)
        thread.start_new_thread(music.Play, (dead_sound3,))





        # returns a random item from the inv list

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]







class Threat2Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Rock", greenEnemySpritePaths, xSpawn, ySpawn, 10)

class Threat3Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Rock", yellowEnemySpritePaths, xSpawn, ySpawn, 20)

class Threat4Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Sword", purpleEnemySpritePaths, xSpawn, ySpawn, 30)

class Threat5Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Botsmasher", redEnemySpritePaths, xSpawn, ySpawn, 50)





        # Class for armor/equipment, in development

class Armor():
    def __init__(self, name):
        self.armorType = "FIX THIS CLASS"






# used for sprite animation, flickering between two sprites at random
# used for twitching/sparking/flames


class AnimatedGiblets():
    def __init__(self, filename1, filename2, x, y):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, self),
                           Sprite(filename2, self)]
        self.sprite = self.spriteList[0]
        gibList.append(self.spriteList[0])




        #activates animation

    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






        # sprite addition and removal to and from display

    def spawnSprite(self):
        display.place(self.sprite, self.coords.x, self.coords.y, 5)
    def removeSprite(self):
        display.remove(self.sprite)



    def threadAnimate(self, container):
        while self.spriteList[0] in gibList:
            time.sleep(random.randint(0, 2)/10.0)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self.spriteList[0] not in gibList:
            self.removeSprite()
            del self






class Potion():
    def __init__(self):
      self.parental = None
      self.name = "Potion"
      self.restoreValue = 10
      self.value = 20

    def use(self):
      self.parental.changeHp(self.restoreValue)



        # Singleton class for player's HP Bar

class HpBar():
    def __init__(self, parental):
      self.sprites = [Sprite(path + "/EffectSprites/hpBarSpriteEmpty.gif", self, 1), Sprite(path + "/EffectSprites/hpBarSpriteCritical.gif", self, 1),
                      Sprite(path + "/EffectSprites/hpBarSpriteLow.gif", self, 1), Sprite(path + "/EffectSprites/hpBarSpriteHalf.gif", self, 1),
                      Sprite(path + "/EffectSprites/hpBarSpriteHigh.gif", self, 1), Sprite(path + "/EffectSprites/hpBarSpriteMost.gif", self, 1),
                      Sprite(path + "/EffectSprites/hpBarSpriteFull.gif", self, 1)]
      self.sprite = self.sprites[6]
      self.parental = parental
      self.coords = Coords(0, 0)
      self.sprite.spawnSprite()

    def updateBar(self):
      hpPercentage = ((self.parental.hp*1.0)/self.parental.maxHp)*100
      self.sprite.removeSprite()
      if hpPercentage >= 100:
        self.sprite = self.sprites[6]
      elif hpPercentage >= 90:
        self.sprite = self.sprites[5]
      elif hpPercentage >= 75:
        self.sprite = self.sprites[4]
      elif hpPercentage >= 50.0:
        self.sprite = self.sprites[3]
      elif hpPercentage >= 25:
        self.sprite = self.sprites[2]
      elif hpPercentage >= 10:
        self.sprite = self.sprites[1]
      else:
        self.sprite = self.sprites[0]
      self.sprite.spawnSprite()










        # Custom 2 stage animated sprite. On animate, flickers
        # semi-randomly.
        # Constructor Parameters:
        #    filename1            - filepath for first sprite image
        #    filename2            - filepath for second sprite image
        #    x                    - x coords in pixels
        #    y                    - y coords in pixels
        #    layer                - on-screen layer
        #
        # Members:
        #    coords               - Coords object indicating location
        #    spriteList           - list of current sprites
        #    sprite               - current Sprite object
        #    spriteLayer          - on-screen layer
        #    isAnimating          - animation status


class StationaryAnimatedSprite():
    def __init__(self, filename1, filename2, x, y, layer = 3):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, self, layer),
                           Sprite(filename2, self, layer)]
        self.sprite = self.spriteList[0]
        self.coords = Coords(x, y)
        self.sprite.layer = layer
        self.isAnimating = false




    def animate(self):
        animatedSpriteList.append(self)
        self.isAnimating = true
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))
    def stopAnimating(self):
        animatedSpriteList.remove(self)

    def spawnSprite(self):
        self.sprite.spawnSprite()
    def removeSprite(self):
        display.remove(self.sprite)


    def threadAnimate(self, container):
        while self in animatedSpriteList:
            time.sleep(random.randint(0, 2)/10.0)
            placeHolderSprite = self.spriteList[0]
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in animatedSpriteList:
            self.removeSprite()
            del self






        # Custom 3-stage animated sprite that animates 3 frames in cycles (1, 2, 3, 1, 2, 3...)
        # Constructor Parameters:
        #    filename1            - filepath for first sprite image
        #    filename2            - filepath for second sprite image
        #    filename3            - filepath for third sprite image
        #    x                    - x coord in pixels
        #    y                    - y coord in pixels
        #    secondsBetween       - seconds each frame is displayed for (floats supported)
        #    layer                - on-screen layer
        #
        # Members:
        #    coords               - Coords object indicating location
        #    spriteList           - list of Sprite objects to be cycled
        #    sprite               - current Sprite
        #    sprite.layer         - on-screen layer
        #    isAnimating          - boolean animation status
        #    secondsBetween       - seconds each frame is displayed for (floats supported)

class ThreeStageAnimationCycle():
    def __init__(self, filename1, filename2, filename3, x, y, secondsBetween, layer = 3):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, self, layer),
                           Sprite(filename2, self, layer),
                           Sprite(filename3, self, layer)]
        self.sprite = self.spriteList[0]
        self.sprite.layer = layer
        self.isAnimating = false
        self.secondsBetween = secondsBetween



        # Initiates animation and adds to current animatedSpriteList

    def animate(self):
        global animatedSpriteList
        animatedSpriteList.append(self)
        self.isAnimating = true
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))
    def stopAnimating(self):
        global animatedSpriteList
        animatedSpriteList.remove(self)

        # shortcut to object's sprite functions
    def spawnSprite(self):
        self.sprite.spawnSprite()
    def removeSprite(self):
        display.remove(self.sprite)

        # core animation
    def threadAnimate(self, x):
        global animatedSpriteList
        self.sprite = self.spriteList[2]
        time.sleep(self.secondsBetween)
        while self in animatedSpriteList:
            placeHolderSprite = self.spriteList[0]
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.removeSprite()
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            elif self.sprite == self.spriteList[1]:
                self.removeSprite()
                self.sprite = self.spriteList[2]
                self.spawnSprite()
            else:
              try:
                self.removeSprite()
              except:
                None
              self.sprite = self.spriteList[0]
              self.spawnSprite()
            time.sleep(self.secondsBetween)
        if self not in animatedSpriteList:
            self.removeSprite()
            self.sprite = self.spriteList[2]
            del self

    def animateOnce(self):
        global animatedSpriteList
        animatedSpriteList.append(self)
        self.isAnimating = true
        x = None
        thread.start_new_thread(self.threadAnimateOnce, (x,))

    def threadAnimateOnce(self, x):
        global animatedSpriteList
        try:
          self.removeSprite()
        except:
          None
        for i in range (0, 3):
          self.sprite = self.spriteList[i]
          self.spawnSprite()
          time.sleep(self.secondsBetween)
          self.removeSprite()
        self.isAnimating = false
        animatedSpriteList.remove(self)




    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the currentBeingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   level:          - Being's starting level

class User(Being):
    def __init__(self, name, weapName, spritePaths, CURRENT_AREA):
        Being.__init__(self, name, weapName, spritePaths, CURRENT_AREA.spawnCoords.x, CURRENT_AREA.spawnCoords.y)
        self.name = name
        self.helm = "Hair"
        self.chest = "BDaySuit"
        self.legs = "Shame"
        self.boots = "Toes"
        self.gloves = "Digits"
        self.area = CURRENT_AREA
        self.hpBar = HpBar(self)
        self.wallet = UserWallet(self, 0)
        self.sprite.spawnSprite()


    def changeWallet(self, amount):
      Being.changeWallet(self, amount)
      self.wallet.updateWalletDisplay()


    def suckUpGiblets(self):
      global CURRENT_AREA
      for gib in CURRENT_AREA.gibList:
        distanceX = abs(self.coords.x - gib.parental.coords.x)
        distanceY = abs(self.coords.y - gib.parental.coords.y)
        if distanceX <= BITS and distanceY <= BITS:
          gib.removeSprite()
          CURRENT_AREA.gibList.remove(gib)
          if gib.fileName == path + r"RobotSprites/friendlyHead.gif" or gib.fileName == path + r"RobotSprites/enemyHeadGib.gif":
            self.changeWallet(5)
          else:
            self.changeWallet(1)


    def giblets():
        None


               # EQUIPMENT CLUSTER###
        # The following 6 functions handle equipping items
        # to  specific parts of the body.  Atk and Df stats
        # are adjusted accordingly.  The equipped item must
        # correlate to one of the itemLists

    def setWeapon(self, weapon):
        self.inventoryAdd(self.weapon)
        self.atk -= weaponStatsList[self.weapon.name][0]
        if weapon in self.inv:
          self.inventoryRemove(weapon)
        self.weapon = weapon
        self.atk += weaponStatsList[self.weapon.name][0]


    def setHelm(self, helm):
        if self.helm != "Hair":
            self.inventoryAdd(self.helm)
        self.df -= helmStatsList(self.helm)
        self.helm = helm
        self.df += helmStatsList(self.helm)


    def setChest(self, chest):
        if self.chest != "BDaySuit":
            self.inventoryAdd(self.chest)
        self.df -= chestStatsList(self.chest)
        self.chest = chest
        self.df += chestStatsList(self.chest)


    def setLegs(self, legs):
        if self.legs != "Shame":
            self.inventoryAdd(self.legs)
        self.df -= legsStatsList(self.legs)
        self.legs = legs
        self.df += legsStatsList(self.legs)


    def setBoots(self, boots):
        if self.boots != "Toes":
            self.inventoryAdd(self.boots)
        self.df -= bootsStatsList(self.boots)
        self.boots = boots
        self.df += bootsStatsList(self.boots)


    def setGloves(self, gloves):
        if self.gloves != "Digits":
            self.inventoryAdd(self.gloves)
        self.df -= glovesStatsList(self.gloves)
        self.gloves = gloves
        self.df += glovesStatsList(self.gloves)






        # equips a given item by calling one of the
        # equipment "set" functions
        # item should be passed as it's key as it appears
        # in the item lists

    def equip(self, item):
        if indexName == weaponStatsList:
            if item in weaponStatsList:
                self.setWeapon(item)
        elif indexName == helmStatsList:
            if item in helmStatsList:
                self.setHelm(item)
        elif indexName == legsStatsList:
            if item in legsStatsList:
                self.setLegs(item)
        elif indexName == chestStatsList:
            if item in chestStatsList:
                self.setChest(item)
        elif indexName == glovesStatsList:
            if item in glovesStatsList:
                self.setGloves(item)
        elif indexName == bootsStatsList:
            if item in bootsStatsList:
                self.setBoots(item)






            # action - attempts to steal an item from a target
            # Being.  If the attempt fails, the Being turns hostile

    def steal(self, target):
      if len(self.inv) < MAX_INVENTORY:
        possibilities = len(target.inv)
        if possibilities>0:
            if random.randint(0, 10)%10 == 0:
                item = target.randomInvItem()
                target.inv.remove(item)
                self.inv.append(item)
                label = gui.Label("You stole "  + item.name)
                showLabel(label)
            else:
                label = gui.Label("You messed up now!")
                showLabel(label)
                target.hostile = true
        else:
            inventoryFull()

    def talk(self):
        global talk_sound
        thread.start_new_thread(music.Play, (talk_sound,))
        target = self.getFrontTarget()
        if target.coords.x < self.coords.x:
          target.faceRight()
        elif target.coords.x > self.coords.x:
          target.faceLeft()
        elif target.coords.y < self.coords.y:
          target.faceDown()
        elif target.coords.y > self.coords.y:
          target.faceUp()
        speech = gui.Label(target.talkingLines[random.randint(0, len(target.talkingLines)-1)])
        showLabel(speech)
        delayRemoveObject(speech, 2)



    def dead(self):
        self.sprite.removeSprite()
        self.dropLoot()
        global currentBeingList
        currentBeingList.remove(self)
        for files in self.bloodySprites:
          try:
            os.remove(files)
          except:
            None
        try:
          self.weapon.currentAnimation.stopAnimating()
        except:
          None
        self.wallet.value = 0
        self.wallet.sprite.removeSprite()
        removeLabel(self.wallet.label)
        self.__init__("bot1", "Stick", userSpritePaths, self.area)
        global dead_sound5
        thread.start_new_thread(music.Play, (dead_sound5,))




class music:

    def __init__(self, music_file):
      self.sound = makeSound(music_file)

    def Play(self):
      play(self.sound)


    def Stop(self):
      self.isPlaying = false
      stopPlaying(self.sound)


    def volume(self, n):
      for sample in getSamples(self.sound):
        value = getSampleValue(sample)
        setSampleValue(sample, value*n)


    def repeat(self):
      while true:
        play(self.sound)
        stopPlaying(self.sound)
        time.sleep(20)
      return

    def loop2(self):
      self.isPlaying = true
      while self.isPlaying:
        play(self.sound)
        stopPlaying(self.sound)
        time.sleep(20)
      return



            ######################
            #                    #
            #    PSEUDO-MAIN     #
            #                    #
            ######################





backWidth = BITS * WIDTH_TILES
backHeight = BITS * HEIGHT_TILES
display = CustomDisplay("Robot Saga", backWidth, backHeight)
layer0 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 0)
layer1 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 1)
layer2 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 2)
layer3 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 3)
layer4 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 4)
layer5 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 5)
layer6 = RawSprite(path + "EffectSprites/blankSprite.gif", 0, 0, 6)
setUpLayers()
loading = RawSprite(path + "Fullscreens/LogoOmega.png", 0, 0, 0)
startScreen = RawSprite(path + "Fullscreens/startScreen.png", 0, 0, 2)
title = RawSprite(path + "EffectSprites/Title.gif", 286, -64, 1)
loading.spawnSprite()
title.spawnSprite()
#initailize background image

tilesPath = path + "Tiles/LPC/tiles/"
#Old, probably dont need textureMap anymore
#textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")

#initailize textures
#  Tile(isTraversable, isPassable, isTough, desc)
#add Dirt
dirt = Tile(true, true, false, "dirt")
#add DirtWall
dirtWall = Tile(false, true, false, "dirtWall")
#add Grass
grass = Tile(true, true, false, "grass")
#add stone
stone = Tile(true, true, false, "stone")
#add stoneWall
stoneWall = Tile(false, true, false, "stoneWall")
#add hole
hole = Tile(true, true, false, "hole")
#add lavaRock
lavaRock = Tile(true, true, false, "lavaRock")
#add Water
water = Tile(false, true, false, "water")
#add Lava
lava = Tile(false, true, false, "lava")
#add Fence
fence = Tile(false, true, false, "fence")
#add Chest
chest = Tile(false, true, false, "chest")
#add Door tile
door = Tile(true, false, false, "door")
#add Blank
blank = Tile(false, false, false, "Filler for structure class")

#structures
structPath = path + "Tiles/LPC/structures/"
house = makePicture(structPath + "house.png")
tree1 = makePicture(structPath + "tree1.png")

#get width and height
#texWidth = getWidth(textureMap)
#texHeight = getHeight(textureMap)


paths = ["d", "s", "h", ".", "o"]
#create empty grass field will clean up later
home  = "fffffffffffffddddfffffffffffffff"
home += "fh......ggt,,ddddgh......ggggggf"
home += "f.......gg,,,ddddg.......dgggggf"
home += "f.......gg,,,ddddg.......ddggggf"
home += "f..o....gggggddddg..o....ddggggf"
home += "f..o....gggggddddg..o....ddggggf"
home += "fgsssssssddddddddddddddddddggggf"
home += "fgsssssssddddddddddddddddddggddd"
home += "fgggsssssggggddddddddddddddddddd"
home += "fgggddssgggggddddddddddddddddddf"
home += "fgggdddggggwwwwddddddh......gggf"
home += "fgggdddgggwwwwwwddddd.......gggf"
home += "fgggdddwwwwwwwwwwwwdd.......gggf"
home += "fgggdddwwwwwwwwwwwwdd..o....t,,f"
home += "fgdddddwwwwwwwwwwwddd..o....,,,f"
home += "fgdddddddwwwwwwwdddddddddddd,,,f"
home += "fggddddddgggggggddddddddddddgdgf"
home += "ffffffffffffffffffffffffffffffff"
townMap = Map(home)
townAnimations = [StationaryAnimatedSprite(path + "/EffectSprites/blankWater.gif", path + "/EffectSprites/waterMoving.gif", 256, 352),
                  ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 320, 0, .3),
                  ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 896, 384, .3)]
currentMap = townMap

nfield  = "ffffffffffffffffffffffffffffffff"
nfield += "fggggggggggggggggggggggggggggggf"
nfield += "fggggggggggggggggggggggggggggggf"
nfield += "fggggggggggwwwwwwwwwgggggggggggf"
nfield += "fgggggggwwwwwwwwwwwwwggggggggggf"
nfield += "fggggggwwwwwwwwwwwwwwggggggggggf"
nfield += "fggggggwwwwwwwwwwwwwdddddddddddg"
nfield += "fgggggwwwwwwwwgt,,gddddddddddddd"
nfield += "fgggggwwwwwwggg,,,ddddwwwwwddddd"
nfield += "fgggggwwwwwwggg,,,dddwwwwwwwddgg"
nfield += "fgggggwwwwwwddddddddgwwwwwwwddgf"
nfield += "fgggggwwwwwdddddddddwwwwwwwwddgf"
nfield += "fggggggwwdddddwwwwwwwwwwwwwwddgf"
nfield += "fggggggggdddwwwwwwwwwwwwwwddddgf"
nfield += "fggggggggddgwwwwwwwwwwwwwdddddgf"
nfield += "fggggggggdddddddddddddddddddgggf"
nfield += "fggggggggddddddddddddddddddggggf"
nfield += "fffffffffffffddddfffffffffffffff"
nfieldMap = Map(nfield)
nFieldAnimations = [ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 480, 192, .3)]

efield  = "fffffffffffffddddfffffffffffffff"
efield += "fggggggggggggddddggggggggggggggf"
efield += "fggggggggggggdddgggggwwwwwwwgggf"
efield += "fggggggggggggdddgggggwwwwwwwwwgf"
efield += "fggggggggggdddddggggwwwwwwwwwwgf"
efield += "fgddddddddddddddggggwwwwwwwwwwgf"
efield += "ddddddddddddddggggggwwwwwwwwwwgf"
efield += "dddddddddddddggggggggggwwwwwwwgf"
efield += "dddddwwwwgggggggggggggggwwwwwggf"
efield += "ddddwwwwwggggggggggggggggggggggf"
efield += "fggwwwwwwwggggggggggggggggt,,ggf"
efield += "fggwwwwwwwwwwwwggggggggggg,,,ggf"
efield += "fggwwwwwwwwwwwwggggggggggg,,,ggf"
efield += "fgwwwwwwwwwwwwwgggggggggt,,t,,gf"
efield += "fgwwwwwwwwwwwggggggggggg,,,,,,gf"
efield += "fggwwwwwwwgggggggggggggg,,,,,,gf"
efield += "fggggggggggggggggggggggggggggggf"
efield += "ffffffffffffffffffffffffffffffff"
efieldMap = Map(efield)
eFieldAnimations = [ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 768, 384, .2),
                    ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 864, 384, .2),
                    ThreeStageAnimationCycle(path + "/EffectSprites/sakuraMoving1.gif", path + "/EffectSprites/sakuraMoving2.gif", path + "/EffectSprites/sakuraMoving3.gif", 832, 288, .2)]

nefield  = "ffffffffffffffffffffffffffffffff"
nefield += "fggggggggggggggggggggggggggggggf"
nefield += "fggggggggggggggggggggwwwwwwwgggf"
nefield += "fggggggggggggggggggggwwwwwwwwwgf"
nefield += "fggggggggggggggggggggwwwwwwwwwgf"
nefield += "fggggggggggggggggdddHHHHHHwwwwgf"
nefield += "ddddddddddddddddddddHHHHHHwwwwgf"
nefield += "ddddddddddddddddddddddHHHHwwwwgf"
nefield += "ddddddddddddddddddddddHHHHwwwggf"
nefield += "ddddddggggggggdddddgHHHHHHgggggf"
nefield += "fggdddddggggggddddggHHHHHHgggggf"
nefield += "fgggdddddddgggdddggggggggggggggf"
nefield += "fgggggdddddddddddggggggggggggggf"
nefield += "fgggggggdddddddddggggggggggggggf"
nefield += "fgggggggdddddddddggggggggggggggf"
nefield += "fggggggggggggddddggggggggggggggf"
nefield += "fggggggggggggddddggggggggggggggf"
nefield += "fffffffffffffddddfffffffffffffff"
nefieldMap = Map(nefield)

#old field no longer in use
field  = "ffffffffffffffffffffffffffffffff"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggwwwwwwwgggf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fgggggggggggggggggggggggggwwwwgf"
field += "fggggggggggggggggggggggggwwwwwgf"
field += "ggggggggggggggggggggggggwwwwwwgf"
field += "ggggggggggggggggggggggggwwwwwggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fffffffffffffggggfffffffffffffff"
fieldMap = Map(field)

entrance  = "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SlllllllllllllLLLllllllllllllllS"
entrance += "SllllllllLLLLlLLLllllLLLlllllllS"
entrance += "SllllllllLLLLLLLLLllLLLLlllllllS"
entrance += "SllllllllLLLLLLLLLLLLLLLlllllllS"
entrance += "SllllllllLLLLLLLLLLLLLlllllllllS"
entrance += "lllllllLLLLLLLooooLLLLllllllllll"
entrance += "lllllllLLLLLLLllllLLLLllllllllll"
entrance += "SllllllLLLLLllllllLLLLlllllllllS"
entrance += "SlllllllLLLLllllllLLLllllllllllS"
entrance += "SlllllllllLLlllllllLLllllllllllS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SllllllllllllllllllllllllllllllS"
entrance += "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
entranceMap = Map(entrance)

westRoom  = "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "Slllllllllllllllllllllllllllllll"
westRoom += "Slllllllllllllllllllllllllllllll"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SllllllllllllllllllllllllllllllS"
westRoom += "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
westRoomMap = Map(westRoom)

eastRoom  = "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
eastRoom += "SllllllllllllllllllllllllllllllS"
eastRoom += "SllllllllllllllllllllllllllllllS"
eastRoom += "SlllLLLLLLLlllllllllllLLLLLLlllS"
eastRoom += "SllLLLLLLLLLlllllllllLLLLLLLLllS"
eastRoom += "SllLLLLLLLLLlllllllllLLLLLLLLllS"
eastRoom += "SlllLLLLLLLlllllllllllLLLLLLlllS"
eastRoom += "SllllllllllllllllllllllllllllllS"
eastRoom += "lllllllllllllllllllllllllllllllS"
eastRoom += "lllllllllllLLLLllllllllllllLLllS"
eastRoom += "SlllLLllllLLLLLlllllllllLLLLLllS"
eastRoom += "SlllLLLlllLLLLLllllllLLLLLLLLllS"
eastRoom += "SlllLLLLLLLLLLLllllllLLLLLLLLllS"
eastRoom += "SlllLLLLLLLLLLLlllllLLLLLLLLlllS"
eastRoom += "SlllLLLLLLLlllllllllLLLLLLLllllS"
eastRoom += "SllllllllllllllllllllllllllllllS"
eastRoom += "SllllllllllllllllllllllllllllllS"
eastRoom += "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
eastRoomMap = Map(eastRoom)

keyRoom  = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
keyRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLllllllllLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLlllc.lllLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLllllllllLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLllllllllLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLllllllllLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
keyRoom += "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
keyRoomMap = Map(keyRoom)

miniBoss  = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
miniBoss += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
miniBoss += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
miniBoss += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
miniBoss += "SLLLLLLLllllllllllllllllLLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLllllllllllllllllllLLLLLLS"
miniBoss += "SLLLLLLLllllllllllllllllLLLLLLLS"
miniBoss += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
miniBoss += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
miniBoss += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
miniBoss += "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
miniBossMap = Map(miniBoss)

bossKey  = "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
bossKey += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
bossKey += "SLLLLLLLLLLLllllllllLLLLLLLLLLLS"
bossKey += "SLLLLLLLLLLllllllllllLLLLLLLLLLS"
bossKey += "SLLLLLLLLLLllllllllllLLLLLLLLLLS"
bossKey += "SLLLLLLLLLLllllllllllLLLLLLLLLLS"
bossKey += "SLLLLLLLlllllllllllllllllLLLLLLS"
bossKey += "SLLLLLLlllllllllllllllllllLLLLLS"
bossKey += "SLLLLLlllllllllllllllllllllLLLLS"
bossKey += "SLLLLLlllllllllllllllllllllLLLLS"
bossKey += "SLLLLLlllllllllllllllllllllLLLLS"
bossKey += "SLLLLllllllllllllllllllllllLLLLS"
bossKey += "SLLLLllllllllllc.llllllllllLLLLS"
bossKey += "SLLLLLllllllllllllllllllllLLLLLS"
bossKey += "SLLLLLLllllllllllllllllllLLLLLLS"
bossKey += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossKey += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossKey += "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
bossKeyMap = Map(bossKey)

bossRoom  = "SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS"
bossRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLlllLLLllllllLLLlllLLLLLLS"
bossRoom += "SLLLLllllllllllllllllllllllLLLLS"
bossRoom += "SLLLllllllllllllllllllllllllLLLS"
bossRoom += "SLLLllllllllllllllllllllllllLLLS"
bossRoom += "SLLLllllllllllllllllllllllllLLLS"
bossRoom += "SLLLllllllllllllllllllllllllLLLS"
bossRoom += "SLLLLllllllllllllllllllllllLLLLS"
bossRoom += "SLLLLLllllllllllllllllllllLLLLLS"
bossRoom += "SLLLLLLllllllllllllllllllLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
bossRoom += "SLLLLLLLLLLLLLllllLLLLLLLLLLLLLS"
bossRoom += "SSSSSSSSSSSSSSSllSSSSSSSSSSSSSSS"
bossRoomMap = Map(bossRoom)




dungeonPath = path + "dungeon/"
TOWN_AREA = Area(RawSprite(path + "newBack.png", 0, 0, 6), townMap, townAnimations)
TOWN_AREA.spawnCoords = Coords(13*BITS, 1*BITS)
TOWN_AREA.lightSources.append(LightSource(bigTorchSpritePaths, 416, 288, 1))
TOWN_AREA.lightSources.append(LightSource(bigTorchSpritePaths, 384, 288, 1))
TOWN_AREA.lightSources.append(LightSource(lightpostSpritePaths, 128, 192, 1))
TOWN_AREA.objectList.append(HealingStation(healingStationSpritePaths, 896, 64))
for i in TOWN_AREA.lightSources:
  TOWN_AREA.objectList.append(i)
E_FIELD_AREA = Area(RawSprite(path + "Efield.png", 0, 0, 6), efieldMap, eFieldAnimations)
NE_FIELD_AREA = Area(RawSprite(path + "NEfield.png", 0, 0, 6), nefieldMap)
N_FIELD_AREA = Area(RawSprite(path + "Nfield.png", 0, 0, 6), nfieldMap, nFieldAnimations)
DUNGEON_ENTRANCE_AREA = Area(RawSprite(dungeonPath + "entrance.png", 0, 0, 6), entranceMap)
DUNGEON_EASTROOM_AREA = Area(RawSprite(dungeonPath + "eastRoom.png", 0, 0, 6), eastRoomMap)
DUNGEON_WESTROOM_AREA = Area(RawSprite(dungeonPath + "westRoom.png", 0, 0, 6), westRoomMap)
DUNGEON_KEYROOM_AREA = Area(RawSprite(dungeonPath + "keyRoom.png", 0, 0, 6), keyRoomMap)
DUNGEON_MINIBOSS_AREA = Area(RawSprite(dungeonPath + "miniBoss.png", 0, 0, 6), miniBossMap)
DUNGEON_BOSSKEY_AREA = Area(RawSprite(dungeonPath + "bossKey.png", 0, 0, 6), bossKeyMap)
DUNGEON_BOSSROOM_AREA = Area(RawSprite(dungeonPath + "bossRoom.png", 0, 0, 6), bossRoomMap)

#OverWorld connections
joinNorthSouthAreas(N_FIELD_AREA, TOWN_AREA)
joinNorthSouthAreas(NE_FIELD_AREA, E_FIELD_AREA)
joinEastWestAreas(NE_FIELD_AREA, N_FIELD_AREA)
joinEastWestAreas(E_FIELD_AREA, TOWN_AREA)
joinOtherAreas(NE_FIELD_AREA, DUNGEON_ENTRANCE_AREA)
#Dungeon Connections
joinOtherAreas(DUNGEON_ENTRANCE_AREA, NE_FIELD_AREA)
joinEastWestAreas(DUNGEON_ENTRANCE_AREA, DUNGEON_WESTROOM_AREA)
joinEastWestAreas(DUNGEON_EASTROOM_AREA, DUNGEON_ENTRANCE_AREA)
joinNorthSouthAreas(DUNGEON_KEYROOM_AREA, DUNGEON_WESTROOM_AREA)
joinNorthSouthAreas(DUNGEON_BOSSROOM_AREA, DUNGEON_ENTRANCE_AREA)
joinNorthSouthAreas(DUNGEON_EASTROOM_AREA, DUNGEON_BOSSKEY_AREA)
joinNorthSouthAreas(DUNGEON_MINIBOSS_AREA, DUNGEON_EASTROOM_AREA)



# Currently acts as the "controller" to read inputs
text = gui.TextField("", 1)

# text.onKeyType(function) sets the function to be called on character entry.  Default is keyAction()
# setting "function" to a different function will alter controls. Make sure to pass a function
# that takes exactly one parameter.  onKeyType will pass the character of the typed key as an argument,
# so for example:
#
# def randomFunction(key)
#   if key == "h":
#       doSomething
#
# text.onKeyType(randomFunction)
#
# would activate doSomething if "h" was pressed.
display.add(text, -32, -32)



#CURRENT_AREA = DUNGEON_ENTRANCE_AREA


#loadIntro()  - Intro credits for production build. see loadIntro() definition for details





#display.drawImage(path + "newBack.png", 0, 0)


#Music

move = music(path+"Audio/footstep.wav")
thread.start_new_thread(music.volume, (move, .08,))
move1 = music(path+"Audio/footstep.wav")
thread.start_new_thread(music.volume, (move, .08,))
move2 = music(path+"Audio/footstep.wav")
thread.start_new_thread(music.volume, (move, .08,))
move3 = music(path+"Audio/footstep.wav")
thread.start_new_thread(music.volume, (move, .08,))
move4 = music(path+"Audio/footstep.wav")
thread.start_new_thread(music.volume, (move, .08,))

dead_sound = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
dead_sound2 = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
dead_sound3 = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
dead_sound4  = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
dead_sound5 = music(path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")



hit_sound  = music(path+"Audio/Metal_Bang.wav")

talk_sound = music(path+"Audio/Robot_blip.wav")


background_music = music(path+"Audio/Still-of-Night_Looping.wav")

#background music altered
#quieter_music = music(path+"Audio/Still-of-Night_Looping.wav")
#thread.start_new_thread(music.volume, (quieter_music, .08,))
#thread.start_new_thread(music.speed, (quieter_music, .05,))
#thread.start_new_thread(music.repeat, (quieter_music,))
#thread.start_new_thread(music.Play, (quieter_music,))

#dungeon_sound = music(path+"Audio/Night-Stalker.wav")
#thread.start_new_thread(music.repeat, (dungeon_sound,))
#thread.start_new_thread(music.Play, (dungeon_sound,))








#Menu Sprites
defaultMenu = RawSprite(path +"Menu/menuDefault.png", 230, 0, 0)
itemMenu = RawSprite(path + "Menu/menuItem.png",230, 0, 0)
statusMenu = RawSprite(path + "Menu/menuStatus.png",230, 0, 0)
shopMenu = RawSprite (path + "Menu/shopMenu.png", 230, 0, 0)
#textBox = RawSprite(path + "Menu/textBox.png", 505, 160, 0)
#potion = Potion()
#potion.parental = bot1
#bot1.inv.append(potion)



#display.add(str(bot1.maxHp), 12, 12)
#display.add(bot1.xp, 12, 24)
#df
#atk
#xp
#level
#
#
#itemMenu = menu([str(bot1.hp), str(bot1.xp), str(bot1.level)])
#itemMenu = menu(bot1.inv)
#
#class menu():
#  def __init__(self, listOfThings):
#    self.lineText = listOfThings
#    self.lineDifference = 12
#    for item in lineText:
#      self.addItem(item)
#
#  def addItem(self, item):
#    itemNameX = 250
#    startingY = 42
#    y = startingY
#    itemNo = 1
#    itemNoX = 240
#    for items in self.lineText:
#      display.addOrder(Label(itemNo), x, y, 0)
#      display.addOrder(Label(items.text), x, y, 0)
#      y += 12
#      itemNo +=1
#
#
#  def useItem
#
#if a == "1":
#  bot1.inv[0].use()
#if a == "2":
#  bot1.inv[2].use()
#
#
#
#
#
#me
class Menu():
 def __init__(self):
   global bot1
   self.statusItems = [str(bot1.hp), str(bot1.xp), str(bot1.level)]
   self.invItems = bot1.inv
   self.labelList = []
   #self.sprite = Sprite(path + "Menu/menuStatus.png",230, 0, 0)


 def openMenu(self):
   self.sprite.spawnSprite()


 def showLabels(self):
   x = 625
   y = 171
   for item in self.statusItems:
     label = gui.Label(item)
     display.add(label, x, y)
     self.labelList.append(label)
     y += 100


"""
old code
     status = ([str(bot1.hp), str(bot1.xp), str(bot1.level)])
         x=625
         y=171

         for item in status :
             textBox =  gui.Label(str(item))
             display.add(textBox,x,y)
             y += 100
"""


loadIntro()
