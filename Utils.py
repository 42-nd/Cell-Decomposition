import matplotlib.pyplot as plt
import numpy as np
import math
import heapq

SIZE_X = 16
SIZE_Y = 16
CANVAS_SIZE = 7
MIN_SQUARE_SIZE = 0.5


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


class Point:
    def __init__(self, x, y, label=None, color="black", delta=None):
        self.x = x
        self.y = y
        self.label = label
        self.color = color
        self.delta = delta


class Line:
    def __init__(self, start_point, end_point, color="black", marker=None):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.marker = marker


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
        print(num_points31,num_points23,num_points12)
        if num_points12 <= 1:
            num_points12 += 1
        if num_points23 <= 1:
            num_points23 += 1
        if num_points31 <= 1:
            num_points31 +=1
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

    supported_shapes = [Triangle, Rectangle, Line]
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


def mark_up_grid_n_graph(grid, graph, point_start, point_end):
    start_flag = True
    end_flag = True

    for i in range(len(grid)):
        if grid[i].color_fill == "white":
            if start_flag and check_dot_in_rectangle(
                Point(grid[i].x, grid[i].y), grid[i].side_length, point_start
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
                Point(grid[i].x, grid[i].y), grid[i].side_length, point_end
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


def is_point_inside_triangle(point, vertex1, vertex2, vertex3):
    def sign(point1, point2, point3):
        return (point1.x - point3.x) * (point2.y - point3.y) - (point2.x - point3.x) * (
            point1.y - point3.y
        )

    d1 = sign(point, vertex1, vertex2)
    d2 = sign(point, vertex2, vertex3)
    d3 = sign(point, vertex3, vertex1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)
