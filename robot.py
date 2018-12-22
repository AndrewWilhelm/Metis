class Robot():
    def __init__(self,targetLoc,maxRows,maxCols, holesMapping, distrosMapping):
        self.hasPackage = False
        self.targetLocation = targetLoc
        self.speed = 1
        self.currentLocation = (0,0)
        self.distroLocation = (5,5)

        self.numRows = maxRows
        self.numColumns = maxCols

        self.holesMap = holesMapping
        self.distrosMap = distrosMapping

    def isOccupied(self,x,y):
        if (self.holesMap[x][y] != -1):
            print("There is a hole there!")
            return True
        if (self.distrosMap[x][y] != False):
            print("There is a distro there!")
            return True
        return False

    def calculatePath(self):
        filler = True

    def nextPosition(self):
        nextX, nextY = self.currentLocation
        targetX, targetY = self.targetLocation
        print(self.targetLocation)
        currentX, currentY = self.currentLocation
        if (currentX > targetX):
            if (not self.isOccupied(currentX-1,currentY) or (self.targetLocation == (currentX-1,currentY))):
                return(currentX-1,currentY)
        if (currentX < targetX):
            if (not self.isOccupied(currentX+1,currentY) or (self.targetLocation == (currentX+1,currentY))):
                return(currentX+1,currentY)
        if (currentY < targetY):
            if (not self.isOccupied(currentX,currentY+1) or (self.targetLocation == (currentX,currentY+1))):
                return(currentX,currentY+1)
        if (currentY > targetY):
            if (not self.isOccupied(currentX,currentY-1) or (self.targetLocation == (currentX,currentY-1))):
                return(currentX,currentY-1)
        return(currentX,currentY)

    def dropOffPackage(self):
        self.hasPackage = False
        self.targetLocation = self.distroLocation

    def pickUpPackage(self, targX, targY):
        self.hasPackage = True
        self.targetLocation = (targX, targY)

    def move(self):
        self.currentLocation = self.nextPosition()

        return self.currentLocation
        
        
