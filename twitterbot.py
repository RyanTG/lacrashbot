#!/usr/bin/python

import tweepy, time, csv, os

# STEP 7 of lacrashbot script package (step 6 is at-job-deploy.py).
# Note: You never have to run this script. at-job-deploy.py instructs the computer to run this whenever
#a tweet is ready to go.
#This script uses the Narration CSV, and tweets any narration that has a date/time for the current date/time.
#This script only runs when the AT scheduler tells it to, which is for every date/time.

CONSUMER_KEY = 'xxx'
CONSUMER_SECRET = 'xxx'
ACCESS_KEY = 'xxx'
ACCESS_SECRET = 'xxx'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

now = time.strftime("%b"+" "+"%d")
nowtime = time.strftime("%H"+":"+"%M")

test_file = './LACinjury2014_Narrate.csv'
csv_file = csv.DictReader(open(test_file, 'rb'), delimiter=',', quotechar='"')

with open(test_file, 'r'):
	for line in csv_file:
		if line['COLLISION_DATE'] == (now) and line['COLLISION_TIME'] == nowtime:
			# print line['event']
			api.update_status(line['Decode_NARRATE'])