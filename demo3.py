import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, \
    QLineEdit, QPushButton, QLabel, QGraphicsTextItem, QGraphicsLineItem, QHBoxLayout, QGraphicsPixmapItem
from PyQt5.QtGui import QPainter, QPen, QFont, QPixmap, QBrush, QPalette, QFontDatabase, QColor
from PyQt5.QtCore import Qt


class PlotWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_fonts()
        self.bar_font_config = FontConfig(self.fonts["DouyinSansBold"], 16, QColor(255, 255, 255))
        self.title_font_config = FontConfig(self.fonts["DouyinSansBold"], 17, QColor(56, 87, 35))
        self.label_font_config = FontConfig(self.label_font, 21, QColor(56, 87, 35))

        self.setWindowTitle("风力发电机组防雷击电涌保护器热稳定试验电源系统")
        self.setGeometry(100, 100, 1280, 720)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 加载时间、电流、温度标签
        self.set_label()

        # 加载标题栏
        self.set_title()

        # 调用素材
        self.add_pics()

        # 加载图表
        self.set_plot()

    def set_title(self):
        # 加载控件素材并设置属性
        self.title_container = QWidget(self.central_widget)
        self.title_container.setGeometry(140, 50, 1000, 60)

        # 顶部标题栏背景
        self.bar_scene = QGraphicsScene()
        self.bar_view = QGraphicsView(self.title_container)
        self.bar_view.setScene(self.bar_scene)
        self.bar_view.setStyleSheet("border: 0px; background-color: transparent;")  # 移除边框
        # 标题栏文字
        self.bar_left = QGraphicsTextItem("数据呈现")
        self.bar_font_config.apply_font(self.bar_left)
        self.bar_scene.addItem(self.bar_left)
        self.bar_left.setPos(51, 62)
        self.bar_left.setZValue(1)

        self.bar_middle = QGraphicsTextItem("风力发电机组防雷击电涌保护器热稳定试验电源系统")
        self.title_font_config.apply_font(self.bar_middle)
        self.bar_scene.addItem(self.bar_middle)
        self.bar_middle.setPos(203, 62)
        self.bar_middle.setZValue(1)

        self.bar_right = QGraphicsTextItem("图表呈现")
        self.bar_font_config.apply_font(self.bar_right)
        self.bar_scene.addItem(self.bar_right)
        self.bar_right.setPos(893, 62)
        self.bar_right.setZValue(1)

    def load_fonts(self):
        # 加载多个字体文件
        self.fonts = {}
        font_files = ["Font/DouyinSansBold.otf", "Font/庞门正道标题体.ttf"]
        font_names = ["DouyinSansBold", "庞门正道标题体"]

        for font_file, font_name in zip(font_files, font_names):
            font_id = QFontDatabase.addApplicationFont(font_file)
            if font_id != -1:
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.fonts[font_name] = QFont(font_families[0], 20)
            else:
                print(f"Fail to load font from {font_file}")

        # 设定字体
        self.label_font = self.fonts["庞门正道标题体"]

    def add_pics(self):  # 加载素材图片
        # 设定背景图片
        pixmap = QPixmap("Pic/Skyline_Background.png")
        brush = QBrush(pixmap)  # 创建画刷并设置纹理
        palette = self.palette()  # 获取调色板并设置画刷作为背景
        palette.setBrush(QPalette.Background, brush)
        self.setPalette(palette)

        # 设定标题栏图片
        title_bar_above = QPixmap("Pic/Title_Bar_Above.png")
        self.titlebar = QGraphicsPixmapItem(title_bar_above)
        self.titlebar.setPos(30, 50)
        self.bar_scene.addItem(self.titlebar)  # 将图片添加到场景中

        # 设定标签栏背景图
        label_background = QPixmap("Pic/Left_Column_Transparent.png")
        self.label_bg = QGraphicsPixmapItem(label_background)
        self.label_bg.setPos(50, 200)
        self.label_background_scene.addItem(self.label_bg)

    def set_label(self):
        self.label_container = QWidget(self.central_widget)
        self.label_container.setGeometry(140, 200, 340, 500)
        self.label_background_scene = QGraphicsScene()
        self.label_background_view = QGraphicsView(self.label_container)
        self.label_background_view.setScene(self.label_background_scene)
        self.label_background_view.setStyleSheet("border: 0px; background-color: transparent;")  # 移除边框

        # 加载时间、电流、温度标签
        self.time_label = QLabel("时间", self.label_container)
        self.time_label.setGeometry(170, 10, 100, 30)
        self.label_font_config.apply_font(self.time_label)
        self.time_edit = QLineEdit(self.label_container)
        self.time_edit.setGeometry(105, 50, 200, 50)

        self.current_label = QLabel("电流", self.label_container)
        self.current_label.setGeometry(170, 150, 100, 30)
        self.label_font_config.apply_font(self.current_label)
        self.current_edit = QLineEdit(self.label_container)
        self.current_edit.setGeometry(105, 190, 200, 50)

        self.temp_label = QLabel("温度", self.label_container)
        self.temp_label.setGeometry(170, 290, 100, 30)
        self.label_font_config.apply_font(self.temp_label)
        self.temp_edit = QLineEdit(self.label_container)
        self.temp_edit.setGeometry(105, 330, 200, 50)

        self.add_button = QPushButton("添加点", self.label_container)
        self.add_button.setGeometry(105, 160, 100, 30)
        self.add_button.clicked.connect(self.add_point)

        # 添加logo
        # 设定logo图片
        self.logo_pixmap = QPixmap("Pic/logo.png")
        self.logo_label = QLabel(self.label_container)
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setGeometry(0, 400, 340, 100)

    def set_plot(self):
        # Create plot view and scene
        self.plot_container = QWidget(self.central_widget)
        self.plot_container.setGeometry(500, 100, 800, 600)
        self.plot_view = PlotView(self.plot_container)
        self.plot_view.setFixedSize(800, 600)  # 设置图表的固定大小
        self.plot_view.setStyleSheet("background-color: lightblue;")  # 设置图表背景颜色
        self.plot_scene = QGraphicsScene()
        self.plot_view.setScene(self.plot_scene)
        self.plot_view.setStyleSheet("border: 0px; background-color: transparent;")  # 移除边框

        # Data storage
        self.data = []

        # Draw axis and legend
        self.draw_axis()
        self.draw_legend()

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
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)

        # 设置场景的背景刷为透明
        self.setBackgroundBrush(Qt.transparent)
        # 启用视图的透明背景属性
        self.setAttribute(Qt.WA_TranslucentBackground)


class FontConfig:
    def __init__(self, font: QFont, font_size = 12, font_color = QColor(0, 0, 0), border_style = "none"):
        self.font = QFont(font)
        self.font.setPointSize(font_size)
        self.font_color = font_color
        self.border_style = border_style  # 设置边框样式

    def apply_font(self, widget):
        css = f"color: {self.font_color.name()}; border: {self.border_style};"  # 用CSS设置字体样式

        if isinstance(widget, QLabel):
            # 应用字体和颜色到 QLabel
            widget.setFont(self.font)
            widget.setStyleSheet(css)
        elif isinstance(widget, QGraphicsTextItem):
            # 应用字体到 QGraphicsTextItem
            widget.setFont(self.font)
            widget.setDefaultTextColor(self.font_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec_())
