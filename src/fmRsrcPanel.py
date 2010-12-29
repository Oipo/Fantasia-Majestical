from PyQt4.QtCore import *
from PyQt4.QtGui import *

import fmGlobals

class provinceItem(QListWidgetItem):

    def __init__(self, province):
        QListWidgetItem.__init__(self)
        self.province = province
        self.setText(province.name())

class provinceListWidget(QListWidget):

    def __init__(self, panel):
        QListWidget.__init__(self)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.panel = panel

        fmGlobals.worldmap.updateSlot.connect(self.update)

    def selectionChanged(self, selected, deselected):
        super(QListWidget, self).selectionChanged(selected, deselected)

        for index in selected.indexes():
            item = self.item(index.row())

            self.setStats(item)

    def update(self):
        for item in self.selectedItems():
            self.setStats(item)

    def setStats(self, item):
        p = item.province
        panel = self.panel

        panel.population.setText(str(p.population()) + "(" + str(p.fightingPopulation()) + ")")
        panel.levy.setText(str(p.normalLevy()) + "(" + str(p.maxLevy()) + ")")
        panel.tax.setText(str(p.taxRate()) + "%")
        panel.monthly.setText(str(p.getTax()) + "(" + str(p.goodsValue()) + ")")
        panel.unrest.setText(str(p.getUnrestDescriptor()))

class RsrcPanel(QDockWidget):
    '''Resource panel. Shows the various resources of the provinces, should later be converted to only showing the players' resources'''

    def __init__(self, mainWindow):
        super(QDockWidget, self).__init__(mainWindow)

        self.contents = QWidget(self)
        self.provinceList = provinceListWidget(self)
        self.population = QLabel("0")
        self.levy = QLabel("0")
        self.tax = QLabel("0")
        self.monthly = QLabel("0")
        self.unrest = QLabel("0")

        grid = QGridLayout()

        grid.addWidget(self.provinceList, 0, 0, 1, 2)

        grid.addWidget(QLabel("Population(fighting):"), 1, 0)
        grid.addWidget(self.population, 1, 1)

        grid.addWidget(QLabel("Levy(maximum):"), 2, 0)
        grid.addWidget(self.levy, 2, 1)

        grid.addWidget(QLabel("Tax Rate:"), 3, 0)
        grid.addWidget(self.tax, 3, 1)

        grid.addWidget(QLabel("Monthly Tax(Monthly Goods Income):"), 4, 0)
        grid.addWidget(self.monthly, 4, 1)

        grid.addWidget(QLabel("Unrest:"), 5, 0)
        grid.addWidget(self.unrest, 5, 1)

        self.contents.setLayout(grid)

        provinces = fmGlobals.worldmap.provinces()

        for p in provinces.values():
            self.provinceList.addItem(provinceItem(p))

        self.provinceList.setCurrentRow(0)

        self.setWidget(self.contents)
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)
