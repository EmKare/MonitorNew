from parkingLots_newWith_list import _parkingLots
import mysql.connector

USERS = [
    ("demouser0","123456789","M","0Demo","User0","demo0@use.yea",8760000000,"100000000",1234567890123456,"100","11","25",),
    ("demouser1","123456789","F","1Demo","User1","demo1@use.yea",8761111111,"111111111",2345678901234567,"111","12","26",),
    ("demouser2","123456789","M","2Demo","User2","demo2@use.yea",8762222222,"122222222",3456789012345678,"122","11","27",),
    ("demouser3","123456789","F","3Demo","User3","demo3@use.yea",8763333333,"133333333",4567890123456789,"133","12","28",),
    ("demouser4","123456789","M","4Demo","User4","demo4@use.yea",8764444444,"144444444",5678901234567890,"144","11","27",),
    ("demouser5","123456789","F","5Demo","User5","demo5@use.yea",8765555555,"155555555",6789012345678901,"155","11","26",),
    ("demouser6","123456789","M","6Demo","User6","demo6@use.yea",8766666666,"166666666",7890123456789012,"166","12","25",),
    ("demouser7","123456789","F","7Demo","User7","demo7@use.yea",8767777777,"177777777",8901234567890123,"177","11","26",),
    ("demouser8","123456789","M","8Demo","User8","demo8@use.yea",8768888888,"188888888",9012345678901234,"188","12","27",),
    ("demouser9","123456789","F","9Demo","User9","demo9@use.yea",8769999999,"199999999",1012345678901234,"199","11","28",),    
]

def create_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="FindMeParking"
    )
    mycursor = mydb.cursor()
    return mydb, mycursor

def close_connection(mydb):
    mydb.close()
    
def create_database_if_not_exists():
    mydb, mycursor = create_connection()
    
    mycursor.execute("CREATE DATABASE IF NOT EXISTS FindMeParking")
    mydb.commit()
    
    print("------TABLES------")
    mycursor.execute("SHOW TABLES;")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        for x in myresult:
            print(x)
    print("------TABLES------")
    
    close_connection(mydb)    
    create_ParkingLot_locations_table()

def create_ParkingLot_locations_table():
    mydb, mycursor = create_connection()
    has_data = False
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS ParkingLot_locations \
    (\
        lot_number INT auto_increment,\
        lot_title VARCHAR(100) NOT NULL,\
        lot_lat_coord FLOAT NOT NULL,\
        lot_long_coord FLOAT NOT NULL,\
        lot_type INT NOT NULL,\
        PRIMARY KEY (lot_number)\
    );")
    mydb.commit()
    
    mycursor.execute("SELECT * FROM ParkingLot_locations")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        has_data = True
        
    #INSERTING INTO THE LOCATIONS TABLE
    if not has_data:
        for name, item_list in _parkingLots.items():        
            sql = "INSERT INTO ParkingLot_locations (lot_title, lot_lat_coord, lot_long_coord, lot_type) VALUES (%s, %s, %s, %s)"        
            val = (name, float(item_list[0][0]), float(item_list[0][1]), int(item_list[1]),)
            mycursor.execute(sql, val)
            mydb.commit()
    has_data = False
    
    close_connection(mydb)
    create_FindMeParking_USERS_table(has_data)
    
def create_FindMeParking_USERS_table(has_data:bool):
    mydb, mycursor = create_connection()
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS FindMeParking_USERS ( \
        user_number INT auto_increment,\
        user_username VARCHAR(20) NOT NULL,\
        user_password VARCHAR(100) NOT NULL,\
        user_gender VARCHAR(1) NOT NULL,\
        user_fname VARCHAR(20) NOT NULL,\
        user_lname VARCHAR(30) NOT NULL,\
        user_email VARCHAR(40) NOT NULL,\
        user_tele BIGINT NOT NULL,\
        user_id VARCHAR(9) NOT NULL,\
        user_cardNo BIGINT NOT NULL,\
        user_cvv VARCHAR(4) NOT NULL,\
        user_exp_month VARCHAR(2) NOT NULL,\
        user_exp_year VARCHAR(2) NOT NULL,\
        PRIMARY KEY (user_number)\
    );")
    mydb.commit()
    
    try:
        mycursor.execute("ALTER TABLE FindMeParking_USERS AUTO_INCREMENT=10101;")
        mydb.commit()
    except Exception:
        print("Exception -- ROLLBACK (( ALTER TABLE FindMeParking_USERS AUTO_INCREMENT=10101 ))")
        mydb.rollback()
    
    try:
        mycursor.execute("ALTER TABLE FindMeParking_USERS ADD UNIQUE (user_email,user_id);")
        mydb.commit()
    except Exception:
        print("Exception -- ROLLBACK (( ALTER TABLE FindMeParking_USERS ADD UNIQUE (user_email,user_id); ))")
        mydb.rollback()
        
    mycursor.execute("SELECT * FROM FindMeParking_USERS")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        has_data = True        
        
    if not has_data:
        for val in USERS:     
            sql = "INSERT INTO FindMeParking_USERS \
                (user_username, user_password, user_gender, user_fname, user_lname, user_email, user_tele, user_id, user_cardNo, user_cvv, user_exp_month, user_exp_year)\
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"    
            try:
                mycursor.execute(sql, val)
                mydb.commit()
            except Exception:
                print(f"Exception @ {val}")
                mydb.rollback()
    has_data = False
    
    try: 
        mycursor.execute("ALTER TABLE FindMeParking_USERS ADD COLUMN user_status ENUM('Active', 'Inactive', 'Blocked') DEFAULT 'Active';")
        mydb.commit()
    except Exception:
        print("Exception (( ALTER TABLE FindMeParking_USERS ADD COLUMN user_status ENUM('Active', 'Inactive', 'Blocked') DEFAULT 'Active'; ))")
        mydb.rollback()
        
    #Update the existing rows with the default status (Active)
    try:
        mycursor.execute("UPDATE FindMeParking_USERS SET user_status = if( user_status = NULL,'Active', user_status);")
        mydb.commit()
    except Exception:
        print("Exception (( UPDATE FindMeParking_USERS SET user_status = 'Active'; ))")
        mydb.rollback()
        
    try:
        mycursor.execute("ALTER TABLE FindMeParking_USERS ADD COLUMN user_balance FLOAT DEFAULT 1000;")
        mydb.commit()
    except Exception:
        print("Exception (( ALTER TABLE FindMeParking_USERS ADD COLUMN user_balance FLOAT DEFAULT 1000; ))")
        mydb.rollback()
        
    try:
        mycursor.execute("UPDATE FindMeParking_USERS SET user_balance = if( user_balance = NULL,1000, user_balance);")
        mydb.commit()
    except Exception:
        print("Exception (( UPDATE FindMeParking_USERS SET user_balance = if( user_balance = NULL,1000, user_balance); ))")
        mydb.rollback()
        
    close_connection(mydb)
    create_FindMeParking_USER_PreviousBookings_table(has_data)
    
def create_FindMeParking_USER_PreviousBookings_table(has_data:bool):
    mydb, mycursor = create_connection()
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS FindMeParking_USER_PreviousBookings ( \
        user_PreviousBookings_no INT auto_increment, \
        user_PreviousBookings_usernumber INT NOT NULL,\
        user_PreviousBookings_String VARCHAR(300) NOT NULL,\
        PRIMARY KEY (user_PreviousBookings_no)\
    );")
    mydb.commit()
    
    try:
        mycursor.execute("ALTER TABLE FindMeParking_USER_PreviousBookings AUTO_INCREMENT=1000000;")
        mydb.commit()
    except Exception:
        mydb.rollback()
    
    close_connection(mydb)
    create_FindMeParking_VALID_USERS_table(has_data)
        
def create_FindMeParking_VALID_USERS_table(has_data):
    mydb, mycursor = create_connection()
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS FindMeParking_VALID_USERS ( \
        valid_user_no INT AUTO_INCREMENT, \
        valid_user_number INT NOT NULL,\
        valid_user_email VARCHAR(40) NOT NULL,\
        valid_user_id VARCHAR(9) NOT NULL,\
        PRIMARY KEY (valid_user_no),\
        FOREIGN KEY (valid_user_number) REFERENCES FindMeParking_USERS(user_number)\
    );")
    mydb.commit()
    
    try:
        mycursor.execute("ALTER TABLE FindMeParking_VALID_USERS AUTO_INCREMENT=100;")
        mydb.commit()
    except Exception:
        mydb.rollback()
            
    #CHECK IF THE 'FindMeParking_VALID_USERS' TABLE ALREADY HAS DATA
    mycursor.execute("SELECT * FROM FindMeParking_VALID_USERS")
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        has_data = True
        
    if not has_data:    
        mycursor.execute("SELECT * FROM FindMeParking_USERS")
        myresult = mycursor.fetchall()
        
        user = 0
        for result in myresult:        
            sql = "INSERT INTO FindMeParking_VALID_USERS (valid_user_number, valid_user_email, valid_user_id) VALUES (%s,%s,%s)"        
            val = (result[0], result[6], result[8])
            mycursor.execute(sql, val)
            mydb.commit()
    has_data = False
    
    close_connection(mydb)
    create_FindMeParking_BLOCKED_USERS_table(has_data)

def create_FindMeParking_BLOCKED_USERS_table(has_data:bool):
    mydb, mycursor = create_connection()
    
    mycursor.execute("CREATE TABLE IF NOT EXISTS FindMeParking_BLOCKED_USERS ( \
        blocked_user_no INT AUTO_INCREMENT, \
        blocked_user_number INT NOT NULL,\
        blocked_user_email VARCHAR(40) NOT NULL,\
        blocked_user_id VARCHAR(9) NOT NULL,\
        PRIMARY KEY (blocked_user_no),\
        FOREIGN KEY (blocked_user_number) REFERENCES FindMeParking_USERS(user_number)\
    );")
    mydb.commit()
    
    try:
        mycursor.execute("ALTER TABLE FindMeParking_BLOCKED_USERS AUTO_INCREMENT=100;")
        mydb.commit()
    except Exception:
        mydb.rollback()
    
    
    
    
    
    
    
    
    
