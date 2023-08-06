#!/usr/bin/env python
import os
import requests

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
whatsapp_number = os.environ['TWILIO_WHATSAPP_NUMBER']
my_number = os.environ['MY_NUMBER']

URL = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"


def get_current_status(fixed_str=None):
    if fixed_str == 'ok':
        with open("./es-status-ok.txt", "r") as result:
            return result.read()
    elif fixed_str == 'ko':
        with open("./es-status-not-ok.txt", "r") as result:
            return result.read()
    return ''


def execute():
    output = get_current_status('ko')
    print(output)
    if 'Active: active (running)' not in output:
        data = {
            "Body": "ATENÇÃO: O serviço do Elastic Search parou de funcionar!",
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

if __name__ == '__main__':
    execute()

