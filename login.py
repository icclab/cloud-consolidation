import os
import novaclient.client as nvclient
import ceilometerclient.client as cclient

def get_nova_creds():
    #returns credentials dictionary from os variables in nova format
    cred = {}
    cred['username'] = os.environ['OS_USERNAME']
    cred['api_key'] = os.environ['OS_PASSWORD']
    cred['auth_url'] = os.environ['OS_AUTH_URL']
    cred['project_id'] = os.environ['OS_TENANT_NAME']
    return cred

def get_ceilometer_creds():
    #returns credentials dictionary from os variables in ceilometer format
    cred = {}
    cred['os_username'] = os.environ['OS_USERNAME']
    cred['os_password'] = os.environ['OS_PASSWORD']
    cred['os_auth_url'] = os.environ['OS_AUTH_URL']
    cred['os_tenant_name'] = os.environ['OS_TENANT_NAME']
    return cred

def get_ceilometer_client():
    #returns ceilometer client
    creds_ceilometer = get_ceilometer_creds()
    return cclient.get_client(2,**creds_ceilometer)

def get_nova_client():
    #returns nova client
    creds_nova = get_nova_creds()
    #return nvclient.Client(**creds_nova)
    return nvclient.Client(2, creds_nova['username'], creds_nova['api_key'], creds_nova['project_id'], creds_nova['auth_url'])
