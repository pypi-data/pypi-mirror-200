import datetime
from typing import List, Optional, Dict, Tuple, Union
from ..domain.entity import Entity
from .value_obj import (
    K3SNodeType,
    Status,
    UBool,
    UDate,
    UDict,
    UFloat,
    UInt,
    UStr
)



class Condition(Entity):
    def __init__(
        self,
        min_cpu_num: Optional[UInt] = UInt(1),
        max_cpu_num: Optional[UInt] = UInt(1),
        min_memory_size: Optional[UInt] = UInt(1),
        max_memory_size: Optional[UInt] = UInt(1),
        min_gpu_num: Optional[UInt] = None,
        max_gpu_num: Optional[UInt] = None,
        min_gpu_memory_size: Optional[UInt] = None,
        max_gpu_memory_size: Optional[UInt] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.min_cpu_num = min_cpu_num
        self.max_cpu_num = max_cpu_num
        self.min_memory_size = min_memory_size
        self.max_memory_size = max_memory_size
        self.min_gpu_num = min_gpu_num
        self.max_gpu_num = max_gpu_num
        self.min_gpu_memory_size = min_gpu_memory_size
        self.max_gpu_memory_size = max_gpu_memory_size



class DatapipeServerInfo(Entity):
    def __init__(
        self,
        id: UStr,
        secret: UStr,
        endpoint: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.secret = secret
        self.endpoint = endpoint



class DatapipeDataInfo(Entity):
    def __init__(
        self,
        bucket: UStr,
        remote_path: UStr,
        local_path: UStr,
        timeout: UInt = UInt(3),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.bucket = bucket
        self.remote_path = remote_path
        self.local_path = local_path
        self.timeout = timeout



class ClusterConfigData(Entity):
    def __init__(
        self,
        data_server: DatapipeServerInfo,
        data: List[DatapipeDataInfo],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.data_server = data_server
        self.data = data



class ClusterConfig(Entity):
    def __init__(
        self,
        cluster_name: UStr,
        region_id: UStr,
        config_data: Optional[ClusterConfigData] = None,
        entry_point: Optional[List[UStr]] = None,
        timeout: UInt = UInt(20),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_name = cluster_name
        self.region_id = region_id
        self.config_data = config_data
        self.entry_point = entry_point
        self.timeout = timeout



class BootstrapInfo(Entity):
    def __init__(
        self,
        cluster_config: ClusterConfig,
        template: UStr = UStr('normal'),
        platform: UStr = UStr('aliyun'),
        patch_setting: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.cluster_config = cluster_config
        self.template = template
        self.platform = platform
        self.patch_setting = patch_setting



class RandomTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        lengths: Optional[List[UInt]] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.lengths = lengths



class FileTemplateVariables(Entity):
    def __init__(
        self,
        variables: Optional[List[UStr]],
        path: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.path = path



class FilesTemplateVariables(Entity):
    def __init__(
        self,
        variables: List[UStr],
        paths: List[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.variables = variables
        self.paths = paths



class APIGatewayRequest(Entity):
    def __init__(
        self,
        service_name: UStr,
        method: UStr,
        ip: Optional[UStr] = None,
        port: Optional[UInt] = None,
        route: Optional[UStr] = None,
        action: Optional[UStr] = None,
        auth: Optional[UDict] = None,
        data: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.service_name = service_name
        self.method = method
        self.ip = ip
        self.port = port
        self.route = route
        self.action = action
        self.auth = auth
        self.data = data



class APIGatewayBlacklistItem(Entity):
    def __init__(
        self,
        ip: UStr,
        creation_time: UStr,
        limit_time: UInt,
        limit_reason: UStr,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.ip = ip
        self.creation_time = creation_time
        self.limit_time = limit_time
        self.limit_reason = limit_reason



class TaskRequest(Entity):
    def __init__(
        self,
        task_name: UStr,
        region_id: UStr,
        condition: Optional[Condition],
        git_url: Optional[UStr],
        git_branch: Optional[UStr],
        task_type: Optional[UStr] = UStr('cluster'),
        task_template: Optional[UStr] = None,
        task_env: Optional[UDict] = None,
        task_command: Optional[List[UStr]] = [UStr('sleep'),UStr('100000')],
        task_arg: Optional[List[UStr]] = None,
        task_working_dir: Optional[UStr] = None,
        task_image: Optional[UStr] = UStr('alpine:3.12'),
        task_start_time: Optional[UStr] = None,
        priority: UInt = UInt(3),
        amount: UInt = UInt(1),
        duration: Optional[UInt] = None,
        disk_size: Optional[UInt] = UInt(20),
        end_style: UStr = UStr('delete'),
        restart_policy: UStr = UStr('never'),
        timeout: UInt = UInt(500),
        cluster_name: Optional[UStr] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.task_name = task_name
        self.region_id = region_id
        self.condition = condition
        self.git_url = git_url
        self.git_branch = git_branch
        self.task_type = task_type
        self.task_template = task_template
        self.task_env = task_env
        self.task_command = task_command
        self.task_arg = task_arg
        self.task_working_dir = task_working_dir
        self.task_image = task_image
        self.task_start_time = task_start_time
        self.priority = priority
        self.amount = amount
        self.duration = duration
        self.disk_size = disk_size
        self.end_style = end_style
        self.restart_policy = restart_policy
        self.timeout = timeout
        self.cluster_name = cluster_name



class TaskDeleteRequest(Entity):
    def __init__(
        self,
        task_name: Optional[UStr],
        task_id: Optional[UStr],
        delay: Optional[UInt],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.task_name = task_name
        self.task_id = task_id
        self.delay = delay



class TaskDetail(Entity):
    def __init__(
        self,
        detail_id: UStr,
        ip: UStr,
        node_status: Optional[Status],
        job_status: Optional[Status],
        exception: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.detail_id = detail_id
        self.ip = ip
        self.node_status = node_status
        self.job_status = job_status
        self.exception = exception



class TaskItem(Entity):
    def __init__(
        self,
        request: Optional[TaskRequest],
        delete_request: Optional[TaskDeleteRequest],
        task_id: UStr,
        creation_time: UDate,
        status: Status,
        details: Optional[List[TaskDetail]],
        entry_time: Optional[UDate],
        exit_time: Optional[UDate],
        exception: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.request = request
        self.delete_request = delete_request
        self.task_id = task_id
        self.creation_time = creation_time
        self.status = status
        self.details = details
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.exception = exception



class NodeInventory(Entity):
    def __init__(
        self,
        node_type: UStr,
        amount: UInt,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.node_type = node_type
        self.amount = amount



class DNSInventory(Entity):
    def __init__(
        self,
        domain: UStr,
        subdomain: UStr,
        node_type: Optional[K3SNodeType],
        pod_name: Optional[UStr],
        namespace_name: Optional[UStr],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.domain = domain
        self.subdomain = subdomain
        self.node_type = node_type
        self.pod_name = pod_name
        self.namespace_name = namespace_name



class RecoverSetting(Entity):
    def __init__(
        self,
        node_inventory: Optional[List[NodeInventory]],
        dns_inventory: Optional[List[DNSInventory]],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.node_inventory = node_inventory
        self.dns_inventory = dns_inventory



class SearchRequest(Entity):
    def __init__(
        self,
        keyword: UStr,
        limit: UInt = UInt(5),
        timeout: UInt = UInt(300),
        request_id: Optional[UStr] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.keyword = keyword
        self.limit = limit
        self.timeout = timeout
        self.request_id = request_id
        self.others = others



class SearchResponse(Entity):
    def __init__(
        self,
        status: Status,
        exception: Optional[UStr] = None,
        result: Optional[UDict] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.status = status
        self.exception = exception
        self.result = result
        self.others = others



class SearchItem(Entity):
    def __init__(
        self,
        item_id: UStr,
        status: Status,
        exception: Optional[UStr] = None,
        request: Optional[SearchRequest] = None,
        response: Optional[SearchResponse] = None,
        entry_time: Optional[UDate] = None,
        exit_time: Optional[UDate] = None,
        create_time: Optional[UDate] = None,
        failure_times: UInt = UInt(0),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.item_id = item_id
        self.status = status
        self.exception = exception
        self.request = request
        self.response = response
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.create_time = create_time
        self.failure_times = failure_times



class ProxyInfo(Entity):
    def __init__(
        self,
        ip: UStr,
        port: UInt,
        protocol: UStr,
        auth: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.auth = auth



class InstanceUserSetting(Entity):
    def __init__(
        self,
        name: UStr,
        region_id: UStr,
        image_id: Optional[UStr],
        internet_pay_type: Optional[UStr],
        key_name: UStr,
        password: UStr = UStr('1234Abcd'),
        amount: UStr = UStr('1'),
        bandwidth_in: UInt = UInt(200),
        bandwidth_out: UInt = UInt(1),
        user_data: Optional[UStr] = None,
        disk_size: UInt = UInt(20),
        exclude_instance_types: List[UStr] = [],
        inner_connection: UBool = UBool(True),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.name = name
        self.region_id = region_id
        self.image_id = image_id
        self.internet_pay_type = internet_pay_type
        self.key_name = key_name
        self.password = password
        self.amount = amount
        self.bandwidth_in = bandwidth_in
        self.bandwidth_out = bandwidth_out
        self.user_data = user_data
        self.disk_size = disk_size
        self.exclude_instance_types = exclude_instance_types
        self.inner_connection = inner_connection



class InstanceCreationRequest(Entity):
    def __init__(
        self,
        instance_user_setting: InstanceUserSetting,
        condition: Condition,
        priority: UInt = UInt(3),
        timeout: UInt = UInt(400),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.instance_user_setting = instance_user_setting
        self.condition = condition
        self.priority = priority
        self.timeout = timeout



class InstanceInfo(Entity):
    def __init__(
        self,
        id: UStr,
        instance_type: UStr,
        create_time: UDate,
        name: UStr,
        hostname: UStr,
        pay_type: UStr,
        public_ip: List[UStr],
        private_ip: Optional[UStr],
        os_name: UStr,
        price: UFloat,
        image_id: UStr,
        region_id: UStr,
        zone_id: UStr,
        internet_pay_type: UStr,
        bandwidth_in: UStr,
        bandwidth_out: UStr,
        status: UStr,
        key_name: UStr,
        security_group_id: List[UStr],
        instance_expired_time: Optional[UStr],
        auto_release_time: Optional[UStr],
        _life_time: UInt = UInt(5),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.instance_type = instance_type
        self.create_time = create_time
        self.name = name
        self.hostname = hostname
        self.pay_type = pay_type
        self.public_ip = public_ip
        self.private_ip = private_ip
        self.os_name = os_name
        self.price = price
        self.image_id = image_id
        self.region_id = region_id
        self.zone_id = zone_id
        self.internet_pay_type = internet_pay_type
        self.bandwidth_in = bandwidth_in
        self.bandwidth_out = bandwidth_out
        self.status = status
        self.key_name = key_name
        self.security_group_id = security_group_id
        self.instance_expired_time = instance_expired_time
        self.auto_release_time = auto_release_time
        self._life_time = _life_time



class InstanceCreationItem(Entity):
    def __init__(
        self,
        id: UStr,
        instance_creation_request: Optional[InstanceCreationRequest],
        status: UStr,
        creation_time: UDate,
        details: Optional[List[InstanceInfo]] = None,
        entry_time: Optional[UDate] = None,
        exit_time: Optional[UDate] = None,
        exception: Optional[UStr] = None,
        _life_time: UStr = UStr('86400'),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.instance_creation_request = instance_creation_request
        self.status = status
        self.creation_time = creation_time
        self.details = details
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.exception = exception
        self._life_time = _life_time



class OpenaiChatMessage(Entity):
    def __init__(
        self,
        content: UStr,
        role: UStr = UStr('user'),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.content = content
        self.role = role



class OpenaiChatInput(Entity):
    def __init__(
        self,
        messages: List[OpenaiChatMessage],
        model: UStr = UStr('gpt-3.5-turbo'),
        temperature: UInt = UInt(1),
        top_p: UInt = UInt(1),
        n: UInt = UInt(1),
        stream: UBool = UBool(False),
        stop: Optional[UStr] = None,
        max_tokens: UInt = UInt(4000),
        presence_penalty: UFloat = UFloat(0),
        frequency_penalty: UFloat = UFloat(0),
        logit_bias: UDict = UDict({}),
        user: UStr = UStr('test'),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.messages = messages
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.n = n
        self.stream = stream
        self.stop = stop
        self.max_tokens = max_tokens
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.logit_bias = logit_bias
        self.user = user



class OpenaiChatUsage(Entity):
    def __init__(
        self,
        prompt_tokens: UInt,
        completion_tokens: UInt,
        total_tokens: UInt,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens



class OpenaiChatChoice(Entity):
    def __init__(
        self,
        message: OpenaiChatMessage,
        finish_reason: Optional[UStr],
        index: UInt,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.message = message
        self.finish_reason = finish_reason
        self.index = index



class OpenaiChatOutput(Entity):
    def __init__(
        self,
        id: UStr,
        object: UStr,
        created: UStr,
        model: UStr,
        usage: OpenaiChatUsage,
        choices: List[OpenaiChatChoice],
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.id = id
        self.object = object
        self.created = created
        self.model = model
        self.usage = usage
        self.choices = choices



class OpenaiRequest(Entity):
    def __init__(
        self,
        input: OpenaiChatInput,
        job_timeout: UInt = UInt(30),
        timeout: UInt = UInt(300),
        request_id: Optional[UStr] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.input = input
        self.job_timeout = job_timeout
        self.timeout = timeout
        self.request_id = request_id
        self.others = others



class OpenaiResponse(Entity):
    def __init__(
        self,
        status: Status,
        exception: Optional[UStr] = None,
        result: Optional[UDict] = None,
        others: Optional[UDict] = None,
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.status = status
        self.exception = exception
        self.result = result
        self.others = others



class OpenaiItem(Entity):
    def __init__(
        self,
        item_id: UStr,
        status: Status,
        exception: Optional[UStr] = None,
        request: Optional[OpenaiRequest] = None,
        response: Optional[OpenaiResponse] = None,
        entry_time: Optional[UDate] = None,
        exit_time: Optional[UDate] = None,
        create_time: Optional[UDate] = None,
        failure_times: UInt = UInt(0),
        **kwargs
    ) -> None:
        all_args=locals()
        del all_args['self']
        del all_args['__class__']
        del all_args['kwargs']
        super().__init__(**all_args)
        self.item_id = item_id
        self.status = status
        self.exception = exception
        self.request = request
        self.response = response
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.create_time = create_time
        self.failure_times = failure_times