from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from ui_mainwindow import Ui_MainWindow

from os import listdir, makedirs
from os.path import isfile, join, basename, exists
from glob import glob

import cv2

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        # UI set-up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Class variables
        self.file_formats = ('.jpg','.png','.bmp','.gif')

        self.img_directory = None
        self.img_current_idx = None
        self.img_current_filename = None
        self.img_current_frame = None

        self.table_db = None
        self.table_height = None

        # Signals & Slots
        self.ui.btn_load_sequence.clicked.connect(self.load_img_dir)
        self.ui.table_filename.itemSelectionChanged.connect(self.on_table_selection_change)

    def load_img_dir(self):
        """Callback for load directory button

        """
        self.img_directory = QFileDialog.getExistingDirectory(self, 'Select Image Directory', options = QFileDialog.ShowDirsOnly)

        if not self.img_directory == '':
            self.load_img_table(self.img_directory)
            self.ui.table_filename.selectRow(0)

    def load_img_table(self, img_file_dir):
        self.ui.label_dir_name.setText(img_file_dir)

        img_files = [f for f in listdir(img_file_dir) if f.endswith(self.file_formats)]

        if not exists(img_file_dir + '/labels'):
            makedirs(img_file_dir + '/labels')

        labels = []
        label_files = [f for f in listdir(img_file_dir + '/labels') if isfile(join(img_file_dir,f))]

        for i, mfile in enumerate(label_files):
            label_files[i] = basename(mfile)

        for fname in img_files:
            if basename(fname) in label_files:
                labels.append(True)
            else:
                labels.append(False)

        self.table_db = [list(tup) for tup in list(zip(img_files,labels))]

        self.table_height = len(self.table_db)
        self.ui.table_filename.clearContents()
        self.ui.table_filename.setRowCount(self.table_height)

        row_position = 0
        for fname, label_status in self.table_db:
            self.ui.table_filename.setItem(row_position, 0, QTableWidgetItem(fname))
            self.ui.table_filename.setItem(row_position, 1, QTableWidgetItem(str(label_status)))
            row_position += 1

    def on_table_selection_change(self):
        self.img_current_idx = self.ui.table_filename.currentRow()
        self.img_current_filename = self.ui.table_filename.item(self.img_current_idx, 0).text()
        self.load_img_frame(self.img_directory + "/" + self.img_current_filename)
        self.ui.label_frame_num.setText(str(self.img_current_idx+1)+"/"+str(self.table_height))

        print("Frame Number: " + str(self.img_current_idx + 1))
        print("Filename: " + self.img_current_filename)

    def load_img_frame(self, img_filename):
        """Load image frame from image file

        """
        self.img_current_frame = cv2.imread(img_filename)
        self.ui.main_display.setPixmap(QPixmap.fromImage(self.cv2qimage(self.img_current_frame)))

    def cv2qimage(self,cv2_img):
        """Transform cv2 np array image to QImage.

        """
        temp_img = cv2_img.copy()

        height, width = temp_img.shape[:2]
        byte_value = 3 * width

        if len(temp_img.shape) == 3:
            cv2.cvtColor(temp_img, cv2.COLOR_BGR2RGB, temp_img)
            qImage_out = QImage(temp_img.data, width, height, byte_value, QImage.Format_RGB888)
        else:
            qImage_out = QImage(temp_img.repeat(3).tostring(), width, height, byte_value, QImage.Format_RGB888)

        return qImage_out

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    LabelerMainWindow = MainWindow()
    LabelerMainWindow.show()
    sys.exit(app.exec_())
