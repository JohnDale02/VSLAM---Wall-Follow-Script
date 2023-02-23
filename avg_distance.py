import math

def min_distance_reached(brush_points, each_wall_point, sidebrush_center_points, brush_radius):

    min = 100000000 # setting to a high value, should get less than this!

    wx = each_wall_point[0]
    wy = each_wall_point[1]

    for brush_point in brush_points:  # brush point is an [X,Y] list , same as each_wall_point
        bx = brush_point[0]
        by = brush_point[1]


        dist = math.sqrt((wx - bx)**2 + (wy - by)**2) # Get distance

        if dist < min:  # Get minimum from the robots run to that point
            min = dist

    if min < (brush_radius):
        for sidebrush_center_point in sidebrush_center_points:
        
            sbx = sidebrush_center_point[0]
            sby = sidebrush_center_point[1]

            sb_dist = math.sqrt((wx - sbx)**2 + (wy - sby)**2) # Get distance

            if sb_dist <= brush_radius:
                return 0
    
    return min

def average_distance(brush_points, wall_subset, sidebrush_center_points, brush_radius):
    # brush_points = list of all valid [X,Y] pairs for brush
    # wall_subset is the list of [X,Y] coordinates for 1000 points on the wall
    # want to create a list that holds the minimum distnace between any point in brush_points and ONE given wall_subset point
        # this will give the closest the robot got to a given point on the wall --> we can average this to get average distance sidebrush was from wall. 
    
    min_dist_numbers = []
    count = 0
    for each_wall_point in wall_subset:
        
        min_distance = min_distance_reached(brush_points, each_wall_point, sidebrush_center_points, brush_radius)
        # each_wall_point will be a list [X,Y]
        #print("One Wall point done: ", count)

        min_dist_numbers.append(min_distance)

        count += 1

    subset_average_distance = sum(min_dist_numbers) / len(min_dist_numbers)

    return subset_average_distance, min_dist_numbers
    

