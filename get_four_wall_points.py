import timestamps

def find_wall_columns(marker_name_list: list, wall_names: list, name: str) -> int: # reading headers to find marker columns
    start = str(wall_names[0])
    outside = str(wall_names[1])
    inside = str(wall_names[2])
    end = str(wall_names[3])

    start_column = None
    outside_column = None
    inside_column = None
    end_column = None

    curr_column_index = 0
    for marker_name in marker_name_list:
        split_marker_name = marker_name.split()
        split_marker_name = split_marker_name[:-1]
        split_marker_name = ''.join(split_marker_name)
        
        if split_marker_name == start and start_column == None:
            start_column = curr_column_index
        if split_marker_name == outside and outside_column == None:
            outside_column = curr_column_index
        if split_marker_name == inside and inside_column == None:
            inside_column = curr_column_index
        if split_marker_name == end and end_column == None:
            end_column = curr_column_index

        curr_column_index += 1
    
    if start_column == None or outside_column == None or inside_column == None or end_column == None:
        print("Names of Wall do not match to Columns in data...Please lookover Hardcoded Wall names")
        exit()
        
    timestamps.print_wall_column_numbers_found(start_column, outside_column, inside_column, end_column, name)
    return start_column, outside_column, inside_column, end_column

def get_xy_values(data_columns: list, start_column: int, outside_column: int, inside_column: int, end_column: int) -> list:  # if point == 0, want to take previous value (dont take 0 will skew)
        
        start_x = float(data_columns[start_column])
        start_y = float(data_columns[start_column+1])
        outside_x = float(data_columns[outside_column])
        outside_y = float(data_columns[outside_column+1])
        inside_x = float(data_columns[inside_column])
        inside_y = float(data_columns[inside_column+1])
        end_x = float(data_columns[end_column])
        end_y = float(data_columns[end_column+1])

        four_wall_points = [[start_x, start_y], [outside_x, outside_y], [inside_x, inside_y], [end_x, end_y]]
        
        return four_wall_points

def get_four_wall_points(FILENAME, wall_names, name):
    # Wall_names = strings for start, outside, inside, end (in that order)
    # [ [startx, starty], [outsidex, outsidey], [insidex, insidey], [endx. endy] ]  =  four_wall_points
    four_wall_points = []

    tsv_file = open(FILENAME, 'r')
    line = tsv_file.readline()
    while not line.__contains__("Frame"):  # Get past first 11 lines
        line = tsv_file.readline()
        line = line.strip()
    marker_name_list = line.split("\t")

    start_column, outside_column, inside_column, end_column = find_wall_columns(marker_name_list, wall_names, name)

    line = tsv_file.readline()  # First Line of numbers
    while line.__contains__("0.000"):
        line = tsv_file.readline()

    data_columns = line.split("\t")
    four_wall_points = get_xy_values(data_columns, start_column, outside_column, inside_column, end_column)
    
    timestamps.print_wall_points(four_wall_points, name)
    return four_wall_points

#---------------------------Testing-------------------------------
'''
wall_names = ['Wall-2', 'Wall-1', 'Wall-4', 'Wall-3']

for i in range(1, 4):  # 1 2 3
        file_to_read = str("j7-" + str(i) + ".tsv")
        print(get_four_wall_points(file_to_read, wall_names))

'''