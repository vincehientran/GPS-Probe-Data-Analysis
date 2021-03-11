import math

def loadData():
    print('Start loading data.')
    filePoints = open('Partition6467MatchedPoints.csv', 'r')
    fileLink = open('Partition6467LinkData.csv','r')

    # key: linkPVID
    # value: list of (distance, altitude) on that link
    altitudes = {}

    linesLink = fileLink.readlines()
    for line in linesLink:
        string = line[0:-1]
        linkRow = string.split(',')
        linkPVID = linkRow[0]
        altitudes[linkPVID] = []

    linesPoints = filePoints.readlines()
    for line in linesPoints:
        string = line[0:-1]
        pointRow = string.split(',')

        linkPVID = pointRow[8]
        distance = float(pointRow[10])
        altitude = float(pointRow[5])

        altitudes[linkPVID].append((distance, altitude))

    filePoints.close()
    fileLink.close()
    print('Finished loading data.')
    run(altitudes)

def run(altitudes):
    print('Start finding slopes.')
    filePoints = open('Partition6467DerivedSlopes.csv', 'a')

    for linkPVID,_ in altitudes.items():
        # no slope for just 1 point
        if (len(altitudes[linkPVID]) > 1):
            lst = sorted(altitudes[linkPVID])
            distance1 = lst[0][0]
            distance2 = lst[-1][0]
            if distance1 == distance2:
                # no slope for 2 identical points
                continue
            height1 = lst[0][1]
            height2 = lst[-1][1]
            slope = findSlope(height1, height2, distance1, distance2)
            filePoints.write(linkPVID + ',' + str(slope) + '\n')

    filePoints.close()
    print('Finished finding slopes.')

def findSlope(height1, height2, distance1, distance2):
    deltaHeight = height2 - height1
    deltaDistance = distance2 - distance1

    return math.atan(deltaHeight / deltaDistance) * (180 / math.pi)

if __name__ == '__main__':
    loadData()
