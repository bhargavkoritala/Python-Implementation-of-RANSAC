"""
RANSAC Algorithm Problem
The goal of this task is to fit a line to the given points using RANSAC algorithm, and output
the names of inlier points and outlier points for the line.
"""
import random
import sys

def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    """
    
    iterations = 0
    samplings = list()

    model_m = 0
    model_c = 0
    model_error = 100000000
    model_inliers = list()
    model_outliers = list()

    while iterations < k:
        sample1, sample2 = random.sample(input_points,2)
        line = sample1['name']+sample2['name']
        if line not in samplings and line[::-1] not in samplings:
            inlier_points_name = list()
            outlier_points_name = list()
            
            samplings.append(line)
            samplings.append(line[::-1])

            #maybe inliners
            x0 = sample1['value'][0]
            y0 = sample1['value'][1]
            x1 = sample2['value'][0]
            y1 = sample2['value'][1]

            #calculate the slope of a line
            m = (y1 - y0) / (x1 - x0 + sys.float_info.epsilon)

            #calculate the intercept of a line
            c = y0-(m*x0)
            line_error = 0
            for item in input_points:
                if item != sample1 and item != sample2:
                    maybe_Outliner = item['value']
                    '''
                    given a line of form aX + bY + c = 0 and a point (m,n)
                    distance between the point and the line is given by |am+bn+c|/squareRoot(a^2+b^2)
                    since we have a line equation of form y = mx + c, we have a = slope  and b = -1 and c= intercept
                    ''' 
                    distance = abs(m*maybe_Outliner[0]+(-1*maybe_Outliner[1])+c)/((m**2+(-1)**2)**(1/2))
                    if distance<t:
                        inlier_points_name.append(item['name'])
                        line_error+=distance**2
                    else:
                        outlier_points_name.append(item['name'])

            if len(inlier_points_name)==0:
                line_error = model_error
            else:    
                line_error/=len(inlier_points_name)
            
            if len(inlier_points_name) >= d:
                if line_error<model_error:
                    model_m = m
                    model_c = c
                    model_error = line_error
                    model_inliers = inlier_points_name.copy()
                    model_outliers = outlier_points_name.copy()
                    model_inliers.append(sample1['name'])
                    model_inliers.append(sample2['name'])
        iterations+=1    
    return model_inliers, model_outliers

    # TODO: implement this function.
    #raise NotImplementedError


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


