from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *

import random
import time

from config import *
from mouse_action import *


class MainWindow(QMainWindow):
    # 主窗口类
    def __init__(self, *args, **kwargs):
        # 开局初始化
        super(MainWindow, self).__init__(*args, **kwargs)
        # 小方格与地雷数，默认等级为中等
        self.b_size, self.n_mines = LEVELS["median"]

        self.init()
        self.game_ready()
        # 展示窗口
        self.setWindowTitle("mines")
        self.show()


    def init(self):
        # 窗口的初始化函数，不仅仅用于开始的初始化，还可以用在后面更新窗口的控件
        # 如在窗口的小方格数目发生变化时，需要重新对窗口进行渲染
        # 布局变量,垂直空间布局
        vb = QVBoxLayout()
        self.create_menubar()
        self.create_horizontal_box()
        self.create_grid_box()

        vb.setMenuBar(self.menubar)
        vb.addLayout(self.horizontal_box)
        vb.addLayout(self.grid)

        # QWidget 指定布局为vb，而vb中加入hb布局以及grid布局
        w = QWidget()
        w.setLayout(vb)

        # QMainWindow 设定主要的中心文件为w
        self.setCentralWidget(w)


    def create_menubar(self):
        # 菜单栏
        self.menubar = QMenuBar()
        # 文件菜单
        self.setting_menu = QMenu("&Setting", self)

        # 退出行为
        exitaction = QAction("&Exit", self)
        exitaction.setShortcut("Ctrl+Q")
        exitaction.setStatusTip("Exit application")
        exitaction.triggered.connect(qApp.quit)

        # 增加子菜单
        self.create_levels_menus()
        self.setting_menu.addMenu(self.levels_menus)
        self.setting_menu.addAction(exitaction)
        # 将文件菜单增加到菜单栏
        self.menubar.addMenu(self.setting_menu)


    def create_levels_menus(self):
        # levels 选择，子菜单，在level下有三个模式
        self.levels_menus = QMenu("Levels", self)

        # 将多个check格组成组
        ag = QActionGroup(self, exclusive = True)
        # 等级
        easy = ag.addAction(QAction("easy", self, checkable = True))
        median = ag.addAction(QAction("median", self, checkable = True))
        hard = ag.addAction(QAction("hard", self, checkable = True))
        median.setChecked(True)
        # 将各个行为添加到levels菜单中
        self.levels_menus.addActions([easy, median, hard])

        # 连接选择函数
        self.levels_menus.triggered.connect(self.levels_select)


    def levels_select(self):
        # 将self.levels_menus赋予给menu，信号的发送体
        menu = self.sender()
        # 遍历menu中所有action
        for action in menu.actions():
            # 判断哪一个action被选中
            if action.isChecked():
                # 获取行为的文本描述，并将其选择成游戏的等级
                level = action.text()
                # 更新等级难度
                self.b_size, self.n_mines = LEVELS[level]
                # 对窗口的内容进行重新渲染
                self.init()
                # 重置游戏
                self.game_ready()


    def create_horizontal_box(self):
        # 水平布局类
        self.horizontal_box = QHBoxLayout()

        # 雷控件
        self.mines = QLabel()
        # 上下左右居中
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 旗帜
        self.flag = QLabel()
        self.flag.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 时钟控件
        self.clocks = QLabel()
        # 上下左右居中
        self.clocks.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 设定雷与时钟的字体大小
        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clocks.setFont(f)
        self.flag.setFont(f)

        # 设定文字
        self.mines.setText("%03d" % self.n_mines)
        self.clocks.setText("000")
        self.flag.setText("000")

        # 设定按钮图片
        self.button = QPushButton()
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        # 按钮点击更新按压状态
        self.button.pressed.connect(self.button_pressed)

        # 炸弹控件图片
        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        # 右对齐以及上下居中
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.horizontal_box.addWidget(l)

        # 旗子控件图片
        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_FLAG))
        l.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # 添加各个控件
        self.horizontal_box.addWidget(self.mines)
        self.horizontal_box.addWidget(l)
        self.horizontal_box.addWidget(self.flag)
        self.horizontal_box.addWidget(self.button)
        self.horizontal_box.addWidget(self.clocks)

        # 时钟图片
        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        # 左对齐以及上下居中
        l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.horizontal_box.addWidget(l)


    def create_grid_box(self):
        # 网格
        self.grid = QGridLayout()
        # 网格空隙
        self.grid.setSpacing(5)


    def game_ready(self):
        self.update_status(STATUS_READY)
        # 初始化map函数
        self.init_map()
        # 重置map函数
        self.reset_map()
        self.update_status(STATUS_PLAYING)

    def init_map(self):
        # map初始化函数
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                # 布局坐标
                w = Pos(x, y)
                self.grid.addWidget(w, y, x)

                # 链接信号
                w.clicked.connect(self.trigger_start)
                w.count.connect(self.monitor)
                w.expandable.connect(self.expand_reveal)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        # 清除所有的雷
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                # 相当于w为Pos类
                w = self.grid.itemAtPosition(y, x).widget()
                # 重置各个参数指定
                w.reset()

        # 增加雷
        # 位置
        positions = []

        # 当雷的个数小于指定的个数时
        while len(positions) < self.n_mines:
            # 随机生成坐标
            x = random.randint(0, self.b_size - 1)
            y = random.randint(0, self.b_size - 1)
            # 如果生成的坐标当前没有雷
            if (x, y) not in positions:
                # Pos类
                w = self.grid.itemAtPosition(y, x).widget()
                # 指定当前的位置为雷
                w.is_mine = True
                # 将当前坐标组成元组添加到坐标位置的列表中
                positions.append((x, y))

        def get_adjacency_n(x, y):
            # 计算邻近的雷个数
            positions = self.get_surrounding(x, y)
            # w 为Pos类，如果附近的坐标中存在雷则返回1,否则0,最后相加
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        # 为每一个坐标上加上邻近的雷的个数
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                # w为Pos类
                w = self.grid.itemAtPosition(y, x).widget()
                w.adjacent_n = get_adjacency_n(x, y)


        # 开始标注位置
        while True:
            x = random.randint(0, self.b_size - 1)
            y = random.randint(0, self.b_size - 1)
            # 根据坐标获取位置的类
            w = self.grid.itemAtPosition(y, x).widget()

            # 开局位置
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                # 标注为小火箭
                w.is_start = True

                # 揭露小火箭附近的空区
                for w in self.get_surrounding(x, y):
                    if not w.is_mine:
                        w.click()
                break

    def get_surrounding(self, x, y):
        positions = []

        # 根据坐标上下左右计算9宫格中各个小方块的坐标
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def button_pressed(self):
        # 当按钮按压时，如果当前的状态为正在玩，将失败，揭露全部小方块
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()

        # 如果当前的状态为失败，当按压按钮，将进入准备状态，重置小方块
        elif self.status == STATUS_FAILED or self.status == STATUS_SUCCESS:
            self.update_status(STATUS_READY)
            self.reset_map()

    def reveal_map(self):
        # 揭露所有小方块
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                # 揭露
                w.reveal()

    # 展开揭露方块邻近没有雷的小方块
    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine and not w.is_flagged:
                    w.click()

    # 开始信号
    def trigger_start(self, *args):
        if self.status != STATUS_PLAYING:
            # 计时器
            self._timer = QTimer()
            # 超时更新
            self._timer.timeout.connect(self.update_timer)
            # 1s 计时
            self._timer.start(1000)
            # 第一次点击
            self.update_status(STATUS_PLAYING)
            # 计时开始
            self._timer_start_nsecs = int(time.time())

    # 监控函数
    def monitor(self):
        # 用户插的旗子
        flags = 0
        # 剩余的雷
        mines = self.n_mines
        #正确插中的旗子
        right_flags = 0
        # 没有翻开的小方格
        rest_grid = 0
        # 遍历整个地图，计算各个的个数
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                # 如果当前被插旗
                if w.is_flagged:
                    flags += 1

                # 如果当前为插旗而实际也为雷的位置
                if w.is_flagged and w.is_mine:
                    # 隐藏的雷计数减1
                    mines += -1
                    # 插中的旗子
                    right_flags += 1

                # 计算当前地图中没有被揭开以及没有被插旗的小方格
                if not w.is_revealed and not w.is_flagged:
                    rest_grid += 1
        # 设置flag控件上显示旗子的个数
        self.flag.setText("%03d" % flags)

        # 判断游戏是否达到结束状态，雷的剩余个数、旗子的个数要与雷的个数相同
        # 最后要判断当前地图上是否还有小方格没有被揭开
        if mines == 0 and right_flags == self.n_mines and rest_grid == 0:
            self.reveal_map()
            self.update_status(STATUS_SUCCESS)

    # 更新状态并设定图标跟随状态变化
    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    # 利用当前的时间减去开始的时间而计算剩下的时间，并clocks更新
    def update_timer(self):
        if self.status == STATUS_PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clocks.setText("%03d" % n_secs)

    # 游戏结束，揭露所有的小方块且更新状态为失败
    def game_over(self):
        self.reveal_map()
        self.update_status(STATUS_FAILED)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
