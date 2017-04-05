from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from ui_mainwindow import Ui_MainWindow
from pxmarkerdialog import PxMarkerDialog

from os import listdir, makedirs
from os.path import isfile, join, basename, exists, splitext
from glob import glob

import pickle

import numpy as np
import cv2

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        # UI set-up
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Class variables
        self.file_formats = ('.jpg','.png','.bmp','.gif')

        self.img_size = (480,640)
        self.img_directory = None
        self.img_table_idx = None
        self.img_filename = None
        self.img_frame = None

        self.pxlabel_filename = None
        self.pxlabel_mat = None
        self.pxlabel_frame = None

        self.table_db = None
        self.table_height = None

        self.pxmarker_table = self.load_pxmarker_table()
        self.update_pxmarker_cbox(self.pxmarker_table)
        self.ui.cbox_pxmarker_select.setCurrentIndex(0)
        self.pxmarker_current = self.pxmarker_table[0]
        self.pxmarker_stylesheet = self.get_pxmarker_stylesheet(self.pxmarker_current[1])
        self.ui.label_pxmarker_color.setStyleSheet(self.pxmarker_stylesheet)

        # Signals & Slots
        self.ui.btn_load_sequence.clicked.connect(self.on_load_img_dir)
        self.ui.btn_frame_next.clicked.connect(self.on_next_frame_click)
        self.ui.btn_frame_prev.clicked.connect(self.on_prev_frame_click)
        self.ui.btn_edit_pxmarker.clicked.connect(self.on_pxmarker_edit_click)
        self.ui.table_filename.itemSelectionChanged.connect(self.on_table_selection_change)
        self.ui.cbox_pxmarker_select.currentIndexChanged.connect(self.on_pxmarker_cbox_change)



    def on_load_img_dir(self):
        """Callback for load directory button

        """
        self.img_directory = QFileDialog.getExistingDirectory(self, "Select Image Directory", options = QFileDialog.ShowDirsOnly)

        if not self.img_directory == '':
            self.load_img_table(self.img_directory)
            self.ui.table_filename.selectRow(0)

    def on_table_selection_change(self):
        """Callback for table selection change.

        Updates image index, filename, frame, and frame label.

        """
        self.img_table_idx = self.ui.table_filename.currentRow()
        self.img_filename = self.ui.table_filename.item(self.img_table_idx, 0).text()

        self.pxlabel_filename = self.img_directory + '/labels/' + splitext(self.img_filename)[0] + '.pkl'
        self.load_pxlabel_mat(self.pxlabel_filename)

        self.load_img_frame(self.img_directory + '/' + self.img_filename)
        self.ui.label_frame_num.setText(str(self.img_table_idx+1) + '/' +str(self.table_height))

    def on_next_frame_click(self):
        if self.img_table_idx < self.table_height - 1:
            current_row = self.img_table_idx + 1
        else:
            current_row = 0

        self.ui.table_filename.selectRow(current_row)

    def on_prev_frame_click(self):
        if self.img_table_idx > 0:
            current_row = self.img_table_idx - 1
        else:
            current_row = self.table_height - 1

        self.ui.table_filename.selectRow(current_row)

    def on_pxmarker_cbox_change(self, index):
        self.pxmarker_current = self.pxmarker_table[index]
        self.pxmarker_stylesheet = self.get_pxmarker_stylesheet(self.pxmarker_current[1])
        self.ui.label_pxmarker_color.setStyleSheet(self.pxmarker_stylesheet)

    def on_pxmarker_edit_click(self):
        pxmarker_dialog = PxMarkerDialog(self,self.pxmarker_table)

        if pxmarker_dialog.exec():
            print(self.pxmarker_table)
            print(pxmarker_dialog.pxmarker_table_out)
        else:
            pass

        pxmarker_dialog = None


    def load_pxmarker_table(self):
        try:
            with open('px_marker.pkl', 'rb') as f:
                pxmarker_table = pickle.load(f)
                return pxmarker_table
        except EnvironmentError as e:
            pxmarker_table = [
                                [0, (0,0,0), 'Eraser'],
                                [1, (255,0,0), 'Feature 1'],
                                [2, (0,255,0), 'Feature 2'],
                                [3, (0,0,255), 'Feature 3'],
                                [4, (255,255,0), 'Feature 4'],
                                [5, (0,255,255), 'Feature 5'],
                                [6, (255,0,255), 'Feature 6'],
                                [7, (128,128,0), 'Feature 7'],
                                [8, (0,128,128), 'Feature 8'],
                                [9, (128,0,128), 'Feature 9'],
                                [10, (255,153,153), 'Feature 10']
            ]

            with open('px_marker.pkl', 'wb') as f:
                pickle.dump(pxmarker_table, f)
                return pxmarker_table

    def get_pxmarker_stylesheet(self, color):
        return "background-color: rgb" + str(color) + ";"

    def update_pxmarker_cbox(self, pxmarker_table):
        cbox_list = []
        for item in pxmarker_table:
            cbox_list.append(item[2])

        self.ui.cbox_pxmarker_select.clear()
        self.ui.cbox_pxmarker_select.addItems(cbox_list)

    def load_img_table(self, img_file_dir):
        """Create table of image files and pxlabel files

        """

        self.ui.label_dir_name.setText(img_file_dir)

        img_files = [f for f in listdir(img_file_dir) if f.endswith(self.file_formats)]

        if not exists(img_file_dir + '/labels'):
            makedirs(img_file_dir + '/labels')

        pxlabels = []
        pxlabel_dir = img_file_dir + '/labels'
        pxlabel_files = [f for f in listdir(pxlabel_dir) if f.endswith('.pkl')]

        for i, mfile in enumerate(pxlabel_files):
            pxlabel_files[i] = splitext(mfile)[0]

        for fname in img_files:
            if splitext(fname)[0] in pxlabel_files:
                pxlabels.append(True)
            else:
                pxlabels.append(False)

        self.table_db = [list(tup) for tup in list(zip(img_files,pxlabels))]

        self.table_height = len(self.table_db)
        self.ui.table_filename.clearContents()
        self.ui.table_filename.setRowCount(self.table_height)

        row_position = 0
        for fname, pxlabel_status in self.table_db:
            self.ui.table_filename.setItem(row_position, 0, QTableWidgetItem(fname))
            self.ui.table_filename.setItem(row_position, 1, QTableWidgetItem(str(pxlabel_status)))
            row_position += 1

    def load_pxlabel_mat(self, pxlabel_filename):
        """Load pxlabel matrix if available, create one if not

        """
        try:
            with open(pxlabel_filename, 'rb') as f:
                self.pxlabel_mat = pickle.load(f)
        except EnvironmentError as e:
            self.pxlabel_mat = np.zeros(self.img_size)

    def save_pxlabel_mat(self):
        """Write pxlabel pickle file and update table_height

        """
        with open(pxlabel_filename, 'wb') as f:
            pickle.dump(self.pxlabel_mat, f)
            print("Pxlabel pickled")

    def load_img_frame(self, img_filename):
        """Load image frame from image file

        """
        self.img_frame = cv2.imread(img_filename)
        self.ui.main_display.setPixmap(QPixmap.fromImage(self.cv2qimage(self.img_frame)))

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
