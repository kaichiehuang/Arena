# import anki_vector
# import io
# from PIL import Image

# with anki_vector.Robot() as robot:
#     for photo_info in robot.photos.photo_info:
#         print(f"Opening photo {photo_info.photo_id}")
#         photo = robot.photos.get_photo(photo_info.photo_id)
#         image = Image.open(io.BytesIO(photo.image))
#         image.show()
# import anki_vector

# with anki_vector.Robot() as robot:
# #     robot.camera.close_camera_feed()
#     image = robot.camera.capture_single_image()
#      #image = robot.camera.latest_image
#     image.raw_image.show()

# import anki_vector

# with anki_vector.Robot() as robot:
#     for photo_info in robot.photos.photo_info:
#         print(f"photo_info.photo_id: {photo_info.photo_id}") # the id to use to grab a photo from the robot
#         print(f"photo_info.timestamp_utc: {photo_info.timestamp_utc}") # utc timestamp of when the photo was taken (according to the robot)

import multiprocessing as mp

from anki_vector import opengl

ctx = mp.get_context('spawn')
close_event = ctx.Event()
input_intent_queue = ctx.Queue(maxsize=10)
nav_map_queue = ctx.Queue(maxsize=10)
world_frame_queue = ctx.Queue(maxsize=10)
extra_render_function_queue = ctx.Queue(maxsize=1)
user_data_queue = ctx.Queue()
process = ctx.Process(target=opengl.main,
                      args=(close_event,
                            input_intent_queue,
                            nav_map_queue,
                            world_frame_queue,
                            extra_render_function_queue,
                            user_data_queue),
                      daemon=True)
process.start()