import csv
import numpy as np
from sympy import Point, Polygon


# read csv and get dict of polygons
def poly_dict_from_csv(path_to_scv):
    reader = csv.reader(open(path_to_scv), delimiter=";")
    # sorted by time
    reader = sorted(reader, key=lambda row: (row[0], row[1]), reverse=True)
    # remove text
    reader = np.array(reader[1:])
    # remove time
    reader = np.delete(reader, [1], axis=1)
    # bring to int
    reader = reader.astype(np.int32)
    # get track ids
    tracks_ids = list(set(reader[:, 0]))
    poly_dict = {}
    for i in tracks_ids:
        vertices_list = []
        # get only rows with current track id in the first place
        vcs = reader[reader[:, 0] == i]
        # collect vertices
        for j in vcs:
            vertices_list.append(Point(int(j[1]), int(j[2])))
        vertices_list = vertices_list
        # make polygon
        poly = Polygon(*vertices_list)
        poly_dict[i] = poly

    return poly_dict


# distance between point and closes point of polygon
def distance_poly_point(poly, point):
    shortestDistance = float(poly.distance(point))
    return shortestDistance


# 'distance' between two polygons
# so called 'distance' in the current task frame
def distance_poly_poly(poly1, poly2):
    m = 0
    n = len(poly1.vertices) + len(poly2.vertices)
    for point in poly1.vertices:
        m += distance_poly_point(poly2, point)**2/n
    for point in poly2.vertices:
        m += distance_poly_point(poly1, point)**2/n
    return int(m)


if __name__ == '__main__':
    poly_dict = poly_dict_from_csv("traks.csv")
    for i in poly_dict.keys():
        for j in poly_dict.keys():
            if j <= i:
                continue
            d = distance_poly_poly(poly_dict[i], poly_dict[j])
            if d < 500:
                print(f'{i} vs {j} == {d}, i.e. good match of tracks {i} and {j} with measure value {d}')
            elif 500 < d and d < 1000:
                print(f'{i} vs {j} == {d}, i.e. slight difference in tracks {i} and {j} with measure value {d}')
            else:
                print(f'{i} vs {j} == {d}, i.e. significant difference in tracks {i} and {j} with measure value {d}')