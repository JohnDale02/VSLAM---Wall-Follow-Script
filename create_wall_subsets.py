import numpy as np
import math
import timestamps

def build_straight(SO_midpoint, OI_midpoint, IE_midpoint , SO, OI, IE, STRAIGHT_DIST_FROM_MIDPOINT, name, SELECT_LIST, i):
    timestamps.print_building_straight(name)

    straight = []
    if "SO" in SELECT_LIST[i-1]:
        for point in SO: 
            px = point[0]
            py = point[1]
            mid_x = SO_midpoint[0]
            mid_y = SO_midpoint[1]
            dist = math.sqrt((mid_x - px)**2 + (mid_y - py)**2) # Get distance
            if dist < STRAIGHT_DIST_FROM_MIDPOINT:
                straight.append(point)

    if "OI" in SELECT_LIST[i-1]:
        for point in OI: 
            px = point[0]
            py = point[1]
            mid_x = OI_midpoint[0]
            mid_y = OI_midpoint[1]
            dist = math.sqrt((mid_x - px)**2 + (mid_y - py)**2) # Get distance
            if dist < STRAIGHT_DIST_FROM_MIDPOINT:
                straight.append(point)

    if "IE" in SELECT_LIST[i-1]:
        for point in IE: 
            px = point[0]
            py = point[1]
            mid_x = IE_midpoint[0]
            mid_y = IE_midpoint[1]
            dist = math.sqrt((mid_x - px)**2 + (mid_y - py)**2) # Get distance
            if dist < STRAIGHT_DIST_FROM_MIDPOINT:
                straight.append(point)
    
    timestamps.print_return_straight(len(straight), straight[0], straight[-1], name)
    return straight

def build_out_in(cornerx, cornery, wall1_list, wall2_list, CORNER_DISTANCE, name):
    timestamps.print_building_corner(name)
    
    corner_subset = []
    
    for point in wall1_list: 
        px = point[0]
        py = point[1]
        corn_x = cornerx
        corn_y = cornery
        dist = math.sqrt((corn_x - px)**2 + (corn_y - py)**2) # Get distance
        if dist < CORNER_DISTANCE:
            corner_subset.append(point)
    
    for point in wall2_list: 
        px = point[0]
        py = point[1]
        corn_x = cornerx
        corn_y = cornery
        dist = math.sqrt((corn_x - px)**2 + (corn_y - py)**2) # Get distance
        if dist < CORNER_DISTANCE:
            corner_subset.append(point)

    timestamps.print_return_corner(len(corner_subset), corner_subset[0], corner_subset[-1], name)
    return corner_subset

def get_xy(four_wall_points):
    startx = four_wall_points[0][0]
    starty = four_wall_points[0][1]
    outsidex = four_wall_points[1][0]
    outsidey = four_wall_points[1][1]
    insidex = four_wall_points[2][0]
    insidey = four_wall_points[2][1]
    endx = four_wall_points[3][0]
    endy = four_wall_points[3][1]

    return startx, starty, outsidex, outsidey, insidex, insidey, endx, endy
    
def create_wall_subsets(four_wall_points, NUM_OF_POINTS, CORNER_DISTANCE, STRAIGHT_DIST_FROM_MIDPOINT, name, SELECT_LIST, i):
    
    # four_wall_points = [ [startx, starty], [outsidex, outsidey], [insidex, insidey], [endx, endy] ] 
    startx, starty, outsidex, outsidey, insidex, insidey, endx, endy = get_xy(four_wall_points)

    SO_array = np.linspace(start=[startx, starty], stop=[outsidex, outsidey], num=NUM_OF_POINTS, axis=0)
    OI_array = np.linspace(start=[outsidex, outsidey], stop=[insidex, insidey], num=NUM_OF_POINTS, axis=0)
    IE_array = np.linspace(start=[insidex, insidey], stop=[endx, endy], num=NUM_OF_POINTS, axis=0)

    SO = SO_array.tolist()
    OI = OI_array.tolist()
    IE = IE_array.tolist()
    
    SO_midpoint = [ (startx + outsidex)/2 , (starty + outsidey)/2 ] 
    OI_midpoint = [ (outsidex + insidex)/2 , (outsidey + insidey)/2 ] 
    IE_midpoint = [ (insidex + endx)/2 , (insidey + endy)/2 ] 
    
    straight = build_straight(SO_midpoint, OI_midpoint, IE_midpoint , SO, OI, IE, STRAIGHT_DIST_FROM_MIDPOINT, name, SELECT_LIST, i)
    outside = build_out_in(outsidex, outsidey, SO, OI, CORNER_DISTANCE, name)
    inside = build_out_in(insidex, insidey, OI, IE, CORNER_DISTANCE, name)

    timestamps.print_return_subsets(name)
    return straight, outside, inside


#print(create_wall_subsets([[-390.863, -1062.724], [-406.442, 151.312], [807.242, 172.666], [808.99, 1376.814]], 100, 50, 50))
# 3 Walls --> start --> outside ,  outside --> inside ,  inside --> end  [SO, OI, IE]
    # straight is 300 cm from midpoint of each wall   o-------------------M-------------------o
    #                                                 o---------[---------M---------]---------o
    #                                                           o-------[Str]-------o
    #                                                              300         300 

    # ouside is 200 cm from corner 
    # inside is 200 cm from corner 

    # Steps:
        # 1. get Slope of each Wall face (3 slopes)
        # 2. Create Wall arrays for each face [ SO = [], OI = [], IE = []]
        # 3. Straight Subset
            # Combine straights of each faces (distance from midpoint < 300)
            # Will take points from SO, OI, IE 
        # 4. Outside Subset
            # Combine points from SO and OI arrays (distance from outside < 200)
            # Will take points from SO, OI ONLY
        # 5. Inside Subset 
            # Combine points from OI and IE arrays (distance from outside < 200)
            # Will take points from OI, IE ONLY
