import random

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
    def __init__(self, tile, isTraversable, isPassable, isTough, desc, char):
        self.char = char
        self.desc = desc
        self.tileArr = tile
        #can a being walk over
        self.isTraversable = isTraversable
        #can a projectile go over
        self.isPassable = isPassable
        #ai gets 2 turns if player is on this tile
        self.isTough = isTough
        self.beings = {} #array of beings in that tile

    def getBase(self, it):
        return self.tileArr[it]

    def getImg(self, around):
        # 1110 1111
        #&0001 0000
        #printNow(not around & upAndRight)
        if not around ^ allRound: return self.tileArr[17]
        if around & up:
            if around & right:
                if around & down:
                    if around & left:
                        if not around & upAndRight: return self.tileArr[7]
                        if not around & upAndLeft: return self.tileArr[13]
                        if not around & downAndRight: return self.tileArr[6]
                        if not around & downAndLeft: return self.tileArr[12]
                    return self.tileArr[3]
                if around & left: return self.tileArr[10]
                return self.tileArr[4]
            if around & left:
                #if around & right: return self.tileArr[10] #redundent
                if around & down: return self.tileArr[15]
                return self.tileArr[16]
        if around & down:
            if around & right:
                #if around & up: return self.tileArr[3]
                if around & left: return self.tileArr[8]
                return self.tileArr[2]
            if around & left:
                #if around & right: return self.tileArr[8] #redundent
                #if around & up: return self.tileArr[15]
                return self.tileArr[14]
        if self.desc == "fence":
            if around & right:
                if around & left: return self.tileArr[8]
                return self.tileArr[6]
            if around & up:
                if around & down: return self.tileArr[3]
                return self.tileArr[7]
            if around & left: return self.tileArr[12]
            if around & down: return self.tileArr[13]

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
    def __init__(self, tileMap, baseTile, filePath):
        self.filePath = filePath
        self.tileMap = {} #change to make map
        #beings will probably be a dictionary with coords as the key and value is the being at the spot
        self.beings = {} #master holder for all of the beings
        self.map = makeEmptyPicture(backWidth, backHeight) #704 is chosen because its divisible by 32
        self.baseTile = baseTile
        self.fillBack(self.baseTile)
        self.updateBackground(tileMap, self.map)


    def fillBack(self, tex):
        printNow(tex.desc)
        baseSpots = [5,11,17,9]
        for startx in range(0, widthTiles):
            for starty in range(0, heightTiles):
                num = random.randint(0,3)
                #printNow(num)
                img = tex.getBase(baseSpots[num])
                for x in range(0, bits):
                    for y in range(0, bits):
                        setColor(getPixel(self.map, x + startx * bits, y + starty * bits), getColor(getPixel(img, x, y)))


    def placeTex(self, tex, spot, around):
        startx = (spot * bits) % backWidth
        starty = ((spot * bits) / backWidth) * bits
        #printNow(spot)
        self.tileMap.update({spot: tex})
        #printNow(around)
        img = tex.getImg(around)
        for x in range(0, bits):
            for y in range(0, bits):
                if getColor(getPixel(img, x, y)) == white: continue
                setColor(getPixel(self.map, startx + x, starty + y), getColor(getPixel(img, x, y)))

    def placeStruct(self, struct, spot):
        startx = (spot * bits) % backWidth
        starty = ((spot * bits) / backWidth) * bits
        structWidth = getWidth(struct) / bits
        structHeight = getHeight(struct) / bits
        for structx in range(0, structWidth):
            for structy in range(0, structHeight):
                curr = spotToCoord(spot)
                newSpot = tileCoordToSpot(Coords(curr.x + structx, curr.y + structy))
                self.tileMap.update({newSpot: water}) #replace water with a blank tile
                for x in range(0,bits):
                    for y in range(0,bits):
                        if getColor(getPixel(struct, x + structx * bits, y + structy * bits)) == white: continue
                        setColor(getPixel(self.map, startx + x + structx * bits, starty + y + structy * bits), getColor(getPixel(struct, x + structx * bits, y + structy * bits)))

    def updateBackground(self, tiles, back):
        for spot in range(0, len(tiles)):
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
                elif tiles[spot] in paths and tiles[tileCoordToSpot(new)] in paths:
                    around = around | d[2] #bitwise or direction with around
            if   tiles[spot] == self.baseTile.char: continue
            elif tiles[spot] == "g": self.placeTex(grass, spot, around)
            elif tiles[spot] == "l": self.placeTex(lavaRock, spot, around)
            elif tiles[spot] == "s": self.placeTex(stone, spot, around)
            elif tiles[spot] == "d": self.placeTex(dirt, spot, around)
            elif tiles[spot] == "w": self.placeTex(water, spot, around)
            elif tiles[spot] == "f": self.placeTex(fence, spot, around)
            elif tiles[spot] == "L": self.placeTex(lava, spot, around)
            elif tiles[spot] == "h": self.placeStruct(house, spot)
            elif tiles[spot] == "t": self.placeStruct(tree1, spot)
            repaint(self.map)
            #not in files yet
            #elif tiles[spot] == "m": placeTex(monster, spot)
            #elif tiles[spot] == "p": placeTex(player, spot)
            #elif tiles[spot] == "w": placeTex(wall, spot)
        writePictureTo(self.map, path + self.filePath)


    def isTraversable(self, spot):
        #printNow(spot)
        if spot < 0 or spot > len(self.tileMap) - 1: return false
        #printNow(self.tileMap[spot].getTraversable())
        #printNow(self.tileMap[spot].getDesc())
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
    #printNow(len(tileArr))
    return tileArr


tilesPath = path + "Tiles/LPC/tiles/"
textureMap = makePicture(path + "Tiles/hyptosis_tile-art-batch-1.png")
#add Dirt
dirtMap = makePicture(tilesPath + "dirt.png")
dirtArr = tileMapToArr(dirtMap)
dirt = Tile(dirtArr, true, true, false, "dirt", "d")
#add Grass
grassMap = makePicture(tilesPath + "grass.png")
grassArr = tileMapToArr(grassMap)
grass = Tile(grassArr, true, true, false, "grass", "g")
#add Stone
stoneMap = makePicture(tilesPath + "stone.png")
stoneArr = tileMapToArr(stoneMap)
stone = Tile(stoneArr, true, true, false, "stone", "s")
#add lavaRock
lavaRockMap = makePicture(tilesPath + "lavarock.png")
lavaRockArr = tileMapToArr(lavaRockMap)
lavaRock = Tile(lavaRockArr, true, true, false, "lavaRock", "l")
#add Water
waterMap = makePicture(tilesPath + "water.png")
waterArr = tileMapToArr(waterMap)
water = Tile(waterArr, false, true, false, "water", "w")
#add lava
lavaMap = makePicture(tilesPath + "lava.png")
lavaArr = tileMapToArr(lavaMap)
lava = Tile(lavaArr, false, true, false, "lava", "L")
#add Fence
fenceMap = makePicture(tilesPath + "fence.png")
fenceArr = tileMapToArr(fenceMap)
fence = Tile(fenceArr, false, true, false, "fence", "f")

#structures
structPath = path + "Tiles/LPC/structures/"
house = makePicture(structPath + "house.png")
tree1 = makePicture(structPath + "tree1.png")

#initailize background image
backWidth = bits * widthTiles
backHeight = bits * heightTiles

#get width and height
texWidth = getWidth(textureMap)
texHeight = getHeight(textureMap)
#initailize textures
#  Tile(imgArr, isTraversable, isPassable, isTough, desc)

paths = ["d", "s", "h", ".", "o"]
#create emply grass field will clean up later
town  = "fffffffffffffddddfffffffffffffff"
town += "fh......ggt,,ddddgh......ggggggf"
town += "f.......gg,,,ddddg.......dgggggf"
town += "f.......gg,,,ddddg.......ddggggf"
town += "f.......gggggddddg..o....ddggggf"
town += "f.......gggggddddg..o....ddggggf"
town += "fgsssssssddddddddddddddddddggggf"
town += "fgsssssssddddddddddddddddddggddd"
town += "fgggsssssggggddddddddddddddddddd"
town += "fgggddssgggggddddddddddddddddddf"
town += "fgggdddggggwwwwddddddh......gggf"
town += "fgggdddgggwwwwwwddddd.......gggf"
town += "fgggdddwwwwwwwwwwwwdd.......gggf"
town += "fgggdddwwwwwwwwwwwwdd..o....t,,f"
town += "fgdddddwwwwwwwwwwwddd..o....,,,f"
town += "fgdddddddwwwwwwwdddddddddddd,,,f"
town += "fggddddddgggggggddddddddddddgdgf"
town += "ffffffffffffffffffffffffffffffff"
townMap = Map(town, grass, "townMap.png")

field  = "ffffffffffffffffffffffffffffffff"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggwwwwwwwwwgggggggggggf"
field += "fgggggggwwwwwwwwwwwwwggggggggggf"
field += "fggggggwwwwwwwwwwwwwwggggggggggf"
field += "fggggggwwwwwwwwwwwwwgggggggggggg"
field += "fgggggwwwwwwwwgt,,gggggggggggggg"
field += "fgggggwwwwwwggg,,,ggggwwwwwggggg"
field += "fgggggwwwwwwggg,,,gggwwwwwwwgggg"
field += "fgggggwwwwwwgggggggggwwwwwwwgggf"
field += "fgggggwwwwwggggggggwwwwwwwwwgggf"
field += "fggggggwwgggggwwwwwwwwwwwwwwgggf"
field += "fgggggggggggwwwwwwwwwwwwwwwggggf"
field += "fgggggggggggwwwwwwwwwwwwwggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggggggggggggf"
field += "fffffffffffffggggfffffffffffffff"
fieldMap = Map(field, grass, "Nfield.png")

field  = "fffffffffffffddddfffffffffffffff"
field += "fggggggggggggddddggggggggggggggf"
field += "fggggggggggggdddgggggwwwwwwwgggf"
field += "fggggggggggggdddgggggwwwwwwwwwgf"
field += "fggggggggggdddddggggwwwwwwwwwwgf"
field += "fgddddddddddddddggggwwwwwwwwwwgf"
field += "ddddddddddddddggggggwwwwwwwwwwgf"
field += "dddddddddddddggggggggggwwwwwwwgf"
field += "dddddwwwwgggggggggggggggwwwwwggf"
field += "ddddwwwwwggggggggggggggggggggggf"
field += "fggwwwwwwwggggggggggggggggt,,ggf"
field += "fggwwwwwwwwwwwwggggggggggg,,,ggf"
field += "fggwwwwwwwwwwwwggggggggggg,,,ggf"
field += "fgwwwwwwwwwwwwwgggggggggt,,t,,gf"
field += "fgwwwwwwwwwwwggggggggggg,,,,,,gf"
field += "fggwwwwwwwgggggggggggggg,,,,,,gf"
field += "fggggggggggggggggggggggggggggggf"
field += "ffffffffffffffffffffffffffffffff"
fieldMap = Map(field, grass, "Efield.png")

field  = "ffffffffffffffffffffffffffffffff"
field += "fggggggggggggggggggggggggggggggf"
field += "fggggggggggggggggggggwwwwwwwgggf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fggggggggggggggggggggwwwwwwwwwgf"
field += "fggggggggggggggggddddddgggwwwwgf"
field += "ddddddddddddddddddddddgggwwwwwgf"
field += "ddddddddddddddddddddddggwwwwwwgf"
field += "ddddddddddddddgddddgggggwwwwwggf"
field += "ddddddggggggggddddgggggggggggggf"
field += "fggdddddgggggggdgggggggggggggggf"
field += "fggggddddddgggddgggggggggggggggf"
field += "fgggggddddddddddgggggggggggggggf"
field += "fggggggggdddddddgggggggggggggggf"
field += "fgggggggddddddddgggggggggggggggf"
field += "fggggggggggggdddgggggggggggggggf"
field += "fggggggggggggdddgggggggggggggggf"
field += "fffffffffffffddddfffffffffffffff"
fieldMap = Map(field, grass, "NEfield.png")

dungeon  = "ffffffffffffffffffffffffffffffff"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllLLLLllllllllllllllllllf"
dungeon += "fllllllllLLLLLLLLllllllllllllllf"
dungeon += "fllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "lllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "lllllllllLLLLLLLLLLLlllllllllllf"
dungeon += "flllllllllllLLLLLLLLlllllllllllf"
dungeon += "flllllllllllLLLLlllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fllllllllllllllllllllllllllllllf"
dungeon += "fffffffffffffllllfffffffffffffff"
dungeonMap = Map(dungeon, lavaRock, "dungeonMap.png")
