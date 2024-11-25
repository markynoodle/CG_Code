import glm
import math
import numpy as np

from cg_helper import *

class Cube:
    def __init__(self, rotational_speed, rotational_axis):
        self.model_matrix = glm.mat4()
        self.rotational_speed = rotational_speed
        self.rotational_axis = rotational_axis

        # load shader programs
        vertex_shader_source_cube = read_shader_source('cube.vertex')
        fragment_shader_source_cube = read_shader_source('cube.fragment')

        self.shader_program_cube = create_shader_program(vertex_shader_source_cube, fragment_shader_source_cube)

        # Define cube vertices and indices
        vertices = np.array([
            -0.5, -0.5, -0.5,
            0.5, -0.5, -0.5,
            0.5, 0.5, -0.5,
            -0.5, 0.5, -0.5,
            -0.5, -0.5, 0.5,
            0.5, -0.5, 0.5,
            0.5, 0.5, 0.5,
            -0.5, 0.5, 0.5
        ], dtype=np.float32)

        self.indices = np.array([
            0, 2, 1, 0, 3, 2,  # Back face
            6, 7, 4, 4, 5, 6,  # Front face
            0, 1, 4, 1, 5, 4,  # Bottom face
            2, 3, 7, 2, 7, 6,  # Top face
            0, 4, 3, 3, 4, 7,  # Left face
            1, 5, 2, 2, 5, 6  # Right face
        ], dtype=np.uint32)

        colors = np.random.rand(vertices.size).astype(np.float32)

        # VAO for cube
        self.vao_cube = glGenVertexArrays(1)
        glBindVertexArray(self.vao_cube)

        # VBO for positions
        vertex_buffer_cube = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_cube)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        # connection to vertex shader (in-attributes)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # VBO for indices
        face_buffer_cube = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, face_buffer_cube)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # VBO for colors
        color_buffer_cube = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, color_buffer_cube)
        glBufferData(GL_ARRAY_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)

        # connection to vertex shader (in-attributes)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * colors.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)


    def translate(self, translation_vector):
        self.model_matrix = glm.translate(self.model_matrix, translation_vector)

    def rotate(self):
        self.model_matrix = glm.rotate(self.model_matrix, math.pi / 180 * self.rotational_speed, self.rotational_axis)

    def draw(self, view_matrix, projection_matrix):
        # rotate first
        self.rotate()

        # general approach to draw an object: activate shader, bind VAO, call draw
        glUseProgram(self.shader_program_cube)

        # send matrices to shader
        view_loc = glGetUniformLocation(self.shader_program_cube, 'view_matrix')
        projection_loc = glGetUniformLocation(self.shader_program_cube, 'projection_matrix')
        model_loc = glGetUniformLocation(self.shader_program_cube, 'model_matrix')

        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view_matrix))
        glUniformMatrix4fv(projection_loc, 1, GL_FALSE, glm.value_ptr(projection_matrix))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(self.model_matrix))

        glBindVertexArray(self.vao_cube)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

