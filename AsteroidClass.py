from tkinter import PhotoImage
import random

class Asteroid():
    
    def __init__(self, canvasArg, sizeArg = 0, xArg = 0, yArg = 0, timeArg = 100, pointsArg = 10, speedArg = 5):
        
        self.__canvas = canvasArg
        self.__numSize = sizeArg
        self.__xPos = xArg
        self.__yPos = yArg
        self.__timeInterval = timeArg
        self.__points = pointsArg
        self.__speed = speedArg
        self.__timerID = None
        self.__isActive = True
        
        self.__listAsteroid = [PhotoImage(file = "images/asteroid0.png"), PhotoImage(file = "images/asteroid1.png"), 
                               PhotoImage(file = "images/asteroid2.png")]
        self.__listExplosion = [PhotoImage(file = "images/explosion0.png"), PhotoImage(file = "images/explosion1.png"), 
                               PhotoImage(file = "images/explosion2.png")]
        self.__currentAsteroid = self.__listAsteroid[self.__numSize]
        
        self.__imgAsteroid = self.__canvas.create_image(self.__xPos, self.__yPos, image = self.__currentAsteroid, anchor = "nw")
    
    def move(self):
        #Asteroid movement restricted: East to West, 10 pixels per step
        self.__xPos -= 10
            
        #Update location of the asteroid
        self.__canvas.coords(self.__imgAsteroid, self.__xPos, self.__yPos)
        self.__timerID = self.__canvas.after(self.__timeInterval, self.move)
            
    def explode(self):
        self.__isActive = False
        #Display explosion animation and audio effects
        self.__canvas.itemconfig(self.__imgAsteroid, image = self.__listExplosion[self.__numSize])
        #ADD AUDIO
        #Shrink after 200 milisecond
        self.__explosionID = self.__canvas.after(200, self.shrink)

    def shrink(self):
        #If the smallest size is blown up, delete the image
        self.__numSize -= 1
        if self.__numSize >= 0:
            self.__canvas.itemconfig(self.__imgAsteroid, image = self.__listAsteroid[self.__numSize])
            self.__yPos += ((self.__listAsteroid[self.__numSize + 1].height() - self.__listAsteroid[self.__numSize].height()) // 2)
            self.__canvas.coords(self.__imgAsteroid, self.__xPos, self.__yPos)
        else:
            self.hide()
            self.reset()
        self.__isActive = True
    
    def hide(self):
        #Hide asteroid
        self.setLocation(self.__canvas.winfo_reqwidth() + 2000, self.__canvas.winfo_reqheight() + 2000)
        
        #Cancel timer if the laser is active
        if self.__timerID != None:
            self.__timerID = self.__canvas.after_cancel(self.__timerID)
            
    def cancelTimer(self):
        if self.__timerID != None:
            self.__timerID = self.__canvas.after_cancel(self.__timerID)
            
    def reset(self):
        #Reset asteroid to a random size
        self.__numSize = random.randint(0, 2)
        self.__canvas.itemconfig(self.__imgAsteroid, image = self.__listAsteroid[self.__numSize])
        
    def setX(self, xArg):
        self.__xPos = xArg
        self.__canvas.coords(self.__imgAsteroid, self.__xPos, self.__yPos)
    
    def setY(self, yArg):
        self.__yPos = yArg
        self.__canvas.coords(self.__imgAsteroid, self.__xPos, self.__yPos)
    
    def setLocation(self, xArg, yArg):
        self.__xPos = xArg
        self.__yPos = yArg
        self.__canvas.coords(self.__imgAsteroid, self.__xPos, self.__yPos)
    
    def setSpeed(self, speedArg):
        self.__speed = speedArg
        
    def decreaseInterval(self, timeArg):
        self.__timeInterval -= timeArg
    
    def setTimeInterval(self, timeArg):
        self.__timeInterval = timeArg
    
    def getX(self):
        return self.__xPos
    
    def getY(self):
        return self.__yPos
    
    def getWidth(self):
        return self.__currentAsteroid.width()
    
    def getHeight(self):
        return self.__currentAsteroid.height()
    
    def getBoundaries(self):
        #Return a tuple of the boundaries of the image
        return self.__canvas.bbox(self.__imgAsteroid)

    def getSpeed(self):
        return self.__speed
    
    def getPoints(self):
        return self.__points
    
    def getDirection(self):
        return self.__direction
    
    def getIsActive(self):
        return self.__isActive
    
    def setIsActive(self, active):
        self.__isActive = active
    