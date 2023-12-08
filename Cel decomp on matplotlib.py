import matplotlib.pyplot as plt
import numpy as np
import math
import heapq

SIZE_X = 16
SIZE_Y = 16
CANVAS_SIZE = 7
MIN_SQUARE_SIZE = 0.25


class Graph:
    def __init__(self):
        self.edges = {}
        self.points = {}

    def add_vertex(self, point, index):
        index = len(self.points)
        self.points[index] = point

    def add_edge(self, index, jindex):
        if index in self.edges:
            if jindex not in self.edges[index]:
                self.edges[index].append(jindex)
        else:
            self.edges[index] = [jindex]

    def plot_dots(self):
        for point in self.points.values():
            point.plot()

    def plot_edges(self):
        for key, values in self.edges.items():
            if key in self.points:
                for value in values:
                    if value in self.points:
                        plt.plot(
                            [self.points[key].x, self.points[value].x],
                            [self.points[key].y, self.points[value].y],
                            linestyle="--",
                            color="blue",
                            alpha=0.1,
                        )

    def plot_neighbors(self, index):
        for value in self.edges[index]:
            plt.plot(
                [self.points[index].x, self.points[value].x],
                [self.points[index].y, self.points[value].y],
                linestyle="solid",
                color="red",
            )


class Point:
    def __init__(self, x, y, label=None, color="black", delta=None):
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.delta = delta

    def plot(self):
        plt.scatter(self.x, self.y, color=self.color)
        if self.label is not None:
            plt.text(self.x, self.y, self.label, fontsize=12, ha="center")


class Line:
    def __init__(self, start_point, end_point, color="black", marker=None):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.marker = marker

    def plot(self):
        plt.plot(
            [self.start_point.x, self.end_point.x],
            [self.start_point.y, self.end_point.y],
            marker=self.marker,
            color=self.color,
        )


class Triangle:
    def __init__(
        self,
        point1,
        point2,
        point3,
        color_border="black",
        color_fill="black",
        marker=None,
    ):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3
        self.color_border = color_border
        self.color_fill = color_fill
        self.marker = marker

    def plot(self):
        plt.fill(
            [self.point1.x, self.point2.x, self.point3.x, self.point1.x],
            [self.point1.y, self.point2.y, self.point3.y, self.point1.y],
            color=self.color_fill,
        )
        plt.plot(
            [self.point1.x, self.point2.x, self.point3.x, self.point1.x],
            [self.point1.y, self.point2.y, self.point3.y, self.point1.y],
            color=self.color_border,
            marker=self.marker,
        )


class Rectangle:
    def __init__(
        self, point, side_length, color_border="black", color_fill="white", marker=None
    ):
        self.x = point.x
        self.y = point.y
        self.side_length = side_length
        self.color_border = color_border
        self.color_fill = color_fill
        self.marker = marker

    def plot(
        self,
    ):
        plt.fill(
            [self.x, self.x + self.side_length, self.x + self.side_length, self.x],
            [self.y, self.y, self.y + self.side_length, self.y + self.side_length],
            color=self.color_fill,
        )
        plt.plot(
            [
                self.x,
                self.x + self.side_length,
                self.x + self.side_length,
                self.x,
                self.x,
            ],
            [
                self.y,
                self.y,
                self.y + self.side_length,
                self.y + self.side_length,
                self.y,
            ],
            color=self.color_border,
            marker=self.marker,
        )


class Circle:
    def __init__(
        self, point, radius, color_fill="black", color_border="black", marker=None
    ):
        self.x = point.x
        self.y = point.y
        self.radius = radius
        self.color_fill = color_fill
        self.color_border = color_border
        self.marker = marker

    def plot(self):
        circle = plt.Circle(
            (self.x, self.y), self.radius, color=self.color_fill, fill=True
        )
        plt.gca().add_patch(circle)

        circle_border = plt.Circle(
            (self.x, self.y), self.radius, color=self.color_border, fill=False
        )
        plt.gca().add_patch(circle_border)
        if self.marker is not None:
            plt.scatter(*(self.x, self.y), color=self.color_border, marker=self.marker)


def check_collision(shape1, shape2):
    def generate_square_points(x, y, side_length, step):
        points = []
        for i in np.arange(0, side_length, step):
            points.append(Point(x + i, y))
        for i in np.arange(0, side_length, step):
            points.append(Point(x + side_length, y + i))
        for i in np.arange(side_length, 0, -step):
            points.append(Point(x + i, y + side_length))
        for i in np.arange(side_length, 0, -step):
            points.append(Point(x, y + i))
        return points

    def generate_triangle_points(point1, point2, point3, step):
        num_points12 = int(np.abs(point2.x - point1.x) / step) + 1
        num_points23 = int(np.abs(point3.x - point2.x) / step) + 1
        num_points31 = int(np.abs(point1.x - point3.x) / step) + 1

        delta_12x = (point2.x - point1.x) / (num_points12 - 1)
        delta_23x = (point3.x - point2.x) / (num_points23 - 1)
        delta_31x = (point1.x - point3.x) / (num_points31 - 1)

        delta_12y = (point2.y - point1.y) / (num_points12 - 1)
        delta_23y = (point3.y - point2.y) / (num_points23 - 1)
        delta_31y = (point1.y - point3.y) / (num_points31 - 1)

        points = []

        for i in range(num_points12):
            x = point1.x + i * delta_12x
            y = point1.y + i * delta_12y
            points.append(Point(x, y))

        for i in range(num_points23):
            x = point2.x + i * delta_23x
            y = point2.y + i * delta_23y
            points.append(Point(x, y))

        for i in range(num_points31):
            x = point3.x + i * delta_31x
            y = point3.y + i * delta_31y
            points.append(Point(x, y))

        return points

    def is_point_inside_triangle(point, vertex1, vertex2, vertex3):
        def sign(point1, point2, point3):
            return (point1.x - point3.x) * (point2.y - point3.y) - (
                point2.x - point3.x
            ) * (point1.y - point3.y)

        d1 = sign(point, vertex1, vertex2)
        d2 = sign(point, vertex2, vertex3)
        d3 = sign(point, vertex3, vertex1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def check_circle_n_rectangle(point1, radius, point0):
        return (point0.x - point1.x) ** 2 + (point0.y - point1.y) ** 2 <= radius**2

    def check_dot_in_rectangle(point1, side_lenght, point0):
        return (
            point1.x <= point0.x <= point1.x + side_lenght
            or point1.x + side_lenght <= point0.x <= point1.x
        ) and (
            point1.y <= point0.y <= point1.y + side_lenght
            or point1.y + side_lenght <= point0.y <= point1.y
        )

    def get_circle_points(x0, y0, radius, step):
        points = []
        for angle in range(0, 361, step):
            t = math.radians(angle)
            x = x0 + radius * math.cos(t)
            y = y0 + radius * math.sin(t)
            points.append(Point(x, y))
        return points

    supported_shapes = [Triangle, Rectangle, Circle, Line]
    if type(shape1) not in supported_shapes or type(shape2) not in supported_shapes:
        raise ValueError("Unsupported shape type")

    if isinstance(shape1, Rectangle) and isinstance(shape2, Triangle):
        square_points = generate_square_points(
            shape1.x, shape1.y, shape1.side_length, step=MIN_SQUARE_SIZE
        )
        square_points = [
            is_point_inside_triangle(point, shape2.point1, shape2.point2, shape2.point3)
            for point in square_points
        ]
        if all(square_points):
            return 2
        triangle_points = generate_triangle_points(
            shape2.point1, shape2.point2, shape2.point3, step=MIN_SQUARE_SIZE
        )
        triangle_points = [
            check_dot_in_rectangle(Point(shape1.x, shape1.y), shape1.side_length, point)
            for point in triangle_points
        ]
        if any(triangle_points) or any(square_points):
            return 1
        return 0
    elif isinstance(shape1, Rectangle) and isinstance(shape2, Circle):
        points = get_circle_points(shape2.x, shape2.y, shape2.radius, step=4)
        points = [
            check_dot_in_rectangle(Point(shape1.x, shape1.y), shape1.side_length, point)
            for point in points
        ]
        if (
            check_circle_n_rectangle(
                Point(shape2.x, shape2.y), shape2.radius, Point(shape1.x, shape1.y)
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y),
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x, shape1.y + shape1.side_length),
            )
            and check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y + shape1.side_length),
            )
        ):
            return 2
        elif (
            check_circle_n_rectangle(
                Point(shape2.x, shape2.y), shape2.radius, Point(shape1.x, shape1.y)
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y),
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x, shape1.y + shape1.side_length),
            )
            or check_circle_n_rectangle(
                Point(shape2.x, shape2.y),
                shape2.radius,
                Point(shape1.x + shape1.side_length, shape1.y + shape1.side_length),
            )
            or any(points)
        ):
            return 1
        elif (
            shape1.x < shape2.x
            and shape1.y < shape2.y
            and shape1.x + shape1.side_length > shape1.x
            and shape1.y + shape1.side_length > shape2.y
            and shape1.side_length > shape2.radius
        ):
            return 2
        return 0
    else:
        raise ValueError("First needs to be as Rectangle and second is another shape")


def create_grid(all_obstacles, grid):
    flag = True
    while flag:
        flag_out = False
        flag = False
        for square in grid:
            if square.side_length == MIN_SQUARE_SIZE:
                continue
            for obstacle in all_obstacles:
                # print(check_collision(square, obstacle))
                if check_collision(square, obstacle) != 0:
                    grid.append(
                        Rectangle(
                            Point(square.x, square.y),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(square.x + square.side_length / 2, square.y),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(square.x, square.y + square.side_length / 2),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.append(
                        Rectangle(
                            Point(
                                square.x + square.side_length / 2,
                                square.y + square.side_length / 2,
                            ),
                            side_length=square.side_length / 2,
                        )
                    )
                    grid.remove(square)
                    flag_out = True
                    flag = True

                    break
            if flag_out:
                break

    for square in grid:
        if square.side_length == MIN_SQUARE_SIZE:
            for obstacle in all_obstacles:
                if square.color_fill == "red":
                    continue
                collision_result = check_collision(square, obstacle)
                if collision_result == 1:
                    square.color_fill = "pink"
                elif collision_result == 2:
                    square.color_fill = "red"
        else:
            square.color_fill = "white"

    return grid


def check_edges_squares(rect1, rect2):
    if rect1.x + rect1.side_length == rect2.x or rect2.x + rect2.side_length == rect1.x:
        if rect1.y >= rect2.y and rect1.y <= rect2.y + rect2.side_length:
            return True
        if rect2.y >= rect1.y and rect2.y <= rect1.y + rect1.side_length:
            return True

    if rect1.y + rect1.side_length == rect2.y or rect2.y + rect2.side_length == rect1.y:
        if rect1.x >= rect2.x and rect1.x <= rect2.x + rect2.side_length:
            return True
        if rect2.x >= rect1.x and rect2.x <= rect1.x + rect1.side_length:
            return True

    return False


def connect_neighbor_squares(graph, grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if check_edges_squares(grid[i], grid[j]) and (
                grid[i].color_fill == "white" and grid[j].color_fill == "white"
            ):
                graph.add_edge(i, j)


def sorting_key(rectangle):
    color_order = {"white": 0, "pink": 1, "red": 2}
    return color_order[rectangle.color_fill]


def check_dot_in_rectangle(point1, side_lenght, point0):
    return (
        point1.x <= point0.x <= point1.x + side_lenght
        or point1.x + side_lenght <= point0.x <= point1.x
    ) and (
        point1.y <= point0.y <= point1.y + side_lenght
        or point1.y + side_lenght <= point0.y <= point1.y
    )


def plot_path(path, graph):
    for i in range(len(path) - 1):
        key = path[i]
        value = path[i + 1]
        if key in graph.points:
            if value in graph.points:
                plt.plot(
                    [graph.points[key].x, graph.points[value].x],
                    [graph.points[key].y, graph.points[value].y],
                    linestyle="solid",
                    color="red",
                )


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def dijkstra(graph, start_index, end_index):
    distances = {index: float("infinity") for index in graph.points}
    distances[start_index] = 0
    previous_vertices = {index: None for index in graph.points}
    visited = set()

    priority_queue = [(0, start_index)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        for neighbor_index in graph.edges.get(current_vertex, []):
            neighbor_point = graph.points[neighbor_index]
            distance_to_neighbor = distances[current_vertex] + distance(
                graph.points[current_vertex], neighbor_point
            )

            if distance_to_neighbor < distances[neighbor_index]:
                distances[neighbor_index] = distance_to_neighbor
                previous_vertices[neighbor_index] = current_vertex
                heapq.heappush(priority_queue, (distance_to_neighbor, neighbor_index))

    path = []
    current_index = end_index
    while previous_vertices[current_index] is not None:
        path.insert(0, current_index)
        current_index = previous_vertices[current_index]

    path.insert(0, start_index)

    return path


def total_distance(path, graph):
    total_distance = 0
    for i in range(len(path) - 1):
        index = path[i]
        jindex = path[i + 1]
        if index in graph.points and jindex in graph.points:
            point1 = graph.points[index]
            point2 = graph.points[jindex]
            total_distance += distance(point1, point2)

    return total_distance


fig = plt.figure(figsize=(CANVAS_SIZE, CANVAS_SIZE))
plt.xlim(0, SIZE_X)
plt.ylim(0, SIZE_Y)

triangle0 = Triangle(Point(16, 4), Point(8, 16), Point(0, 8))
triangle1 = Triangle(Point(1, 2), Point(4, 5), Point(2, 7))
triangle2 = Triangle(Point(8, 3), Point(6, 9), Point(10, 7))
point_goal_a = Point(0.75, 0.75, "S")
point_goal_b = Point(12, 12, "E")
my_circle = Circle(Point(2, 3), 1.7)
my_circle2 = Circle(Point(10, 2), 1)
# my_circle3 = Circle(Point(6, 11), 2)
# my_circle4 = Circle(Point(12, 8), 3)
# my_circle5 = Circle(Point(6, 6), 0.7)
# my_square1 = Rectangle(Point(3, 3), side_length=3)
# my_square2 = Rectangle(Point(6, 3), side_length=1)
all_obstacles = [triangle1, my_circle, my_circle2, triangle2]

grid = [Rectangle(Point(0, 0), side_length=16)]
grid = create_grid(all_obstacles, grid)
grid = sorted(grid, key=sorting_key)
graph = Graph()

start_flag = True
end_flag = True


for i in range(len(grid)):
    if grid[i].color_fill == "white":
        if start_flag and check_dot_in_rectangle(
            Point(grid[i].x, grid[i].y), grid[i].side_length, point_goal_a
        ):
            graph.add_vertex(
                index=i,
                point=Point(
                    grid[i].x + grid[i].side_length / 2,
                    grid[i].y + grid[i].side_length / 2,
                    color="red",
                    delta=grid[i].side_length / 2,
                ),
            )
            start_flag = False
        elif end_flag and check_dot_in_rectangle(
            Point(grid[i].x, grid[i].y), grid[i].side_length, point_goal_b
        ):
            graph.add_vertex(
                index=i,
                point=Point(
                    grid[i].x + grid[i].side_length / 2,
                    grid[i].y + grid[i].side_length / 2,
                    color="orange",
                    delta=grid[i].side_length / 2,
                ),
            )
            end_flag = False
        else:
            graph.add_vertex(
                index=i,
                point=Point(
                    grid[i].x + grid[i].side_length / 2,
                    grid[i].y + grid[i].side_length / 2,
                    color="green",
                    delta=grid[i].side_length / 2,
                ),
            )


start_index = None
end_index = None

for index, point in graph.points.items():
    if point.color == "red":
        start_index = index
    elif point.color == "orange":
        end_index = index


for i in grid:
    i.plot()

connect_neighbor_squares(graph, grid)
shortest_path = dijkstra(graph, start_index, end_index)
print(shortest_path)
graph.plot_edges()
graph.plot_dots()
plot_path(shortest_path, graph)
total_weight = total_distance(shortest_path, graph)
print(total_weight)
# for i in all_obstacles:
#     i.plot()

point_goal_a.plot()
point_goal_b.plot()
plt.xlabel("X-координата")
plt.ylabel("Y-координата")
plt.show()
