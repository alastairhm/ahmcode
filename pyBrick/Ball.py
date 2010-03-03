import pyglet
import random
import math

class Ball(pyglet.sprite.Sprite):
    image = pyglet.resource.image('graphics/ball12.png')
    width = image.width
    height = image.height
    bounce = pyglet.resource.media('sounds/ball.wav', streaming=False)

    def __init__(self,xpos,window,batch,group):
        x = xpos
        #x = random.random() * (window.width-self.width)
        y = 40
        super(Ball, self).__init__(self.image,x,y,batch = batch, group=group)
        self.dx = (random.random() - 0.5) * 500
        #self.dy = (random.random() * 250) + 250
        self.dy = 240
        self.anchor_x = self.width /2
        self.anchor_y = self.height /2
        self.scale = 1
        self.width = self.width * self.scale
        self.height = self.height * self.scale
        self.max_x = window.width - self.width
        self.max_y = window.height - self.height

    def update(self,dt):
        # Move multi_x/y pixels per second
        flag = True        
        #Ball leaves bottom of screen
        if self.y <= 0:
            self.y = self.max_y - self.height
            self.dx = (random.random() - 0.5) * 500
            flag = False
        else:
            #Right wall hit
            if self.x >= self.max_x or self.x <= 0:
                self.dx *= -1
                self.bounce.play()
            #Left wall hit
            if self.y >= self.max_y:
                self.dy *= -1
                self.bounce.play()
        #Set new ball positon
        self.x += dt * self.dx
        self.y += dt * self.dy
        self.x = min(max(self.x,0),self.max_x)
        self.y = min(max(self.y,0),self.max_y)
        return flag
        
    def collision(self,dt,mid):
        self.bounce.play()
        #Change speed if hit with edge of bat
        if self.x < mid-10:
            self.dx = self.dx - 100
        elif self.x > mid+10:
            self.dx = self.dx + 100
        #Bounce ball    
        self.dy *= -1
        self.y += dt * self.dy
