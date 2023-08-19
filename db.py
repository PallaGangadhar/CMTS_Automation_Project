import psycopg2
from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

def db_connection():
    conn = psycopg2.connect(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}")
    curr = conn.cursor()
    return curr, conn

def add_regression(regression_name,total_tc_selected):
    curr, conn=db_connection()
    curr.execute(
        '''INSERT INTO regression \
        (regression_name, pass_count, fail_count, no_run_count, total_count) VALUES (%s, %s, %s, %s,%s) RETURNING regression_id''',
        (regression_name, 0, 0, 0,int(total_tc_selected)))

    r_id = curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    r_id=str(r_id[0])
    return r_id
        


def update_regression(pass_tc,fail_tc,r_id):
    curr, conn=db_connection()
    curr.execute(f'SELECT * FROM regression WHERE regression_id={r_id}')
    query_data=curr.fetchone()
    pass_count=query_data[2]
    fail_count=query_data[3]
    total_count=query_data[5]

    pass_count+=pass_tc
    fail_count+=fail_tc
    total_count = pass_count+fail_count
    curr.execute(f'UPDATE regression SET pass_count={pass_count}, fail_count={fail_count}, total_count={total_count} WHERE regression_id={r_id}')
    conn.commit()
    curr.close()
    conn.close()


def add_regression_details(response):
    status_list=[]
    status=None
    names=response.get('names')
    r_id=response.get('r_id')
    pass_tc=response.get('pass')
    
    status="PASS" if pass_tc == 1 else "FAIL"
    status_list.append(status)
    status = "FAIL" if "FAIL" in status_list else "PASS"
    curr, conn=db_connection()
    curr.execute('''INSERT INTO regression_logs_details(regression_id,testcase_name,status) VALUES (%s,%s,%s)''',(r_id,names,status) )
    curr.execute('''UPDATE regression SET status=%s WHERE regression_id=%s''',( status, r_id))
    conn.commit()
    curr.close()
    conn.close()

    
    
    

# def insert()
# curr.execute('CREATE TABLE IF NOT EXISTS regression (regression_id INT,'
#                                  'regression_name varchar (1000) NOT NULL,'
#                                  'pass_count integer NOT NULL,'
#                                  'fail_count integer NOT NULL,'
#                                  'total_count integer NOT NULL,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP),'
#                                 'PRIMARY KEY(regression_id)'
#                                  )


# curr.execute('CREATE TABLE IF NOT EXISTS logs (logs_id serial,'
#                                  'regression_id INT,'
#                                  'status varchar(1000) NOT NULL,'
#                                  'date_added date DEFAULT CURRENT_TIMESTAMP,'
#                                  'CONSTRAINT fk_regression FOREIGN KEY(regression_id) REFERENCES regression(regression_id)'
#                                  )
# CREATE TABLE IF NOT EXISTS logs(
#     logs_id INT,
#     regression_id INT,
#     status varchar(1000) NOT NULL,
#     date_added date DEFAULT CURRENT_TIMESTAMP,

#     CONSTRAINT fk_regression FOREIGN KEY(regression_id)
#         REFERENCES regression(regression_id)
# );

# regression_name='ABC',
# pass_count=1
# fail_count=1
# total_count=0
# curr.execute(
#         '''INSERT INTO regression \
#         (regression_name, pass_count, fail_count,total_count) VALUES (%s, %s, %s, %s) RETURNING regression_id''',
#         (regression_name, pass_count, fail_count, total_count))

# data = curr.fetchone()
# print("User ID of latest entry:", type(data[0]))

# curr.execute(
#         '''INSERT INTO logs \
#         (regression_id,testcase_name, status) VALUES (%s,%s, %s)''',
#         (1,"TC_1","PASS"))

# CREATE TABLE IF NOT EXISTS regression_logs_details(
#     log_id serial,
#     regression_id INT,
#     testcase_name text,
#     status varchar(1000),
#     date_added timestamp DEFAULT CURRENT_TIMESTAMP,

#     CONSTRAINT fk_regression FOREIGN KEY(regression_id)
#         REFERENCES regression(regression_id)
# );

# CREATE TABLE IF NOT EXISTS regression(
#     regression_id serial,
#     regression_name text NOT NULL, 
#     pass_count integer NOT NULL,
#     fail_count integer NOT NULL,
#     no_run_count integer NOT NULL,
#     total_count integer NOT NULL,
#     status varchar(1000),
#     date_added timestamp DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(regression_id)

# );
