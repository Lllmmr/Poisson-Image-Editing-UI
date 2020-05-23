import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial

from Myimg import *

class MyLabel(QLabel):
	def __init__(self,parent=None):
		super(MyLabel,self).__init__(parent)
		self.setMouseTracking(False)
		self.pos_xy = []
		self.dst_img=MyImg_dst()
		self.src_img=MyImg_src()
		self.result_img=None

	def init_dis_img(self):
		self.dis_img=np.zeros([self.width()-1,self.height()-1,3],np.uint8)

	def init_mask(self):
		self.dis_mask=np.zeros([self.width()-1,self.height()-1],np.uint8)
		self.dis_mask[:,:]=255

	def load_img(self,img,is_dst):
		imgName,imgType=QFileDialog.getOpenFileName(self, "Open", "", "*.jpg;;*.png")
		img.load_img(imgName)
		if not img.exist:
			return
		if not is_dst:
			self.init_mask()
		img.getDisImg(self.width()-1,self.height()-1)
		self.display_img()

	def display_img(self):
		self.init_dis_img()
		tmp_mask=np.zeros([self.width()-1,self.height()-1],np.uint8)
		rgb_mask=cv2.cvtColor(self.dis_mask,cv2.COLOR_GRAY2BGR)
		if self.dst_img.exist and self.src_img.exist:
			tmp_fore=np.zeros([self.width()-1,self.height()-1,3],np.uint8)
			tmp_back=np.zeros([self.width()-1,self.height()-1,3],np.uint8)
			tmp_back[0:self.dst_img.dis_w,0:self.dst_img.dis_h,:]=self.dst_img.dis_img
			tmp_fore[0:self.src_img.dis_w,0:self.src_img.dis_h,:]=self.src_img.dis_img
			tmp_fore=cv2.bitwise_and(tmp_fore,rgb_mask)
			self.dis_img=cv2.addWeighted(tmp_back,0.4,tmp_fore,0.6,0)
			tmp_mask[0:self.src_img.dis_w,0:self.src_img.dis_h]=255
			tmp_mask=cv2.bitwise_and(tmp_mask,self.dis_mask)
			tmp_mask[0:self.dst_img.dis_w,0:self.dst_img.dis_h]=255
		elif self.dst_img.exist:
			self.dis_img[0:self.dst_img.dis_w,0:self.dst_img.dis_h,:]=self.dst_img.dis_img
			tmp_mask[0:self.dst_img.dis_w,0:self.dst_img.dis_h]=255
		elif self.src_img.exist:
			self.dis_img[0:self.src_img.dis_w,0:self.src_img.dis_h,:]=self.src_img.dis_img
			tmp_mask[0:self.src_img.dis_w,0:self.src_img.dis_h]=255
			self.dis_img=cv2.bitwise_and(self.dis_img,rgb_mask)
			tmp_mask=cv2.bitwise_and(tmp_mask,self.dis_mask)

		dis_rgba=cv2.merge((self.dis_img,tmp_mask))
		q_img=QImage(dis_rgba.data,dis_rgba.shape[1],dis_rgba.shape[0],QImage.Format_ARGB32)
		self.setPixmap(QPixmap(q_img))

	def displayResult(self):
		tmp_result=cv2.cvtColor(self.result_img,cv2.COLOR_BGR2RGB)
		q_img=QImage(tmp_result,tmp_result.shape[1],tmp_result.shape[0],QImage.Format_RGB888)
		self.setPixmap(QPixmap(q_img))

	def poissonEdit(self):
		center=(self.src_img.dis_h//2,self.src_img.dis_w//2)
		self.result_img=cv2.seamlessClone(self.src_img.dis_img,self.dst_img.dis_img,self.dis_mask,center,cv2.NORMAL_CLONE)
		self.displayResult()

	def paintEvent(self, event):
		super().paintEvent(event)
		painter = QPainter()
		painter.begin(self)
		pen = QPen(Qt.red, 1, Qt.SolidLine)
		painter.setPen(pen)
		if len(self.pos_xy) > 1:
			point_start = self.pos_xy[0]
			for pos_tmp in self.pos_xy:
				point_end = pos_tmp
				painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
				point_start = point_end
		painter.end()

	def mousePressEvent(self, event):
		if event.buttons() == QtCore.Qt.RightButton:
			self.init_mask()
			self.display_img()


	def mouseMoveEvent(self, event):
		pos_tmp = (event.pos().x(), event.pos().y())
		self.pos_xy.append(pos_tmp)
		self.update()

	def mouseReleaseEvent(self, event):
		if event.buttons() == QtCore.Qt.RightButton:
			print("A")
			return
		if len(self.pos_xy)<3:
			self.pos_xy.clear()
			return
		self.dis_mask[:,:]=0
		roi_corners = np.array([self.pos_xy], dtype=np.int32)
		cv2.fillPoly(self.dis_mask,roi_corners,(255,255,255))
		self.pos_xy.clear()
		self.display_img()
		self.update()
