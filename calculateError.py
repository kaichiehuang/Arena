import arena
import time
from scipy.spatial import distance
#arena.init("oz.andrew.cmu.edu", "realm", "kaichieh5")
arena.init("arena.andrew.cmu.edu", "realm", "kaichieh5")

fixedCamera = "test"
cam_last_position = [0.0,0.0,0.0]
number = []
numberBackground = []

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

def show_button_callback(event=None):
    if event.event_type == arena.EventType.mousedown:
        draw_dial_pad()

def hide_button_callback(event=None):
    if event.event_type == arena.EventType.mousedown:
        erase_dial_pad()

def draw_dial_pad():
    create_number_button(-0.5, 1, '1')#1
    create_number_button(0, 1, '2')#2
    create_number_button(0.5, 1, '3')#3
    create_number_button(-0.5, 0.5, '4')#4
    create_number_button(0, 0.5, '5')#5
    create_number_button(0.5, 0.5, '6')#6
    create_number_button(-0.5, 0, '7')#7
    create_number_button(0, 0, '8')#8
    create_number_button(0.5, 0, '9')#9
    create_number_button(-0.5, -0.5, '.')#.
    create_number_button(0, -0.5, '0')#0
    create_number_button(0.5, -0.5, 'GO!')#Go!

def erase_dial_pad():
    global number, numberBackground
    for i in range(len(number)):
        number[i].delete()
        numberBackground[i].delete()
    number = []
    numberBackground = []

def create_number_button(dx, dy, content):
    global number, numberBackground
    number.append(arena.Object(
        persist=False,
        objName=content,
        objType=arena.Shape.text,
        text=content,
        location = (cam_last_position[0]+dx, cam_last_position[1]+dy, cam_last_position[2]-1.5),
        scale=(0.5, 0.5, 0.5),
        color = (0, 0, 0)
    ))
    numberBackground.append(arena.Object(objName=content + "_circle",
             objType=arena.Shape.circle,
             location = (cam_last_position[0]+dx, cam_last_position[1]+dy, cam_last_position[2]-1.5),
             rotation=(0, 0, 0, 1),
             scale=(0.1, 0.1, 0.1),
             color=(255, 255, 255), #white
             clickable=True,
             callback = button_callback,
             ))
        


cameraStr = "camera_" + fixedCamera + "_" + fixedCamera

my_camera = arena.Object(objName=cameraStr,
                         transparency=arena.Transparency(True, 0),
                         callback=camera_callback,
                         persist=False)

showButton = arena.Object(objName='showDialPad',
                                 objType=arena.Shape.circle,
                                 location = (cam_last_position[0]-1, cam_last_position[1], cam_last_position[2]-1),
                                 color = (0, 255, 0), #green
                                 scale=(0.1, 0.1, 0.1),
                                 clickable=True,
                                 callback=show_button_callback
                                 )

showButtonText = arena.Object(objName='showDialPadText',
                                    objType = arena.Shape.text,
                                    text = 'Show',
                                    location = (cam_last_position[0]-1, cam_last_position[1], cam_last_position[2]-1),
                                    color = (255, 255, 255),
                                    scale=(0.3, 0.3, 0.3)
                                    )


# number = arena.Object(
#         persist=False,
#         objName="number",
#         objType=arena.Shape.text,
#         text="1",
#         location = (cam_last_position[0], cam_last_position[1], cam_last_position[2]-1.5),
#         scale=(0.5, 0.5, 0.5),
#         color = (0, 0, 0)
#     )

# numberBackgroud = arena.Object(objName="circle",
#              objType=arena.Shape.circle,
#              location = (cam_last_position[0], cam_last_position[1], cam_last_position[2]-1.5),
#              rotation=(0, 0, 0, 1),
#              scale=(0.1, 0.1, 0.1),
#              color=(255, 255, 255), #white
#              clickable=True,
#              callback = button_callback,
#              )

draw_dial_pad()


arena.handle_events()


