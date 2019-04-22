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
import sys










        ####################
        #                  #
        #      CLASSES     #
        #                  #
        ####################






class music():

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







# Basic class for turn counter instances.

class TurnCounter():
  def __init__(self):
        self.turn = 0






# universal coordinates object. Coords in pixels.

class Coords():
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def printCoords(self):
      printNow(str(self.x) + "," + str(self.y))






    # A custom class created to override gui.Display's default destructor.
    # Though not useful for Python, this will be useful when converting to a new language

class CustomDisplay(gui.Display):


  def __init__(self, title = "", width = 600, height = 400, x=0, y=0, color = None):
    gui.Display.__init__(self, title, width, height, x, y, color)
  def __del__(self):
    #insert stop music logic here
    music.Stop(SoundData.move)
    music.Stop(SoundData.dead_sound)
    music.Stop(SoundData.quieter_music)
    music.Stop(SoundData.background_Music)
    music.Stop(SoundData.dungeon_sound)
    gui.display.__del__(self)






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
        WorldData.display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)

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
        WorldData.display.remove(self)





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
      try:
        self.icon = gui.ImageIO.read(File(filename))
      except:
        None
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
        WorldData.display.place(self, self.parental.coords.x, self.parental.coords.y, self.layer)



      # removes the sprite

  def removeSprite(self):
        WorldData.display.remove(self)



      # not a huge fan of the weaponOut flag, but it works for now.
      # without the check in putAwayWeap, JES complains

  def displayWeapon(self, sprite, coords):
    WorldData.display.add(sprite, coords.x, coords.y)



      # hides the weapon. may be unnecessary if we get
      # animations figured out

  def hideWeapon(self):
      WorldData.display.remove(self.weap)



      #moves sprite to location given

  def moveTo(self, x, y):
      self.parental.coords.x = x
      self.parental.coords.y = y
      WorldData.display.addOrder(self, 4, x, y)






    # Class used when an ownerless sprite is needed
    # Acts as a sprite with Coords

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






class WorldData():
  BITS = 32
  WIDTH_TILES = 32
  HEIGHT_TILES = 18
  backWidth = BITS * WIDTH_TILES
  backHeight = BITS * HEIGHT_TILES
  PIXEL_WIDTH = WIDTH_TILES * BITS
  PIXEL_HEIGHT = HEIGHT_TILES * BITS
  MAX_BEINGS = 6
  MAX_INVENTORY = 10
  CURRENT_AREA = None
  CURRENT_BG = None
  bot1 = None
  menu = None
  layer0 = None
  layer1 = None
  layer2 = None
  layer3 = None
  layer4 = None
  layer5 = None
  layer6 = None
  currentMap = None
  try:
           path #test to see if WorldData.path exists
  except NameError: #if WorldData.path does not exist make new WorldData.path
           printNow("Please select your game install folder")
           path = pickAFolder()
  else:
    printNow("Welcome Back") #welcome the player back to the game
  display = None
  loading = None
  title = None
  startScreen = None
  dirt = None
  dirtWall = None
  grass = None
  stone = None
  stoneWall = None
  hole = None
  lavaRock = None
  water = None
  lava = None
  fence = None
  chest = None
  door = None
  blank = None
  shopKeeper = None
  friendlyOrange = None
  friendlyGreen = None
  boss = None

  # Currently acts as the "controller" to read inputs

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
  text = gui.TextField("", 1)
  structPath = None
  counter = TurnCounter()
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






class ListData():


  # Dictionaries for items
  # Numbers correspond to stats


  # Weapon dictionary. Array in form [attack power, weaponSprites[], burnable, flamingWeaponSprites[], range, currencyValue]
  # weaponSprites and flamingWeaponSprites arrays in form [first up frame, first down frame, first left frame,
  # first right frame, repeat for frames two and three]
  weaponStatsList = {
      "Stick": [1, [WorldData.path + "WeaponSprites/Stick/stickUp1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickDown1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickLeft1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickRight1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickUp2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickDown2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickLeft2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickRight2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickUp3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickDown3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickLeft3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickRight3.gif",], true, [WorldData.path + "WeaponSprites/Stick/stickFireUp1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireDown1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireLeft1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireRight1.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireUp2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireDown2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireLeft2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireRight2.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireUp3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireDown3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireLeft3.gif",
                    WorldData.path + "WeaponSprites/Stick/stickFireRight3.gif"], 1, 0],
      "Rock": [2, [WorldData.path + "WeaponSprites/Rock/rockUp1.gif",
                    WorldData.path + "WeaponSprites/Rock/rockDown1.gif",
                    WorldData.path + "WeaponSprites/Rock/rockLeft1.gif",
                    WorldData.path + "WeaponSprites/Rock/rockRight1.gif",
                    WorldData.path + "WeaponSprites/Rock/rockUp2.gif",
                    WorldData.path + "WeaponSprites/Rock/rockDown2.gif",
                    WorldData.path + "WeaponSprites/Rock/rockLeft2.gif",
                    WorldData.path + "WeaponSprites/Rock/rockRight2.gif",
                    WorldData.path + "WeaponSprites/Rock/rockUp3.gif",
                    WorldData.path + "WeaponSprites/Rock/rockDown3.gif",
                    WorldData.path + "WeaponSprites/Rock/rockLeft3.gif",
                    WorldData.path + "WeaponSprites/Rock/rockRight3.gif",], false, None, 1, 200],
      "Sword": [5, [WorldData.path + "WeaponSprites/Sword/swordUp1.gif",
                    WorldData.path + "WeaponSprites/Sword/swordDown1.gif",
                    WorldData.path + "WeaponSprites/Sword/swordLeft1.gif",
                    WorldData.path + "WeaponSprites/Sword/swordRight1.gif",
                    WorldData.path + "WeaponSprites/Sword/swordUp2.gif",
                    WorldData.path + "WeaponSprites/Sword/swordDown2.gif",
                    WorldData.path + "WeaponSprites/Sword/swordLeft2.gif",
                    WorldData.path + "WeaponSprites/Sword/swordRight2.gif",
                    WorldData.path + "WeaponSprites/Sword/swordUp3.gif",
                    WorldData.path + "WeaponSprites/Sword/swordDown3.gif",
                    WorldData.path + "WeaponSprites/Sword/swordLeft3.gif",
                    WorldData.path + "WeaponSprites/Sword/swordRight3.gif"], false, None, 1, 1000],
      "Botsmasher": [12, [WorldData.path + "WeaponSprites/Botsmasher/botsmasherUp1.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherDown1.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherLeft1.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherRight1.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherUp2.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherDown2.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherLeft2.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherRight2.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherUp3.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherDown3.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherLeft3.gif",
                    WorldData.path + "WeaponSprites/Botsmasher/botsmasherRight3.gif"], false, None, 1, 10000]
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

  mapNameList = ["town", "dungeon", "WorldData.path"]






class SpriteData():

  # Sprite paths for beings. Arrays in form [back, front, left, right,
  # moving left, moving right, moving front, moving back]

  userSpritePaths = [WorldData.path + "RobotSprites/botBlueBack.gif",
                 WorldData.path + "RobotSprites/botBlueFront.gif",
                 WorldData.path + "RobotSprites/botBlueSideLeft.gif",
                 WorldData.path + "RobotSprites/botBlueSideRight.gif",
                 WorldData.path + "RobotSprites/botBlueMovingLeft.gif",
                 WorldData.path + "RobotSprites/botBlueMovingRight.gif",
                 WorldData.path + "RobotSprites/botBlueMovingFront.gif",
                 WorldData.path + "RobotSprites/botBlueMovingBack.gif",]
  friendlyGreenSpritePaths = [WorldData.path + "RobotSprites/botGreenBack.gif",
                 WorldData.path + "RobotSprites/botGreenFront.gif",
                 WorldData.path + "RobotSprites/botGreenSideLeft.gif",
                 WorldData.path + "RobotSprites/botGreenSideRight.gif",
                 WorldData.path + "RobotSprites/botGreenMovingLeft.gif",
                 WorldData.path + "RobotSprites/botGreenMovingRight.gif",
                 WorldData.path + "RobotSprites/botGreenMovingFront.gif",
                 WorldData.path + "RobotSprites/botGreenMovingBack.gif",]
  friendlyOrangeSpritePaths = [WorldData.path + "RobotSprites/botOrangeBack.gif",
                 WorldData.path + "RobotSprites/botOrangeFront.gif",
                 WorldData.path + "RobotSprites/botOrangeSideLeft.gif",
                 WorldData.path + "RobotSprites/botOrangeSideRight.gif",
                 WorldData.path + "RobotSprites/botOrangeMovingLeft.gif",
                 WorldData.path + "RobotSprites/botOrangeMovingRight.gif",
                 WorldData.path + "RobotSprites/botOrangeFront.gif",
                 WorldData.path + "RobotSprites/botOrangeBack.gif",]
  friendlyPinkSpritePaths = [WorldData.path + "RobotSprites/botPinkBack.gif",
                 WorldData.path + "RobotSprites/botPinkFront.gif",
                 WorldData.path + "RobotSprites/botPinkSideLeft.gif",
                 WorldData.path + "RobotSprites/botPinkSideRight.gif",
                 WorldData.path + "RobotSprites/botPinkMovingLeft.gif",
                 WorldData.path + "RobotSprites/botPinkMovingRight.gif",
                 WorldData.path + "RobotSprites/botPinkFront.gif",
                 WorldData.path + "RobotSprites/botPinkBack.gif",]
  friendlyYellowSpritePaths = [WorldData.path + "RobotSprites/botYellowBack.gif",
                 WorldData.path + "RobotSprites/botYellowFront.gif",
                 WorldData.path + "RobotSprites/botYellowSideLeft.gif",
                 WorldData.path + "RobotSprites/botYellowSideRight.gif",
                 WorldData.path + "RobotSprites/botYellowMovingLeft.gif",
                 WorldData.path + "RobotSprites/botYellowMovingRight.gif",
                 WorldData.path + "RobotSprites/botYellowFront.gif",
                 WorldData.path + "RobotSprites/botYellowBack.gif",]
  blueEnemySpritePaths = [WorldData.path + "RobotSprites/blueRobotBack.gif",
                 WorldData.path + "RobotSprites/blueRobotFront.gif",
                 WorldData.path + "RobotSprites/BlueRobotSideLeft.gif",
                 WorldData.path + "RobotSprites/BlueRobotSideRight.gif",
                 WorldData.path + "RobotSprites/BlueRobotMovingLeft.gif",
                 WorldData.path + "RobotSprites/BlueRobotMovingRight.gif",
                 WorldData.path + "RobotSprites/BlueRobotMovingFront.gif",
                 WorldData.path + "RobotSprites/BlueRobotMovingBack.gif",]
  greenEnemySpritePaths = [WorldData.path + "RobotSprites/GreenRobotBack.gif",
                 WorldData.path + "RobotSprites/GreenRobotFront.gif",
                 WorldData.path + "RobotSprites/GreenRobotSideLeft.gif",
                 WorldData.path + "RobotSprites/GreenRobotSideRight.gif",
                 WorldData.path + "RobotSprites/GreenRobotMovingLeft.gif",
                 WorldData.path + "RobotSprites/GreenRobotMovingRight.gif",
                 WorldData.path + "RobotSprites/GreenRobotFront.gif",
                 WorldData.path + "RobotSprites/GreenRobotBack.gif",]
  redEnemySpritePaths = [WorldData.path + "RobotSprites/RedRobotBack.gif",
                 WorldData.path + "RobotSprites/RedRobotFront.gif",
                 WorldData.path + "RobotSprites/RedRobotSideLeft.gif",
                 WorldData.path + "RobotSprites/RedRobotSideRight.gif",
                 WorldData.path + "RobotSprites/RedRobotMovingLeft.gif",
                 WorldData.path + "RobotSprites/RedRobotMovingRight.gif",
                 WorldData.path + "RobotSprites/RedRobotFront.gif",
                 WorldData.path + "RobotSprites/RedRobotBack.gif",]
  purpleEnemySpritePaths = [WorldData.path + "RobotSprites/PurpleRobotBack.gif",
                 WorldData.path + "RobotSprites/PurpleRobotFront.gif",
                 WorldData.path + "RobotSprites/PurpleRobotSideLeft.gif",
                 WorldData.path + "RobotSprites/PurpleRobotSideRight.gif",
                 WorldData.path + "RobotSprites/PurpleRobotMovingLeft.gif",
                 WorldData.path + "RobotSprites/PurpleRobotMovingRight.gif",
                 WorldData.path + "RobotSprites/PurpleRobotFront.gif",
                 WorldData.path + "RobotSprites/PurpleRobotBack.gif",]
  yellowEnemySpritePaths = [WorldData.path + "RobotSprites/YellowRobotBack.gif",
                 WorldData.path + "RobotSprites/YellowRobotFront.gif",
                 WorldData.path + "RobotSprites/YellowRobotSideLeft.gif",
                 WorldData.path + "RobotSprites/YellowRobotSideRight.gif",
                 WorldData.path + "RobotSprites/YellowRobotMovingLeft.gif",
                 WorldData.path + "RobotSprites/YellowRobotMovingRight.gif",
                 WorldData.path + "RobotSprites/YellowRobotFront.gif",
                 WorldData.path + "RobotSprites/YellowRobotBack.gif",]
  shopKeeperSpritePaths = [WorldData.path + "RobotSprites/ShopkeeperbotBack.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotFront.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotLeft.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotRight.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotMovingLeft.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotMovingRight.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotMovingFront.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotMovingBack.gif",
                 WorldData.path + "RobotSprites/ShopkeeperbotCloseup.gif",]
  bossDragonHeadSpritePaths = [WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png",
                               WorldData.path + "dungeon/boss/SkullDragonHeadLarge.png"]
  emptySpritePaths = [WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif",
                      WorldData.path + "emptySprite.gif"]
  bossRightHandSpritePaths = [WorldData.path + "dungeon/boss/AttackRightHand.png",
                              WorldData.path + "dungeon/boss/AttackRightHand.png"]
  bossLeftHandSpritePaths = [WorldData.path + "dungeon/boss/AttackLeftHand.png",
                             WorldData.path + "dungeon/boss/AttackLeftHand.png"]
  bombSpritePaths = [WorldData.path + "dungeon/boss/BombDrop.png",
                     WorldData.path + "dungeon/boss/BombDrop.png",
                     WorldData.path + "dungeon/boss/BombExplode.png",
                     WorldData.path + "dungeon/boss/BombAfter.png",
                     WorldData.path + "dungeon/boss/BombAfter.png",
                     WorldData.path + "dungeon/boss/BombAfter.png",
                     WorldData.path + "dungeon/boss/BombAfter.png",
                     WorldData.path + "dungeon/boss/BombAfter.png"]
  doorSpritePaths = [WorldData.path + "ObjectSprites/tempDoorSprite.gif"]


  # Sprites for light sources.  Arrays in form [off, on, bright]
  lightpostSpritePaths = [WorldData.path + "ObjectSprites/lampOff.gif",
                          WorldData.path + "ObjectSprites/lampOn.gif",
                          WorldData.path + "ObjectSprites/lampBright.gif"]
  torchSpritePaths = [WorldData.path + "ObjectSprites/metalTorchOff.gif",
                          WorldData.path + "ObjectSprites/metalTorchOn1.gif.gif",
                          WorldData.path + "ObjectSprites/metalTorchOn2.gif.gif"]

  bigTorchSpritePaths = [WorldData.path + "ObjectSprites/metalBigTorchOff.gif",
                          WorldData.path + "ObjectSprites/metalBigTorchOn1.gif",
                          WorldData.path + "ObjectSprites/metalBigTorchOn2.gif"]
  healingStationSpritePaths = [WorldData.path + "ObjectSprites/rechargeStation1.gif",
                          WorldData.path + "ObjectSprites/rechargeStation2.gif",
                          WorldData.path + "ObjectSprites/rechargeStation3.gif",
                          WorldData.path + "ObjectSprites/rechargeStation4.gif"]






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



        # Initiates the animation by creating a new thread.
    def animate(self):
        WorldData.animatedSpriteList.append(self)
        self.isAnimating = true
        thread.start_new_thread(self.threadAnimate, (None,))
    def stopAnimating(self):
        WorldData.animatedSpriteList.remove(self)



        # Sprite creation/removal
    def spawnSprite(self):
        self.sprite.spawnSprite()
    def removeSprite(self):
        WorldData.display.remove(self.sprite)



        # Actual animation logic. Meant for use in thread.start_new_thread().
        # Flickers between two sprites at random intervals. Animation is stopped when
        # the object is removed from the animatedSpriteList
    def threadAnimate(self, container):
        while self in WorldData.animatedSpriteList:
            time.sleep(random.randint(0, 2)/10.0)
            placeHolderSprite = self.spriteList[0]
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in WorldData.animatedSpriteList:
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
        WorldData.animatedSpriteList.append(self)
        self.isAnimating = true
        thread.start_new_thread(self.threadAnimate, (None,))



    def stopAnimating(self):
        WorldData.animatedSpriteList.remove(self)



        # shortcut to object's sprite functions
    def spawnSprite(self):
        self.sprite.spawnSprite()
    def removeSprite(self):
        WorldData.display.remove(self.sprite)



        # core animation, cycles through the sprites repeatedly at set intervals
    def threadAnimate(self, x):
        self.sprite = self.spriteList[2]
        time.sleep(self.secondsBetween)
        while self in WorldData.animatedSpriteList:
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
        if self not in WorldData.animatedSpriteList:
            self.removeSprite()
            self.sprite = self.spriteList[2]
            del self



        # Runs one 3-stage animation cycle by creating a new thread
    def animateOnce(self):
        WorldData.animatedSpriteList.append(self)
        self.isAnimating = true
        thread.start_new_thread(self.threadAnimateOnce, (None,))



    def threadAnimateOnce(self, x):
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
        WorldData.animatedSpriteList.remove(self)






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
        self.music = music(WorldData.path+"Audio/Strange-Zone.wav")



    def isTraversable(self, being, spot):
        if self.mapObject.isTraversable(spot):
            testCoords = tileSpotToCoord(spot)
            #TODO beinglist and objectList into dicitionary so I can look up effifiently
            for thing in self.beingList:
                if thing.name == being.name:
                    continue
                if testCoords.x == thing.coords.x and testCoords.y == thing.coords.y:
                    return false
            for thing in self.objectList:
                if thing.isPassable:
                    continue
                if testCoords.x == thing.coords.x and testCoords.y == thing.coords.y:
                    return false
            return true
        return false



    def activateAnimations(self):
        for animatedSprite in self.persistentAnimations:
          animatedSprite.animate()






class AreaData():
  TOWN_AREA = Area(RawSprite(WorldData.path + "newBack.png", 0, 0, 6), None, [StationaryAnimatedSprite(WorldData.path + "/EffectSprites/blankWater.gif", WorldData.path + "/EffectSprites/waterMoving.gif", 256, 352),
                  ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 320, 0, .3),
                  ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 896, 384, .3)])
  E_FIELD_AREA = Area(RawSprite(WorldData.path + "Efield.png", 0, 0, 6), None, [ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 768, 384, .2),
                    ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 864, 384, .2),
                    ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 832, 288, .2)])
  NE_FIELD_AREA = Area(RawSprite(WorldData.path + "NEfield.png", 0, 0, 6), None)
  N_FIELD_AREA = Area(RawSprite(WorldData.path + "Nfield.png", 0, 0, 6), None, [ThreeStageAnimationCycle(WorldData.path + "/EffectSprites/sakuraMoving1.gif", WorldData.path + "/EffectSprites/sakuraMoving2.gif", WorldData.path + "/EffectSprites/sakuraMoving3.gif", 480, 192, .3)])
  dungeonPath = WorldData.path + "dungeon/"
  DUNGEON_ENTRANCE_AREA = Area(RawSprite(dungeonPath + "entrance.png", 0, 0, 6), None)
  DUNGEON_EASTROOM_AREA = Area(RawSprite(dungeonPath + "eastRoom.png", 0, 0, 6), None)
  DUNGEON_WESTROOM_AREA = Area(RawSprite(dungeonPath + "westRoom.png", 0, 0, 6), None)
  DUNGEON_KEYROOM_AREA = Area(RawSprite(dungeonPath + "keyRoom.png", 0, 0, 6), None)
  DUNGEON_MINIBOSS_AREA = Area(RawSprite(dungeonPath + "miniBoss.png", 0, 0, 6), None)
  DUNGEON_BOSSKEY_AREA = Area(RawSprite(dungeonPath + "bossKey.png", 0, 0, 6), None)
  DUNGEON_BOSSROOM_AREA = Area(RawSprite(dungeonPath + "bossRoom.png", 0, 0, 6), None)






class SoundData():
  move = music(WorldData.path+"Audio/footstep.wav")
  move1 = music(WorldData.path+"Audio/footstep.wav")
  move2 = music(WorldData.path+"Audio/footstep.wav")
  move3 = music(WorldData.path+"Audio/footstep.wav")
  move4 = music(WorldData.path+"Audio/footstep.wav")
  dead_sound = music(WorldData.path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
  dead_sound2 = music(WorldData.path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
  dead_sound3 = music(WorldData.path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
  dead_sound4  = music(WorldData.path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
  dead_sound5 = music(WorldData.path+"Audio/zapsplat_cartoon_rocket_launch_missle.wav")
  hit_sound  = music(WorldData.path+"Audio/Metal_Bang.wav")
  talk_sound = music(WorldData.path+"Audio/Robot_blip.wav")
  background_Music = music(WorldData.path+"Audio/Strange-Zone.wav")
  dungeon_sound = music(WorldData.path+"Audio/Night-Stalker.wav")






class Menu():
  def __init__(self, player, popText = "popText", x=230, y=0):
    self.statusItems = [gui.Label(str(player.hp)), gui.Label(str(player.xp)), gui.Label(str(player.level))]
    self.invItems = []
    for item in player.inv:
      self.invItems.append(gui.Label(item.name))
    self.labelList = []
    self.player = player
    self.text = [gui.Label(popText)]
    self.coords = Coords(x, y)
    self.animationHoldList = []
    self.sprites = [Sprite(WorldData.path +"Menu/menuDefault.png", self, 1),
                    Sprite(WorldData.path + "Menu/menuItem.png", self, 1),
                    Sprite(WorldData.path + "Menu/menuStatus.png", self, 1),
                    Sprite(WorldData.path + "Menu/shopMenu.png", self, 1),
                    Sprite(WorldData.path + "Menu/popUp.png", self, 1)
                    ]
    self.sprite = self.sprites[0]






  def openMenu(self):
    self.updateStats()
    for light in WorldData.CURRENT_AREA.lightSources:
      if light.isOn:
        light.turnOff()
        WorldData.CURRENT_AREA.wasOn.append(light)
    for animation in WorldData.CURRENT_AREA.persistentAnimations:
      if animation not in self.animationHoldList:
        self.animationHoldList.append(animation)
      try:
        animation.stopAnimating()
      except:
        None
    self.sprite.spawnSprite()


  def openPopMenu(self):
    WorldData.text.onKeyType(menuAction)
    self.updateStats()
    self.coords= Coords(368, 196)
    self.switchToPop(self.sprites[4], [self.text])





  def openItemMenu(self):
    self.updateStats()
    newItemLabels = []
    itemNumber = 1
    for label in self.invItems:
      newItemLabels.append(gui.Label("Press " + str(itemNumber) + " to use: " + label.text))
      itemNumber += 1
    self.switchToMenu(self.sprites[1], newItemLabels)
    WorldData.text.onKeyType(inventoryAction)



  def openStatusMenu(self):
    self.updateStats()
    self.switchToMenu(self.sprites[2], self.statusItems)



  def openShopMenu(self, transaction):
    self.updateStats()
    self.switchToMenu(self.sprites[3], transaction.itemLabels)

#Modified to pass startX and Y
  def switchToPop(self, newSprite, labelsToShow = None):
    if labelsToShow == None:
      labelsToShow = self.labelList
    self.updateStats()
    self.sprite.removeSprite()
    self.sprite = newSprite
    self.openMenu()
    try:
      for label in self.labelList:
        removeLabel(label)
    except:
      None
    self.labelList = []
    for label in labelsToShow:
      self.labelList.append(label)
    self.showLabels(self.labelList, startX = 412, startY= 274)
    self.sprite.spawnSprite


  def switchToMenu(self, newSprite, labelsToShow = None):
    if labelsToShow == None:
      labelsToShow = self.labelList
    self.updateStats()
    self.sprite.removeSprite()
    self.sprite = newSprite
    self.openMenu()
    try:
      for label in self.labelList:
        removeLabel(label)
    except:
      None
    self.labelList = []
    for label in labelsToShow:
      self.labelList.append(label)
    self.showLabels(self.labelList)
    self.sprite.spawnSprite



  def closeMenu(self):
    try:
      for label in self.labelList:
        removeLabel(label)
    except:
      None
    self.sprite.removeSprite()
    for light in WorldData.CURRENT_AREA.wasOn:
      light.turnOn()
      WorldData.CURRENT_AREA.wasOn.remove(light)
    for animation in self.animationHoldList:
      animation.animate()
    self.animationHoldList = []
    self.coords= Coords(230, 0) #resets to default menu location



  def updateStats(self):
    self.statusItems = [gui.Label(str(self.player.hp)), gui.Label(str(self.player.xp)), gui.Label(str(self.player.level)),
    gui.Label(str(self.player.atk)), gui.Label(str(self.player.df))]
    self.invItems = []
    for item in self.player.inv:
      self.invItems.append(gui.Label(item.name))




  def showLabels(self, labelsToShow, startX = 700, startY = 171, lineJump = 50):
    #x = 625 - old measurements, might be better for items
    self.updateStats()
    x = startX
    y = startY
    for item in labelsToShow:
      WorldData.display.addOrder(item, 0, x, y)
      y +=lineJump



  def removeMenuLabels (self):
     for item in self.labelList:
         label = item
         removeLabel(label)






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
        return self.tileMap[spot].desc



    def placeStruct(self, struct, spot, desc):
        startx = (spot * WorldData.BITS) % WorldData.backWidth
        starty = ((spot * WorldData.BITS) / WorldData.backWidth) * WorldData.BITS
        #if desc == "tree":
            #printNow("Tree at: " + str(startx) + " " + str(starty))



    def updateMap(self, tiles):
        for spot in range(0, len(tiles)):
            if tiles[spot] == "g":
                self.placeTex(WorldData.grass, spot)
            elif tiles[spot] == "l":
                self.placeTex(WorldData.lavaRock, spot)
            elif tiles[spot] == "s":
                self.placeTex(WorldData.stone, spot)
            elif tiles[spot] == "S":
                self.placeTex(WorldData.stoneWall, spot)
            elif tiles[spot] == "d":
                self.placeTex(WorldData.dirt, spot)
            elif tiles[spot] == "D":
                self.placeTex(WorldData.dirtWall, spot)
            elif tiles[spot] == "w":
                self.placeTex(WorldData.water, spot)
            elif tiles[spot] == "f":
                self.placeTex(WorldData.fence, spot)
            elif tiles[spot] == "L":
                self.placeTex(WorldData.lava, spot)
            elif tiles[spot] == "H":
                self.placeTex(WorldData.hole, spot)
            elif tiles[spot] == ".":
                self.placeTex(WorldData.blank, spot)
            elif tiles[spot] == ",":
                self.placeTex(WorldData.blank, spot)
            elif tiles[spot] == "o":
                self.placeTex(WorldData.door, spot)
            elif tiles[spot] == "h":
                self.placeStruct(makePicture(WorldData.structPath + "house.png"), spot, "house")
            elif tiles[spot] == "t":
                self.placeStruct(makePicture(WorldData.structPath + "tree1.png"), spot, "tree")
            elif tiles[spot] == "c":
                self.placeStruct(WorldData.chest, spot, "chest")



    def isTraversable(self, spot):
        #printNow(spot)
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
    def __init__(self, filepaths, x, y, passable = true, layer = 3):
        self.destructible = false
        self.isPassable = passable
        self.coords = Coords(x, y)
        self.layer = layer
        self.spriteList = filepaths
        self.sprite = Sprite(filepaths[0], self, layer)
        self.isAnimating = false
        try:
          self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], x, y, self.layer)
        except:
          None
        self.sprite.spawnSprite()
        self.type = "doodad"
        WorldData.objectList.append(self)






class Activatable(Doodad):
    def __init__(self, filepaths, x, y, onActivateFunction, layer = 3):
      Doodad.__init(self, filepaths, x, y, layer)



    def activate(self):
      onActivateFunction()






      # Special doodad that heals the user upon activation.
      # Inherits from doodad and calls doodad.__init__()
      # Constructor Parameters:
      #    filepaths        -   sprite filepaths for animations (4 total)
      #    x                -   x coords
      #    y                -   y coords
      #    layer            -   display layer position
      #
      # Members:
      #    animatedSprite   -   ThreeStageAnimationCycle that plays upon usage using spriteList[1-3]
      #    type             -   string type used in targeting

class HealingStation(Doodad):
    def __init__(self, filepaths, x, y, layer = 2):
      passable = false #Change if you want to be passable
      Doodad.__init__(self, filepaths, x, y, passable, layer)
      self.animatedSprite = ThreeStageAnimationCycle(self.spriteList[1], self.spriteList[2], self.spriteList[3], self.coords.x - 32, self.coords.y - 64, .12, 1)
      self.type = "healingStation"
      self.sprite.spawnSprite = self.spawnSprite
      self.sprite.layer = 1
      self.sprite.spawnSprite()


    def spawnSprite(self):
      WorldData.display.place(self.sprite, self.coords.x - 32, self.coords.y - 64)

      # core function. Heals activator and clears out bloody sprites
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






      # Special doodad class used mainly in dungeons. Can be activated by player with user.activateTarget()
      # Constructor Parameters:
      #    filepaths        -   sprite filepaths for animations (4 total)
      #    x                -   x coords
      #    y                -   y coords
      #    layer            -   display layer position
      #    passable         -   default isPassable status
      #    locked           -   default locked status
      #    lockedMessage    -   string displayed on attempted activate() while locked
      #
      # Members:
      #    isLocked         -   bool determining locked status
      #    coords           -   Coords object for placement
      #    sprite           -   object sprite

class Door(Doodad):
    def __init__(self, filepaths, x, y, passable = false, locked = true, lockedMessage = "It's locked!", layer = 3):
      Doodad.__init__(self, filepaths, x, y, passable = false)
      self.lockedMessage = lockedMessage
      self.isLocked = locked
      self.coords = Coords(x, y)
      self.sprite = Sprite(WorldData.path + "ObjectSprites/tempDoorSprite.gif", self, 3)



      # allows a being to pass through the door's coords and removes the sprite
    def open(self):
      self.isPassable = true
      self.sprite.removeSprite()



      # prevents beings from passing through the door's coords and spawns the sprite
    def close(self):
      self.isPassable = false
      self.sprite.spawnSprite()



      # opens the door if it is unlocked, otherwise desplays the door's locked message
    def activate():
      if self.isLocked:
        WorldData.menu.text = gui.Label(lockedMessage)
        WorldData.menu.openPopMenu()
      else:
        self.open()

    def unlock(self):
      self.isLocked = false




      # special animated doodad that emits light within 3 tiles. if is burnable, attacking
      # with an onFire weapon will turnOn the light source. Added to CURRENT_AREA.lightSources
      # Constructor Parameters:
      #    filepaths        -   sprite filepaths for animations (4 total)
      #    x                -   x coords
      #    y                -   y coords
      #    layer            -   display layer position
      #    burnable         -   burnable bool that determines interaction with flaming weapons
      #
      # Members:
      #    isOn             -   boolean light on/off status
      #    type             -   string type for targeting
      #    isBurnable       -   bool burnable status.

class LightSource(Doodad):
    def __init__(self, filepaths, x, y, burnable = false, layer = 3):
        passable = false #Change if you want to be passable
        Doodad.__init__(self, filepaths, x, y, passable, layer)
        self.isOn = false
        self.type = "light"
        self.isBurnable = burnable
        WorldData.lightSources.append(self)



        # turns the light on or off. Activated by a user's activateTarget()
    def activate(self):
        if self.isOn == true:
            self.turnOff()
        else:
            self.turnOn()



        # turns the light on and runs a non-trivial check for nearby beings.
        # Any beings in the area will activate lightenDarken(), lightening their sprites
    def turnOn(self):
        if self.isOn == false:
            self.isOn = true
            self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], self.coords.x, self.coords.y, self.layer)
            self.animatedSprite.animate()
            for being in WorldData.currentBeingList:
                distanceX = abs(being.coords.x - self.coords.x)
                distanceY = abs(being.coords.y - self.coords.y)
                if distanceX <= WorldData.BITS*3 and distanceY <= range:
                    being.lightenDarken()



        # turns the light off and runs a non-trivial check for nearby beings.
        # Any beings in the area will activate lightenDarken(), returning their sprites to pre-light status
    def turnOff(self):
        if self.isOn == true:
            self.isOn = false
            WorldData.animatedSpriteList.remove(self.animatedSprite)
            for being in WorldData.currentBeingList:
                distanceX = abs(being.coords.x - self.coords.x)
                distanceY = abs(being.coords.y - self.coords.y)
                if distanceX <= WorldData.BITS*3 and distanceY <= range:
                    being.lightenDarken()


class DungeonTorch(LightSource):
    def __init__(self, filepaths, x, y, room, burnable = false, layer = 3):
      LightSource.__init__(self, filepaths, x, y, burnable = false, layer = 3)
      self.room = room

    def torchRoomCheck(self):
      for light in self.room.lightSources:
        if isinstance(light, DungeonTorch) and not light.isOn:
          return
      for door in self.room.objectList:
        if isinstance(door, Door):
          door.unlock()
          door.open()


    def turnOn(self):
        if self.isOn == false:
            self.isOn = true
            self.animatedSprite = StationaryAnimatedSprite(self.spriteList[1], self.spriteList[2], self.coords.x, self.coords.y, self.layer)
            self.animatedSprite.animate()
            for being in WorldData.currentBeingList:
                distanceX = abs(being.coords.x - self.coords.x)
                distanceY = abs(being.coords.y - self.coords.y)
                if distanceX <= WorldData.BITS*3 and distanceY <= range:
                    being.lightenDarken()
        self.torchRoomCheck()


      # Class  that handles the buying/selling logic.
      # Runs a check to make sure the buyer has room in the inv before attempting to
      # initiate "buy" mode
      # Constructor Parameters:
      #    buyer              - buyer being
      #    seller             - seller being
      #
      # Members:
      #    buyer              - buyer being
      #    seller             - seller being
      #

class Transaction():
    def __init__(self, buyer, seller):
      self.buyer = buyer
      self.seller = seller
      self.itemLabels = []
      MenuData.transaction = self
      #self.buyingWindowSprite = Sprite()
      #self.sellingWindowSprite = Sprite()
      if seller is WorldData.bot1:
        self.sellingMode()
      else:
        if len(WorldData.bot1.inv) < WorldData.MAX_INVENTORY:
          self.buyingMode()
        else:
          inventoryFull()



          # pops up the selling display and adjusts the keyAction
    def buyingMode(self):
      WorldData.text.onKeyType(buyTransactionKeyAction)
      itemNumber = 1
      for item in self.seller.inv:
        self.itemLabels.append(gui.Label("Press " + str(itemNumber) + " to buy: " + item.name +"-Cost: " + str(item.value*1.5)))
        itemNumber += 1
      WorldData.menu.openShopMenu(self) # Add an attribute menu class at some point, don't use the worldData one
        #Add item to display, add price to display, assign a buying key
        #set buying price to int(item.value * (1.5))

        # completes a transaction. Item is added to buyer inv, currency is removed
        # from buyer, item is removed from seller inv, currency is added to seller
        # runs a check to make sure the buyer has room in the inv



        # pops up the buying display and adjusts the keyAction
    def sellingMode(self):
      #self.buyingWindowSprite.spawnSprite()
      for item in self.seller.inv:
        None
        #Add item to display, selling price, assign selling key
        #set selling price to item.value
        #set keyaction



    def buy(self, item):
      cost = item.value * (1)
      if self.buyer is WorldData.bot1:
        cost = int(item.value * (1.5))
      if WorldData.bot1.wallet.value - cost < 0:
        WorldData.menu.text = gui.Label("Not enough money!")
        WorldData.menu.openPopMenu()
      elif len(self.buyer.inv) >= WorldData.MAX_INVENTORY:
        WorldData.menu.text = gui.Label("Inventory Full!")
        WorldData.menu.openPopMenu()
      else:
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






      # User-exclusive wallet class. Inherits from Wallet and calls Wallet.__init__()
      # Expansions:
      #   coords                - coords for the HUD icon (User only)
      #   sprite                - sprite for the HUD icon (User only)
      #   label                 - currency amount display for HUD (User only)

class UserWallet(Wallet):
    def __init__(self, parental, amount):
      Wallet.__init__(self, parental, amount)
      self.coords = Coords(960, 16)
      self.sprite = Sprite(WorldData.path + r"EffectSprites/walletSprite.gif", self, 1)
      self.label = gui.Label(str(self.value), gui.RIGHT)
      self.sprite.spawnSprite()
      WorldData.display.add(self.label, 1000, 24)



      # updates the currency display to the wallet's current value

    def updateWalletDisplay(self):
      self.sprite.spawnSprite()
      try:
        removeLabel(self.label)
      except:
        None
      self.label = gui.Label(str(self.value), gui.RIGHT)
      WorldData.display.add(self.label, 1000, 24)






    # Container object for obtainable items. Often dropped by enemies.
    # Animates in a new thread.  The object is added to the screen an objectList
    # on instantiation.
    # Constructor Parameters:
    #    itemList             - list of items held by the Lootbag
    #    coords               - coords object holding location
    #    spriteList           - images used for animation
    #    sprite               - current spryte
    #    type                 - used for certain logic checks
    #
    # Members:
    #    isPassable           - defaults to true allowing beings to pass through
    #    contents             - items contained within, to be picked up by beings
    #    coords               - Coords object signifying location
    #    spriteList           - object sprites (2, used for animation)
    #    sprite               - current sprite
    #    type                 - string type used for targeting

class Lootbag():
    def __init__(self, itemList, coords):
        self.isPassable = true
        self.contents = itemList
        self.coords = coords
        self.spriteList = [Sprite(WorldData.path + r"EffectSprites/lootBag.gif", self),
                           Sprite(WorldData.path + r"EffectSprites/lootBag2.gif", self)]
        self.sprite = self.spriteList[0]
        self.type = "lootbag"
        WorldData.objectList.append(self)

        self.spawnSprite()
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))



        # quick access to sprite functions
    def spawnSprite(self):
        WorldData.display.place(self.sprite, self.coords.x, self.coords.y, 1)
    def removeSprite(self):
        WorldData.display.remove(self.sprite)



        # meant for use with thread.start_new_thread.
        # alternates between the object's sprites at half-second intervals.
        # Stops animation once the lootBag is removed from the CURRENT_AREA.objectList
    def threadAnimate(self, x):
        while self in WorldData.objectList:
            time.sleep(.5)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self not in WorldData.objectList:
            self.removeSprite()
            del self







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
          self.power = ListData.weaponStatsList[self.name][0]
          self.originalSprites = ListData.weaponStatsList[self.name][1]
          self.isBurnable = ListData.weaponStatsList[self.name][2]
          self.burningSprites = ListData.weaponStatsList[self.name][3]
          self.range = ListData.weaponStatsList[self.name][4]
          self.coords = Coords(0, 0)
          self.sprites = self.originalSprites
          self.sprite = Sprite(self.sprites[3], self)
          self.onFire = false
          self.value = ListData.weaponStatsList[self.name][5]
          self.displayed = false
          self.currentAnimation = None
          self.animationDelay = .15
          self.animationUp = ThreeStageAnimationCycle(self.sprites[0], self.sprites[4], self.sprites[8], 0, 0, self.animationDelay)
          self.animationDown = ThreeStageAnimationCycle(self.sprites[1], self.sprites[5], self.sprites[9], 0, 0, self.animationDelay)
          self.animationLeft = ThreeStageAnimationCycle(self.sprites[2], self.sprites[6], self.sprites[10], 0, 0, self.animationDelay)
          self.animationRight = ThreeStageAnimationCycle(self.sprites[3], self.sprites[7], self.sprites[11], 0, 0, self.animationDelay)
          self.burningAnimationUp = None
          self.burningAnimationDown = None
          self.burningAnimationLeft = None
          self.burningAnimationRight = None
          if self.isBurnable:
            self.burningAnimationUp = ThreeStageAnimationCycle(self.burningSprites[0], self.burningSprites[4], self.burningSprites[8], 0, 0, self.animationDelay)
            self.burningAnimationDown = ThreeStageAnimationCycle(self.burningSprites[1], self.burningSprites[5], self.burningSprites[9], 0, 0, self.animationDelay)
            self.burningAnimationLeft = ThreeStageAnimationCycle(self.burningSprites[2], self.burningSprites[6], self.burningSprites[10], 0, 0, self.animationDelay)
            self.burningAnimationRight = ThreeStageAnimationCycle(self.burningSprites[3], self.burningSprites[7], self.burningSprites[11], 0, 0, self.animationDelay)



    def use(self, equipper):
      equipper.setWeapon(self)



      # sets the weapon on fire. Starts a new thread for a count down to put out fire

    def burn(self):
        x = None
        self.onFire = true
        thread.start_new_thread(self.threadFireCountdown, (x, ))



      # meant for use with thread.start_new_thread. Sets onFire to false after 15 turns
      # and reverts the weapon's sprites to the original sprites
    def threadFireCountdown(self, x):
        start = WorldData.counter.turn
        finish = start + 15
        while WorldData.counter.turn < finish:
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
        WorldData.display.remove(self.sprite)
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
        self.active = true
        self.inv = []
        self.coords = Coords(xSpawn, ySpawn)
        self.forwardCoords = Coords(self.coords.x + WorldData.BITS, self.coords.y)
        self.unchangedSpritePaths = spritePaths
        self.spritePaths = spritePaths
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.weapon = Weapon(weapName)
        self.wallet = Wallet(self, self.lootValue)
        self.facing = ListData.directionList["down"]
        self.isMoving = false
        self.talkingLines = ["Hello!",
                             "Yes?",
                             "Can I Help you?",
                             "Something weird in the NE Field"]
        self.bloodySprites = []
        self.lightSprites = []
        self.darkSprites = []
        if itemList != None:
            self.inv += itemList
        if not name or not "Boss" in name:
            WorldData.currentBeingList.append(self)



        # use this moveTo when moving beings around
        # Being's coords will be set to the passed x/y

    def stun(self):
        thread.start_new_thread(self.threadStun, (None,))
    def threadStun(self, x):
        start = WorldData.counter.turn
        self.active = false
        finish = start + 3
        while WorldData.counter.turn < finish:
          None
        self.active = true



    def moveTo(self, x, y):
        self.sprite.moveTo(x, y)
        self.coords.x = x
        self.coords.y = y



        # activates an activatable object directly in front
        # Calls the target's activate() function
    def activateTarget(self):
      target = self.getFrontTarget()
      try:
        target.activate(self)
      except:
        target.activate()



        # Updates wallet by amount
        # Wallet will increase by amount if positive, decrease if negative
    def changeWallet(self, amount):
        self.wallet.value += amount
        if self.wallet <= 0:
            self.wallet == 0
        self.wallet.updateWalletDisplay()



        # Adds/removes item to/from inventory list
        # Checks to ensure inventory is not full
    def inventoryAdd(self, item):
        if len(self.inv) < WorldData.MAX_INVENTORY:
          self.inv.append(item)
        else:
          inventoryFull()

    def inventoryRemove(self, item):
        self.inv.remove(item)



        # returns the Being's level
    def getLevel(self):
        return self.level



        # level-up logic. Semi-randomly increases max HP, Atk, df
        # and refreshes hp
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
        if isinstance(self, User):
            self.music = music(WorldData.path+"Audio/level-up.wav")
            self.music.Play()
            WorldData.menu.text = gui.Label("You leveled up!")
            WorldData.menu.openPopMenu()
 



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
        distanceX = self.coords.x - WorldData.bot1.coords.x
        distanceY = self.coords.y - WorldData.bot1.coords.y
        closeProximity = WorldData.BITS * 3
        if self.forwardCoords.x == WorldData.bot1.coords.x and self.forwardCoords.y == WorldData.bot1.coords.y:
            self.meleeAtk()
        elif self.coords.x-WorldData.BITS == WorldData.bot1.coords.x and self.coords.y == WorldData.bot1.coords.y:
            self.faceLeft()
            self.meleeAtk()
        elif self.coords.x+WorldData.BITS == WorldData.bot1.coords.x and self.coords.y == WorldData.bot1.coords.y:
            self.faceRight()
            self.meleeAtk()
        elif self.coords.x == WorldData.bot1.coords.x and self.coords.y+WorldData.BITS == WorldData.bot1.coords.y:
            self.faceDown()
            self.meleeAtk()
        elif self.coords.x == WorldData.bot1.coords.x and self.coords.y-WorldData.BITS == WorldData.bot1.coords.y:
            self.faceUp()
            self.meleeAtk()
        elif abs(self.coords.x - WorldData.bot1.coords.x) < WorldData.BITS and abs(self.coords.y - WorldData.bot1.coords.y) < WorldData.BITS:
            self.moveRandom()
        elif abs(self.coords.x - WorldData.bot1.coords.x) <= closeProximity and abs(self.coords.y - WorldData.bot1.coords.y) <= closeProximity:
            self.moveTowardsPlayer(distanceX, distanceY)
        else:
            self.moveRandom()



        # distanceX and distanceY are compared. The caller will attempt to reduce the distance
        # Depending on which absolute value is greater, the caller will move either vertically
        # or horizontally one space. If decision is made based on distanceX, movement will be horizontal
        # distances can be either positive or negative. Movement seeks to approach zero (e.g., if value is negative,
        # movement is in a positive direction)
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



        # drops all contents of the inv list in a lootbag object on the map
        # The being's wallet is also dropped with any currency
    def dropLoot(self):
        newWallet = Wallet(None, self.wallet.value)
        self.inv.append(newWallet)
        loot = Lootbag(self.inv, self.coords)



        # Actions to be taken on hp <= 0
    def dead(self):
        self.inv.append(self.weapon)
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        WorldData.currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (SoundData.dead_sound,))



        # Handles lighting of sprites. If a valid light object is within the range
        # currently set to * 3, a new set of sprites will be created and applied
        # to simulate lighting.
        # Starts a new thread.
    def lightenDarken(self):
        bright = self.lightWithinRange(WorldData.BITS * 3)
        if self.spritePaths != self.lightSprites and bright:
            self.lightenPixels()
        elif self.spritePaths == self.lightSprites and not bright:
            self.resumePixels()
            deletePath = WorldData.path + "RobotSprites"
            deleteKey = self.name + str(WorldData.currentBeingList.index(self)) + "lightSprite"
            thread.start_new_thread(self.threadDeleteLightSprites, (None,))



        # Helper for lightenDarken(). Separated to allow for early returns. Determines if
        # a valid light source is within the range passed
    def lightWithinRange(self, range):
        for light in WorldData.lightSources:
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



        # Lightens the BeingSprites by creating new image files for lightened sprites and
        # setting the being's spritelist to a list containing the new sprites. Sprites are lightened pixel
        # by pixel.
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
            newPicPath = WorldData.path + "RobotSprites/" + self.name + str(WorldData.currentBeingList.index(self)) + "lightSprite" + str(spriteNum) + ".gif"
            writePictureTo(pic, newPicPath)
            self.lightSprites.append(newPicPath)
            spriteNum += 1
        self.spritePaths = self.lightSprites
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.lightSprites[self.facing], self)
        self.sprite.spawnSprite()



        # Adds an oil effect to the BeingSprites at varied intensity depending
        # on being.hp (higher effect at lower hp).  Achieved by creating new image files
        # and setting the beings spriteList to a list containing the new sprites.
        # Note ** controls are intentionally locked during this logic
    def bloodify(self):
        if isinstance(self, User):
          WorldData.text.onKeyType(blockKeys)
        try:
          spriteNum = 0
          for files in self.bloodySprites:
              os.remove(files)
          self.bloodySprites = []
          for sprites in range(0, len(self.unchangedSpritePaths)):
              pic = makePicture(self.unchangedSpritePaths[sprites])
              for x in range(0, getWidth(pic)-1):
                  for y in range(0, getHeight(pic)-1):
                      p = getPixel(pic, x, y)
                      if getColor(p) != makeColor(0, 0, 0):
                          if random.randint(0, 100) > (self.hp*100)/self.maxHp:
                            setRed(p, (getRed(p)+228)/3)
                            setGreen(p, (getGreen(p)+174)/3)
                            setBlue(p, (getBlue(p)+14)/3)
              newPicPath = WorldData.path + "RobotSprites/" + self.name + str(WorldData.currentBeingList.index(self)) + "bloodySprite" + str(spriteNum) + ".gif"
              writePictureTo(pic, newPicPath)
              self.bloodySprites.append(newPicPath)
              spriteNum += 1
          self.spritePaths = self.bloodySprites
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.bloodySprites[self.facing], self)
          self.sprite.spawnSprite()
        except:
          None
        if isinstance(self, User):
          WorldData.text.onKeyType(keyAction)



        # For use with actions that can target more than one target (e.g., attacks)
        # Returns a list of objects and beings that are directly in front of the being
    def getFrontTargetList(self):
        bigList = WorldData.currentBeingList + WorldData.objectList
        targetList = []
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                targetList.append(target)
        return targetList



        #for use with actions that can only target one target (e.g., talking)
        # Returns one object or being directly in front of the target
    def getFrontTarget(self):
        bigList = WorldData.currentBeingList + WorldData.objectList
        for target in bigList:
            if target.coords.x == self.forwardCoords.x and target.coords.y == self.forwardCoords.y:
                return target



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
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
        self.displayWeapon()
        x = None
        thread.start_new_thread(self.threadHideWeapon, (None,))
        if WorldData.CURRENT_AREA.mapObject.getTileDesc(tileCoordToSpot(coordToTileCoord(self.forwardCoords))) == "lava":# SORRY ABOUT THIS MESS
          self.weapon.burn()
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
        damage = Sprite(WorldData.path + r"EffectSprites/damage.gif", self)
        WorldData.display.add(damage, self.coords.x, self.coords.y)
        thread.start_new_thread(threadRemoveSprite, (.25, damage))



        # For use with meleeAtk and thread.start_new_thread().
    def threadHideWeapon(self, x):
        time.sleep(self.weapon.currentAnimation.secondsBetween*4)
        self.weapon.currentAnimation.stopAnimating()
        self.weapon.displayed = false



        # displays the being's weapon at the being's forward coords
        # note that the weapon sprite is not despawned
    def displayWeapon(self):
        if self.facing == ListData.directionList["up"]:
            self.weapon.displayUp(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == ListData.directionList["down"]:
            self.weapon.displayDown(self.forwardCoords.x, self.forwardCoords.y)
        elif self.facing == ListData.directionList["left"]:
            self.weapon.displayLeft(self.forwardCoords.x, self.forwardCoords.y)
        else:  #right
            self.weapon.displayRight(self.forwardCoords.x, self.forwardCoords.y)



        # picks up any LootBag objects at the coords given
    def pickUpLoot(self, coords):
        for item in WorldData.objectList:
            if item.type == "lootbag" and item.coords.x == coords.x and item.coords.y == coords.y:
                if len(self.inv) + len(item.contents) < WorldData.MAX_INVENTORY:
                  self.inv += item.contents
                  WorldData.objectList.remove(item)
                  try:
                    item.removeSprite()
                  except:
                    None
                  del item
                  for item in self.inv:
                    if isinstance(item, Wallet):
                      self.changeWallet(item.value)
                      self.inv.remove(item)
                      self.music = music(WorldData.path+"Audio/pickup.wav")
                      self.music.Play()
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
        self.isMoving = true
        self.faceUp()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y >= 0 and WorldData.CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.y -= WorldData.BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[7], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            x = None
            thread.start_new_thread(self.threadMoveUp, (x,))
            if self.facing == ListData.directionList["up"]:
              self.forwardCoords.y = self.coords.y - WorldData.BITS - WorldData.BITS/2
              self.forwardCoords.x = self.coords.x
              thread.start_new_thread(music.Play, (SoundData.move,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (SoundData.move,))

    def threadMoveUp(self, x):
        time.sleep(.15)
        self.coords.y -= WorldData.BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[0], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.y%32 != 0:
          self.coords.y = (self.coords.y/32)*32
        self.isMoving = false

    def moveDown(self):
        self.isMoving = true
        self.faceDown()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.y += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.y < WorldData.backHeight and WorldData.CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.y += WorldData.BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[6], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            thread.start_new_thread(self.threadMoveDown, (None,))
            self.sprite.moveTo(self.coords.x, self.coords.y)
            if self.facing == ListData.directionList["down"]:
              self.forwardCoords.y = self.coords.y + WorldData.BITS + WorldData.BITS/2
              self.forwardCoords.x = self.coords.x
              thread.start_new_thread(music.Play, (SoundData.move2,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (SoundData.move2,))

    def threadMoveDown(self, x):
        time.sleep(.15)
        self.coords.y += WorldData.BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[1], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.y%32 != 0:
          self.coords.y = (self.coords.y/32)*32
        self.isMoving = false

    def moveLeft(self):
        self.isMoving = true
        self.faceLeft()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x -= 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x >= 0 and WorldData.CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.x -= WorldData.BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[4], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            thread.start_new_thread(self.threadMoveLeft, (None,))
            if self.facing == ListData.directionList["left"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x - WorldData.BITS - WorldData.BITS/2
              thread.start_new_thread(music.Play, (SoundData.move3,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (SoundData.move3,))

    def threadMoveLeft(self, x):
        time.sleep(.15)
        self.coords.x -= WorldData.BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[2], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.x%32 != 0:
          self.coords.x = (self.coords.x/32)*32
        self.isMoving = false

    def moveRight(self):
        self.isMoving = true
        self.faceRight()
        targetCoord = coordToTileCoord(self.coords)
        targetCoord.x += 1
        targetSpot = tileCoordToSpot(targetCoord)
        if self.coords.x < WorldData.backWidth and WorldData.CURRENT_AREA.isTraversable(self, targetSpot):
            self.coords.x += WorldData.BITS/2
            self.sprite.removeSprite()
            self.sprite = BeingSprite(self.spritePaths[5], self)
            self.sprite.moveTo(self.coords.x, self.coords.y)
            thread.start_new_thread(self.threadMoveRight, (None,))
            if self.facing == ListData.directionList["right"]:
              self.forwardCoords.y = self.coords.y
              self.forwardCoords.x = self.coords.x + WorldData.BITS+ WorldData.BITS/2
              thread.start_new_thread(music.Play, (SoundData.move4,))
        else:
            self.isMoving = false
            thread.start_new_thread(music.Stop, (SoudData.move4,))

    def threadMoveRight(self, x):
        time.sleep(.1)
        self.coords.x += WorldData.BITS/2
        self.sprite.removeSprite()
        self.sprite = BeingSprite(self.spritePaths[3], self)
        self.sprite.moveTo(self.coords.x, self.coords.y)
        self.pickUpLoot(self.coords)
        self.lightenDarken()
        if isinstance(self, User):
            loadAreaCheck(self)
            self.suckUpGiblets()
        if self.coords.x%32 != 0:
          self.coords.x = (self.coords.x/32)*32
        self.isMoving = false



        # changes the being's sprite to one facing the corresponding
        # direction. If a weapon is displayed, it is first hidden.
        # adjusts forwardCoords accordingly

    def faceUp(self):
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != ListData.directionList["up"]:
          self.facing = ListData.directionList["up"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[0], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y - WorldData.BITS
          self.forwardCoords.x = self.coords.x
    def faceDown(self):
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != ListData.directionList["down"]:
          self.facing = ListData.directionList["down"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[1], self)
          self.sprite.spawnSprite()
          self.forwardCoords.y = self.coords.y + WorldData.BITS
          self.forwardCoords.x = self.coords.x
    def faceLeft(self):
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != ListData.directionList["left"]:
          self.facing = ListData.directionList["left"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[2], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x - WorldData.BITS
          self.forwardCoords.y = self.coords.y
    def faceRight(self):
        if self.weapon.displayed == true:
          self.weapon.hide()
        if self.facing != ListData.directionList["right"]:
          self.facing = ListData.directionList["right"]
          self.sprite.removeSprite()
          self.sprite = BeingSprite(self.spritePaths[3], self)
          self.sprite.spawnSprite()
          self.forwardCoords.x = self.coords.x + WorldData.BITS
          self.forwardCoords.y = self.coords.y






#Hitbox class passes hits to parent class
class Hitbox(Being):
  def __init__(self, parent, xSpawn, ySpawn, itemList = None):
    name = parent.getName() + "Hitbox"
    Being.__init__(self, name, None, SpriteData.emptySpritePaths, xSpawn, ySpawn, itemList = None)
    self.parent = parent



    #if hitbox hit parent
  def changeHp(self, amount):
    self.parent.changeHp(amount)



  #override thinking so it doesn't do anything
  def simpleHostileAI(self):
    return



#hitbox helper class
def makeHitbox(parent, width, height):
    startx = parent.coords.x
    starty = parent.coords.y
    boxes = []
    for x in range(0, width):
        for y in range(0, height):
            if x == 0 and y == 0:
                continue
            spawnx = startx + (x*WorldData.BITS)
            spawny = starty + (y*WorldData.BITS)
            tempBox = Hitbox(parent, spawnx, spawny)
            boxes.append(tempBox)
    return boxes






        # Custom being instance for friendlies. Slightly different giblets/giblet logic
class Friendly(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [RawSprite(WorldData.path + r"RobotSprites/friendlyBigGib1.gif", self.coords.x, self.coords.y),
                              RawSprite(WorldData.path + r"RobotSprites/friendlyBigGib2.gif", self.coords.x, self.coords.y),
                              RawSprite(WorldData.path + r"RobotSprites/friendlyHead.gif", self.coords.x, self.coords.y),
                              ]



    def gibSpawn(self, gibSprite, x, y):
        WorldData.gibList.append(gibSprite.sprite)
        WorldData.display.add(gibSprite.sprite, x, y)



    def giblets(self):
        x = random.randint(self.coords.x - WorldData.BITS, self.coords.x + WorldData.BITS)
        y = random.randint(self.coords.y - WorldData.BITS, self.coords.y + WorldData.BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(WorldData.path + r"RobotSprites/friendlyBigGib1.gif", WorldData.path + r"RobotSprites/friendlyBigGib2.gif", x, y)
          animatedGib.animate()
        possibilities = random.randint(0, 3)
        if possibilities == 3:
          for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - WorldData.BITS, self.coords.x + WorldData.BITS)
            y = random.randint(self.coords.y - WorldData.BITS, self.coords.y + WorldData.BITS)
            if isTraversable(x, y):
              self.gibSpawn(self.gibSpriteList[2], x, y)



        # Actions to be taken on hp <= 0
    def dead(self):
        self.giblets()
        self.inventoryAdd(self.weapon)
        self.dropLoot()
        self.sprite.removeSprite()
        for files in self.bloodySprites:
          try:
            os.remove(files)
          except:
            None
        WorldData.currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (SoundData.dead_sound2,))






        # Custom being instance for friendlies. Slightly different giblets/giblet logic
class ShopKeeper(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn, itemList = None)
        self.gibSpriteList = [Sprite(WorldData.path + r"RobotSprites/shopKeeperGib1.gif", self),
                              Sprite(WorldData.path + r"RobotSprites/shopKeeperGib2.gif", self)
                              ]



    def activate(self):
      transaction = Transaction(WorldData.bot1, self)
      transaction.sellingMode()



        # Displays gore effects
    def giblets(self):
        x = random.randint(self.coords.x - WorldData.BITS, self.coords.x + WorldData.BITS)
        y = random.randint(self.coords.y - WorldData.BITS, self.coords.y + WorldData.BITS)
        if isTraversable(x, y):
          animatedGib = AnimatedGiblets(WorldData.path + r"RobotSprites/shopKeeperGib1.gif", WorldData.path + r"RobotSprites/shopKeeperGib2.gif", x, y)
          animatedGib.animate()



    def dead(self):
        self.giblets()
        self.inventoryAdd(self.weapon)
        self.dropLoot();
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        WorldData.currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (SoundData.dead_sound4,))






    # Custom being for enemies. Slightly different logic for giblets and loot

class Enemy(Being):
    def __init__(self, name, weapName, spritePaths, xSpawn, ySpawn, level):
        Being.__init__(self, name, weapName, spritePaths, xSpawn, ySpawn)
        for num in range(0, level):
            self.levelUp()
        self.gibSpriteList = [Sprite(WorldData.path + r"RobotSprites/enemyArmGib.gif", self),
                              Sprite(WorldData.path + r"RobotSprites/enemyLegGib.gif", self),
                              Sprite(WorldData.path + r"RobotSprites/enemyLegGib2.gif", self),
                              Sprite(WorldData.path + r"RobotSprites/enemyBodyGib.gif", self),
                              Sprite(WorldData.path + r"RobotSprites/enemyHeadGib.gif", self),
                              ]
        self.hostile = true



        # Drops a Lootbag instance with a random inv item
    def dropLoot(self):
        items = []
        items.append(self.randomInvItem())
        items.append(self.wallet)
        loot = Lootbag(items, self.coords)



        # adds a sprite to the gibList and display at the pixel coords given
    def gibSpawn(self, gibSprite, x, y):
        WorldData.gibList.append(gibSprite)
        WorldData.display.add(gibSprite, x, y)



        # Gore effect for enemies
    def giblets(self):
        gibIndex = 0
        for i in range(0, random.randint(0, len(self.gibSpriteList))):
            x = random.randint(self.coords.x - WorldData.BITS, self.coords.x + WorldData.BITS)
            y = random.randint(self.coords.y - WorldData.BITS, self.coords.y + WorldData.BITS)
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
        WorldData.currentBeingList.remove(self)
        del self
        thread.start_new_thread(music.Play, (SoundData.dead_sound3,))



        # returns a random item from the inv list
    def randomInvItem(self):
        possibilities = len(self.inv)
        if possibilities>0:
            itemIndex = random.randint(0, possibilities-1)
            return self.inv[itemIndex]






  # The following cluster acts as shortcuts to create higher level enemies with better weapons
class Threat2Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Rock", SpriteData.greenEnemySpritePaths, xSpawn, ySpawn, 10)

class Threat3Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Rock", SpriteData.yellowEnemySpritePaths, xSpawn, ySpawn, 20)

class Threat4Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Sword", SpriteData.purpleEnemySpritePaths, xSpawn, ySpawn, 30)

class Threat5Enemy(Enemy):
    def __init__(self, name, xSpawn, ySpawn):
      Enemy.__init__(self, name, "Botsmasher", SpriteData.redEnemySpritePaths, xSpawn, ySpawn, 50)


#Bomb class dropped by the first boss targeted at the players location
class Bomb(Enemy):
    def __init__(self, target):
        Enemy.__init__(self, "Bomb", "Rock", SpriteData.bombSpritePaths, target.x, target.y, 20)
        self.coords = target
        self.tick = 0
        self.hostile = true
        self.sprite = BeingSprite(self.spritePaths[self.tick], self)
        self.damage = -10 #change this to modify bomb damage
        self.sprite.spawnSprite()

    def simpleHostileAI(self):
        #printNow("Tick")
        if self.tick == 3:
            self.dead()
        if self.tick == 2:
            #printNow("Boom")
            thread.start_new_thread(music.Play, (SoundData.dead_sound,))
            for being in WorldData.CURRENT_AREA.beingList:
                if being is not self and being.coords.x == self.coords.x and being.coords.y == self.coords.y:
                    being.changeHp(self.damage)
        self.sprite = BeingSprite(self.spritePaths[self.tick], self)
        self.sprite.spawnSprite()
        self.tick += 1

        # Actions to be taken on hp <= 0
    def dead(self):
        self.sprite.removeSprite()
        for files in self.bloodySprites:
            os.remove(files)
        WorldData.currentBeingList.remove(self)
        del self

def dropBomb(coords):
    coords.printCoords()
    return Bomb(Coords(coords.x, coords.y))

#Main Class for the first Boss
class Boss1(Enemy):
    def __init__(self, area):
        Enemy.__init__(self, "DragonHeadBoss", "Rock", SpriteData.bossDragonHeadSpritePaths, 14*WorldData.BITS, 4*WorldData.BITS, 50)
        self.idle = 4 #drop bombs every X turns
        self.area = area
        self.leftHand = None
        self.rightHand = None
        self.hitBoxes = makeHitbox(self, 4, 4)
        for box in self.hitBoxes:
            self.area.beingList.append(box)



    def changeHp(self, amount):
        #if healing heal
        if amount >= 0:
            self.hp += int(amount)
            return
        #can only take damage if both hands are stunned
        try:
          if (self.leftHand == None and self.rightHand == None) or (self.leftHand.stunned and self.rightHand.stunned):
              self.hp = int(self.hp + amount)
              if self.hp > self.maxHp:
                  self.hp = self.maxHp
              elif self.hp <= 0:
                  self.dead()
        except:
          None



    def simpleHostileAI(self):
        #printNow("Boss thinking")
        if not WorldData.counter.turn % self.idle:
            #printNow("Dropping Bomb")
            dropBomb(WorldData.bot1.coords)
            #DoNothingSucessfully
        if WorldData.counter.turn % 10 == 0:
          self.leftHand = BossArm(320, 256, true, self)
          self.rightHand = BossArm(672, 256, false, self)

        return


class BossArm(Enemy):
    def __init__(self, xSpawn, ySpawn, isLeft, parental):
      Enemy.__init__(self, "Hand", None, SpriteData.bossLeftHandSpritePaths, xSpawn, ySpawn, 0) #dummy values, do not rely on
      self.sprite = None
      self.maxHp = 50
      self.hp = 50
      self.isLeft = false
      self.isRight = false
      self.hostile = true
      self.active = true
      self.parental = parental
      self.stunned = false
      self.coords = Coords(xSpawn, ySpawn)
      WorldData.currentBeingList.append(self)
      if isLeft:
        self.isLeft = true
        self.sprite = Sprite(SpriteData.bossLeftHandSpritePaths[0], self)
        self.parental.leftHand = true
      else:
        self.isRight = true
        self.sprite = Sprite(SpriteData.bossRightHandSpritePaths[0], self)
      self.sprite.spawnSprite()

    def giblets(self):
      None
    def dropLoot(self):
      None
    def randomInvItem(self):
      None


    def stun(self):
        thread.start_new_thread(self.threadStun, (None,))
    def threadStun(self, x):
        start = WorldData.counter.turn
        self.active = false
        self.stunned = true
        finish = start + 5
        while WorldData.counter.turn < finish:
          None
        self.active = true

    def slideRight(self, targetXBig):
        time.sleep(.005)
        self.coords.x += 1
        self.forwardCoords.x += 1
        WorldData.display.add(self.sprite, self.coords.x, self.coords.y)
        try:
          for being in WorldData.CURRENT_AREA.beingList:
            if isinstance(being, User) and being.coords.x == self.coords.x and (being.coords.y == self.coords.y or being.coords.y == self.coords.y + 32):
              being.changeHp(-30)
        except:
          None
        if self.coords.x < targetXBig:
          thread.start_new_thread(self.slideRight, (targetXBig,))

    def slideLeft(self, targetXSmall):
        time.sleep(.005)
        self.coords.x -= 1
        self.forwardCoords.x -= 1
        WorldData.display.add(self.sprite, self.coords.x, self.coords.y)
        for being in WorldData.CURRENT_AREA.beingList:
            if isinstance(being, User) and being.coords.x == self.coords.x and (being.coords.y == self.coords.y or being.coords.y == self.coords.y + 32):
              being.changeHp(-30)
        if self.coords.x > targetXSmall:
          thread.start_new_thread(self.slideLeft, (targetXSmall,))

    def moveLeft(self):
      slideLeft(self, self.coords.x - 32)


    def moveRight(self):
      slideRight(self, self.coords.x + 32)
    def lightenDarken(self):
      None
    def lightWithinRange(self, range):
        None


    def threadDeleteLightSprites(self, x):
        None


    def resumePixels(self):
        None



    def lightenPixels(self):
        None
        self.sprite.spawnSprite()



    def bloodify(self):
        None


    def getFrontTargetList(self):
        None


    def getFrontTarget(self):
        None



    def meleeAtk(self):
        None

    def simpleHostileAI(self):
        if self.isLeft:
          if self.coords.x < 480:
            self.moveRight()
          else:
            self.despawn()
        else:
          if self.coords.x > 512:
            self.moveLeft()
          else:
            self.despawn()


    def despawn(self):
        self.sprite.removeSprite()
        try:
          for files in self.bloodySprites:
            os.remove(files)
        except:
          None
        if self.isLeft:
          self.parental.leftHand = None
        else:
          self.parental.rightHand = None
        WorldData.currentBeingList.remove(self)


    def dead(self):
        self.sprite.removeSprite()
        try:
          for files in self.bloodySprites:
            os.remove(files)
        except:
          None
        if self.isLeft:
          self.parental.leftHand = None
        else:
          self.parental.rightHand = None
        WorldData.currentBeingList.remove(self)
        thread.start_new_thread(music.Play, (SoundData.dead_sound,))


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
        WorldData.gibList.append(self.spriteList[0])



        #activates animation
    def animate(self):
        x = None
        thread.start_new_thread(self.threadAnimate, (x,))



        # sprite addition and removal to and from display
    def spawnSprite(self):
        WorldData.display.place(self.sprite, self.coords.x, self.coords.y, 5)
    def removeSprite(self):
        WorldData.display.remove(self.sprite)



    def threadAnimate(self, container):
        while self.spriteList[0] in WorldData.gibList:
            time.sleep(random.randint(0, 2)/10.0)
            self.removeSprite()
            if self.sprite == self.spriteList[0]:
                self.sprite = self.spriteList[1]
                self.spawnSprite()
            else:
                self.sprite = self.spriteList[0]
                self.spawnSprite()
        if self.spriteList[0] not in WorldData.gibList:
            self.removeSprite()
            del self






    # In development class for potions
class Potion():
    def __init__(self):
      self.parental = WorldData.bot1
      self.name = "Potion"
      self.restoreValue = 10
      self.value = 20



    def use(self, user):
      user.changeHp(self.restoreValue)
      user.inv.remove(self)






        # Singleton class for player's HP Bar
        # Parental        - Owner (meant to be player)
        # Sprites         - Sprites for visual "levels"
        # coords          - sprite coords
class HpBar():
    def __init__(self, parental):
      self.sprites = [Sprite(WorldData.path + "/EffectSprites/hpBarSpriteEmpty.gif", self, 1), Sprite(WorldData.path + "/EffectSprites/hpBarSpriteCritical.gif", self, 1),
                      Sprite(WorldData.path + "/EffectSprites/hpBarSpriteLow.gif", self, 1), Sprite(WorldData.path + "/EffectSprites/hpBarSpriteHalf.gif", self, 1),
                      Sprite(WorldData.path + "/EffectSprites/hpBarSpriteHigh.gif", self, 1), Sprite(WorldData.path + "/EffectSprites/hpBarSpriteMost.gif", self, 1),
                      Sprite(WorldData.path + "/EffectSprites/hpBarSpriteFull.gif", self, 1)]
      self.sprite = self.sprites[6]
      self.parental = parental
      self.coords = Coords(0, 0)
      self.sprite.spawnSprite()



      # Updates the bar's sprite based on owner HP levels
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
        self.specialSprites1 = [ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv1Stun1Up.gif", WorldData.path + "EffectSprites/lv1Stun2Up.gif", WorldData.path + "EffectSprites/lv1Stun3Up.gif", self.coords.x, self.coords.y-32, .1),
                                ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv1Stun1Down.gif", WorldData.path + "EffectSprites/lv1Stun2Down.gif", WorldData.path + "EffectSprites/lv1Stun3Down.gif", self.coords.x, self.coords.y+32, .1),
                                ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv1Stun1Left.gif", WorldData.path + "EffectSprites/lv1Stun2Left.gif", WorldData.path + "EffectSprites/lv1Stun3Left.gif", self.coords.x, self.coords.x-32, .1),
                                ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv1Stun1Right.gif", WorldData.path + "EffectSprites/lv1Stun2Right.gif", WorldData.path + "EffectSprites/lv1Stun3Right.gif", self.coords.x, self.coords.x+32, .1),]
        self.specialSprite2 = ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv2Stun1.gif", WorldData.path + "EffectSprites/lv2Stun2.gif", WorldData.path + "EffectSprites/lv2Stun3.gif", self.coords.x, self.coords.x+32, .1)
        self.specialSprite3 = ThreeStageAnimationCycle(WorldData.path + "EffectSprites/lv3Stun1.gif", WorldData.path + "EffectSprites/lv3Stun2.gif", WorldData.path + "EffectSprites/lv3Stun3.gif", self.coords.x, self.coords.x+32, .1)
        self.area = WorldData.CURRENT_AREA
        self.hpBar = HpBar(self)
        self.wallet = UserWallet(self, 0)
        self.sprite.spawnSprite()
        self.held = false



        # for use with inventory. Will be altered.  All usable items
        # in the future will have a use() method that will be called here.
    def useItem(self, item):
      item.use(self)



        # Initiates bot1's special attack. The attack has three levels, based
        # on bot1's atk value. Level 1 stuns the target(s) directly ahead for 3 turns.
        # Level 2 stuns targets that are exactly 2 tiles away for 3 turns
        # Level 3 stuns and damages all targets within 2 tiles
        #
        # bot1's Hp will be drained 25% (rounded up)
        # One of the three stun's will be called
    def specialAtk(self):
      if self.atk <= 45:
        self.stunLevel1()
      elif self.atk <= 85:
        self.stunLevel2()
      else:
        self.stunLevel3()



        # Level 1 stun logic.
        # Handles targeting.
        # The target directly ahead of bot1 will be stunned
        # for 3 turns and hostile thereafter
    def stunLevel1(self):
      self.changeHp((self.hp/(-4.0)))
      self.stunLv1Animate()
      self.music = music(WorldData.path+"Audio/zap.wav")
      self.music.Play()
      for target in self.getFrontTargetList():
        if isinstance(target, Being) or isinstance(target, Enemy):
          target.hostile = true
          target.stun()
    def stunLv1Animate(self):
      if self.facing == ListData.directionList["up"]:
        self.specialSprites1[0].coords.x = self.coords.x
        self.specialSprites1[0].coords.y = self.coords.y - 32
        self.specialSprites1[0].animateOnce()
      elif self.facing == ListData.directionList["down"]:
        self.specialSprites1[1].coords.x = self.coords.x
        self.specialSprites1[1].coords.y = self.coords.y + 32
        self.specialSprites1[1].animateOnce()
      elif self.facing == ListData.directionList["left"]:
        self.specialSprites1[2].coords.x = self.coords.x - 32
        self.specialSprites1[2].coords.y = self.coords.y
        self.specialSprites1[2].animateOnce()
      else:
        self.specialSprites1[3].coords.x = self.coords.x + 32
        self.specialSprites1[3].coords.y = self.coords.y
        self.specialSprites1[3].animateOnce()



        # Level 2 stun logic.
        # Handles targeting.
        # Targets exactly 2 tiles away will be stunned in
        # addition to the target directly in front
        # for 3 turns and hostile thereafter
        # calls stunLevel1
        # hp is reduced through the stunLevel1 call
    def stunLevel2(self):
      self.music = music(WorldData.path+"Audio/zap.wav")
      self.music.Play()
      self.stunLevel1()
      self.specialSprite2.coords.x = self.coords.x - 64
      self.specialSprite2.coords.y = self.coords.y - 64
      self.specialSprite2.animateOnce()
      for being in WorldData.CURRENT_AREA.beingList:
        if self.stun2InRange(being) and being is not self:
          being.hostile = true
          being.stun()



        # Returns a boolean if the being passed
        # is exactly 2 tiles (64pixels) away.
        # For use with stunLevel2()
    def stun2InRange(self, being):
      distanceX = abs(self.coords.x - being.coords.x)
      distanceY = abs(self.coords.y - being.coords.y)
      return (distanceX + distanceY > 32 and distanceX + distanceY <= 64)



        # Level 3 stun logic.
        # Handles targeting.
        # Targets within 2 tiles will be stunned for 3 turns,
        # hostile after, and will take damage scaled with bot1's atk
    def stunLevel3(self, damage = (-10)):
      self.music = music(WorldData.path+"Audio/zap.wav")
      self.music.Play()
      self.changeHp((self.hp/(-4.0)))
      self.specialSprite3.coords.x = self.coords.x - 64
      self.specialSprite3.coords.y = self.coords.y - 64
      self.specialSprite3.animateOnce()
      damage = self.atk/(-4)
      beingsToDamage = []
      for being in WorldData.CURRENT_AREA.beingList:
        if self.stun3InRange(being) and being is not self:
          beingsToDamage.append(being)
      for being in beingsToDamage:
        being.hostile = true
        being.stun()
        being.changeHp(damage)
      beingsToDamage = []



        # Returns a boolean if the being passed
        # is exactly 2 tiles (64pixels) away.
        # for use with stunLevel3()
    def stun3InRange(self, being):
      distanceX = abs(self.coords.x - being.coords.x)
      distanceY = abs(self.coords.y - being.coords.y)
      return distanceX + distanceY <= 64



      # Updates the user's wallet by the amount given,
      # positive or negative.  calls wallet.updateWalletDisplay()
    def changeWallet(self, amount):
      Being.changeWallet(self, amount)
      self.wallet.updateWalletDisplay()



      # Combination cleanup/money creation.
      # Too many giblets on screen causes issues, so
      # This was implemented to give the user a reason to cleanup
      # Removes giblets within WorldData.BITS pixels of the player
      # and converts them to money for the player's wallet
    def suckUpGiblets(self):
      for gib in WorldData.CURRENT_AREA.gibList:
        distanceX = abs(self.coords.x - gib.parental.coords.x)
        distanceY = abs(self.coords.y - gib.parental.coords.y)
        if distanceX + distanceY<= WorldData.BITS:
          gib.removeSprite()
          WorldData.CURRENT_AREA.gibList.remove(gib)
          if gib.fileName == WorldData.path + r"RobotSprites/friendlyHead.gif" or gib.fileName == WorldData.path + r"RobotSprites/enemyHeadGib.gif":
            self.changeWallet(5)
          else:
            self.changeWallet(1)
          break



      # Player doesn't currently drop gibs
    def giblets():
        None



               # EQUIPMENT CLUSTER###
        # The following 6 functions handle equipping items
        # to  specific parts of the body.  Atk and Df stats
        # are adjusted accordingly.  The equipped item must
        # correlate to one of the itemLists

    def setWeapon(self, weapon):
        self.inventoryAdd(self.weapon)
        self.atk -= ListData.weaponStatsList[self.weapon.name][0]
        if weapon in self.inv:
          self.inventoryRemove(weapon)
        self.weapon = weapon
        self.atk += ListData.weaponStatsList[self.weapon.name][0]


    def setHelm(self, helm):
        if self.helm != "Hair":
            self.inventoryAdd(self.helm)
        self.df -= ListData.helmStatsList(self.helm)
        if helm in self.inv:
          self.inventoryRemove(helm)
        self.helm = helm
        self.df += ListData.helmStatsList(self.helm)


    def setChest(self, chest):
        if self.chest != "BDaySuit":
            self.inventoryAdd(self.chest)
        self.df -= chestStatsList(self.chest)
        if chest in self.inv:
          self.inventoryRemove(chest)
        self.chest = chest
        self.df += chestStatsList(self.chest)


    def setLegs(self, legs):
        if self.legs != "Shame":
            self.inventoryAdd(self.legs)
        self.df -= legsStatsList(self.legs)
        if legs in self.inv:
          self.inventoryRemove(legs)
        self.legs = legs
        self.df += legsStatsList(self.legs)


    def setBoots(self, boots):
        if self.boots != "Toes":
            self.inventoryAdd(self.boots)
        self.df -= bootsStatsList(self.boots)
        if boots in self.inv:
          self.inventoryRemove(boots)
        self.boots = boots
        self.df += bootsStatsList(self.boots)


    def setGloves(self, gloves):
        if self.gloves != "Digits":
            self.inventoryAdd(self.gloves)
        self.df -= glovesStatsList(self.gloves)
        if gloves in self.inv:
          self.inventoryRemove(gloves)
        self.gloves = gloves
        self.df += glovesStatsList(self.gloves)



            # action - attempts to steal an item from a target
            # Being.  If the attempt fails, the Being turns hostile
            # Attempt will not initiate if the inventory is full

    def steal(self, target):
      if len(self.inv) < WorldData.MAX_INVENTORY:
        possibilities = len(target.inv)
        if possibilities>0:
            if random.randint(0, 10)%10 == 0:
                item = target.randomInvItem()
                target.inv.remove(item)
                self.inv.append(item)
                WorldData.menu.text = gui.Label("You stole "  + item.name)
                WorldData.menu.openPopMenu()
            else:
                WorldData.menu.text = gui.Label("You messed up now!")
                WorldData.menu.openPopMenu()
                target.hostile = true
        else:
            WorldData.menu.text = gui.Label("Nothing to steal!")
            WorldData.menu.openPopMenu()
      else:
            inventoryFull()



            # Talks to the being directly in front
    def talk(self):
        thread.start_new_thread(music.Play, (SoundData.talk_sound,))
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
        WorldData.menu.text = speech
        WorldData.menu.openPopMenu()
        delayRemoveObject(speech, 2)



        # Logic for hp == 0.  The player will drop all loot/money
        # and respawn at lv 0 with default eqiupment
    def dead(self):
        self.sprite.removeSprite()
        self.dropLoot()
        WorldData.currentBeingList.remove(self)
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
        self.__init__("bot1", "Stick", SpriteData.userSpritePaths, self.area)
        thread.start_new_thread(music.Play, (SoundData.dead_sound5,))





class MenuData():
    transaction = None
    popupCoords = None







        ####################
        #                  #
        #    FUNCTIONS     #
        #                  #
        ####################



# Removes the passed object from the display

def removeLabel(label):
    WorldData.display.remove(label)



# All actions that depend on the turn counter go here. All actions/functions within
# will occur with the passing of each turn (e.g., attack, player-directed movement)

def turnPass():
    WorldData.counter.turn += 1
    if  WorldData.CURRENT_AREA != AreaData.TOWN_AREA and len(WorldData.currentBeingList)< WorldData.MAX_BEINGS:
      if WorldData.counter.turn % 100 == 0 and bot1.level > 40:
        spawnThreat5()
      elif WorldData.counter.turn % 80 == 0 and bot1.level >= 28:
        spawnThreat4()
      elif WorldData.counter.turn % 40 == 0 and bot1.level >= 19:
        if bot1.level >= 19:
          spawnThreat3()
        elif bot1.level >= 10:
          spawnThreat2()
      elif WorldData.counter.turn % 20 == 0:
        spawnEnemy()
    if WorldData.CURRENT_AREA == AreaData.TOWN_AREA:
      if WorldData.counter.turn < 100:
        None
      elif WorldData.counter.turn < 200 and WorldData.counter.turn % 25 == 0:
        WorldData.shopKeeper.inv = [Weapon("Rock"), Potion(), Potion(), Potion()]
      elif WorldData.counter.turn < 500 and WorldData.counter.turn % 25 == 0:
        WorldData.shopKeeper.inv = [Weapon("Rock"), Weapon("Sword"), Potion(), Potion()]
      elif WorldData.counter.turn % 100:
        WorldData.shopKeeper.inv = [Weapon("Rock"), Weapon("Sword"), Weapon("Botsmasher"), Potion()]

    for person in WorldData.currentBeingList:
      if person.active: #separated to leave room for friendly AIs in the future
        if person.hostile:
            person.simpleHostileAI()
    if WorldData.bot1.hp <= 0:
        WorldData.bot1.coords.x = 0
        WorldData.bot1.coords.y = 0
        WorldData.bot1.sprite.spawnSprite()
    clearBadSprites()



def inventoryFull():
    WorldData.menu.text = gui.Label("Not enough inventory space!")
    WorldData.menu.openPopMenu()


# slides an object to the right one pixel at a time until the object's coords.x == targetXBig.
# parameters:
# object        - object to be moved (must have a sprite)
# targetXBig    - x coord target (must be greater than object.coords.x)

def slideRight(toBeMoved, targetXBig):
    time.sleep(.005)
    toBeMoved.coords.x += 1
    toBeMoved.forwardCoords.x += 1
    WorldData.display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.x < targetXBig:
        thread.start_new_thread(slideRight, (toBeMoved, targetXBig))

def slideLeft(toBeMoved, targetXSmall):
    time.sleep(.005)
    toBeMoved.coords.x -= 1
    toBeMoved.forwardCoords.x -= 1
    WorldData.display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.x > targetXSmall:
        thread.start_new_thread(slideLeft, (toBeMoved, targetXSmall))


# Slide-down logic identical to the above, but for vertical sliding
def slideSpriteDown(toBeMoved, targetYBig):
    time.sleep(.005)
    toBeMoved.coords.y += 1
    WorldData.display.add(toBeMoved.sprite, toBeMoved.coords.x, toBeMoved.coords.y)
    if toBeMoved.coords.y < targetYBig:
        thread.start_new_thread(slideSpriteDown, (toBeMoved, targetYBig))



# Checks player coords to determine if a load is necessary.
# may call loadNewArea
# double calls for garbage sprite cleanup

def loadAreaCheck(player):
    maxAceptableWidth = 960
    maxAceptableHeight = 512
    if WorldData.CURRENT_AREA.otherAreas:
        currCoord = coordToTileCoord(WorldData.bot1.coords)
        currSpot = tileCoordToSpot(currCoord)
        if WorldData.currentMap.getTileDesc(currSpot) == "hole":
            #enter the dungeon!
            coordY = (WorldData.HEIGHT_TILES/2) * WorldData.BITS
            coordX = (WorldData.WIDTH_TILES/2) * WorldData.BITS
            WorldData.bot1.coords.y = coordY
            WorldData.bot1.coords.x = coordX
            loadNewArea(WorldData.CURRENT_AREA.otherAreas[0])
            WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)
        elif WorldData.currentMap.getTileDesc(currSpot) == "door":
            coordY = (WorldData.HEIGHT_TILES/2) * WorldData.BITS
            coordX = (WorldData.WIDTH_TILES/2) * WorldData.BITS
            WorldData.bot1.coords.y = coordY
            WorldData.bot1.coords.x = coordX
            loadNewArea(WorldData.CURRENT_AREA.otherAreas[0])
            WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)
    if player.coords.y <= 0:
        WorldData.bot1.coords.y = maxAceptableHeight
        loadNewArea(WorldData.CURRENT_AREA.northArea)
        WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)

    elif player.coords.y > maxAceptableHeight:
        WorldData.bot1.coords.y = WorldData.BITS #place user one in from the edge
        loadNewArea(WorldData.CURRENT_AREA.southArea)
        WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)
    elif player.coords.x <= 0:
        WorldData.bot1.coords.x = maxAceptableWidth
        loadNewArea(WorldData.CURRENT_AREA.westArea)
        WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)
    elif player.coords.x > maxAceptableWidth:
        WorldData.bot1.coords.x = WorldData.BITS #place user one in from the edge
        loadNewArea(WorldData.CURRENT_AREA.eastArea)
        WorldData.CURRENT_AREA.spawnCoords = Coords(WorldData.bot1.coords.x, WorldData.bot1.coords.y)



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
      toSpawn = Enemy(None, "Stick", SpriteData.blueEnemySpritePaths, random.randint(0, 10)*32, random.randint(0, 10)*32, 1)
    if toSpawn.name == None:
      toSpawn.name = ("EnemyBorn" + str(WorldData.counter.turn)+str(len(WorldData.CURRENT_AREA.beingList)))
    if len(WorldData.CURRENT_AREA.beingList) < WorldData.MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()



      # Quick spawn commands for higher level enemies
def spawnThreat2():
    toSpawn = Threat2Enemy("EnemyBorn" + str(WorldData.counter.turn)+str(len(WorldData.CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(WorldData.CURRENT_AREA.beingList) < WorldData.MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat3():
    toSpawn = Threat3Enemy("EnemyBorn" + str(WorldData.counter.turn)+str(len(WorldData.CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(WorldData.CURRENT_AREA.beingList) < WorldData.MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat4():
    toSpawn = Threat4Enemy("EnemyBorn" + str(WorldData.counter.turn)+str(len(WorldData.CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(WorldData.CURRENT_AREA.beingList) < WorldData.MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()
def spawnThreat5():
    toSpawn = Threat5Enemy("EnemyBorn" + str(WorldData.counter.turn)+str(len(WorldData.CURRENT_AREA.beingList)), random.randint(0, 10)*32, random.randint(0, 10)*32)
    if len(WorldData.CURRENT_AREA.beingList) < WorldData.MAX_BEINGS:
      while not isTraversable(toSpawn.coords.x, toSpawn.coords.y):
          toSpawn.coords.x = random.randint(0, 10)*32
          toSpawn.coords.y =  random.randint(0, 10)*32
      toSpawn.sprite.spawnSprite()



# Spawns a friendly with the given parameters.  Default is green friendly with stick at random location.

def spawnFriendly(name = None, weap = "Stick", spritePaths = SpriteData.friendlyGreenSpritePaths,  x = random.randint(0, 10)*32, y =  random.randint(0, 10)*32):
    if name == None:
      name = ("FriendlyBorn" + str(WorldData.counter.turn))
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
    WorldData.display.remove(object)



# cleanup for duplicate sprites created when input is given
# too quickly

def clearBadSprites():
    goodSprites = []
    for being in WorldData.currentBeingList:
        goodSprites.append(being.sprite)
    stop = time.time() + .5
    for sprite in WorldData.display.items:
      if sprite not in goodSprites and type(sprite) == BeingSprite :
          WorldData.display.remove(sprite)
      if time.time() >= stop:
          break



# clears giblets from the display()

def clearGibList():
    for sprite in WorldData.gibList:
        WorldData.display.remove(sprite)
        WorldData.gibList.remove(sprite)
        del sprite



# used with thread.start_new_thread(threadRemoveSprite, (timeToWait, sprite))
# in order to despawn a sprite after a delay. For use with animations.
# parameters:
#   timeToWait      - time in seconds to delay the sprite removal
#   sprite          - sprite to be removed

def threadRemoveSprite(timeToWait, sprite):
    time.sleep(timeToWait)
    WorldData.display.remove(sprite)



#helper Functions
def spotToCoord(spot):
    #if low set to 0d
    if spot < 0: spot = 0
    #if high set to max (should probably just throw error
    if spot > WorldData.WIDTH_TILES * WorldData.HEIGHT_TILES: spot = WorldData.WIDTH_TILES * WorldData.HEIGHT_TILES - 1
    return Coords(spot % WWorldData.IDTH_TILES, spot / WorldData.WIDTH_TILES)


#given tile Coords give tile Spot in 1d array
def tileCoordToSpot(coord):
    return coord.x + coord.y * WorldData.WIDTH_TILES


#Goes from pixel coords to tile Coords
def coordToTileCoord(coord):
    return Coords(coord.x/WorldData.BITS, coord.y/WorldData.BITS)



#Goes from tile spot to pixel coords
def tileSpotToCoord(spot):
    return Coords((spot * WorldData.BITS)% WorldData.PIXEL_WIDTH, (spot / WorldData.WIDTH_TILES)*WorldData.BITS)


def coordToTile(coord):
    return coord.x/WorldData.BITS + (coord.y/WorldData.BITS) * WorldData.WIDTH_TILES


#takes pixel coordanates and returns if the tile at that location is
def isTraversable(x, y):
    spot = coordToTile(Coords(x,y))
    return WorldData.currentMap.isTraversable(spot)


# Converts pixel coordinates to "spot" coordinates
def textCoordToSpot(x, y):
  col = texWidth/32
  row = texHeight/32
  return x + y*col


# intro credits, adjust to add fade, etc.

def loadIntro():
    WorldData.loading.spawnSprite()
    WorldData.startScreen = RawSprite(WorldData.path + "Fullscreens/startScreen.png", 0, 0, 2)
    WorldData.loading.spawnSprite()
    WorldData.title = RawSprite(WorldData.path + "EffectSprites/Title.gif", 286, -64, 1)
    WorldData.loading.spawnSprite()
    WorldData.title.spawnSprite()
    WorldData.loading.spawnSprite()
    time.sleep(1.5)
    WorldData.startScreen.spawnSprite()
    WorldData.loading.removeSprite()
    WorldData.title.spawnSprite()
    slideSpriteDown(WorldData.title, 104)
    time.sleep(1.5)
    WorldData.text.onKeyType(mainMenuAction)
    WorldData.text.grabFocus()
    #thread.start_new_thread(music.play, (SoundData.dungeon_sound,))



# Clears the display, sets up layers for use, and displays
# the SAGA logo

def loadingScreen():
    WorldData.display.removeAll()
    setUpLayers()
    WorldData.loading.spawnSprite()



# Compacts and stores information about the current area and
# loads the next. The player will be spawned on the opposite side
# of the screen they exited from.
# Parameters:
#     Area      - The area to be loaded

def loadNewArea(area):
    loadingScreen()
    setUpLayers()

#   thread.start_new_thread(music.loop2, (SoundData.background_Music,))

    for light in WorldData.lightSources:
      if light.isOn:
        light.turnOff()
        WorldData.CURRENT_AREA.wasOn.append(light)
    WorldData.currentMap = area.mapObject
    WorldData.CURRENT_BG = area.mapSprite
    WorldData.CURRENT_AREA = area
    WorldData.CURRENT_BG.spawnSprite()
    WorldData.display.add(WorldData.text)
    try:
      WorldData.currentBeingList.remove(WorldData.bot1)
    except:
      None
    WorldData.currentBeingList = area.beingList
    WorldData.currentBeingList.append(WorldData.bot1)
    WorldData.bot1.area = WorldData.CURRENT_AREA
    WorldData.objectList = area.objectList
    WorldData.gibList = area.gibList
    WorldData.animatedSpriteList = area.animatedSpriteList
    WorldData.lightSources = area.lightSources
    for being in WorldData.currentBeingList:
      being.sprite.spawnSprite()
    for thing in area.objectList:
        thing.sprite.spawnSprite()
    for gib in WorldData.gibList:
        WorldData.display.add(gib)
    WorldData.loading.removeSprite()
    for light in WorldData.CURRENT_AREA.wasOn:
        light.turnOn()
    for sprite in WorldData.CURRENT_AREA.persistentAnimations:
      if sprite in WorldData.animatedSpriteList:
        WorldData.animatedSpriteList.remove(sprite)
      sprite.animate()
    WorldData.text.grabFocus()
    WorldData.bot1.hpBar.updateBar()
    WorldData.bot1.wallet.updateWalletDisplay()
    turnPass()



 # Adds 7 sprites as placeholders to create layers
 # for use with future sprites

def setUpLayers():
    try:
      WorldData.layer0.removeSprite()
      WorldData.layer1.removeSprite()
      WorldData.layer2.removeSprite()
      WorldData.layer3.removeSprite()
      WorldData.layer4.removeSprite()
      WorldData.layer5.removeSprite()
      WorldData.layer6.removeSprite()
      WorldData.layer0.spawnSprite()
      WorldData.layer1.spawnSprite()
      WorldData.layer2.spawnSprite()
      WorldData.layer3.spawnSprite()
      WorldData.layer4.spawnSprite()
      WorldData.layer5.spawnSprite()
      WorldData.layer6.spawnSprite()
    except:
      WorldData.layer0 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 0)
      WorldData.layer1 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 1)
      WorldData.layer2 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 2)
      WorldData.layer3 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 3)
      WorldData.layer4 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 4)
      WorldData.layer5 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 5)
      WorldData.layer6 = RawSprite(WorldData.path + "EffectSprites/blankSprite.gif", 0, 0, 6)
      WorldData.layer0.spawnSprite()
      WorldData.layer1.spawnSprite()
      WorldData.layer2.spawnSprite()
      WorldData.layer3.spawnSprite()
      WorldData.layer4.spawnSprite()
      WorldData.layer5.spawnSprite()
      WorldData.layer6.spawnSprite()



# Default keybindings/controls



#Inventory Control: resets closes and resets menu with each item select. If no item, reloads.
def inventoryAction(menuInput):
  bot1Ready = (WorldData.bot1.weapon.displayed == false and WorldData.bot1.isMoving == false)
  if menuInput == "1":
    if bot1Ready:
      try:
        WorldData.bot1.inv[0].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "2":
    if bot1Ready:
      try:
        WorldData.bot1.inv[1].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "3":
    if bot1Ready:
      try:
        WorldData.bot1.inv[2].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "4":
    if bot1Ready:
      try:
        WorldData.bot1.inv[3].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "5":
    if bot1Ready:
      try:
        WorldData.bot1.inv[4].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "6":
    if bot1Ready:
      try:
        WorldData.bot1.inv[5].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "7":
    if bot1Ready:
      try:
        WorldData.bot1.inv[6].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "8":
    if bot1Ready:
      try:
        WorldData.bot1.inv[7].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "9":
    if bot1Ready:
      try:
        WorldData.bot1.inv[8].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "0":
    if bot1Ready:
      try:
        WorldData.bot1.inv[9].use(WorldData.bot1)
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "!":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[0])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "@":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[1])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "#":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[2])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "$":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[3])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "%":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[4])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "^":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[5])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "&":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[6])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "*":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[7])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "(":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[8])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == ")":
    if bot1Ready:
      try:
        WorldData.bot1.inv.remove(WorldData.bot1.inv[9])
      except:
        thread.start_new_thread(music.Play, (SoundData.hit_sound,))
    WorldData.menu.closeMenu()
    WorldData.menu.openItemMenu()

  elif menuInput == "m":
    if bot1Ready:
      WorldData.menu.openStatusMenu()
      WorldData.text.onKeyType(menuAction)



def keyAction(a):
  bot1Ready = (WorldData.bot1.weapon.displayed == false and WorldData.bot1.isMoving == false)
  if a == "w":
    if bot1Ready:
        WorldData.bot1.moveUp()
        turnPass()
  elif a == "s":
    if bot1Ready:
        WorldData.bot1.moveDown()
        turnPass()
  elif a == "a":
    if bot1Ready:
        WorldData.bot1.moveLeft()
        turnPass()
  elif a == "d":
    if bot1Ready:
        WorldData.bot1.moveRight()
        turnPass()
  elif a == "W":
        WorldData.bot1.faceUp()
  elif a == "A":
        WorldData.bot1.faceLeft()
  elif a == "S":
        WorldData.bot1.faceDown()
  elif a == "D":
        WorldData.bot1.faceRight()
  elif a == "f": #attack
    if bot1Ready:
        WorldData.bot1.meleeAtk()
        turnPass()
  elif a == "z": #attack
    if bot1Ready:
        WorldData.bot1.specialAtk()
        turnPass()
  elif a == "g": #steal
    if bot1Ready:
        WorldData.bot1.steal(WorldData.bot1.getFrontTarget())
        turnPass()
  elif a == "q":
    print("NotImplementedAtAll")
  elif a == "t":
    print("not implemented")
  elif a == "v":
    WorldData.bot1.talk()
  elif a == " ":
      WorldData.bot1.activateTarget()
     #Menu Logic
  elif a == "m": #Activates menu, switches to menu controls
    if bot1Ready:
      WorldData.menu.openStatusMenu()
      WorldData.text.onKeyType(menuAction)



def buyTransactionKeyAction(inp):
    if inp == "1":
      MenuData.transaction.buy(MenuData.transaction.seller.inv[0])
    if inp == "2":
      MenuData.transaction.buy(MenuData.transaction.seller.inv[1])
    if inp == "3":
      MenuData.transaction.buy(MenuData.transaction.seller.inv[2])
    if inp == "4":
      MenuData.transaction.buy(MenuData.transaction.seller.inv[3])
    elif inp == "m":
        WorldData.menu.closeMenu()
        WorldData.text.onKeyType(keyAction)


    # Keybindings/controls for menus


def menuAction(menuInput):

  bot1Ready = (WorldData.bot1.weapon.displayed == false and WorldData.bot1.isMoving == false)

  if menuInput == "u":
    if bot1Ready:
      WorldData.menu.openStatusMenu()

  elif menuInput == "x": #testing
    if bot1Ready:
        WorldData.menu.openPopMenu()

  elif menuInput == "i":
    if bot1Ready:
        WorldData.text.onKeyType(inventoryAction)
        WorldData.menu.openItemMenu()

  elif menuInput == "q":
    if bot1Ready:
      try:
        music.Stop(SoundData.dungeon_sound)
      except:
        None
      try:
        music.Stop(SoundData.quieter_music)
      except:
        None
      try:
        music.Stop(SoundData.background_Music)
      except:
        None
      saveBot()
      WorldData.display.hide()
   #   sys.exit()
      print "When this works, it will quit game."

  elif menuInput == "m":
    if bot1Ready:
      WorldData.menu.closeMenu()
      WorldData.text.onKeyType(keyAction)



    # Default controls for main menu
def mainMenuAction(inp):
  WorldData.text.onKeyType(blockKeys)
  WorldData.title.removeSprite()
  WorldData.startScreen.removeSprite()
  if inp == "2":
    loadBot()
  else:
    newBot()
    startGame()



# To pass to getKeyTyped in order to block inputs
# (e.g., during animations or delays)

def blockKeys(a):
    None



# Damage calculation logic for combat. Note:
# Certain friendlies will be obliterated on defeat
# Currently meant to be called with thread.start_new_thread
# to line up damage with animations

def threadDamageCalculation(self, target, damage, delay):
  time.sleep(delay)
  if target != WorldData.bot1:
    target.hostile = true
  target.changeHp(damage*(-1))
  target.displayDamage()
  if target.hp <= 0:
    self.changeXp(target.xpValue)
    if target == WorldData.friendlyGreen:
      del WorldData.friendlyGreen
    elif target == WorldData.friendlyOrange:
      del WorldData.friendlyOrange
    elif target == WorldData.shopKeeper:
      del WorldData.shopKeeper



  # Game startup/bootup logic

def startGame():
  WorldData.loading.spawnSprite()
  WorldData.CURRENT_AREA = AreaData.TOWN_AREA
  WorldData.CURRENT_BG = AreaData.TOWN_AREA.mapSprite
  WorldData.CURRENT_BG.spawnSprite()
  WorldData.currentBeingList = AreaData.TOWN_AREA.beingList
  WorldData.objectList = AreaData.TOWN_AREA.objectList
  WorldData.gibList = AreaData.TOWN_AREA.gibList
  WorldData.animatedSpriteList = AreaData.TOWN_AREA.animatedSpriteList
  WorldData.lightSources = AreaData.TOWN_AREA.lightSources
  bot1Spawn = Coords(13*WorldData.BITS, 1*WorldData.BITS)
  WorldData.shopKeeper = ShopKeeper("shopKeep", "Stick", SpriteData.shopKeeperSpritePaths, 3*WorldData.BITS, 6*WorldData.BITS)
  WorldData.shopKeeper.inv.append(Weapon("Rock"))
  WorldData.shopKeeper.sprite.spawnSprite()
  WorldData.friendlyOrange = Friendly("orange", "Stick", SpriteData.friendlyOrangeSpritePaths, 8*WorldData.BITS, 10*WorldData.BITS)
  WorldData.friendlyGreen = Friendly("green", "Stick", SpriteData.friendlyGreenSpritePaths, 10*WorldData.BITS, 10*WorldData.BITS)
  WorldData.friendlyOrange.sprite.spawnSprite()
  WorldData.friendlyGreen.sprite.spawnSprite()
  #should be spawning boss in the dungeon?
  AreaData.DUNGEON_BOSSROOM_AREA.beingList.append(WorldData.boss)
  loadNewArea(AreaData.TOWN_AREA)#refresh screen, start animations
  WorldData.loading.removeSprite()
  WorldData.menu = Menu(WorldData.bot1)
  WorldData.text.grabFocus()
  time.sleep(.2) #gives sliding title time to finish
  WorldData.text.onKeyType(keyAction)

  # Logic for starting a new character.  Bot1/User will have starting stats
def newBot():
  WorldData.bot1 = User("bot1", "Stick", SpriteData.userSpritePaths, AreaData.TOWN_AREA)
  WorldData.bot1.area = WorldData.CURRENT_AREA
  WorldData.bot1.inv.append(Potion())
  WorldData.bot1.inv.append(Potion())



  # Logic for loading a character. If data exists, bot1 will be loaded from it.
  # Otherwise, the starting screen will replay with a message warning the user
def loadBot():
  WorldData.bot1 = User("bot1", "Stick", SpriteData.userSpritePaths, AreaData.TOWN_AREA)
  try:
    fin = open(WorldData.path + "SaveData.txt")
    for line in fin:
      if "CharName:" in line:
        WorldData.bot1.name = line[len("Name:"):line.index('\n')]
      elif "Weapon:" in line:
        WorldData.bot1.weapon = Weapon(line[len("Weapon:"):line.index('\n')])
      elif "Level:" in line:
        WorldData.bot1.level = int(line[len("Level:"):line.index('\n')])
      elif "MaxHp:" in line:
        WorldData.bot1.maxHp = int(line[len("MaxHp:"):line.index('\n')])
      elif "CurrentHp:" in line:
        WorldData.bot1.maxHp = int(line[len("CurrentHp:"):line.index('\n')])
      elif "Xp:" in line:
        WorldData.bot1.xp = int(line[len("Xp:"):line.index('\n')])
      elif "Atk:" in line:
        WorldData.bot1.atk = int(line[len("Atk:"):line.index('\n')])
      elif "Def" in line:
        WorldData.bot1.df = int(line[len("Def:"):line.index('\n')])
      elif "Wallet" in line:
        WorldData.bot1.changeWallet(int(line[len("Wallet:"):line.index('\n')]))
    fin.close()
    startGame()
  except:
    thread.start_new_thread(loadIntro, ())
  


    # Saves the user's stats to a file for future loading
def saveBot():
  fout = open(WorldData.path + "SaveData.txt", 'w')
  fout.write("CharName:"+str(WorldData.bot1.name)+"\n")
  fout.write("Weapon:"+str(WorldData.bot1.weapon.name)+"\n")
  fout.write("Level:"+str(WorldData.bot1.level)+"\n")
  fout.write("MaxHp:"+str(WorldData.bot1.maxHp)+"\n")
  fout.write("CurrentHp:"+str(WorldData.bot1.hp)+"\n")
  fout.write("Xp:"+str(WorldData.bot1.xp)+"\n")
  fout.write("Atk:"+str(WorldData.bot1.atk)+"\n")
  fout.write("Def:"+str(WorldData.bot1.df)+"\n")
  fout.write("Wallet:"+str(WorldData.bot1.wallet.value)+"\n")
  fout.close()



def areaSetup():
  #initailize background image
  tilesPath = WorldData.path + "Tiles/LPC/tiles/"
  #Old, probably dont need textureMap anymore
  #textureMap = makePicture(WorldData.path + "Tiles/hyptosis_tile-art-batch-1.png")

  #initailize textures
  #  Tile(isTraversable, isPassable, isTough, desc)
  #add Dirt
  WorldData.dirt = Tile(true, true, false, "dirt")
  WorldData.dirtWall = Tile(false, true, false, "dirtWall")
  WorldData.grass = Tile(true, true, false, "grass")
  WorldData.stone = Tile(true, true, false, "stone")
  WorldData.stoneWall = Tile(false, true, false, "stoneWall")
  WorldData.hole = Tile(true, true, false, "hole")
  WorldData.lavaRock = Tile(true, true, false, "lavaRock")
  WorldData.water = Tile(false, true, false, "water")
  WorldData.lava = Tile(false, true, false, "lava")
  WorldData.fence = Tile(false, true, false, "fence")
  WorldData.chest = Tile(false, true, false, "chest")
  WorldData.door = Tile(true, false, false, "door")
  WorldData.blank = Tile(false, false, false, "Filler for structure class")
  WorldData.structPath = WorldData.path + "Tiles/LPC/structures/"

  #get width and height
  #texWidth = getWidth(textureMap)
  #texHeight = getHeight(textureMap)


  paths = ["d", "s", "h", ".", "o"]
  #create empty grass field will clean up later
  home  = "fffffffffffffddddfffffffffffffff"
  home += "fh......ggt,,ddddgh......gg,,,gf"
  home += "f.......gg,,,ddddg.......dg,,,gf"
  home += "f.......gg,,,ddddg.......dd,g,gf"
  home += "f..o....gggggddddg..o....dd,g,gf"
  home += "f..o....gggggddddg..o....dd,g,gf"
  home += "fgsssssssddddddddddddddddddggddd"
  home += "fgsssssssddddddddddddddddddddddd"
  home += "fgggsssssggggddddddddddddddddddd"
  home += "fgggddssgggggddddddddddddddddddd"
  home += "fgggdddggggwwwwddddddh......gggf"
  home += "fgggdddgggwwwwwwddddd.......gggf"
  home += "fgggdddwwwwwwwwwwwwdd.......gggf"
  home += "fgggdddwwwwwwwwwwwwdd..o....t,,f"
  home += "fgdddddwwwwwwwwwwwddd..o....,,,f"
  home += "fgdddddddwwwwwwwdddddddddddd,,,f"
  home += "fggddddddgggggggddddddddddddgdgf"
  home += "ffffffffffffffffffffffffffffffff"
  townMap = Map(home)
  AreaData.TOWN_AREA.mapObject = townMap
  WorldData.currentMap = townMap

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
  AreaData.N_FIELD_AREA.mapObject = nfieldMap

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
  AreaData.E_FIELD_AREA.mapObject = efieldMap

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
  AreaData.NE_FIELD_AREA.mapObject = nefieldMap

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
  AreaData.DUNGEON_ENTRANCE_AREA.mapObject = entranceMap

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
  AreaData.DUNGEON_WESTROOM_AREA.mapObject = westRoomMap

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
  AreaData.DUNGEON_EASTROOM_AREA.mapObject = eastRoomMap

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
  AreaData.DUNGEON_KEYROOM_AREA.mapObject = keyRoomMap

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
  AreaData.DUNGEON_MINIBOSS_AREA.mapObject = miniBossMap

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
  AreaData.DUNGEON_BOSSKEY_AREA.mapObject = bossKeyMap

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
  AreaData.DUNGEON_BOSSROOM_AREA.mapObject = bossRoomMap
  AreaData.TOWN_AREA.spawnCoords = Coords(13*WorldData.BITS, 1*WorldData.BITS)
  AreaData.TOWN_AREA.lightSources.append(LightSource(SpriteData.bigTorchSpritePaths, 416, 288, 1))
  AreaData.TOWN_AREA.lightSources.append(LightSource(SpriteData.bigTorchSpritePaths, 384, 288, 1))
  AreaData.TOWN_AREA.lightSources.append(LightSource(SpriteData.lightpostSpritePaths, 128, 192, 1))
  AreaData.TOWN_AREA.objectList.append(HealingStation(SpriteData.healingStationSpritePaths, 896, 64))
  for i in AreaData.TOWN_AREA.lightSources:
    AreaData.TOWN_AREA.objectList.append(i)
  AreaData.DUNGEON_ENTRANCE_AREA.lightSources.append(DungeonTorch(SpriteData.bigTorchSpritePaths, 32, 32, AreaData.DUNGEON_ENTRANCE_AREA, 1))
  AreaData.DUNGEON_ENTRANCE_AREA.lightSources.append(DungeonTorch(SpriteData.bigTorchSpritePaths, 960, 32, AreaData.DUNGEON_ENTRANCE_AREA, 1))
  AreaData.DUNGEON_ENTRANCE_AREA.lightSources.append(DungeonTorch(SpriteData.bigTorchSpritePaths, 32, 512, AreaData.DUNGEON_ENTRANCE_AREA, 1))
  AreaData.DUNGEON_ENTRANCE_AREA.lightSources.append(DungeonTorch(SpriteData.bigTorchSpritePaths, 960, 512, AreaData.DUNGEON_ENTRANCE_AREA, 1))
  for i in AreaData.DUNGEON_ENTRANCE_AREA.lightSources:
    AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(i)
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 992, 288))
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 0, 288))
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 992, 256))
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 0, 256))
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 512, 0))
  AreaData.DUNGEON_ENTRANCE_AREA.objectList.append(Door(SpriteData.doorSpritePaths, 480, 0))
  #OverWorld connections
  joinNorthSouthAreas(AreaData.N_FIELD_AREA, AreaData.TOWN_AREA)
  joinNorthSouthAreas(AreaData.NE_FIELD_AREA, AreaData.E_FIELD_AREA)
  joinEastWestAreas(AreaData.NE_FIELD_AREA, AreaData.N_FIELD_AREA)
  joinEastWestAreas(AreaData.E_FIELD_AREA, AreaData.TOWN_AREA)
  joinOtherAreas(AreaData.NE_FIELD_AREA, AreaData.DUNGEON_ENTRANCE_AREA)
  #Dungeon Connections
  joinOtherAreas(AreaData.DUNGEON_ENTRANCE_AREA, AreaData.NE_FIELD_AREA)
  joinEastWestAreas(AreaData.DUNGEON_ENTRANCE_AREA, AreaData.DUNGEON_WESTROOM_AREA)
  joinEastWestAreas(AreaData.DUNGEON_EASTROOM_AREA, AreaData.DUNGEON_ENTRANCE_AREA)
  joinNorthSouthAreas(AreaData.DUNGEON_KEYROOM_AREA, AreaData.DUNGEON_WESTROOM_AREA)
  joinNorthSouthAreas(AreaData.DUNGEON_BOSSROOM_AREA, AreaData.DUNGEON_ENTRANCE_AREA)
  joinNorthSouthAreas(AreaData.DUNGEON_EASTROOM_AREA, AreaData.DUNGEON_BOSSKEY_AREA)
  joinNorthSouthAreas(AreaData.DUNGEON_MINIBOSS_AREA, AreaData.DUNGEON_EASTROOM_AREA)



def displaySetup():
  setUpLayers()
  WorldData.display.add(WorldData.text, -32, -32)



#music
def soundSetup():
  thread.start_new_thread(music.volume, (SoundData.move, .08,))
  thread.start_new_thread(music.volume, (SoundData.move1, .08,))
  thread.start_new_thread(music.volume, (SoundData.move2, .08,))
  thread.start_new_thread(music.volume, (SoundData.move3, .08,))
  thread.start_new_thread(music.volume, (SoundData.move4, .08,))
  thread.start_new_thread(music.volume, (SoundData.background_Music, .07,))



def main():

  WorldData.display = CustomDisplay("Robot Saga", WorldData.backWidth, WorldData.backHeight)
  WorldData.loading = RawSprite(WorldData.path + "Fullscreens/LogoOmega.png", 0, 0, 0)
  WorldData.boss = Boss1(AreaData.DUNGEON_BOSSROOM_AREA)
  displaySetup()
  areaSetup()
  soundSetup()
  loadIntro()



               #################
               #               #
               #   LETS GO!!   #
               #               #
               #################


main()
