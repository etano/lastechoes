Last echoes
===========

Get API info here: https://apps.twitter.com/app/5465048/keys

Install requirements:

    sudo pip install -r requirements.txt

To regenerate the list:

    python scrape.py

To get running:

    python lastechoes.py

For crontab (every day):

    0 17 * * * /usr/bin/python /path/to/lastechoes/scrape.py >> /path/to/lastechoes/scrape.log 2>&1
    0 18 * * * /usr/bin/python /path/to/lastechoes/lastechoes.py >> /path/to/lastechoes/lastechoes.log 2>&1
