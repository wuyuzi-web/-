import os

# 屏幕设置大小
SCREENSIZE = (700, 700)
# 元素尺寸
NUMGRID = 8
GRIDSIZE = 64
XMARGIN = (SCREENSIZE[0] - GRIDSIZE * NUMGRID) // 2
YMARGIN = (SCREENSIZE[1] - GRIDSIZE * NUMGRID) // 2
# 获取根目录
ROOTDIR = os.getcwd()
# FPS
FPS = 30