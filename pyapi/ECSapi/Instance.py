from aliyunsdkecs.request.v20140526 import CreateInstanceRequest, StartInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest, StopInstanceRequest


class Instance(object):
    def __init__(self, aliyunclient):
        self.client = aliyunclient
        self.instance_id = None

    def CreateInstance(self):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.set_ImageId('centos_7_3_64_40G_base_20170322.vhd')
        request.set_Password('cnp200@HW')
        request.set_InstanceType('ecs.xn4.small')
        result = self.client.do_action_with_exception(request)

        self.instance_id = result.get('InstanceId')
        return result

    def StartInstance(self):
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(self.instance_id)
        result = self.client.do_action_with_exception(request)
        return result

    def StopInstance(self):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(self.instance_id)
        result = self.client.do_action_with_exception(request)
        return result

    def deleteInstance(self):
        #  StopInstance(self.instance_id)
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_InstanceId(self.instance_id)
        result = self.client.do_action_with_exception(request)
        return result
