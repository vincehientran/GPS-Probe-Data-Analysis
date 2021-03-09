import math

def main():
    fileProbe = open('Partition6467ProbePoints.csv', 'r')
    fileLink = open('Partition6467LinkData.csv','r')

    linesProbe = fileProbe.readlines()
    probeData = {}
    for line in linesProbe:
        string = line[0:-1]
        probeRow = string.split(',')
        sampleID = probeRow[0]
        if sampleID not in probeData:
            probeData[sampleID] = [probeRow]
        else:
            probeData[sampleID].append(probeRow)

    linesLink = fileLink.readlines()
    linkData = []

    for line in linesLink:
        string = line[0:-1]
        linkRow = string.split(',')

        if linkRow[-3] != '':
            shapeInfo = linkRow[-3].split('|')
            temp = []
            for shape in shapeInfo:
                temp.append(shape.split('/'))
            linkRow[-3] = temp

        if linkRow[-2] != '':
            curvatureInfo = linkRow[-2].split('|')
            temp = []
            for curvature in curvatureInfo:
                temp.append(curvature.split('/'))
            linkRow[-2] = temp

        if linkRow[-1] != '':
            slopeInfo = linkRow[-1].split('|')
            temp = []
            for slope in slopeInfo:
                temp.append(slope.split('/'))
            linkRow[-1] = temp

        linkData.append(linkRow)

    print('Finished reading data.')
    run(probeData, linkData)


def run(probeData, linkData):
    print(len(probeData), len(linkData))

    # each sampleID is a different path
    # paths is a dictionary with key of sampleIDs and values of the probe points from that sampleID
    vals = []
    count = 0
    for k,v in probeData.items():
        lat = float(probeData[k][0][3])
        long = float(probeData[k][0][4])
        minDistance = float('inf')
        minLink = None
        for i in range(len(linkData)):
            linkLat = float(linkData[i][14][0][0])
            linkLong = float(linkData[i][14][0][1])
            distance = calcDistance(lat,long,linkLat,linkLong)
            if minDistance > distance:
                minDistance = distance
                minLink = i
        vals.append(minDistance)
        count += 1
        if count > 10:
            break
    print(vals)


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

if __name__ == '__main__':
    #calcDistance(51.9844299,9.2704199,51.9844699,9.2698900)
    main()
