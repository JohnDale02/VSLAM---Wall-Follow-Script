import pandas as pd
import time


EXCEL_FILE = 'Claims and Competitive Wall Follow Try1.xlsx'

def read_CCWF(EXCEL_FILE): # read the Claims and Competitive Wall Follow 

    # Load the xlsx file
    excel_data = pd.read_excel(EXCEL_FILE)
    
    # Read the values of the file into a dataframe
    data = pd.DataFrame(excel_data, columns=[
                        'Robot',
                        'Name of side brush',
                        'Name of center',
                        'Folder Name',
                        'Brush radius',
                        'Ready to be analyzed?'])

    robot_data = []

    for index in range(len(data)):
        individual_robot = {'Robot': data['Robot'][index],
                            'center_name': data['Name of center'][index],
                            'sidebrush_center_name': data['Name of side brush'][index],
                            'Folder Name': data['Folder Name'][index],
                            'Ready?': data['Ready to be analyzed?'][index],
                            'brush_radius': data['Brush radius'][index],
                            }
        robot_data.append(individual_robot)
    

    return robot_data

