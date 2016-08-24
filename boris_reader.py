'''
Author: Benji Kessler
Date: August 15, 2016

A program to convert BORIS output csv files into csv files more
easily analyzed by R. 

'''
from sys import argv
import csv

#script, data_file = argv

behaviors = {}
behaviors['male'], behaviors['female'] = ({}, {})

possibilities = ['copulate', 'copulate_duration', 'escape', 'grapple', 
'grapple_duration', 'insert', 'insert_right', 'insert_right_duration', 
'insert_left', 'insert_left_duration', 'jump_toward', 'jump_away', 
'jump_neutral', 'jump_attack', 'lost', 'lost_duration', 'move', 
'move_duration', 'orient_away', 'orient_toward', 'sidle', 'sidle_duration',
'sidle_percent', 'vibrate', 'vibrate_duration', 'vibrate_percent', 'walk_away', 
'walk_away_duration', 'walk_neutral', 'walk_neutral_duration','walk_toward', 
'walk_toward_duration', 'wave', 'wave_duration', 'wave_percent']

male_list = ['', 'Male']
female_list = ['', 'Female']

r = 0 #If I need to use row #

with open("borisfiles/time_budget.csv", 'rb') as csvfile:
#with open(data_file, 'rb') as csvfile:

    
    in_file = csv.reader(csvfile)
    
    for row in in_file:
    	
    	if r == 1:
    		obs_name = row[0] #name of the observation
    		male_list[0] = obs_name
    		female_list[0] = obs_name
    	
    	#Reads each row that is a behavior
    	if (row[0] == 'male' or row[0] == 'female') and row[1] != '':
    		#For the individual (male or female) adds an item to the dictionary
    		#	whose key is the name of the behavior and whose value is 
    		#	the number of occurrences of that behavior
    		if len(row[2]) > 1: #Checks is there are modifiers
        		behaviors[row[0]]["_".join([row[1], row[2]])] = row[3]
        		if row[4] != "-": #Adds duration for state variables
        			behaviors[row[0]]["_".join([row[1], row[2], 'duration'])] = row[4]
        	else:
        		behaviors[row[0]][row[1]] = row[3]
        		if row[4] != "-": #Adds duration for state variables
        			behaviors[row[0]]["_".join([row[1], 'duration'])] = row[4]
        		if row[1] in ['wave', 'sidle', 'vibrate']:
        			behaviors[row[0]]["_".join([row[1], 'percent'])] = row[9]
        	
        		
        r += 1 # counts the row #
        
    '''    
    for sex in [['male', male_list], ['female', female_list]]:
    
    	#Creates a list of all possible behaviors
    	for item in behaviors[sex[0]]:
    		if not item in possibilities:
    			possibilities.append(item)
    			
    '''
    
    for sex in [['male', male_list], ['female', female_list]]:
    	#Creates a list of values for each individual
    	for behavior in possibilities:
    		if behavior in behaviors[sex[0]]:
    			sex[1].append(behaviors[sex[0]][behavior])	
    		else:
    			sex[1].append(0)	
    


out_lines = []
out_lines.append(['Observation', 'Sex',] + possibilities)
out_lines.append(male_list)
out_lines.append(female_list)

with open("behaviors.csv", 'wb') as csv_out:
	out_file = csv.writer(csv_out)
	
	for row in out_lines:
		out_file.writerow(row)





