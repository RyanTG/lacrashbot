#!/usr/bin/python

import csv, os, pprint

# STEP 2 of lacrashbot script package

#this script creates a new csv containing one column with the months spelled out. 
#The column should then be pasted into the working LACinjury2014.csv
#It's important to use this three letter month spelling, because that's what the unix %b uses

#TODO: create a column header. I don't know how to do that.
test_file = './LACinjury2014.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')

with open('month_spell.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput)

    for line in csv_file:
        event = None

        if line['COLLISION_MONTH'] == '01':
            event = 'Jan'
        elif line['COLLISION_MONTH'] == '02':
        	event = 'Feb'
        elif line['COLLISION_MONTH'] == '03':
            event = 'Mar'
        elif line['COLLISION_MONTH'] == '04':
            event = 'Apr'
        elif line['COLLISION_MONTH'] == '05':
            event = 'May'
        elif line['COLLISION_MONTH'] == '06':
            event = 'Jun'
        elif line['COLLISION_MONTH'] == '07':
            event = 'Jul'
        elif line['COLLISION_MONTH'] == '08':
            event = 'Aug'
        elif line['COLLISION_MONTH'] == '09':
            event = 'Sep'
        elif line['COLLISION_MONTH'] == '10':
            event = 'Oct'
        elif line['COLLISION_MONTH'] == '11':
            event = 'Nov'
        elif line['COLLISION_MONTH'] == '12':
            event = 'Dec'

        writer.writerow([
            event
        ])