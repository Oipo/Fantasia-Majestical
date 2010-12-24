/****************************************************************************
** Meta object code from reading C++ file 'bMain.h'
**
** Created: Fri Dec 24 17:15:55 2010
**      by: The Qt Meta Object Compiler version 62 (Qt 4.7.1)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include "bMain.h"
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'bMain.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 62
#error "This file was generated using the moc from 4.7.1. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
static const uint qt_meta_data_bMain[] = {

 // content:
       5,       // revision
       0,       // classname
       0,    0, // classinfo
      10,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       5,       // signalCount

 // signals: signature, parameters, type, tag, flags
      11,    7,    6,    6, 0x05,
      45,   36,    6,    6, 0x05,
      75,   36,    6,    6, 0x05,
     107,    6,    6,    6, 0x05,
     126,    6,    6,    6, 0x05,

 // slots: signature, parameters, type, tag, flags
     145,    7,    6,    6, 0x08,
     171,   36,    6,    6, 0x08,
     202,   36,    6,    6, 0x08,
     235,    6,    6,    6, 0x08,
     255,    6,    6,    6, 0x08,

       0        // eod
};

static const char qt_meta_stringdata_bMain[] = {
    "bMain\0\0x,y\0mouseMoveSignal(int,int)\0"
    "x,y,type\0mousePressSignal(int,int,int)\0"
    "mouseReleaseSignal(int,int,int)\0"
    "leaveEventSignal()\0enterEventSignal()\0"
    "mouseMoveTrigger(int,int)\0"
    "mousePressTrigger(int,int,int)\0"
    "mouseReleaseTrigger(int,int,int)\0"
    "leaveEventTrigger()\0enterEventTrigger()\0"
};

const QMetaObject bMain::staticMetaObject = {
    { &QObject::staticMetaObject, qt_meta_stringdata_bMain,
      qt_meta_data_bMain, 0 }
};

#ifdef Q_NO_DATA_RELOCATION
const QMetaObject &bMain::getStaticMetaObject() { return staticMetaObject; }
#endif //Q_NO_DATA_RELOCATION

const QMetaObject *bMain::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->metaObject : &staticMetaObject;
}

void *bMain::qt_metacast(const char *_clname)
{
    if (!_clname) return 0;
    if (!strcmp(_clname, qt_meta_stringdata_bMain))
        return static_cast<void*>(const_cast< bMain*>(this));
    return QObject::qt_metacast(_clname);
}

int bMain::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        switch (_id) {
        case 0: mouseMoveSignal((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 1: mousePressSignal((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 2: mouseReleaseSignal((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 3: leaveEventSignal(); break;
        case 4: enterEventSignal(); break;
        case 5: mouseMoveTrigger((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 6: mousePressTrigger((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 7: mouseReleaseTrigger((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 8: leaveEventTrigger(); break;
        case 9: enterEventTrigger(); break;
        default: ;
        }
        _id -= 10;
    }
    return _id;
}

// SIGNAL 0
void bMain::mouseMoveSignal(int _t1, int _t2)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void bMain::mousePressSignal(int _t1, int _t2, int _t3)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)), const_cast<void*>(reinterpret_cast<const void*>(&_t3)) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void bMain::mouseReleaseSignal(int _t1, int _t2, int _t3)
{
    void *_a[] = { 0, const_cast<void*>(reinterpret_cast<const void*>(&_t1)), const_cast<void*>(reinterpret_cast<const void*>(&_t2)), const_cast<void*>(reinterpret_cast<const void*>(&_t3)) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void bMain::leaveEventSignal()
{
    QMetaObject::activate(this, &staticMetaObject, 3, 0);
}

// SIGNAL 4
void bMain::enterEventSignal()
{
    QMetaObject::activate(this, &staticMetaObject, 4, 0);
}
QT_END_MOC_NAMESPACE
