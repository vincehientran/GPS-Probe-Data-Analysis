
class ProbePoint(object):
    def __init__(self, row):
        values = row.split(',')

        self.sampleID = values[0]
        self.dateTime = values[1]
        self.sourceCode = values[2]
        self.latitude = values[3]
        self.longitude = values[4]
        self.altitude = values[5]
        self.speed = values[6]
        self.heading = values[7]

        self.linkPVID = None
        self.direction = None
        self.distFromRef = None
        self.distFromLink = None

    def __str__(self):
        return self.sampleID + ',' + self.dateTime + ',' + self.sourceCode + ',' + self.latitude + ',' + self.longitude + ',' + self.altitude + ',' + self.speed + ',' + self.heading + ',' + self.linkPVID + ',' + self.direction + ',' + str(self.distFromRef) + ',' + str(self.distFromLink)
