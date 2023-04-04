from bs4 import BeautifulSoup
import requests
import re
import random
import sqlite3

class CrawlingBot: 
    def __init__(self, url_page = 'https://bonbanh.com/') -> None:
        self.url_page = url_page
        self.proxies = self.crawling_IP()
        self.proxy = None # proxy current
        return
    
    def get_content(self, url, proxy = None): 
        if proxy is None:
            print('Crawling with my IP!')
            respone = requests.get(url)
        else: 
            while True: 
                try:
                    respone = requests.get(url, proxies = proxy)
                    self.proxy = proxy
                except Exception as e: 
                    print(e)
                    proxy = self.create_prox()
                else: 
                    break
            print(f'Crawling with proxy ==> {proxy}')
        soup = BeautifulSoup(respone.content, 'html5lib')
        return soup 
    
    def crawling_IP(self):
        url = 'https://free-proxy-list.net/'
        
        soup = self.get_content(url)

        table = soup.find('table', class_ = 'table table-striped table-bordered')
        infos = table.find('tbody').find_all('tr')

        proxies = []
        for info in infos: 
            lst_info = [i.text for i in info.find_all('td')]
            if lst_info[6] == 'yes': 
                proxies.append(f'http://{lst_info[0]}:{lst_info[1]}')
        print(f"Have {len(proxies)} proxies by crawling")
        return proxies

    def create_prox(self):
        IP = random.choice(self.proxies)
        proxy = {
            'http' : IP,
            'https' : IP
        }
        return proxy
    
    def get_npages(self): 
        soup = self.get_content(self.url_page, proxy = self.create_prox())
        
        return int(soup.find('div', class_ = 'cpage').text.split('/')[-1].split()[0].replace(',', '').strip())
    
    def getUrl(self, id_page): 
        url = 'https://bonbanh.com/oto/page,' + str(id_page)
        soup = self.get_content(url, self.proxy)

        li_tags = soup.find('div', class_ = 'g-box-content').find_all('li', class_ = re.compile(r'car-item'))
        filtered_li_tags = [li.find('a').get('href') for li in li_tags if 'car-item' in li['class']]
        lst_url_car = ['https://bonbanh.com/'+ href for href in filtered_li_tags]
        
        return lst_url_car
    
    def crawl_car_data(self, sourcePage, url): 
        carJson = {
            'Mã tin' : None, 'Xuất xứ' : None, 'Tình trạng' : None, 'Dòng xe' : None, 'Số Km đã đi' : None, 'Màu ngoại thất' : None, 
           'Màu nội thất' : None, 'Số cửa' : None, 'Số chỗ ngồi' : None, 'Động cơ' : None, 'Hệ thống nạp nhiên liệu' : None, 
           'Hộp số' : None, 'Dẫn động' : None, 'Tiêu thụ nhiên liệu' : None, 'Mô tả' : None, 'Hãng' : None, 'Grade' : None, 
           'Năm sản xuất' : None, 'Tên xe' : None, 'Giá' : None, 'URL' : None
           }

        span = sourcePage.find('div', class_= 'breadcrum')

        raw1 = [ele.text.replace('Loading...', '') for ele in span.find_all('strong')]

        if len(raw1) < 3: # brand - grade - year ==> fix miss year 
            raw1.insert(2, '')  

        lotno = span.find('span', text = re.compile(r'Mã tin :')).text.replace('Mã tin : ', '')

        carJson['Tên xe'] = [ele.text for ele in span.find_all('i')][0]
        carJson['Mã tin'] = lotno
        carJson['Giá'] = sourcePage.find('h1').text.split('- ')[-1]
        carJson['URL'] = url

        info = sourcePage.find('div', class_ = 'tabbertab')
        car_info = info.find_all('div', class_ = 'col')

        record = []
        for col in car_info: 
            record += [value.text for value in col.find_all('div', class_ = ['txt_input', 'inputbox'])]

        carJson['Xuất xứ'] = record[0]
        carJson['Tình trạng'] = record[1]
        carJson['Dòng xe'] = record[2]
        carJson['Số Km đã đi'] = record[3]
        carJson['Màu ngoại thất'] = record[4]
        carJson['Màu nội thất'] = record[5]
        carJson['Số cửa'] = record[6]
        carJson['Số chỗ ngồi'] = record[7]
        carJson['Động cơ'] = record[8]
        carJson['Hệ thống nạp nhiên liệu'] = record[9]
        carJson['Hộp số'] = record[10]
        carJson['Dẫn động'] = record[11]
        carJson['Tiêu thụ nhiên liệu'] = record[12]
        carJson['Mô tả'] = [info.find('div', class_ = 'des_txt').text][0]

        carJson['Hãng'] = raw1[0]
        carJson['Grade'] = raw1[1]
        carJson['Năm sản xuất'] = raw1[2]
        
        return carJson, lotno

    def car_buyer_data(self, sourcePage, lotno):
        buyerJson = {
            'Mã tin' : None, 'Tên' : None, 'Địa chỉ' : None, 'Website' : None, 'Điện thoại 1' : None, 'Điện thoại 2' : None
            }
       
        cus_info = sourcePage.find('div', class_ = 'contact-txt')

        try:
            tag_name = cus_info.find('a', class_ = 'cname')
            website = tag_name['href']
        except: 
            tag_name = cus_info.find('span', class_ = 'cname')
            website = None

        buyerJson['Mã tin'] = lotno
        buyerJson['Tên'] = tag_name.text
        buyerJson['Địa chỉ'] = cus_info.findAll('br')[1].next_sibling.text.replace('Địa chỉ:', '')
        buyerJson['Website'] = website

        phones = []
        for phone in cus_info.find_all('span', class_ = 'cphone'):
            number = phone.text.replace(' ', '')
            if 'document' in number:
                try: 
                    number = re.search(r'\d+', number).group()
                except: 
                    number = None                        
            phones.append(number)
        buyerJson['Điện thoại 1'] = phones[0]
        buyerJson['Điện thoại 2'] = phones[1]
        
        return buyerJson
    
    def insert_car_data(self, data, conn, cursor): 
        cursor.execute('''INSERT OR IGNORE INTO CAR_DETAIL 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        return
    
    def insert_buyer_data(self, data, conn, cursor): 
        cursor.execute('''INSERT OR IGNORE INTO BUYER
                        VALUES (?, ?, ?, ?, ?, ?)''', data)
        conn.commit()
        return
    
    def crawl_data(self):
        numberofPages = self.get_npages()
        for idx in range(1, numberofPages+1): 

            conn = sqlite3.connect('data.db')
            cursor = conn.cursor() 


            lst_url_car = self.getUrl(idx)
            print(f'<=============== Crawling Page {idx} ===============>')
            for url in lst_url_car: 
                soup = self.get_content(url, self.proxy)

                try:
                    carJson, lotno = self.crawl_car_data(soup, url)
                    self.insert_car_data(list(carJson.values()), conn, cursor)

                    buyerJson = self.car_buyer_data(soup, lotno)
                    self.insert_buyer_data(list(buyerJson.values()), conn, cursor)

                except Exception as e: 
                    print(e)
            conn.close()
        return

bot = CrawlingBot()
bot.crawl_data()