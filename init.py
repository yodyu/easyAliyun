import sys
from aliyunsdkcore import client
from ConfigParser import ConfigParser

from pyapi.ECSapi.InstanceAction import InstanceAction
from entity.ECSentity.Instance import Instance
from pyapi.ECSapi.NetworkAction import NetworkAction
from entity.ECSentity.Network import Network


def initClient():
    with open('config.ini') as f:
        cfp = ConfigParser()
        cfp.read(f)

    key_id = cfp.get('KEY', 'Access_key_id')
    key_secret = cfp.get('KEY', 'Access_key_secret')
    region = cfp.get('ECS', 'region')

    return client.AcsClient(key_id, key_secret, region)


def start_one_instance():
    instance = Instance()
    instanceAct = InstanceAction(clt)
    network = Network()
    networkAct = NetworkAction(clt)

    # create
    res = instanceAct.createInstance(instance)
    instance.instance_id = res.get('InstanceId')

    # network ip
    res = networkAct.allocateEipAddress(network)
    print (res)
    network.allocation_id = res.get('AllocationId')

    res = networkAct.associateEipAddress(instance, network)

    # start
    res = instanceAct.startInstance(instance)


def get_instance():
    # insure there is only one instance
    instance = Instance()
    instanceAct = InstanceAction(clt)
    res = instanceAct.queryInstances()

    if res.get('TotalCount') != 1:
        print('Error: instance total count = %s, not 1, exit' % res.get('TotalCount'))
        sys.exit(1)

    ins_dic = res.get('instances').get('instance')[1]
    instance.instance_id = ins_dic.get('InstanceId')
    instance.status = ins_dic.get('Status')

    return instance


def get_network(instance):
    network = Network()
    networkAct = NetworkAction(clt)

    res = networkAct.queryEipAddresses(instance)

    if res.get('TotalCount') != 1:
        print('Error: network total count = %s, not 1, exit' % res.get('TotalCount'))
        sys.exit(1)

    net_dic = res.get('EipAddresses').get('EipAddress')[1]
    network.allocation_id = net_dic.get('AllocationId')

    return network


def delete_one_instance():
    networkAct = NetworkAction(clt)
    # instance
    instanceAct = InstanceAction(clt)
    instance = get_instance()
    if instance.status == 'Running':
        instanceAct.stopInstance(instance)

    for i in range(1,30):
        instance = get_instance()
        if instance.status == 'Stopped':
            break
    else:
        print('Error: failed to stop instance')


    network = get_network(instance)

    instanceAct.deleteInstance(instance)
    networkAct.releaseEipAddress(network)

if __name__ == '__main__':
    clt = initClient()




