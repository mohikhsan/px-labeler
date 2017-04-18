from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QColor
from PyQt5.QtCore import QEvent, Qt

from pxgui.ui_mainwindow import Ui_MainWindow
from pxmarkerdialog import PxMarkerDialog

from os import listdir, makedirs, remove, getcwd
from os.path import isfile, join, basename, exists, splitext, realpath, dirname
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
        self.file_abs_dir = realpath(join(getcwd(), dirname(__file__)))

        # Image variables
        self.img_size = None
        self.img_directory = None
        self.img_table_idx = None
        self.img_filename = None

        # cv2 images of us image, label, and display
        self.img_frame = None
        self.pxlabel_frame = None
        self.pxlabel_frame_ori = None
        self.pxlabel_frame_prev = None
        self.display_frame = None
        self.mouse_pos = None

        # Label variables
        self.pxlabel_filename = None
        self.pxlabel_display_filename = None
        self.pxlabel_mat = None

        # Cursor variables
        self.cursor_size = 5
        self.cursor_color = None

        # Image database array & variables
        self.table_db = None
        self.table_height = None
        self.table_loaded = False

        # Marker table & variables
        if not exists(self.file_abs_dir + '/settings'):
            makedirs(self.file_abs_dir + '/settings')

        self.pxmarker_table = self.load_pxmarker_table()
        self.update_pxmarker_cbox(self.pxmarker_table)
        self.ui.cbox_pxmarker_select.setCurrentIndex(0)
        self.pxmarker_current = self.pxmarker_table[0]
        self.pxmarker_stylesheet = self.get_pxmarker_stylesheet(self.pxmarker_current[1])
        self.ui.label_pxmarker_color.setStyleSheet(self.pxmarker_stylesheet)

        self.cursor_color = self.pxmarker_current[1]

        # Signals & Slots
        self.ui.btn_load_sequence.clicked.connect(self.on_load_img_dir)
        self.ui.btn_frame_next.clicked.connect(self.on_next_frame_click)
        self.ui.btn_frame_prev.clicked.connect(self.on_prev_frame_click)
        self.ui.btn_edit_pxmarker.clicked.connect(self.on_pxmarker_edit_click)
        self.ui.btn_copy_labels.clicked.connect(self.on_copy_click)
        self.ui.btn_clear_labels.clicked.connect(self.on_clear_click)

        self.ui.table_filename.itemSelectionChanged.connect(self.on_table_selection_change)
        self.ui.cbox_pxmarker_select.currentIndexChanged.connect(self.on_pxmarker_cbox_change)

        # Main frame event filter
        self.ui.main_display.setMouseTracking(True)
        self.ui.main_display.installEventFilter(self)
    #########################
    # Main Display functions
    #########################

    def eventFilter(self, source, event):
        """Callback to handle main display events

        """
        if event.type() == QEvent.MouseMove and self.table_loaded:
            self.mouse_pos = event.pos()
            if event.buttons() == Qt.NoButton:
                #Paint only cursor and size
                self.update_display(self.mouse_pos, True)
            else:
                cv2.circle(self.pxlabel_frame, (self.mouse_pos.x(), self.mouse_pos.y()), self.cursor_size, self.cursor_color[::-1], -1)
                self.update_display(self.mouse_pos, False)

        elif event.type() == QEvent.Leave and self.table_loaded:
            self.update_display()

        return QWidget.eventFilter(self, source, event)

    def update_display(self, mouse_pos=None, cursor_flag=False):
        """Updates main display when called

        """
        self.display_frame = self.img_frame.copy()
        self.display_frame = cv2.addWeighted(self.display_frame, 1, self.pxlabel_frame, 0.5, 0)
        if cursor_flag:
            cv2.circle(self.display_frame, (mouse_pos.x(), mouse_pos.y()), self.cursor_size, self.cursor_color[::-1], 3)
        self.ui.main_display.setPixmap(QPixmap.fromImage(self.cv2qimage(self.display_frame)))

    def pxlabel2frame(self, img_size, pxlabel_mat, pxmarker_table):
        """Creates pixel label display frame from pixel label matrix

        """
        pxlabel_frame_out = np.zeros(img_size, np.uint8)
        idx = 0
        for marker in pxmarker_table[1:]:
            pxlabel_frame_out[pxlabel_mat[idx] == 1] = marker[1]
            idx += 1

        return pxlabel_frame_out

    def load_img_frame(self, img_filename):
        """Load image frame from image file and set to main display pixmap

        """
        self.img_frame = cv2.imread(img_filename)
        self.img_size = self.img_frame.shape
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

    #########################
    # File table functions
    #########################

    def on_load_img_dir(self):
        """Callback for load directory button

        """
        self.img_directory = QFileDialog.getExistingDirectory(self, "Select Image Directory", options = QFileDialog.ShowDirsOnly)

        if not self.img_directory == '':
            self.load_img_table(self.img_directory)
            self.ui.table_filename.selectRow(0)

    def load_img_table(self, img_file_dir):
        """Create table of image files and pxlabel files

        """

        self.ui.label_dir_name.setText(img_file_dir)

        img_files = [f for f in listdir(img_file_dir) if f.endswith(self.file_formats)]

        if not exists(img_file_dir + '/labels'):
            makedirs(img_file_dir + '/labels')

        if not exists(img_file_dir + '/labels_display'):
            makedirs(img_file_dir + '/labels_display')

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
            if pxlabel_status:
                item_name = QTableWidgetItem(fname)
                item_name.setForeground(QColor(0,255,0))

                item_status = QTableWidgetItem(str(pxlabel_status))
                item_status.setForeground(QColor(0,255,0))
            else:
                item_name = QTableWidgetItem(fname)
                item_status = QTableWidgetItem(str(pxlabel_status))

            self.ui.table_filename.setItem(row_position, 0, item_name)
            self.ui.table_filename.setItem(row_position, 1, item_status)
            row_position += 1

        self.ui.label_status.setText("Directory loaded")

    def on_table_selection_change(self):
        """Callback for table selection change.

        Updates image index, filename, frame, and frame label.

        """
        if self.table_loaded:
            self.pxlabel_frame_prev = self.pxlabel_frame.copy()
            self.save_pxlabel_mat()

        self.img_table_idx = self.ui.table_filename.currentRow()
        self.img_filename = self.ui.table_filename.item(self.img_table_idx, 0).text()

        self.load_img_frame(self.img_directory + '/' + self.img_filename)
        self.ui.label_frame_num.setText(str(self.img_table_idx+1) + '/' +str(self.table_height))

        self.pxlabel_filename = self.img_directory + '/labels/' + splitext(self.img_filename)[0] + '.pkl'
        self.pxlabel_display_filename = self.img_directory + '/labels_display/' + splitext(self.img_filename)[0] + '.png'
        self.pxlabel_mat = self.load_pxlabel_mat(self.pxlabel_filename)
        self.pxlabel_frame = self.pxlabel2frame(self.img_size, self.pxlabel_mat, self.pxmarker_table)
        self.pxlabel_frame_ori = self.pxlabel_frame.copy()

        self.table_loaded = True

        self.update_display()


    def on_next_frame_click(self):
        """Callback for next button click

        """
        if self.table_loaded:
            if self.img_table_idx < self.table_height - 1:
                current_row = self.img_table_idx + 1
            else:
                current_row = 0
            self.ui.table_filename.selectRow(current_row)

    def on_prev_frame_click(self):
        """Callback for prev button click

        """

        if self.table_loaded:
            if self.img_table_idx > 0:
                current_row = self.img_table_idx - 1
            else:
                current_row = self.table_height - 1

            self.ui.table_filename.selectRow(current_row)

    def on_clear_click(self):
        """Callback for clear button click

        """
        if self.table_loaded:
            self.pxlabel_frame = np.zeros(self.img_size, np.uint8)
            self.update_display()

    def on_copy_click(self):
        """Callback for copy button click

        """
        if self.table_loaded and self.pxlabel_frame_prev is not None:
            self.pxlabel_frame = self.pxlabel_frame_prev.copy()
            self.update_display()
    #########################
    # Drawing marker functions
    #########################

    def on_pxmarker_cbox_change(self, index):
        """Callback for marker combobox change

        """

        self.pxmarker_current = self.pxmarker_table[index]
        self.pxmarker_stylesheet = self.get_pxmarker_stylesheet(self.pxmarker_current[1])
        self.ui.label_pxmarker_color.setStyleSheet(self.pxmarker_stylesheet)
        self.cursor_color = self.pxmarker_current[1]

        if self.mouse_pos:
            self.update_display(self.mouse_pos, True)

    def on_pxmarker_edit_click(self):
        """Callback for marker edit button click. Launches edit marker dialog.

        """
        pxmarker_dialog = PxMarkerDialog(self,self.pxmarker_table)

        if pxmarker_dialog.exec_():
            self.pxmarker_table = pxmarker_dialog.pxmarker_table_out
            self.update_pxmarker_cbox(self.pxmarker_table)

            self.save_pxmarker_table()

            self.ui.label_status.setText("Pixel markers saved.")
        else:
            pass

        pxmarker_dialog = None

    def load_pxmarker_table(self):
        """Initiates pixel marker table (from .pkl file if availble)

        """
        try:
            with open(self.file_abs_dir + '/settings/px_marker.pkl', 'rb') as f:
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

            with open(self.file_abs_dir + '/settings/px_marker.pkl', 'wb') as f:
                pickle.dump(pxmarker_table, f)
                return pxmarker_table

    def save_pxmarker_table(self):
        """Save edited pixel marker to .pkl file

        """
        with open(self.file_abs_dir + '/settings/px_marker.pkl', 'wb') as f:
            pickle.dump(self.pxmarker_table, f)

    def get_pxmarker_stylesheet(self, color):
        """Create stylesheet for pixel marker color indicator

        """
        return "background-color: rgb" + str(color) + ";"

    def update_pxmarker_cbox(self, pxmarker_table):
        """Updates pixel marker combobox with edited values

        """
        cbox_list = []
        for item in pxmarker_table:
            cbox_list.append(item[2])

        self.ui.cbox_pxmarker_select.clear()
        self.ui.cbox_pxmarker_select.addItems(cbox_list)

    #########################
    # Label matrix functions
    #########################

    def load_pxlabel_mat(self, pxlabel_filename):
        """Load pxlabel matrix if available, create one if not

        """
        try:
            with open(pxlabel_filename, 'rb') as f:
                return pickle.load(f)
        except EnvironmentError as e:
            num_labels = 10
            num_rows = self.img_size[0]
            num_cols = self.img_size[1]
            return np.zeros((num_labels,num_rows,num_cols), dtype=np.uint8)

    def save_pxlabel_mat(self):
        """Write pxlabel pickle file and update table_height

        """
        if self.pxlabel_frame.any() and not (self.pxlabel_frame == self.pxlabel_frame_ori).all():
            self.pxlabel_mat = self.update_pxlabel_mat(self.pxlabel_mat, self.pxlabel_frame, self.pxmarker_table)

            item_status = QTableWidgetItem(str(True))
            item_status.setForeground(QColor(0,255,0))

            item_name = QTableWidgetItem(self.img_filename)
            item_name.setForeground(QColor(0,255,0))

            self.ui.table_filename.setItem(self.img_table_idx,1,item_status)
            self.ui.table_filename.setItem(self.img_table_idx,0,item_name)

            with open(self.pxlabel_filename, 'wb') as f:
                pickle.dump(self.pxlabel_mat, f)

            try:
                cv2.imwrite(self.pxlabel_display_filename, self.display_frame)
            except:
                pass

            statusText = "Labels for " + self.img_filename + " saved."
            self.ui.label_status.setText(statusText)

    def update_pxlabel_mat(self, pxlabel_mat, pxlabel_frame, pxmarker_table):
        """Updates the pixel label matrix based on values in the pixel label frame

        """
        pxlabel_mat_out = pxlabel_mat.copy()
        idx = 0
        for marker in pxmarker_table[1:]:
            marker_label = np.zeros(self.img_size[:2], dtype=np.uint8)
            marker_label[np.where((pxlabel_frame == marker[1]).all(axis=2))[:2]] = 1
            marker_label = np.array([marker_label])
            pxlabel_mat_out[idx] = marker_label
            idx += 1

        return pxlabel_mat_out

    #########################
    # Keyboard Events
    #########################
    def keyReleaseEvent(self,event):
        """Keyboard shortcuts callback

        """
        key = event.key()
        if key == Qt.Key_W:
            if self.cursor_size < 20:
                self.cursor_size += 1
                if self.table_loaded:
                    self.update_display(self.mouse_pos, True)
        if key == Qt.Key_S:
            if self.cursor_size > 5:
                self.cursor_size -= 1
                if self.table_loaded:
                    self.update_display(self.mouse_pos, True)
        if key == Qt.Key_A:
            self.on_prev_frame_click()
        if key == Qt.Key_D:
            self.on_next_frame_click()
        if key == Qt.Key_E:
            self.ui.cbox_pxmarker_select.setCurrentIndex(0)
