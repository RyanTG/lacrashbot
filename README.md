# LA Crashbot

LA Crashbot is a Twitter Bot that posts crashes as they occurred. The idea is to help people better understand the frequency at which people crash. The data used is two years old, so the crashes are "real-time." 

### Basic overview

- Uses publically available data.
- Decodes the values in the data, so that sentences can be constructed.
- Construct narratives of each crash (that are under 140 characters).
- Uses a Raspberry Pi to schedule and execute each tweet.
- All the scripts are python. And you also need spreadsheet software, such as LibreOffice Calc or Excel.

Note that I'm an amateur pythonist. I used this project as a way to learn it. So do not use this project if you want to learn best practices.

If anyone wants to use these scripts as a starter kit for their own bots, feel free (The decoding and narrative scripts can be useful for other goals, as well). As long as you have the data (which is not included here), you can create something similar for your region, or for just pededstrian-involved crashes, or for just crashes that resulted in death, etc.

### Requirements

- Python
- These python modules: tweepy, time, csv, os, pandas, numpy (I think that's all of them)
- A computer that will stay on all the time

### Steps

- **Get some data**. For Los Angeles County I got raw [SWITRS data from the CHP website](http://iswitrs.chp.ca.gov/Reports/jsp/userLogin.jsp).

- Use the [switrs-handling.py script](https://github.com/RyanTG/lacrashbot/blob/master/switrs-handling.py) to **filter those collisions** to suit your desires. In my case, I filtered them to only include injury collisions. This reduced the amount of collisions from 49023 to 25498 (in LA County, 2014).

- In the new csv, **clean up the dates**. Right now, the timestamps look like this: `time = 0000` `date = 0101`. We want them to look like: `time = 00:00` `date = Jan 01`. So first you have to split the month from the day. In [LibreOffice Calc, use Text to Columns](https://help.libreoffice.org/Calc/Text_to_Columns). Then use the [decode-month.py script](https://github.com/RyanTG/lacrashbot/blob/master/decode-month.py) to convert the two numbers t0 spelled out (to three letters) months; then insert that into your working csv. Then merge that field with the day field, to produce "Jan 01". Next, format the time field to be four digits, with a colon in the middle. Use this: `00\:00` as the custom format option.

- **Decode the data**. The values in the data are more machine-readable than human-readable. For example, collision severity is 1, 2, or 3. By decoding those, we convert the numbers into strings, such as "injured," "severely injured," "killed." In [decode.py](https://github.com/RyanTG/lacrashbot/blob/master/decode.py) I'm choosing which fields I'm (probably) going to use, and decoding them in ways that will simplify the narration process. That file also carries over some fields that didn't need decoding. And it doesn't carry over a whole bunch of fields that we don't care about.

- **Create narratives from the decoded data**. [narrate.py](https://github.com/RyanTG/lacrashbot/blob/master/narrate.py) has LOTS of if/else statements in it. I put this together after much trial and error. It will probably give you a headache to look at. And it will probably annoy people who actually know python. But it works. When you create your own narratives you'll discover quirks in the data. This is where you iron out those quirks the best you can. I feel that I didn't do a great job with the bicyclist section. I was hesitant to publish it as is. But ultimately I did so because I concluded that _it's better_ than how the data originally was. Neither were totally accurate; but this is more accurate.

- Use the Date and Time fields to **schedule the tweets**. [at-job-create.py](https://github.com/RyanTG/lacrashbot/blob/master/at-job-create.py) is a script that creates another script, called at-job-deploy.py (not included). Make sure to read the comments in at-job-create.py that tell you the header to add to at-job-deploy.py after it's been created. When at-job-deploy.py is run, it schedules the tweets for the entire span of the data. It does so using the [**at** command](http://www.computerhope.com/unix/uat.htm). When a tweet is scheduled to occur, the **at** command runs the [twitterbot.py script](https://github.com/RyanTG/lacrashbot/blob/master/twitterbot.py), which checks LACinjury2014_Narrate.csv (or whatever your file generated by narrate.py is called) for any narrative that occurs this _very day and minute_. Then twitterbot.py tweets it!

- Make sure to put your **Twitter app credentials** in twitterbot.py ([tutorial on setting that up](https://github.com/RyanTG/lacrashbot/blob/master/twitterbot.py)). I left those fields blank here. In the future, I should move those credentials to a separate file that is imported into twitterbot.py, and is ignored by git.

- **Test beforehand!** Just keep your twitter account private at first; make a csv with like five crashes; set the dates of them for five minutes from now; run at-job-create.py; then at-job-deploy.py; then wait five minutes to see if they post. Note that twitter doesn't always like when your tweets have the exact same content as your other tweets. That's why I included the timestamps in the narratives. Also, do some tests by just running twitterbot.py (because it's easier to see errors when you run it yourself). Make sure you only run it when there's a tweet with a timestamp of this very minute. Also, make sure to test this on the computer where you'll be storing this stuff. In my case, I was ssh'ing into my Raspberry Pi.