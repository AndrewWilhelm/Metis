import Tkinter as tk
import random
import robot

'''NOTE: Currently the robot detects that there is a hole where it is moving, but it chooses to walk right through it...
    It may be a problem with the decision structure in the robot class'''

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 100
        self.columns = 100
        self.cellwidth = 25
        self.cellheight = 25
        self.numColumns = 20
        self.numRows = 20
        self.numHoles = 3


        self.holesMap = [[-1 for x in range(self.numColumns)] for y in range(self.numRows)]
        self.distrosMap = [[False for x in range(self.numColumns)] for y in range(self.numRows)]

        self.distroLocation = (5,5)
        self.distrosMap[5][5] = True
        #self.distrosMap[3][0] = True

        self.rect = {}
        self.robots = {}
        self.oval = {}
        self.innerOval = {}
        self.holes = {}
        self.distros = {}

        for column in range(self.numColumns):
            for row in range(self.numRows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval")
                #self.innerOval[row,column] = self.canvas.create_oval(x1+10,y1+10,x2-10,y2-10, fill="red", tags="oval")

        x,y = self.distroLocation
        x1 = x*self.cellwidth
        y1 = y * self.cellheight
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight
        self.distros[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="red", tags="distro")
        self.distros[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="red", tags="distro")

        for number1 in range(self.numHoles):
            column = random.randint(0,self.numColumns - 1)
            row = random.randint(0,self.numRows - 1)
            nein1, nein2 = self.distroLocation
            while((row == nein1 and column == nein2) or (row == 0 and column == 0)):
                column = random.randint(0,self.numColumns - 1)
                row = random.randint(0,self.numRows - 1)
                
            x1 = column*self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.holes[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="hole")
            self.holes[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="hole")
            self.holesMap[row][column] = number1

        self.robot = robot.Robot(self.getRandomHoleLoc(),self.numRows,self.numColumns,self.holesMap,self.distrosMap)
        self.robotList = [self.robot]

        for robotic in self.robotList:
            row, column = robotic.currentLocation
            x1 = column*self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.robots[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="robot")
            self.innerOval[row,column] = self.canvas.create_oval(x1+10,y1+10,x2-10,y2-10, fill="red", tags="oval")

        self.count = 0;
        self.redraw(500)

    '''def isOccupied(self,x,y):
        if (self.holesMap[x][y] == -1):
            print("There is a hole there!")
        if (self.distrosMap[x][y] != False):
            print("There is a distro there!")'''


    def colorRobot(self,x,y,hasPackage):
        '''item_id = self.oval[x,y]
        self.canvas.itemconfig(item_id, fill="green")
        item_id = self.innerOval[x,y]
        if (hasPackage):
            self.canvas.itemconfig(item_id, fill="yellow")
        else:
            self.canvas.itemconfig(item_id, fill="red")'''

        row, column = x,y
        x1 = column*self.cellwidth
        y1 = row * self.cellheight
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight
        self.robots[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="robot")
        self.innerOval[row,column] = self.canvas.create_oval(x1+10,y1+10,x2-10,y2-10, fill="red", tags="oval")

        item_id = self.innerOval[x,y]
        if (hasPackage):
            self.innerOval[row,column] = self.canvas.create_oval(x1+10,y1+10,x2-10,y2-10, fill="yellow", tags="oval")
        else:
            self.innerOval[row,column] = self.canvas.create_oval(x1+10,y1+10,x2-10,y2-10, fill="red", tags="oval")

    def colorAllRobots(self):
        for robot in self.robotList:
            drawX, drawY = self.robot.move()
            self.colorRobot(drawX,drawY,robot.hasPackage)


    def colorDistro(self,x,y):
        self.canvas.itemconfig("distro", fill="red")

    def colorHoles(self):
        self.canvas.itemconfig("hole", fill = "blue")

    def checkRobots(self):
        for robot in self.robotList:
            if (robot.currentLocation == robot.targetLocation):
                if (robot.hasPackage):
                    #assume that the robot is now on the correct drop off hole
                    robot.dropOffPackage()
                else:
                    #assume that the robot must need to pick up a new package
                    holeX, holeY = self.getRandomHoleLoc()
                    robot.pickUpPackage(holeX, holeY)

    #returns a random hole location has a tuple (returns -1,-1 if something fails)
    def getRandomHoleLoc(self):
        holeNum = random.randint(0,self.numHoles - 1)
        print "Hole num is ",holeNum
        holeX, holeY = -1,-1
        for i in range(len(self.holesMap)):
            for j in range(len(self.holesMap[0])):
                if (self.holesMap[i][j] == holeNum):
                    holeX = i
                    holeY = j
        return (holeX, holeY)
            

    def redraw(self, delay):
        self.canvas.itemconfig("rect", fill="white")
        self.canvas.itemconfig("oval", fill="black")

        self.checkRobots()
        self.colorAllRobots()

        distroX, distroY = self.distroLocation
        self.colorDistro(distroX,distroY)

        self.colorHoles()

        self.after(delay, lambda: self.redraw(delay))
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
