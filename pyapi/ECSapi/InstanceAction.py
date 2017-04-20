from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest, DescribeInstancesRequest

class InstanceAction(object):
    def __init__(self, aliyunclient):
        self.client = aliyunclient

    def createInstance(self, instance):
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.set_ImageId(instance.image_id)
        request.set_Password(instance.password)
        request.set_InstanceType(instance.instance_type)

        result = self.client.do_action_with_exception(request)
        return result

    def startInstance(self, instance):
        request = StartInstanceRequest.StartInstanceRequest()
        request.set_InstanceId(instance.instance_id)
        result = self.client.do_action_with_exception(request)
        return result

    def queryInstances(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        result = self.client.do_action_with_exception(request)
        return result

    def stopInstance(self, instance):
        request = StopInstanceRequest.StopInstanceRequest()
        request.set_InstanceId(instance.instance_id)
        result = self.client.do_action_with_exception(request)
        return result

    def deleteInstance(self, instance):
        # instance status should be stopped
        request = DeleteInstanceRequest.DeleteInstanceRequest()
        request.set_InstanceId(instance.instance_id)
        result = self.client.do_action_with_exception(request)
        return result
