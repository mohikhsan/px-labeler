from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QTreeWidgetItem
from ui_mainwindow import Ui_MainWindow

from os import listdir, makedirs
from os.path import isfile, join, basename

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        # UI set-up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Class variables
        self.img_directory = None

        # Signals & Slots
        self.ui.btn_load_sequence.clicked.connect(self.load_img_dir)

    def load_img_dir(self):
        """Callback for load directory button

        """
        self.img_directory = QFileDialog.getExistingDirectory(self, "Select Image Directory", options = QFileDialog.ShowDirsOnly)

        col_headers = ['Filename', 'Labeled']
        img_files = [f for f in listdir(self.img_directory) if isfile(join(self.img_directory,f))]
        labels = []

        

        label_files = basename([f for f in listdir(self.img_directory + '/labels') if isfile(join(self.img_directory,f))])
        for fname in img_files:
            if basename(fname) in label_files:
                labels.append(True)
            else:
                labels.append(False)
        print(img_files)
        print(label_files)
        print(labels)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    LabelerMainWindow = MainWindow()
    LabelerMainWindow.show()
    sys.exit(app.exec_())
