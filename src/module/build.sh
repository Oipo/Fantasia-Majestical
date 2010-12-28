gcc -shared -fPIC -I /usr/include/python2.6/ -I /usr/include/GL/ module/glmod.c -lpython2.6 -lGL -o glmod.so
