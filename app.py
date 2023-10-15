from flask import Flask, render_template, request, Response, redirect
from flask_socketio import SocketIO, emit
import os
from test_code import *
from db import *
from send_mail import mail_box
async_mode = None

app = Flask(__name__)
app.secret_key = 'super secret key'

socketio = SocketIO(app, async_mode=async_mode)


def background_thread(data):
    socketio.emit('my_response',
                    {'data': str(data)})


def send_chart_details(data):
    pass_tc = data.get('pass')
    fail_tc = data.get('fail')
    p=0
    f=0
    pass_count, fail_count, total_count,no_run = select_query_to_get_count_details(reg_id)
    p=int(pass_count)+pass_tc
    f=int(fail_count)+fail_tc
    update_regression(pass_tc, fail_tc, reg_id)
    socketio.emit('charts_details',{'pass_tc':p, 'fail_tc':f,'r_id':reg_id,'total_count':total_count})


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/logs', methods=['GET','POST'])
def logs():

    if request.method == "POST":
        global reg_id
        reg_id=add_regression(request)
        tc = request.form.get('data')
        for tc_name in tc.split(','):

            eval(tc_name + "()")
           
        call_after_execution(reg_id)
    return render_template('logs.html')

@app.route('/i_cmts', methods=['GET','POST'])
def i_cmts():
    
    return render_template('i_cmts.html')

@app.route('/harmony', methods=['GET','POST'])
def harmony():
    return render_template('harmony.html')

@app.route("/connect", methods=['GET','POST'])
@socketio.event
def connect():
    if request.method == "POST":
        data=request.json.get('data')
        socketio.start_background_task(background_thread, data)
        return Response({'msg':"Hi"})
    else:
        emit('my_response', {'data': ''})

@app.route("/charts", methods=['GET','POST'])
@socketio.event
def charts():    
    if request.method == "POST":
        data=request.json
        send_chart_details(data)
        return Response({'msg':"Hi"})
    else:
        return render_template('charts.html')



@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    emit('client disconnected','a client disconnected but I dont know who',broadcast = True)


@app.route("/stop", methods=['GET','POST'])
def stop():
    if request.method == "POST":
        socketio.stop()
        os.system("python -m flask run --reload")
    return Response({'msg':''})


@app.route("/add_regression_logs", methods=['GET','POST'])
def add_regression_logs():
    if request.method == "POST":
        response=request.json
        response['r_id']=reg_id
        add_regression_details(response)
    return Response({'msg':''})


@app.route("/view_regression_details", methods=['GET','POST'])
def view_regression_details():
    curr,conn=db_connection()
    cmts_type = request.args.get('cmts_type')
    if cmts_type != None and cmts_type != "":
        cmts_type="'"+cmts_type+"'"
        curr.execute(f"SELECT * FROM regression WHERE cmts_type="+cmts_type)
    else:
        curr.execute('SELECT * FROM regression ORDER BY date_added DESC')

    regression_details=curr.fetchall()
    
    curr.execute('SELECT cmts_type FROM regression')
    c_type_curr=curr.fetchall()
    c_type=[]
    [c_type.append(t[0]) for t in c_type_curr if t[0] not in c_type]
    
    conn.commit()
    curr.close()
    conn.close()
    if cmts_type != None:
        return render_template('regression_cmts_type_details.html',regression_details=regression_details,c_type=c_type)
    else:
        return render_template('regression_details.html',regression_details=regression_details,c_type=c_type)

@app.route("/view_tc_logs_details/<int:reg_id>", methods=['GET','POST'])
def view_tc_logs_details(reg_id):
    curr,conn=db_connection()
    # curr.execute(f'SELECT regression_logs_details.*,regression.summary_path FROM regression_logs_details,regression WHERE regression_logs_details.regression_id={reg_id} and regression.regression_id=regression_logs_details.regression_id')
    curr.execute(f'SELECT * FROM regression_logs_details WHERE regression_id={reg_id}')
    tc_logs_details=curr.fetchall()
    curr.execute(f"SELECT summary_path FROM regression WHERE regression_id={reg_id}")
    summary_path=curr.fetchone()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('view_tc_logs_details.html',tc_logs_details=tc_logs_details,summary_path=summary_path,reg_id=reg_id)


@app.route('/delete_regression/<int:id>', methods=['GET','POST'])
def delete_regression(id):
    if request.method == "POST":
        curr,conn=db_connection()
        curr.execute(f'DELETE FROM regression_logs_details WHERE regression_id={id}')
        curr.execute(f'DELETE FROM regression WHERE regression_id={id}')
        conn.commit()
        curr.close()
        conn.close()
        return redirect("/view_regression_details")

@app.route('/send_mail/<int:reg_id>', methods=['GET','POST'])
def send_mail(reg_id): 
    curr,conn=db_connection()
    curr.execute(f'SELECT summary_path FROM regression WHERE regression_id={reg_id}')
    summary_path = curr.fetchone()

    with open(f"static/files/{summary_path[0]}","r") as f:
        message=f.readlines()
    message_text=""
    for data in message:
        message_text+=data+"\n"

    conn.commit()
    curr.close()
    conn.close()
    mail_box(message)
    # os.system("python send_mail.py")
    return redirect("/")

if __name__ == '__main__':
    socketio.run(app, debug=True)


