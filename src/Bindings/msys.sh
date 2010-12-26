
# Contents will change a lot if versions are changed

PYTHON="/c/Python26"
QT="/c/Qt/2009.03"

CFLAGS="-shared -O2 -Wall"
DEFINES="-DQT_NO_DEBUG -DNDEBUG -D_REENTRANT -DQT_CORE_LIB -DQT_GUI_LIB -DQT_SHARED"
INCLUDES="-I. -I${PYTHON} -I${QT}/qt/include -I${QT}/qt/include/qt -I${QT}/qt/include/QtCore -I${PYTHON}/include -I${PYTHON}/Lib/site-packages/PyQt4/include"
LIBDIRS="-L${PYTHON}/libs -L${QT}/qt/lib"

echo "removing previously created files"
rm -f moc_bMain.cpp sip* *.o

echo "creating new files"
$QT/qt/bin/moc bMain.h -o moc_bMain.cpp
$PYTHON/python.exe configure.py

for file in $(ls -1 *.cpp); do
  output=`echo $file | sed 's/.cpp/.o/'`
  echo "compiling $file into $output"
  g++ -c $CFLAGS $DEFINES $INCLUDES $file -o $output
done

echo "Generting pyd"
g++ $CFLAGS $LIBDIRS *.o ../../qt4/release/librandom-game-generator.a -lpython26 -lQtCore4 -lQtGui4 -lQtOpenGL4 -o _bmainmod.pyd
