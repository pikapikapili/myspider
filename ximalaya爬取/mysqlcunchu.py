import pymysql

def get_conn():
    conn=pymysql.Connection(host="127.0.0.1",port=3306,
                            user='root',password='123456',
                            database='ximalaya')
    return conn

def execute_sql(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql)
    id=cursor.fetchone()
    return id

def close_conn(conn):
    conn.close()

def execute1_sql(sql, conn):
    cursor = conn.cursor()
    cursor.execute(sql)
    id=cursor.fetchone()[0]
    return