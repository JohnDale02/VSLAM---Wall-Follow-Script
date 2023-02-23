import math
import matplotlib.pyplot as plt

pi = math.pi

def PointsInCircum(initial_x, initial_y, r,n=200):
    adjusted_points = []
   
    list_around_0 = [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
    for x,y in list_around_0:
        x_true = x + initial_x
        y_true = y + initial_y
        adjusted_points.append([x_true, y_true])
        
    return adjusted_points

def plot_brush_points(brush):
    x = []
    y = []
    for point in brush:
        x.append(point[0])
        y.append(point[1])
    
    plt.plot(x,y, 'o', c ="blue", markersize= 1)

plt.rcParams["figure.figsize"] = [10, 10]
plt.rcParams["figure.autolayout"] = True

plot_brush_points(PointsInCircum(1))

plt.show()