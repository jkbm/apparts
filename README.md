# apparts
Script for monitoring appartments offers on OLX. Offers use set up filters and are displayed in a generated html-page. Also, there is Scrapy realization that is in development

## Instructions

Launch one-time data fetch by executing 'appartments.py' file. This requests, edits, saves and presents data in a html-page format.
Launch scheduling script that repeats data-recieving process every set period. This updates data without opening browser.

## Requirements
Python 3+
Libraries:
BeutifulSoup4
Scrapy
requests
yattag
