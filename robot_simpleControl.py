import arena
import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps
arena.init("oz.andrew.cmu.edu", "realm", "kaichieh1")

robot = anki_vector.Robot()
red = (255, 0, 0)
button = {}

def initGoStraightButton():
    button["straight"] = arena.Object(objType=arena.Shape.cube,
        objName='straight',
        clickable=True,
        location=(0,3,-3),
        scale=(0.6, 0.6, 0.6),
        callback=goStraightCallback,
        )

def initTurnRightButton():
    button["right"] = arena.Object(objType=arena.Shape.cube,
        objName='right',
        clickable=True,
        location=(1,3,-3),
        scale=(0.6, 0.6, 0.6),
        callback=turnRightCallback,
        )

def initTurnLeftButton():
    button["left"] = arena.Object(objType=arena.Shape.cube,
        objName='left',
        clickable=True,
        location=(-1,3,-3),
        scale=(0.6, 0.6, 0.6),
        callback=turnLeftCallback,
        )

def initAll():
    initGoStraightButton()
    initTurnRightButton()
    initTurnLeftButton()

def goStraightCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("go straight!")
        button["straight"].update(
            color = (255,255,255)
        )
        robot.behavior.drive_straight(distance_mm(200), speed_mmps(50))
    if event.event_type == arena.EventType.mousedown:
        button["straight"].update(
            color = red
        )


def turnRightCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("turn right!")
        button["right"].update(
            color = (255,255,255)
        )
        robot.behavior.turn_in_place(degrees(-90))
    if event.event_type == arena.EventType.mousedown:
        button["right"].update(
            color = red
        )
        

def turnLeftCallback(event=None):
    if event.event_type == arena.EventType.mouseup:
        print("turn left!")
        button["left"].update(
            color = (255,255,255)
        )
        robot.behavior.turn_in_place(degrees(90))
    if event.event_type == arena.EventType.mousedown:
        button["left"].update(
            color = red
        )


if __name__ == "__main__":
    robot.connect()
    initAll()

arena.handle_events()