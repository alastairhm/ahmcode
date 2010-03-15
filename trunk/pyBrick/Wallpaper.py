# Wallpaper class
#
# 
#
# Alastair Montgomery 2010
# http://www.twitter.com/alastair_hm
#

import pyglet

class Wallpaper(pyglet.sprite.Sprite):
    
    paper = None
    total = 0
    count = 0

    def __init__(self,filename,batch,group):
        self.paper = self.fileRead(filename)
        total = len(self.paper)
        if total > 0:
            wallImage = pyglet.resource.image(self.paper[self.count])
        else:
            wallImage = pyglet.resource.image('graphics/background.jpg')
        super(Wallpaper, self).__init__(wallImage,batch = batch, group = group)
        
    def fileRead(self,filename):
        tmpText = []
        try:
            myFile = open(filename, 'r')
            for line in myFile:
                tmpText.append(line.strip())
            myFile.close()
        except IOError:
            print 'Problems reading file ',filename
        return tmpText

    def update(self):
        self.count = (self.count + 1) % self.total
        wallImage = pyglet.resource.image(self.paper[self.count])
        self.image = wallImage
        return 0
