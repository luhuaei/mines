from PyQt5.QtGui import QImage, QColor

    # 表情图片
IMG_BOMB = QImage("./images/bug.png")
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")
IMG_COFFEE = QImage("./images/cup.png")

    # 时钟颜色
NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}

# 等级
LEVELS = {
    'easy': (8, 10),
    'median': (16, 40),
    'hard': (24, 99),
}

# 状态
STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3
STATUS_STOP = 4

STATUS_ICONS = {
    STATUS_READY: "./images/plus.png",
    STATUS_PLAYING: "./images/smiley.png",
    STATUS_FAILED: "./images/cross.png",
    STATUS_SUCCESS: "./images/smiley-lol.png",
    STATUS_STOP: "./images/cup.png",
}
