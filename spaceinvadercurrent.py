
# Momin Qadri
# CS-UY 1114
# Final project

import turtle
import time

# This variable store the horizontal position
# of the player's ship. It will be adjusted
# when the user press left and right keys, and
# will be used by the draw_frame() function to draw
# the ship. The ship never moves vertically, so
# we don't need a variable to store its y position.
userx = -20

# This variable is a list of enemies currently in
# the game. Each enemy is represented by a tuple
# containing its x,y position as well as a string
# indicated the enemy's current direction of travel
# (either left or right). 
# Your final game should include more enemies, although
# the exact arrangement is up to you.
enemies = [(200,-50, "left"),(0, -50, "right"),(-200,-50,'right'),(250,50, "left"),(200,50,'left'),(150,50,'left'), (0,150,'right'),\
(-300,150,'left'),(-400,150,'left'),(-400,-50,'right'),(-200,-50,'left'),(0,-50,'right'),(200,50,'left'),(100,-150,'right'),(0,-150,'right')]

# This variable is a list of all bullets currently
# in the game. It is a list of tuples of (x,y)
# coordinates, one for each bullet. An elements will
# be added when a new bullet is fired, and removed
# when a bullet is destroyed (either by leaving
# the screen or by hitting an enemy).
bullets = []

# This variable is checked by the game's main
# loop to determine when it should end. When
# the game ends (either when the player's ship
# is destroyed, or when all enemies have been 
# destroyed), your code should set this variable
# to True, causing the main loop to end.
gameover = False


def drawborders():
    """
    Begins by drawing out the borders in which the game will take place.
    Nothing is permitted to travel outside this area.
    """
    
    turtle.up()
    turtle.setpos(-500,350)
    turtle.down()
    for i in range(4):
        turtle.color("black")
        turtle.forward(990)
        turtle.right(90)
    turtle.up()
    
def drawship():
    """
    Draws out the ship to be controlled by the user.
    """

    turtle.setheading(0)
    turtle.setpos(userx,250)
    turtle.down()
    turtle.color("blue")
    turtle.begin_fill()
    turtle.forward(25)
    turtle.right(120)
    turtle.forward(25)
    turtle.right(120)
    turtle.forward(25)
    turtle.end_fill()
    turtle.up()

def drawenemies():
    """
    Takes the list of enemy coordinates and draws
    out each of the enemies currently on the screen.
    """
    
    global enemies
    turtle.setheading(0)
    for (x,y,direction) in enemies:
        turtle.setpos(x,y)
        turtle.down()
        turtle.color('red')
        turtle.begin_fill()
        turtle.circle(8)
        turtle.end_fill()
        turtle.up()  
    
def drawbullets():
    """
    Takes the list of bullets that have are
    added everytime the user fires, draws each
    one currently present.
    """
    
    global bullets
    global userx
    
    turtle.setheading(0)
    turtle.color('black')
    for (x,y) in bullets:
        turtle.setpos(x, y)
        turtle.down()
        turtle.dot()
        turtle.up()

def draw_frame():
    """
    signature: () -> NoneType
    Given the current state of the game in
    the global variables, draw all visual
    elements on the screen: the player's ship,
    the enemies, and the bullets.
    Please note that this is your only function
    where drawing should happen (i.e. the only
    function where you call functions in the
    turtle module). Other functions in this
    program merely update the state of global
    variables.
    This function also should not modify any
    global variables.
    Hint: write this function first!
    """
    global userx
    global enemies

    drawborders()
    drawship()
    drawbullets()
    drawenemies()
    
       
def key_left():
    """
    signature: () -> NoneType
    This function is called by turtle whenever
    the user press the left arrow. It should
    adjust the position of the player's ship
    appropriately by modifying the variable
    userx.
    """
    global userx

    if userx < -480: # prevents user from going past left border
        userx = userx
    else:
        userx -= 20


def key_right():
    """
    signature: () -> NoneType
    This function is called by turtle whenever
    the user press the left arrow. It should
    adjust the position of the player's ship
    appropriately by modifying the variable
    user1x.
    """
    global userx
    if userx > 440: # prevents user from going past right border
        userx = userx
    else:
        userx += 20
    
def key_space():
    """
    signature: () -> NoneType
    This function is called by turtle whenever
    the user press the space key. It should
    add a new bullet to the list of bullets.
    """

    global bullets
    global userx
    
    bullets.append((userx + 13 ,220))    

def physics():
    """
##    signature: () -> NoneType
##    Update the state of the game world, as
##    stored in the global variables. Here, you
##    should check the positions of the bullets,
##    and remove them if they go off the screen
##    or collide with an enemy. In the later case
##    you should also remove the enemy. That is,
##    given the current position of the bullets,
##    calculate their position in the next frame.
##    """
    global bullets
    global enemies
    
    breaker = 0 
    breaker2 = 0
    # While nesting the loops for the bullet and enemy list,
    # we check to see if the bullet and enemy collide,
    # and remove both if they do. To avoid out of bounds errors,
    # we must break out of the loop if there is a removal of
    # an enemy or a bullet. These variables simply function as
    # a test of whether or not the previous iteration resulted
    # in a removal of any values in the lists. If there was,
    # then there should be a break from the loop.
    
    for i in range(len(bullets)):
        if breaker or breaker2: 
            break
        x_bullet = bullets[i][0] 
        y_bullet = bullets[i][1]
        y_bullet -= 10
        bullets[i] = (x_bullet,y_bullet)
        # Checking to see if the bullet has left the screen
        if y_bullet <= -360:
            bullets.pop(i)
            break
        # Checking to see if the bullet hits the enemy, should remove both the enemy and the bullet from the screen
        for j in range(len(enemies)):
            x_enemy = enemies[j][0]
            y_enemy = enemies[j][1]
            if x_enemy - 8 <= x_bullet <= x_enemy + 8 and y_enemy - 8 <= y_bullet <= y_enemy + 8:
                breaker = bullets.pop(i)
                breaker2 = enemies.pop(j)
                break
                            
def ai():
    """
    signature: () -> NoneType
    Perform the 'artificial intelligence' of
    the game, by updating the position of the
    enemies, storied in the enemies global
    variable. That is, given their current
    position, calculate their position
    in the next frame.
    If the enemies reach the player's ship,
    you should set the gameover variable
    to True. Also, if there are no more
    enemies left, set gameover to True.
    """
    global enemies
    global gameover

    enemyspeed = 1
    widthleft = -440
    widthright = 480

    # Ends the game if all enemies have been defeated
    if len(enemies) == 0:
        gameover = True
    
    for i in range(len(enemies)):
        x = enemies[i][0] # x coordinate of enemy
        y = enemies[i][1] # y coordinate of enemy
        direction = enemies[i][2] # enemy going left / right ?
        enemyspeed += .03 
        if x-8 <= userx <= x+8 and y-8 <= 250 <= y+8: # ends game if enemy reaches the user ship
            gameover = True
        if x <= widthleft or x >= widthright: # changes direction of the enemy when it reaches the border from either side, also moves it up
            if direction == 'left':
                direction = 'right' 
            elif direction == 'right':
                direction = 'left'
            y += 50
            enemies[i] = (x,y,direction)
        if direction == 'left': # calculation of new position of the enemies, speeds up as game moves along
            enemies[i] = (x-(5*enemyspeed),y,direction)
        elif direction == 'right':
            enemies[i] = (x+(5*enemyspeed),y,direction)

def reset():
    """
    signature: () -> NoneType
    This function is called when your game starts.
    It should set initial value for all the
    global variables.
    """
    global enemies
    global bullets
    global userx
    global gameover

    gameover = False
    enemies = [(200,-50, "left"),(0, -50, "right"),(-200,-50,'right'),(250,50, "left"),(200,50,'left'),(150,50,'left'), (0,150,'right'),\
    (-300,150,'left'),(-400,150,'left'),(-400,-50,'right'),(-200,-50,'left'),(0,-50,'right'),(200,50,'left'),(100,-150,'right'),(0,-150,'right')]
    bullets = []
    userx = -20

def main():
    """
    signature: () -> NoneType
    Run the game. You shouldn't need to
    modify this function.
    """
    turtle.tracer(0,0)
    turtle.hideturtle()
    turtle.onkey(key_left, "Left")
    turtle.onkey(key_right, "Right")
    turtle.onkey(key_space, "space")
    turtle.listen()
    reset()
    while not gameover:
        physics()
        ai()
        turtle.clear()
        draw_frame()
        turtle.update()
        time.sleep(0.05)

main()
