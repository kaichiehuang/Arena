import arena
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps, Angle, Pose
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")

robot = anki_vector.Robot()
red = (255, 0, 0)
location = {}

def initLocA():
    location["A"] = arena.Object(objType=arena.Shape.circle,
        objName='A',
        clickable=True,
        location=(0,0.1,-0.5),
        scale=(0.05, 0.05, 0.05),
        rotation=(-0.7, 0, 0, 0.7),
        callback=aCallback,
        )

def initLocB():
    location["B"] = arena.Object(objType=arena.Shape.circle,
        objName='B',
        clickable=True,
        location=(0.5,0.1,-0.7),
        scale=(0.05, 0.05, 0.05),
        rotation=(-0.7, 0, 0, 0.7),
        callback=bCallback,
        )

def initLocC():
    location["C"] = arena.Object(objType=arena.Shape.circle,
        objName='C',
        clickable=True,
        location=(-0.5,0.1,-0.7),
        scale=(0.05, 0.05, 0.05),
        rotation=(-0.7, 0, 0, 0.7),
        callback=cCallback,
        )

def poseConvert(original, position):
    if original == 'arena':
        x = position[0]
        y = -1 * position[2]
        z = position[1]
        print("Converted position for vector is " + str((x*100, y*100, 0)))
        return (x*1000, y*1000, 0)
    else:
        x = position[0]
        y = position[2]
        z = -1 * position[1]
        return (x, y, z)

def aCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("A pressed! go to " + str(location['A'].location))
        x, y, z = poseConvert("arena", location['A'].location)
        pose = Pose(x, y, z, angle_z=Angle(degrees=0))
        robot.behavior.go_to_pose(pose)
        location['A'].update(
            color = (255,255,255)
        )
    if event.event_type == arena.EventType.mousedown:
        location['A'].update(
            color = red
        )

def bCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("B pressed! go to " + str(location['B'].location))
        x, y, z = poseConvert("arena", location['B'].location)
        pose = Pose(x, y, z, angle_z=Angle(degrees=0))
        robot.behavior.go_to_pose(pose)
        location['B'].update(
            color = (255,255,255)
        )
    if event.event_type == arena.EventType.mousedown:
        location['B'].update(
            color = red
        )

def cCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("C pressed! go to " + str(location['C'].location))
        x, y, z = poseConvert("arena", location['C'].location)
        pose = Pose(x, y, z, angle_z=Angle(degrees=0))
        robot.behavior.go_to_pose(pose)
        location['C'].update(
            color = (255,255,255)
        )
    if event.event_type == arena.EventType.mousedown:
        location['C'].update(
            color = red
        )
        


def initAll():
    initLocA()
    initLocB()
    initLocC()




if __name__ == "__main__":
    #robot.connect()
    initAll()

arena.handle_events()