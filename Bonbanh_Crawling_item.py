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

with open('car.csv', 'w', newline='', encoding = 'utf8') as csv_file, open('contact.csv', 'w', newline='', encoding='utf8') as contact_file:
    writer1 = csv.writer(csv_file)
    writer1.writerow(['Xuất xứ', 'Tình trạng', 'Dòng xe', 'Số Km đã đi', 'Màu ngoại thất', 'Màu nội thất', 
                     'Số cửa', 'Số chỗ ngồi', 'Động cơ', 'Hệ thống nạp nhiên liệu', 'Hộp số', 'Dẫn động', 
                     'Tiêu thụ nhiên liệu', 'Mô tả', 'Hãng', 'Grade', 'Năm sản xuất', 'Tên xe', 'Giá', 'Mã tin', 'URL'])
    
    writer2 = csv.writer(contact_file)
    writer2.writerow(['Mã tin', 'Tên', 'Địa chỉ', 'Website', 'Điện thoại 1', 'Điện thoại 2'])

    for idx in range(1, n_pages+1): 
        print(f'<=============== Crawling Page {idx} ===============>')
        url_next_page = 'https://bonbanh.com/oto/page,' + str(idx)

        soup = get_content(url_next_page)

        li_tags = soup.find('div', class_ = 'g-box-content').find_all('li', class_ = re.compile(r'car-item'))
        filtered_li_tags = [li.find('a').get('href') for li in li_tags if 'car-item' in li['class']]

        lst_url_car = ['https://bonbanh.com/'+ href for href in filtered_li_tags] 

        for url in lst_url_car: 
            print(url)
            # item info 
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
            writer1.writerow(record)

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
                    number = re.search(r'\d+', number).group()
                
                number = '@' + number
                phones.append(number)
            record_cus += phones
            writer2.writerow(record_cus)
        break