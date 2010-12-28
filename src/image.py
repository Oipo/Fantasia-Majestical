from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

import fmGlobals

import numpy

class Image:
    '''
    Class for storing image data, position and some opengl stuff
    '''

    def __init__(self, image, textureRect, drawRect, dynamicity):
        self.image = image
        self.drawRect = drawRect
        self.textureRect = textureRect
        self.dynamicity = dynamicity

        self.textureId = None

        self.offsetv = None
        self.offsett = None

        self.VBO = None
        self.VBOData = None

    def setDrawRect(self, drawRect):
        self.drawRect = drawRect

        if fmGlobals.vbos:
            self.createVBOData()

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBO)
            glBufferData(GL_ARRAY_BUFFER_ARB, ADT.arrayByteCount(self.VBOData), (self.VBOData), self.dynamicity)

            self.VBOData = None

    def createVBOData(self):
        x, y, w, h = textureRect
        dx, dy, dw, dh = drawRect

        self.VBOData = numpy.zeros((8, 2), 'f')

        self.VBOData[0, 0] = x #tex
        self.VBOData[0, 1] = y+h

        self.VBOData[1, 0] = dx #vert
        self.VBOData[1, 1] = dy

        self.VBOData[2, 0] = x+w #tex
        self.VBOData[2, 1] = y+h

        self.VBOData[3, 0] = dx+dw #vert
        self.VBOData[3, 1] = dy

        self.VBOData[4, 0] = x+w
        self.VBOData[4, 1] = y

        self.VBOData[5, 0] = dx+dw
        self.VBOData[5, 1] = dy+dh

        self.VBOData[6, 0] = x
        self.VBOData[6, 1] = y

        self.VBOData[7, 0] = dx
        self.VBOData[7, 1] = dy+dh

    def buildVBO(self):
        self.createVBOData()

        #Generate and bind the vbo
    	self.VBOVertices = int(glGenBuffersARB(1))
        glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBO)
        glBufferData(GL_ARRAY_BUFFER_ARB, ADT.arrayByteCount(self.VBOData), (self.VBOData), self.dynamicity)

        #Delete from RAM, it's in VRAM now
        self.VBOData = None
