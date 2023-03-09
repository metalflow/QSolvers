#imports
import numpy

#define constants
NUM_ESPISODE=1000
NUM_ACTIONS=100
EPISODE_GROUP_SIZE=100
OUTPUT_FILE_NAME="stats.csv"

#initialize variables
TotalEpisodeReward=0
rewardPerGroup=0

#define classes
#data class for the world
class World:
    #Class Constants
    MAPWIDTH = 10
    MAPLENGTH = 10
    CANPROBABILITY = 0.5

    #class variables

    #constructor
    def __init__(self):
        self.grid = [[Location() for _ in range(self.MAPWIDTH)] for _ in range(self.MAPLENGTH)]
        self.robots=[]
        self.numCans=0
        return

    def addBot(self):
        newBot = Robot(self)
        self.robots.append(newBot)
        return newBot

    #methods
    def reset(self):
        #oldBots = self.robots.copy()
        #del self.robots
        #self.robots=[]
        emptyBotLocations=[]
        #repopulate cans
        for y in range(self.MAPLENGTH):
            for x in range(self.MAPWIDTH):
                #check a random number against the probability of a can
                if numpy.random.random() >= self.CANPROBABILITY:
                    self.grid[x][y].Can=True
                    self.numCans+=1
                else:
                    self.grid[x][y].Can=False
                #ensure there is no bot in this location
                self.grid[x][y].Robot=None
                #add this locaiton to the bot placement list
                emptyBotLocations.append([x,y])
                #ensure no wall is popualated
                self.grid[x][y].Wall=None
        #randomly place robots
        for oldBot in self.robots:
            oldBot.reset()
            #pick a new place from the list of open places to place robots
            randIndex=numpy.random.randint(0,len(emptyBotLocations)-1)
            coordSet=emptyBotLocations.pop(randIndex)
            oldBot.place(coordSet[0],coordSet[1])
        #while len(oldBots)>0:
        #    oldBot=oldBots.pop()
        #    oldBot.reset()
        #    #pick a new place from the list of open places to place robots
        #    randIndex=numpy.random.randint(0,len(emptyBotLocations)-1)
        #    coordSet=emptyBotLocations.pop(randIndex)
        #    oldBot.place(coordSet[0],coordSet[1])
        #    #add the oldBot back into the list of robots
        #    self.robots.append(oldBot)
        #del oldBots
        return

    def displayWorld(self):
        for y in range(self.MAPLENGTH):
            for x in range(self.MAPWIDTH):
                print(self.grid[x][y],end=",")
            print("")
        return

#data class for storing world grid information
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

#actor class for robots in the world
class Robot(World):
    #Class constants
    ACTIONS=["GONORTH","GOEAST","GOSOUTH","GOWEST","PICKUP"]
    COLLISION=-5
    PICK_UP_NOTHING=-1
    PICKUP_CAN=10
    MINIMUM_REWARD=-10
    DISCOUNT_FACTOR=0.2
    STARTING_GREED_FACTOR=0.1

    #class variables

    #constructor
    def __init__(self,world:World):
        self.GreedFactor = self.STARTING_GREED_FACTOR
        self.parentWorld=world
        self.coords = numpy.array([-1,-1])
        self.northLocation = ""
        self.eastLocation = ""
        self.southLocation = ""
        self.westLocation = ""
        self.centerLocation = ""
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
        self.centerLocation = ""
        #QMap does *not* get reset between runs
        return

    def place(self,x:int,y:int):
        #remove robot from old Location
        self.parentWorld.grid[self.coords[0]][self.coords[1]].Robot=None
        #update coordinates
        self.coords=numpy.array([x,y])
        #place robot in new Location
        self.parentWorld.grid[self.coords[0]][self.coords[1]].Robot=self
        return

    def lookAround(self):
        #if looking outside the edge of the map, return Wall...
        if (self.coords[1]-1)>0:
            self.northLocation = str(self.parentWorld.grid[self.coords[0]][self.coords[1]-1])
        #otherwise return the value of the Location
        else:
            self.northLocation = Location.STATES[3]
        #if looking outside the edge of the map, return Wall...
        if (self.coords[0]+1)<(self.parentWorld.MAPWIDTH-1):
            self.eastLocation = str(self.parentWorld.grid[self.coords[0]+1][self.coords[1]])
        #otherwise return the value of the Location
        else:
            self.eastLocation = Location.STATES[3]
        #if looking outside the edge of the map, return Wall...
        if (self.coords[1]+1)<(self.parentWorld.MAPLENGTH-1):
            self.southLocation = str(self.parentWorld.grid[self.coords[0]][self.coords[1]+1])
        #otherwise return the value of the Location
        else:
            self.southLocation = Location.STATES[3]
        #if looking outside the edge of the map, return Wall...
        if (self.coords[0]-1)>0:
            self.westLocation = str(self.parentWorld.grid[self.coords[0]-1][self.coords[1]])
        #otherwise return the value of the Location
        else:
            self.westLocation = Location.STATES[3]
        self.centerLocation = str(self.parentWorld.grid[self.coords[0]][self.coords[1]])
        return

    def takeAction(self)->int:
        #analyze percept
        #check all members of the percept to ensure percept is correctly formed
        #if a member is not a defined Location desriptor character, raise
        #an exception
        if Location.STATES.count(self.northLocation) == 0:
            raise Exception("northLocation is not a valid location")
        elif Location.STATES.count(self.eastLocation) == 0:
            raise Exception("eastLocation is not a valid location")
        elif Location.STATES.count(self.southLocation) == 0:
            raise Exception("southLocation is not a valid location")
        elif Location.STATES.count(self.westLocation) == 0:
            raise Exception("westLocation is not a valid location")
        elif Location.STATES.count(self.centerLocation) == 0:
            raise Exception("centerLocation is not a valid location")

        #determine if we should take a random action
        if numpy.random.random()<self.GreedFactor:
            #if not
            #Examine QMap for known actions
            action = self._checkQMap()
        else:
            action = self.ACTIONS[numpy.random.randint(0,len(self.ACTIONS))]

        reward = 0
        #execute action selected and compute any rewards generated by the action
        if action == self.ACTIONS[0]:
            reward = self._move(self.coords[0],self.coords[1]-1)
        elif action == self.ACTIONS[1]:
            reward = self._move(self.coords[0]+1,self.coords[1])
        elif action == self.ACTIONS[2]:
            reward = self._move(self.coords[0],self.coords[1]+1)
        elif action == self.ACTIONS[3]:
            reward = self._move(self.coords[0]-1,self.coords[1])
        elif action == self.ACTIONS[4]:
            reward = self._pickup()
        else:
            raise Exception("action "+str(action)+" is not a member of allowed ACTIONS:"+str(self.ACTIONS))

        #update the QMap with the reward (if greater than the current value)

        return reward

    def _checkQMap(self):
        action = self.ACTIONS[4] #just a dummy action for now
        #find maximum QMap entry for the current location
        #find the maximum QMap entry for the adjacent locations
        #if the discounted adjacent reward are greater than the current reward
            #update the current location with a move to adjacent command
            #return move to adjacent command
        #return the current location command
        return action

    def _move(self,newX:int,newY:int)->int:
        #check to see of attempting to move out of bounds
        if newX<0:
            return self.COLLISION
        elif newY<0:
            return self.COLLISION
        elif newX>=Location.MAPWIDTH:
            return self.COLLISION
        elif newY>=Location.MAPLENGTH:
            return self.COLLISION
        #check for COLLISION
        elif self.parentWorld.grid[newX][newY] == Location.STATES[3]:
            return self.COLLISION
        elif self.parentWorld.grid[newX][newY] == Location.STATES[2]:
            return self.COLLISION
        else:
            self.place(newX,newY)
        return 0

    def _pickup(self)->int:
        #check for the presence of a can
        if self.parentWorld.grid[self.coords[0]][self.coords[1]].Can:
            self.parentWorld.grid[self.coords[0]][self.coords[1]].Can = False
            self.parentWorld.numCans-=1
            return self.PICKUP_CAN
        else:
            return self.PICK_UP_NOTHING

#define functions

#begin main program
#open stats file if defined
if (type(OUTPUT_FILE_NAME) == str)&(OUTPUT_FILE_NAME != ""):
    statsFile=open("TRAINING"+OUTPUT_FILE_NAME,"w")
    statsFile.write("Episode,totalReward\n")
    print(OUTPUT_FILE_NAME+" opened for writing.")
else:
    statsFile=None
#make a world
currentWorld=World()
#add a robot to that world
currentWorld.addBot()
#start training episode loop
for episodeCount in range(0,NUM_ESPISODE):
    #reset world
    currentWorld.reset()
    #reset robots
    #should be handled by world reset
    #reset reward TotalEpisodeReward
    TotalEpisodeReward = 0
    #begin actions loop
    for actionCount in range(0,NUM_ACTIONS):
        #have robot(s) look around
        for bot in currentWorld.robots:
            bot.lookAround()
        #have robot(s) take actions and add reward (if any) to TotalEpisodeReward
        for bot in currentWorld.robots:
            TotalEpisodeReward += bot.takeAction()
        #print out world for human monitoring
        #print("Episode number:"+str(episodeCount)+" action number:"+str(actionCount))
        #currentWorld.displayWorld()
    #log total reward gathered
    if statsFile != None:
        statsFile.write(str(episodeCount)+","+str(TotalEpisodeReward)+"\n")
    rewardPerGroup+=TotalEpisodeReward
    #reduce GreedFactor by (STARTING_GREED_FACTOR/NUM_ESPISODE)
    for bot in currentWorld.robots:
        bot.GreedFactor=bot.GreedFactor-(bot.STARTING_GREED_FACTOR/NUM_ESPISODE)
    #print out world for human monitoring
    #print("Episode number:"+str(episodeCount)+" reward gathered:"+str(TotalEpisodeReward))
    #currentWorld.displayWorld()
    #every EPISODE_GROUP_SIZEth episode, print the total reward divided by EPISODE_GROUP_SIZE
    if episodeCount%100 == 0:
        print("Average Reward over the last "+str(EPISODE_GROUP_SIZE)+" episodes:"+str(rewardPerGroup/EPISODE_GROUP_SIZE))
        rewardPerGroup = 0
#clean up
statsFile.close()

#start test episode loop
    #set GreedFactor to STARTING_GREED_FACTOR
    #reset world
    #reset robots
    #begin actions loop
        #have robot(s) look around
        #have robot(s) take actions
    #log total reward gathered
    #every EPISODE_GROUP_SIZEth episode, print the total reward divided by EPISODE_GROUP_SIZE
#clean up
statsFile.close()