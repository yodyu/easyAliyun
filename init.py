from aliyunsdkcore import client
from ConfigParser import ConfigParser


def initClient():
    with open('config.ini') as f:
        cfp = ConfigParser()
        cfp.read(f)

    key_id = cfp.get('KEY', 'Access_key_id')
    key_secret = cfp.get('KEY', 'Access_key_secret')
    region = cfp.get('ECS', 'region')

    clt = client.AcsClient(key_id, key_secret, region)
    return clt

clt = initClient()
