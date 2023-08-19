import requests
import time
import secrets

def send_req(message):
    # time.sleep(0.3)
    requests.post("http://localhost:5000/connect", json={"data": message},headers = {'Content-type': 'application/json'})
    
def generate_key():
    ''' genearate key '''
    return secrets.token_hex(6)