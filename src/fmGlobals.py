#general
vbos = False
glwidget = None
worldmap = None

#gui
rsrcpanel = None

#music
mediaobject = None

try:
    import PyQt4.phonon
    musicOn = True
except ImportError:
    musicOn = False
    