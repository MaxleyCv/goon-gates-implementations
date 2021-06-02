import csv
import math
import copy

k = 2

ROWS = []


def k_means_manual(data1: list, data2: list) -> list:
    points = [-1 for _ in range(len(data1))]
    #print(points)
    previous = copy.deepcopy(points)
    centroids = [[0.1, 0], [0.9, 1]]
    for point in range(len(data1)):
        dist1 = math.sqrt((data1[point] - centroids[0][0]) ** 2 + (data2[point] - centroids[0][1])**2)
        dist2 = math.sqrt((data1[point] - centroids[1][0]) ** 2 + (data2[point] - centroids[1][1])**2)
        if dist2 > dist1:
            points[point] = 0
        else:
            points[point] = 1

    while previous != points:
        #print(points)
        previous = copy.deepcopy(points)
        x1, y1, x2, y2 = 0, 0, 0, 0
        n1_c, n2_c = 0, 0
        for stop in range(len(points)):
            if points[stop] == 0:
                x1 += data1[stop]
                y1 += data2[stop]
                n1_c += 1
            else:
                x2 += data1[stop]
                y2 += data2[stop]
                n2_c += 1
        centroids = [[x1 / n1_c, y1 / n1_c], [x2 / n2_c, y2 / n2_c]]
        for point in range(len(data1)):
            dist1 = math.sqrt((data1[point] - centroids[0][0]) ** 2 + (data2[point] - centroids[0][1]) ** 2)
            dist2 = math.sqrt((data1[point] - centroids[1][0]) ** 2 + (data2[point] - centroids[1][1]) ** 2)
            if dist2 >= dist1:
                points[point] = 0
            else:
                points[point] = 1
    return points, centroids


def check(data):
    points, centroids = k_means_manual(data, data)
    if abs(points[1] - points[0]) > 200:
        return True
    else:
        return False
