import sys
import cv2
import numpy as np

class MyImg():
	def __init__(self):
		self.exist=False
		self.img=None
		self.dis_img=None
		self.width=0
		self.height=0
		self.dis_w=0
		self.dis_h=0

	def load_img(self,imgName):
		self.img=cv2.imread(imgName)
		if self.img is None:
			return
		self.exist=True
		self.width,self.height = self.img.shape[0:2]

class MyImg_dst(MyImg):
	def __init__(self):
		super(MyImg_dst,self).__init__()

	def getDisImg(self,w,h):
		dis_mult=min(w/self.width,h/self.height)
		self.dis_w=int(dis_mult*self.width)
		self.dis_h=int(dis_mult*self.height)
		self.dis_img=cv2.resize(self.img,(self.dis_h,self.dis_w),interpolation=cv2.INTER_LINEAR)

class MyImg_src(MyImg):
	def __init__(self):
		super(MyImg_src,self).__init__()
		self.pos_x=0
		self.pos_y=0
		self.zoom=1.0
		self.edit_img=None
		self.edit_mask=None

	def getDisImg(self,w,h):
		dis_mult=min(w/self.width,h/self.height)
		self.dis_w=int(dis_mult*self.width)
		self.dis_h=int(dis_mult*self.height)
		self.dis_img=cv2.resize(self.img,(self.dis_h,self.dis_w),interpolation=cv2.INTER_LINEAR)
