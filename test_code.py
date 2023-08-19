from utlis import send_req
import requests


def TC_1(r_id):
    print("\n\nTC_1 Called===")
    output = """ASD-GT0003-CCAP001# show clock 
    2023 June 1 07:00:46 
    ASD-GT0003-CCAP001# 
    """

    send_req("\n\n########### Executed command: show clock #################\n\n")

    for i in output.splitlines():
        # print(i)
        send_req(i)

    send_req("====== TABLE ====================")
    # print(tableObj.draw())
    # for t in tableObj.draw().splitlines():
    #     send_req(t)
    #     print(t)
    send_req("Teststep:Pass")
    requests.post("http://localhost:5000/charts", json={"pass":0, "fail":1,'r_id':r_id},headers = {'Content-type': 'application/json'})

def TC_2(r_id):
    print("\n\nTC_2 Called===")
    output = """ 
  ASD-GT0003-CCAP001# show clock 
    2023 June 1 07:00:46 
    ASD-GT0003-CCAP001# 
    """

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0,'r_id':r_id},headers = {'Content-type': 'application/json'})

def TC_3(r_id):
    
    output = """ 
        Hello GPA........
    """

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    send_req("Teststep:FAIL")
    requests.post("http://localhost:5000/charts", json={"pass":1, "fail":0,'r_id':r_id},headers = {'Content-type': 'application/json'})
    

def TC_4(r_id):
    
    output = """ 
        Hello Arjun........
    """

    send_req("\n\n########### Test Case 2 #################\n\n")
    for i in output.splitlines():
        send_req(i)
    requests.post("http://localhost:5000/charts", json={"pass":0, "fail":1,'r_id':r_id},headers = {'Content-type': 'application/json'})
    
