import math
from ProbePoint import ProbePoint
import pygeohash as pgh

def loadData():
    fileLink = open('Partition6467LinkData.csv','r')

    print('Start loading data.')

    linesLink = fileLink.readlines()
    linkData = {}

    geohash6 = {}
    geohash5 = {}
    for line in linesLink:
        string = line[0:-1]
        linkRow = string.split(',')

        linkPVID = linkRow[0]
        if linkRow[-3] != '':
            shapeInfo = linkRow[-3].split('|')
            temp = []
            for shape in shapeInfo:
                temp.append(shape.split('/'))
            linkRow[-3] = temp
        rNode = linkRow[-3][0]
        shapeInfo = linkRow[-3]

        if linkRow[-1] != '':
            slopeInfo = linkRow[-1].split('|')
            temp = []
            for slope in slopeInfo:
                temp.append(slope.split('/'))
            linkRow[-1] = temp
        slopeInfo = linkRow[-1]

        linkData[linkPVID] = [shapeInfo,slopeInfo]

        # geohash precision 6
        areaGeohash6 = pgh.encode(float(rNode[0]), float(rNode[1]), precision=6)
        if areaGeohash6 in geohash6:
            geohash6[areaGeohash6].append(linkPVID)
        else:
            geohash6[areaGeohash6] = [linkPVID]

        # geohash precision 5
        areaGeohash5 = pgh.encode(float(rNode[0]), float(rNode[1]), precision=5)
        if areaGeohash5 in geohash5:
            geohash5[areaGeohash5].append(linkPVID)
        else:
            geohash5[areaGeohash5] = [linkPVID]
    print('Finished loading data.')
    fileLink.close()
    run(linkData, geohash5, geohash6)


def run(linkData, geohash5, geohash6):
    print('Start matching.')

    fileProbe = open('Partition6467ProbePoints.csv', 'r')
    fileWrite = open("MatchedResult.csv", "a")
    linesProbe = fileProbe.readlines()
    matchedCount = 0
    errors = 0

    for line in linesProbe:
        string = line[0:-1]
        probePoint = ProbePoint(string)

        areaGeohash6 = pgh.encode(float(probePoint.latitude), float(probePoint.longitude), precision=6)
        areaGeohash5 = pgh.encode(float(probePoint.latitude), float(probePoint.longitude), precision=5)
        candidates = []

        if areaGeohash6 in geohash6:
            candidates = geohash6[areaGeohash6]
        elif areaGeohash5 in geohash5:
            # zoom out, maybe we can get a refnode that exists in that area
            candidates = geohash5[areaGeohash5]
        else:
            probePoint.linkPVID = '62007637'
            probePoint.direction = 'F'
            probePoint.distFromRef = 0.0
            probePoint.distFromLink = 0.0
            fileWrite.write(str(probePoint) + '\n')

            matchedCount += 1
            if matchedCount % 100000 == 0:
                print('Matched ' + str(matchedCount) + ' probe points.')
            errors += 1

            continue

        minDistance = float('inf')
        minCandidate = None
        for candidate in candidates:
            link = linkData[candidate]
            shapeInfo = link[0]
            latRef = float(shapeInfo[0][0])
            longRef = float(shapeInfo[0][1])
            latNonRef = float(shapeInfo[-1][0])
            longNonRef = float(shapeInfo[-1][1])
            d2Ref = calcDistance(float(probePoint.latitude), float(probePoint.longitude), latRef, longRef)
            d2nRef = calcDistance(float(probePoint.latitude), float(probePoint.longitude), latNonRef, longNonRef)
            dRef2nRef = calcDistance(latRef, longRef, latNonRef, longNonRef)
            distance = calcDistFromLink(dRef2nRef, d2Ref, d2nRef)
            if d2Ref < (dRef2nRef * 1.2) and d2nRef < (dRef2nRef * 1.2) and distance < minDistance:
                minDistance = distance
                minCandidate = candidate

        if not minCandidate:
            minDistance = float('inf')
            minCandidate = None
            for candidate in candidates:
                link = linkData[candidate]
                shapeInfo = link[0]
                latRef = float(shapeInfo[0][0])
                longRef = float(shapeInfo[0][1])
                latNonRef = float(shapeInfo[-1][0])
                longNonRef = float(shapeInfo[-1][1])
                d2Ref = calcDistance(float(probePoint.latitude), float(probePoint.longitude), latRef, longRef)
                d2nRef = calcDistance(float(probePoint.latitude), float(probePoint.longitude), latNonRef, longNonRef)
                dRef2nRef = calcDistance(latRef, longRef, latNonRef, longNonRef)
                distance = calcDistFromLink(dRef2nRef, d2Ref, d2nRef)
                if distance < minDistance:
                    minDistance = distance
                    minCandidate = candidate

        link = linkData[minCandidate]
        shapeInfo = link[0]
        latRef = float(shapeInfo[0][0])
        longRef = float(shapeInfo[0][1])
        latNonRef = float(shapeInfo[-1][0])
        longNonRef = float(shapeInfo[-1][1])
        heading = linkHeading(latRef, longRef, latNonRef, longNonRef)
        probePoint.linkPVID = minCandidate
        diff = abs(float(probePoint.heading) -  heading)
        if diff > 180:
            diff = 360 - diff
        if diff > 90:
            # towards from ref Node
            probePoint.direction = 'T'
        else:
            # away from ref Node
            probePoint.direction = 'F'
        probePoint.distFromRef = calcDistance(float(probePoint.latitude), float(probePoint.longitude), latRef, longRef)
        probePoint.distFromLink = minDistance

        fileWrite.write(str(probePoint) + '\n')

        matchedCount += 1
        if matchedCount % 100000 == 0:
            print('Matched ' + str(matchedCount) + ' probe points.')

    fileProbe.close()
    fileWrite.close()

    print('Finished matching.')

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

def calcDistFromLink(distRef2NonRef, distPoint2Ref, distPoint2NonRef):
    if distPoint2Ref == 0 or distRef2NonRef == 0 or distPoint2NonRef == 0:
        return 0

    semiperimeter = (distPoint2Ref + distRef2NonRef + distPoint2NonRef) / 2
    area = math.sqrt(semiperimeter * (semiperimeter - distPoint2Ref) * (semiperimeter - distRef2NonRef) * (semiperimeter - distPoint2NonRef) )

    return (2*area)/distRef2NonRef

def linkHeading(startLat, startLong, endLat, endLong):
    startLat = startLat * math.pi/180
    startLong = startLong * math.pi/180
    endLat = endLat * math.pi/180
    endLong = endLong * math.pi/180

    x = math.cos(endLat) * math.sin(endLong - startLong)
    y = (math.cos(startLat) * math.sin(endLat)) - (math.sin(startLat) * math.cos(endLat) * math.cos(endLong - startLong))

    heading = math.atan2(x,y)
    heading = heading * (180 / math.pi)
    if heading < 0 :
        heading = 360 + heading
    return heading

if __name__ == '__main__':
    #calcDistance(51.9844299,9.2704199,51.9844699,9.2698900)
    '''d = calcDistance(51.496868217364, 9.38602223061025, 51.4965800, 9.3862299)
    print(d)
    h = linkHeading(51.496868217364, 9.38602223061025, 51.49555901643563, 9.385918378829958)
    print(h)'''
    loadData()
