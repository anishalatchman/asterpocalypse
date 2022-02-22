from Direction import Direction
from tkinter import PhotoImage

class Ship():
    def __init__(self, canvasArg):
        #declare class variables
        self.__canvas = canvasArg
        self.__xPos = 10
        self.__yPos = 282
        self.__shipDir = Direction.EAST
        self.__health = 10
        self.__listShips = [PhotoImage(file = "images/spaceship_west.png"), 
                            PhotoImage(file = "images/spaceship_east.png"), PhotoImage(file = "images/exploded_ship.png")]
        self.__currentShip = self.__listShips[1]
        self.__imgShip = self.__canvas.create_image(self.__xPos, self.__yPos, image = self.__currentShip, anchor = "nw")
        self.__shipWidth = self.__currentShip.width()
        self.__shipHeight = self.__currentShip.height()
        self.__explodeID = None
        
    def move(self, x = 0, y = 0):
        #update x and y position of ship
        self.__xPos += x
        self.__yPos += y
        #update direction of current ship image
#         self.__currentShip = self.__listShips[self.__shipDir.value]
#         self.__canvas.itemconfig(self.__imgShip, image = self.__currentShip)
        #set new canvas coordinates
        self.__canvas.coords(self.__imgShip, self.__xPos, self.__yPos)
        
    def explode(self):
        #show exploded ship image
        self.__currentShip = self.__listShips[2]
        self.__canvas.itemconfig(self.__imgShip, image = self.__currentShip) 
#         self.__explodeID = self.__canvas.after(1000, self.reset)
        
    def reset(self):
#         self.__canvas.after_cancel(self.__explodeID)
        self.__currentShip = self.__listShips[1]
        self.__canvas.itemconfig(self.__imgShip, image = self.__currentShip)         
        
    def getX(self):
        return self.__xPos
    
    def getY(self):
        return self.__yPos
    
    def getWidth(self):
        return self.__currentShip.width()
    
    def getHeight(self):
        return self.__currentShip.height()
    
    def getXSpeed(self):
        return self.__XSpeed
    
    def getYSpeed(self):
        return self.__YSpeed
    
    def getDirection(self):
        return self.__shipDir
    
    def getBoundaries(self):
        #return [left, top, right, bottom]
        return self.__canvas.bbox(self.__imgShip)
    
    def getPhotoImage(self):
        return self.__currentShip
    
    def setX(self, xArg):
        self.__xPos = xArg
        self.__canvas.coords(self.__imgShip, self.__xPos, self.__yPos)
    
    def setY(self, yArg):
        self.__yPos = yArg
        self.__canvas.coords(self.__imgShip, self.__xPos, self.__yPos)
    
    def setXSpeed(self, xSpeedArg):
        self.__XSpeed = xSpeedArg
        
    def setYSpeed(self, ySpeedArg):
        self.__ySpeed = ySpeedArg
    
    def setLocation(self, xArg, yArg):
        self.__xPos = xArg
        self.__yPos = yArg
        self.__canvas.coords(self.__imgShip, self.__xPos, self.__yPos)
    
    def setDirection(self, dirArg):
        self.__shipDir = dirArg
        self.setPhotoImage(self.__listShips[dirArg.value])
        
    def setPhotoImage(self, photoArg):
        self.__currentShip = photoArg
        self.__canvas.itemconfig(self.__imgShip, image = self.__currentShip)
        