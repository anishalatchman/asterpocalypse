from Direction import Direction
from tkinter import PhotoImage

class Laser():
    def __init__(self, canvasArg, xArg = 2000, yArg = 1000, dirArg = Direction.EAST, timeArg = 50, speedArg = 20):
        self.__canvas = canvasArg
        self.__xPos = xArg
        self.__yPos = yArg
        self.__direction = dirArg
        self.__timeInterval = timeArg
        self.__speed = speedArg
        self.__photoLaser = PhotoImage(file = "images/laserbeam.png")
        self.__canvasWidth = self.__canvas.winfo_reqwidth()
        self.__canvasHeight = self.__canvas.winfo_reqheight()
        self.__isFired = False
        self.__timerID = None
        self.__imgLaser = self.__canvas.create_image(self.__xPos, self.__yPos, image = self.__photoLaser, anchor = "nw")
    
    def fire(self, dirArg, shipBounds):
        #Update direction
        self.__direction = dirArg
        
        if  self.__isFired == False:
            #Set initial laser position based on ship bounds and direction
            if self.__direction == Direction.EAST:
                self.__xPos = shipBounds[2] - 20
                self.__yPos = shipBounds[3] - 25
            elif self.__direction == Direction.WEST:
                self.__xPos = shipBounds[0] - self.__photoLaser.width() + 20
                self.__yPos = shipBounds[3] - 25
            self.__isFired = True
        
        #Shoot the laser depending on the direction
        if self.__direction == Direction.EAST:
            self.__xPos += self.__speed
        elif self.__direction == Direction.WEST:
            self.__xPos -= self.__speed
        
        #Update the location of the laser
        self.__canvas.coords(self.__imgLaser, self.__xPos, self.__yPos)
        self.__timerID = self.__canvas.after(self.__timeInterval, lambda: self.fire(dirArg, shipBounds)) 
        
    def hide(self):
        #Hide laser
        self.setLocation(self.__canvasWidth + 1000, self.__canvasHeight + 1000)
        
        #Cancel timer if the laser is active
        if self.__isFired == True:
            self.__canvas.after_cancel(self.__timerID)
            self.__isFired = False
            self.__moveCounter = 0
            
    def cancelTimer(self):
        if self.__timerID != None:
            self.__canvas.after_cancel(self.__timerID)
    
    def setX(self, xArg):
        self.__xPos = xArg
        self.__canvas.coords(self.__imgLaser, self.__xPos, self.__yPos)
    
    def setY(self, yArg):
        self.__yPos = yArg
        self.__canvas.coords(self.__imgLaser, self.__xPos, self.__yPos)
    
    def setLocation(self, xArg, yArg):
        self.__xPos = xArg
        self.__yPos = yArg
        self.__canvas.coords(self.__imgLaser, self.__xPos, self.__yPos)
    
    def setSpeed(self, speedArg):
        self.__speed = speedArg
        
    def getX(self):
        return self.__xPos
    
    def getY(self):
        return self.__yPos
    
    def getWidth(self):
        return self.__photoLaser.width()
    
    def getHeight(self):
        return self.__photoLaser.height()
    
    def getBoundaries(self):
        return self.__canvas.bbox(self.__imgLaser)
    
    def getSpeed(self):
        return self.__speed
    
    def getIsFired(self):
        return self.__isFired
    