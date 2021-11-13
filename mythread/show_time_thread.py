import time
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime


class show_time(QThread):
    update_time_signal = pyqtSignal(str)

    def __init__(self):
        super(show_time, self).__init__()
        # self.cur_time = QDateTime.currentDateTime()
        self.str_cur_time = QDateTime.currentDateTime().toString()

    def now_time(self):
        self.str_cur_time = QDateTime.currentDateTime().toString()

    def get_now_time(self):
        return self.str_cur_time

    def run(self):
        while True:
            self.str_cur_time = QDateTime.currentDateTime().toString()
            time.sleep(1)
            self.update_time_signal.emit(self.str_cur_time)
