# app.py
import os
import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

api_contact = 'https://app.nectarcrm.com.br/crm/api/1/contatos/'
api_oportunidades = 'https://app.nectarcrm.com.br/crm/api/1/oportunidades/'
api_local= "https://5000-haislanmontanha-gev-55t1r8kq5qw.ws-us29.gitpod.io/"
menu_cpf = "cpf"
menu_cnpj = "cnpj"
menu_telefone = "telefone"
menu_email = "email"
menu_statistics = "statistics"
menu_proximaAtividade = "proximaAtividade"
menu_qualificacao = "qualificacao"
menu_oportunidade = "oportunidade"

headers = {
    'Accept': 'application/json', 
    'Access-Token':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw',
    'User-Agent':'request'}

params = {'api_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDI3OTA4MDgsImV4cCI6MTY3NDMyMjM2OSwidXNlckxvZ2luIjoiaGFpc2xhbi5uYXNjaW1lbnRvQGdtYWlsLmNvbSIsInVzZXJJZCI6IjEyNjQ2NiIsInVzdWFyaW9NYXN0ZXJJZCI6IjEyNjQ2NSJ9.08lkZ8ou0mxda9Hq45J07elTRTpD-2MZYS6pYcMnOcw'}

def menu_inicial(msg):
    return {
        "type":"MENU",
        "text": msg,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url":"https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
            }
        ],
        "items":[
            {
                "number":1,
                "text":"CPF",
                "callback":{
                    "endpoint": api_local+"nectarcrm_cpf",
                    "data":{
                    }
                }
            },
            {
                "number":2,
                "text":"CNPJ",
                "callback":{
                    "endpoint": api_local+"nectarcrm_cnpj",
                    "data":{
                    }
                }
            },
            {
                "number":3,
                "text":"Telefone",
                "callback":{
                    "endpoint": api_local+"nectarcrm_telefone",
                    "data":{
                    }
                }
            },
            {
                "number":4,
                "text":"Email",
                "callback":{
                    "endpoint": api_local+"nectarcrm_email",
                    "data":{
                    }
                }
            }
        ]
    }

def menu_user(user_json, msg):
    return {
        "type":"MENU",
        "text": msg,
        "attachments":[
            {
                "position":"BEFORE",
                "type":"IMAGE",
                "name":"image.png",
                "url":"https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
            }
        ],
        "items":[
            {
                "number":1,
                "text":"Analisar Estatistica",
                "callback":{
                    "endpoint": api_local+"nectarcrm_statistics",
                    "data":{
                        "user": user_json
                    }
                }
            },
            {
                "number":2,
                "text":"Próxima tarefa",
                "callback":{
                    "endpoint": api_local+"nectarcrm_proximaAtividade",
                    "data":{
                        "user": user_json
                    }
                }
            },
            {
                "number":3,
                "text":"Qualificações",
                "callback":{
                    "endpoint": api_local+"nectarcrm_qualificacao",
                    "data":{
                        "user": user_json
                    }
                }
            },
            {
                "number":4,
                "text":"Oportunidade",
                "callback":{
                    "endpoint": api_local+"nectarcrm_oportunidade",
                    "data":{
                        "user": user_json
                    }
                }
            }
        ]
    }

def response_question(text, callback):
    return {
        "type": "QUESTION",
        "text": text,
        "attachments": [{
            "position": "BEFORE",
            "type": "IMAGE",
            "name": "image.png",
            "url": "https://itsstecnologia.com.br/blogs/wp-content/uploads/2021/04/integracao-na-empresa.png"
        }],
        "callback": {
            "endpoint": callback,
            "data": {
                
            }
        }
    }

def informacao_invalida(msg_menu):
    if msg_menu == menu_cpf:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"nectarcrm_cpf")
    elif msg_menu == menu_cnpj:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"nectarcrm_cnpj")
    elif msg_menu == menu_telefone:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"nectarcrm_telefone")
    elif msg_menu == menu_email:
        return response_question("O "+msg_menu+" é inválido. Por favor informe um "+msg_menu+" válido.", api_local+"nectarcrm_email")
    else:
        return menu_inicial("Olá, por favor informe uma das seguintes informações.")

def getUser(request_mz, msg_menu):

    if (request_mz.status_code == 200):
        print("The request was a success!")
        # Code here will only run if the request is successful
        resposta_json = request_mz.json()
        json_size = len(resposta_json)

        print(f"Status Code: {request_mz.status_code}, Content: {resposta_json}, Size Json {json_size}")

        msg_erro_menu = "Olá, não encontramos seu contato pelo "+msg_menu+". Informe uma das seguintes opções: "

        if json_size == 0:
            return informacao_invalida(msg_menu), 201
        else:

            s1 = json.dumps(resposta_json)
            user = json.loads(s1)
            
            if 'message' not in user:

                userId = resposta_json[0]["id"]
                request_user = requests.get(api_contact+str(userId), params=params, headers=headers)
                user_json = request_user.json()

                msg = "Olá "+user_json['nome']+", informe qual opção deseja consultar"

                return menu_user(user_json, msg), 201
            else:
                return informacao_invalida(msg_menu), 201
                
    elif (request_mz.status_code == 404):
        return {"error": "Request must be JSON"}, 404

@app.post("/nectarcrm")
def start_nectarcrm():
    if request.is_json:
        mz = request.get_json()
        telefone = mz["contact"]["key"]

        request_mz = requests.get(api_contact+'telefone/'+telefone, params=params, headers=headers) 
        
        return getUser(request_mz, "menu_inicial")

    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_cpf")
def getcpf_nectarcrm():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'cpf/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_cpf)

    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_cnpj")
def getcnpj_nectarcrm():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'cnpj/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_cnpj)

    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_telefone")
def gettelefone_nectarcrm():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'telefone/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_telefone)

    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_email")
def getemail_nectarcrm():
    if request.is_json:

        mz = request.get_json()
        text = mz["text"]

        request_mz = requests.get(api_contact+'email/'+text, params=params, headers=headers)

        return getUser(request_mz, menu_email)

    return {"error": "Request must be JSON"}, 415

@app.post("/nectarcrm_oportunidade")
def getoportunidade_nectarcrm():
    if request.is_json:
        return {'msg':'Chegou aqui - nectarcrm_oportunidade'}, 201

    return {"error": "Request must be JSON"}, 415