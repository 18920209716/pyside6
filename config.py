#
# 所有用到的路径信息都放在Config类里


class Config:
    def __init__(self):
        super(Config, self).__init__()
        self.model_bin = None
        self.config_text = None
        self.video_url_1 = None
        self.video_url_2 = None
        self.model_path()

        self.histogram_path = None
        self.co_density_data = None
        self.density_data = None
        self.user_data = None
        self.back_img_path = None
        self.other_path()

    def model_path(self):
        # self.model_bin = "./model/person-detection-retail-0013.bin"
        # self.config_text = "./model/person-detection-retail-0013.xml"
        self.model_bin = "./model/MobileNetSSD_deploy.caffemodel"
        self.config_text = "./model/MobileNetSSD_deploy.prototxt"
        # self.video_url_1 = "rtsp://admin:2321welcome@192.168.1.102:554/Streaming/Channels/101"
        self.video_url_1 = 0
        # self.video_url_2 = "rtsp://admin:2321welcome@192.168.1.104:554/Streaming/Channels/101"
        self.video_url_2 = "111.mp4"

    def other_path(self):
        self.histogram_path = "./data/histogram.jpg"
        self.co_density_data = "./data/co_density.txt"
        self.user_data = "./data/user.txt"
        self.back_img_path = "./back_img/b9.jpg"
        self.density_data = None


path_config = Config()
