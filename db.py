import psycopg2

def db_connection():
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/postgres")
    curr = conn.cursor()
    print(curr)
    return curr, conn
# db_connection()
# curr, conn=db_connection()
# curr.execute("DELETE  FROM regression_logs_details")
# curr.execute("DELETE  FROM regression")
# conn.commit()
# curr.close()
# conn.close()

def add_regression(request):
    curr, conn=db_connection()
    regression_name = request.form.get('regression_name')
    total_tc_selected = request.form.get('total_tc_selected')
    cmts_type = request.form.get('cmts_type')
    curr.execute(
        '''INSERT INTO regression \
        (regression_name, pass_count, fail_count, no_run_count, total_count,status,cmts_type) VALUES (%s, %s, %s, %s,%s,%s,%s) RETURNING regression_id''',
        (regression_name, 0, 0, 0,int(total_tc_selected),"In Progress", cmts_type))

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
    print(query_data)
    pass_count=query_data[2]
    fail_count=query_data[3]
    no_run_count=query_data[4]
    total_count=query_data[5]

    pass_count+=pass_tc
    fail_count+=fail_tc
    curr.execute(f'UPDATE regression SET pass_count={pass_count}, fail_count={fail_count} WHERE regression_id={r_id}')
    
    if int(total_count) == int(pass_count)+int(fail_count)+int(no_run_count):

        curr.execute('''UPDATE regression SET status=%s WHERE regression_id=%s''',( "Completed", r_id))
    
    conn.commit()
    curr.close()
    conn.close()


def add_regression_details(response):
    r_id=response.get('r_id')
    status=response.get('status')
    fail_in=response.get('fail_in')
    tc_no=str(response.get('tc_no'))
    execution_time=response.get('execution_time')
    testcase_name=response.get('testcase_name')
    tc_logs_path=response.get('tc_logs_path')
    
    status=status.upper()
    # status_list.append(status)
    # status = "FAIL" if "FAIL" in status_list else "PASS"
    curr, conn=db_connection()
    curr.execute('''INSERT INTO regression_logs_details(regression_id,testcase_number,testcase_name,status, failed_in,execution_time,tc_logs_path) VALUES (%s,%s,%s,%s,%s,%s,%s)''',(r_id,tc_no,testcase_name,status, fail_in, execution_time,tc_logs_path) )
    
    conn.commit()
    curr.close()
    conn.close()

    
def update_regression_summary_path(r_id, path):
    curr, conn=db_connection()
    curr.execute('''UPDATE regression SET summary_path=%s WHERE regression_id=%s''',( str(path), r_id))
    conn.commit()
    curr.close()
    conn.close()
    

def select_query_to_get_count_details(reg_id):
    curr,conn=db_connection()
    curr.execute(f"SELECT * FROM regression WHERE regression_id={reg_id}")
    query_data=curr.fetchone()
    pass_count=query_data[2]
    fail_count=query_data[3]
    no_run=query_data[4]
    total_count=query_data[5]
    conn.commit()
    curr.close()
    conn.close()
    return pass_count, fail_count, total_count,no_run
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
#     testcase_number INT,
#     testcase_name text,
#     status varchar(1000),
#     failed_in text,
#     execution_time text,
#     tc_logs_path text,
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
#     summary_path text,
#     status varchar(1000),
#     cmts_type varchar(1000),
#     date_added timestamp DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY(regression_id)

# );
