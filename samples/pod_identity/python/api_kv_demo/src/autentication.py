import os
from datetime import datetime
import requests
from azure.common.credentials import ServicePrincipalCredentials
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from msrestazure.azure_active_directory import MSIAuthentication, ServicePrincipalCredentials


CLIENT = "ba165219-f319-4083-b47a-331e6671f1f1"
TENANT_ID = "ef29fa23-67e1-4363-8f49-6c521029bd71"
KEY = '15nw_cy_vS9p3gaHZP063.GpUvjG504-D6'
KEY_VAULT = "https://aksidentitydemo.vault.azure.net/"
RESOURCE_KV= 'https://vault.azure.net'

from flask import Flask
app = Flask(__name__)

def kv_get_secret(secret_id):
    client = KeyVaultClient(get_kv_credentials())
    value_id = client.get_secret(KEY_VAULT, secret_id, "")  
    if(value_id is None):
            return ("")
    else:
        print('Geting Secret %s with value %s' % (secret_id,value_id.value))
        return (value_id.value)


def get_kv_credentials():
    
    if "APPSETTING_WEBSITE_SITE_NAME" in os.environ:
        return MSIAuthentication(
            resource=RESOURCE_KV
        )
    else:    
        credentials = ServicePrincipalCredentials(
        client_id = CLIENT,
        secret = KEY,
        tenant = TENANT_ID,
        resource = RESOURCE_KV
    )
    
    return credentials


@app.route('/')
def hello_world():
    try:
        return kv_get_secret("pythonsecret")
    except Exception as err:
        return str(err)


@app.route('/ping')
def ping():
    return "Hello world"


if __name__ == '__main__':
    app.run()
