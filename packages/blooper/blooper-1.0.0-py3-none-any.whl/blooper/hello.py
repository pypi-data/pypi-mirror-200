import math
import random
import numpy as np
def euclidean_distance(point1, point2):
    """
    Calculate the Euclidean distance between two tuples.
    """
    distance = 0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    return math.sqrt(distance)



def get_points(pca_embeddings, target, nearby_points):
    # nearby_points = (1,4.5)
    add_points = []
    index = 0
    for point_x, point_y in pca_embeddings:
        distance = euclidean_distance((point_x,point_y),nearby_points)
        if distance < 1 and target[index] == 1:
            add_points.append([point_x,point_y])
        index+=1


    synthetic = []
    for i in range(10):
        for j in range(len(add_points)):
            random_number = random.uniform(0, 0.2)
            synthetic.append([add_points[j][0]*random_number,add_points[j][1]*random_number])
    merged_arr = np.concatenate((pca_embeddings, synthetic), axis=0)
    merged_target = target + [1]*len(synthetic)
    return merged_target 