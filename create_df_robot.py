import pandas as pd
import timestamps

# takes in names of center and side_brush_center
    # [ center name, side_brush_center name ]

def find_pointer_columns(marker_name_list: list, names: list, name: str) -> int: # reading headers to find marker columns

    center_name = str(names[0])
    side_brush_center_name = str(names[1])

    
    timestamps.print_find_pointer_columns(center_name, side_brush_center_name, name)

    center_column = None
    sidebrush_center_column = None

    curr_column_index = 0
    for marker_name in marker_name_list:
        split_marker_name = marker_name.split()
        split_marker_name = split_marker_name[:-1]
        split_marker_name = ''.join(split_marker_name)
        
        if split_marker_name == center_name and center_column == None:
            center_column = curr_column_index
        if split_marker_name == side_brush_center_name and sidebrush_center_column == None:
            sidebrush_center_column = curr_column_index
        curr_column_index += 1
    
    if center_column == None or sidebrush_center_column == None:
        print("Names of points do not match to Columns in data...Please lookover point names in Spreadsheet")
        exit()
        
    return center_column, sidebrush_center_column

def get_xy_values(data_columns: list, center_column, sidebrush_center_column, previous, counters) -> list:  # if point == 0, want to take previous value (dont take 0 will skew)
        
        center_x_prev = previous[0][0]
        center_y_prev = previous[0][1]

        sidebrush_center_x_prev = previous[1][0]
        sidebrush_center_y_prev = previous[1][1]

        center_x = float(data_columns[center_column])
        center_y = float(data_columns[center_column+1])

        sidebrush_center_x = float(data_columns[sidebrush_center_column])
        sidebrush_center_y = float(data_columns[sidebrush_center_column+1])

        if center_x == 0.000:
            center_x = center_x_prev
            counters[0] = counters[0]+1
        if center_y == 0.000:
            center_y = center_y_prev
        if sidebrush_center_x == 0.000:
            sidebrush_center_x = sidebrush_center_x_prev
            counters[1] = counters[1]+1
        if sidebrush_center_y == 0.000:
            sidebrush_center_y = sidebrush_center_y_prev
        
        two_pair_position_list = [[center_x, center_y], [sidebrush_center_x, sidebrush_center_y]]
        
        return two_pair_position_list, counters


def create_df_robot(FILENAME: str, point_names: list, name: str) -> list:
    center_0_counter = 0
    sidebrush_center_0_counter = 0
    counters = [center_0_counter, sidebrush_center_0_counter]

    all_two_pair_position_list = []

    tsv_file = open(FILENAME, 'r')
    line = tsv_file.readline()
    while not line.__contains__("Frame"):  # Get past first 11 lines
        line = tsv_file.readline()
        line = line.strip()
    marker_name_list = line.split("\t")

    center_column, sidebrush_center_column = find_pointer_columns(marker_name_list, point_names, name)

    line = tsv_file.readline()  # First Line of numbers
    while line.__contains__("0.000"):
        line = tsv_file.readline()

    previous_xy_values = [[0,0] ,[0,0]]

    while len(line.split("\t")) >= 9:
        data_columns = line.split("\t")
        
        two_pair_position_list, counters = get_xy_values(data_columns, center_column, sidebrush_center_column, previous_xy_values, counters)
        previous_xy_values = two_pair_position_list

        all_two_pair_position_list.append(two_pair_position_list)
        line = tsv_file.readline()

    timestamps.print_0_counters(counters, name)
    timestamps.print_returning_2_point_positions(len(all_two_pair_position_list), name)
    return all_two_pair_position_list


#all_three_pair_position_list = create_df_robot('j7-1.tsv', ['j7-5', 'right', 'head'])
#list = all_three_pair_position_list
#print(list[3210::])

