from tkinter import Tk, Canvas, PhotoImage, messagebox
from Direction import Direction
from ShipClass import Ship
from AsteroidClass import Asteroid
from LaserClass import Laser
import random
import pygame


def exit_program():
    # pause movement
    pauseGame()
    answer = messagebox.askyesno("Are You Sure?", "Are you sure you want to quit?")
    if answer:
        exit()
    elif not answer:
        # resume movement
        unPauseGame()


def playSound(indexAudio):
    # Play audio of corresponding index
    pygame.mixer.Sound.play(sound_effects[indexAudio])


def pauseGame():
    # stop all timers/movements
    root.after_cancel(btid)
    canvas.after_cancel(collisionID)
    for asteroid in listAsteroid:
        asteroid.cancelTimer()
    canvas.after_cancel(asteroidID)
    for laser in listLaser:
        laser.cancelTimer()


def unPauseGame():
    checkCollision()
    background_timer()

    for asteroid in listAsteroid:
        if asteroid.getX() <= canvasWidth:
            # resume movement of each asteroid within canvas
            asteroid.move()
    for laser in listLaser:
        if laser.getX() <= canvasWidth and laser.getBoundaries()[2] >= 0:
            # resume movement of each laser within canvas
            laser.fire(ship.getDirection(), ship.getBoundaries())

            # resume asteroid movement
    asteroid_timer()


def background_timer():
    global btid
    for i in range(len(background_list)):
        canvas.coords(background_list[i], xpos[i] - 5, 0)
        xpos[i] -= 5

    btid = root.after(50, lambda: background_timer())

    if xpos[0] + imgBackground.width() <= 0:
        xpos[0] = xpos[1] + imgBackground.width()
    if xpos[1] + imgBackground.width() <= 0:
        xpos[1] = xpos[0] + imgBackground.width()


def spacePress(event):
    global laserCounter

    # Reset index of lasers
    if laserCounter > 19:
        laserCounter = 0

    if listLaser[laserCounter].getIsFired() == False:
        if laserCounter == 0:
            # fire each laser if it is not yet fired
            listLaser[laserCounter].fire(ship.getDirection(), ship.getBoundaries())
        elif listLaser[laserCounter - 1].getBoundaries()[0] >= 60:
            listLaser[laserCounter].fire(ship.getDirection(), ship.getBoundaries())

    # Increase laser counter play audio effect
    laserCounter += 1
    playSound(1)


def mouseMove(event):
    global ship, prevShipX
    #     offBounds = False
    #     #check for off bounds and move ship
    #     if event.x + ship.getWidth() // 2 >= canvas.winfo_reqwidth():
    #         offBounds = True
    #         ship.setX(canvas.winfo_reqwidth())
    #     if event.x - ship.getWidth() // 2 <= 0:
    #         offBounds = True
    #         ship.setX(0)
    #     if event.y - ship.getHeight() // 2 <= 60:
    #         offBounds = True
    #         ship.setY(60)
    #     if event.y + ship.getHeight() // 2 <= canvas.winfo_reqheight():
    #         offBounds = True
    #         ship.setY(canvas.winfo_reqheight())

    #     if not offBounds:
    ship.setLocation(event.x - ship.getWidth() // 2, event.y - ship.getHeight() // 2)
    if event.x >= prevShipX:
        # change ship image to east
        ship.setDirection(Direction.EAST)
    elif event.x <= prevShipX:
        # change ship image to west
        ship.setDirection(Direction.WEST)
    prevShipX = event.x


def keyPress(event):
    global ship
    # move ship according to keyboard presses
    if ship.getBoundaries()[2] < canvas.winfo_reqwidth() and (
            event.char == 'd' or event.char == 'D' or event.keysym == "Right"):
        ship.setDirection(Direction.EAST)
        # move right if ship is on canvas bounds
        ship.move(x=5)
    if ship.getX() > 0 and (event.char == 'a' or event.char == 'A' or event.keysym == "Left"):
        ship.setDirection(Direction.WEST)
        # move left if ship is on canvas bounds
        ship.move(x=-5)
    if ship.getY() > 80 and (event.char == 'w' or event.char == 'W' or event.keysym == "Up"):
        # move up if ship is on canvas bounds
        ship.move(y=-5)
    if ship.getBoundaries()[3] < canvas.winfo_reqheight() and (
            event.char == 's' or event.char == 'S' or event.keysym == "Down"):
        # move down if ship is on canvas bounds
        ship.move(y=5)


def asteroid_timer():
    global asteroidID, asteroidCounter, canvasWidth, canvasHeight, timeInterval
    # Reset index of asteroids
    if asteroidCounter > 19:
        asteroidCounter = 0

    # Set initial location to right side of screen, with a random yPos value between 50 and height of canvas - the height of the image
    yPos = random.randint(50, (canvasHeight - listAsteroid[asteroidCounter].getHeight()) // 1)
    listAsteroid[asteroidCounter].setLocation(canvasWidth, yPos)

    # Begin asteroid movement
    listAsteroid[asteroidCounter].move()

    # Increase counter
    asteroidCounter += 1

    # Display asteroid every 2 seconds
    asteroidID = canvas.after(2000, asteroid_timer)


def checkCollision():
    global collisionID
    # Get the boundaries of the ship
    shipBoundaries = ship.getBoundaries()

    # Cycle through the boundaries of every asteroid
    for asteroid in listAsteroid:
        asteroidBoundaries = asteroid.getBoundaries()

        # Check ship to asteroid collision
        if shipBoundaries[2] >= asteroidBoundaries[0] and shipBoundaries[0] <= asteroidBoundaries[
            2] and updatedLives == False:
            if shipBoundaries[3] >= asteroidBoundaries[1] and shipBoundaries[1] <= asteroidBoundaries[3]:
                ship.explode()
                playSound(2)
                pauseGame()
                updateLives()
                # break out of function and resume game
                return unPauseGame()

        # check for asteroid off screen
        if asteroidBoundaries[2] <= 0:
            asteroid.hide()
            # decrease health by one
            pauseGame()
            updateHealth()
            # break out of function and resume game
            return unPauseGame()

        # Cycle through the boundaries of every laser
        for laser in listLaser:
            laserBoundaries = laser.getBoundaries()

            # Check laser to asteroid collision
            if asteroidBoundaries[2] >= laserBoundaries[0] and asteroidBoundaries[0] <= laserBoundaries[
                2] and asteroid.getIsActive() == True:
                if asteroidBoundaries[3] >= laserBoundaries[1] and asteroidBoundaries[1] <= laserBoundaries[3]:
                    asteroid.explode()
                    playSound(3)
                    laser.hide()
                    updatePoints()

                    # check for laser off screen
            if laserBoundaries[2] >= canvas.winfo_reqwidth() or laserBoundaries[0] <= 0:
                laser.hide()

                # Check for collision every 1 milisecond
    collisionID = canvas.after(1, checkCollision)


def updateHealth():
    global health
    # Decrease health by one and update the health bar
    health -= 1
    photoHealth = listHealth[health]
    canvas.itemconfig(imgHealth, image=photoHealth)
    if health == 0:
        #         canvas.after(1000, updateLives)
        updateLives()


def updateLives():
    global lives, updatedLives
    updatedLives = True
    lives -= 1
    # Decrease lives by one and update number of lives
    if lives == 0:
        photoHealth = listHealth[0]
        canvas.itemconfig(imgHealth, image=photoHealth)
    photoLives = listLives[lives]
    canvas.itemconfig(imgLives, image=photoLives)

    # Display a message informing the user of their current number
    answer = messagebox.showinfo("Lost Life", "You're dead! You have " + str(lives) + " lives remaining.")

    # If the user runs out of lives,
    if lives == 0:
        playSound(5)
        answer = messagebox.askyesno("Game Over",
                                     "You finished with " + str(points) + " points. \nWould you like to play again?")
        if answer == True:
            reset(True)
        else:
            exit()
    else:
        # Reset screen
        reset(False)


def updatePoints():
    global points, level
    # add 10 points for every asteroid shrink
    points += 10
    canvas.itemconfig(pointsTxt, text=str(points))

    if points % 100 == 0:
        level += 1
        updateLevel()
        if level <= 5:
            for asteroid in listAsteroid:
                asteroid.decreaseInterval(20)


def updateLevel():
    global level
    playSound(4)
    # Display updated level
    canvas.itemconfig(levelTxt, text="Level " + str(level))


def reset(newGame):
    global asteroidID, health, points, lives, prevShipX, asteroidCounter, laserCounter, level, updatedLives
    updatedLives = False

    # Hide all of the lasers and asteroids
    for laser in listLaser:
        laser.hide()

    for asteroid in listAsteroid:
        asteroid.hide()

    # Reset health bar
    health = 10
    photoHealth = listHealth[health]
    canvas.itemconfig(imgHealth, image=photoHealth)

    # Reset ship location
    ship.reset()
    ship.setLocation(10, 282)

    # Reset the whole game
    if newGame == True:
        # reset variables to default values
        points = 0
        lives = 3
        prevShipX = 0
        asteroidCounter = 0
        laserCounter = 0
        level = 1
        # reset points
        canvas.itemconfig(pointsTxt, text=str(points))
        # reset lives images
        photoLives = listLives[3]
        canvas.itemconfig(imgLives, image=photoLives)
        # Update level
        updateLevel()
        # Reset asteroid speeds
        for asteroid in listAsteroid:
            asteroid.setTimeInterval(100)


# Declare default variables and lists
listHealth = [0] * 11
health = 10
points = 0
lives = 3
level = 1
prevShipX = 0
updatedLives = False

asteroidCounter = 0
laserCounter = 0
asteroidInterval = 3000

asteroidID = None
btid = None

root = Tk()
root.title('Asterpocalypse')
root.protocol('WM_DELETE_WINDOW', exit_program)
# root.bind("<ButtonPress>", mouseMove)
root.bind("<KeyPress>", keyPress)
root.bind("<space>", spacePress)
root.bind("<Motion>", mouseMove)

imgBackground = PhotoImage(file='images/space_background.png')
imgTitle = PhotoImage(file='images/asterpocalypse_title.png')

root.geometry("%dx%d+%d+%d" % (
imgBackground.width(), imgBackground.height(), root.winfo_screenwidth() // 2 - imgBackground.width() // 2,
root.winfo_screenheight() // 2 - imgBackground.height() // 2))

canvas = Canvas(root, width=imgBackground.width(), height=imgBackground.height())
canvas.pack()

background_list = [0] * 2
xpos = [0, imgBackground.width()]

for i in range(len(background_list)):
    background_list[i] = canvas.create_image(xpos[i], 0, image=imgBackground, anchor='nw')

listHealth = [0] * 11
for num in range(len(listHealth)):
    # Create list of health photo images
    listHealth[num] = PhotoImage(file="images/health" + str(num) + ".png")

listLives = [0] * 4
for indexLives in range(len(listLives)):
    listLives[indexLives] = PhotoImage(file="images/lives" + str(indexLives) + ".png")

listAsteroid = [0] * 20
for indexAsteroid in range(len(listAsteroid)):
    # Initialize a list of 20 asteroids of varying sizes
    size = random.randint(0, 2)
    listAsteroid[indexAsteroid] = Asteroid(canvas, size)
    # Hide Asteroid
    listAsteroid[indexAsteroid].hide()

ship = Ship(canvas)

listLaser = [0] * 20
for indexLaser in range(len(listLaser)):
    # Initialize a list of 20 lasers (ship's magazine)
    listLaser[indexLaser] = Laser(canvas)
    # Hide Laser
    listLaser[indexLaser].hide()

# Create health image on canvas
photoHealth = listHealth[health]
imgHealth = canvas.create_image(canvas.winfo_reqwidth() - photoHealth.width() - 20, 20, image=photoHealth, anchor="nw")

# Create lives image on canvas
photoLives = listLives[lives]
imgLives = canvas.create_image(canvas.winfo_reqwidth() - photoLives.width() - 30, photoHealth.height() + 30,
                               image=photoLives, anchor="nw")

# create points text on canvas
pointsTxt = canvas.create_text(120, 50, text=str(points), font=("neuropol", 32), fill="orange")

# Create and display title
canvas.create_image(canvas.winfo_reqwidth() // 2 - imgTitle.width() // 2, 10, image=imgTitle, anchor='nw')

# Create and display game level
levelTxt = canvas.create_text(canvas.winfo_reqwidth() - 160, canvas.winfo_reqheight() - 50,
                              text="Level " + str(level), font=("neuropol", 20), fill="orange", anchor="nw")

# Initialize pygame mixer
pygame.mixer.init()

# Create a list of sound effects (bgMusic = 0, laser = 1, ship explosion, asteroid explosion = 3, level up = 4, game over = 5)
listAudio = ["audio/bgMusic.wav", "audio/laser.wav", "audio/shipExplosion.wav",
             "audio/asteroidExplosion.wav", "audio/levelup.wav", "audio/gameOver.wav"]
sound_effects = [0] * 6
for indexAudio in range(1, len(listAudio)):
    sound_effects[indexAudio] = pygame.mixer.Sound(listAudio[indexAudio])

# play background music
pygame.mixer.music.load(listAudio[0])
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Get canvas width and height
canvasWidth = canvas.winfo_reqwidth()
canvasHeight = canvas.winfo_reqheight()

# Run game
asteroid_timer()
checkCollision()
background_timer()
root.mainloop()
