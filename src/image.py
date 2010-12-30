# -*- coding: utf-8 -*-
#
#Image convenience class
#
#By Oipo (kingoipo@gmail.com)

from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

import fmGlobals

import numpy

class Image:
    '''
    Class for storing image data, position and some opengl stuff
    '''

    def __init__(self, image, textureRect, drawRect, dynamicity = GL_DYNAMIC_DRAW_ARB):
        self.image = image
        self.drawRect = drawRect
        self.textureRect = textureRect
        self.dynamicity = dynamicity

        self.textureId = None

        self.VBOTexCoords = None
        self.VBOVertices = None

        if fmGlobals.vbos:
            x, y, w, h = textureRect
            dx, dy, dw, dh = drawRect

            self.TexCoords = numpy.zeros((4, 2), 'f')

            self.TexCoords[0, 0] = x
            self.TexCoords[0, 1] = y+h

            self.TexCoords[1, 0] = x+w
            self.TexCoords[1, 1] = y+h

            self.TexCoords[2, 0] = x+w
            self.TexCoords[2, 1] = y

            self.TexCoords[3, 0] = x
            self.TexCoords[3, 1] = y


            self.Vertices = numpy.zeros((4, 3), 'f')

            self.Vertices[0, 0] = dx
            self.Vertices[0, 1] = dy

            self.Vertices[1, 0] = dx+dw
            self.Vertices[1, 1] = dy

            self.Vertices[2, 0] = dx+dw
            self.Vertices[2, 1] = dy+dh

            self.Vertices[3, 0] = dx
            self.Vertices[3, 1] = dy+dh


    def setDrawRect(self, drawRect):
        self.drawRect = drawRect

        if fmGlobals.vbos:
            self.Vertices = numpy.zeros((4, 3), 'f')
            dx, dy, dw, dh = drawRect

            self.Vertices[0, 0] = dx
            self.Vertices[0, 1] = dy

            self.Vertices[1, 0] = dx+dw
            self.Vertices[1, 1] = dy

            self.Vertices[2, 0] = dx+dw
            self.Vertices[2, 1] = dy+dh

            self.Vertices[3, 0] = dx
            self.Vertices[3, 1] = dy+dh

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOVertices)
            glBufferData(GL_ARRAY_BUFFER_ARB, ADT.arrayByteCount(self.Vertices), (self.Vertices), self.dynamicity)

            self.Vertices = None

    def buildVBO(self):
        #Generate and bind the vertice coordinate buffer
    	self.VBOVertices = int(glGenBuffersARB(1))
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOVertices)
        glBufferData(GL_ARRAY_BUFFER_ARB, ADT.arrayByteCount(self.Vertices), (self.Vertices), self.dynamicity)

        #Generate and bind the texture coordinate buffer
        self.VBOTexCoords = int(glGenBuffersARB(1))
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOTexCoords)
        glBufferData(GL_ARRAY_BUFFER_ARB, ADT.arrayByteCount(self.TexCoords), (self.TexCoords), self.dynamicity)

        #Delete from RAM, it's in VRAM now
        self.Vertices = None
        self.TexCoords = None
