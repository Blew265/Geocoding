from psycopg2.extras import RealDictCursor
import psycopg2
import time


"""
The code below is responsible for connecting to the database when using raw sql in the project  comes
"""

while True:
    try:
        conn = psycopg2.connect(host='localhost', 
                                database='geocoding', 
                                user='postgres', 
                                password='blewDoppler',
                                cursor_factory=RealDictCursor)
        

        cursor = conn.cursor()
        
        print("Connection to the database was successful")
        break
    except Exception as error:
        print('Connection to database failed')
        print(f'Error: {error}')
        time.sleep(5)
