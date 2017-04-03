from PyQt5.QtWidgets import QWidget, QApplication
from ui_mainwindow import Ui_MainWindow

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    LabelerMainWindow = MainWindow()
    LabelerMainWindow.show()
    sys.exit(app.exec_())
