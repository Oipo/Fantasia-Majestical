from PyQt4.QtCore import *
from PyQt4.QtGui import *

import fmGlobals
from fmGov import *

class governProvinceDialog(QDialog):

    def __init__(self, province):
        QDialog.__init__(self)

        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.tax = QLineEdit(str(province.taxRate()))
<<<<<<< HEAD
        self.tax.setValidator(QDoubleValidator(0, 100, 1, self))
=======
        self.tax.setValidator(QIntValidator(0, 100, self))
>>>>>>> b2790967b644d62c28a46930d0a05cbd4f4a9774

        x = 0

        grid = QGridLayout()

        grid.addWidget(QLabel("Tax Rate:"), x, 0)
        grid.addWidget(self.tax, x, 1)
        x += 1

        grid.addWidget(self.okButton, x, 0)
        grid.addWidget(self.cancelButton, x, 1)
        x += 1

        self.setLayout(grid)

        #debug
        from fmProv import Province

        if not isinstance(province, Province):
            f_code = sys._getframe(0).f_code #really bad hack to get the filename and number
            print "Doing it wrong in" + f_code.co_filename + ":" + str(f_code.co_firstlineno)

    def okPressed(self, checked):
        self.done(1)

    def cancelPressed(self, checked):
        self.done(0)

class governGovernerDialog(QDialog):

    def __init__(self, province):
        QDialog.__init__(self)

        self.okButton = QPushButton("Ok")
        self.cancelButton = QPushButton("Cancel")

        self.okButton.clicked.connect(self.okPressed)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.tax = QLineEdit(str(province.taxRate()))
        self.tax.setValidator(QDoubleValidator(0, 100, 1, self))

        descriptions = province.getUnrestDescList()
        self.unrest = QComboBox()

        for desc in descriptions:
            self.unrest.addItem(desc)

        x = 0

        grid = QGridLayout()

        grid.addWidget(QLabel("Tax Rate:"), x, 0)
        grid.addWidget(self.tax, x, 1)
        x += 1

        grid.addWidget(QLabel("Unrest:"), x, 0)
        grid.addWidget(self.unrest, x, 1)
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

    def __init__(self, province, panel):
        QListWidgetItem.__init__(self)
        self.province = province

        if province == panel.player.governedProvince():
            self.setText(province.name() + " (Governed)")
        else:
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
            #p.government().getLeader() == fmGlobals.worldmap.getHumanPlayer()
            self.provinceList.addItem(provinceItem(p, self))

        self.provinceList.setCurrentRow(0)

        self.setWidget(self.contents)
        mainWindow.addDockWidget(Qt.RightDockWidgetArea, self)

    def governPressed(self, checked):
        playerP = fmGlobals.worldmap.getCharacterProvince(self.player.sovereign())
        selectedP = None

        for item in self.provinceList.selectedItems():
            selectedP = item.province

        if selectedP == playerP:
            d = governProvinceDialog(selectedP)
            if d.exec_():
                selectedP.setTaxRate(int(d.tax.text()))
                self.provinceList.updateStats()
        else:
            d = governGovernerDialog(selectedP)
            if d.exec_():
                order = Order(str(d.tax.text()), str(d.unrest.currentText()))
                origin = fmGlobals.worldmap.getCharacterProvince(fmGlobals.worldmap.getHumanPlayer().sovereign()).government()
                target = selectedP.government()
                request = OrderRequest(origin, target, order)
                fmGlobals.worldmap.addOrderRequestToQueue(request)

