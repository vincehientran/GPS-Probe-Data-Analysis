
def loadData():
    #print('Start loading data.')
    fileLink = open('Partition6467LinkData.csv','r')

    counter = 0
    linesLinks = fileLink.readlines()
    for line in linesLinks:
        string = line[0:-1]
        linkRow = string.split(',')

        direction = linkRow[5]
        if direction == 'B':
            counter += 1

    fileLink.close()
    #print('Finished loading data.')
    print('\n' + str(counter) + ' roads are bidirectional out of 200,089.')

if __name__ == '__main__':
    loadData()
