# Brick class
#
# 
#
# Alastair Montgomery 2010
# http://www.twitter.com/alastair_hm
#

import pyglet

class Brick(pyglet.sprite.Sprite):

    image = pyglet.resource.image('graphics/brick_black.png')
    width = 0
    height = 0
    
    def __init__(self,nx,ny,colour,batch,group):
        x = nx
        y = ny
        if colour == '#':
            self.image = pyglet.resource.image('graphics/brick_black.png')
            super(Brick, self).__init__(self.image,x,y,batch = batch,group = group)
            self.hit = 1
        elif colour == '~':
            self.image = pyglet.resource.image('graphics/brick_red.png')
            super(Brick, self).__init__(self.image,x,y,batch = batch,group = group)        
            self.hit = 2
        elif colour == '@':
            self.image = pyglet.resource.image('graphics/brick_green.png')
            super(Brick, self).__init__(self.image,x,y,batch = batch,group = group)        
            self.hit = 3            
        else:
            self.image = pyglet.resource.image('graphics/brick_black.png')
            super(Brick, self).__init__(self.image,x,y,batch = batch,group = group)        
            self.hit = 1
        self.dx = 0
        self.dy = 0
        self.anchor_x = x
        self.anchor_y = y    
        self.width = self.image.width
        self.height = self.image.height
        
    def collision(self):
        self.hit -= 1
        if self.hit == 0:
            return True
        else:
            self.opacity = self.opacity -64
            return False
