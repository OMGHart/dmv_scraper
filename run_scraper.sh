#!/bin/bash
source /home/hart/.venvs/dmv-scraper/bin/activate

export GOOGLE_APPLICATION_CREDENTIALS="/home/hart/dmv/creds.json"
cd /home/hart/dmv

python scraper.py >>"$HOME/dmv/scrape.log" 2>&1
