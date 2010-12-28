from OpenGL.GL import *
from OpenGL.GL.ARB.vertex_buffer_object import *

from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *

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
        self.vbos = False
        self.x = 0
        self.images = []

    #GL functions
    def paintGL(self):
        '''
        Drawing routine
        '''
        
        glClear(GL_COLOR_BUFFER_BIT)

        if self.vbos:
            vbolist = []
            for img in self.images: #leave it here, removing it increases CPU consumption against expectations
                vbolist.append(img.textureId)
                vbolist.append(img.VBOTexCoords)
                vbolist.append(img.VBOVertices)
            glmod.drawVBO(tuple(vbolist))
        else:
            for img in self.images:
                self.drawImage(img)

    def resizeGL(self, w, h):
        '''
        Resize the GL window 
        '''
        
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, w, h, 0, -1, 1);
    
    def initializeGL(self):
        '''
        Initialize GL
        '''

        glEnable(GL_TEXTURE_RECTANGLE_ARB)
        glEnable(GL_BLEND)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glViewport(0, 0, self.width(), self.height())
        glClearColor(0.0, 0.0, 0.0, 0.0)

        if mod and glInitVertexBufferObjectARB():
            self.vbos = True
            print "using VBOs"

        qimg = QImage("test.png")
        for x in range(20):
            for y in range(20):
                img = Image(qimg, (0, 0, 63, 63), (x*63, y*63, 63, 63), self.vbos)
                self.images.append(img)
                self.createTexture(img)

    #util functions
    def createTexture(self, image):
        '''
        image is from image.py
        texture is an int, pointing to the correct location in VRAM
        '''

        img = self.convertToGLFormat(image.image)
        texture = glGenTextures(1)
        imgdata = img.bits().asstring(img.numBytes())

        glBindTexture(GL_TEXTURE_RECTANGLE_ARB, texture)

        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGBA, img.width(), img.height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, imgdata);

        image.textureId = texture

        if self.vbos:
            image.buildVBO()

    def deleteImage(self, image):
        '''
        textures can be a list, but doesn't have to be.
        '''

        glDeleteTextures(image.textureId)

        if self.vbos:
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


# You don't need anything below this

        

