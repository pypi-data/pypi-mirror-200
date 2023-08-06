from typing import List, Optional, Dict, Tuple, Union
from ..infrastructure.converter import Converter
from .entity import (
    APIGatewayBlacklistItem,
    APIGatewayRequest,
    BootstrapInfo,
    ClusterConfig,
    ClusterConfigData,
    Condition,
    DNSInventory,
    DatapipeDataInfo,
    DatapipeServerInfo,
    FileTemplateVariables,
    FilesTemplateVariables,
    InstanceCreationItem,
    InstanceCreationRequest,
    InstanceInfo,
    InstanceUserSetting,
    NodeInventory,
    OpenaiChatChoice,
    OpenaiChatInput,
    OpenaiChatMessage,
    OpenaiChatOutput,
    OpenaiChatUsage,
    OpenaiItem,
    OpenaiRequest,
    OpenaiResponse,
    ProxyInfo,
    RandomTemplateVariables,
    RecoverSetting,
    SearchItem,
    SearchRequest,
    SearchResponse,
    TaskDeleteRequest,
    TaskDetail,
    TaskItem,
    TaskRequest
)
from .do import (
    APIGatewayBlacklistItemDO,
    APIGatewayRequestDO,
    BootstrapInfoDO,
    ClusterConfigDO,
    ClusterConfigDataDO,
    ConditionDO,
    DNSInventoryDO,
    DatapipeDataInfoDO,
    DatapipeServerInfoDO,
    FileTemplateVariablesDO,
    FilesTemplateVariablesDO,
    InstanceCreationItemDO,
    InstanceCreationRequestDO,
    InstanceInfoDO,
    InstanceUserSettingDO,
    NodeInventoryDO,
    OpenaiChatChoiceDO,
    OpenaiChatInputDO,
    OpenaiChatMessageDO,
    OpenaiChatOutputDO,
    OpenaiChatUsageDO,
    OpenaiItemDO,
    OpenaiRequestDO,
    OpenaiResponseDO,
    ProxyInfoDO,
    RandomTemplateVariablesDO,
    RecoverSettingDO,
    SearchItemDO,
    SearchRequestDO,
    SearchResponseDO,
    TaskDeleteRequestDO,
    TaskDetailDO,
    TaskItemDO,
    TaskRequestDO
)
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



class ConditionConverter(Converter):
    def to_entity(self, do: ConditionDO):
        return Condition(
            min_cpu_num = None if do.min_cpu_num is None else UInt(do.min_cpu_num),
            max_cpu_num = None if do.max_cpu_num is None else UInt(do.max_cpu_num),
            min_memory_size = None if do.min_memory_size is None else UInt(do.min_memory_size),
            max_memory_size = None if do.max_memory_size is None else UInt(do.max_memory_size),
            min_gpu_num = None if do.min_gpu_num is None else UInt(do.min_gpu_num),
            max_gpu_num = None if do.max_gpu_num is None else UInt(do.max_gpu_num),
            min_gpu_memory_size = None if do.min_gpu_memory_size is None else UInt(do.min_gpu_memory_size),
            max_gpu_memory_size = None if do.max_gpu_memory_size is None else UInt(do.max_gpu_memory_size)
        )
    def to_do(self, x:Condition):
        return ConditionDO(
            min_cpu_num = None if x.min_cpu_num is None else x.min_cpu_num.get_value(),
            max_cpu_num = None if x.max_cpu_num is None else x.max_cpu_num.get_value(),
            min_memory_size = None if x.min_memory_size is None else x.min_memory_size.get_value(),
            max_memory_size = None if x.max_memory_size is None else x.max_memory_size.get_value(),
            min_gpu_num = None if x.min_gpu_num is None else x.min_gpu_num.get_value(),
            max_gpu_num = None if x.max_gpu_num is None else x.max_gpu_num.get_value(),
            min_gpu_memory_size = None if x.min_gpu_memory_size is None else x.min_gpu_memory_size.get_value(),
            max_gpu_memory_size = None if x.max_gpu_memory_size is None else x.max_gpu_memory_size.get_value()
        )
condition_converter=ConditionConverter()



class DatapipeServerInfoConverter(Converter):
    def to_entity(self, do: DatapipeServerInfoDO):
        return DatapipeServerInfo(
            id = UStr(do.id),
            secret = UStr(do.secret),
            endpoint = UStr(do.endpoint)
        )
    def to_do(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_converter=DatapipeServerInfoConverter()



class DatapipeDataInfoConverter(Converter):
    def to_entity(self, do: DatapipeDataInfoDO):
        return DatapipeDataInfo(
            bucket = UStr(do.bucket),
            remote_path = UStr(do.remote_path),
            local_path = UStr(do.local_path),
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_converter=DatapipeDataInfoConverter()



class ClusterConfigDataConverter(Converter):
    def to_entity(self, do: ClusterConfigDataDO):
        return ClusterConfigData(
            data_server = datapipe_server_info_converter.to_entity(do.data_server),
            data = [datapipe_data_info_converter.to_entity(m) for m in do.data]
        )
    def to_do(self, x:ClusterConfigData):
        return ClusterConfigDataDO(
            data_server = datapipe_server_info_converter.to_do(x.data_server),
            data = [datapipe_data_info_converter.to_do(m) for m in x.data]
        )
cluster_config_data_converter=ClusterConfigDataConverter()



class ClusterConfigConverter(Converter):
    def to_entity(self, do: ClusterConfigDO):
        return ClusterConfig(
            cluster_name = UStr(do.cluster_name),
            region_id = UStr(do.region_id),
            config_data = None if do.config_data is None else cluster_config_data_converter.to_entity(do.config_data),
            entry_point = None if do.entry_point is None else [UStr(m) for m in do.entry_point],
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:ClusterConfig):
        return ClusterConfigDO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_converter.to_do(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_converter=ClusterConfigConverter()



class BootstrapInfoConverter(Converter):
    def to_entity(self, do: BootstrapInfoDO):
        return BootstrapInfo(
            cluster_config = cluster_config_converter.to_entity(do.cluster_config),
            template = UStr(do.template),
            platform = UStr(do.platform),
            patch_setting = None if do.patch_setting is None else UDict(do.patch_setting)
        )
    def to_do(self, x:BootstrapInfo):
        return BootstrapInfoDO(
            cluster_config = cluster_config_converter.to_do(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_info_converter=BootstrapInfoConverter()



class RandomTemplateVariablesConverter(Converter):
    def to_entity(self, do: RandomTemplateVariablesDO):
        return RandomTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            lengths = None if do.lengths is None else [UInt(m) for m in do.lengths]
        )
    def to_do(self, x:RandomTemplateVariables):
        return RandomTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            lengths = None if x.lengths is None else [m.get_value() for m in x.lengths]
        )
random_template_variables_converter=RandomTemplateVariablesConverter()



class FileTemplateVariablesConverter(Converter):
    def to_entity(self, do: FileTemplateVariablesDO):
        return FileTemplateVariables(
            variables = None if do.variables is None else [UStr(m) for m in do.variables],
            path = UStr(do.path)
        )
    def to_do(self, x:FileTemplateVariables):
        return FileTemplateVariablesDO(
            variables = None if x.variables is None else [m.get_value() for m in x.variables],
            path = x.path.get_value()
        )
file_template_variables_converter=FileTemplateVariablesConverter()



class FilesTemplateVariablesConverter(Converter):
    def to_entity(self, do: FilesTemplateVariablesDO):
        return FilesTemplateVariables(
            variables = [UStr(m) for m in do.variables],
            paths = [UStr(m) for m in do.paths]
        )
    def to_do(self, x:FilesTemplateVariables):
        return FilesTemplateVariablesDO(
            variables = [m.get_value() for m in x.variables],
            paths = [m.get_value() for m in x.paths]
        )
files_template_variables_converter=FilesTemplateVariablesConverter()



class APIGatewayRequestConverter(Converter):
    def to_entity(self, do: APIGatewayRequestDO):
        return APIGatewayRequest(
            service_name = UStr(do.service_name),
            method = UStr(do.method),
            ip = None if do.ip is None else UStr(do.ip),
            port = None if do.port is None else UInt(do.port),
            route = None if do.route is None else UStr(do.route),
            action = None if do.action is None else UStr(do.action),
            auth = None if do.auth is None else UDict(do.auth),
            data = None if do.data is None else UDict(do.data)
        )
    def to_do(self, x:APIGatewayRequest):
        return APIGatewayRequestDO(
            service_name = x.service_name.get_value(),
            method = x.method.get_value(),
            ip = None if x.ip is None else x.ip.get_value(),
            port = None if x.port is None else x.port.get_value(),
            route = None if x.route is None else x.route.get_value(),
            action = None if x.action is None else x.action.get_value(),
            auth = None if x.auth is None else x.auth.get_value(),
            data = None if x.data is None else x.data.get_value()
        )
api_gateway_request_converter=APIGatewayRequestConverter()



class APIGatewayBlacklistItemConverter(Converter):
    def to_entity(self, do: APIGatewayBlacklistItemDO):
        return APIGatewayBlacklistItem(
            ip = UStr(do.ip),
            creation_time = UStr(do.creation_time),
            limit_time = UInt(do.limit_time),
            limit_reason = UStr(do.limit_reason)
        )
    def to_do(self, x:APIGatewayBlacklistItem):
        return APIGatewayBlacklistItemDO(
            ip = x.ip.get_value(),
            creation_time = x.creation_time.get_value(),
            limit_time = x.limit_time.get_value(),
            limit_reason = x.limit_reason.get_value()
        )
api_gateway_blacklist_item_converter=APIGatewayBlacklistItemConverter()



class TaskRequestConverter(Converter):
    def to_entity(self, do: TaskRequestDO):
        return TaskRequest(
            task_name = UStr(do.task_name),
            region_id = UStr(do.region_id),
            condition = None if do.condition is None else condition_converter.to_entity(do.condition),
            git_url = None if do.git_url is None else UStr(do.git_url),
            git_branch = None if do.git_branch is None else UStr(do.git_branch),
            task_type = None if do.task_type is None else UStr(do.task_type),
            task_template = None if do.task_template is None else UStr(do.task_template),
            task_env = None if do.task_env is None else UDict(do.task_env),
            task_command = None if do.task_command is None else [UStr(m) for m in do.task_command],
            task_arg = None if do.task_arg is None else [UStr(m) for m in do.task_arg],
            task_working_dir = None if do.task_working_dir is None else UStr(do.task_working_dir),
            task_image = None if do.task_image is None else UStr(do.task_image),
            task_start_time = None if do.task_start_time is None else UStr(do.task_start_time),
            priority = UInt(do.priority),
            amount = UInt(do.amount),
            duration = None if do.duration is None else UInt(do.duration),
            disk_size = None if do.disk_size is None else UInt(do.disk_size),
            end_style = UStr(do.end_style),
            restart_policy = UStr(do.restart_policy),
            timeout = UInt(do.timeout),
            cluster_name = None if do.cluster_name is None else UStr(do.cluster_name)
        )
    def to_do(self, x:TaskRequest):
        return TaskRequestDO(
            task_name = x.task_name.get_value(),
            region_id = x.region_id.get_value(),
            condition = None if x.condition is None else condition_converter.to_do(x.condition),
            git_url = None if x.git_url is None else x.git_url.get_value(),
            git_branch = None if x.git_branch is None else x.git_branch.get_value(),
            task_type = None if x.task_type is None else x.task_type.get_value(),
            task_template = None if x.task_template is None else x.task_template.get_value(),
            task_env = None if x.task_env is None else x.task_env.get_value(),
            task_command = None if x.task_command is None else [m.get_value() for m in x.task_command],
            task_arg = None if x.task_arg is None else [m.get_value() for m in x.task_arg],
            task_working_dir = None if x.task_working_dir is None else x.task_working_dir.get_value(),
            task_image = None if x.task_image is None else x.task_image.get_value(),
            task_start_time = None if x.task_start_time is None else x.task_start_time.get_value(),
            priority = x.priority.get_value(),
            amount = x.amount.get_value(),
            duration = None if x.duration is None else x.duration.get_value(),
            disk_size = None if x.disk_size is None else x.disk_size.get_value(),
            end_style = x.end_style.get_value(),
            restart_policy = x.restart_policy.get_value(),
            timeout = x.timeout.get_value(),
            cluster_name = None if x.cluster_name is None else x.cluster_name.get_value()
        )
task_request_converter=TaskRequestConverter()



class TaskDeleteRequestConverter(Converter):
    def to_entity(self, do: TaskDeleteRequestDO):
        return TaskDeleteRequest(
            task_name = None if do.task_name is None else UStr(do.task_name),
            task_id = None if do.task_id is None else UStr(do.task_id),
            delay = None if do.delay is None else UInt(do.delay)
        )
    def to_do(self, x:TaskDeleteRequest):
        return TaskDeleteRequestDO(
            task_name = None if x.task_name is None else x.task_name.get_value(),
            task_id = None if x.task_id is None else x.task_id.get_value(),
            delay = None if x.delay is None else x.delay.get_value()
        )
task_delete_request_converter=TaskDeleteRequestConverter()



class TaskDetailConverter(Converter):
    def to_entity(self, do: TaskDetailDO):
        return TaskDetail(
            detail_id = UStr(do.detail_id),
            ip = UStr(do.ip),
            node_status = None if do.node_status is None else Status(do.node_status),
            job_status = None if do.job_status is None else Status(do.job_status),
            exception = None if do.exception is None else UStr(do.exception)
        )
    def to_do(self, x:TaskDetail):
        return TaskDetailDO(
            detail_id = x.detail_id.get_value(),
            ip = x.ip.get_value(),
            node_status = None if x.node_status is None else x.node_status.get_value(),
            job_status = None if x.job_status is None else x.job_status.get_value(),
            exception = None if x.exception is None else x.exception.get_value()
        )
task_detail_converter=TaskDetailConverter()



class TaskItemConverter(Converter):
    def to_entity(self, do: TaskItemDO):
        return TaskItem(
            request = None if do.request is None else task_request_converter.to_entity(do.request),
            delete_request = None if do.delete_request is None else task_delete_request_converter.to_entity(do.delete_request),
            task_id = UStr(do.task_id),
            creation_time = UDate(do.creation_time),
            status = Status(do.status),
            details = None if do.details is None else [task_detail_converter.to_entity(m) for m in do.details],
            entry_time = None if do.entry_time is None else UDate(do.entry_time),
            exit_time = None if do.exit_time is None else UDate(do.exit_time),
            exception = None if do.exception is None else UStr(do.exception)
        )
    def to_do(self, x:TaskItem):
        return TaskItemDO(
            request = None if x.request is None else task_request_converter.to_do(x.request),
            delete_request = None if x.delete_request is None else task_delete_request_converter.to_do(x.delete_request),
            task_id = x.task_id.get_value(),
            creation_time = x.creation_time.get_value(),
            status = x.status.get_value(),
            details = None if x.details is None else [task_detail_converter.to_do(m) for m in x.details],
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            exception = None if x.exception is None else x.exception.get_value()
        )
task_item_converter=TaskItemConverter()



class NodeInventoryConverter(Converter):
    def to_entity(self, do: NodeInventoryDO):
        return NodeInventory(
            node_type = UStr(do.node_type),
            amount = UInt(do.amount)
        )
    def to_do(self, x:NodeInventory):
        return NodeInventoryDO(
            node_type = x.node_type.get_value(),
            amount = x.amount.get_value()
        )
node_inventory_converter=NodeInventoryConverter()



class DNSInventoryConverter(Converter):
    def to_entity(self, do: DNSInventoryDO):
        return DNSInventory(
            domain = UStr(do.domain),
            subdomain = UStr(do.subdomain),
            node_type = None if do.node_type is None else K3SNodeType(do.node_type),
            pod_name = None if do.pod_name is None else UStr(do.pod_name),
            namespace_name = None if do.namespace_name is None else UStr(do.namespace_name)
        )
    def to_do(self, x:DNSInventory):
        return DNSInventoryDO(
            domain = x.domain.get_value(),
            subdomain = x.subdomain.get_value(),
            node_type = None if x.node_type is None else x.node_type.get_value(),
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value()
        )
dns_inventory_converter=DNSInventoryConverter()



class RecoverSettingConverter(Converter):
    def to_entity(self, do: RecoverSettingDO):
        return RecoverSetting(
            node_inventory = None if do.node_inventory is None else [node_inventory_converter.to_entity(m) for m in do.node_inventory],
            dns_inventory = None if do.dns_inventory is None else [dns_inventory_converter.to_entity(m) for m in do.dns_inventory]
        )
    def to_do(self, x:RecoverSetting):
        return RecoverSettingDO(
            node_inventory = None if x.node_inventory is None else [node_inventory_converter.to_do(m) for m in x.node_inventory],
            dns_inventory = None if x.dns_inventory is None else [dns_inventory_converter.to_do(m) for m in x.dns_inventory]
        )
recover_setting_converter=RecoverSettingConverter()



class SearchRequestConverter(Converter):
    def to_entity(self, do: SearchRequestDO):
        return SearchRequest(
            keyword = UStr(do.keyword),
            limit = UInt(do.limit),
            timeout = UInt(do.timeout),
            request_id = None if do.request_id is None else UStr(do.request_id),
            others = None if do.others is None else UDict(do.others)
        )
    def to_do(self, x:SearchRequest):
        return SearchRequestDO(
            keyword = x.keyword.get_value(),
            limit = x.limit.get_value(),
            timeout = x.timeout.get_value(),
            request_id = None if x.request_id is None else x.request_id.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
search_request_converter=SearchRequestConverter()



class SearchResponseConverter(Converter):
    def to_entity(self, do: SearchResponseDO):
        return SearchResponse(
            status = Status(do.status),
            exception = None if do.exception is None else UStr(do.exception),
            result = None if do.result is None else UDict(do.result),
            others = None if do.others is None else UDict(do.others)
        )
    def to_do(self, x:SearchResponse):
        return SearchResponseDO(
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            result = None if x.result is None else x.result.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
search_response_converter=SearchResponseConverter()



class SearchItemConverter(Converter):
    def to_entity(self, do: SearchItemDO):
        return SearchItem(
            item_id = UStr(do.item_id),
            status = Status(do.status),
            exception = None if do.exception is None else UStr(do.exception),
            request = None if do.request is None else search_request_converter.to_entity(do.request),
            response = None if do.response is None else search_response_converter.to_entity(do.response),
            entry_time = None if do.entry_time is None else UDate(do.entry_time),
            exit_time = None if do.exit_time is None else UDate(do.exit_time),
            create_time = None if do.create_time is None else UDate(do.create_time),
            failure_times = UInt(do.failure_times)
        )
    def to_do(self, x:SearchItem):
        return SearchItemDO(
            item_id = x.item_id.get_value(),
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            request = None if x.request is None else search_request_converter.to_do(x.request),
            response = None if x.response is None else search_response_converter.to_do(x.response),
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            create_time = None if x.create_time is None else x.create_time.get_value(),
            failure_times = x.failure_times.get_value()
        )
search_item_converter=SearchItemConverter()



class ProxyInfoConverter(Converter):
    def to_entity(self, do: ProxyInfoDO):
        return ProxyInfo(
            ip = UStr(do.ip),
            port = UInt(do.port),
            protocol = UStr(do.protocol),
            auth = None if do.auth is None else UDict(do.auth)
        )
    def to_do(self, x:ProxyInfo):
        return ProxyInfoDO(
            ip = x.ip.get_value(),
            port = x.port.get_value(),
            protocol = x.protocol.get_value(),
            auth = None if x.auth is None else x.auth.get_value()
        )
proxy_info_converter=ProxyInfoConverter()



class InstanceUserSettingConverter(Converter):
    def to_entity(self, do: InstanceUserSettingDO):
        return InstanceUserSetting(
            name = UStr(do.name),
            region_id = UStr(do.region_id),
            image_id = None if do.image_id is None else UStr(do.image_id),
            internet_pay_type = None if do.internet_pay_type is None else UStr(do.internet_pay_type),
            key_name = UStr(do.key_name),
            password = UStr(do.password),
            amount = UStr(do.amount),
            bandwidth_in = UInt(do.bandwidth_in),
            bandwidth_out = UInt(do.bandwidth_out),
            user_data = None if do.user_data is None else UStr(do.user_data),
            disk_size = UInt(do.disk_size),
            exclude_instance_types = [UStr(m) for m in do.exclude_instance_types],
            inner_connection = UBool(do.inner_connection)
        )
    def to_do(self, x:InstanceUserSetting):
        return InstanceUserSettingDO(
            name = x.name.get_value(),
            region_id = x.region_id.get_value(),
            image_id = None if x.image_id is None else x.image_id.get_value(),
            internet_pay_type = None if x.internet_pay_type is None else x.internet_pay_type.get_value(),
            key_name = x.key_name.get_value(),
            password = x.password.get_value(),
            amount = x.amount.get_value(),
            bandwidth_in = x.bandwidth_in.get_value(),
            bandwidth_out = x.bandwidth_out.get_value(),
            user_data = None if x.user_data is None else x.user_data.get_value(),
            disk_size = x.disk_size.get_value(),
            exclude_instance_types = [m.get_value() for m in x.exclude_instance_types],
            inner_connection = x.inner_connection.get_value()
        )
instance_user_setting_converter=InstanceUserSettingConverter()



class InstanceCreationRequestConverter(Converter):
    def to_entity(self, do: InstanceCreationRequestDO):
        return InstanceCreationRequest(
            instance_user_setting = instance_user_setting_converter.to_entity(do.instance_user_setting),
            condition = condition_converter.to_entity(do.condition),
            priority = UInt(do.priority),
            timeout = UInt(do.timeout)
        )
    def to_do(self, x:InstanceCreationRequest):
        return InstanceCreationRequestDO(
            instance_user_setting = instance_user_setting_converter.to_do(x.instance_user_setting),
            condition = condition_converter.to_do(x.condition),
            priority = x.priority.get_value(),
            timeout = x.timeout.get_value()
        )
instance_creation_request_converter=InstanceCreationRequestConverter()



class InstanceInfoConverter(Converter):
    def to_entity(self, do: InstanceInfoDO):
        return InstanceInfo(
            id = UStr(do.id),
            instance_type = UStr(do.instance_type),
            create_time = UDate(do.create_time),
            name = UStr(do.name),
            hostname = UStr(do.hostname),
            pay_type = UStr(do.pay_type),
            public_ip = [UStr(m) for m in do.public_ip],
            private_ip = None if do.private_ip is None else UStr(do.private_ip),
            os_name = UStr(do.os_name),
            price = UFloat(do.price),
            image_id = UStr(do.image_id),
            region_id = UStr(do.region_id),
            zone_id = UStr(do.zone_id),
            internet_pay_type = UStr(do.internet_pay_type),
            bandwidth_in = UStr(do.bandwidth_in),
            bandwidth_out = UStr(do.bandwidth_out),
            status = UStr(do.status),
            key_name = UStr(do.key_name),
            security_group_id = [UStr(m) for m in do.security_group_id],
            instance_expired_time = None if do.instance_expired_time is None else UStr(do.instance_expired_time),
            auto_release_time = None if do.auto_release_time is None else UStr(do.auto_release_time),
            _life_time = UInt(do._life_time)
        )
    def to_do(self, x:InstanceInfo):
        return InstanceInfoDO(
            id = x.id.get_value(),
            instance_type = x.instance_type.get_value(),
            create_time = x.create_time.get_value(),
            name = x.name.get_value(),
            hostname = x.hostname.get_value(),
            pay_type = x.pay_type.get_value(),
            public_ip = [m.get_value() for m in x.public_ip],
            private_ip = None if x.private_ip is None else x.private_ip.get_value(),
            os_name = x.os_name.get_value(),
            price = x.price.get_value(),
            image_id = x.image_id.get_value(),
            region_id = x.region_id.get_value(),
            zone_id = x.zone_id.get_value(),
            internet_pay_type = x.internet_pay_type.get_value(),
            bandwidth_in = x.bandwidth_in.get_value(),
            bandwidth_out = x.bandwidth_out.get_value(),
            status = x.status.get_value(),
            key_name = x.key_name.get_value(),
            security_group_id = [m.get_value() for m in x.security_group_id],
            instance_expired_time = None if x.instance_expired_time is None else x.instance_expired_time.get_value(),
            auto_release_time = None if x.auto_release_time is None else x.auto_release_time.get_value(),
            _life_time = x._life_time.get_value()
        )
instance_info_converter=InstanceInfoConverter()



class InstanceCreationItemConverter(Converter):
    def to_entity(self, do: InstanceCreationItemDO):
        return InstanceCreationItem(
            id = UStr(do.id),
            instance_creation_request = None if do.instance_creation_request is None else instance_creation_request_converter.to_entity(do.instance_creation_request),
            status = UStr(do.status),
            creation_time = UDate(do.creation_time),
            details = None if do.details is None else [instance_info_converter.to_entity(m) for m in do.details],
            entry_time = None if do.entry_time is None else UDate(do.entry_time),
            exit_time = None if do.exit_time is None else UDate(do.exit_time),
            exception = None if do.exception is None else UStr(do.exception),
            _life_time = UStr(do._life_time)
        )
    def to_do(self, x:InstanceCreationItem):
        return InstanceCreationItemDO(
            id = x.id.get_value(),
            instance_creation_request = None if x.instance_creation_request is None else instance_creation_request_converter.to_do(x.instance_creation_request),
            status = x.status.get_value(),
            creation_time = x.creation_time.get_value(),
            details = None if x.details is None else [instance_info_converter.to_do(m) for m in x.details],
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            _life_time = x._life_time.get_value()
        )
instance_creation_item_converter=InstanceCreationItemConverter()



class OpenaiChatMessageConverter(Converter):
    def to_entity(self, do: OpenaiChatMessageDO):
        return OpenaiChatMessage(
            content = UStr(do.content),
            role = UStr(do.role)
        )
    def to_do(self, x:OpenaiChatMessage):
        return OpenaiChatMessageDO(
            content = x.content.get_value(),
            role = x.role.get_value()
        )
openai_chat_message_converter=OpenaiChatMessageConverter()



class OpenaiChatInputConverter(Converter):
    def to_entity(self, do: OpenaiChatInputDO):
        return OpenaiChatInput(
            messages = [openai_chat_message_converter.to_entity(m) for m in do.messages],
            model = UStr(do.model),
            temperature = UInt(do.temperature),
            top_p = UInt(do.top_p),
            n = UInt(do.n),
            stream = UBool(do.stream),
            stop = None if do.stop is None else UStr(do.stop),
            max_tokens = UInt(do.max_tokens),
            presence_penalty = UFloat(do.presence_penalty),
            frequency_penalty = UFloat(do.frequency_penalty),
            logit_bias = UDict(do.logit_bias),
            user = UStr(do.user)
        )
    def to_do(self, x:OpenaiChatInput):
        return OpenaiChatInputDO(
            messages = [openai_chat_message_converter.to_do(m) for m in x.messages],
            model = x.model.get_value(),
            temperature = x.temperature.get_value(),
            top_p = x.top_p.get_value(),
            n = x.n.get_value(),
            stream = x.stream.get_value(),
            stop = None if x.stop is None else x.stop.get_value(),
            max_tokens = x.max_tokens.get_value(),
            presence_penalty = x.presence_penalty.get_value(),
            frequency_penalty = x.frequency_penalty.get_value(),
            logit_bias = x.logit_bias.get_value(),
            user = x.user.get_value()
        )
openai_chat_input_converter=OpenaiChatInputConverter()



class OpenaiChatUsageConverter(Converter):
    def to_entity(self, do: OpenaiChatUsageDO):
        return OpenaiChatUsage(
            prompt_tokens = UInt(do.prompt_tokens),
            completion_tokens = UInt(do.completion_tokens),
            total_tokens = UInt(do.total_tokens)
        )
    def to_do(self, x:OpenaiChatUsage):
        return OpenaiChatUsageDO(
            prompt_tokens = x.prompt_tokens.get_value(),
            completion_tokens = x.completion_tokens.get_value(),
            total_tokens = x.total_tokens.get_value()
        )
openai_chat_usage_converter=OpenaiChatUsageConverter()



class OpenaiChatChoiceConverter(Converter):
    def to_entity(self, do: OpenaiChatChoiceDO):
        return OpenaiChatChoice(
            message = openai_chat_message_converter.to_entity(do.message),
            finish_reason = None if do.finish_reason is None else UStr(do.finish_reason),
            index = UInt(do.index)
        )
    def to_do(self, x:OpenaiChatChoice):
        return OpenaiChatChoiceDO(
            message = openai_chat_message_converter.to_do(x.message),
            finish_reason = None if x.finish_reason is None else x.finish_reason.get_value(),
            index = x.index.get_value()
        )
openai_chat_choice_converter=OpenaiChatChoiceConverter()



class OpenaiChatOutputConverter(Converter):
    def to_entity(self, do: OpenaiChatOutputDO):
        return OpenaiChatOutput(
            id = UStr(do.id),
            object = UStr(do.object),
            created = UStr(do.created),
            model = UStr(do.model),
            usage = openai_chat_usage_converter.to_entity(do.usage),
            choices = [openai_chat_choice_converter.to_entity(m) for m in do.choices]
        )
    def to_do(self, x:OpenaiChatOutput):
        return OpenaiChatOutputDO(
            id = x.id.get_value(),
            object = x.object.get_value(),
            created = x.created.get_value(),
            model = x.model.get_value(),
            usage = openai_chat_usage_converter.to_do(x.usage),
            choices = [openai_chat_choice_converter.to_do(m) for m in x.choices]
        )
openai_chat_output_converter=OpenaiChatOutputConverter()



class OpenaiRequestConverter(Converter):
    def to_entity(self, do: OpenaiRequestDO):
        return OpenaiRequest(
            input = openai_chat_input_converter.to_entity(do.input),
            timeout = UInt(do.timeout),
            request_id = None if do.request_id is None else UStr(do.request_id),
            others = None if do.others is None else UDict(do.others)
        )
    def to_do(self, x:OpenaiRequest):
        return OpenaiRequestDO(
            input = openai_chat_input_converter.to_do(x.input),
            timeout = x.timeout.get_value(),
            request_id = None if x.request_id is None else x.request_id.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
openai_request_converter=OpenaiRequestConverter()



class OpenaiResponseConverter(Converter):
    def to_entity(self, do: OpenaiResponseDO):
        return OpenaiResponse(
            status = Status(do.status),
            exception = None if do.exception is None else UStr(do.exception),
            result = None if do.result is None else UDict(do.result),
            others = None if do.others is None else UDict(do.others)
        )
    def to_do(self, x:OpenaiResponse):
        return OpenaiResponseDO(
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            result = None if x.result is None else x.result.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
openai_response_converter=OpenaiResponseConverter()



class OpenaiItemConverter(Converter):
    def to_entity(self, do: OpenaiItemDO):
        return OpenaiItem(
            item_id = UStr(do.item_id),
            status = Status(do.status),
            exception = None if do.exception is None else UStr(do.exception),
            request = None if do.request is None else search_request_converter.to_entity(do.request),
            response = None if do.response is None else search_response_converter.to_entity(do.response),
            entry_time = None if do.entry_time is None else UDate(do.entry_time),
            exit_time = None if do.exit_time is None else UDate(do.exit_time),
            create_time = None if do.create_time is None else UDate(do.create_time),
            failure_times = UInt(do.failure_times)
        )
    def to_do(self, x:OpenaiItem):
        return OpenaiItemDO(
            item_id = x.item_id.get_value(),
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            request = None if x.request is None else search_request_converter.to_do(x.request),
            response = None if x.response is None else search_response_converter.to_do(x.response),
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            create_time = None if x.create_time is None else x.create_time.get_value(),
            failure_times = x.failure_times.get_value()
        )
openai_item_converter=OpenaiItemConverter()
