#!/usr/bin/python

import csv, os, pprint

# STEP 3 of lacrashbot script package

#Decodes the SWITRS codes, creating a new csv containing date, time, and new columns with Decoded values, plus carry-over columns
#Before you run it, you should have pasted in the new COLLISION_MONTH, and then merged it with the COLLISION_DAY, so the result is like Jan 01
#You should also look at the COLLISION_TIME field, and convert it to this format: 00:00. To do so, format the field in excel/librecalc to this: 00\:00

#TODO: Include headers.

test_file = './LACinjury2014.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')

with open('LACinjury2014_Decode.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput)

    for line in csv_file:
        Decode_COLLISION_SEVERITY = None
        Decode_STWD_VEHTYPE_AT_FAULT = None
        Decode_PCF_VIOL_CATEGORY = None
        Decode_HIT_AND_RUN = None
        Decode_TYPE_OF_COLLISION = None
        Decode_MVIW = None
        Decode_PED_ACTION = None
        Decode_PEDESTRIAN_ACCIDENT = None
        Decode_BICYCLE_ACCIDENT = None

        #Decode severity. All collisions in this dataset resulted in an least one injury.
        if line['COLLISION_SEVERITY'] == '2':
            Decode_COLLISION_SEVERITY = 'severely injured'
        elif line['COLLISION_SEVERITY'] == '3' or line['COLLISION_SEVERITY'] == '4' or line['COLLISION_SEVERITY'] == '':
            Decode_COLLISION_SEVERITY = 'injured'
        elif line['COLLISION_SEVERITY'] == '1':
            Decode_COLLISION_SEVERITY = 'killed'

        #Decode vehicle type.
        if line['STWD_VEHTYPE_AT_FAULT'] == 'A' or line['STWD_VEHTYPE_AT_FAULT'] == 'B' or line['STWD_VEHTYPE_AT_FAULT'] == 'D' or line['STWD_VEHTYPE_AT_FAULT'] == 'E' or line['STWD_VEHTYPE_AT_FAULT'] == 'N' or line['STWD_VEHTYPE_AT_FAULT'] == 'M' or line['STWD_VEHTYPE_AT_FAULT'] == '-':
            Decode_STWD_VEHTYPE_AT_FAULT = 'driving a car'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'F' or line['STWD_VEHTYPE_AT_FAULT'] == 'G':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'driving a truck'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'H' or line['STWD_VEHTYPE_AT_FAULT'] == 'I':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'driving a bus'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'J':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'driving an emergency vehicle'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'K':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'using construction equipment'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'C':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'driving a motorcycle'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'L':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'riding a bicycle'
        elif line['STWD_VEHTYPE_AT_FAULT'] == 'O':
        		Decode_STWD_VEHTYPE_AT_FAULT = 'driving a moped'

        #Decode violation category
        if line['PCF_VIOL_CATEGORY'] == '1':
            Decode_PCF_VIOL_CATEGORY = 'a DUI'
        elif line['PCF_VIOL_CATEGORY'] == '2':
        		Decode_PCF_VIOL_CATEGORY = 'an impeding traffic'
        elif line['PCF_VIOL_CATEGORY'] == '3':
        		Decode_PCF_VIOL_CATEGORY = 'an unsafe speed'
        elif line['PCF_VIOL_CATEGORY'] == '4':
        		Decode_PCF_VIOL_CATEGORY = 'a following too closely'
        elif line['PCF_VIOL_CATEGORY'] == '5':
        		Decode_PCF_VIOL_CATEGORY = 'a wrong side of road'
        elif line['PCF_VIOL_CATEGORY'] == '6':
        		Decode_PCF_VIOL_CATEGORY = 'an improper passing'
        elif line['PCF_VIOL_CATEGORY'] == '7':
        		Decode_PCF_VIOL_CATEGORY = 'an unsafe lane change'
        elif line['PCF_VIOL_CATEGORY'] == '8':
        		Decode_PCF_VIOL_CATEGORY = 'an improper turning'
        elif line['PCF_VIOL_CATEGORY'] == '9':
        		Decode_PCF_VIOL_CATEGORY = 'an auto right of way'
        elif line['PCF_VIOL_CATEGORY'] == '10':
        		Decode_PCF_VIOL_CATEGORY = 'a ped right of way'
        elif line['PCF_VIOL_CATEGORY'] == '11':
        		Decode_PCF_VIOL_CATEGORY = 'a pedestrian'
        elif line['PCF_VIOL_CATEGORY'] == '12':
        		Decode_PCF_VIOL_CATEGORY = 'a traffic signals'
        elif line['PCF_VIOL_CATEGORY'] == '13':
        		Decode_PCF_VIOL_CATEGORY = 'a hazardous parking'
        elif line['PCF_VIOL_CATEGORY'] == '14':
        		Decode_PCF_VIOL_CATEGORY = 'a lights'
        elif line['PCF_VIOL_CATEGORY'] == '15':
        		Decode_PCF_VIOL_CATEGORY = 'a brakes'
        elif line['PCF_VIOL_CATEGORY'] == '16':
        		Decode_PCF_VIOL_CATEGORY = 'an other equipment'
        elif line['PCF_VIOL_CATEGORY'] == '17':
        		Decode_PCF_VIOL_CATEGORY = 'an other hazardous'
        elif line['PCF_VIOL_CATEGORY'] == '18':
        		Decode_PCF_VIOL_CATEGORY = 'an other than driver'
        elif line['PCF_VIOL_CATEGORY'] == '19' or line['PCF_VIOL_CATEGORY'] == '20' or line['PCF_VIOL_CATEGORY'] == '00' or line['PCF_VIOL_CATEGORY'] == '0' or line['PCF_VIOL_CATEGORY'] == '-':
        		Decode_PCF_VIOL_CATEGORY = 'an unknown'
        elif line['PCF_VIOL_CATEGORY'] == '21':
        		Decode_PCF_VIOL_CATEGORY = 'an unsafe speed'
        elif line['PCF_VIOL_CATEGORY'] == '22':
        		Decode_PCF_VIOL_CATEGORY = 'an improper driving'
        elif line['PCF_VIOL_CATEGORY'] == '23':
        		Decode_PCF_VIOL_CATEGORY = 'a PUI'
        elif line['PCF_VIOL_CATEGORY'] == '24':
        		Decode_PCF_VIOL_CATEGORY = 'a fell asleep'

        #Decode hit and run. In the narration, 'yes' will be included.
        if line['HIT_AND_RUN'] == 'F' or line['HIT_AND_RUN'] == 'M':
            Decode_HIT_AND_RUN = 'yes'
        else:
        	Decode_HIT_AND_RUN = 'no'

        #Decode type of collision. Not used. But I decoded it anyway.
        if line['TYPE_OF_COLLISION'] == 'A' or line['TYPE_OF_COLLISION'] == 'G' or line['TYPE_OF_COLLISION'] == 'E' or line['TYPE_OF_COLLISION'] == 'H' or line['TYPE_OF_COLLISION'] == '-':
            Decode_TYPE_OF_COLLISION = 'hit'
        elif line['TYPE_OF_COLLISION'] == 'B':
            Decode_TYPE_OF_COLLISION = 'sideswiped'
        elif line['TYPE_OF_COLLISION'] == 'C':
            Decode_TYPE_OF_COLLISION = 'rear-ended'
        elif line['TYPE_OF_COLLISION'] == 'D':
            Decode_TYPE_OF_COLLISION = 'broadsided'
        elif line['TYPE_OF_COLLISION'] == 'F':
            Decode_TYPE_OF_COLLISION = 'overturned'

        #Decode Motor Vehicle Involved With (aka who did the person at fault hit)
        if line['MVIW'] == 'A':
            Decode_MVIW = 'a non-collision'
        elif line['MVIW'] == 'B':
            Decode_MVIW = 'a pedestrian'
        elif line['MVIW'] == 'C':
            Decode_MVIW = 'a vehicle'
        elif line['MVIW'] == 'D':
            Decode_MVIW = 'a vehicle on another roadway'
        elif line['MVIW'] == 'E':
            Decode_MVIW = 'a parked vehicle'
        elif line['MVIW'] == 'F':
            Decode_MVIW = 'a train'
        elif line['MVIW'] == 'G':
            Decode_MVIW = 'a person on a bike'
        elif line['MVIW'] == 'H':
            Decode_MVIW = 'an animal'
        elif line['MVIW'] == 'I':
            Decode_MVIW = 'a fixed object'
        elif line['MVIW'] == 'J':
            Decode_MVIW = 'an object'
        elif line['MVIW'] == '-':
            Decode_MVIW = 'an unknown object'

        #Decode ped_action. Was a pedestrian hit?
        if line['PED_ACTION'] == 'A' or line['PED_ACTION'] == '-':
            Decode_PED_ACTION = 'no'
        elif line['PED_ACTION'] == 'B' or line['PED_ACTION'] == 'C' or line['PED_ACTION'] == 'D' or line['PED_ACTION'] == 'E' or line['PED_ACTION'] == 'F' or line['PED_ACTION'] == 'G':
            Decode_PED_ACTION = 'yes'

        #These are all the columns that are created or carried over. This is the order of them.
        #In the new file, you'll need to insert these as headers in the first row.
        writer.writerow([
            line['ACCIDENT_YEAR'],
            line['COLLISION_TIME'],
            line['COLLISION_DATE'],
            line['PRIMARY_RD'],
            line['SECONDARY_RD'],
            line['NUMBER_KILLED'],
            line['NUMBER_INJURED'],
            line['COUNT_PED_INJURED'],
            line['COUNT_PED_KILLED'],
            line['COUNT_BICYCLIST_INJURED'],
            line['COUNT_BICYCLIST_KILLED'],
            Decode_COLLISION_SEVERITY,
            Decode_STWD_VEHTYPE_AT_FAULT,
            Decode_PCF_VIOL_CATEGORY,
            Decode_HIT_AND_RUN,
            Decode_TYPE_OF_COLLISION,
            Decode_MVIW,
            Decode_PED_ACTION,
            Decode_PEDESTRIAN_ACCIDENT,
            Decode_BICYCLE_ACCIDENT,
            line['Decode_PED_BIKE']
        ])


