from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
from aliyunsdkecs.request.v20140526 import AllocateEipAddressRequest
from aliyunsdkecs.request.v20140526 import AssociateEipAddressRequest
from aliyunsdkecs.request.v20140526 import ReleaseEipAddressRequest


class NetworkAction(object):
    def __init__(self, aliyunclient):
        self.client = aliyunclient

    #     貌似不可用
    # def AllocatePublicIpAddress(self, instance_id):
    #     request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
    #     request.set_InstanceId(instance_id)
    #     result = self.client.do_action_with_exception(request)
    #     print (result)

    def AllocateEipAddress(self, network):
        request = AllocateEipAddressRequest.AllocateEipAddressRequest()
        request.set_InternetChargeType(network.charge_type)
        result = self.client.do_action_with_exception(request)
        return result

    def AssociateEipAddress(self, instance, network):
        request = AssociateEipAddressRequest.AssociateEipAddressRequest()
        request.set_AllocationId(network.allocation_id)
        request.set_InstanceId(instance.instance_id)
        result = self.client.do_action_with_exception(request)
        return result

    def ReleaseEipAddress(self, allocation_id):
        request = ReleaseEipAddressRequest.ReleaseEipAddressRequest()
        request.set_AllocationId(allocation_id)
        result = self.client.do_action_with_exception(request)
        return result