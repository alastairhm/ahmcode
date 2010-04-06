# Walls class
#
# Creates a batch of walls either from passed file or using a default set
#
# Alastair Montgomery 2010
# http://www.twitter.com/alastair_hm
#

class Walls():
    '''Define a set of walls for level'''
    walls = []
    length = 0

    def __init__(self,filename):
        self.fileRead(filename)
        if len(self.walls) == 0:
            '''Setup default walls if none read in'''
            self.walls.append(('##########','#.#.#.#.#.','##########','~#~#~#~#~#','#~#~#~#~#~','~#~#~#~#~#','#~#~#~#~#~'))
            self.walls.append(('##########','#~~~~~~~~#','#~######~#','#~#~~~~#~#','#~######~#','#~~~~~~~~#','##########'))
            self.walls.append(('~~~~~~~~~~','~~~~~~~~~~','##########','~~~~~~~~~~','~~~~~~~~~~','##########','~~~~~~~~~~'))
            self.fileWrite(filename)
        self.length = len(self.walls)

    def fileRead(self,filename):
        '''Read Walls from a file'''
        lines = []
        try:
            myFile = open(filename, "r")
            for line in myFile:
                if line == '#Wall Start\n':
                    lines = []
                elif line == '#Wall End\n':
                    self.walls.append(lines[:8])
                else:
                    lines.append(line.strip())
            myFile.close()
        except IOError:
            print "Error reading from file "+filename
        
    def fileWrite(self,filename):
        '''Write to a file'''
        try:
            myFile = open(filename, "w")
            for wall in self.walls:
                myFile.write("#Wall Start\n")
                for line in wall:
                    myFile.write(line+"\n")
                myFile.write("#Wall End\n")
            myFile.close()
        except IOError:
            print "Error writing to file "+filename
            
if __name__ == "__main__":
    w = Walls()
