import anki_vector
from anki_vector.util import distance_mm, speed_mmps, Pose, Angle
from anki_vector.events import Events
import time
import heapq
import arena
import math
import numpy as np
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")

robot = anki_vector.AsyncRobot()
#robot = anki_vector.Robot()
robot.connect()
location = {}
current_direction = (1, 0)
red = (255, 0, 0)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'
    Source: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#answer-13849249 """
    # v1_u = unit_vector(v1)
    # v2_u = unit_vector(v2)
    # return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    angle = np.math.atan2(np.linalg.det([v1,v2]),np.dot(v1,v2))
    return angle

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = []
    
    def in_bounds(self, id):
        (x, y) = id
        return -1*self.width/2 < x < self.width/2 and -1*self.height/2 <= y < self.height/2
    
    def passable(self, id):
        return id not in self.obstacles
    
    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse() # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def add_obstacle(self, id):
        self.obstacles.append(id)

def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)    

def plan_path(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    came_from[start] = None

    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            if next not in came_from:
                priority =  heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    
    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    print("in reconstruct path, goal is {}".format(goal))
    print(came_from)
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

#below are Arena functions
def poseConvert(original, to, position):
    if original == 'arena' and to == 'robot':
        x = position[0] * 1000
        y = -1 * position[2] * 1000
        z = 0
        print("Converted position for vector is " + str((x, y, z)))
        return (x, y, z)
    elif original == 'robot' and to == 'arena':
        x = position[0]/1000
        y = position[2]/1000
        z = -1 * position[1]/1000
        return (x, y, z)
    elif original == 'arena' and to == 'grid':
        # x = math.floor(position[0]/0.1)
        # y = math.floor(position[2]/0.1)
        x = int(position[0]/0.1)
        y = int(position[2]/0.1)
        return (x, y)
    elif original == 'robot' and to == 'grid':
        return poseConvert('arena', 'grid', poseConvert('robot', 'arena', position))
    elif original == 'grid' and to == 'arena':
        return (position[0]/10, 0, position[1]/10)
    elif original == 'grid' and to == 'robot':
        return poseConvert('arena', 'robot', poseConvert('grid', 'arena', position))


def initLocA():
    location["A"] = arena.Object(objType=arena.Shape.circle,
        objName='A',
        clickable=True,
        location=(0.3,0.1,-0.5),
        scale=(0.05, 0.05, 0.05),
        rotation=(-0.7, 0, 0, 0.7),
        callback=aCallback,
        )

def aCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("A pressed! go to " + str(location['A'].location))
        goal = poseConvert("arena", "grid", location['A'].location)
        #pose = Pose(x, y, z, angle_z=Angle(degrees=0))
        #robot.behavior.go_to_pose(pose)
        start_navigation(goal)
        location['A'].update(
            color = (255,255,255)
        )
    if event.event_type == arena.EventType.mousedown:
        location['A'].update(
            color = red
        )

def start_navigation(goal):
    robotPos = (robot.pose.position.x, robot.pose.position.y, robot.pose.position.z)
    start = poseConvert("robot", "grid", robotPos)
    print('The start position is {} (robot) {} (grid)'.format(robotPos, start))
    came_from = plan_path(grid, start, goal)
    path = reconstruct_path(came_from, start, goal)

    current = path[0]

    print(path)

    for position in path[1:]:
        global current_direction 

        to_vector = tuple(np.subtract(position, current))
        print(to_vector)

        #caculate rotation
        rotate = angle_between(to_vector, current_direction)
        robot.behavior.turn_in_place(Angle(radians = rotate)).result()

        current_direction = to_vector

        if robot.proximity.last_sensor_reading.distance.distance_mm < 150:
                print("obstacle at {} encountered!".format(position))
                grid.add_obstacle(position)
                start_navigation(goal)

        #calculate distance
        dist = np.linalg.norm(to_vector) * 100
        drive_future = robot.behavior.drive_straight(distance_mm(dist), speed_mmps(50))

        print(drive_future.done())
        while not drive_future.done():

            print('robot.pose is {}'.format(robot.pose))
            if robot.proximity.last_sensor_reading.distance.distance_mm < 150:
                drive_future.cancel()
                print("obstacle at {} encountered!".format(position))
                grid.add_obstacle(position)
                start_navigation(goal) 

            time.sleep(1)
        
        drive_future.result()

        current = position

grid = SquareGrid(20, 20)
# grid.add_obstacle((0, 1))
# grid.add_obstacle((1, 1))          
# grid.add_obstacle((2, 1))          
# goal = (1, -2)
# start = (0, 0)

if __name__ == "__main__":

    print(robot.pose)

    initLocA()
    arena.handle_events()

