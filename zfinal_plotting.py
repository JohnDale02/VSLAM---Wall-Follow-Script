import matplotlib.pyplot as plt
import os



def plot_brush_points(brush):
    x = []
    y = []
    for point in brush:
        x.append(point[0])
        y.append(point[1])
    
    plt.plot(x,y, 'o', c='blue' , markersize= .5)

def plot_wall_subset(subset, color_string):
    x_norm = []
    y_norm = []
    x_edge = [subset[0][0], subset[-1][0]]
    y_edge = [subset[0][1], subset[-1][1]]
    for point in subset:
        x_norm.append(point[0])
        y_norm.append(point[1])
    
    plt.plot(x_norm,y_norm, 'o', c=color_string, markersize=.5)
    plt.plot(x_edge, y_edge, 'o', c = color_string, markersize = 3)

def plot_four_wall(four_points):
    x = []
    y = []
    for point in four_points:
        x.append(point[0])
        y.append(point[1])
    
    plt.plot(x,y, 'o', c ="orange", markersize= 10)

def plot_min_points(min_list, picture, foldername, file_name):


    x = []
    for i in range(len(min_list)):
        x.append(i)

    plt.figure()
    plt.plot(x, min_list)
    plt.title(f'Min_list {file_name}')
    plt.xlabel('Min_point number')
    plt.ylabel(' Min Distance (mm)')

    photo_main = r"C:\Users\John Dale\Desktop\Programming\Wall_Follow_Updated\Wall_Follow_Updated"
    picture_path = os.path.join(photo_main, foldername, picture)
    plt.savefig(picture_path, dpi = 3800)
    
   # plot.show()

def plot_subsets(brush, straight, outside, inside, four_wall, name, file_name, foldername):

    plt.figure()
    # Brush = [[x,y], [x,y]......]
    # straight, outside, inside  = [[x,y], [x,y]......]
    # Four_wall = [[x,y] [x,y], [x,y], [x,y]]

    plt.rcParams["figure.figsize"] = [7, 7]
    plt.rcParams["figure.autolayout"] = True
  

    plot_brush_points(brush)
    plot_wall_subset(straight, 'red')
    plot_wall_subset(outside, 'purple')
    plot_wall_subset(inside, 'green')
    plot_four_wall(four_wall)
    title = name + f" Run:{file_name} Trajectory"
    
    plt.title(title)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    
    picture = f"plot{file_name}.jpg"
    photo_main = r"C:\Users\John Dale\Desktop\Programming\Wall_Follow_Updated\Wall_Follow_Updated"
    picture_path = os.path.join(photo_main, foldername, picture)

   

    plt.savefig(picture_path, dpi = 3800)

    #picture_for_straight_mins = f" Min Straight Dist plot{file_name}.jpg"
    #picture_for_outside_mins =  f" Min Outside Dist plot{file_name}.jpg"
    #picture_for_inside_mins =  f" Min Inside Dist plot{file_name}.jpg"

    #plot_min_points(all_min_straight, picture_for_straight_mins, foldername, file_name)
    #plot_min_points(all_min_outside, picture_for_outside_mins, foldername, file_name)
    #plot_min_points(all_min_inside, picture_for_inside_mins, foldername, file_name)


    #plt.show(

