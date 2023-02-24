

def get_sidebrush_center_points(all_two_pair_position_list):

    sidebrush_center_points = []

    for point_position in all_two_pair_position_list: # 1 list of 2 known (X,Y) pairs  [[centerx, centery], [sidebrush_centerx, sidebrush_centery]]
        side_brush_x = float(point_position[1][0])
        side_brush_y = float(point_position[1][1])
        sidebrush_center_point = [side_brush_x, side_brush_y]

        sidebrush_center_points.append(sidebrush_center_point)

    return sidebrush_center_points