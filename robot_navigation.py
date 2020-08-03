import anki_vector
from anki_vector.util import distance_mm, speed_mmps, Pose, Angle
from anki_vector.events import Events
from pyquaternion import Quaternion
import time
import heapq
import arena
import math
import numpy as np
print("before arena init")
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")
print("after")

robot = anki_vector.AsyncRobot()
#robot = anki_vector.Robot()
robot.connect()
location = {}
current_direction = tuple()
current_position = tuple()
current_rotation = tuple()
current = tuple()
red = (255, 0, 0)
cleanUpdate = False
robot_is_not_moving = True
arrived = False

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'
    Source: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python#answer-13849249 """
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

def calibrate_robot(calibrate_to_position, calibrate_to_direction = (1, 0)):
    if cleanUpdate == True:
        pass
        

#below are Arena functions
def tag_callback(event=None):
    ''' Since we expect the position/rotation updates, we can react here.'''
    global current_rotation, current_position, cleanUpdate
    if event.event_action == arena.EventAction.update and \
            event.event_type == arena.EventType.object and robot_is_not_moving == True:
        print("Tag position: " + str(event.position))
        print("Tag rotation: " + str(event.rotation))
        current_position = event.position
        current_rotation = event.rotation

        cleanUpdate = True
        




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
        x = int(position[0]/0.1)
        y = int(position[2]/0.1)
        return (x, y)
    elif original == 'robot' and to == 'grid':
        return poseConvert('arena', 'grid', poseConvert('robot', 'arena', position))
    elif original == 'grid' and to == 'arena':
        return (position[0]/10, 0, position[1]/10)
    elif original == 'grid' and to == 'robot':
        return poseConvert('arena', 'robot', poseConvert('grid', 'arena', position))


def init():
    location["A"] = arena.Object(objType=arena.Shape.circle,
        objName='A',
        clickable=True,
        location=(0.3,0.1,-0.5),
        scale=(0.05, 0.05, 0.05),
        rotation=(-0.7, 0, 0, 0.7),
        callback=aCallback,
        )

    TAG = arena.Object(objName="apriltag_500",
                   transparency=arena.Transparency(True, 0),
                   callback=tag_callback,
                   persist=True)

def aCallback(event=None):
    global current_direction, arrived
    if event.event_type == arena.EventType.mouseup:
        arrived = False
        print("A pressed! go to " + str(location['A'].location))
        goal = poseConvert("arena", "grid", location['A'].location)

        counter = 0
        while cleanUpdate == False:
            time.sleep(1)
            print(str(cleanUpdate) + ' '+ str(counter))
            counter+=1

        x, y, z, w = current_rotation
        quaternionObj = Quaternion(w, x, y, z)
        current_direction = quaternionObj.rotate((0, 0, -1))
        print('Current direction before convert is {}'.format(current_direction))
        current_direction = poseConvert("arena", "grid", current_direction)
        print('Current direction after convert is {}'.format(current_direction))

        start = poseConvert("arena", "grid", current_position)
        print('yo')
        #calibrate_robot(start)

        start_navigation(start, goal)

        location['A'].update(
            color = (255,255,255)
        )
    if event.event_type == arena.EventType.mousedown:
        location['A'].update(
            color = red
        )

def start_navigation(start, goal):
    global robot_is_not_moving, current_direction, arrived

    print('The start position {}'.format(start))

    #start path planning
    came_from = plan_path(grid, start, goal)
    path = reconstruct_path(came_from, start, goal)
    print(path)
    
    current = path[0]
    for next_position in path[1:]:
        robot_is_not_moving = False

        to_vector = tuple(np.subtract(next_position, current))
        print(to_vector)

        #caculate rotation
        rotate = angle_between(to_vector, current_direction)
        robot.behavior.turn_in_place(Angle(radians = rotate), speed = Angle(radians = 1.0)).result()

        current_direction = to_vector

        if robot.proximity.last_sensor_reading.distance.distance_mm < 100:
                print("obstacle at {} encountered!".format(next_position))
                robot_is_not_moving = True
                grid.add_obstacle(next_position)
                start_navigation(current, goal)

        #calculate distance and drive
        dist = np.linalg.norm(to_vector) * 100
        drive_future = robot.behavior.drive_straight(distance_mm(dist), speed_mmps(50))

        while not drive_future.done():
            if robot.proximity.last_sensor_reading.distance.distance_mm < 100:
                drive_future.cancel() #robot stops
                robot_is_not_moving = True
                print("obstacle at {} encountered!".format(next_position))
                grid.add_obstacle(next_position)
                start_navigation(current, goal) 
            time.sleep(1)
            if arrived == True:
                print('arrived!')
                return
        
        #drive_future.result()

        robot_is_not_moving = True

        #calibrate_robot()

        # if arrived == True:
        #     return


        current = next_position
    
    arrived = True
        


grid = SquareGrid(20, 20)

if __name__ == "__main__":

    init()
    arena.handle_events()

