import sys	
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
from gui import *

class MyWindow(QMainWindow,Ui_MainWindow):
	def __init__(self, parent=None):
		super(MyWindow,self).__init__(parent)
		self.setupUi(self)
		self.slot_init()

	def slot_init(self):
		self.action_dst_img.triggered.connect(partial(self.label_img.load_img,False))
		self.action_src_img.triggered.connect(partial(self.label_img.load_img,True))
		self.actionSave_Src.triggered.connect(partial(self.label_img.saveSrc,True))
		self.actionSave_Mask.triggered.connect(partial(self.label_img.saveSrc,False))
		self.action_save_as.triggered.connect(partial(self.label_img.save_img))
		self.Button_poisson.clicked.connect(self.label_img.poissonEdit)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = MyWindow()
	myWin.show()
	sys.exit(app.exec_())