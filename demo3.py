import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QLineEdit, QPushButton, QLabel, QGraphicsTextItem, QGraphicsLineItem, QHBoxLayout, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QPen, QFont, QPixmap, QBrush, QPalette, QFontDatabase
from PyQt5.QtCore import Qt


class PlotWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载字体文件
        font_id = QFontDatabase.addApplicationFont("Font/AaWuDaoJia-2.ttf")
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            self.custom_font = QFont(font_families[0], 20)
        else:
            print("Fail to load font")

        self.custom_style = "color: rgb(255, 0, 102); border: 2px solid rgb(0, 255, 0)"

        self.setWindowTitle("风力发电机组防雷击电涌保护器热稳定试验电源系统")
        self.setGeometry(100, 100, 1280, 720)

        # 加载背景图片
        self.set_background("Pic/Skyline_Background.png")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.top_scene = QGraphicsScene()
        self.top_view = QGraphicsView()
        self.top_view.setScene(self.top_scene)
        self.top_view.setFixedSize(1000, 61)  # 根据需要调整大小
        self.top_view.setStyleSheet("border: 0px;")  # 可选，移除边框
        # 设置场景的背景刷为透明
        self.top_view.setBackgroundBrush(Qt.transparent)
        # 启用视图的透明背景属性
        self.top_view.setAttribute(Qt.WA_TranslucentBackground)
        self.add_pics()

        # 顶层的垂直布局
        top_layout = QVBoxLayout()
        central_widget.setLayout(top_layout)

        # 数据层的水平布局
        data_layout = QHBoxLayout()
        central_widget.setLayout(data_layout)

        # 左侧的垂直布局
        left_layout = QVBoxLayout()
        central_widget.setLayout(left_layout)

        # 右侧的垂直布局
        right_layout = QVBoxLayout()
        central_widget.setLayout(right_layout)

        # logo附近的水平布局
        logo_layout = QHBoxLayout()
        central_widget.setLayout(logo_layout)

        # logo附近的水平布局
        plot_layout = QHBoxLayout()
        central_widget.setLayout(plot_layout)

        # 将两侧的布局添加到顶层的水平布局
        data_layout.addLayout(left_layout, 1)
        data_layout.addLayout(right_layout, 3)
        top_layout.addLayout(data_layout)
        top_layout.insertWidget(0, self.top_view)  # 将 top_view 添加到顶层布局的最上方

        # 将logo布局添加到右侧布局
        right_layout.addLayout(plot_layout)
        right_layout.addLayout(logo_layout)

        # 左侧上边距
        left_layout.addSpacing(50)

        # Create input fields and add point button
        self.time_label = QLabel("时间:")
        self.time_label.setFixedWidth(100)
        self.time_label.setFont(self.custom_font)
        self.time_label.setStyleSheet(self.custom_style)
        left_layout.addWidget(self.time_label)
        self.time_edit = QLineEdit()
        self.time_edit.setFixedWidth(200)
        self.time_edit.setFixedHeight(30)
        left_layout.addWidget(self.time_edit)
        left_layout.addSpacing(30)  # 添加额外的间距

        self.current_label = QLabel("电流:")
        self.current_label.setFixedWidth(100)
        self.current_label.setFont(self.custom_font)
        self.current_label.setStyleSheet(self.custom_style)
        left_layout.addWidget(self.current_label)
        self.current_edit = QLineEdit()
        self.current_edit.setFixedWidth(200)
        self.current_edit.setFixedHeight(30)
        left_layout.addWidget(self.current_edit)
        left_layout.addSpacing(30)  # 添加额外的间距

        self.temp_label = QLabel("温度:")
        self.temp_label.setFixedWidth(100)
        self.temp_label.setFont(self.custom_font)
        self.temp_label.setStyleSheet(self.custom_style)
        left_layout.addWidget(self.temp_label)
        self.temp_edit = QLineEdit()
        self.temp_edit.setFixedWidth(200)
        self.temp_edit.setFixedHeight(30)
        left_layout.addWidget(self.temp_edit)
        left_layout.addSpacing(200)  # 添加额外的间距

        self.add_button = QPushButton("添加点")
        self.add_button.setFixedWidth(250)
        left_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.add_point)
        left_layout.addStretch(1)  # 添加伸缩项

        # Create plot view and scene
        self.plot_view = PlotView()
        self.plot_view.setFixedSize(800, 400)  # 设置图表的固定大小
        self.plot_view.setStyleSheet("background-color: lightblue;")  # 设置图表背景颜色
        plot_layout.addWidget(self.plot_view)
        self.plot_scene = QGraphicsScene()
        self.plot_view.setScene(self.plot_scene)

        # 创建 QLabel 用于显示 logo 图像
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("Pic/logo.png")  # 加载 logo 图像
        self.logo_label.setPixmap(logo_pixmap)
        logo_layout.addStretch()
        logo_layout.addWidget(self.logo_label)

        # Data storage
        self.data = []

        # Draw axis and legend
        self.draw_axis()
        self.draw_legend()

    def add_pics(self):
        # 加载素材图片
        title_bar_above = QPixmap("Pic/Title_Bar_Above.png")

        self.titlebar = QGraphicsPixmapItem(title_bar_above)
        self.titlebar.setPos(30, 50)

        # 将图片添加到场景中
        self.top_scene.addItem(self.titlebar)

    def set_background(self, image_path):  # 设定背景图片
        # 加载图片
        pixmap = QPixmap(image_path)

        # 创建画刷并设置纹理
        brush = QBrush(pixmap)

        # 获取调色板并设置画刷作为背景
        palette = self.palette()
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

    def draw_axis(self):
        # Draw X axis
        self.plot_scene.addLine(50, 350, 750, 350)
        x_axis_label = QGraphicsTextItem("时间")
        x_axis_label.setPos(760, 340)
        self.plot_scene.addItem(x_axis_label)

        # Draw Y axis for current
        self.plot_scene.addLine(50, 50, 50, 350)
        y1_axis_label = QGraphicsTextItem("电流")
        y1_axis_label.setPos(20, 40)
        self.plot_scene.addItem(y1_axis_label)

        # Draw Y axis for temperature
        self.plot_scene.addLine(750, 50, 750, 350)
        y2_axis_label = QGraphicsTextItem("温度")
        y2_axis_label.setPos(735, 40)
        self.plot_scene.addItem(y2_axis_label)

    def draw_legend(self):
        # Draw blue line legend
        blue_line = QGraphicsLineItem(545, 20, 600, 20)
        blue_pen = QPen(Qt.blue)
        blue_pen.setWidth(2)
        blue_line.setPen(blue_pen)
        self.plot_scene.addItem(blue_line)

        # Add text for blue line
        blue_text = QGraphicsTextItem("温度")
        blue_text.setPos(605, 0)  # 向上移动温度文字
        self.plot_scene.addItem(blue_text)

        # Draw red line legend
        red_line = QGraphicsLineItem(545, 50, 600, 50)
        red_pen = QPen(Qt.red)
        red_pen.setWidth(2)
        red_line.setPen(red_pen)
        self.plot_scene.addItem(red_line)

        # Add text for red line
        red_text = QGraphicsTextItem("电流")
        red_text.setPos(605, 30)  # 向下移动电流文字
        self.plot_scene.addItem(red_text)

    def add_point(self):
        try:
            time = float(self.time_edit.text())
            current = float(self.current_edit.text())
            temp = float(self.temp_edit.text())

            # 每个单位时间对应的像素值
            time_pixel_ratio = 700 / 70
            # 每个单位电流对应的像素值
            current_pixel_ratio = 300 / 30
            # 每个单位温度对应的像素值
            temp_pixel_ratio = 300 / 100

            # 将时间、电流和温度值转换为像素位置
            x = 50 + time * time_pixel_ratio
            y_current = 350 - current * current_pixel_ratio
            y_temp = 350 - temp * temp_pixel_ratio

            self.data.append((time, current, temp))
            self.draw_point(x, y_current, y_temp)

            # 连接同一类别的点
            self.connect_points()

            # 清除输入字段
            self.time_edit.clear()
            self.current_edit.clear()
            self.temp_edit.clear()

        except ValueError:
            print("Invalid input")

    def draw_point(self, x, y_current, y_temp):
        # Draw point for current
        self.plot_scene.addEllipse(x - 2, y_current - 2, 4, 4, QPen(Qt.blue), Qt.blue)

        # Draw point for temperature
        self.plot_scene.addEllipse(x - 2, y_temp - 2, 4, 4, QPen(Qt.red), Qt.red)

    def connect_points(self):
        # Connect current points
        if len(self.data) > 1:
            pen = QPen(Qt.blue)
            pen.setWidth(2)
            for i in range(len(self.data) - 1):
                x1 = 50 + (self.data[i][0] * 700 / 70)
                y1 = 350 - (self.data[i][1] * 300 / 30)
                x2 = 50 + (self.data[i + 1][0] * 700 / 70)
                y2 = 350 - (self.data[i + 1][1] * 300 / 30)
                self.plot_scene.addLine(x1, y1, x2, y2, pen)

        # Connect temperature points
        if len(self.data) > 1:
            pen = QPen(Qt.red)
            pen.setWidth(2)
            for i in range(len(self.data) - 1):
                x1 = 50 + (self.data[i][0] * 700 / 70)
                y1 = 350 - (self.data[i][2] * 300 / 100)
                x2 = 50 + (self.data[i + 1][0] * 700 / 70)
                y2 = 350 - (self.data[i + 1][2] * 300 / 100)
                self.plot_scene.addLine(x1, y1, x2, y2, pen)


class PlotView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)

        # 设置场景的背景刷为透明
        self.setBackgroundBrush(Qt.transparent)
        # 启用视图的透明背景属性
        self.setAttribute(Qt.WA_TranslucentBackground)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec_())
