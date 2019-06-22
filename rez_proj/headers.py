from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

import re
import time
from tqdm import tqdm_notebook as tqdm
# import random
# import winsound
# from random import choice

from selenium import webdriver
# from random import uniform
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
import warnings
warnings.filterwarnings("ignore")

import os, shutil

proxy_list = []
proxies = []

def get_proxy():
    print("Mining proxy servers...")
    first = 'https://hidemyna.me/ru/proxy-list/?country=AFAMATAZBYBEHRCZDKFRGEDEGRIEILITJPKZLVMDNLPLPTRORURSSKSIESSECHTJTRUAGB&maxtime=300&type=h&anon=34#list'
    #second= 'https://hidemyna.me/ru/proxy-list/?type=h&anon=34#list'
    #third = 'https://hidemyna.me/ru/proxy-list/?type=h&anon=34&start=64#list'
    #fourth = 'https://hidemyna.me/ru/proxy-list/?type=h&anon=34&start=128#list'
    page_list = [first]
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") 
    #proxy_list = []
    for page in page_list:
        driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/chromedriver',chrome_options=chrome_options)
        page_url = page
        driver.get(page_url);
        time.sleep(10)
        url = driver.page_source
        driver.quit()
        search_page = BeautifulSoup(url, 'lxml')
        stage_1 = str(search_page.findAll('tr')).split('<td class="tdl">')[1:]   
        protocol,ip,port=0,0,0
        for stage_2 in stage_1:
            stage_2 = stage_2.split('</td><td>')
            ping = int(stage_2[3].split('<p>')[1].split(' мс</p>')[0])
            if ping <=600: 
                protocol = stage_2[4].lower()
                ip = stage_2[0]
                port = stage_2[1]
                lst= [protocol,ip,port, ping]
                proxy_list.append(lst)
    proxy_list.sort(key = lambda row: row[-1])
    print("Proxy servers Mining Completed!")
                
def proxy_pretty():
    for line in proxy_list:
        ip = line[-3]
        port = line[-2]
        proxies.append(ip+':'+port)
        
def proxy_connection(page):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    marker = 1
    flag = 0

    while flag == 0:
        if len(proxies)<=5:
            get_proxy()
            proxy_pretty()
        
        PROXY = proxies[0]
        #print("I'm using proxy = "+str(PROXY))
        chrome_options.add_argument('--proxy-server=http://{}'.format(PROXY))
        chrome = webdriver.Chrome(executable_path='C:/Program Files (x86)/chromedriver'
                                  , chrome_options=chrome_options)
        time.sleep(1)
        chrome.get(page)
        
        try:
            content = chrome.find_element_by_class_name('error-code') 
            if str(content.text) != '':
                del proxies[proxies.index(PROXY)]
                if len(proxies) == 1:
                    get_proxy()
                    proxy_pretty()               
        except:
            page_source = chrome.page_source
            ps = BeautifulSoup(page_source, 'lxml')
            stroka = ps.findAll('title')
            if 'Captcha' in str(stroka) :
                del proxies[proxies.index(PROXY)]
            else:
                if 'Технические работы' not in str(stroka):
                    flag = 1
            pass
        chrome.quit()
    return page_source

def connection(page,marker):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    
    if marker == 0:
        chrome = webdriver.Chrome(executable_path='C:/Program Files (x86)/chromedriver'
                                      , chrome_options=chrome_options
                                     )
        chrome.get(page)
        #time.sleep(1)
        page_source = chrome.page_source
        ps = BeautifulSoup(page_source, 'lxml')
        stroka = ps.findAll('title')
        chrome.quit()
        if 'Captcha' in str(stroka):
            print("Here's Captcha - I'm going to use proxy")
            marker = 1
            page_source = proxy_connection(page)
        else:
            marker = 0
        
    else:
        page_source = proxy_connection(page)
    return page_source, marker



def link_data_parcer(link, marker):
    links = []
    with open('links_to_parce.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            links.append(line.replace('\n',''))
    f.close()

    links = pd.Series(links).drop_duplicates().tolist()
    d = os.listdir()
    del d[d.index('links_to_parce.txt')]

    parced_links = []
    for file in d:
        e = 'https://'+file.replace('_','/').replace('.html','')
        #print(e)
        parced_links.append(e)

    print(len(links))
    for p_link in parced_links:
        del links[links.index(p_link)]
    print(len(links))

    marker = 0
    for link in tqdm(links):
        data, m = headers.connection(link, marker)
        marker = m
        search_page1 = BeautifulSoup(data, 'lxml')
        with open(link.split('//')[1].replace('/','_')+'.html', 'w', encoding='UTF-8') as f:
            f.write(str(search_page1))
        f.close()
        
def get_title(search_page):   
    # ЗАГОЛОВОК
    title = search_page.findAll('h1', attrs={'class':'a10a3f92e9--title--2Widg'})
    #print(title)
    title = str(title).split('>')[1].split('<')[0]
    return title
def get_coordinates(search_page):
    coords = search_page.findAll('a', attrs={'class':'a10a3f92e9--link--379Yt'})
    coords = str(coords).split('center=')[1].split('&')[0]
    lon = re.compile("[0-9.]+").findall(coords)[0]
    lat = re.compile("[0-9.]+").findall(coords)[-1]
    return lon, lat
    
def get_full_address(search_page):
    # АДРЕС!
    address = search_page.findAll('a', attrs={'class':'a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr'})
    address = str(address).split(',')
    city = address[0].split('>')[1].split('<')[0]
    regi = address[1].split('>')[1].split('<')[0]
    if len(address)<3:
        dist = np.nan
    else:
        try:
            dist = address[2].split('>')[1].split('<')[0]
        except:
            dist = address[2]
    if len(address)<4:
        stre = np.nan
    else:
        stre = address[3].split('>')[1].split('<')[0]
    
    if len(address)<5:
        hous = np.nan
    else:
        hous = address[4].split('>')[1].split('<')[0]
    return city,regi,dist,stre,hous  

def get_address(search_page):
    # АДРЕС!
    address = search_page.findAll('a', attrs={'class':'a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr'})
    addr = ''
    for i in range(len(address)):
        if i < len(address) - 1:
            addr+=str(address[i]).split('">')[1].replace('</a>','')+', '
        else:
            addr+=str(address[i]).split('">')[1].replace('</a>','')

    return addr

def get_metro(search_page):    
    # МЕТРО
    # <li class="a10a3f92e9--underground--kONgx">
    name = search_page.findAll('li', attrs={'class':'a10a3f92e9--underground--kONgx'})
    name = str(name).split('target="_blank">')[1:]
    _dict = {}
    for i in name:
        name_ = str(i).split('</span>')[0].split('</a>')[0]
        valu_ = np.nan
        if '<!-- -->⋅<!-- --> <!-- --> ' in i.split('</span>')[0].split('</a>')[1]:
            valu_ = str(i).split('</span>')[0].split('</a>')[1].split('<!-- -->⋅<!-- --> <!-- --> ')[1]
        _dict.update({name_:valu_})
    
    return _dict

def get_description(search_page):
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--info-title--mSyXn'})
    valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--info-text--2uhvD'})
    text = search_page.findAll('p', attrs={'class':'a10a3f92e9--description-text--1_Lup'})
    text = ' '.join(' '.join(str(text).split('>')[1:]).split('<br/')).split('<')[0]
    _dict = {}
    for i in range(len(name)):
        name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = str(valu[i]).split('>')[1].split('<')[0]
        _dict.update({name_:valu_})
    return _dict, text

def get_rules(search_page):
    # <div class="a10a3f92e9--name--3lKTM">Цена</div>
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--name--3lKTM'})
    # <div class="a10a3f92e9--value--2rq_x">57 550 500 ₽</div>
    valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--value--2rq_x'})
    _dict = {}
    for i in range(len(name)):
        name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = ''.join(''.join(''.join(str(valu[i]).split('>')[1:-1]).split('<')[:-1]).split('br/'))
        valu_ = ''.join(valu_.split('\xa0'))
        _dict.update({name_:valu_})
    return _dict

def get_add_info(search_page):
    # <span class="a10a3f92e9--name--3bt8k">Высота потолков</span>
    name = search_page.findAll('span', attrs={'class':'a10a3f92e9--name--3bt8k'})
    # <span class="a10a3f92e9--value--3Ftu5">3,65 м</span>
    valu = search_page.findAll('span', attrs={'class':'a10a3f92e9--value--3Ftu5'})
    _dict = {}
    for i in range(len(name)):
        name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = str(valu[i]).split('>')[1].split('<')[0]
        _dict.update({name_:valu_})
    return _dict

def get_add_info_about_building(search_page):
    # <div class="a10a3f92e9--name--22FM0">Год постройки</div>
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--name--22FM0'})
    # <div class="a10a3f92e9--value--38caj">1960</div>
    valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--value--38caj'})
    _dict = {}
    for i in range(len(name)):
        name_ = ''.join(str(name[i]).split('>')[1:-1]).split('<')[:-1]#.replace(' ','_').replace(',','')
        name_ = ''.join(''.join(name_).split('sup')).replace('/','').replace('!-- --','')
        valu_ = str(valu[i]).split('>')[1].split('<')[0]
        _dict.update({name_:valu_})
    return _dict

def get_add_info_about_district(search_page):
    # <div class="a10a3f92e9--name--2rGyv">Название</div>
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--name--2rGyv'})
    # <div class="a10a3f92e9--value--u7vxM">Южнопортовый</div>
    valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--value--u7vxM'})
    _dict = {}
    for i in range(len(name)):
        #name_ = str(name[i]).split('>')#[1].split('<')[0].replace(' ','_').replace(',','')
        name_ = ''.join(str(name[i]).split('>')[1:-1]).split('<')[:-1]#.replace(' ','_').replace(',','')
        name_ = ''.join(''.join(name_).split('sup')).replace('/','').replace('!-- --','')
        valu_ = str(valu[i]).split('>')[1].split('<')[0]
        _dict.update({name_:valu_})
    return _dict

def get_add_info_about_infrastructure(search_page):
    # <div class="a10a3f92e9--name--2rGyv">Название</div>
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--title--11nUH'})
    # <div class="a10a3f92e9--value--u7vxM">Южнопортовый</div>
    _valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--container--Q-ZlN'})
    _valu = str(_valu).split('a10a3f92e9--item--3ZzPU')[1:]
    valu = []
    for val in _valu:
        valu.append(' '.join(re.compile("[а-яА-Я]+").findall(val)))
    _dict = {}
    for i in range(len(name)):
        name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = valu
        _dict.update({name_:valu_})
    return _dict

def get_add_info_about_technical_details(search_page):
    # <div class="a10a3f92e9--ab_title--3KCHf">Технические характеристики</div>
    name = search_page.findAll('div', attrs={'class':'a10a3f92e9--ab_title--3KCHf'})
    # <li class="a10a3f92e9--item--Ecr_d a10a3f92e9--radiator--1HOZK">Отопление</li>
    # <ul class="a10a3f92e9--container--L-EIV">
    _valu = search_page.findAll('ul', attrs={'class':'a10a3f92e9--container--L-EIV'})
    _valu = str(_valu).split('a10a3f92e9--item--Ecr_d a10a3f92e9')[1:]
    valu = []
    for val in _valu:
        valu.append(' '.join(re.compile("[а-яА-Я]+").findall(val)))
    _dict = {}
    for i in range(len(name)):
        name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = valu
        _dict.update({name_:valu_})
    return _dict

def get_add_info_about_technical_details_comm(search_page):
    # <div class="a10a3f92e9--container--hUyYy"> Технические характеристики</div>
    name_ = 'add_infrastructure'
    
    _valu = search_page.findAll('div', attrs={'class':'a10a3f92e9--container--hUyYy'})
    _valu = str(_valu).split('>')[2:]
    valu = []
    for val in _valu:
        valu.append(' '.join(re.compile("[а-яА-Я]+").findall(val)) )
    _dict = {}
    for i in range(len(_valu)):
        #name_ = str(name[i]).split('>')[1].split('<')[0].replace(' ','_').replace(',','')
        valu_ = []
        for val in valu:
            if val !='':
                valu_.append(val)
        _dict.update({name_:valu_})
    return _dict

def get_html_file(file):
    with open(file, 'r', encoding = 'UTF-8') as f:
        page_source = f.read()
    f.close()
    return page_source

def feature_extractor(url, search_page):
#     path = data[0]
#     file = data[1]
#     page_source = get_html_file(path+'\\'+file)
#     search_page = BeautifulSoup(page_source, 'lxml')
#     url = file.replace('_','/').replace('.html','')
#     # 'http://'+
#     print(url)
    
    
    
    lil = []
    try:
        title = get_title(search_page)
        try:
            lat,lon = get_coordinates(search_page)
        except:
            lat,lon = (np.nan, np.nan)
        address = get_address(search_page)
        city,region,district,street,house = get_full_address(search_page)
        metro = get_metro(search_page)
        description = get_description(search_page)
        rules = get_rules(search_page)
        add_info = get_add_info(search_page)
        add_info_about_building = get_add_info_about_building(search_page)
        add_info_about_district = get_add_info_about_district(search_page)
        add_info_about_infrastructure = get_add_info_about_infrastructure(search_page)
        add_info_about_technical_details = get_add_info_about_technical_details(search_page)
        add_info_about_technical_details_comm = get_add_info_about_technical_details_comm(search_page)
        deal_type =  url.split('ru/')[1].split('/commercial')[0]
        listt = [url,deal_type, lat,lon,title,address,city,region,
                 district,street,house,metro,description,
                 rules,add_info,add_info_about_building,add_info_about_district,
                 add_info_about_infrastructure,add_info_about_technical_details,
                 add_info_about_technical_details_comm]
        lil.append(listt)
    except:
        pass
    columns = ['url','deal_type','lat','lon', 'title', 'address','city','region',
               'district','street','house','metro','description',
               'rules','add_info','building_info','district_info',
               'infrastructure','technical_details','add_infrastructure']
    df = pd.DataFrame(data = lil, columns=columns)
    return df