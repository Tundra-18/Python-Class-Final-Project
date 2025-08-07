import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname='employee_database',
        user='komg',
        password='321',
        host='localhost',
        port='5432'
    )
    return conn

