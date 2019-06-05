import math
import random

import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
#from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6

# For Python 3.7:
from ps2_verify_movement37 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.7

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.cleaned = [] #Keep track of the cleaned tiles
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        #Position represented as whole numbers
        intPos = (int(pos.getX()), int(pos.getY()))
        
        #Add to list of cleaned tiles
        if intPos not in self.cleaned:
            self.cleaned.append(intPos)

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        pos = (m, n)
        return pos in self.cleaned
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return int(self.width * self.height)

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleaned)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        #Compute random x and y coordinates within the room
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        
        return (Position(x, y))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        #Check if height and width values are both within the room
        return pos.x >= 0 and pos.x < self.width and pos.y >= 0 and pos.y < self.height


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.pos = room.getRandomPosition()#Assign robot a random posiiton to begine with
        self.dir = random.randint(0, 360)#Assign robot a random direction to begin with
        self.room.cleanTileAtPosition(self.pos)#Mark current tile as cleaned

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.dir

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.dir = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #Implemented below for the 2 different types of robots
        raise NotImplementedError # don't change this!


class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #get a new position for the robot
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        
        #Clean tile if the new position is in the room
        if self.room.isPositionInRoom(nextPos):
            self.room.cleanTileAtPosition(nextPos)
            self.setRobotPosition(nextPos)
        #If the position is not in the room, adjust direction
        else:
            self.setRobotDirection(random.randint(0, 360))

# Uncomment this line to see your implementation of StandardRobot in action!
testRobotMovement(StandardRobot, RectangularRoom)


class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #get a new position for the robot
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        
        #If next position is in the room, clean that tile, update robot position
        #to the new position and set random direction
        if self.room.isPositionInRoom(nextPos):
            self.room.cleanTileAtPosition(nextPos)
            self.setRobotPosition(nextPos)
            self.setRobotDirection(random.randint(0, 360))
        #If next position is not in the room, then set random direction
        else:
            self.setRobotDirection(random.randint(0, 360))

# Uncomment line below to see your implementation of RandomWalkRobot in action!
testRobotMovement(RandomWalkRobot, RectangularRoom)


def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    """
    The "anim = ", "anim.update" and "anim.done()" lines are intentionally commented out.
    Uncomment them to view the animation. However, make sure that the runSimulation
    program is not being called near the bottom of this program as that call will run
    extremly slowly.
    """
    robots = []
    timeStep = 0
    for i in range(num_trials):
        #anim = ps2_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        for j in range(num_robots):
            robots.append(robot_type(room, speed))
        while (room.getNumCleanedTiles()/room.getNumTiles() < min_coverage):
            timeStep += 1
            for k in robots:
                #anim.update(room, robots)
                k.updatePositionAndClean()
        #anim.done()
    
    return timeStep/num_trials

# Uncomment the 2 lines below to see how many steps your simulation takes on average
print("Running time for Standard Robot: " + str(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)))
print("Running time for Random Walk Robot: " + str(runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot)))

def showPlot1(title, x_label, y_label):
    """
    Plots the cleaning time required by range(n) number of Standard and RandomWalk Robots
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 10, 10, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 10, 10, 0.8, 20, RandomWalkRobot))
    pylab.figure()
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

def showPlot2(title, x_label, y_label):
    """
    Plots the relationship between aspect ratio and cleaning time for Standard
    and RandomWalk Robots
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 20, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 20, RandomWalkRobot))
    pylab.figure()
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

# Uncomment the lines below to see the plots of Robots cleaning times.
    
showPlot1("Cleaning time based on Number of Robots", "Robots", "Cleaning Time")
showPlot2("Running Time based on Aspect Ratios", "Aspect Ratios", "Time")