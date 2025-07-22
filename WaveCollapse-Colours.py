import os
import cv2
import numpy as np
import random
import time


mapSize = 32
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
trees = ['trees', 'grass', 'plants'] #brown
sand = ['sand','grass', 'rocks', 'water'] #yellow
housing = ['housing','grass']#purple , 'trees', 'sand', 'water', 'plants'
rocks = ['rocks','grass', 'sand']#grey
water = ['grass', 'water', 'sand']#blue
plants = ['plants', 'grass', 'trees']#red

frame = 0

def initialiseMap(map):
    for i in range (0, mapSize):
        for j in range(0, mapSize):
            map[i][j] = Tile()

    return map

def First_Pick(map):
    x = random.randint(0, mapSize - 1)
    y = random.randint(0, mapSize - 1)
    print("X: " + str(x))
    print("Y: " + str(y))
    tile = map[y][x]

    domainRange = len(tile.domain)
    pick = random.randint(0, domainRange - 1)

    pickString = tile.domain[pick]
    tile.generated = 1
    tile.tileTypeString = pickString
    print("Type: " + str(tile.tileTypeString))
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
            #print("I: " + str(i) + " J: " + str(j))

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
    go =True
    count = 0
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
        try:
            tile = map[tileToChange[0]][tileToChange[1]]
            if tile.generated == 0:
                go = False
        except:
            changedTile = (random.randint(0, mapSize - 1), random.randint(0, mapSize - 1))
            #print(changedTile)
            #tile = map[tileToChange[0]][tileToChange[1]]
            #We've hit the edge, lets find a new place to generate.
            #Scan through array and find a generated tile
        if count > 10:
            changedTile = (random.randint(0, mapSize - 1), random.randint(0, mapSize - 1))
            #print(changedTile)
            #tile = map[tileToChange[0]][tileToChange[1]]
    
        
        count = count + 1
        

    print(tile.domain)
    domainRange = len(tile.domain)
    pick = random.randint(0, domainRange - 1)
      
    pickString = tile.domain[pick]
    tile.generated = 1
    tile.tileTypeString = pickString
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
                    colour = (0, 255, 0)
                elif(map[i][j].tileTypeString == 'trees'):
                    colour = (38, 38, 68)
                elif(map[i][j].tileTypeString == 'sand'):
                    colour = (63, 227, 252)
                elif(map[i][j].tileTypeString == 'housing'):
                    colour = (252, 63, 107)
                elif(map[i][j].tileTypeString == 'rocks'):
                    colour = (110, 110, 110)
                elif(map[i][j].tileTypeString == 'water'):
                    colour = (236, 182, 31)
                elif(map[i][j].tileTypeString == 'plants'):
                    colour = (0, 0, 200)

                mapImage = cv2.rectangle(mapImage, (int((i/mapSize)*windowSize),int((j/mapSize)*windowSize)), (int(((i + 1)/mapSize)*windowSize),int(((j + 1)/mapSize)*windowSize)), colour, -1)
    cv2.imshow("Map", mapImage)
    cv2.waitKey(0)



def main(map):
    global frame


    changedTile = (0, 0)
    map = initialiseMap(map)

    map, changedTile = First_Pick(map)
    Render(map)
    #ProcessLoop:
    while(True):
        print(frame)
        
        map = Update_Domains(map, changedTile)

        map, changedTile = Generate_Tile(map, changedTile)

        Render(map)
        frame = frame + 1
        #time.sleep(0.05)

if __name__ == '__main__':
    main(map)
