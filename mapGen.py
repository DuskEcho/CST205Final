#bits is how many pixels are in each texture
bits = 32
#how many tiles there are wide
widthTiles = 40
#how many tiles there are tall
heightTiles = 22

try:
           path #test to see if path exists
except NameError: #if path does not exist make new path
           printNow("Please select your game install folder")
           path = pickAFolder()
else: printNow("Welcome Back") #welcome the player back to the game

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

#convert texture coord to a spot 
def textCoordToSpot(x, y):
  col = texWidth/32
  row = texHeight/32
  return x + y*col

#retrieve texture from spot on textureMap
def getTexture(spot, texMap):
    texture = makeEmptyPicture(bits,bits)
    #spot to coord conversion
    startx = (spot * bits) % texWidth;
    starty = ((spot * bits) / texWidth) * bits;
    for x in range(0, bits):
        for y in range(0, bits):
            setColor(getPixel(texture, x, y), getColor(getPixel(texMap, x + startx, y + starty)))
    return texture


class Map():
    def __init__(self, tileMap):
        self.tileMap = {} #change to make map
        #beings will probably be a dictionary with coords as the key and value is the being at the spot
        self.beings = {} #master holder for all of the beings
        self.map = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
        self.updateBackground(tileMap, self.map)


    def placeTex(self, tex, spot):
        startx = (spot * bits) % backWidth
        starty = ((spot * bits) / backWidth) * bits
        #printNow(spot)
        self.tileMap.update({spot: tex})
        #placeTex(tex.getImg(), spot, self.Map)
        for x in range(0, bits):
            for y in range(0, bits):
                setColor(getPixel(self.map, startx + x, starty + y), getColor(getPixel(tex.getImg(), x, y)))


    def updateBackground(self, tiles, back):
        for spot in range(0, len(tiles)):
            if   tiles[spot] == "g": self.placeTex(grass, spot)
            elif tiles[spot] == "s": self.placeTex(stone, spot)
            #not in files yet
            #elif tiles[spot] == "m": placeTex(monster, spot)
            #elif tiles[spot] == "p": placeTex(player, spot)
            #elif tiles[spot] == "w": placeTex(wall, spot)
        writePictureTo(self.map, path + "newBack.png")


    def isTraversable(self, spot):
        printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1: return false
        printNow(self.tileMap[spot].getTraversable())
        printNow(self.tileMap[spot].getDesc())
        return self.tileMap[spot].getTraversable()


    def getMap(self):
        return self.map


textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")
#explore(textureMap)

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)
#initailize textures
stone = Tile(getTexture(textCoordToSpot(3,24), textureMap), false, true, false, "stone")
grass = Tile(getTexture(textCoordToSpot(10,19), textureMap), true, true, false, "grass")


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
home += "ssssssssssssssssssssssssssssssssssssssss"
#initailize background image
backWidth = bits * widthTiles
backHeight = bits * heightTiles
baseMap = Map(home)
