from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *
from OpenGL.arrays import ArrayDatatype as ADT

from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *

import fmGlobals

mod = False
try:
    import glmod
    mod = True
except:
    pass

from image import *

class GLWidget(QGLWidget):
    '''
    Widget for drawing everything, and for catching mouse presses and similar
    '''
    
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.x = 0
        self.images = dict()
        self.lastMousePos = [0, 0]
        self.camera = [0, 0]
        self.layers = []
        self.zoom = 1
        self.VBOVertices = None
        self.VBOTexCoords = None
        self.VBOBuffer = 0
        self.offsetv = 0
        self.offsett = 0
        self.vbolist = []

    #GL functions
    def paintGL(self):
        '''
        Drawing routine
        '''
        
        glClear(GL_COLOR_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(self.camera[0], self.camera[1], 1)
        glScaled(self.zoom, self.zoom, 0)

        if fmGlobals.vbos:
            for layer in self.layers:
                for img in self.images[layer]:
                    self.vbolist.append(img.textureId)
                    self.vbolist.append(img.VBOTexCoords)
                    self.vbolist.append(img.VBOVertices)
            glmod.drawVBO(tuple(self.vbolist))

            #glmod.drawVBO2(tuple(self.vbolist))
        else:
            for layer in self.layers:
                for img in self.images[layer]:
                    self.drawImage(img)

        glScaled(1/self.zoom, 1/self.zoom, 0)
        glTranslatef(-self.camera[0], -self.camera[1], 1)
        glPopMatrix()

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)

    def initializeGL(self):
        '''            self.VBOTexCoords = int(glGenBuffersARB(1))
        Initialize GL
        '''

        glEnable(GL_TEXTURE_RECTANGLE_ARB)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, self.width(), self.height())
        glClearColor(0.0, 0.0, 0.0, 0.0)

        if mod and not glInitVertexBufferObjectARB():
            fmGlobals.vbos = True
            print "using VBOs"
            self.VBOVertices = int(glGenBuffersARB(1))
            self.VBOTexCoords = int(glGenBuffersARB(1))

        qimg = QImage("test.png")
        for x in range(20):
            for y in range(20):
                self.createImage(qimg, 1, (0, 0, 63, 63), (x*16, y*16, 16, 16))

    #util functions
    def createImage(self, qimage, layer, textureRect, drawRect, dynamicity = GL_STATIC_DRAW_ARB):
        '''
        image is from image.py
        texture is an int, pointing to the correct location in VRAM
        '''

        image = Image(qimage, textureRect, drawRect, dynamicity)

        img = self.convertToGLFormat(image.image)
        texture = glGenTextures(1)
        imgdata = img.bits().asstring(img.numBytes())

        glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture)

        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata);

        image.textureId = texture

        if fmGlobals.vbos:
            #image.buildVBO()
            pass

        if layer not in self.images:
            self.images[layer] = []
            self.layers = self.images.keys()
            self.layers.sort()

        self.images[layer].append(image)

        if fmGlobals.vbos:
            '''self.fillBuffers(image)
            self.vbolist = [self.VBOTexCoords, self.VBOVertices]
            for layer in self.layers:
                for img in self.images[layer]:#leave it here, removing it increases CPU consumption against expectations
                    self.vbolist.append(img.textureId)'''
            image.buildVBO()


        return image

    def fillBuffers(self, image = None):
        size = 0
        vertByteCount = texByteCount = 0

        for layer in self.layers:
            size += len(self.images[layer])
            vertByteCount = ADT.arrayByteCount(self.images[layer][0].Vertices)
            texByteCount = ADT.arrayByteCount(self.images[layer][0].TexCoords)

        print vertByteCount, texByteCount, size
        print self.VBOBuffer

        if self.VBOBuffer <= size or image == None:

            self.VBOBuffer = glmod.nextPowerOfTwo(size)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOVertices)
            glBufferData(GL_ARRAY_BUFFER_ARB, self.VBOBuffer*vertByteCount, None, GL_STATIC_DRAW_ARB)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOTexCoords)
            glBufferData(GL_ARRAY_BUFFER_ARB, self.VBOBuffer*texByteCount, None, GL_STATIC_DRAW_ARB)

        self.offsetv = self.offsett = 0

        for layer in self.layers:
            for img in self.images[layer]:
                img.offsetv = self.offsetv
                img.offsett = self.offsett

                glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOVertices)
                glBufferSubData(GL_ARRAY_BUFFER_ARB, self.offsetv, ADT.arrayByteCount(img.Vertices), img.Vertices)

                glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOTexCoords)
                glBufferSubData(GL_ARRAY_BUFFER_ARB, self.offsett, ADT.arrayByteCount(img.TexCoords), img.TexCoords)

                self.offsetv += ADT.arrayByteCount(img.Vertices)
                self.offsett += ADT.arrayByteCount(img.TexCoords)

        '''else:
            image.offsetv = self.offsetv
            image.offsett = self.offsett

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOVertices)
            glBufferSubData(GL_ARRAY_BUFFER_ARB, self.offsetv, ADT.arrayByteCount(image.Vertices), image.Vertices)

            glBindBuffer(GL_ARRAY_BUFFER_ARB, self.VBOTexCoords)
            glBufferSubData(GL_ARRAY_BUFFER_ARB, self.offsett, ADT.arrayByteCount(image.TexCoords), image.TexCoords)

            self.offsetv += ADT.arrayByteCount(image.Vertices)
            self.offsett += ADT.arrayByteCount(image.TexCoords)'''



    def deleteImage(self, image):
        '''
        textures can be a list, but doesn't have to be.
        '''

        glDeleteTextures(image.textureId)

        if fmGlobals.vbos:
            glDeleteBuffers(image.VBOVertices)
            glDeleteBuffers(image.VBOTexCoords)

    def drawImage(self, image):
        if mod:
            x, y, w, h = image.textureRect
            dx, dy, dw, dh = image.drawRect

            glmod.drawTexture(image.textureId, dx, dy, dw, dh, x, y, w, h)
        else:
            self.drawTexture(image.textureId, image.textureRect, image.drawRect)

    def drawTexture(self, texture, textureRect, drawRect):
        '''
        texture is an int
        textureRect is a list of size 4, determines which square to take from the texture
        drawRect is a list of size 4, is used to determine the drawing size
        '''

        glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture)

        x, y, w, h = textureRect
        dx, dy, dw, dh = drawRect

        x += self.camera[0]
        y += self.camera[1]

        glBegin(GL_QUADS);
        #Top-left vertex (corner)
        glTexCoord2i(x, y+h); #image/texture
        glVertex3f(dx, dy, 0); #screen coordinates

        #Bottom-left vertex (corner)
        glTexCoord2i(x+w, y+h);
        glVertex3f((dx+dw), dy, 0);

        #Bottom-right vertex (corner)
        glTexCoord2i(x+w, y);
        glVertex3f((dx+dw), (dy+dh), 0);

        #Top-right vertex (corner)
        glTexCoord2i(x, y);
        glVertex3f(dx, (dy+dh), 0);
        glEnd();

    def mouseMoveEvent(self, mouse):
        self.camera[0] += mouse.pos().x() - self.lastMousePos[0]
        self.camera[1] += mouse.pos().y() - self.lastMousePos[1]
        self.lastMousePos = [mouse.pos().x(), mouse.pos().y()]

        mouse.accept()

    def mousePressEvent(self, mouse):
        self.lastMousePos = (mouse.pos().x(), mouse.pos().y())

        mouse.accept()

    def wheelEvent(self, mouse):
        if mouse.delta() < 0:
            self.zoom -= 0.10
        elif mouse.delta() > 0:
            self.zoom += 0.10

        if self.zoom < 0.30:
            self.zoom = 0.30
        elif self.zoom > 4:
            self.zoom = 4

        mouse.accept()

