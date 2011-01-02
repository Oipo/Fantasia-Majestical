#include <Python.h>
#include <GL/gl.h>

#ifdef _WIN32
#include <windows.h>
#include "glext.h"
PFNGLBINDBUFFERPROC glBindBuffer = NULL;
#endif

#define BUFFER_OFFSET(i) ((char *)NULL + (i))

GLenum extension = GL_TEXTURE_RECTANGLE_ARB;

int *texid, *offsets, VBO, stride, arrSize;

static PyObject * glmod_drawTexture(PyObject *self, PyObject* args)
{
    int texid, x, y, w, h, cx, cy, cw, ch, ok;

    ok = PyArg_ParseTuple(args, "iiiiiiiii", &texid, &x, &y, &w, &h, &cx, &cy, &cw, &ch);

    if(!ok)
       return PyInt_FromLong(-1L); 

    glBindTexture(extension, texid);

    glBegin(GL_QUADS);
    //Top-left vertex (corner)
    glTexCoord2i(cx, cy+ch); //image/texture
    glVertex3i(x, y, 0); //_screen coordinates

    //Bottom-left vertex (corner)
    glTexCoord2i(cx+cw, cy+ch);
    glVertex3i(x+w, y, 0);

    //Bottom-right vertex (corner)
    glTexCoord2i(cx+cw, cy);
    glVertex3i(x+w, y+h, 0);

    //Top-right vertex (corner)
    glTexCoord2i(cx, cy);
    glVertex3i(x, y+h, 0);
    glEnd();

    return PyInt_FromLong(0L);
}

static PyObject * glmod_drawVBO(PyObject *self, PyObject* args)
{
    int i;

    glBindBuffer(GL_ARRAY_BUFFER_ARB, VBO);
    glTexCoordPointer(2, GL_FLOAT, stride, 0);
    glVertexPointer(2, GL_FLOAT, stride, BUFFER_OFFSET(stride/2));

    glEnableClientState(GL_VERTEX_ARRAY);
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);

    for(i = 0; i < arrSize; i++)
    {
        glBindTexture(extension, texid[i]);

        glDrawArrays(GL_QUADS, offsets[i], 4);
    }

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER_ARB, 0);

    return PyInt_FromLong(0L);
}

static PyObject * glmod_setVBO(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GetItem(args, 0);
    int i, x;

    if(PyTuple_Size(tuple) % 2 != 0)
    {
        printf("Failure with size: %i\n", PyTuple_Size(tuple));
        return PyInt_FromLong(-1L);
    }

    free(texid);
    free(offsets);

    arrSize = (PyTuple_Size(tuple)-2)/2;
    texid = (int*)malloc(arrSize*sizeof(int));
    offsets = (int*)malloc(arrSize*sizeof(int));

    VBO = PyInt_AsLong(PyTuple_GetItem(tuple, 0));
    stride = PyInt_AsLong(PyTuple_GetItem(tuple, 1));

    for(i = 2; i < PyTuple_Size(tuple); i++)
    {
        x = PyInt_AsLong(PyTuple_GetItem(tuple, i));
        if(i % 2 == 0)
            texid[(i-2)/2] = x;
        else
            offsets[(i-2)/2] = x;
    }

    return PyInt_FromLong(0L);
}

static PyObject * glmod_generateTexture(PyObject *self, PyObject* args)
{
    int texid, w, h, ok;
    const char *pixels;

    ok = PyArg_ParseTuple(args, "iis", &w, &h, &pixels);

    texid = -1;
    glGenTextures(1, &texid);
    glBindTexture(extension, texid);

    glTexParameteri(extension, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(extension, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(extension, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(extension, GL_TEXTURE_MIN_FILTER, GL_LINEAR);

    //'''possibly GL_COMPRESSED_RGBA_ARB as third parameter'''
    glTexImage2D(extension, 0, GL_RGBA, w, h, 
                 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels);

    return PyInt_FromLong(texid);
}

static PyObject * glmod_init(PyObject *self, PyObject* args)
{
    texid = NULL;
    offsets = NULL;

#ifdef _WIN32
    glBindBuffer = (PFNGLBINDBUFFERARBPROC)wglGetProcAddress("glBindBuffer");
#endif

    return PyInt_FromLong(0L);
}

static PyObject * glmod_clear(PyObject *self, PyObject* args)
{
    glClear(GL_COLOR_BUFFER_BIT);
    return PyInt_FromLong(0L);
}

//blatantly stolen from Box2D
static PyObject * glmod_nextPowerOfTwo(PyObject *self, PyObject* args)
{
    int x, ok;

    ok = PyArg_ParseTuple(args, "i", &x);

    if(!ok)
        return PyInt_FromLong(-1L);

    x |= (x >> 1);
    x |= (x >> 2);
    x |= (x >> 4);
    x |= (x >> 8);
    x |= (x >> 16);
    x++;
    return PyInt_FromLong(x);
}

static PyMethodDef GLModMethods[] = {
    {"drawTexture",  glmod_drawTexture, METH_VARARGS, "draw a texture"},
    {"drawVBO",  glmod_drawVBO, METH_VARARGS, "draw the list of texids with VBO"},
    {"setVBO",  glmod_setVBO, METH_VARARGS, "set the list of texids"},
    {"nextPowerOfTwo",  glmod_nextPowerOfTwo, METH_VARARGS, "glBufferData"},
    {"generateTexture",  glmod_generateTexture, METH_VARARGS, "generate texture id"},
    {"clear",  glmod_clear, METH_VARARGS, "clear"},
    {"init",  glmod_init, METH_VARARGS, "init"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC initglmod(void)
{
    PyObject *m;
    PyImport_AddModule("glmod");
    m = Py_InitModule("glmod", GLModMethods);
    if (m == NULL)
        return;
}


