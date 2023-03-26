import csv
from bs4 import BeautifulSoup
import requests
import html5lib
import re 

url = 'https://bonbanh.com/xe-mitsubishi-pajero-3.0-2008-4662377?fbclid=iwar1zkwbqftwcjfp_xyzipjsy5mkkrmpkwtedvqhsx43x8-q89pu4fkrzkb8'


def get_content(url): 
    respone = requests.get(url)
    soup = BeautifulSoup(respone.content, 'html5lib')
    return soup

record = []
soup = get_content(url)

span = soup.find('div', class_= 'breadcrum')

raw1 = [ele.text.strip().replace('Loading...', '') for ele in span.find_all('strong')]
name = [ele.text for ele in span.find_all('i')]
lotno = span.find('span', text = re.compile(r'Mã tin :')).text.replace('Mã tin : ', '').strip()
price = soup.find('h1').text.split('- ')[-1].strip()

info = soup.find('div', class_ = 'tabbertab')

car_info = info.find_all('div', class_ = 'col')

for col in car_info: 
    record += [value.text.strip() for value in col.find_all('div', class_ = ['txt_input', 'inputbox'])]

record += [info.find('div', class_ = 'des_txt').text]
record += (raw1 + name)
record += [price, lotno, url]

record = [ele.strip() for ele in record]

# contact info
cus_info = soup.find('div', class_ = 'contact-txt')

try:
    tag_name = cus_info.find('a', class_ = 'cname')
    website = tag_name['href'].strip()
except: 
    tag_name = cus_info.find('span', class_ = 'cname')
    website = None

name_cus = tag_name.text.strip()

record_cus = [lotno, name_cus,
                cus_info.findAll('br')[1].next_sibling.text.replace('Địa chỉ:', '').strip(), # br tag --> \n in text --> use next_sibling for next text
                website]

phones = []
for phone in cus_info.find_all('span', class_ = 'cphone'):
    number = phone.text.replace(' ', '').strip()
    if 'document' in number:
        try: 
            number = re.search(r'\d+', number).group()
        except: 
            number = ''
    
    number = '@' + number
    phones.append(number)
record_cus += phones

print(record_cus)