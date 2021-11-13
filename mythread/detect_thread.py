from PyQt5.QtCore import QThread, QTimer
import cv2 as cv
from config import path_config
from function import get_pixel_distance
from PyQt5.QtCore import pyqtSignal
from cv2.dnn import DNN_TARGET_CPU
import datetime
from function import uptotxt


class detect(QThread):
    # 检测完人数密度时将密度发送回主进程
    density_detect_signal = pyqtSignal(float)
    # 当检测完一幅图像 将人数发送给主进程
    per_num_signal = pyqtSignal(int)

    def __init__(self):
        super(detect, self).__init__()
        self.model_bin = path_config.model_bin
        self.config_text = path_config.config_text
        self.objName = ["background",
                        "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair",
                        "cow", "diningtable", "dog", "horse",
                        "motorbike", "person", "pottedplant",
                        "sheep", "sofa", "train", "tvmonitor"]

        # load caffe model
        self.net = cv.dnn.readNetFromCaffe(self.config_text, self.model_bin)
        self.net.setPreferableTarget(DNN_TARGET_CPU)

        # 获得所有层名称与索引
        self.layerNames = self.net.getLayerNames()
        self.lastLayerId = self.net.getLayerId(self.layerNames[-1])
        self.lastLayer = self.net.getLayer(self.lastLayerId)

        # 读取指定url地址的实时视频流
        # self.video_url = path_config.video_url_1
        # self.cap = cv.VideoCapture(self.video_url)
        # if not self.cap.isOpened():
        #     self.cap = cv.VideoCapture(1)
        self.cap = None

        self.frame = None
        self.width = 680
        self.height = 430
        self.dim = (self.width, self.height)
        # 每一幅图像中所有人的中心坐标
        self.coordinate = []
        # 图像中人得高度
        self.w_and_h_box = []
        # 记录检测图片得帧数
        self.frame_count = 0
        # 开始记录帧数时，每一帧人数之和
        self.per_num = 0
        # 一幅图像的人数
        self.one_frame_per_num = 0

        # 两个人是否大致在同一水平线
        self.eq_level = 100
        # 两点之间的阈值
        self.scale_factor1 = 50
        self.scale_factor2 = 150
        # 框的面积
        self.Count_area_p = 0.3
        self.A_area = 480*640

        # 每五秒计算一次密度
        # 通过 compute_density 函数将密度值发给主进程
        self.density_timer = QTimer()
        self.density_timer.timeout.connect(self.compute_density)
        self.density_timer.start(5000)
        # 到一个小时上传至数据库
        self.time_min_sec = datetime.datetime.now().strftime('%M%S')
        self.time_min_sec_text = str(self.time_min_sec)
        self.time_list = ['5954', '5955', '5956', '5957', '5958', '5959']

    # 返回处理的结果图像
    def get_detect_res(self):
        return self.frame

    # 计算图像中人的距离是否符合阈值
    def compare_distance(self, coordinate_list):
        # print("计算图像中人的距离是否符合阈值")
        per_num = len(coordinate_list)
        if per_num >= 2:
            i = 0
            while i < per_num:
                print("人数 %d " % len(coordinate_list))
                j = i + 1
                while j < per_num:
                    # print("当前是第 %d 和 %d 个框" % (i, j))
                    is_eq_level = coordinate_list[i][1] - coordinate_list[j][1]
                    print("相似水平线差值 %d" % is_eq_level)
                    if self.eq_level >= is_eq_level >= -self.eq_level:
                        pixel_distance = get_pixel_distance(coordinate_list[i], coordinate_list[j])  # 求两点之间的欧式距离
                        print("最小距离 : %d " % pixel_distance)
                        person_h = self.w_and_h_box[i][1]  # 人的身高
                        # i号框的左上角和右下角坐标
                        (x1, y1) = (
                            int(coordinate_list[i][0] - self.w_and_h_box[i][0] / 2),
                            int(coordinate_list[i][1] - self.w_and_h_box[i][1] / 2))
                        (x2, y2) = (
                            int(coordinate_list[i][0] + self.w_and_h_box[i][0] / 2),
                            int(coordinate_list[i][1] + self.w_and_h_box[i][1] / 2))
                        # j号框的左上角和右下角坐标
                        (t1, p1) = (
                            int(coordinate_list[j][0] - self.w_and_h_box[j][0] / 2),
                            int(coordinate_list[j][1] - self.w_and_h_box[j][1] / 2))
                        (t2, p2) = (
                            int(coordinate_list[j][0] + self.w_and_h_box[j][0] / 2),
                            int(coordinate_list[j][1] + self.w_and_h_box[j][1] / 2))

                        # print("两行人之间的距离 %d" % pixel_distance)
                        # print("框比例高 %d" % person_h)
                        if pixel_distance < self.scale_factor1 and pixel_distance < person_h * 1:
                            print("最小距离1 : %d " % pixel_distance)
                            # if pixel_distance < 50:
                            color = (0, 0, 255)
                            cv.line(self.frame, coordinate_list[i], coordinate_list[j], color, 2)
                            cv.rectangle(self.frame, (t1, p1), (t2, p2), color, 1)
                            cv.rectangle(self.frame, (x1, y1), (x2, y2), color, 1)
                        elif self.scale_factor2 > pixel_distance > self.scale_factor1 and pixel_distance < person_h * 0.8:
                            print("最小距离2 : %d " % pixel_distance)
                            color = (0, 0, 255)
                            cv.line(self.frame, coordinate_list[i], coordinate_list[j], color, 2)
                            cv.rectangle(self.frame, (t1, p1), (t2, p2), color, 1)
                            cv.rectangle(self.frame, (x1, y1), (x2, y2), color, 1)
                    j += 1
                i += 1

    # 每五秒计算一次人的密度
    def compute_density(self):
        # print("计算密度")
        try:
            per_density = round(self.per_num / self.frame_count, 2)  # 保留两位小数
        except:
            per_density = 0

        if per_density >= 1:
            self.density_detect_signal.emit(per_density)
        else:
            self.density_detect_signal.emit(0.0)

        self.time_min_sec = datetime.datetime.now().strftime('%M%S')
        self.time_min_sec_text = str(self.time_min_sec)
        for i in self.time_list:
            if self.time_min_sec_text == i:
                hour = str(datetime.datetime.now().strftime('%H'))
                uptotxt(hour, per_density, False)

        self.per_num = 0
        self.frame_count = 0

    # 开始处理一幅图像
    def to_detect(self):
        ret, frame = self.cap.read()
        if ret is False:
            print("读取视频错误!")
            return
        h, w = frame.shape[:2]
        blobImage = cv.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), True, False)
        print()
        self.net.setInput(blobImage)
        cvOut = self.net.forward()
        self.coordinate.clear()
        for detection in cvOut[0, 0, :, :]:
            score = float(detection[2])
            objIndex = int(detection[1])
            if score > 0.5 and objIndex == 15:
                left = detection[3] * w
                top = detection[4] * h
                right = detection[5] * w
                bottom = detection[6] * h
                center = (int(left + (right - left) / 2), int(top + (bottom - top) / 2))
                self.coordinate.append(center)
                self.w_and_h_box.append((right - left, bottom - top))
                area = round((right - left)*(bottom - top), 2)
                area_proportion = round(area/self.A_area, 2)
                # print("框的面积:", area_proportion)

                # 绘制
                cv.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (255, 0, 0), thickness=2)
                cv.putText(frame, "score:%.2f, %s" % (score, self.objName[objIndex]),
                           (int(left) - 10, int(top) - 5), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, 8)

        self.frame = frame
        self.one_frame_per_num = len(self.coordinate)
        self.frame_count += 1
        self.per_num += self.one_frame_per_num
        self.compare_distance(self.coordinate)

        # frame = cv.resize(frame, self.dim)

    def change_channel_slot(self, channel):
        print("main send a data", channel)
        if channel == 1:
            self.cap = cv.VideoCapture(path_config.video_url_1)
            if not self.cap.isOpened():
                print("正在尝试打开摄像头。。。")
                self.cap = cv.VideoCapture(1)
                if not self.cap.isOpened():
                    print("正在尝试打开摄像头。。。")
                    self.cap = cv.VideoCapture(2)
        else:
            self.cap = cv.VideoCapture(path_config.video_url_2)

        # self.to_detect()

    # 线程的run函数
    def run(self):
        while True:
            self.to_detect()
            self.per_num_signal.emit(self.one_frame_per_num)
