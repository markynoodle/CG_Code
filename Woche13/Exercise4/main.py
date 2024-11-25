import random
import math
from Sphere import *

os.chdir(os.path.dirname(__file__)) #fix for vs studio users: set current working directory

window = create_window("Das ist ein Testfenster")

glClearColor(0.5, 0.5, 0.5, 0)

position_sphere1 = glm.vec3(10,5,4)
position_sphere2 = glm.vec3(-5,-9,-13)

sphere1 = Sphere(random.randint(0, 100) / 1000, glm.vec3(random.randint(0, 100) / 100, random.randint(0, 100) / 100, random.randint(0, 100) / 100), position_sphere2-position_sphere1, glm.vec3(0.8,0.5,0.2))
sphere1.translate(position_sphere1)
sphere2 = Sphere(random.randint(0, 100) / 1000, glm.vec3(random.randint(0, 100) / 100, random.randint(0, 100) / 100, random.randint(0, 100) / 100),position_sphere1-position_sphere2, glm.vec3(0.1,0.2,0.9))
sphere2.translate(position_sphere2)

glEnable(GL_DEPTH_TEST) # makes sure that the distances to camera of objects are compared
glDepthFunc(GL_LESS) # tells the depth test to render the fragment with the least depth

camera_position = glm.vec3(10,10,10)
view_matrix = glm.lookAt(camera_position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0)) # camera position, camera target, up vector
projection_matrix = glm.perspective(glm.radians(60.0), 800.0/800.0, 0.1, 1000.0) # FoV, Aspect Ratio, Near Clipping Plane, Far Clipping Plane

fly = False
def key_callback(window, key, scancode, action, mods):
    global view_matrix, camera_position, fly
    if key == glfw.KEY_I and action == glfw.PRESS:
        camera_position = camera_position * 0.7
    if key == glfw.KEY_O and action == glfw.PRESS:
        camera_position = camera_position * 1.3

    if key == glfw.KEY_F and action == glfw.PRESS:
        fly = not fly

    view_matrix = glm.lookAt(camera_position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))  # camera position, camera target, up vector

glfw.set_key_callback(window, key_callback)


while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window)):
    #clear buffer first
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if fly:
        dx = camera_position.x
        dz = camera_position.z
        radius = math.sqrt(camera_position.x**2 + camera_position.z**2)

        # calculate the angle in radians
        angle_radians = np.arctan2(dz, dx)
        new_angle_radians = angle_radians - np.radians(0.1) # for clockwise rotation

        # set new camera positions
        camera_position.x = radius * np.cos(new_angle_radians)
        camera_position.z = radius * np.sin(new_angle_radians)

        view_matrix = glm.lookAt(camera_position, glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))  # camera position, camera target, up vector

    if Sphere.check_collision(sphere1, sphere2):
        print("Collision")
        sphere1.reverse_direction()
        sphere2.reverse_direction()

    sphere1.draw(view_matrix, projection_matrix)
    sphere2.draw(view_matrix, projection_matrix)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()

