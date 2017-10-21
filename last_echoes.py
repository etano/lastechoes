import os, random, time
import datetime as dt
import pandas as pd
import tweepy

def breakup_status(status, max_size=140):
    statuses = []
    for word in status.split():
        if len(statuses) == 0:
            statuses.append(word)
        elif len(statuses[-1]) + len(word) < max_size:
            statuses[-1] += ' '+word
        else:
            statuses.append(word)
    return statuses

dir = os.path.dirname(os.path.abspath(__file__))

f = open(os.path.join(dir, 'auth.txt'))
lines = [x.rstrip() for x in f.readlines()]
CONSUMER_KEY = lines[0] # To get this stuff, sign in at https://dev.twitter.com/ and Create a New Application
CONSUMER_SECRET = lines[1] # Make sure access level is Read And Write in the Settings tab
ACCESS_KEY = lines[2] # Create a new Access Token
ACCESS_SECRET = lines[3] # Shhhhhhhhh....
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

try:
    df = pd.read_csv(os.path.join(dir, 'last.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    executions_today = df[(df['Date'].dt.day == dt.datetime.today().day) & (df['Date'].dt.month == dt.datetime.today().month)]
    for index, row in executions_today.iterrows():
        status = ('%s - %s %s, %s') % (row['Last Statement'], row['First Name'], row['Last Name'], row['Date'].strftime('%b %d, %Y'))
        statuses = breakup_status(status)
        x = api.update_status(statuses[0])
        for s in statuses[1:]:
            x = api.update_status(s, in_reply_to_status_id=x.id)
except Exception as e:
    print 'ERROR: ', e
