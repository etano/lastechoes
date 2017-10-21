Last echoes
===========

Get API info here: https://apps.twitter.com/app/5465048/keys

Install requirements:

    sudo pip install -r requirements.txt

To regenerate the list:

    python scrape.py

To get running:

    python last_echoes.py

For crontab (every day):

    0 17 * * * /usr/bin/python /path/to/last_echoes/scrape.py >> /path/to/last_echoes/scrape.log 2>&1
    0 18 * * * /usr/bin/python /path/to/last_echoes/last_echoes.py >> /path/to/last_echoes/last_echoes.log 2>&1
