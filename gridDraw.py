import Tkinter as tk
import random
import robot

#Create branch to investigate the necessary components of the GUI
#Would probably be easier if there was a list of distro locations...
#Known bug where if a hole is located to the left of the distro, then the robot will get stuck
#Might also affect if the hole is above the distro

SIM_DELAY = 500; #The delay, in milliseconds, between simulation cycles

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
	self.title('Metis')
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

#Draw the distribution center (colored red)
        x,y = self.distroLocation
        x1 = x*self.cellwidth
        y1 = y * self.cellheight
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight

        self.distros[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="red", tags="distro")
        self.distros[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="red", tags="distro")

#Draw the drop-off locations (a.k.a. holes) as blue
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

#Draw the robots (blue circles with status icons)
        self.robot = robot.Robot(self.distroLocation,self.numRows,self.numColumns,self.holesMap,self.distrosMap)
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
        self.redraw(SIM_DELAY)


    def colorRobot(self,x,y,hasPackage):

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
        x,y = self.distroLocation
        x1 = x*self.cellwidth
        y1 = y * self.cellheight
        x2 = x1 + self.cellwidth
        y2 = y1 + self.cellheight

        self.distros[x,y] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="red", tags="distro")
        self.distros[x,y] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="red", tags="distro")

    def colorHoles(self):
	holesList = []
	for r in range(self.numRows):
		for c in range(self.numColumns):
			if self.holesMap[r][c] != -1:
				holesList.append((r,c))

        for (row,column) in holesList:
                
            x1 = column*self.cellwidth
            y1 = row * self.cellheight
            x2 = x1 + self.cellwidth
            y2 = y1 + self.cellheight
            self.holes[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="hole")
            self.holes[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="hole")
            #self.holesMap[row][column] = number1



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
        holeX, holeY = -1,-1
        for i in range(len(self.holesMap)):
            for j in range(len(self.holesMap[0])):
                if (self.holesMap[i][j] == holeNum):
                    holeX = i
                    holeY = j
        return (holeX, holeY)
            

    def redraw(self, delay):

        for column in range(self.numColumns):
            for row in range(self.numRows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="white", tags="rect")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="black", tags="oval")

        distroX, distroY = self.distroLocation
        self.colorDistro(distroX,distroY)

        self.colorHoles()

        self.checkRobots()
        self.colorAllRobots()


        self.after(delay, lambda: self.redraw(delay))
        


if __name__ == "__main__":
    app = App()
    app.mainloop()
