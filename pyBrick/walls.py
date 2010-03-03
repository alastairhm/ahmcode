import pyglet

class Wall():
    walls = []

    def __init__(self):
        self.walls.append(('##########','##########','##########','~#~#~#~#~#','#~#~#~#~#~','~#~#~#~#~#','#~#~#~#~#~'))
        self.walls.append(('##########','#~~~~~~~~#','#~######~#','#~#~~~~#~#','#~######~#','#~~~~~~~~#','##########'))
        self.walls.append(('~~~~~~~~~~','~~~~~~~~~~','##########','~~~~~~~~~~','~~~~~~~~~~','##########','~~~~~~~~~~'))

    def fileRead(self,filename):
        '''Read Walls from a file'''
        lines = []
        try:
            myFile = open(filename, "r")
            for line in myFile:
                if line == '#Wall Start\n':
                    lines = []
                    print "start"
                elif line == '#Wall End\n':
                    print "end"
                else:
                    lines.append(line)
        except IOError:
            print "Error reading from file "+filename
        finally:
            myFile.close()
        
    def fileWrite(self,filename):
        '''Write to a file'''
        try:
            myFile = open(filename, "w")
            for wall in self.walls:
                myFile.write("#Wall Start\n")
                for line in wall:
                    myFile.write(line+"\n")
                myFile.write("#Wall End\n")
        except IOError:
            print "Error writing to file "+filename
        finally:
            myFile.close()
            
if __name__ == "__main__":
    
    w = Wall()
    #w.fileWrite("defaultWalls.txt")