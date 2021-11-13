from ui.ui_01 import Ui_MainWindow
from ui.Dialog import Ui_Dialog
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMessageBox
import sys
from mythread.show_time_thread import *
from mythread.detect_thread import *
from mythread.make_histogram_thread import *


# 登陆对话框
class Dialog(QtWidgets.QWidget, Ui_Dialog):
    close_signal = pyqtSignal()

    def __init__(self):
        super(Dialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("登录")
        # self.resize(350,150)
        self.pushButton_cancel.clicked.connect(self.close)  # 点击取消关闭窗口
        self.pushButton_ok.clicked.connect(self.textchanged)
        self.lineEdit.setEchoMode(self.lineEdit.Password)  # 设置密码不可见
        self.username, self.key = self.get_key()

    @staticmethod
    def get_key():
        user, key = get_txtdatabase(path_config.user_data)
        # print(user, key)
        return user, key

    # 核对密码是否正确
    def textchanged(self):
        key_g = self.lineEdit.text()
        flag = 0
        for key_w in self.key:
            if str(int(key_w)) == key_g:
                flag = 1
                self.close_signal.emit()
                self.close()
                break
        if flag == 0:
            self.lineEdit.setText('')
            QMessageBox.warning(self, '错误', '密码错误')


class fun(QtWidgets.QMainWindow, Ui_MainWindow):
    m_change_channel_signal = pyqtSignal(int)

    def __init__(self):
        super(fun, self).__init__()
        self.setupUi(self)
        # self.histogram = Histogram()  # 实例化人流量图形子界面类
        self.B_histogram.clicked.connect(self.play_pic)  # show人流量图形子界面
        self.B_video1.clicked.connect(self.video1)  # 视频1按键连接负责开启timer1定时器
        self.channel2.clicked.connect(self.video2)
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.detect)  # 定时器timer1每15ms触发一次detect函数

        self.show_time_th = show_time()  # 实例化显示时间的线程类
        self.show_time_th.start()  # 当主界面被创建时此线程开启
        # 线程每一秒将时间通过 update_time_signal信号 发送给主进程，主进程通过 showtime槽 来显示到label上
        self.show_time_th.update_time_signal.connect(self.showtime)

        self.detect_th_1 = detect()  # 创建检测线程对象
        # 检测线程获取到当前图像帧人数时通过 per_num_signal信号 将人数值发送回来
        # 主进程通过 get_people_num slot 来显示到label上
        self.detect_th_1.per_num_signal.connect(self.get_people_num)
        # 检测线程将密度通过 density_detect_signal信号 发回主进程，连接其 get_density槽 显示到label
        self.detect_th_1.density_detect_signal.connect(self.get_density)
        # 点击切换视频源，通过此信号控制线程处理哪个视频
        self.m_change_channel_signal.connect(self.detect_th_1.change_channel_slot)

        self.show_histogram_th = make_histogram()  # 创建生成流量曲线的线程对象

    def main_show(self):
        self.show()

    # 连接视频1
    def video1(self):
        self.m_change_channel_signal.emit(1)
        self.detect_th_1.start()
        self.timer1.start(10)  # 开始以每五毫秒的速率刷新显示的label
        # self.timer1.start(10)
        self.B_video1.setText("正在监测")
        self.channel2.setText("线路2")

    # 连接视频2
    def video2(self):
        self.m_change_channel_signal.emit(2)
        self.timer1.start(10)  # 开始以每五毫秒的速率刷新显示的label
        self.detect_th_1.start()
        self.B_video1.setText("线路1")
        self.channel2.setText("正在监测")

    def get_people_num(self, one_frame_per_num):
        self.label_9.setText(str(one_frame_per_num))

    def get_density(self, density):
        self.label_12.setText(str(density))
        if density >= 10:
            self.label_13.setStyleSheet("image: url(:/bg/back_img/red.png);")
        else:
            self.label_13.setStyleSheet("image: url(:/bg/back_img/green.png);")

    # 获取线程处理完的图像显示到主界面
    def detect(self):
        image = self.detect_th_1.get_detect_res()
        if image is not None:
            QIm = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            QIm = QImage(QIm.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            self.label_5.setPixmap(QPixmap.fromImage(QIm))
            self.label_5.setScaledContents(True)  # 每一帧适应label的大小

    # 显示曲线图
    def play_pic(self):
        self.show_histogram_th.start()
        self.show_histogram_th.histogram_window.show()

    # 显示日期
    def showtime(self, str_now_time):
        self.label_2.setText("     " + str_now_time)

    # 关闭程序（释放内存）
    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self,
                                     "社交距离监测系统",
                                     "是否退出程序",
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # Dialog_ui = Dialog()
    main_ui = fun()
    # Dialog_ui.close_signal.connect(main_ui.main_show)
    # Dialog_ui.show()
    main_ui.show()
    sys.exit(app.exec_())
