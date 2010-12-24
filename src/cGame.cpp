/*
Random Game Generator - The generation of time transcending tabletop games!
Copyright (C) 2009 Michael de Lang

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/


/*
<Doctus> Random, Procedural, Chaotic, Non-deterministic, Automated
<Doctus> Game, Amusement, Pastime
<Doctus> Generator, Producer, Creator, Factory
*/

#include "cGame.h"

unsigned int FPScounter = 0;

cGame::cGame(QWidget *parent) : QObject(parent)
{
    mShapeManager = new cShapeManager();

    mGLWidget = new wGLWidget(parent, this);
    ((QMainWindow*)parent)->setCentralWidget(mGLWidget);

    mTilesetManager = new cTilesetManager(mGLWidget);

    title = "Fantasia Majestical";
    ((QMainWindow*)parent)->setWindowTitle(title);

    QTimer *timer = new QTimer(this);
    QTimer *timer2 = new QTimer(this);
    connect(timer , SIGNAL(timeout()), this, SLOT(draw()));
    connect(timer2, SIGNAL(timeout()), this, SLOT(displayFPS()));
    timer ->start(16);
    timer2->start(1000);
}

cGame::~cGame()
{
    delete mTilesetManager;
    delete mShapeManager;
    delete mGLWidget;
}

void cGame::draw()
{
    mGLWidget->updateGL();

    FPScounter++;
}

void cGame::displayFPS()
{
    QString str = title + QString(" | FPS: ") + QString::number(FPScounter);
    ((QMainWindow*)parent())->setWindowTitle(str);
    FPScounter = 0;
}


QString cGame::getTitle()
{
    return title;
}

