#!/usr/bin/python

import csv, os, pprint

# STEP 4 of lacrashbot script package

#Create the Narration CSV from the Decode CSV. Output contains date, time, and tweet contents.
#Note that this file could probably use clean-up. Such as, more variables could be defined up front.
#There are a lot of IFs in here, and some of them are only for one or two crashes - outlier cases that I discovered
#while visually looking at the output.

#TODO: create a test that checks for blank rows; rewrite the bicyclist section; add more comments

test_file = './LACinjury2014_Decode.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')

with open('LACinjury2014_Narrate.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput)

    for line in csv_file:
        Decode_NARRATE = None

        timestamp = ' (' + line['COLLISION_DATE'] + ' ' + line['COLLISION_TIME'] + ' ' + line['ACCIDENT_YEAR'] + ')'

        if line['NUMBER_KILLED'] == '1':
        		number_killed = line['NUMBER_KILLED'] + ' person killed'
        elif line['NUMBER_KILLED'] > '1':
        		number_killed = line['NUMBER_KILLED'] + ' people killed'

        if line['NUMBER_INJURED'] == '1':
        		number_injured = line['NUMBER_INJURED'] + ' person injured'
        elif line['NUMBER_INJURED'] > '1':
        		number_injured = line['NUMBER_INJURED'] + ' people injured'

        if line['Decode_HIT_AND_RUN'] == 'yes':
        		hit_and_run = ' Hit & run.'
        else:
        		hit_and_run = ''

        intro = 'A person ' + line['Decode_STWD_VEHTYPE_AT_FAULT'] + ' on ' + line['PRIMARY_RD']
        intro_type = intro + ' ' + line['Decode_TYPE_OF_COLLISION'] 

        #if a bicyclist hit a pedestrian
        if line['Decode_STWD_VEHTYPE_AT_FAULT'] == 'riding a bicycle' and line['Decode_TYPE_OF_COLLISION'] == 'hit':
            if line['COUNT_PED_INJURED'] == '1' and line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                Decode_NARRATE = intro_type + ' & injured a pedestrian.' + hit_and_run + timestamp
            elif line['COUNT_PED_INJURED'] == '1' and line['Decode_COLLISION_SEVERITY'] == 'severely injured':
                Decode_NARRATE = intro_type + ' & ' + line['Decode_COLLISION_SEVERITY'] + ' a pedestrian.' + hit_and_run + timestamp
            elif line['COUNT_PED_INJURED'] > '1':
                Decode_NARRATE = intro_type + ' & injured ' + line['COUNT_PED_INJURED'] + ' pedestrians.' + hit_and_run + timestamp
            elif line['COUNT_PED_KILLED'] == '1':
                Decode_NARRATE = intro_type + ' & killed a pedestrian.' + hit_and_run + timestamp
            elif line['COUNT_PED_KILLED'] > '1':
                Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_PED_KILLED'] + ' pedestrians.' + hit_and_run + timestamp

        if line['Decode_PED_BIKE'] == 'no' and line['Decode_MVIW'] != 'a non-collision':
            if line['NUMBER_KILLED'] > '0' and line['NUMBER_INJURED'] == '0':
        	    Decode_NARRATE = intro_type + ' ' + line['Decode_MVIW'] + '; ' + number_killed + '.' + hit_and_run + timestamp
            elif line['NUMBER_KILLED'] > '0' and line['NUMBER_INJURED'] > '0':
    			Decode_NARRATE = intro_type + ' ' + line['Decode_MVIW'] + '; ' + number_killed + ' & ' + number_injured + '.' + hit_and_run + timestamp
            elif line['NUMBER_KILLED'] == '0' and line['NUMBER_INJURED'] > '0':
    			Decode_NARRATE = intro_type + ' ' + line['Decode_MVIW'] + '; ' + number_injured + '.' + hit_and_run + timestamp

        elif line['Decode_PED_BIKE'] == 'ped' and line['Decode_MVIW'] != 'a non-collision':
            if line['COUNT_PED_KILLED'] == '1':
                if line['NUMBER_INJURED'] == '0':
            	   Decode_NARRATE = intro_type + ' & killed a pedestrian.' + hit_and_run + timestamp
                elif line['NUMBER_INJURED'] == '1':
                    if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
            	        Decode_NARRATE = intro_type + ' & killed a pedestrian & injured another person.' + hit_and_run + timestamp
                    else:
                        Decode_NARRATE = intro_type + ' & killed a pedestrian & ' + line['Decode_COLLISION_SEVERITY'] + ' another person.' + hit_and_run + timestamp
                elif line['NUMBER_INJURED'] > '1':
            	   Decode_NARRATE = intro_type + ' & killed a pedestrian & injured ' + line['NUMBER_INJURED'] + ' other people.' + hit_and_run + timestamp
            
            elif line['COUNT_PED_KILLED'] > '1':
                if line['NUMBER_INJURED'] == '0':
            	   Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_PED_KILLED'] + ' pedestrians.' + hit_and_run + timestamp
                elif line['NUMBER_INJURED'] == '1':
                    if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                        Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_PED_KILLED'] + ' pedestrians & injured another person.' + hit_and_run + timestamp
                    else:
                        Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_PED_KILLED'] + ' pedestrians & ' + line['Decode_COLLISION_SEVERITY'] + ' another person.' + hit_and_run + timestamp
                elif line['NUMBER_INJURED'] > '1':
            	   Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_PED_KILLED'] + ' pedestrians & injured ' + line['NUMBER_INJURED'] + ' other people.' + hit_and_run + timestamp   
            
            elif line['COUNT_PED_KILLED'] == '0':
                if line['NUMBER_INJURED'] == '1': #Guaranteed the person injured is a ped
                    if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
            	        Decode_NARRATE = intro_type + ' & injured a pedestrian.' + hit_and_run + timestamp
                    else:
                        Decode_NARRATE = intro_type + ' & ' + line['Decode_COLLISION_SEVERITY'] + ' a pedestrian.' + hit_and_run + timestamp
                elif line['NUMBER_INJURED'] > '1': #Not guaranteed the person injured is a ped
                    if line['COUNT_PED_INJURED'] == line['NUMBER_INJURED']:
                	  	Decode_NARRATE = intro_type + ' & injured ' + line['COUNT_PED_INJURED'] + ' pedestrians.' + hit_and_run + timestamp
                    elif line['COUNT_PED_INJURED'] < line['NUMBER_INJURED']:			
        			    Decode_NARRATE = intro_type + ' & injured ' + line['NUMBER_INJURED'] + ' people.' + hit_and_run + timestamp
            
        if line['Decode_PED_BIKE'] == 'bike' and line['Decode_MVIW'] != 'a non-collision':
            if line['Decode_STWD_VEHTYPE_AT_FAULT'] != 'riding a bicycle':
                if line['COUNT_BICYCLIST_KILLED'] == '1':
                    if line['NUMBER_INJURED'] == '0':
                	    Decode_NARRATE = intro_type + ' & killed a person on a bike.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] == '1':
                        if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                	        Decode_NARRATE = intro_type + ' & killed a person on a bike & injured another.' + hit_and_run + timestamp
                        else:
                            Decode_NARRATE = intro_type + ' & killed a person on a bike & ' + line['Decode_COLLISION_SEVERITY'] + ' another.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] > '1':
                	   Decode_NARRATE =  intro_type + ' & killed a person on a bike & injured ' + line['NUMBER_INJURED'] + ' others.' + hit_and_run + timestamp
                
                elif line['COUNT_BICYCLIST_KILLED'] > '1':
                    if line['NUMBER_INJURED'] == '0':
                        Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_BICYCLIST_KILLED'] + ' people on bikes.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] > '1':
                	    Decode_NARRATE = intro_type + ' & killed ' + line['COUNT_BICYCLIST_KILLED'] + ' people on bikes & injured ' + line['NUMBER_INJURED'] + ' others.' + hit_and_run + timestamp
                
                elif line['COUNT_BICYCLIST_KILLED'] == '0':
                    if line['COUNT_BICYCLIST_INJURED'] == '1': 
                        if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                            Decode_NARRATE = intro_type + ' & injured a person on a bike.' + hit_and_run + timestamp
                        else:
                            Decode_NARRATE = intro_type + ' & ' + line['Decode_COLLISION_SEVERITY'] + ' a person on a bike.' + hit_and_run + timestamp                
                    elif line['COUNT_BICYCLIST_INJURED'] == '0' and line['NUMBER_INJURED'] == '1': #necessary because of screw ups in the data
                        Decode_NARRATE = intro_type + ' ' + line['Decode_MVIW'] + '; 1 person injured.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] > '1':
                        if line['COUNT_BICYCLIST_INJURED'] == line['NUMBER_INJURED']:
                    	  	Decode_NARRATE = intro_type + ' & injured ' + line['COUNT_BICYCLIST_INJURED'] + 'people on bikes.' + hit_and_run + timestamp
                        elif line['COUNT_BICYCLIST_INJURED'] < line['NUMBER_INJURED'] and line['COUNT_BICYCLIST_INJURED'] == '1' and line['NUMBER_INJURED'] == '2':          
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + line['Decode_TYPE_OF_COLLISION'] + ' & injured ' + line['COUNT_BICYCLIST_INJURED'] + ' person on a bike & injured another person.' + hit_and_run + timestamp
                        elif line['COUNT_BICYCLIST_INJURED'] < line['NUMBER_INJURED'] and line['COUNT_BICYCLIST_INJURED'] == '1' and line['NUMBER_INJURED'] > '2':          
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + line['Decode_TYPE_OF_COLLISION'] + ' & injured ' + line['COUNT_BICYCLIST_INJURED'] + ' people on bikes & injured others.' + hit_and_run + timestamp
            #Unfortunately necessary to change the 'at fault' to car when the injured party is a bicyclist, due to widespread false attribution of blame on bicyclists. This is MORE accurate than leaving it as is.
            #Hopefully, "collided with" is neutral enough to inform readers that we're not assigning fault to the driver. Fault is unclear. In the future, we may need to coordinate this data with the party data,
            #to determine if the bicyclist is injuring themselves, or another bicyclist, or what. If I didn't make the alterations below, 4% of the crashes would have been like "a bicyclist broadsided a bicyclist."
            elif line['Decode_STWD_VEHTYPE_AT_FAULT'] == 'riding a bicycle':
                if line['COUNT_BICYCLIST_KILLED'] == '1':
                    if line['NUMBER_INJURED'] == '0':
                        Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed a person on a bike.' + hit_and_run + timestamp 
                    elif line['NUMBER_INJURED'] == '1': 
                        if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed a person on a bike & injured another.' + hit_and_run + timestamp
                        else:
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed a person on a bike & ' + line['Decode_COLLISION_SEVERITY'] + ' another.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] > '1':
                        Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed a person on a bike & injured ' + line['NUMBER_INJURED'] + ' others.' + hit_and_run + timestamp
                
                elif line['COUNT_BICYCLIST_KILLED'] > '1':
                    if line['NUMBER_INJURED'] == '0':
                        Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed ' + line['COUNT_BICYCLIST_KILLED'] + ' people on bikes.' + hit_and_run + timestamp
                    elif line['NUMBER_INJURED'] > '1':
                        Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & killed ' + line['COUNT_BICYCLIST_KILLED'] + ' people on bikes & injured ' + line['NUMBER_INJURED'] + ' others.' + hit_and_run + timestamp
                
                elif line['COUNT_BICYCLIST_KILLED'] == '0':
                    if line['NUMBER_INJURED'] == '1':
                        if line['Decode_COLLISION_SEVERITY'] != 'severely injured':
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & injured a person on a bike.' + hit_and_run + timestamp
                        else:
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & ' + line['Decode_TYPE_OF_COLLISION'] + ' a person on a bike.' + hit_and_run + timestamp
                    elif line['COUNT_BICYCLIST_INJURED'] == '0' and line['NUMBER_INJURED'] == '1':
                        Decode_NARRATE = intro_type + '; 1 person injured.'
                    elif line['NUMBER_INJURED'] > '1':
                        if line['COUNT_BICYCLIST_INJURED'] == line['NUMBER_INJURED']:
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & injured ' + line['COUNT_BICYCLIST_INJURED'] + ' people on bikes.' + hit_and_run + timestamp
                        elif line['COUNT_BICYCLIST_INJURED'] < line['NUMBER_INJURED'] and line['COUNT_BICYCLIST_INJURED'] == '1' and line['NUMBER_INJURED'] == '2':          
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & injured ' + line['COUNT_BICYCLIST_INJURED'] + ' person on a bike & injured another person.' + hit_and_run + timestamp
                        elif line['COUNT_BICYCLIST_INJURED'] < line['NUMBER_INJURED'] and line['COUNT_BICYCLIST_INJURED'] == '1' and line['NUMBER_INJURED'] > '2':          
                            Decode_NARRATE = 'A person driving a car on ' + line['PRIMARY_RD'] + ' collided with & injured ' + line['COUNT_BICYCLIST_INJURED'] + ' people on bikes & injured others.' + hit_and_run + timestamp  
                        elif line['COUNT_BICYCLIST_INJURED'] < line['NUMBER_INJURED'] and line['COUNT_BICYCLIST_INJURED'] == '0' and line['NUMBER_INJURED'] > '1':          
                            Decode_NARRATE = intro + ' collided w/ ' + 'another bicyclist. ' + line['NUMBER_INJURED'] + ' other people injured. Strange.' + hit_and_run + timestamp

        if line['Decode_MVIW'] == 'a non-collision':
            if line['NUMBER_KILLED'] > '0' and line['NUMBER_INJURED'] == '0':
                Decode_NARRATE = intro + ' was involved in a non-collision; ' + number_killed + '.' + timestamp 
            elif line['NUMBER_KILLED'] > '0' and line['NUMBER_INJURED'] > '0':
                Decode_NARRATE = intro + ' was involved in a non-collision; ' + number_killed + ' & ' + number_injured + '.' + timestamp 
            elif line['NUMBER_KILLED'] == '0' and line['NUMBER_INJURED'] > '0':
                Decode_NARRATE = intro + ' was involved in a non-collision; ' + number_injured + '.' + timestamp 
            

        writer.writerow([
            line['COLLISION_TIME'],
            line['COLLISION_DATE'],
            Decode_NARRATE
		])