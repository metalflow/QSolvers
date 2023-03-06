#imports
import numpy

#define constants

#initialize variables

#define classes
class World:
    #Class Constants
    MAPWIDTH = 10
    MAPLENGTH = 10
    CANPROBABILITY = 0.5

    #class varaibles

    #constructor
    def __init__(self):
        self.grid = [[Location()]*self.MAPLENGTH]*self.MAPWIDTH
        self.robots=[]
        return

    #methods
    def reset(self):
        oldBots = self.robots.copy()
        del self.robots
        self.robots=[]
        emptyBotLocations=[]
        #repopulate cans
        for y in range(self.MAPLENGTH):
            for x in range(self.MAPWIDTH):
                #check a random number against the probability of a can
                if numpy.random.random() >= self.CANPROBABILITY:
                    self.grid[x][y].Can=True
                else:
                    self.grid[x][y].Can=False
                #ensure there is no bot in this location
                self.grid[x][y].Robot=None
                #add this locaiton to the bot placement list
                emptyBotLocations.append([x,y])
                #ensure no wall is popualated
                self.grid[x][y].Wall=None
        #randomly place robots
        while len(oldBots)>0:
            oldBot=oldBots.pop()
            oldBot.reset()
            #pick a new place from the list of open places to place robots
            randIndex=numpy.random.randint(0,len(emptyBotLocations)-1)
            coordSet=emptyBotLocations.pop(randIndex)
            oldBot.place(coordSet[0],coordSet[1])
            #add the oldBot back into the list of robots
            self.robots.append(oldBot)
        del oldBots
        return

    def displayWorld(self):
        for y in range(self.MAPLENGTH):
            for x in range(self.MAPWIDTH):
                print(self.grid[x][y],end=",")
            print("/n")
        return


#data class for storing map information
class Location(World):
    #Class Constants
    STATES=["_","C","R","W"]

    #class variables

    #constructor
    def __init__(self):
        self.Can=False
        self.Robot=None
        self.Wall=False
        return

    #methods
    def __str__(self):
        if self.Wall:
            return self.STATES[3]
        elif self.Robot != None:
            return self.STATES[2]
        elif self.Can:
            return self.STATES[1]
        else:
            return self.STATES[0]

class Robot(World):
    #Class constants
    ACTIONS=["GONORTH","GOEAST","GOSOUTH","GOWEST","PICKUP"]
    COLLISION=-5
    PICK_UP_NOTHING=-1
    PICKUP_CAN=10
    MINIMUM_REWARD=-10

    #class variables

    #constructor
    def __init__(self):
        self.coords = numpy.array([-1,-1])
        self.northLocation = ""
        self.eastLocation = ""
        self.southLocation = ""
        self.westLocation = ""
        self.self.centerLocation = ""
        #QMap reads as follows [north],[east],[south],[west],[center],[action]=reward
        self.QMap = []
        return

    #methods
    def reset(self):
        self.coords = numpy.array([-1,-1])
        self.northLocation = ""
        self.eastLocation = ""
        self.southLocation = ""
        self.westLocation = ""
        self.self.centerLocation = ""
        #QMap does *not* get reset between runs
        return

    def place(self,x:int,y:int):
        self.coords=numpy.array([x,y])
        super().grid[x][y].Robot=self
        if super().robots.count(self) == 0:
            super().robots.append(self)
        return

    def lookAround(self):
        #if looking outside the edge of the map, return Wall...
        if (self.coords[1]-1)>0:
            self.northLocation = str(super().grid[self.coords[0]][self.coords[1]-1])
        #otherwise return the value of the Location
        else:
            northLocation = Location().Wall=True
        #if looking outside the edge of the map, return Wall...
        if (self.coords[0]+1)<(super().MAPWIDTH-1):
            self.eastLocation = str(super().grid[self.coords[0]+1][self.coords[1]])
        #otherwise return the value of the Location
        else:
            eastLocation = Location().Wall=True
        #if looking outside the edge of the map, return Wall...
        if (self.coords[1]+1)<(super().MAPLENGTH-1):
            self.southLocation = str(super().grid[self.coords[0],self.coords[1]+1])
        #otherwise return the value of the Location
        else:
            self.southLocation = Location().Wall=True
        #if looking outside the edge of the map, return Wall...
        if (self.coords[0]-1)>0:
            self.westLocation = str(super().grid[self.coords[0]+1],[self.coords[1]])
        #otherwise return the value of the Location
        else:
            self.westLocation = Location().Wall=True
        self.centerLocation = str(super().grid[self.coords[0]][self.coords[1]])
        return

    def takeAction(self):
        #analyze percept
        #check all members of the percept to ensure percept is correctly formed
        #if a member is not a defined Location desriptor character, quit early
        if Location.STATES.count(self.northLocation) == 0:
            return
        elif Location.STATES.count(self.eastLocation) == 0:
            return
        elif Location.STATES.count(self.southLocation) == 0:
            return
        elif Location.STATES.count(self.westLocation) == 0:
            return
        elif Location.STATES.count(self.currentLocation) == 0:
            return

        #take action
        actionList = None
        #first check to see if there is an action for the currently defined state
        try:
            actionList = self.QMap[self.northLocation][self.eastLocation][self.southLocation][self.westLocation]
        except:
            actionList = None
        #if there is an action for the current percept
        if len(actionList) > 0:
            maxReward = self.MINIMUM_REWARD
            maxRewardIndex= -1
            indexCounter = 0
            #analyze each action for the highest reward
            for action in actionList:
                if action > maxReward:
                    maxReward = action
                    maxRewardIndex = indexCounter
                indexCounter+=1
            #if the maxreward is not the maximum possible
        action = self.ACTIONS[numpy.random.randint(0,len(self.ACTIONS))]
        return      

#define functions

#begin main program



#clean up