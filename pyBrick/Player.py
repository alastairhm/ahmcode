import pyglet
import random
import math

class Player(pyglet.sprite.Sprite):
    image = pyglet.resource.image('graphics/player.png')
    width = 0
    height = 0
    
    def __init__(self,window,batch,group):
        self.width = self.image.width
        self.max_x = window.width - self.width
        self.height = self.image.height
        self.max_y = window.height - self.height
        
        x = window.width//2 - self.width//2
        y = 20
        super(Player, self).__init__(self.image,x,y,batch = batch,group = group)
        self.dx = 0
        self.dy = 0
        self.anchor_x = x
        self.anchor_y = y

    def update(self,dt):
        self.x += self.dx
        if self.x >= self.max_x or self.x <= 0:
            self.dx *= -1
        self.x = min(max(0,self.x),self.max_x)
        
    def move(self,amount):
        self.x += amount
        self.x = min(max(0,self.x),self.max_x)
