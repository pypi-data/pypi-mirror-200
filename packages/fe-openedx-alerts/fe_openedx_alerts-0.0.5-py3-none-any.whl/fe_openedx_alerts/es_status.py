#!/usr/bin/env python
import os
import requests
import subprocess
from datetime import datetime

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
whatsapp_number = os.environ['TWILIO_WHATSAPP_NUMBER']
my_number = os.environ['MY_NUMBER']
server_name = os.environ['SERVER_NAME']

URL = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


def get_current_status(fixed_str=None):
    output = subprocess.run(['/usr/sbin/service', 'elasticsearch', 'status'], capture_output=True, text=True)
    return output.stdout


def main():
    output = get_current_status('ko')
    if 'Active: active (running)' not in output:
        data = {
            "Body": f"ATENÇÃO: O serviço do Elastic Search parou de funcionar! Servidor: {server_name}",
            "From": f"{whatsapp_number}",
            "To": f"{my_number}"
        }
        auth = (account_sid, auth_token)
        response = requests.post(URL, data=data, auth=auth)

        if response.status_code == 201:
            print("Mensagem enviada com sucesso!")
            print(f"response: {response.text}")
        else:
            print(f"Erro ao enviar mensagem: {response.text}")
    else:
        print(f"{datetime.now()} => All good! :D")


if __name__ == '__main__':
    main()

