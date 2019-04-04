#bits is how many pixels are in each texture
bits = 32
#how many tiles there are wide
widthTiles = 32 #old value 40
#how many tiles there are tall
heightTiles = 18 #old value 22

#consts
right = 1
left = 2
up = 4
down = 8
downAndRight = 16
downAndLeft = 32
upAndRight = 64
upAndLeft = 128
downRight = down | right | downAndRight
downLeft = down | left | downAndLeft
upRight = up | right | upAndRight
upLeft = up | left | upAndLeft
upRightDown = up | right | down | upAndRight | downAndRight
upLeftDown = up | left | down | upAndLeft | downAndLeft
rightUpLeft = right | up | left | upAndRight | upAndLeft
rightDownLeft = right | down | left | downAndLeft | downAndRight
allRound = up | down | left | right | downAndLeft | downAndRight | upAndRight | upAndLeft

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
        self.tileArr = tile
        #can a being walk over
        self.isTraversable = isTraversable
        #can a projectile go over
        self.isPassable = isPassable
        #ai gets 2 turns if player is on this tile
        self.isTough = isTough
        self.beings = {} #array of beings in that tile

    def getImg(self, around):
        # 1110 1111
        #&0001 0000
        #printNow(not around & upAndRight)
        if not around ^ allRound: return self.tileArr[9]
        elif around & upRightDown: return self.tileArr[3]
        elif around & upLeftDown: return self.tileArr[15]
        elif around & rightUpLeft: return self.tileArr[10]
        elif around & rightDownLeft: return self.tileArr[8]
        elif around & upDownLeftRight: return self.tileArr[9]
        elif around & upDownLeftRight: return self.tileArr[9]
        elif not around ^ downRight: return self.tileArr[2]
        elif not around ^ downLeft: return self.tileArr[14]
        elif not around ^ upRight: return self.tileArr[4]
        elif not around ^ upLeft: return self.tileArr[16]
        elif not around & upAndRight: return self.tileArr[7]
        elif not around & upAndLeft: return self.tileArr[13]
        elif not around & downAndRight: return self.tileArr[6]
        elif not around & downAndLeft: return self.tileArr[12]
        return self.tileArr[1]

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

#given tile Coords give tile Spot in 1d array
def tileCoordToSpot(coord):
    return coord.x + coord.y * widthTiles

def spotToCoord(spot):
    #if low set to 0d
    if spot < 0: spot = 0
    #if high set to max (should probably just throw error
    if spot > widthTiles * heightTiles: spot = widthTiles * heightTiles - 1
    return Coords(spot % widthTiles, spot / widthTiles)

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


    def placeTex(self, tex, spot, around):
        startx = (spot * bits) % backWidth
        starty = ((spot * bits) / backWidth) * bits
        #printNow(spot)
        self.tileMap.update({spot: tex})
        printNow(around)
        img = tex.getImg(around)
        for x in range(0, bits):
            for y in range(0, bits):
                setColor(getPixel(self.map, startx + x, starty + y), getColor(getPixel(img, x, y)))

    def updateBackground(self, tiles, back):
        for spot in range(0, len(tiles)):
            # dirs [right, left, up, down, downRight, downLeft, upRight, upLeft]
            around = 0
            #dirs = [[1,0,right],[-1,0,left],[0,-1,up],[0,1,down]]
            dirs = [[1,0,right],[-1,0,left],[0,-1,up],[0,1,down],[1,1,downAndRight],[-1,1,downAndLeft],[1,-1,upAndRight],[-1,-1,upAndLeft]]
            for d in dirs:
                curr = spotToCoord(spot)
                new = Coords(curr.x + d[0], curr.y + d[1])
                if new.x >= widthTiles or new.y >= heightTiles: continue
                if new.x < 0 or new.y < 0: continue
                #if tileCoordToSpot(new) >= len(tiles): continue
                if tiles[tileCoordToSpot(new)] == tiles[spot]:
                    around = around | d[2] #bitwise or direction with around
                    #printNow(around)
                    #d[2] = true
            if   tiles[spot] == "g": self.placeTex(grass, spot, around)
            elif tiles[spot] == "s": self.placeTex(stone, spot, around)
            elif tiles[spot] == "d": self.placeTex(dirt, spot, around)
            elif tiles[spot] == "h": self.placeTex(houseWall, spot, around)
            elif tiles[spot] == "r": self.placeTex(houseRoof, spot, around)
            repaint(self.map)
            #not in files yet
            #elif tiles[spot] == "m": placeTex(monster, spot)
            #elif tiles[spot] == "p": placeTex(player, spot)
            #elif tiles[spot] == "w": placeTex(wall, spot)
        writePictureTo(self.map, path + "newBack.png")
        explore(self.map)


    def isTraversable(self, spot):
        printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1: return false
        printNow(self.tileMap[spot].getTraversable())
        printNow(self.tileMap[spot].getDesc())
        return self.tileMap[spot].getTraversable()


    def getMap(self):
        return self.map

def tileMapToArr(tileMap):
    width = getWidth(tileMap)/bits
    height = getHeight(tileMap)/bits
    tileArr = [];
    for startx in range(0, width):
        for starty in range(0, height):
            tile = makeEmptyPicture(bits,bits)
            for x in range(0, bits):
                for y in range(0, bits):
                    setColor(getPixel(tile, x, y), getColor(getPixel(tileMap, x + startx * bits, y + starty * bits)))
            #explore(tile)
            tileArr.append(tile)
    printNow(len(tileArr))
    return tileArr


tilesPath = path + "Tiles/LPC/tiles/"
textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")
dirtMap = makePicture(tilesPath + "dirt.png")
dirtArr = tileMapToArr(dirtMap)
grassMap = makePicture(tilesPath + "grass.png")
grassArr = tileMapToArr(grassMap)
stoneMap = makePicture(tilesPath + "stone.png")
stoneArr = tileMapToArr(stoneMap)

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)
#initailize textures
#  Tile(imgArr, isTraversable, isPassable, isTough, desc)
dirt = Tile(dirtArr, false, true, false, "dirt")
grass = Tile(grassArr, true, true, false, "grass")
stone = Tile(stoneArr, true, true, false, "stone")


#create emply grass field will clean up later
home  = "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "ggggggssssggggggggggggggddgggggg"
home += "ggggggssssgggggggggggggddddggggg"
home += "ggggggssssgggggggggggggddddggggg"
home += "ggggggsssggggggggggggggddggggggg"
home += "gggggssssggggggggggggggggggggggg"
home += "ggggsssssggggggggggggggggggggggg"
home += "ggggsssssggggggggggggggggggggggg"
home += "ggggggssgggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
home += "gggggggggggggggggggggggggggggggg"
#initailize background image
backWidth = bits * widthTiles
backHeight = bits * heightTiles
baseMap = Map(home)
