#   pyBrick.py
#
#   Remake of the old Breakout/ Arkanoid game
#
#   Alastair Montgomery (c) 2010
#

import pdb
import pyglet
import random
import math

from pyglet.window import key
from pyglet.window import mouse

from Ball import Ball
from Brick import Brick
from Player import Player
from Walls import Walls

#Setup Window
window = pyglet.window.Window(640,480,caption="pyBrick",vsync = True)
window.set_location(window.screen.width/2 - window.width/2,window.screen.height/2 - window.height/2)


#create a sprite batch, graphics order, etc
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
wallpaper = pyglet.resource.image('graphics/background.jpg')
wpSprite = pyglet.sprite.Sprite(wallpaper,batch=batch,group=background)

#Initialise Player etc
player = Player(window,batch,foreground)
lifes = 0
score = 0
hiscore = 0
level = 0
balls = []
bricks = []
myWalls = Walls()

#Setup Text Labels for scoring etc
playerLabel = pyglet.text.Label('Score', font_name='Arial', font_size=12, x=40, y=464, anchor_x='center', anchor_y='center',batch = batch)
playerScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=40, y=440, anchor_x='center', anchor_y='center',batch = batch)
hiLabel = pyglet.text.Label('Hi Score', font_name='Arial', font_size=12, x=600, y=464, anchor_x='center', anchor_y='center',batch = batch)
hiScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=600, y=440, anchor_x='center', anchor_y='center',batch = batch)
lifeLabel = pyglet.text.Label('Lifes', font_name='Arial', font_size=12, x=320, y=464, anchor_x='center', anchor_y='center',batch = batch)
lifeScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=320, y=440, anchor_x='center', anchor_y='center',batch = batch)

def newWall(level):
    global myWalls
    mod = myWalls.length
    lines = myWalls.walls[level%myWalls.length]
    wall = []
    loopY = 0
    for line in lines:
        loopX = 0
        for a in line:
            if a != ' ':
                wall.append(Brick(loopX*64,200+(loopY*32),a,batch,foreground))
            loopX += 1
        loopY +=1    
    return wall

def newGame():
    global score, hiscore, lifes, balls, bricks, level,player
    
    for a in range(0,1):
        newBall()
    if score > hiscore:
        hiscore = score
    score = 0
    level = 0
    lifes = 2        
    bricks = newWall(level)

def newBall():
    global balls, player
    balls.append(Ball(player.x+(player.width//2),window,batch,foreground))
    
def bang(left,right,top,bottom,b,dt):
    #Collision between bat (a)  and ball (b)
    nextPY = b.y+(b.dy*dt)
    nextPX = b.x+(b.dx*dt)

    if (nextPY <= top and nextPY >= bottom) and (nextPX <= right and nextPX >= left):
        return True
    else:
        return False

def update(dt):
    global score, hiscore, bricks,balls,lifes,level

    player.update(dt)
    mid = player.x + (player.width/2)
    right = player.x + player.width
    top = player.y + player.height

    for p2 in balls:
        if bang(player.x,right,top,player.y,p2,dt):
            #collision with bat and ball
            p2.collision(dt,mid)
        else:
            for b in bricks:
                if bang(b.x,b.x+b.width,b.y+b.height,b.y,p2,dt):
                    #collision with ball and brick
                    if b.collision():
                        b.delete()
                        bricks.remove(b)
                        if len(bricks) == 0:
                            level += 1
                            bricks = newWall(level)
                    p2.collision(dt,b.x+(b.width/2))
                    score += 1
        if p2.update(dt) == False:
            lifes -= 1
            if lifes < 0:
                for b in balls:
                    b.delete()
                    balls.remove(b)
                newGame()
            else:
                for b in balls:
                    b.delete()
                    balls.remove(b)
                newBall()

@window.event
def on_key_press(symbol,modifiers):
    window.close()

@window.event
def on_mouse_press(x1, y1, button, modifiers):
    mgr = pyglet.image.get_buffer_manager()
    mgr.get_color_buffer().save("screen.png")
    window.close()

@window.event
def on_mouse_motion(x,y,dx,dy):
    player.x = x

@window.event
def on_draw():
    window.clear()
    playerScore.text = "%3d" % score
    hiScore.text = "%3d" % hiscore
    lifeScore.text = "%d" % lifes
    batch.draw()

def main():
    newGame()
    pyglet.clock.schedule_interval(update, 1.0/60.0)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()

if __name__ == "__main__":
    main()
