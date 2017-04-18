from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest, \
    AllocateEipAddressRequest
from aliyunsdkecs.request.v20140526 import AssociateEipAddressRequest, \
    ReleaseEipAddressRequest

class Network(object):
    def __init__(self, aliyunclient):
        self.client = aliyunclient
        self.allocation_id = None
        
    def AllocatePublicIpAddress(self, instance_id):
        request = AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
        request.set_InstanceId(instance_id)
        result = self.client.do_action_with_exception(request)
        print result
    
    
    def AllocateEipAddress(self):
        request = AllocateEipAddressRequest.AllocateEipAddressRequest()
        request.set_InternetChargeType('PayByTraffic')
        result = self.client.do_action_with_exception(request)
        print result
    
    
    def AssociateEipAddress(self, instance_id):
        request = AssociateEipAddressRequest.AssociateEipAddressRequest()
        request.set_AllocationId(self.allocation_id)
        request.set_InstanceId(instance_id)
        result = self.client.do_action_with_exception(request)
        print result
    
    
    def ReleaseEipAddress(self, allocation_id):
        request = ReleaseEipAddressRequest.ReleaseEipAddressRequest()
        request.set_AllocationId(allocation_id)
        result = self.client.do_action_with_exception(request)
        print result    