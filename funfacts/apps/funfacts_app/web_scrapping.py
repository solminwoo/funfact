#Import Libraries
from bs4 import BeautifulSoup
import requests
import re
from pprint import pprint

from googleapiclient.discovery import build
my_api_key = "AIzaSyDhS48SlWomdW4LEnpVdRxmBUeduzxpbmY"
my_cse_id = "009395138716893887355:pknqtkcmva6"


#<script async src="https://cse.google.com/cse.js?cx=009395138716893887355:2gorvorgy7j"></script>
#<div class="gcse-search"></div>

def google_search(search_term, api_key, cse_id, **kwargs):
    # fields= kind,items(link)
    service = build("customsearch", "v1", developerKey=api_key)
    #fields = "items(title,link,snippet)",
    res = service.cse().list(q=search_term, cx=cse_id,  **kwargs).execute()
    return res

def lunarCalendar(year_to_search):
    zodiac_sign = year_to_search % 12
    return zodiac_sign

def getZodiac(date_to_search):
    date_details = date_to_search.split(' ')
    month = date_details[0].lower()
    day = int(date_details[1])

    if month == 'december':
        astro_sign = '9' if (day < 22) else '10'
    elif month == 'january':
        astro_sign = '10' if (day < 20) else '11'
    elif month == 'february':
        astro_sign = '11' if (day < 19) else '12'
    elif month == 'march':
        astro_sign = '12' if (day < 21) else '1'
    elif month == 'april':
        astro_sign = '1' if (day < 20) else '2'
    elif month == 'may':
        astro_sign = '2' if (day < 21) else '3'
    elif month == 'june':
        astro_sign = '3' if (day < 21) else '4'
    elif month == 'july':
        astro_sign = '4' if (day < 23) else '5'
    elif month == 'august':
        astro_sign = '5' if (day < 23) else '6'
    elif month == 'september':
        astro_sign = '6' if (day < 23) else '7'
    elif month == 'october':
        astro_sign = '7' if (day < 23) else '8'
    elif month == 'november':
        astro_sign = '8' if (day < 22) else '9'
    
    #return astro_sign
    print("Your Astrological sign is :",astro_sign)
    return astro_sign

def get_src(date_to_search,category =""):
    search_query = f"the famous personality birthday {date_to_search}" 
    print(search_query)
    #fields=kind,items(title,characteristics/length)
    result = google_search(search_query, my_api_key, my_cse_id)
    #print(result)
    link_url = result['items'][0]['link']
    print (result['items'][0])

    # Specify with which URL/web page we are going to bes scraping
    url = requests.get(f"{link_url}").text
    soup = BeautifulSoup(url)

    mytable = soup.find('table',{'class':'infobox'})
    image = mytable.find('img')
    
    #ret_values = {}
    r#et_values['name'] = result['items'][0]['title']
    #ret_values['image'] = image['src']  
    return image['src']

def getHoroscope(year_to_search,date_to_search):
    zodiac_sign = lunarCalendar(year_to_search)
    astro_sign = getZodiac(date_to_search)
    url = requests.get(f"https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign={astro_sign}").text
    soup = BeautifulSoup(url)
    main_div = soup.find('div',{'class':'main-horoscope'})
    p_vals = main_div.find_all('p')
    horo_dict = {
        "1":"Aries", 
        "2":"Taurus",
        "3":"Gemini",
        "4":"Cancer",
        "5":"Leo",
        "6":"Virgo",
        "7":"Libra",
        "8":"Scorpio",
        "9":"Sagittarius",
        "10":"Capricorn",
        "11":"Aquarius",
        "12":"Pisces",
    }
    r_val ={
        "atro" :horo_dict[f'{astro_sign}'],
        "p_vals":p_vals[0].text
    }
    print('%'*80)
    print(p_vals[0].text)
    print('%'*80)
    return r_val
    
def get_historical_data(date_to_search,year_to_search):
    # search_query = f"{date_to_search}" 
    date_details = date_to_search.split(' ')
    month = date_details[0].lower()
    day = int(date_details[1])

    url = requests.get(f"https://en.wikipedia.org/wiki/{month}_{day}").text

    #navbox-title
    soup = BeautifulSoup(url)
    #print (soup.prettify)
    birth_id = soup.find(id="Births")
    birth_list = birth_id.find_next_siblings('ul')
    ul_links = birth_id.find_parent('h2').find_next_sibling('ul')
    year_to_search_cp = year_to_search
    while True:
        li_list = ul_links.find('a',string = year_to_search)
        if li_list == None:
            year = int(year_to_search) - 1
            year_to_search = year
        else:
            break
    #required url
    req_link = li_list.find_next_sibling('a')
    if req_link ==None:
        ret_values['image'] = get_src(date_to_search)
    else:
        try:
            names = req_link.attrs['title'].split(' ')
            name_str = names[0]
            for i in range (1,len(names)):
                name_str += '_' + names[i]
            print (name_str)
            new_url = requests.get(f"https://en.wikipedia.org/wiki/{name_str}").text
            print (new_url)
            new_soup = BeautifulSoup(new_url)
            mytable = new_soup.find('table',{'class':'infobox'})
            print (mytable)
            image = mytable.find('img')
            print (image)
            ret_values ={}
            ret_values['name'] = req_link.attrs['title']
            if image == None:
                ret_values['image'] = get_src(date_to_search)
            else:
                ret_values['image'] = image['src']  
        except:
            ret_values['image'] ="https://www.petmd.com/sites/default/files/petmd-puppy-weight.jpg"
    ##### historical data
    search_query = f"{date_to_search}" 
    print(search_query)
    result = google_search(search_query, my_api_key, my_cse_id)
    print(result)
    ret_result =[]
    ret_result.append(result['items'][0]['snippet'])
    ret_result.append(result['items'][1]['snippet'])
    ret_result.append(result['items'][2]['snippet'])
    ret_values['ret_result'] = ret_result

    return ret_values   

def events_past(date_to_search):
#http://www.thepeoplehistory.com/may25th.html
    date_details = date_to_search.split(' ')
    month = date_details[0].lower()
    day = int(date_details[1])

    url = requests.get(f"http://www.thepeoplehistory.com/{month}{day}th.html").text
    soup = BeautifulSoup(url)
    all_divs = soup.find_all('div',{'class' :"text-nowrap"})
    ret_result = []
    ret_result.append(all_divs[0].get_text())
    ret_result.append(all_divs[1].get_text())
    ret_result.append(all_divs[2].get_text())
    return ret_result