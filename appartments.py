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


def generate_html(offers):
    #Generate HTML PAGE

    doc, tag, text = Doc().tagtext()
    with tag('table', id="myTable", klass="table"):
        with tag('thead'):
            with tag('tr'):
                with tag('th'):
                    text('Заголовок')	    
                with tag('th'):
                    text('Цена')
                with tag('th'):
                    text('Ссылка')
                with tag('th'):
                    text('Район')
                with tag('th'):
                    text('Время')
                with tag('th'):
                    text('Реклама')
        with tag('tbody'):
            for offer in offers:
                with tag('tr', klass = "offer"):
                    for x in offer.items():
                        if x[0] == 'link':
                            with tag('th', scope='row'):
                                with tag('a', href=x[1], target="_blank"):
                                    text('Ссылка')
                        else:
                            with tag('td'):
                                text(x[1])
                    with tag('td', klass="remove"):
                        text("✖")

    result = doc.getvalue()
    return result

def setup():
    """
    Setting up. Getting page and finding offers
    """

    #Genarate url from filters file and base path
    with open("filters.json") as filters:
        jfilters = json.load(filters)
        filters.close()
        url = """https://www.olx.ua/nedvizhimost/kvartiry-komnaty/arenda-kvartir-komnat/kvartira/kiev/
        ?search%5Bfilter_float_price%3Afrom%5D={0}&search%5Bfilter_float_price%3Ato%5D={1}
        &search%5Bfilter_float_number_of_rooms%3Afrom%5D={2}&search%5Bfilter_float_number_of_rooms%3Ato%5D={3}
        &search%5Bphotos%5D=1""".format(jfilters['price_from'], jfilters['price_to'], jfilters['rooms_from'], jfilters['rooms_to'])

        r = requests.get(url)

        soup = bs(r.content, "html.parser")
        offers = soup.find_all('td', class_="offer")

    #check for existing offers and modify old ones
    with open('appartments.json', 'r') as base:
        jbase = json.load(base)
        base.close()
    today = datetime.today().strftime("%Y-%m-%d")

    if jbase['today'] != today:
        jbase['today'] = today
        for of in jbase['offers']:
            of['time'].replace('Сегодня', today)
    #get ids of today's offers
    links = [x['link'] for x in jbase['offers']]
    districts = set()
    today_count = 0

    #getting relevant data
    csv_list = []
    news = []
    for offer in list(reversed(offers)):
        try:
            if "promoted" in dict(offer.attrs)["class"]:
                promoted = "Yes"
            else:
                promoted = " "
            title = offer.find('a', class_='link').find('strong').get_text()
            price = offer.find('p', class_='price').get_text()
            link = offer.find('a', class_='link', href=True)['href']
            bottom = offer.find('td', class_="bottom-cell")
            time = bottom.find_all('span')[-1].get_text()
            if "Сегодня" in time:
                print(title)
                print("{0} Ссылка: {1}".format(price.strip(), link.strip()))
                bottom_clean = "|".join([s.get_text().strip() for s in bottom.find_all('span')])
                print(bottom_clean + "\n")
                today_count += 1
                districts.add(bottom.find_all('span')[0].get_text().strip())
                d_offer = {'title': title, 'price': price, 'link': link, 'district': bottom_clean.split('|')[0], 'time': bottom_clean.split('|')[1], 'promoted': promoted}
                csv_list.append(d_offer)
                if link not in links:
                    news.append(d_offer)
                    jbase['offers'].append(d_offer)

        except Exception as e:
            print("Error in html: %s" % e)

    return jbase, csv_list, news, districts, today_count

def save_results(jbase, csv_list, json_save=True, csv_save=True, html_save=True):
    #save results

    #save csv
    if csv_save:
        with open('apps.csv', 'w', newline='') as csvfile:
            fieldnames = ['title', 'link', 'price', 'district', 'time', 'promoted']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for app in csv_list:
                writer.writerow(app)
    
    #save json
    if json_save:
        with open('appartments.json', 'w+') as base:
            jstr = json.dumps(jbase, indent=4,)
            base.write(jstr)
            base.close()
    
    #save html
    if html_save:

        web_page = generate_html(csv_list)
        filename = 'appartments.html'
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        hf = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "base.html"), "r")	
        with open(filename, "w") as f:
            f.write(hf.read().replace("{{ block }}", web_page))
            hf.close()
            f.close()



#open a web page
url = 'http://docs.python.org/'
def get_appartments(web=True):
    apps_json, apps_csv, news, districts, today_count = setup()
    save_results(apps_json, apps_csv)

    # open broweser
    if web==True:
        chrome_path = '/usr/bin/google-chrome %s'
        filename = 'appartments.html'
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        webbrowser.get(chrome_path).open(path)
    print("\nНайдено {0} предложений в таких районах: {1}".format(today_count, "; ".join(districts)))

if __name__ == "__main__":
    get_appartments()
    

