#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
import sys, io
import datetime

# I _think_ we might be able to get this, which would be nice? But it appears to
# maybe only apply to past events. Not sure what the deal is with that.
# """
# <script type="application/ld+json">{"@context":"http:\/\/schema.org","@type":"MusicEvent","name":"Shakopee Bowl","startDate":"2022-02-11T20:30:00","url":"https:\/\/thelookband.com\/event\/4437850\/588146120\/shakopee-bowl","location":{"@type":"Place","name":"Shakopee Bowl","address":"3020 133rd St W, Shakopee, MN 55379"}}</script>
# """

session = requests.Session()
session.headers = { # Gotta spoof 'em; the default ones get us 403'd
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:102.0) Gecko/20100101 Firefox/102.0",
}

res = session.get("https://thelookband.com/shows")
pat = re.compile('href="/go/events/(\d*)')
ids = set(re.findall(pat, res.text))

# https://stackoverflow.com/a/49709310
# https://www.rfc-editor.org/rfc/rfc5545#section-3.1
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, newline='\r\n')

print("BEGIN:VCALENDAR")
print("VERSION:2.0")
print("X-WR-CALNAME:The Look")

for id in ids:
    print("BEGIN:VEVENT")
    res = session.get(f'https://thelookband.com/go/events/{id}')
    soup = BeautifulSoup(res.text, 'html.parser')
    datestring = soup.find(class_='date').string
    if datestring.count(',') < 2: # Sometimes they don't put the year in
        datestring += ", " + str(datetime.datetime.now().year)
    datestring += " " + soup.find(class_='time').string
    start_time = datetime.datetime.strptime(datestring, "%A, %B %d, %Y %I:%M%p")

    summary = soup.find(class_='event-title').a.string
    # Escape chars: https://www.rfc-editor.org/rfc/rfc5545#section-3.3.11
    summary = re.sub(r"([\;,])", r"\\\1", summary)
    summary = re.sub("\n", r"\\n", summary)

    location = soup.find(class_='event-location').a.string
    location = re.sub(r"([\;,])", r"\\\1", location)
    location = re.sub("\n", r"\\n", location)

    print("SUMMARY:The Look at " + summary)
    print("DTSTART:" + start_time.strftime("%Y%m%dT%H%M%S"))
    print("DTEND:" + (start_time + datetime.timedelta(hours=3)).strftime("%Y%m%dT%H%M%S"))
    print("LOCATION:" + location)
    print("END:VEVENT")

print("END:VCALENDAR")
