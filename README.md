##Poisson Image Editing UI

这是一个能够进行泊松图像编辑的图形用户界面应用，是算法设计与分析课程project的简化版

该简化版仅保留泊松图像编辑的部分，以解决完整版GUI环境配置困难、深度学习模型文件过大导致难以运行的问题

完整版见https://github.com/Lllmmr/Image-Blending-GUI

###运行

该项目在`python 3`下运行

需要安装`pyqt5`, `numpy`, `opencv`

```
$ pip install pyqt5 numpy opencv-python
```

下载该项目到本地，运行`main.py`即可

###操作指南

####图片操作：

`File->Open->dst_img/src_img`加载目标（背景）图像

按住空格键不放，可以用鼠标左键对源图像位置进行拖动

使用鼠标滚轮可以对源图像进行缩放

使用鼠标左键圈出源图像要进行编辑的区域

单击鼠标右键可以取消对编辑区域的选择

将图片移动/缩放/选区完毕后，可以使用右侧的按键进行图像编辑

`File->Save As`将图像编辑的结果保存到本地

####按键及功能：

右侧上方按键为对各种图像编辑模式的选择，模式都选择完后，即可按右侧最下方`Poisson Image Editing`按键进行图像编辑

最上方三个选项`Normal`, `Mixed`, `Transfer`分别表示“正常”，“混合”和“特征转换”

混合模式可以进行图像中线条的迁移，例如将文字迁移到背景上

特征转换模式可以进行纹路特征的转换，例如橘子和梨表面的特征转换



第四个选项`Local Changes`表示利用泊松编辑对源图像进行局部的改动，该模式下目标图像和源图像为同一张，因此只显示通过`File->Open->src_img`加载的图像

在该模式下，还需至少选择`Flattening`, `Illumination`, `Color`中的至少一项（建议只选一项）

`Flattening`对图像的编辑区域做扁平化处理

`low`, `high`两个滑动条调整扁平化的参数

`Illumination`调整图像所选区域的亮度

`a`, `b`两个滑动条调整亮度变化的参数

`Color`改变所选区域的颜色

通过下方按键选择要变成的颜色，选中`Gray`可将背景变为灰色

#### 拓展功能：

`File->Save Mask/Save Src`可将经过缩放、裁剪后的源图像及其单通道mask保存到本地，方便其他未加入GUI的算法获取ROI