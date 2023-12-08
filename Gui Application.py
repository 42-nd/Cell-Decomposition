import sys
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import rgr
from rgr import *

SCREEN_WIDTH = 900
SCREEN_HEIGH = 600
POINT_SIZE = 8
PEN_SIZE = 2
CANVAS_SIZE = 20
WHITE_COLOR = "#F5F5F5"
DARK_BLUE_COLOR = "#364F6B"
LIGHT_BLUE_COLOR = "#3FC1C9"
RED_COLOR = "#FC5185"
NORM = 32


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        triangle1 = Triangle(Point(1, 2), Point(4, 5), Point(2, 7))
        triangle2 = Triangle(Point(8, 3), Point(6, 9), Point(10, 7))
        self.obstacles = [triangle1, triangle2]
        self.start_point = Point(0.75, 0.75)
        self.end_point = Point(13, 11)
        # self.obstacles = []
        # self.start_point = Point(0, 0)
        # self.end_point = Point(0, 0)
        self.grid = []
        self.graph = Graph()
        self.flag = False
        self.result = []
        self.total_weight = -1
        self.flag_obst = False

        self.setStyleSheet(f"background-color: {DARK_BLUE_COLOR};" "")

        self.start_button = QPushButton(self)
        self.start_button.setGeometry(QRect(20, 550, 141, 41))
        self.start_button.setStyleSheet(
            f"background-color: {RED_COLOR};" "font: 16pt Arial;" "border-radius: 10;"
        )
        self.start_button.setObjectName("start_button")
        self.start_button.setText("Start")
        self.start_button.clicked.connect(self.start)

        self.exit_button = QPushButton(self)
        self.exit_button.setGeometry(QRect(181, 550, 141, 41))
        self.exit_button.setStyleSheet(
            f"background-color: {RED_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.exit_button.setObjectName("exit_button")
        self.exit_button.setText("Exit")
        self.exit_button.clicked.connect(self.stop)

        self.add_end_point = QPushButton(self)
        self.add_end_point.setGeometry(QRect(550, 20, 180, 41))
        self.add_end_point.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.add_end_point.setObjectName("add_end_point")
        self.add_end_point.setText("Add End Point")
        self.add_end_point.clicked.connect(self.get_end_point)

        self.add_start_point = QPushButton(self)
        self.add_start_point.setGeometry(QRect(550, 81, 180, 41))
        self.add_start_point.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.add_start_point.setObjectName("add_start_point")
        self.add_start_point.setText("Add Start Point")
        self.add_start_point.clicked.connect(self.get_start_point)

        self.export_button = QPushButton(self)
        self.export_button.setGeometry(QRect(550, 201, 180, 41))
        self.export_button.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.export_button.setObjectName("export_button")
        self.export_button.setText("Export")
        self.export_button.clicked.connect(self.export_scene)

        self.import_button = QPushButton(self)
        self.import_button.setGeometry(QRect(550, 261, 180, 41))
        self.import_button.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.import_button.setObjectName("import_button")
        self.import_button.setText("Import")
        self.import_button.clicked.connect(self.import_scene)

        self.change_sq_size = QPushButton(self)
        self.change_sq_size.setGeometry(QRect(550, 321, 180, 41))
        self.change_sq_size.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.change_sq_size.setObjectName("change_sq_size")
        self.change_sq_size.setText("Change Sq")
        self.change_sq_size.clicked.connect(self.get_sq_size)

        self.gen_sq_size = QLineEdit(self)
        self.gen_sq_size.setGeometry(QRect(750, 321, 180, 41))
        self.gen_sq_size.setLayoutDirection(Qt.LeftToRight)
        self.gen_sq_size.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 5;"
        )
        self.gen_sq_size.setObjectName("gen_sq_size")
        self.gen_sq_size.setText("Sq size")

        self.add_obstacle_button = QPushButton(self)
        self.add_obstacle_button.setGeometry(QRect(550, 141, 180, 41))
        self.add_obstacle_button.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.add_obstacle_button.setObjectName("add_obstacle_button")
        self.add_obstacle_button.setText("Add obstacle")
        self.add_obstacle_button.clicked.connect(self.add_obstacle)

        self.input_start_coords = QLineEdit(self)
        self.input_start_coords.setGeometry(QRect(750, 20, 180, 41))
        self.input_start_coords.setLayoutDirection(Qt.LeftToRight)
        self.input_start_coords.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 5;"
        )
        self.input_start_coords.setObjectName("input_start_coords")
        self.input_start_coords.setText("Start coords")

        self.input_end_coords = QLineEdit(self)
        self.input_end_coords.setGeometry(QRect(750, 81, 180, 41))
        self.input_end_coords.setLayoutDirection(Qt.LeftToRight)
        self.input_end_coords.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 5;"
        )
        self.input_end_coords.setObjectName("input_end_coords")
        self.input_end_coords.setText("End coords")

        self.input_obsctale_coords = QLineEdit(self)
        self.input_obsctale_coords.setGeometry(QRect(750, 141, 180, 41))
        self.input_obsctale_coords.setLayoutDirection(Qt.LeftToRight)
        self.input_obsctale_coords.setStyleSheet(
            f"background-color: {LIGHT_BLUE_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 5;"
        )
        self.input_obsctale_coords.setText("Obst coords")

        self.result_label = QLabel(self)
        self.result_label.setGeometry(QRect(551, 550, 400, 41))
        self.result_label.setStyleSheet(
            "background-color: #ffffff;\n" "font: 16pt Arial;\n" "border-radius: 10;"
        )
        self.result_label.setText(f"  Result: ")

        self.clear_button = QPushButton(self)
        self.clear_button.setGeometry(QRect(341, 550, 180, 41))
        self.clear_button.setStyleSheet(
            f"background-color: {RED_COLOR};\n"
            "font: 16pt Arial;\n"
            "border-radius: 10;"
        )
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setText("Clear Scene")
        self.clear_button.clicked.connect(self.clear_scene)

    def NameProgramm(self):
        self.setWindowTitle("Cell decomposition")
        self.setWindowIcon(QIcon("cell.png"))

    def get_start_point(self):
        self.start_point.x, self.start_point.y = [
            int(item) for item in self.input_start_coords.text().split(",")
        ]

    def get_end_point(self):
        self.end_point.x, self.end_point.y = [
            int(item) for item in self.input_end_coords.text().split(",")
        ]

    def get_obsctale_coords(self):
        return [int(item) for item in self.input_obsctale_coords.text().split(",")]

    def get_sq_size(self):
        rgr.MIN_SQUARE_SIZE = float(self.gen_sq_size.text())

    def add_obstacle(self):
        coords = self.get_obsctale_coords()
        self.obstacles.append(
            Triangle(
                Point(coords[0], coords[1]),
                Point(coords[2], coords[3]),
                Point(coords[4], coords[5]),
            )
        )

    def import_scene(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            "Выбрать файл",
            ".",
            "Text Files(*.txt);;JPEG Files(*.jpeg);;\
                                                         PNG Files(*.png);;GIF File(*.gif);;All Files(*)",
        )
        with open(f"{filename}", "r") as F:
            lines = F.readlines()
        temp = []
        temp = list(map(float, lines[0].replace("\n", "").split(",")))
        self.start_point.x = temp[0]
        self.start_point.y = temp[1]

        temp = list(map(float, lines[1].replace("\n", "").split(",")))
        self.end_point.x = temp[0]
        self.end_point.y = temp[1]

        for i in range(2, len(lines)):
            temp = list(map(float, lines[i].replace("\n", "").split(",")))

            self.obstacles.append(
                Triangle(
                    Point(temp[0], temp[1]),
                    Point(temp[2], temp[3]),
                    Point(temp[4], temp[5]),
                )
            )

    def export_scene(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self,
            "Выбрать файл",
            ".",
            "Text Files(*.txt);;JPEG Files(*.jpeg);;\
                                                         PNG Files(*.png);;GIF File(*.gif);;All Files(*)",
        )
        with open(f"{filename}", "w") as F:
            F.write(f"{self.start_point.x},{self.start_point.y}\n")
            F.write(f"{self.end_point.x},{self.end_point.y}\n")
            for item in self.obstacles:
                F.write(
                    f"{item.point1.x},{item.point1.y},{item.point2.x},{item.point2.y},{item.point3.x},{item.point3.y}\n"
                )

    def stop(self):
        exit(0)

    def clear_scene(self):
        self.obstacles = []
        self.start_point = Point(0, 0)
        self.end_point = Point(0, 0)
        self.grid = []
        self.graph = Graph()
        self.flag = False
        self.flag_obst = False
        self.shortest_path = []
        self.result_label.setText("  Result: ")
        self.update()

    def start(self):
        self.grid = [Rectangle(Point(0, 0), side_length=16)]
        self.grid = create_grid(self.obstacles, self.grid)
        self.grid = sorted(self.grid, key=sorting_key)

        mark_up_grid_n_graph(self.grid, self.graph, self.start_point, self.end_point)

        start_index = None
        end_index = None

        for index, point in self.graph.points.items():
            if point.color == "red":
                start_index = index
            elif point.color == "orange":
                end_index = index

        connect_neighbor_squares(self.graph, self.grid)
        self.shortest_path = dijkstra(self.graph, start_index, end_index)
        self.total_weight = total_distance(self.shortest_path, self.graph)

        if self.total_weight == -1:
            self.result_label.setText("  Unable to find the path")
        else:
            self.result_label.setText(f"  Result: {str(self.total_weight)}")
        self.flag = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.setBrush(QBrush(Qt.white))
        painter.drawRect(CANVAS_SIZE, CANVAS_SIZE, 512, 512)

        if self.flag:
            painter.setBrush(QBrush(Qt.white))
            painter.drawRect(CANVAS_SIZE, CANVAS_SIZE, 512, 512)
            painter.setPen(QPen(Qt.black, 3))
            for square in self.grid:
                if square.color_fill == "white":
                    painter.setBrush(QBrush(Qt.white))
                elif square.color_fill == "red":
                    painter.setBrush(QBrush(Qt.red))
                else:
                    painter.setBrush(QBrush(Qt.yellow))

                rect = QRect(
                    int(square.x * NORM + CANVAS_SIZE),
                    int(square.y * NORM + CANVAS_SIZE),
                    int(square.side_length * NORM),
                    int(square.side_length * NORM),
                )
                painter.drawRect(rect)

            painter.setBrush(QBrush(Qt.white))
            painter.setPen(QPen(Qt.blue, 2))
            for key, values in self.graph.edges.items():
                if key in self.graph.points:
                    for value in values:
                        if value in self.graph.points:
                            line_start = QPoint(
                                int(self.graph.points[key].x * NORM) + CANVAS_SIZE,
                                int(self.graph.points[key].y * NORM) + CANVAS_SIZE,
                            )
                            line_end = QPoint(
                                int(self.graph.points[value].x * NORM) + CANVAS_SIZE,
                                int(self.graph.points[value].y * NORM) + CANVAS_SIZE,
                            )
                            painter.drawLine(line_start, line_end)

            painter.setBrush(QBrush(Qt.white))
            painter.setPen(QPen(Qt.red, 2))
            for i in range(len(self.shortest_path) - 1):
                key = self.shortest_path[i]
                value = self.shortest_path[i + 1]
                if key in self.graph.points:
                    if value in self.graph.points:
                        line_start = QPoint(
                            int(self.graph.points[key].x * NORM) + CANVAS_SIZE,
                            int(self.graph.points[key].y * NORM) + CANVAS_SIZE,
                        )
                        line_end = QPoint(
                            int(self.graph.points[value].x * NORM) + CANVAS_SIZE,
                            int(self.graph.points[value].y * NORM) + CANVAS_SIZE,
                        )
                        painter.drawLine(line_start, line_end)

            line_start = QPoint(
                int(self.start_point.x * NORM) + CANVAS_SIZE,
                int(self.start_point.y * NORM) + CANVAS_SIZE,
            )
            line_end = QPoint(
                int(self.graph.points[self.shortest_path[0]].x * NORM) + CANVAS_SIZE,
                int(self.graph.points[self.shortest_path[0]].y * NORM) + CANVAS_SIZE,
            )
            painter.drawLine(line_start, line_end)

            line_start = QPoint(
                int(self.end_point.x * NORM) + CANVAS_SIZE,
                int(self.end_point.y * NORM) + CANVAS_SIZE,
            )
            line_end = QPoint(
                int(self.graph.points[self.shortest_path[-1]].x * NORM) + CANVAS_SIZE,
                int(self.graph.points[self.shortest_path[-1]].y * NORM) + CANVAS_SIZE,
            )
            painter.drawLine(line_start, line_end)

            painter.setPen(QPen(Qt.NoPen))
            painter.setBrush(QBrush(Qt.green))
            painter.drawEllipse(
                int(self.start_point.x * NORM) + CANVAS_SIZE,
                int(self.start_point.y * NORM) + CANVAS_SIZE,
                POINT_SIZE,
                POINT_SIZE,
            )
            painter.setBrush(QBrush(Qt.red))
            painter.drawEllipse(
                int(self.end_point.x * NORM) + CANVAS_SIZE,
                int(self.end_point.y * NORM) + CANVAS_SIZE,
                POINT_SIZE,
                POINT_SIZE,
            )
            self.update()
        else:
            if self.end_point.x != 0 and self:
                painter.setPen(QPen(Qt.NoPen))
                painter.setBrush(QBrush(Qt.red))
                painter.drawEllipse(
                    int(self.end_point.x * NORM) + CANVAS_SIZE,
                    int(self.end_point.y * NORM) + CANVAS_SIZE,
                    POINT_SIZE,
                    POINT_SIZE,
                )
                self.update()
            if self.start_point.x != 0:
                painter.setPen(QPen(Qt.NoPen))
                painter.setBrush(QBrush(Qt.green))
                painter.drawEllipse(
                    int(self.start_point.x * NORM) + CANVAS_SIZE,
                    int(self.start_point.y * NORM) + CANVAS_SIZE,
                    POINT_SIZE,
                    POINT_SIZE,
                )
                self.update()
            if len(self.obstacles) != 0:
                for obst in self.obstacles:
                    painter.setPen(QPen(Qt.black))
                    line_start = QPoint(
                        int(obst.point1.x * NORM) + CANVAS_SIZE,
                        int(obst.point1.y * NORM) + CANVAS_SIZE,
                    )
                    line_end = QPoint(
                        int(obst.point2.x * NORM) + CANVAS_SIZE,
                        int(obst.point2.y * NORM) + CANVAS_SIZE,
                    )
                    painter.drawLine(line_start, line_end)

                    line_start = QPoint(
                        int(obst.point2.x * NORM) + CANVAS_SIZE,
                        int(obst.point2.y * NORM) + CANVAS_SIZE,
                    )
                    line_end = QPoint(
                        int(obst.point3.x * NORM) + CANVAS_SIZE,
                        int(obst.point3.y * NORM) + CANVAS_SIZE,
                    )
                    painter.drawLine(line_start, line_end)

                    line_start = QPoint(
                        int(obst.point3.x * NORM) + CANVAS_SIZE,
                        int(obst.point3.y * NORM) + CANVAS_SIZE,
                    )
                    line_end = QPoint(
                        int(obst.point1.x * NORM) + CANVAS_SIZE,
                        int(obst.point1.y * NORM) + CANVAS_SIZE,
                    )
                    painter.drawLine(line_start, line_end)
                    self.update()
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Window()
    ex.resize(970, 600)
    ex.show()
    sys.exit(app.exec_())
