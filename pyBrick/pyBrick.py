#   pyBrick.py
#
#   Remake of the old Breakout/ Arkanoid game
#
# Alastair Montgomery 2010
# http://www.twitter.com/alastair_hm
#

import pyglet

#from pyglet.window import key
#from pyglet.window import mouse

from Ball import Ball
from Brick import Brick
from Player import Player
from Walls import Walls
from Wallpaper import Wallpaper

#Setup Window
window = pyglet.window.Window(640,480,caption="pyBrick",vsync = True)
window.set_location(window.screen.width/2 - window.width/2,window.screen.height/2 - window.height/2)
window.set_exclusive_mouse()


#create a sprite batch, graphics order, etc
batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
wallpaper = Wallpaper('data/background.txt',batch,background)

#Initialise Player etc
player = Player(window,batch,foreground)
lifes = 0
score = 0
hiscore = 0
level = 0
balls = []
bricks = []
myWalls = Walls('data/defaultWalls.txt')

#Setup Text Labels for scoring etc
playerLabel = pyglet.text.Label('Score', font_name='Arial', font_size=12, x=40, y=464, anchor_x='center', anchor_y='center',batch = batch)
playerScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=40, y=440, anchor_x='center', anchor_y='center',batch = batch)
hiLabel = pyglet.text.Label('Hi Score', font_name='Arial', font_size=12, x=600, y=464, anchor_x='center', anchor_y='center',batch = batch)
hiScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=600, y=440, anchor_x='center', anchor_y='center',batch = batch)
lifeLabel = pyglet.text.Label('Lifes', font_name='Arial', font_size=12, x=320, y=464, anchor_x='center', anchor_y='center',batch = batch)
lifeScore = pyglet.text.Label('000', font_name='Arial', font_size=24, x=320, y=440, anchor_x='center', anchor_y='center',batch = batch)

def newWall(level):
    '''Create wall of bricks'''
    global myWalls

    lines = myWalls.walls[level%myWalls.length]
    wall = []
    loopY = 0
    for line in lines:
        loopX = 0
        for a in line:
            if a != '.':
                wall.append(Brick(loopX*64,200+(loopY*32),a,batch,foreground))
            loopX += 1
        loopY +=1    
    return wall

def test():
    global score, hiscore, lifes, balls, bricks, level,player

    newBall()
    bricks.append(Brick(320,200,'#',batch,foreground))
    balls[0].x = 200
    balls[0].y = 100
    balls[0].dx = 100
    balls[0].dy = 100


def newGame():
    global score, hiscore, lifes, balls, bricks, level,player
    
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
    
def bang(a,b,dt):
    '''Collision between sprite (a) and sprite (b)'''
    left = a.x
    right = a.x + a.width
    top = a.y + a.height
    bottom = a.y

    nextPY = b.y+(b.dy*dt)
    nextPX = b.x+(b.dx*dt)
    nextPTY = nextPY + b.height
    nextPTX = nextPX + b.width
    
    #print 'ball [%d,%d],[%d,%d] brick [%d,%d,%d,%d]' % (b.x,b.y,nextPX,nextPY,left,bottom,right,top)    
    if ((nextPY <= top and nextPY >= bottom) and (nextPX <= right and nextPX >= left)) or ((nextPTY <= top and nextPTY >= bottom) and (nextPTX <= right and nextPTX >= left)):
        #print 'ball [%d,%d],[%d,%d] brick [%d,%d,%d,%d]' % (b.x,b.y,nextPX,nextPY,left,bottom,right,top)
        if b.y >= bottom and b.y <= top:
            if b.x < left:
                #print 'left hit'
                return 1
            elif b.x > right:
                #print 'right hit'
                return 2
        else:
            if b.y < bottom:
                #print 'bottom hit'
                return 3
            elif b.y > top:
                #print 'top hit'
                return 4
    else:
        return 0

def update(dt):
    global score, hiscore, bricks,balls,lifes,level

    #player.update(dt)
    mid = player.x + (player.width/2)

    for p2 in balls:
        result = bang(player,p2,dt)
        if result > 0:
            #collision with bat and ball
            p2.collision(dt,mid,result,True)
        else:
            for b in bricks:
                result = bang(b,p2,dt)
                if result > 0:
                    #collision with ball and brick
                    if b.collision():
                        b.delete()
                        bricks.remove(b)
                        if len(bricks) == 0:
                            level += 1
                            bricks = newWall(level)
                            wallpaper.update()
                    p2.collision(dt,b.x+(b.width/2),result,False)
                    score += 1
        if p2.update(dt) == False:
            # Ball missed
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
    #mgr = pyglet.image.get_buffer_manager()
    #mgr.get_color_buffer().save("screen.png")
    window.close()

@window.event
def on_mouse_motion(x,y,dx,dy):
    player.x += dx

@window.event
def on_draw():
    window.clear()
    playerScore.text = "%d" % score
    hiScore.text = "%d" % hiscore
    lifeScore.text = "%d" % lifes
    batch.draw()

def main():
    newGame()
    #test()
    pyglet.clock.schedule_interval(update, 1.0/60.0)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    pyglet.app.run()

if __name__ == "__main__":
    main()
