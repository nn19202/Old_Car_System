import mysql.connector

def create_car_table(cursor): 
    query = '''
    CREATE TABLE IF NOT EXISTS CAR_DETAIL (
    `Mã tin` INT PRIMARY KEY,
    `Xuất xứ` TEXT,
    `Tình trạng` TEXT,
    `Dòng xe` TEXT,
    `Số Km đã đi` TEXT,
    `Màu ngoại thất` TEXT,
    `Màu nội thất` TEXT,
    `Số cửa` TEXT,
    `Số chỗ ngồi` TEXT,
    `Động cơ` TEXT,
    `Hệ thống nạp nhiên liệu` TEXT,
    `Hộp số` TEXT,
    `Dẫn động` TEXT,
    `Tiêu thụ nhiên liệu` TEXT,
    `Mô tả` TEXT,
    `Hãng` TEXT,
    `Grade` TEXT,
    `Năm sản xuất` TEXT,
    `Tên xe` TEXT,
    `Giá` TEXT,
    `URL` TEXT
    )'''

    cursor.execute(query)
    return

def create_buyer_table(cursor): 
    query = '''
    CREATE TABLE IF NOT EXISTS BUYER (
    `Mã tin` INT PRIMARY KEY,
    `Tên` TEXT, 
    `Địa chỉ` TEXT, 
    `Website` TEXT, 
    `Điện thoại 1` TEXT, 
    `Điện thoại 2` TEXT
    )'''

    cursor.execute(query)
    return 


def customize_query(cursor, query = None): 
    if query == None: 
        return 'Invalid syntax'
    
    cursor.execute(query)
    myresult = cursor.fetchall()
    return myresult

def insert_car_data(data, conn, cursor): 

    lot_no_check = data[0].strip()
    data.append(lot_no_check)
    cursor.execute('''INSERT INTO CAR_DETAIL 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    WHERE NOT EXISTS (SELECT 1 FROM CAR_DETAIL WHERE [Mã tin] = %s)''', data)
    conn.commit()
    return

def insert_buyer_data(data, conn, cursor): 

    lot_no_check = data[0].strip()
    data.append(lot_no_check)
    cursor.execute('''INSERT INTO BUYER
                    VALUES (%s, %s, %s, %s, %s, %s)
                    WHERE NOT EXISTS (SELECT 1 FROM CAR_DETAIL WHERE [Mã tin] = %s)''', data)
    conn.commit()
    return

def connect_database():
    config = {
        'user': '5chubaonho',
        'password': '5chubaonho',
        'host': '35.198.238.178',
        'database': 'databasecar'
    }
    
    cnx = mysql.connector.connect(**config)

    if cnx.is_connected():
        print("Đã kết nối đến cơ sở dữ liệu MySQL")
    else:
        print("Không thể kết nối đến cơ sở dữ liệu MySQL")

    cursor = cnx.cursor()
    return cnx, cursor