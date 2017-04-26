import sys
import os
import argparse

from aliyunsdkcore import client
from ConfigParser import ConfigParser

from pyapi.ECSapi.InstanceAction import InstanceAction
from entity.ECSentity.Instance import Instance
from pyapi.ECSapi.NetworkAction import NetworkAction
from entity.ECSentity.Network import Network

#import script.ssAction

record_file = 'record.json'


def initClient():
    conf = 'config.ini'
    if not os.path.exists(conf):
        print 'Err: file config.ini not exists'
    cfp = ConfigParser()
    cfp.read(conf)

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
    #res = instanceAct.createInstance(instance)
    #print res
    res = '{"InstanceId":"i-bp16tljwj6370h208yma","RequestId":"FB282AD4-8E9E-4668-B85B-7AEE27A6E7C6"}'
    print res
    instance.instance_id = eval(res).get('InstanceId')

    # network ip
    res = networkAct.allocateEipAddress(network)
    print (res)
    network.allocation_id = eval(res).get('AllocationId')

    res = networkAct.associateEipAddress(instance, network)
    print (res)
    # start
    res = instanceAct.startInstance(instance)
    print (res)

def get_instance():
    # insure there is only one instance
    instance = Instance()
    instanceAct = InstanceAction(clt)
    res = instanceAct.queryInstances()

    if res.get('TotalCount') != 1:
        print('Error: instance total count = %s, not 1, exit' % res.get('TotalCount'))
        sys.exit(1)

    ins_dic = eval(res).get('instances').get('instance')[1]
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

    net_dic = eval(res).get('EipAddresses').get('EipAddress')[1]
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

    parser = argparse.ArgumentParser()
    parser.add_argument('--action', help='start or delete a ECS instance', default='start')

    args = parser.parse_args()
    action = args.action
    if action == 'start':
        start_one_instance()
        script.ssAction.Shadowsocks().start_ss_server()
    elif action == 'stop':
        delete_one_instance()






