from ui import Histogram
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from config import path_config
from function import *
from PyQt5.QtGui import QPixmap


# 曲线界面类
class Histogram(QtWidgets.QMainWindow, Histogram.Ui_MainWindow):
    def __init__(self):
        super(Histogram, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("今日曲线图")


class make_histogram(QThread):
    def __init__(self):
        super(make_histogram, self).__init__()
        self.histogram_window = Histogram()

    def show_histo(self):
        pixmap = QPixmap(path_config.histogram_path)  # 按指定路径找到图片
        self.histogram_window.l_histogram.setPixmap(pixmap)
        self.histogram_window.l_histogram.setScaledContents(True)  # 让图片自适应label大小

        time, density = get_txtdatabase(path_config.co_density_data)
        plt.bar(time, density)  # 条形图
        # plt.plot(time, density)  # 折线图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.xlabel("时间段")
        plt.ylabel("平均密度")
        plt.title("流量统计图")
        for x, y in enumerate(density):
            plt.text(x, y, '%s' % y)
        plt.savefig(path_config.histogram_path)

        mor_den, after_den, even_den = 0, 0, 0
        for x in range(5, 11):
            # print(density[x])
            mor_den += density[x]
        mor_den = round(mor_den / 6, 2)
        for x in range(12, 14):
            after_den += density[x]
        after_den = round(after_den / 3, 2)
        for x in range(15, 20):
            even_den += density[x]
        even_den = round(even_den / 5, 2)
        self.histogram_window.morning.setText(str(mor_den))
        self.histogram_window.afternoon.setText(str(after_den))
        self.histogram_window.evening.setText(str(even_den))
        # self.histogram.show()

    def run(self):
        self.show_histo()
