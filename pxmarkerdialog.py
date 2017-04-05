from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from ui_pxmarkerdialog import Ui_PxMarkerDialog

class PxMarkerDialog(QDialog):
    def __init__(self, parent=None, pxmarker_table=None):
        super(PxMarkerDialog, self).__init__(parent)

        self.ui = Ui_PxMarkerDialog()
        self.ui.setupUi(self)

        self.pxmarker_table_out = pxmarker_table
        self.pxmarker_table_height = len(self.pxmarker_table_out)
        self.load_pxmarker_table()

    def load_pxmarker_table(self):
        self.ui.pxmarker_table_widget.clearContents()
        self.ui.pxmarker_table_widget.setRowCount(self.pxmarker_table_height)

        row_position = 0
        for classnum, color, feature in self.pxmarker_table_out:
            class_item = QTableWidgetItem(str(classnum))
            class_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            class_item.setTextAlignment(Qt.AlignCenter)
            self.ui.pxmarker_table_widget.setItem(row_position, 0, class_item)

            color_item = QTableWidgetItem()
            color_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            color_item.setBackground(QColor(color[0],color[1],color[2]))
            self.ui.pxmarker_table_widget.setItem(row_position, 1, color_item)

            feature_item = QTableWidgetItem(feature)
            if row_position == 0:
                feature_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.ui.pxmarker_table_widget.setItem(row_position, 2, feature_item)

            row_position += 1
