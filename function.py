import math
import matplotlib.pyplot as plt
import time
import cv2


# 输入原图中的一点，得到放射变换后图像中对应的点
def cvt_pos(pos, cvt_mat_t):
    u = pos[0]
    v = pos[1]
    x = int((cvt_mat_t[0][0] * u + cvt_mat_t[0][1] * v + cvt_mat_t[0][2]) / (
            cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2]))
    y = int((cvt_mat_t[1][0] * u + cvt_mat_t[1][1] * v + cvt_mat_t[1][2]) / (
            cvt_mat_t[2][0] * u + cvt_mat_t[2][1] * v + cvt_mat_t[2][2]))
    return (x, y)


# 计算两点之间的欧式距离
def get_pixel_distance(center1, center2):
    pixel_distance = int(math.sqrt((center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2))
    return pixel_distance


# 传入txt文件路径，以列表的形式返回txt的第一列和第二列数据
#
def get_txtdatabase(data_path):
    data1 = []
    data2 = []
    with open(data_path, "r") as f:  # 打开文件
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            content_value = line.split(sep=' ')
            if content_value[0] != '':
                data1.append(content_value[0])
                data2.append(float(content_value[1]))

    return data1, data2


def save_pic():
    time, density = get_txtdatabase("../data/density.txt")
    plt.bar(time, density)  # 条形图
    # plt.plot(time, density)  # 折线图

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.xlabel("时间段")
    plt.ylabel("平均密度")
    plt.title("流量统计图")
    for x, y in enumerate(density):
        plt.text(x, y, '%s' % y)
    plt.savefig('../data/his.jpg')


def uptotxt(hour, den, flag):
    time = []
    density = []

    with open("./data/density.txt", "r") as f:  # 打开文件
        for line in f.readlines():
            line = line.strip('\n')  # 去掉列表中每一个元素的换行符
            content_value = line.split(sep=' ')
            if content_value[0] != '':
                time.append(content_value[0])
                density.append(content_value[1])

    co_content = []
    for i in range(0, len(time)):
        if not flag:
            if i == int(hour):
                density[i] = str(den)
        else:
            density[i] = str(0)
        co_content.append(str(time[i]) + " " + str(density[i]) + "\n")

    # print(time)
    # print(density)
    # print(co_content)

    n = open('./data/co_density.txt', 'w+')
    n.writelines(co_content)
    n.close()


class Count_FPS:
    def __init__(self):
        super(Count_FPS, self).__init__()

        self.start_time = time.time()
        self.count = 0

    # 计算帧率：
    # param1：图片
    # param2：
    def fps_on_frame(self, frame):
        self.count += 1
        if (time.time() - self.start_time) != 0:
            fps = round(self.count / (time.time() - self.start_time), 2)
            cv2.putText(frame, "FPS {0}".format(str(fps)), (10, 45), 2, 2, (0, 0, 255),
                        2)
            self.count = 0
            self.start_time = time.time()
