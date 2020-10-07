import datetime as dt
import logging

import pandas as pd
import tweepy


def breakup_status(status, max_size=140):
    statuses = []
    for word in status.split():
        if len(statuses) == 0:
            statuses.append(word)
        elif len(statuses[-1]) + len(word) < max_size:
            statuses[-1] += " " + word
        else:
            statuses.append(word)
    return statuses


def main():
    consumer_key = sys.argv[1]
    consumer_secret = sys.argv[2]
    access_key = sys.argv[3]
    access_secret = sys.argv[4]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    try:
        df = pd.read_csv("last.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        executions_today = df[
            (df["Date"].dt.day == dt.datetime.today().day) & (df["Date"].dt.month == dt.datetime.today().month)
        ]
        for index, row in executions_today.iterrows():
            status = ("%s - %s %s, %s") % (
                row["Last Statement"],
                row["First Name"],
                row["Last Name"],
                row["Date"].strftime("%b %d, %Y"),
            )
            statuses = breakup_status(status)
            x = api.update_status(statuses[0])
            for s in statuses[1:]:
                x = api.update_status(s, in_reply_to_status_id=x.id)
    except Exception as e:
        log.exception("failed to execute")


if __name__ == "__main__":
    main()
