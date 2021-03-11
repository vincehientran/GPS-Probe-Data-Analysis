import math

def loadData():
    print('Start loading data.')
    fileSlopes = open('Partition6467RoadSlopes.csv', 'r')
    fileLink = open('Partition6467LinkData.csv','r')

    # key: linkPVID
    # value: slope of link
    slopes = {}

    linesSlopes = fileSlopes.readlines()
    for line in linesSlopes:
        string = line[0:-1]
        slopeRow = string.split(',')
        linkPVID = slopeRow[0]
        slope = slopeRow[1]
        slopes[linkPVID] = slope

    # key: linkPVID
    # value: shapeInfo
    linkData = {}

    linesLinks = fileLink.readlines()
    for line in linesLinks:
        string = line[0:-1]
        linkRow = string.split(',')

        linkPVID = linkRow[0]
        if linkRow[-3] != '':
            shapeInfo = linkRow[-3].split('|')
            temp = []
            for shape in shapeInfo:
                temp.append(shape.split('/'))
            linkRow[-3] = temp
        shapeInfo = linkRow[-3]

        linkData[linkPVID] = shapeInfo

    fileSlopes.close()
    fileLink.close()
    print('Finished loading data.')
    run(slopes, linkData)

def run(slopes, linkData):
    print('Start evaluation.')
    fileSlopes = open('Partition6467EvaluatedSlopes.csv', 'a')

    for linkPVID,_ in linkData.items():
        shapeInfo = linkData[linkPVID]
        refNode = shapeInfo[0]
        if refNode[2] == '' or linkPVID not in slopes:
            # only calculate slope if there is 3D data
            # and if there are a probe points for that link
            continue
        nRefNode = shapeInfo[-1]

        linkDistance = calcDistance(float(refNode[0]), float(refNode[1]), float(nRefNode[0]), float(nRefNode[1]))
        slope = findSlope(float(refNode[2]), float(nRefNode[2]), linkDistance)
        fileSlopes.write(linkPVID + ',' + slopes[linkPVID] + ',' + str(slope) + '\n')

    fileSlopes.close()
    print('Finished evaluation.')

def calcDistance(latStart, longStart, latEnd, longEnd):
    R = 6371e3
    latRadianStart = latStart * math.pi/180
    latRadianEnd = latEnd * math.pi/180
    deltaLatRadian = (latEnd-latStart) * math.pi/180
    deltaLongRadian = (longEnd-longStart) * math.pi/180

    a = math.sin(deltaLatRadian/2) * math.sin(deltaLatRadian/2) + math.cos(latRadianStart) * math.cos(latRadianEnd) * math.sin(deltaLongRadian/2) * math.sin(deltaLongRadian/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c; # in meters
    return abs(distance)

def findSlope(height1, height2, distance):
    deltaHeight = height2 - height1
    return math.atan(deltaHeight / distance) * (180 / math.pi)

if __name__ == '__main__':
    loadData()
