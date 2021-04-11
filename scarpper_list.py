import os
from math import floor
import selenium
from selenium import webdriver
import time
from PIL import Image
import io
import requests
import re
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
# driver = webdriver.Chrome(ChromeDriverManager().install())
#Specify Search URL 
search_url="https://www.spareroom.co.uk/flatshare/?flatshare_type=offered&user_id=424291&search_results=%2Fflatshare%2Fmythreads_beta.pl%3Fthread_id%3D424291_15714142%26listing_restrict%3D%26offset%3D0%26show_deleted_too%3D%26label_id%3D%26keywords%3D%26only_unreplied%3D%26folder%3Dinbox%26sort%3D"
price_limit = 500

website_ = 'https://www.spareroom.co.uk/'
page = requests.get(search_url)
soup = BeautifulSoup(page.content,"html.parser")
det_container = soup.find('ul',class_='listing-results')
num_pages=int(soup.find(class_='searching_options').findAll('strong')[-1].text.strip())
num = floor(num_pages / 10)
offset =0
for li in det_container:
    if li != '\n':
        li.find('article')
        art = li.find('article')
        a = art.find('a')
        # print(a.text)
        link = a['href']
        go = requests.get(website_ + link)
        soup2 = BeautifulSoup(go.content, "html.parser")
        dev_  = soup2.findAll(class_='property-details')[0]
        roomates = dev_.find(text=re.compile('Males'))

        price =dev_.findAll('strong')
        if price is not None:
            for p in price:
                p = p.text.strip()
                p = re.findall(r'\d+',p)[0]
                if int(p) <=price_limit and "Female" not in roomates:
                    print(p +' | ' + roomates.strip() + ' | ' + website_+link)

for i in range(num):
    offset = i + 1 * 10
    search_url="https://www.spareroom.co.uk/flatshare/?offset={}&flatshare_type=offered&user_id=424291&search_results=%2Fflatshare%2Fmythreads_beta.pl%3Fthread_id%3D424291_15714142%26listing_restrict%3D%26offset%3D0%26show_deleted_too%3D%26label_id%3D%26keywords%3D%26only_unreplied%3D%26folder%3Dinbox%26sort%3D".format(offset)
    page = requests.get(search_url)
    soup = BeautifulSoup(page.content,"html.parser")
    det_container = soup.find('ul',class_='listing-results')
    for li in det_container:
        if li != '\n':
            li.find('article')
            art = li.find('article')
            a = art.find('a')
            # print(a.text)
            link = a['href']
            go = requests.get(website_ + link)
            soup2 = BeautifulSoup(go.content, "html.parser")
            dev_  = soup2.findAll(class_='property-details')[0]
            roomates = dev_.find(text=re.compile('Males'))

            price =dev_.findAll('strong')
            if price is not None:
                for p in price:
                    p = p.text.strip()
                    p = re.findall(r'\d+',p)[0]
                    if int(p) <=price_limit and "Female" not in roomates:
                        print(p +' | ' + roomates.strip() + ' | ' + website_+link)