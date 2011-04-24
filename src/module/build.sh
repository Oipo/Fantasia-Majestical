g++ -O2 -fomit-frame-pointer -shared -fPIC -L /usr/lib/i386-linux-gnu -I /usr/include/python2.7/ `pkg-config --cflags --libs-only-L x11` glmod.c -lpython2.7 -lGL -o glmod.so
