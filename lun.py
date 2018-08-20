#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import json
import csv
from yattag import Doc
import webbrowser
import os
from datetime import datetime
import re

url = "https://www.lun.ua/%D0%B0%D1%80%D0%B5%D0%BD%D0%B4%D0%B0-%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80-%D0%BA%D0%B8%D0%B5%D0%B2?roomCount=2&priceMin=7000&priceMax=8000"

r = requests.get(url)

soup = bs(r.content, "html.parser")
offers = soup.find_all('article')

offers_data = []
for article in offers:
    offers_data.append(article.find(class_=re.compile("^jss16+")))