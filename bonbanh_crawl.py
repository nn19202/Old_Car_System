import csv
from bs4 import BeautifulSoup
import requests
import html5lib
import re 

def get_content(url): 
    respone = requests.get(url)
    soup = BeautifulSoup(respone.content, 'html5lib')
    return soup

soup = get_content('https://bonbanh.com/')

n_pages = int(soup.find('div', class_ = 'cpage').text.split('/')[-1].split()[0].replace(',', '').strip())

# Mở tệp CSV và ghi dữ liệu
with open('data.csv', 'w', newline='', encoding = 'utf8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Xuất xứ', 'Tình trạng', 'Dòng xe', 'Số Km đã đi', 'Màu ngoại thất', 'Màu nội thất', 'Số cửa', 
                     'Động cơ', 'Hệ thống nạp nhiên liệu', 'Hộp số', 'Dẫn động', 'Tiêu thụ nhiên liệu', 'Mô tả']) # Định nghĩa các trường

    for idx in range(1, n_pages+1): 
        print(f'<=============== Crawling Page {idx} ===============>')
        url_next_page = 'https://bonbanh.com/oto/page,' + str(idx)

        soup = get_content(url_next_page)
    
        li_tags = soup.find('div', class_ = 'g-box-content').find_all('li', class_ = re.compile(r'car-item'))
        filtered_li_tags = [li.find('a').get('href') for li in li_tags if 'car-item' in li['class']]

        lst_url_car = ['https://bonbanh.com/'+ href for href in filtered_li_tags] 
        
        for url in lst_url_car: 
            record = []

            soup = get_content(url)

            info = soup.find('div', class_ = 'tabbertab')

            car_info = info.find_all('div', class_ = 'col')

            for col in car_info: 
                record += [value.text.strip() for value in col.find_all('div', class_ = 'txt_input')]
            
            record += [info.find('div', class_ = 'des_txt').text]
            writer.writerow(record)
        break

