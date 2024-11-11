from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from cg_helper import *

window = create_window("Das ist ein Testfenster")

glClearColor(0.8, 0.2, 0.1, 0)

# load shader programs
vertex_shader_source_triangle = read_shader_source('C:\CG_Code\Woche10\start\shaders\triangle.vertex')
fragment_shader_source_triangle = read_shader_source('C:\CG_Code\Woche10\start\shaders\triangle.fragment')

shader_program_triangle = create_shader_program(vertex_shader_source_triangle, fragment_shader_source_triangle)



# VAO and VBO for triangle
vao_triangle = glGenVertexArrays(1)
glBindVertexArray(vao_triangle)

vertex_data_triangle = [-1, -1, 0,
                        1, -0.5, 0,
                        0,  1, 0]

vertex_buffer_triangle = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_triangle)

array_type = (GLfloat * len(vertex_data_triangle))
glBufferData(GL_ARRAY_BUFFER,
             len(vertex_data_triangle) * ctypes.sizeof(ctypes.c_float),
             array_type(*vertex_data_triangle),
             GL_STATIC_DRAW)

#connection to vertex shader (in-attributes)
attr_id = 0
glVertexAttribPointer(
    attr_id,            # attribute 0.
    3,                  # components per vertex attribute
    GL_FLOAT,           # type
    False,              # to be normalized?
    0,                  # stride
    None                # array buffer offset
)
glEnableVertexAttribArray(attr_id)


while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and not glfw.window_should_close(window)):
    #clear buffer first
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #general approach to draw an object: activate shader, bind VAO, call draw
    glUseProgram(shader_program_triangle)
    glBindVertexArray(vao_triangle)
    glDrawArrays(GL_TRIANGLES, 0, 3)


    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()

