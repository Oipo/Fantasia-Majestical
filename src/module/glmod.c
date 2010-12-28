#include <Python.h>
#include <gl.h>

GLenum extension = GL_TEXTURE_RECTANGLE_ARB;

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
    PyObject *tuple = PyTuple_GetItem(args, 0);

    if(PyTuple_Size(tuple) % 3 != 0)
    {
        printf("Failure with size: %i\n", PyTuple_Size(tuple));
        return PyInt_FromLong(-1L);
    }

    int texid[PyTuple_Size(tuple)/3], VBOTex[PyTuple_Size(tuple)/3], VBOVer[PyTuple_Size(tuple)/3], i, x;

    glEnableClientState(GL_VERTEX_ARRAY);
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);

    for(i = 0; i < PyTuple_Size(tuple); i++)
    {
        x = PyInt_AsLong(PyTuple_GetItem(tuple, i));
        if(i % 3 == 0)
            texid[i/3] = x;
        else if(i % 3 == 1)
            VBOTex[i/3] = x;
        else if(i % 3 == 2)
            VBOVer[i/3] = x;
    }

    for(i = 0; i < PyTuple_Size(tuple)/3; i++)
    {
        glBindTexture(extension, texid[i]);

        glBindBuffer(GL_ARRAY_BUFFER_ARB, VBOTex[i]);
        glTexCoordPointer(2, GL_FLOAT, 0, 0);

        glBindBuffer(GL_ARRAY_BUFFER_ARB, VBOVer[i]);
        glVertexPointer(3, GL_FLOAT, 0, 0);

        glDrawArrays(GL_QUADS, 0, 4);
    }

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER_ARB, 0);

    return PyInt_FromLong(0L);
}

static PyObject * glmod_drawVBO2(PyObject *self, PyObject* args)
{
    PyObject *tuple = PyTuple_GetItem(args, 0);

    if(PyTuple_Size(tuple) < 3)
    {
        printf("Failure with size: %i\n", PyTuple_Size(tuple));
        return PyInt_FromLong(-1L);
    }

    int texid[PyTuple_Size(tuple)-2], VBOTex, VBOVer, i, x;

    VBOTex = PyInt_AsLong(PyTuple_GetItem(tuple, 0));
    VBOVer = PyInt_AsLong(PyTuple_GetItem(tuple, 1));

    glEnableClientState(GL_VERTEX_ARRAY);
    glEnableClientState(GL_TEXTURE_COORD_ARRAY);

    for(i = 2; i < PyTuple_Size(tuple); i++)
    {
        x = PyInt_AsLong(PyTuple_GetItem(tuple, i));
        texid[i-2] = x;
    }

    glBindBuffer(GL_ARRAY_BUFFER_ARB, VBOTex);
    glTexCoordPointer(2, GL_FLOAT, 0, 0);

    glBindBuffer(GL_ARRAY_BUFFER_ARB, VBOVer);
    glVertexPointer(3, GL_FLOAT, 0, 0);

    for(i = 0; i < PyTuple_Size(tuple)-2; i++)
    {
        glBindTexture(extension, texid[i]);

        glDrawArrays(GL_QUADS, i*4, 4);
    }

    glDisableClientState(GL_VERTEX_ARRAY);
    glDisableClientState(GL_TEXTURE_COORD_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER_ARB, 0);

    return PyInt_FromLong(0L);
}

static PyObject * glmod_glBufferData(PyObject *self, PyObject* args)
{
    int target, size, data, type, ok;

    ok = PyArg_ParseTuple(args, "iiii", &target, &size, &data, &type);

    if(!ok)
       return PyInt_FromLong(-1L); 

    glBufferData(target, size, data, type);

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
    int x, y, w, h, ok;

    ok = PyArg_ParseTuple(args, "iiii", &x, &y, &w, &h);

    glEnable(extension);
    glEnable(GL_BLEND);
    glDisable(GL_DEPTH_TEST);
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glViewport(0, 0, w, h);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0.0, x, y, 0.0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
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
    {"drawVBO",  glmod_drawVBO, METH_VARARGS, "draw var args VBO"},
    {"drawVBO2",  glmod_drawVBO2, METH_VARARGS, "draw var args VBO"},
    {"glBufferData",  glmod_glBufferData, METH_VARARGS, "glBufferData"},
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


