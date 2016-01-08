#!/usr/bin/python

import csv, os, pprint

# STEP 5 of lacrashbot script package

#This file creates a python script (called at-job-deploy.py) containing an AT scheduled event for each crash.

#Once at-job-deploy.py is created, you need to edit it and paste this into the top of it:

#!/usr/bin/python

#import subprocess

#after pasting, remove the # from "#import subprocess" but don't remove it from "#!/usr/bin/python"

test_file = './LACinjury2014_Narrate.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',')

with open('at-job-deploy.py', 'w') as csvoutput:
  for line in csv_file:

      event = "print subprocess.Popen('echo python twitterbot.py | at " + line['COLLISION_TIME'] + " " + line['COLLISION_DATE'] + "', shell=True, stdout=subprocess.PIPE).stdout.read() \n"
      csvoutput.write(event)
