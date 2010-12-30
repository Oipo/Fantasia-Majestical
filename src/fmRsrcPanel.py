from PyQt4.QtCore import *
from PyQt4.QtGui import *

import fmGlobals

class governDialog(QDialog):

    def __init__(self, province):
        QDialog.__init__(self)

        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.tax = QLineEdit(str(province.taxRate()))
        self.tax.setValidator(QIntValidator())

        x = 0

        grid = QGridLayout()

        grid.addWidget(QLabel("Tax Rate:"), x, 0)
        grid.addWidget(self.tax, x, 1)
        x += 1

        grid.addWidget(self.okButton, x, 0)
        grid.addWidget(self.cancelButton, x, 1)
        x += 1

        self.setLayout(grid)

    def okPressed(self, checked):
        self.done(1)

    def cancelPressed(self, checked):
        self.done(0)

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

        fmGlobals.worldmap.updateSlot.connect(self.updateStats)

    def selectionChanged(self, selected, deselected):
        super(QListWidget, self).selectionChanged(selected, deselected)

        for index in selected.indexes():
            item = self.item(index.row())

            self.setStats(item)

    def updateStats(self):
        for item in self.selectedItems():
            self.setStats(item)

    def setStats(self, item):
        p = item.province
        panel = self.panel

        if p.name() == panel.player.governedProvince():
            panel.govern.setEnabled(True)
        else:
            panel.govern.setEnabled(False)

        panel.population.setText(str(p.population()) + "(" + str(p.fightingPopulation()) + ")")
        panel.levy.setText(str(p.normalLevy()) + "(" + str(p.maxLevy()) + ")")
        panel.tax.setText(str(p.taxRate()) + "%")
        panel.monthly.setText(str(p.getTax()) + "(" + str(p.goodsValue()) + ")")
        panel.unrest.setText(str(p.getUnrestDescriptor()))

class RsrcPanel(QDockWidget):
    '''Resource panel. Shows the various resources of the provinces, should later be converted to only showing the players' resources'''

    def __init__(self, mainWindow):
        super(QDockWidget, self).__init__(mainWindow)

        self.player = fmGlobals.worldmap.getHumanPlayer()

        self.contents = QWidget(self)
        self.provinceList = provinceListWidget(self)
        self.population = QLabel("0")
        self.levy = QLabel("0")
        self.tax = QLabel("0")
        self.monthly = QLabel("0")
        self.unrest = QLabel("0")

        self.govern = QPushButton("Govern")
        self.govern.setEnabled(False)

        self.govern.clicked.connect(self.governPressed)

        x = 0

        grid = QGridLayout()

        grid.addWidget(self.provinceList, x, 0, 1, 2)
        x += 1

        grid.addWidget(self.govern, x, 0)
        x += 1

        grid.addWidget(QLabel("Population(fighting):"), x, 0)
        grid.addWidget(self.population, x, 1)
        x += 1

        grid.addWidget(QLabel("Levy(maximum):"), x, 0)
        grid.addWidget(self.levy, x, 1)
        x += 1

        grid.addWidget(QLabel("Tax Rate:"), x, 0)
        grid.addWidget(self.tax, x, 1)
        x += 1

        grid.addWidget(QLabel("Monthly Tax(Monthly Goods Income):"), x, 0)
        grid.addWidget(self.monthly, x, 1)
        x += 1

        grid.addWidget(QLabel("Unrest:"), x, 0)
        grid.addWidget(self.unrest, x, 1)
        x += 1

        self.contents.setLayout(grid)

        provinces = fmGlobals.worldmap.provinces()

        for p in provinces.values():
            self.provinceList.addItem(provinceItem(p))

        self.provinceList.setCurrentRow(0)

        self.setWidget(self.contents)
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

    def governPressed(self, checked):
        p = fmGlobals.worldmap.province(self.player.governedProvince())
        d = governDialog(p)
        if d.exec_():
            p.setTaxRate(int(d.tax.text()))
            self.provinceList.updateStats()
