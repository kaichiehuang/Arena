import arena
import time
from scipy.spatial import distance
#arena.init("oz.andrew.cmu.edu", "realm", "kaichieh5")
arena.init("arena.andrew.cmu.edu", "realm", "kaichieh5")

fixedCamera = "test"
cam_last_position = [0.0,0.0,0.0]
tag_position = [1, 1, 1]
errorNum = int()

def camera_callback(event=None):
    #print(event.position)
    global cam_last_position
    cam_moved = distance.euclidean(event.position, cam_last_position)
    if cam_moved > 0.25:
        cam_last_position = event.position
        print(event.position)

def button_callback(event=None):
    if event.event_type == arena.EventType.mousedown:
        print("clicked!")

# def tag_callback(event=None):
#     ''' Since we expect the position/rotation updates, we can react here.
#     '''
#     global tag_position
#     if event.event_action == arena.EventAction.update and \
#             event.event_type == arena.EventType.object:
#         #tag_position = event.position
#         print(event.position)

       

cameraStr = "camera_" + fixedCamera + "_" + fixedCamera

my_camera = arena.Object(objName=cameraStr,
                         transparency=arena.Transparency(True, 0),
                         callback=camera_callback,
                         persist=False)

arena.Object(objName="test_click",
             objType=arena.Shape.sphere,
             location = (0,1,-0.5),
             rotation=(0, 0, 0, 1),
             scale=(0.1, 0.1, 0.1),
             color=(255,0,0), #red
             clickable=True,
             callback = button_callback,
             )

# TAG = arena.Object(objName="apriltag_400",
#                    transparency=arena.Transparency(True, 0),
#                    callback=tag_callback,
#                    persist=True)

def draw_center(x, y, z):
    arena.Object(objName="cone",
             objType=arena.Shape.cone,
             location = (x, y, z),
             scale=(0.1, 0.1, 0.1),
             #rotation=(0.7, 0, 0, 0.7),
             #parent=TAG.objName,
             color = (255, 0, 0),
            )

# number = arena.Object(
#         persist=False,
#         objName="number",
#         objType=arena.Shape.text,
#         text="testtesttest",
#         # location = (cam_last_position[0], cam_last_position[1], cam_last_position[2]-1.5),
#         location = (-0.2, 0.15, -0.5),
#         scale=(0.2, 0.2, 0.2),
#         parent = cameraStr,
#         color = (255, 255, 255)
#     )

def draw_error_num(errorNum):
    arena.Object(
        persist=False,
        objName="errorNum",
        objType=arena.Shape.text,
        text= "Error entered: {}".format(errorNum),
        location = (0, 0.15, -0.5),
        scale=(0.2, 0.2, 0.2),
        parent = cameraStr,
        color = (255, 255, 255),
        ttl = 3,
    )

def demonstrate(errorNum):
    nx, ny, nz = calculate_location(errorNum)
    arena.Object(objName="sphere",
             location = (nx, ny, nz),
             objType=arena.Shape.sphere,
             scale=(0.1, 0.1, 0.1),
             color = (0, 255, 0),
             )


def calculate_location(errorNum):
    global x, y, z

    return x + errorNum, y + errorNum, z + errorNum


x, y, z = input("Enter location (format: x y z): ").split()
draw_center(x, y, z)

errorNum = input("Enter an error number: ")
draw_error_num(errorNum)
demonstrate(errorNum)


arena.handle_events()