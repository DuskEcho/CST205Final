# Copyright SAGA 2019
# Not to be duplicated without express consent of
# original members. Not for release. 


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


#bits is how many pixels are in each texture
bits = 32
#how many tiles there are wide
widthTiles = 40
#how many tiles there are tall
heightTiles = 24

shopKeeperX = 5*bits
shopKeeperY = 2*bits



#beings
beingList = []
#interactable objects
objectList = []
#gore pieces
gibList = []
animatedSpriteList = []
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






# Dictionaries for items
# Numbers correspond to stats
# arrays in form [attack/def, spritePaths]
userSpritePaths = [path + "RobotSprites/botBlueBack.gif",
               path + "RobotSprites/botBlueFront.gif",
               path + "RobotSprites/botBlueSideLeft.gif",
               path + "RobotSprites/botBlueSideRight.gif",
               path + "RobotSprites/botBlueMovingLeft.gif",
               path + "RobotSprites/botBlueMovingRight.gif",]
blueEnemySpritePaths = [path + "RobotSprites/blueRobotBack.gif",
               path + "RobotSprites/blueRobotFront.gif",
               path + "RobotSprites/BlueRobotSideLeft.gif",
               path + "RobotSprites/BlueRobotSideRight.gif",
               path + "RobotSprites/BlueRobotMovingLeft.gif",
               path + "RobotSprites/BlueRobotMovingRight.gif",]
shopKeeperSpritePaths = [path + "RobotSprites/ShopkeeperbotCloseup.gif",
                         path + "RobotSprites/ShopkeeperbotFront.gif"]
lightpostSpritePaths = [path + "ObjectSprites/lampOff.gif",
                        path + "ObjectSprites/lampOn.gif",
                        path + "ObjectSprites/lampBright.gif"]

weaponStatsList = {    
    "Stick": [1, [path + "WeaponSprites/Stick/stickUp.gif",
                  path + "WeaponSprites/Stick/stickDown.gif",
                  path + "WeaponSprites/Stick/stickLeft.gif",
                  path + "WeaponSprites/Stick/stickRight.gif"]],
   "Rock": [2, "spritePath"]
   }
helmStatsList = {
    "Hair": [0, "spritePath"],
    "Leaf": [1, "spritePath"]
    }
chestStatsList = {
    "BDaySuit": [0, "spritePath"],
    "Fur Coat": [1, "spritePath"]
    }
legsStatsList = {
    "Shame": [0, "spritePath"],
    "Fur Pants": [1, "spritePath"]
    }
feetStatsList = {
    "Toes": [0, "spritePath"],
    "Fur Boots": [1, "spritePath"]
    }
handStatsList = {
    "Digits": [0, "spritePath"],
    "Fur Gloves": [1, "spritePath"]
    }
itemsList = {}  #potions, etc.


lootTable = {}


directionList = {
    "up": 0,
    "down": 1,
    "left": 2,
    "right": 3,
    "movingLeft": 4,
    "movingRight":5
    }




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
    display.add(rawText, coordsX, coordsY)






    
# TEMPORARY TEXT DISPLAY UNTIL MENUS ARE IN PLACE
# Adds the given gui.Label to the display at the Label's coords (default 0, 0)

def showLabel(label):
    display.add(label, 1280*(2/5), 0)


# Deletes all files in folderpath whose name contains targetString

def deleteFilesWithString(folderPath, targetString):
        for file in os.listdir(folderPath):
            print(folderPath)
            if targetString in file:
                os.remove(file)




class TurnCounter():
    def __init__(self):
        self.turn = 0


counter = TurnCounter()
# All actions that depend on the turn counter go here

def turnPass():
    counter.turn += 1
    if counter.turn % 20 == 0:
        spawnEnemy()
    for person in beingList:
        if person.hostile == true:
            person.simpleHostileAI()
    if bot1.hp <= 0:
        bot1.coords.x = 0
        bot1.coords.y = 0
        bot1.sprite.spawnSprite(bot1.coords.x, bot1.coords.y)
    clearBadSprites()

    #total action counter to affect shop/store stock
    





def slideRight(object, targetXBig, sprite):
    time.sleep(.005)
    object.coords.x += 1 
    object.forwardCoords.x += 1
    display.remove(object.sprite)
    object.sprite = sprite
    display.add(object.sprite, object.coords.x, object.coords.y)
    if object.coords.x < targetXBig:
        thread.start_new_thread(slideRight, (object, targetXBig, sprite))



        self, name, weapName, spritePaths, xSpawn, ySpawn, species, level






# Spawns an enemy with the given parameters.  Default is blue enemy lv 1 with stick at random location.

def spawnEnemy(name = ("EnemyBorn" + str(counter.turn)), weap = "Stick", spritePaths = blueEnemySpritePaths,  x = random.randint(0, 10)*32, y =  random.randint(0, 10)*32, species = "orc", level = 1):
    enemy = Enemy(name, weap, spritePaths, x, y, species, level)
    enemy.sprite.spawnSprite(enemy.coords.x, enemy.coords.y)
    





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
    for being in beingList:
        goodSprites.append(being.sprite)
    for sprite in display.items:
        if sprite not in goodSprites and type(sprite) == BeingSprite:
            display.remove(sprite)







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
    if spot > widthTiles * heightTiles: spot = widthTiles * heightTiles - 1
    return Coords(spot % widthTiles, spot / widthTiles)


#given tile Coords give tile Spot in 1d array
def tileCoordToSpot(coord):
    return coord.x + coord.y * widthTiles


#Goes from pixel coords to tile Coords
def coordToTileCoord(coord):
    return Coords(coord.x/bits, coord.y/bits)


#probably bad?
def coordToTile(coord):
    return coord.x/bits + (coord.y * widthTiles)/bits




def placeTex(tex, spot, back):
    startx = (spot * bits) % backWidth;
    starty = ((spot * bits) / backWidth) * bits;
    for x in range(0, bits):
        for y in range(0, bits):
            setColor(getPixel(baseMap, startx + x, starty + y), getColor(getPixel(tex, x, y)))




def textCoordToSpot(x, y):
  col = texWidth/32
  row = texHeight/32
  return x + y*col

def getTexture(spot):
    texture = makeEmptyPicture(bits,bits)
    #spot to coord conversion
    startx = (spot * bits) % texWidth;
    starty = ((spot * bits) / texWidth) * bits;
    for x in range(0, bits):
        for y in range(0, bits):
            setColor(getPixel(texture, x, y), getColor(getPixel(textureMap, x + startx, y + starty)))
    return texture






# intro credits, adjust to add fade, etc.

def loadIntro():
    display.drawImage(path + "Fullscreens\\LogoOmega.png", 0, 0)
    time.sleep(1.5)
    display.drawImage(path + "Fullscreens\\dummyStartScreen.png", 0, 0)
    time.sleep(1.5)










                              
# any function passed to onKeyType() must have one and exactly one
# parameter.  This parameter is how the function knows which key is pressed


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
        turnPass()
  elif a == "A":
        bot1.faceLeft()
        turnPass()
  elif a == "S":
        bot1.faceDown()
        turnPass()
  elif a == "D": 
        bot1.faceRight()
        turnPass()

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






    # To pass to getKeyTyped in order to block inputs 
    # (e.g., during animations or delays)

def blockKeys(a):
    None





          
# Currently only sets up the lootTable

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





        
  





        ####################
        #                  #
        #      CLASSES     #
        #                  #
        ####################




# universal coordinates object 

class Coords():
  def __init__(self, x, y):
    self.x = x
    self.y = y


class Tile():
  def __init__(self, tile, isTraversable, isPassable, isTough, desc):
    self.desc = desc
    self.tileImg = tile
    #can a being walk over
    self.isTraversable = isTraversable
    #can a projectile go over
    self.isPassable = isPassable
    #ai gets 2 turns if player is on this tile
    self.isTough = isTough
    self.beings = {} #array of beings in that tile

  def getImg(self):
    return self.tileImg

  def getTraversable(self):
    return self.isTraversable

  def addBeing(self, being):
    self.beings.append(being)

  def getDesc(self):
    return self.desc


class Map():
    def __init__(self, tileMap):
        self.tileMap = {} #change to make map
        #beings will probably be a dictionary with coords as the key and value is the being at the spot
        self.beings = {} #master holder for all of the beings
        self.Map = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
        self.updateBackground(tileMap, self.Map)
        #for key, value in self.tileMap.iteritems():
            #printNow(key)


    def placeTex(self, tex, spot):
        startx = (spot * bits) % backWidth
        starty = ((spot * bits) / backWidth) * bits
        #printNow(spot)
        self.tileMap.update({spot: tex})
        #placeTex(tex.getImg(), spot, self.Map)
        for x in range(0, bits):
            for y in range(0, bits):
                setColor(getPixel(self.Map, startx + x, starty + y), getColor(getPixel(tex.getImg(), x, y)))


    def updateBackground(self, tiles, back):
        for spot in range(0, len(tiles)):
            if   tiles[spot] == "g": self.placeTex(grass, spot)
            elif tiles[spot] == "s": self.placeTex(stone, spot)
            #not in files yet
            #elif tiles[spot] == "m": placeTex(monster, spot)
            #elif tiles[spot] == "p": placeTex(player, spot)
            #elif tiles[spot] == "w": placeTex(wall, spot)
        writePictureTo(self.Map, path + "newBack.png")

    def isTraversable(self, spot):
        printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1: return false
        printNow(self.tileMap[spot].getTraversable())
        printNow(self.tileMap[spot].getDesc())
        return self.tileMap[spot].getTraversable()









class Doodad():
    def __init__(self, filepaths, x, y):
        self.destructible = false
        self.sprites = filepaths
        self.coords = Coords(x, y)
        self.spriteList = filepaths
        self.sprite = Sprite(filepaths[0], x, y)
        self.sprite.spawnSprite()
        self.isAnimating = false
        self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], x, y)
        objectList.append(self)



class LightSource(Doodad):
    def __init__(self, filepaths, x, y):
        Doodad.__init__(self, filepaths, x, y)
        self.isOn = false
        self.type = "light"
        lightSources.append(self)

    def activate(self):
        if self.isOn == true:
            self.turnOff()
        else:
            self.turnOn()

    def turnOn(self):
        if self.isOn == false:
            self.isOn = true            
            self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], self.coords.x, self.coords.y)
            self.animatedSprite.animate()
            self.sprite.removeSprite()
    def turnOff(self):
        if self.isOn == true:
            self.isOn = false
            animatedSpriteList.remove(self.animatedSprite.spriteList[0])
            animatedSpriteList.remove(self.animatedSprite.spriteList[1])
            self.sprite.removeSprite()
            self.sprite = Sprite(self.sprites[0], self.coords.x, self.coords.y)
            self.sprite.spawnSprite()

    







# Class for merchant items and "buy/sell" transaction

class ItemForSale():
    def __init__(self, price, item):
        self.price = price
        self.item = item

    def buy(self, buyer, seller):
        buyer.inventoryAdd(self.item)
        buyer.changeWallet(self.price * - 1)
        seller.changeWallet(self.price)
        seller.inventoryRemove(self)
        del self
        


class Lootbag():
    def __init__(self, itemList, coords):
        self.contents = itemList
        self.coords = coords
        self.spriteList = [Sprite(path + r"EffectSprites\lootBag.gif", self.coords.x, self.coords.y),
                           Sprite(path + r"EffectSprites\lootBag2.gif", self.coords.x, self.coords.y)]
        self.sprite = self.spriteList[0]
        self.type = "lootbag"
        
        self.spawnSprite()
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






    def spawnSprite(self):
        display.add(self.sprite, self.coords.x, self.coords.y)
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


        




# general class for sprites. Use with display.add(spritename, sprite.coords.x, sprite.coords.y)
# to display on the main screen.
# parameters: 
#   filename    - filename in string format
#   x           - x coordinate
#   y           - y coordinate

class Sprite(gui.Icon):

  def __init__(self, filename, x, y):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM- LEGACY, NOT SURE OF NECESSITY
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, NOT SURE OF NECESSITY
      self.position = (0,0)              # assume placement at a Display's origin- LEGACY, NOT SURE OF NECESSITY
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, NOT SURE OF NECESSITY

      printNow(filename)
      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality)- LEGACY, NOT SURE OF NECESSITY
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )
      self.coords = Coords(x, y)






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self):
        display.add(self, self.coords.x, self.coords.y)
 





      # removes the sprite from the display
        
  def removeSprite(self):
        display.remove(self)











                     
  # inherits from Sprite. Separated to give   See sprite for function exacts. 
  # ownership to sub-sprites (e.g., weapon)

class BeingSprite(Sprite):
  def __init__(self, filename, x, y):
      gui.JPanel.__init__(self)
      gui.Widget.__init__(self)
      filename = gui.fixWorkingDirForJEM( filename )   # does nothing if not in JEM - LEGACY, UNUSED FOR NOW
      self.fileName = filename
      self.offset = (0,0)                # How much to compensate - LEGACY, UNUSED FOR NOW
      self.position = (0,0)              # assume placement at a Display's origin - LEGACY, UNUSED FOR NOW
      self.display = None
      self.degrees = 0                   # used for icon rotation - LEGACY, UNUSED FOR NOW
      printNow(filename)
      self.icon = gui.ImageIO.read(File(filename))
      iconWidth = self.icon.getWidth(None)
      iconHeight = self.icon.getHeight(None)

      # keep a deep copy of the image (useful for repeated scalings - we always scale from original
      # for higher quality) - LEGACY, UNUSED FOR NOW
      self.originalIcon = gui.BufferedImage(self.icon.getWidth(), self.icon.getHeight(), self.icon.getType())
      self.originalIcon.setData( self.icon.getData() )






      # adds the sprite to the display. If the sprite already exists,
      # moves the sprite to the self.coords location

  def spawnSprite(self, x, y):
        display.add(self, x, y)





        
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
    display.add(self, x, y)











          
    # Class for weapon objects. weapName must correspond to a weapon
    # in the weaponList. Contains stats and sprites.
    #
    #
    #
    #spritePaths should be array of order [up, down, left, right]


class Weapon():
    def __init__(self, weapName):
        self.name = weapName
        if self.name != None:
          self.sprites = weaponStatsList[self.name][1]
          self.sprite = Sprite(self.sprites[3], 0, 0)
          self.power = weaponStatsList[self.name][0]
        self.displayed = false
    





        # Displays the weapon's "up/down/left/right" sprite at the coords.
        # For use with being's "self.forwardCoords.x/y" 
        
    def displayUp(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[0], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayDown(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[1], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayLeft(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[2], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true
    def displayRight(self, x, y):
        if self.displayed == false:
            self.sprite = Sprite(self.sprites[3], 0, 0)
            display.add(self.sprite, x, y)
            self.displayed = true






        # removes the weapon from the display

    def hide(self):
        display.remove(self.sprite)
        self.displayed = false










        

    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location

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
        self.forwardCoords = Coords(self.coords.x + bits, self.coords.y)
        self.unchangedSpritePaths = spritePaths
        self.spritePaths = spritePaths
        self.sprite = BeingSprite(self.spritePaths[1], xSpawn, ySpawn)
        self.weapon = Weapon(weapName)
        self.wallet = 0
        self.facing = directionList["right"]
        self.isMoving = false
        self.talkingLines = ["Hello!",
                             "Yes?",
                             "Can I Help you?"]
        self.bloodySprites = []
        self.lightSprites = []
        self.darkSprites = []
        self.inv.append(self.weapon)
        if itemList != None:
            self.inv += itemList
        beingList.append(self)



         


    def activateTarget(self):
      self.getFrontTarget().activate()


        # Updates wallet by amount

    def changeWallet(self, amount):
        self.wallet += amount
        if self.wallet <= 0:
            self.wallet == 0
            




            
        # Adds item to inventory list

    def inventoryAdd(self, item):
        self.inv.append(item)


    def inventoryRemove(self, item):
        self.inv.Remove(item)



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






# Basic enemy AI. Enemy moves in a random direction and attacks if 
# the player is directly in front.

    def simpleHostileAI(self):
        distanceX = self.coords.x - bot1.coords.x
        distanceY = self.coords.y - bot1.coords.y
        closeProximity = bits * 3
        if self.forwardCoords.x == bot1.coords.x and self.forwardCoords.y == bot1.coords.y:
            self.meleeAtk()
        elif self.coords.x-bits == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceLeft()
            self.meleeAtk()
        elif self.coords.x+bits == bot1.coords.x and self.coords.y == bot1.coords.y:
            self.faceRight()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y+bits == bot1.coords.y:
            self.faceDown()
            self.meleeAtk()
        elif self.coords.x == bot1.coords.x and self.coords.y-bits == bot1.coords.y:
            self.faceUp()
            self.meleeAtk()
        elif abs(self.coords.x - bot1.coords.x) < bits and abs(self.coords.y - bot1.coords.y) < bits:
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
        loot = Lootbag(self.inv, self.coords)
        objectList.append(loot)






        # Actions to be taken on hp <= 0

    def dead(self):
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        beingList.remove(self)
        del self


        # Handles lighting of sprites. If a valid light object is within the range
        # currently set to bits * 3, a new set of sprites will be created and applied
        # to simulate lighting.
        # Starts a new thread.

    def lightenDarken(self):
        bright = self.lightWithinRange(bits * 3)
        if self.spritePaths != self.lightSprites and bright:
            self.lightenPixels()
        elif self.spritePaths == self.lightSprites and not bright:
            self.resumePixels()
            deletePath = path + "RobotSprites"
            deleteKey = self.name + str(beingList.index(self)) + "lightSprite"
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


    def threadDeleteLightSprites(self, x):
        for sprite in self.lightSprites:
            os.remove(sprite)
        self.lightSprites = []

    def resumePixels(self):
        self.spritePaths = self.darkSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[self.facing], self.coords.x, self.coords.y)
        self.sprite.spawnSprite(self.coords.x, self.coords.y)


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
            newPicPath = path + "RobotSprites\\" + self.name + str(beingList.index(self)) + "lightSprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.lightSprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.lightSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.lightSprites[self.facing], self.coords.x, self.coords.y)
        self.sprite.spawnSprite(self.coords.x, self.coords.y)
        

    def bloodify(self):
        spriteNum = 0
        for sprites in range(0, len(self.spritePaths)):
            pic = makePicture(self.spritePaths[sprites])
            for x in range(0, getWidth(pic)-1):
                for y in range(0, getHeight(pic)-1):
                    p = getPixel(pic, x, y)
                    if getColor(p) != makeColor(0, 0, 0):
                        if random.randint(0, 100) > (self.hp*100)/self.maxHp:
                            setColor(p, makeColor(114, 87, 7))
            newPicPath = path + "RobotSprites\\" + self.name + str(beingList.index(self)) + "bloodySprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.bloodySprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.bloodySprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.bloodySprites[self.facing], self.coords.x, self.coords.y)
        self.sprite.spawnSprite(self.coords.x, self.coords.y)
  




        # For use with actions that can target more than one target (e.g., attacks)

    def getFrontTargetList(self):
        bigList = beingList + objectList
        targetList = []
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                targetList.append(target)
        return targetList
        






        #for use with actions that can only target one target (e.g., talking)

    def getFrontTarget(self):
        bigList = beingList + objectList
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                return target

            


            
        #needs to be reworked for better decomp
        #
        # activates the melee attack action.
        # displays the weapon at the being's forward coord
        # and activates a damage calculation if any being is there
        # Friendly fire is enabled. Attacking a friendly turns them hostile
        # if the target is killed, exp is calculated.  If the player is killed,
        # the player loses all levels/items and respawns as a new instance of the
        # User class.

    def meleeAtk(self):
        self.displayWeapon()
        x = 1
        thread.start_new_thread(threadRemoveSprite, (.2, self.weapon.sprite))
        self.weapon.displayed = false
        for target in self.getFrontTargetList():
            if target != bot1:
                target.hostile = true
            damage = self.atk
            if damage <= 0:
                damage = 1
            target.changeHp(damage*(-1))
            target.displayDamage()
            if target.hp <= 0:
                self.changeXp(target.xpValue)
                    
            



                    
        # Display's the "damage splash" sprite at
        # the given location. Uses multithreading.

    def displayDamage(self):
        damage = Sprite(path + r"EffectSprites\damage.gif", self.coords.x, self.coords.y)
        display.add(damage, self.coords.x, self.coords.y)
        thread.start_new_thread(threadRemoveSprite, (.25, damage))

        




        # For use with meleeAtk and thread.start_new_thread().
        # may be removed and have functionality replaced by 
        # more general function

    def threadHideWeapon(self, x):
            time.sleep(.2)
            self.weapon.hide()






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


    
    def pickUpLoot(self, coords):
        for item in objectList:
            if item.type == "lootbag" and item.coords.x == coords.x and item.coords.y == coords.y:
                self.inv += item.contents
                item.removeSprite()
                objectList.remove(item)
                del item



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
        self.faceUp()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y >= 0 and baseMap.isTraversable(targetSpot):
            self.coords.y -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveUp, (x,))
            if self.facing == directionList["up"]: 
              self.forwardCoords.y = self.coords.y - bits - bits/2
              self.forwardCoords.x = self.coords.x
        else:
            self.isMoving = false
                           
    def threadMoveUp(self, x):
        time.sleep(.15)
        self.coords.y -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        

    def moveDown(self):
        self.faceDown()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y < backHeight and baseMap.isTraversable(targetSpot):
            self.coords.y += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveDown, (x,))
            self.sprite.moveTo(self.coords.x, self.coords.y)
            if self.facing == directionList["down"]:
              self.forwardCoords.y = self.coords.y + bits + bits/2
              self.forwardCoords.x = self.coords.x
        else:
            self.isMoving = false
                   
    def threadMoveDown(self, x):
        time.sleep(.15)
        self.coords.y += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()


    def moveLeft(self):
        self.faceLeft()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x >= 0 and baseMap.isTraversable(targetSpot):
            self.coords.x -= bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[4], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveLeft, (x,))
            if self.facing == directionList["left"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x - bits - bits/2 
        else:
            self.isMoving = false

    def threadMoveLeft(self, x):
        time.sleep(.15)
        self.coords.x -= bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[2], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()

    def moveRight(self):
        self.faceRight()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x < backWidth and baseMap.isTraversable(targetSpot):
            self.coords.x += bits/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[5], self.coords.x, self.coords.y)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveRight, (x,))
            if self.facing == directionList["right"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x + bits+ bits/2
        else:
            self.isMoving = false


    def threadMoveRight(self, x):
        time.sleep(.1)
        self.coords.x += bits/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[3], self.coords.x, self.coords.y)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.isMoving = false
        self.pickUpLoot(self.coords)
        self.lightenDarken()


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
          self.sprite = BeingSprite(self.spritePaths[0], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.y = self.coords.y - bits
          self.forwardCoords.x = self.coords.x
                           
    def faceDown(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["down"]:
          self.facing = directionList["down"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[1], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.y = self.coords.y + bits
          self.forwardCoords.x = self.coords.x
                   
    def faceLeft(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["left"]:
          self.facing = directionList["left"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[2], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.x = self.coords.x - bits
          self.forwardCoords.y = self.coords.y
                   
    def faceRight(self):
        #playAnimation
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != directionList["right"]:
          self.facing = directionList["right"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[3], self.coords.x, self.coords.y)
          self.sprite.spawnSprite(self.coords.x, self.coords.y)
          self.forwardCoords.x = self.coords.x + bits
          self.forwardCoords.y = self.coords.y











class ShopKeeper(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [Sprite(path + r"RobotSprites/shopKeeperGib1.gif", self.coords.x, self.coords.y),
                              Sprite(path + r"RobotSprites/shopKeeperGib2.gif", self.coords.x, self.coords.y)
                              ]








    def giblets(self):
        animatedGib = AnimatedGiblets(path + r"RobotSprites/shopKeeperGib1.gif", path + r"RobotSprites/shopKeeperGib2.gif", random.randint(self.coords.x - bits, self.coords.x + bits), random.randint(self.coords.y - bits, self.coords.y + bits))
        animatedGib.animate()



    def dead(self):
        #play animation
        #delete coordinate data from grid
        self.giblets()
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        beingList.remove(self)
        del self








    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class Enemy(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, species, level):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        self.species = species 
        for val in range(0, level):
            self.levelUp()
        self.gibSpriteList = [Sprite(path + r"RobotSprites\enemyArmGib.gif", self.coords.x, self.coords.y),
                              Sprite(path + r"RobotSprites\enemyLegGib.gif", self.coords.x, self.coords.y),
                              Sprite(path + r"RobotSprites\enemyLegGib2.gif", self.coords.x, self.coords.y),
                              Sprite(path + r"RobotSprites\enemyBodyGib.gif", self.coords.x, self.coords.y),
                              Sprite(path + r"RobotSprites\enemyHeadGib.gif", self.coords.x, self.coords.y),
                              ]
        self.hostile = true
        





        
        # in progress loot-dropping function

    def dropLoot(self):
        items = []
        items.append(self.randomInvItem())
        loot = Lootbag(items, self.coords)
        objectList.append(loot)





    def gibSpawn(self, gibSprite, x, y):
        gibList.append(gibSprite)
        display.add(gibSprite, x, y)



    def giblets(self):
        gibIndex = 0
        for i in range(0, random.randint(0, len(self.gibSpriteList))):
            self.gibSpawn(self.gibSpriteList[gibIndex], random.randint(self.coords.x - bits, self.coords.x + bits), random.randint(self.coords.y - bits, self.coords.y + bits))
            print(gibIndex)
            gibIndex += 1



        # in progress hp == 0 action

    def dead(self):
        #play animation
        #delete coordinate data from grid
        self.giblets()
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        beingList.remove(self)
        del self
        




               
        # returns a random item from the inv list

    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]
            



        






        
        # Class for armor/equipment, in development

class Armor():
    def __init__(self, name):
        self.armorType = "FIX THIS CLASS"






# used for sprite animation, flickering between two sprites at random
# used for twitching/sparking/flames


class AnimatedGiblets():
    def __init__(self, filename1, filename2, x, y):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, x, y),
                           Sprite(filename2, x, y)]
        self.sprite = self.spriteList[0]
        gibList.append(self.spriteList[0])
        gibList.append(self.spriteList[1])
        self.coords = Coords(x, y)




        #activates animation

    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))






        # sprite addition and removal to and from display

    def spawnSprite(self):
        display.add(self.sprite, self.coords.x, self.coords.y)
    def removeSprite(self):
        display.remove(self.sprite)


    def threadAnimate(self, container):
        while self.spriteList[0] in gibList or self.spriteList[1] in gibList:
            time.sleep(random.randint(0, 2)/10.0)
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
                     
            











# used for sprite animation, flickering between two sprites at random
# used for twitching/sparking/flames


class StationaryAnimatedSprite():
    def __init__(self, filename1, filename2, x, y):
        self.coords = Coords(x, y)
        self.spriteList = [Sprite(filename1, x, y),
                           Sprite(filename2, x, y)]
        self.sprite = self.spriteList[0]
        animatedSpriteList.append(self.spriteList[0])
        animatedSpriteList.append(self.spriteList[1])
        self.coords = Coords(x, y)




    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))

    def spawnSprite(self):
        display.add(self.sprite, self.coords.x, self.coords.y)
    def removeSprite(self):
        display.remove(self.sprite)


    def threadAnimate(self, container):
        while self.spriteList[0] in animatedSpriteList or self.spriteList[1] in animatedSpriteList:
            time.sleep(random.randint(0, 2)/10.0)
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










    # Class for living entities (people, enemies, bosses, etc.)
    # handles stats, movement, experience, inventory
    # spritePaths should be an array of order [up, down, leftFace, rightFace, leftMove, rightMove]
    # All beings are added to the beingList[]
    # Parameters:
    #   name:           - Being's name as a string
    #   weapName:       - Being's starting weapon as a string - must correlate with weaponList
    #   spritePaths:    - list containing the filePaths of the Being's sprites
    #   xSpawn:         - initial x location
    #   ySpawn:         - initial y location
    #   species:        - Being's species as a string
    #   level:          - Being's starting level

class User(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        self.name = name
        self.helm = "Hair"
        self.chest = "BDaySuit"
        self.legs = "Shame"
        self.boots = "Toes"
        self.gloves = "Digits"

        self.sprite.spawnSprite(self.coords.x, self.coords.y)





    def giblets():
        None


               # EQUIPMENT CLUSTER
        # The following 6 functions handle equipping items
        # to  specific parts of the body.  Atk and Df stats
        # are adjusted accordingly.  The equipped item must
        # correlate to one of the itemLists

    def setWeapon(self, weapon):
        if self.weapon != "Stick":
            inventoryAdd(self.weapon)
        self.atk -= weaponStatsList[self.weapon]
        self.weapon = weapon
        self.atk += weaponStatsList[self.weapon]
               

    def setHelm(self, helm):
        if self.helm != "Hair":
            inventoryAdd(self.helm)
        self.df -= helmStatsList(self.helm)
        self.helm = helm
        self.df += helmStatsList(self.helm)


    def setChest(self, chest):
        if self.chest != "BDaySuit":
            inventoryAdd(self.chest)
        self.df -= chestStatsList(self.chest)
        self.chest = chest
        self.df += chestStatsList(self.chest)
               

    def setLegs(self, legs):
        if self.legs != "Shame":
            inventoryAdd(self.legs)
        self.df -= legsStatsList(self.legs)
        self.legs = legs
        self.df += legsStatsList(self.legs)
                 
        
    def setBoots(self, boots):
        if self.boots != "Toes":
            inventoryAdd(self.boots)
        self.df -= bootsStatsList(self.boots)
        self.boots = boots
        self.df += bootsStatsList(self.boots)
        

    def setGloves(self, gloves):
        if self.gloves != "Digits":
            inventoryAdd(self.gloves)
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
            delayRemoveObject(label, 2)

    def talk(self):
        target = self.getFrontTarget()
        speech = gui.Label(target.talkingLines[random.randint(0, len(target.talkingLines)-1)])
        showLabel(speech)
        delayRemoveObject(speech, 2)

    def dead(self):
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        self.__init__("bot1", "Stick", userSpritePaths, 32, 32)



            ######################
            #                    #
            #    PSEUDO-MAIN     #
            #                    #
            ######################







textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")
#explore(textureMap)

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)
#initailize textures
stone = Tile(getTexture(textCoordToSpot(3,24)), false, true, false, "stone")
grass = Tile(getTexture(textCoordToSpot(10,19)), true, true, false, "grass")


#create emply grass field will clean up later
home  = "ssssssssssssssssssssssssssssssssssssssss"
home += "sggsggggggggggggggsgsgsgsgsgsgsgsgsgsgss"
home += "sggsgggggggggggggsgsgsgsgssggggggggggggs"
home += "sggsssgggggggsgggggggggggggggggggggggggs"
home += "sgggssgggggggsgggggggggggggggggggggggggs"
home += "sgggssssssssssgggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggggggggggg"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "sggggggggggggggggggggggggggggggggggggggs"
home += "ssssssssssssssssssssssssssssssssssssssss"
#initailize background image
backWidth = bits * widthTiles
backHeight = bits * heightTiles
baseMap = Map(home)
#background = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
#updateBackground(home)


display = gui.Display("Robot Saga", backWidth, backHeight)
#loadIntro()
text = gui.TextField("", 1)
text.onKeyType(keyAction)
display.add(text)
#create background (probably prerender home background later)
display.drawImage(path + "newBack.png", 0, 0)

bot1 = User("bot1", "Stick", userSpritePaths, 32, 32)
shopKeeper = ShopKeeper("shopKeep", "Stick", shopKeeperSpritePaths, shopKeeperX, shopKeeperY)
light = LightSource(lightpostSpritePaths, 256, 256)
shopKeeper.sprite.spawnSprite(shopKeeper.coords.x, shopKeeper.coords.y)






