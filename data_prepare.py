#script to prepare data for CNN
#analyses labelled images (in labelled images folder)
#converts JSON to required information

"""
will extract:

- classification of image (0 = driveway, 1 = curb, 2 = off street parking bay)
- x pixel coordinate of driveway/curb/offstreet parking bay
- y pixel coordinate of driveway/curb/offstreet parking bay
- theta (angle between line designating object and horizontal)

"""

import os
import json
import pandas as pd
import math
import shutil

#function to get list of files in directory
def list_of_files(mypath):
	from os import listdir
	from os.path import isfile, join
	files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

	return files

#use pythogas's theorem to calculate distance between coorindates
def calculate_distance(x1,y1,x2,y2):  
     dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
     return dist  

#function to calculate midpoint of two points
def calculate_midpoint(x1,y1,x2,y2):
    return ((x1+x2)/2, (y1+y2)/2)

#function to do division that avoids division by zero
def calculate_angle(y_distance, x_distance):

	#if divide by zero angle is vertical so 90 degrees
	try:
		angle = math.degrees(math.atan(y_distance/x_distance))

	except:
		angle = 90

	return angle
	

#function to take json file from path and convert the information inside to a pandas dataframe
def JSON_to_dataframe(path):

	with open(path, 'r') as f:

	    data_dict = json.load(f)
	    objects_list = data_dict['objects']
	    print(len(objects_list))

	    #print(objects_list)

	    #create dataframe
	    df = pd.DataFrame()

	    #get coordinates into dataframe
	    for i in range(len(objects_list)):

	    	#start and finish coordinates of each line
	    	start = objects_list[i]['points']['exterior'][0]
	    	finish = objects_list[i]['points']['exterior'][1]

	    	#get x and y coordiantes
	    	#starts
	    	x_start = start[0] 
	    	y_start = start[1] 

	    	#finish
	    	x_finish = finish[0] 
	    	y_finish = finish[1] 

	    	#distance
	    	distance = calculate_distance(x_start, y_start, x_finish, y_finish)

	    	#midpoint
	    	midpoint_x = calculate_midpoint(x_start, y_start, x_finish, y_finish)[0]
	    	midpoint_y = calculate_midpoint(x_start, y_start, x_finish, y_finish)[1]

	    	#calculate angle
	    	y_distance = y_start - y_finish
	    	x_distance = x_start - x_finish
	    	angle = calculate_angle(y_distance, x_distance)

	    	#add starts and finishes to dataframe
	    	df2 = {'class_title': objects_list[i]['classTitle'], 'x_start': x_start, 'y_start': y_start, 'x_finish': x_finish, 'y_finish': y_finish, 'distance': distance, 'midpoint_x': midpoint_x, 'midpoint_y': midpoint_y, 'angle_to_horizonal': angle}
	    	df = df.append(df2, ignore_index = True)

	    try:
	    	final_df = df[['class_title', 'midpoint_x', 'midpoint_y', 'distance', 'angle_to_horizonal']]
	    	return final_df

	    except:
	    	return None

#function to create directory
#replace directory is if already exists
def create_directory(directory_name):
	name = os.getcwd()+'/'+str(directory_name)
	try:
	    os.makedirs(name)    
	except FileExistsError:
	    shutil.rmtree(name) 
	    os.makedirs(name)  


#create new directory
create_directory('processed_JSON')


x_files = ['1855744', '1855744', '1855747']

for x in x_files:

	#create new directory for x coordinate
	create_directory('processed_JSON/'+str(x))

	#get all requires files in this folder
	files = list_of_files(os.getcwd()+'/labelled_images/'+str(x)+'/ann/')

	for file in files:

		print(file)

		location = file.split('.', 2)[0]
		print(location)

		path = os.getcwd()+'/labelled_images/'+str(x)+'/ann/' + file
		print(path)

		df = JSON_to_dataframe(path)
		print(df)

		if(df is not None):

			df.to_csv(os.getcwd()+'/processed_JSON/'+str(x)+'/'+str(location)+'.csv', header=True, index=None, sep=',', mode='a')






