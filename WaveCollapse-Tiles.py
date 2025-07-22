import os
import cv2
import numpy as np
import random
import time

grassImage = cv2.imread("grass.png")
treesImage = cv2.imread("trees.png")
sandImage = cv2.imread("sand.png")
housingImage = cv2.imread("housing.png")
rocksImage = cv2.imread("rocks.png")
waterImage = cv2.imread("water.png")
plantsImage = cv2.imread("flowers.png")

mapSize = 128
windowSize = 1024
mapImage = np.zeros((windowSize,windowSize,3), np.uint8)
map = []

for i in range(mapSize):
    a = []
    for j in range(mapSize):
        a.append(None)
    map.append(a)

class Tile:
    generated = 0
    tileTypeString = None
    domain = ['grass', 'trees', 'sand', 'housing', 'rocks', 'water', 'plants']

#Rules:
grass = ['grass','trees', 'sand', 'housing', 'rocks', 'water', 'plants'] #green 
grassWeights = [0.143, 0.143, 0.143, 0.143, 0.143, 0.143, 0.143] #green 
trees = ['trees', 'grass', 'plants'] #brown
treesWeights = [0.333, 0.333, 0.333] 
sand = ['sand','grass', 'rocks', 'water'] #yellow
sandWeights = [0.25, 0.25, 0.25, 0.25]
housing = ['housing','grass']#purple , 'trees', 'sand', 'water', 'plants'
housingWeights=[0.5, 0.5]
rocks = ['rocks','grass', 'sand']#grey
rocksWeights=[0.333,0.333,0.333]
water = ['grass','water', 'sand']#blue
waterWeights=[0.00001, 0.99, 0.00999]
plants = ['plants', 'grass', 'trees']#red
plantsWeights=[0.333, 0.333, 0.333]
frame = 0

def initialiseMap(map):
    for i in range (0, mapSize):
        for j in range(0, mapSize):
            map[i][j] = Tile()
    return map

def First_Pick(map):
    x = random.randint(0, mapSize - 1)
    y = random.randint(0, mapSize - 1)
    tile = map[y][x]
    domainRange = len(tile.domain)
    pick = random.randint(0, domainRange - 1)
    pickString = tile.domain[pick]
    tile.generated = 1
    tile.tileTypeString = pickString
    return map, (y, x)

def Update_Domains(map, changedTile):
    y = changedTile[0]
    x = changedTile[1]
    subjectTile = map[changedTile[0]][changedTile[1]]
    ruleList = []
    if(subjectTile.tileTypeString == 'grass'):
        ruleList = grass
    elif(subjectTile.tileTypeString == 'trees'):
        ruleList = trees
    elif(subjectTile.tileTypeString == 'sand'):
        ruleList = sand
    elif(subjectTile.tileTypeString == 'housing'):
        ruleList = housing
    elif(subjectTile.tileTypeString == 'rocks'):
        ruleList = rocks
    elif(subjectTile.tileTypeString == 'water'):
        ruleList = water
    elif(subjectTile.tileTypeString == 'plants'):
        ruleList = plants
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if (i == y and j == x):
                continue
            newDomain = []
            if(i > mapSize - 1) or (i < 0) or (j < 0) or (j > mapSize - 1):
                continue
            for types in map[i][j].domain:
                for ruleTypes in ruleList:
                    if ruleTypes == types:
                        newDomain.append(types)
                        continue
            map[i][j].domain = newDomain
    return map

def Generate_Tile(map, changedTile):
    global water
    go =True
    count = 0
    waterTile = 0
    if map[changedTile[0]][changedTile[1]].tileTypeString == "water":
        waterTile = 1
    while(go):
        pick = random.randint(0, 7)
        if pick == 0:
            tileToChange = (changedTile[0]-1, changedTile[1]-1)
        if pick == 1:
            tileToChange = (changedTile[0]-1, changedTile[1])
        if pick == 2:
            tileToChange = (changedTile[0]-1, changedTile[1]+1)
        if pick == 3:
            tileToChange = (changedTile[0], changedTile[1]-1)
        if pick == 4:
            tileToChange = (changedTile[0], changedTile[1]+1)
        if pick == 5:
            tileToChange = (changedTile[0]+1, changedTile[1]-1)
        if pick == 6:
            tileToChange = (changedTile[0]+1, changedTile[1])
        if pick == 7:
            tileToChange = (changedTile[0]+1, changedTile[1]+1)
        #Make it so that it can't pick bad values
        if(tileToChange[0] < 0) or (tileToChange[0] > mapSize-1) or (tileToChange[1] < 0) or (tileToChange[1] > mapSize-1):
            continue
        tile = map[tileToChange[0]][tileToChange[1]]
        if tile.generated == 0:
            go = False
        if count > 10:
            changedTile = (random.randint(0, mapSize - 1), random.randint(0, mapSize - 1))
        count = count + 1
    if((len(tile.domain) == 3) and (waterTile == 1)):
        pickString = random.choices(population = water, weights= waterWeights, k=1)
        tile.tileTypeString = pickString[0]
    else:
        tile.tileTypeString = random.choice(tile.domain)
    tile.generated = 1
    return map, (tileToChange[0], tileToChange[1])

def Render(map):
    global mapImage
    basicRenderArray = []
    for i in range(mapSize):
        a = []
        for j in range(mapSize):
            a.append(None)
        basicRenderArray.append(a)
    for i in range (0, mapSize):
        for j in range(0, mapSize):
            if int(map[i][j].generated) == 0:    
                pass
            else:
                if(map[i][j].tileTypeString == 'grass'):
                    image = grassImage
                elif(map[i][j].tileTypeString == 'trees'):
                    image = treesImage
                elif(map[i][j].tileTypeString == 'sand'):
                    image = sandImage
                elif(map[i][j].tileTypeString == 'housing'):
                    image = housingImage
                elif(map[i][j].tileTypeString == 'rocks'):
                    image = rocksImage
                elif(map[i][j].tileTypeString == 'water'):
                    image = waterImage
                elif(map[i][j].tileTypeString == 'plants'):
                    image = plantsImage
                image = cv2.resize(image, (int(windowSize/mapSize),int(windowSize/mapSize)), interpolation = cv2.INTER_AREA)
                mapImage[int((i/mapSize)*windowSize):int(((i + 1)/mapSize)*windowSize), int((j/mapSize)*windowSize):int(((j + 1)/mapSize)*windowSize)] = image
    cv2.imshow("Map", mapImage)
    cv2.imwrite("MapImage4.jpg", mapImage)
    cv2.waitKey(0)

def main(map):
    global frame, mapImage
    while(True):
        changedTile = (0, 0)
        map = initialiseMap(map)
        map, changedTile = First_Pick(map)
        #ProcessLoop:
        while(True):
            map = Update_Domains(map, changedTile)
            map, changedTile = Generate_Tile(map, changedTile)
            #Render(map)
            frame = frame + 1
            if(frame == (mapSize*mapSize)-1):
                Render(map)
                mapImage = np.zeros((windowSize,windowSize,3), np.uint8)
                frame = 0
                break
        

if __name__ == '__main__':
    main(map)