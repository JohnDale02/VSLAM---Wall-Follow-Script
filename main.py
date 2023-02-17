from excel_read import read_CCWF
from avg_distance import average_distance
from create_brush_points import create_brush_points
from create_df_robot import create_df_robot
from get_four_wall_points import get_four_wall_points
from create_wall_subsets import create_wall_subsets
from zfinal_plotting import plot_subsets
import timestamps 
import time
import pandas as pd
from pathlib import Path
import numpy as np
import random
from get_sidebrush_center_points import get_sidebrush_center_points



#EXCEL_FILE = 'Claims and Competitive Wall Follow Multiple.xlsx'
EXCEL_FILE = "Claims and Competitive Wall Follow 2-15.xlsx"
NUM_OF_POINTS = 150  # (should be >100 (150 is good) ; number of points for each wall segment (higher --> more accurate)
CIRCLE_POINTS = 500 # # of points for circle for each frame (500 = 1mm accuracy), 50 = good speed  
CORNER_DISTANCE = 200  # mm in either direction from corner for "corner" measurement

STRAIGHT_DIST_FROM_MIDPOINT = 250 # mm in either direction for "straight" measurement 
WALL_NAMES = ['wall-1', 'wall-2', 'wall-3', 'wall-4']   # should be the same for every run (because wall is defined)
#             Start     Outside    Inside     End 


robot_data = read_CCWF(EXCEL_FILE)

# Robot data = list of dictionaries: 
        # Robot --> name   
        # center_name
        # sidebrush_center_name
        # brush_radius
        # Folder Name --> the folder name for all the .tsv files

# Currently --> 4 Wall point names are HardCODED ! [start: Wall-2, outside: Wall-1, inside: Wall-4, end: Wall-3]

Final_Scores = {'Robot_name': [],
        'Average_Straight (mm)': [],
        'Average_Outside (mm)': [],
        'Average_Inside (mm)': [],
        '75th Percentile Straight Distance (mm)':[],
        '75th Percentile Outside Distance (mm)':[],
        '75th Percentile Inside Distance (mm)':[],
        '25th Percentile Straight Distance (mm)':[],
        '25th Percentile Outside Distance (mm)':[],
        '25th Percentile Inside Distance (mm)':[],
        'Median Straight Distance (mm)':[],
        'Median Outside Distance (mm)':[],
        'Median Inside Distance (mm)':[],
        }



for each_robot in robot_data:  # for each robot Model
    name = each_robot['Robot']
    straights = []  # lists to hold the average scores (3 items)
    outsides = [] 
    insides = []
    all_min_straight = []
    all_min_outside = []
    all_min_inside = []

    #if each_robot['Ready?'] != "yes":   # If not ready to be analyzed, continue
    #if each_robot['Robot'] != 'Roborock s7 MaxV':
    #if each_robot['Robot'] != 'Roomba Combo j7':
    #if each_robot['Robot'] != 'Roomba j7':
    #if each_robot['Robot'] != 'Roomba s9':
    #if each_robot['Robot'] != 'Ecovacs Deebot Turbo X1':
    #if each_robot['Robot'] != 'Shark AI Ultra 2-in-1':
    #if each_robot['Robot'] != 'Shark AI Ultra':
    #if each_robot['Robot'] != 'Roomba i3':
    #if each_robot['Robot'] != 'Roborock s7 Plus':
    #if each_robot['Robot'] != 'Roomba i7 w Lapis':
    #if each_robot['Robot'] != 'Samsung JetBot AI+':
    #if each_robot['Robot'] != '600 series':
    #if each_robot['Robot'] != 'Ecovacs N8+':
    #if each_robot['Robot'] != 'Ecovacs N8 Pro':
    if each_robot['Robot'] != 'Shark VACMOP Pro':

        

        timestamps.print_each_robot(name)
        continue

    else:  # Ready to be analyzed, CALCULATE ITS AVERAGES

        distance_straight = []  # creating lists to hold all 3 run averages
        distance_outside = []
        distance_inside = []
        point_names = [ each_robot['center_name'], each_robot['sidebrush_center_name'] ] 
        # Samsung SELECT_LIST = [ [ "OI"], ["OI"], [ "OI"] ]
                                # FILE 1    FILE 2   FILE 3

        SELECT_LIST = [ ["SO" "OI", "IE" ], ["SO", "OI", "IE"], ["SO", "OI", "IE"] ] # For N8plus
        NUM_RUNS = 3
                   
        
        brush_radius = float(each_robot['brush_radius'])
        folderName = each_robot['Folder Name']
        

        for i in range(1, NUM_RUNS+1):  # For Processing Runs 1, 2 and 3
            timestamps.print_file_number(i, name)
            #file_to_read = str("j7-" + str(i) + ".tsv")
            file_to_read =  str(each_robot['Folder Name'] + "/" + each_robot['Folder Name'] + "_wall_follow000" + str(i) + ".tsv")
            
            timestamps.print_create_df_robot(name)
            all_two_pair_position_list = create_df_robot(file_to_read, point_names, name)
            
            timestamps.print_get_four_wall_points(name)
            four_wall_points = get_four_wall_points(file_to_read, WALL_NAMES, name)
            # List of [X,Y] array pairs

            timestamps.print_create_brush_points(name)
        
            brush_points = create_brush_points(all_two_pair_position_list, brush_radius, name, CIRCLE_POINTS)

            sidebrush_center_points = get_sidebrush_center_points(all_two_pair_position_list)
            # List of brush point X, Y coordinates
                # create an array of points representing sidebrush circle for every frame --> based on brush_radius 
                # brush_points = []
                # for each [sidebrush_center_x sidebrush_center_y] --> append list of points representing circle to brush_points (w/ radius brush_radius)


            timestamps.print_create_wall_subsets(name)
            straight, outside, inside = create_wall_subsets(four_wall_points, NUM_OF_POINTS, CORNER_DISTANCE, STRAIGHT_DIST_FROM_MIDPOINT, name, SELECT_LIST, i)
            # list of X,Y coordinates representing the wall   

            timestamps.print_calculating_average_distance_striaght(name)
            straight_run_average, straight_min_points = average_distance(brush_points, straight, sidebrush_center_points, brush_radius)
            all_min_straight.extend(straight_min_points)

            distance_straight.append(straight_run_average)
            straights.append(straight_run_average)

            timestamps.print_calculating_average_distance_outside(name)
            outside_run_average, outside_min_points = average_distance(brush_points, outside, sidebrush_center_points, brush_radius)
            all_min_outside.extend(outside_min_points)

            distance_outside.append(outside_run_average)
            outsides.append(outside_run_average) 

            timestamps.print_calculating_average_distance_inside(name)
            inside_run_average, inside_min_points = average_distance(brush_points, inside, sidebrush_center_points, brush_radius)
            all_min_inside.extend(inside_min_points)

            distance_inside.append(inside_run_average)
            insides.append(inside_run_average)

            plot_subsets(brush_points, straight, outside, inside, four_wall_points, name, i, folderName)


    timestamps.print_calculating_average_of_averages(name)
    average_straight = float(sum(distance_straight)) / NUM_RUNS
    average_outside = float(sum(distance_outside)) / NUM_RUNS
    average_inside = float(sum(distance_inside)) / NUM_RUNS

    straight_percentile_25 = np.percentile(all_min_straight, 25)
    outside_percentile_25 = np.percentile(all_min_outside, 25)
    inside_percentile_25 = np.percentile(all_min_inside, 25)

    straight_percentile_75 = np.percentile(all_min_straight, 75)
    outside_percentile_75 = np.percentile(all_min_outside, 75)
    inside_percentile_75 = np.percentile(all_min_inside, 75)

    straight_median = np.percentile(all_min_straight, 50)
    outside_median = np.percentile(all_min_outside, 50)
    inside_median = np.percentile(all_min_inside, 50)


    Final_Scores['Robot_name'].append(each_robot['Robot'])
    Final_Scores['Average_Straight (mm)'].append(average_straight)
    Final_Scores['Average_Outside (mm)'].append(average_outside)
    Final_Scores['Average_Inside (mm)'].append(average_inside)

    Final_Scores['75th Percentile Straight Distance (mm)'].append(straight_percentile_75)
    Final_Scores['75th Percentile Outside Distance (mm)'].append(outside_percentile_75)
    Final_Scores['75th Percentile Inside Distance (mm)'].append(inside_percentile_75)
    Final_Scores['25th Percentile Straight Distance (mm)'].append(straight_percentile_25)
    Final_Scores['25th Percentile Outside Distance (mm)'].append(outside_percentile_25)
    Final_Scores['25th Percentile Inside Distance (mm)'].append(inside_percentile_25)
    Final_Scores['Median Straight Distance (mm)'].append(straight_median)
    Final_Scores['Median Outside Distance (mm)'].append(outside_median)
    Final_Scores['Median Inside Distance (mm)'].append(inside_median)

    plot_subsets(brush_points, straight, outside, inside, four_wall_points, name, i, folderName)

   # for i_final in range(0, i):
       # print(f"Straight Average Run{i_final}: {straights[i_final]}\n", f"Outside Average Run{i}: {outsides[i_final]} \n", f"Inside Average Run{i}: {insides[i_final]}")
   
timestamps.print_exporting_data()

Final_Export_dataframe = pd.DataFrame(Final_Scores)

int = str(random.randint(0, 100))

try:
    Final_Export_dataframe.to_excel(r"C:\Users\jdale\Wall_Follow_Updated\Wall_Follow1_Scores.xlsx", index=False, float_format="%.2f", header=True)
except:
    Final_Export_dataframe.to_excel(r"C:\Users\jdale\Wall_Follow_Updated\Wall_Follow1_Scores"+ int + ".xlsx")


