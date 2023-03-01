#imports
import numpy

#define constants
MAPWIDTH = 10
MAPLENGTH = 10
CANPROBABILITY = 0.5

#initialize variables

#define classes
class World:
    #Class Constants

    #class varaibles

    #constructor
    def __init__(self):
        self.grid = [[Location()]*MAPLENGTH]*MAPWIDTH
        self.robots=[]
        return
    #methods
    def reset(self):
        oldBots = self.robots.copy()
        del self.robots
        self.robots=[]
        emptyBotLocations=[]
        #repopulate cans
        for y in range(MAPLENGTH):
            for x in range(MAPWIDTH):
                #check a random number against the probability of a can
                if numpy.random.random() > CANPROBABILITY:
                    self.grid[x][y].Can=False
                else:
                    self.grid[x][y].Can=False
                #ensure there is no bot in this location
                self.grid[x][y].Robot=None
                #add this locaiton to the bot placement list
                emptyBotLocations.append([x,y])
                #ensure no wall is popualated
                self.grid[x][y].Wall=None
        #randomly place robots
        for oldBot in oldBots:
            randIndex=numpy.random.randint(0,len(emptyBotLocations))
            coordSet=emptyBotLocations.pop(randIndex)
            
        return

#data class for storing map information
class Location(World):
    #Class Constants

    #class variables

    #constructor
    def __init__(self):
        self.Can=False
        self.Robot=None
        self.Wall=False
        QMap = []

    #methods

class Robot(World):
    #Class constants
    GONORTH = None
    GOEAST = None
    GOSOUTH = None
    GOWEST = None
    PICKUP = None

    #class variables

    #constructor
    def __init__(self):
        self.coords = [-1,-1]
        self.World = None
        return

    #methods
    def reset(self):
        self.Location = numpy.array([0,0])
        World.reset()
        return

    def place(self,x:int,y:int):
        self.coords=numpy.array([x,y])
        return

    def lookAround(self):
        self.percept=[]
        return


        

#define functions

#begin main program

#clean up