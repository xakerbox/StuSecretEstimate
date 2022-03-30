import pymysql.cursors
import pymysql
import db_variables
from db_variables import *


# Connect to the database
def get_head_data(westnum):
    connection = pymysql.connect(host=MYSQL_HOST,
                                user=MYSQL_USER,
                                password=MYSQL_PASSWORD,
                                db=MYSQL_DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `ehead` WHERE estnum={str(westnum)}"
            cursor.execute(sql)
            db_fetch_result = cursor.fetchone()
            if db_fetch_result:
                for i in db_fetch_result:
                    if db_fetch_result[i] == None:
                        db_fetch_result[i] = ''
                return db_fetch_result
            else:
                print('No match with such Estimate #. Try another number.')
    finally:
        connection.close()


#conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)


# Connect to the database
def get_line_data(westnum):
    connection = pymysql.connect(host=MYSQL_HOST,
                                user=MYSQL_USER,
                                password=MYSQL_PASSWORD,
                                db=MYSQL_DB,
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = f"SELECT * FROM `elines` WHERE elnum={str(westnum)}"
            cursor.execute(sql)
            db_fetch_result = cursor.fetchone()
            if db_fetch_result:
                for i in db_fetch_result:
                    if db_fetch_result[i] == None:
                        print('No fetch result. ')
                        db_fetch_result[i] = '  '
                return db_fetch_result
            else:
                print('No match with such Estimate #. Try another number.')
    finally:
        connection.close()        