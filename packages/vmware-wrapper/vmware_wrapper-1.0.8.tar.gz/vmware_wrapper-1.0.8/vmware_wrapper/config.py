import requests
from vmware.vapi.bindings.stub import ApiClient, StubFactoryBase
from vmware.vapi.lib.connect import get_requests_connector
from vmware.vapi.stdlib.client.factories import StubConfigurationFactory
from vmware.vapi.vsphere.client import StubFactory
from vmware.vapi.vsphere.client import create_vsphere_client
import urllib3

session = requests.session()
session.verify = False
requests.packages.urllib3.disable_warnings()


# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# client = create_vsphere_client(server='127.0.0.1:8697', username='administrator@vsphere.local', password='Root_123', session=session)
# print(dir(client))

class Config:
    hostname = 'msk-vcenter-02.infotecs-nt'
    datacenter = 'QA DataCenter'
    cluster = 'QAHostClusterManual'
    resource_pool = 'R602 PKI Service'
    username = 'svcr602.pkis'
    password = '123654'
    datastore = 'R595_1'