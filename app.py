from flask import Flask, render_template, session, request, Response
from flask_socketio import SocketIO, emit
import os
from test_code import *
from db import *
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
    r_id = data.get('r_id')
    update_regression(pass_tc, fail_tc, r_id)
    socketio.emit('charts_details',{'pass_tc':pass_tc, 'fail_tc':fail_tc,'r_id':r_id})


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/logs', methods=['GET','POST'])
def logs():
    if request.method == "POST":
        regression_name = request.form.get('regression_name')
        total_tc_selected = request.form.get('total_tc_selected')
        r_id=add_regression(regression_name, total_tc_selected)
        # r_id='0'
        tc = request.form.get('data')
        for tc_name in tc.split(','):
            eval(tc_name + "("+r_id+")")
        
    return render_template('logs.html')

@app.route('/i_cmts', methods=['GET','POST'])
def i_cmts():
    return render_template('i_cmts.html')

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
        add_regression_details(response)
    return Response({'msg':''})


@app.route("/view_regression_details", methods=['GET','POST'])
def view_regression_details():
    curr,conn=db_connection()
    curr.execute('SELECT * FROM regression ORDER BY date_added DESC')
    regression_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('regression_details.html',regression_details=regression_details)

@app.route("/view_tc_logs_details/<int:reg_id>", methods=['GET','POST'])
def view_tc_logs_details(reg_id):
    curr,conn=db_connection()
    curr.execute(f'SELECT * FROM regression_logs_details WHERE regression_id={reg_id}')
    tc_logs_details=curr.fetchall()
    conn.commit()
    curr.close()
    conn.close()
    return render_template('view_tc_logs_details.html',tc_logs_details=tc_logs_details)


if __name__ == '__main__':
    socketio.run(app, debug=True)
