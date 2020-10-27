from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGroupBox, QHBoxLayout

from core.grid import Grid
from gui.Overlay import GridOverlay
import core.env as env


class FighterView(QWidget):
    def __init__(self):
        super(FighterView, self).__init__()

        self.initButton()
        self.initLayout()

    def initButton(self):
        # next map button
        self.highlight_grid_button = QPushButton("highlight grid")
        self.highlight_grid_button.clicked.connect(self.highlightGrid)

    def initLayout(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.button_combat_box = QGroupBox()
        self.button_combat_layout = QHBoxLayout()
        self.button_combat_box.setLayout(self.button_combat_layout)

        self.button_combat_layout.addWidget(self.highlight_grid_button)

        self.layout.addWidget(self.button_combat_box)
        self.layout.insertLayout(0, self.button_combat_layout)

    def highlightGrid(self, event):
        self.hide()
        self.combat_grid = Grid(env.Region.COMBAT_R, env.VCELLS, env.HCELLS)
        self.combat_grid.parse()
        self.combat_grid.highlight(3)
        self.show()