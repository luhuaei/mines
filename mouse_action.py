from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from config import *

# 行为类，用来控制各种行为
class Pos(QWidget):
    # 信号
    # 后面两个int表示发送两个数字信号
    expandable = pyqtSignal(int, int)
    clicked = pyqtSignal()
    count = pyqtSignal()
    ohno = pyqtSignal()

    # 初始化设定
    def __init__(self, x, y, *args, **kwargs):
        # 对父类更改
        super(Pos, self).__init__(*args, **kwargs)
        # 固定大小
        self.setFixedSize(QSize(20, 20))

        # 坐标
        self.x = x
        self.y = y

    # 重置
    def reset(self):
        # 是否开始
        self.is_start = False
        # 是否隐藏
        self.is_mine = False
        # 相邻的个数
        self.adjacent_n = 0

        # 是否显示
        self.is_revealed = False
        # 是否插旗
        self.is_flagged = False
        # 更新
        self.update()

    def paintEvent(self, event):
        '''用来展示当前位置的状态，使用QPainter进行描绘，而event.rect()将会提供一个需要
        描绘的分界。'''
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # 分界，具有四个坐标
        r = event.rect()

        # 被揭露的瓦片将会根据是否为一个开始的位置、埋雷、空地方而描绘不同的形状。
        if self.is_revealed:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        # 填充的位置，以及指定的颜色
        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.is_revealed:
            if self.is_start:
                # 需要使用QPixmap对QImages进行转化
                # 使用drawPixmap进行描绘
                # 如果当前的坐标是开始的第一个坐标，则显示小火箭图标
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:
                # 如果当前的坐标是雷则显示雷的图标
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            # 对于空的位置，展示在当前坐标旁边9宫格内雷的数目
            elif self.adjacent_n > 0:
                # 指定展示的数字的颜色
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                # 字体设置
                f = p.font()
                # 加粗
                f.setBold(True)
                # 对QPainter进行设置字体
                p.setFont(f)
                # 使用drawText来描绘文字
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))
        # 如果当前位置为旗子
        elif self.is_flagged:
                p.drawPixmap(r, QPixmap(IMG_FLAG))

    def flag(self):
        # 插旗函数，如果已经插旗则取消
        if self.is_flagged:
            self.is_flagged = False
        else:
            self.is_flagged = True
        self.update()

        # 发送当前坐标点击信号
        self.clicked.emit()
        self.count.emit()

    def reveal(self):
        # 揭开函数
        self.is_revealed = True
        self.update()

    def click(self):
        # 如果没有揭露，就揭露
        if not self.is_revealed:
            self.reveal()
            # 如果邻近没有雷，则揭露判断没有雷的小方块
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)
        # 发送点击信号
        self.clicked.emit()
        self.count.emit()

    def mouseReleaseEvent(self, e):
        # 如果点击右键并且当前位置没有被揭露，则插旗
        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()

        # 如果点击左键且当前坐标没有插旗，如果正好揭开具有雷的方块则结束游戏
        elif (e.button() == Qt.LeftButton and not self.is_flagged):
            self.click()

            if self.is_mine:
                self.ohno.emit()
