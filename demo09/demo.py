#Copyright (c) 2018-2020 William Emerison Six
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

# PURPOSE
#
# Make the rotations work correctly by thinking about the problem
# more clearly
#
# In the previous demo, The initial translate is effectively canceled out,
# leaving a rotation and then a translation.
# Translate inverse(Translate) Rotate Translate
#
# Translate inverse(Translate) = Identity.  i.e. 5 * 1/5 = 1,
# so we really just need to do a rotation first, and then a translation,
# but this can be counterintuitive at first because we like to think
# in relative terms.

# To understand why the code in this demo works, you can think
# about it in one of two ways.  Either there is a sequence
# of function calls, all of which happen relative to the global
# origin; or, you can read the transformations backwards,
# where instead of doing operations on points, the operations
# all modifying the current axis to a new relative axises,
# and all subsequent functions move those relative axises to
# new relative axises.

# Strong suggestion for computer graphics, especially from
# modelspace to global space:
# Read the transformations in the latter.

# See the transformations below, and the associated animated gifs.



import sys
import os
import numpy as np
import math
from OpenGL.GL import *
import glfw

if not glfw.init():
    sys.exit()

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR,1)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR,4)

window = glfw.create_window(500,
                            500,
                            "ModelViewProjection Demo 9",
                            None,
                            None)
if not window:
    glfw.terminate()
    sys.exit()

# Make the window's context current
glfw.make_context_current(window)

# Install a key handler
def on_key(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window,1)
glfw.set_key_callback(window, on_key)

glClearColor(0.0,
             0.0,
             0.0,
             1.0)


glMatrixMode(GL_PROJECTION);
glLoadIdentity();
glMatrixMode(GL_MODELVIEW);
glLoadIdentity();


def draw_in_square_viewport():

    glClearColor(0.2, #r
                 0.2, #g
                 0.2, #b
                 1.0) #a
    glClear(GL_COLOR_BUFFER_BIT)

    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    min = width if width < height else height

    glViewport(int(0.0 + (width - min)/2.0),  #min x
               int(0.0 + (height - min)/2.0), #min y
               min,                           #width x
               min)                           #width y

    glEnable(GL_SCISSOR_TEST)
    glScissor(int(0.0 + (width - min)/2.0),  #min x
              int(0.0 + (height - min)/2.0), #min y
              min,                           #width x
              min)                           #width y

    glClearColor(0.0, #r
                 0.0, #g
                 0.0, #b
                 1.0) #a
    glClear(GL_COLOR_BUFFER_BIT)
    glDisable(GL_SCISSOR_TEST)



class Vertex:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def translate(self, tx, ty):
        return Vertex(x=self.x + tx, y=self.y + ty)

    def scale(self, x, y):
        return Vertex(x=self.x * x, y=self.y * y)

    def rotate(self,angle_in_radians):
        return Vertex(x= self.x * math.cos(angle_in_radians) - self.y * math.sin(angle_in_radians),
                      y= self.x * math.sin(angle_in_radians) + self.y * math.cos(angle_in_radians))

    # NEW
    # removed rotate_around, as it was useless for our purpose

class Paddle:
    def __init__(self,vertices, r, g, b, global_position, rotation=0.0, offset_x=0.0, offset_y=0.0):
        self.vertices = vertices
        self.r = r
        self.g = g
        self.b = b
        self.rotation = rotation
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.global_position = global_position


paddle1 = Paddle(vertices=[Vertex(x=-10.0, y=-30.0),
                           Vertex(x= 10.0, y=-30.0),
                           Vertex(x= 10.0, y=30.0),
                           Vertex(x=-10.0, y=30.0)],
                 r=0.578123,
                 g=0.0,
                 b=1.0,
                 global_position=Vertex(-90.0,0.0))

paddle2 = Paddle(vertices=[Vertex(x=-10.0, y=-30.0),
                           Vertex(x= 10.0, y=-30.0),
                           Vertex(x= 10.0, y=30.0),
                           Vertex(x=-10.0, y=30.0)],
                 r=1.0,
                 g=0.0,
                 b=0.0,
                 global_position=Vertex(90.0,0.0))


def handle_movement_of_paddles():
    global paddle1, paddle2

    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        paddle1.offset_y -= 10.0
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        paddle1.offset_y += 10.0
    if glfw.get_key(window, glfw.KEY_K) == glfw.PRESS:
        paddle2.offset_y -= 10.0
    if glfw.get_key(window, glfw.KEY_I) == glfw.PRESS:
        paddle2.offset_y += 10.0

    global paddle_1_rotation, paddle_2_rotation

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        paddle1.rotation += 0.1
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        paddle1.rotation -= 0.1
    if glfw.get_key(window, glfw.KEY_J) == glfw.PRESS:
        paddle2.rotation += 0.1
    if glfw.get_key(window, glfw.KEY_L) == glfw.PRESS:
        paddle2.rotation -= 0.1


# Loop until the user closes the window
while not glfw.window_should_close(window):
    # Poll for and process events
    glfw.poll_events()

    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # render scene
    draw_in_square_viewport()
    handle_movement_of_paddles()

    # draw paddle1
    glColor3f(paddle1.r,
              paddle1.g,
              paddle1.b)


    # if you read the operations below as rotate, translate1, translate2,
    # you should imagine it as follows
    # eog ../images/rotation1F.gif

    # if instead you read them backwards, imagine the transformations
    # as follows
    # eog ../images/rotation1B.gif

    # side note.  Typically I use a debugger as an interactive evaluator,
    # in order to understand how code which I do not understand works.
    # In computer graphics, the debugger is of limited help because
    # the transformations on the individual points is not worth
    # thinking about, and therefore the intermediat results
    # are worthless for reasoning.
    #
    # In order to be successful, I highly recommend reading the transformations
    # backwards, with a moving/rotating/scaled axises.
    #
    # (This advise will be modified when I introduce transformation stacks,
    # but the same principle will apply.  Also, on the note of transformation
    # stacks, N.B. that the scaling from world space to ndc is shared
    # for both paddles, and that changing the code in one place would
    # required changing the code for all shapes.)
    #


    glBegin(GL_QUADS)
    for model_space in paddle1.vertices:
        world_space = model_space.rotate(paddle1.rotation) \
                                 .translate(tx=paddle1.global_position.x,
                                            ty=paddle1.global_position.y) \
                                 .translate(tx=paddle1.offset_x,
                                            ty=paddle1.offset_y)

        ndc_space = world_space.scale(x=1.0/100.0,
                                      y=1.0/100.0)
        glVertex2f(ndc_space.x,
                   ndc_space.y)
    glEnd()
    # draw paddle2
    glColor3f(paddle2.r,
              paddle2.g,
              paddle2.b)

    # Same thing for the second paddle.
    # eog ../images/rotation2F.gif

    # eog ../images/rotation2B.gif
    glBegin(GL_QUADS)
    for model_space in paddle2.vertices:
        world_space = model_space.rotate(paddle2.rotation) \
                                 .translate(tx=paddle2.global_position.x,
                                            ty=paddle2.global_position.y) \
                                 .translate(tx=paddle2.offset_x,
                                            ty=paddle2.offset_y)

        ndc_space = world_space.scale(x=1.0/100.0,
                                      y=1.0/100.0)
        glVertex2f(ndc_space.x,
                   ndc_space.y)
    glEnd()



    # done with frame, flush and swap buffers
    # Swap front and back buffers
    glfw.swap_buffers(window)

glfw.terminate()
