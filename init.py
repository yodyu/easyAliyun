import sys
from aliyunsdkcore import client
from configparser import ConfigParser
from pyapi.ESCapi.Instance import InstanceAction
from entity.ECSentity.Instance import Instance
import Network
import NetworkAction


def initClient():
    with open('config.ini') as f:
        cfp = ConfigParser()
        cfp.read(f)

    key_id = cfp.get('KEY', 'Access_key_id')
    key_secret = cfp.get('KEY', 'Access_key_secret')
    region = cfp.get('ECS', 'region')

    clt = client.AcsClient(key_id, key_secret, region)

    return clt

myclient = initClient()

def start_one_instance(clt):
    instance = Instance()
    instanceAct = InstanceAction(clt)
    network = Network()
    networkAct = NetworkAction(clt)

    # create
    res = instanceAct.createInstance(instance)
    instance.instance_id = res.get('InstanceId')

    # network ip
    res = networkAct.AllocateEipAddress(network)
    print (res)
    network.allocation_id = res.get('AllocationId')

    res = network.AssociateEipAddress(instance, network)

    # start
    res = instanceAct.startInstance(instance)

def delete_one_instance(clt):
    # list
    instance = Instance()
    instanceAct = InstanceAction(clt)
    network = Network()
    networkAct = NetworkAction(clt)

    res = instanceAct.listInstances()
    # if only one instance
    if res.get('TotalCount') != 1:
        print('Error: instance total count = %s, not 1, exit ' % res.get('TotalCount'))
        sys.exit(1)

    ins_dic = res.get('instances').get('instance')[1]
    instance.instance_id = ins_dic.get('InstanceId')
    instance.status = ins_dic.get('Status')
    # if stop
    if instance.status == 'Running':
        instanceAct.stopInstance(instance)

    for i in range(1,30):
        pass

    # loop to insure  stop
    instanceAct.deleteInstance(instance)

    pass




