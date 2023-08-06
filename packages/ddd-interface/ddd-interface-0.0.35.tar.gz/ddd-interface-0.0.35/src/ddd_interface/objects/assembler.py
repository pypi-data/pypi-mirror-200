from typing import List, Optional, Dict, Tuple, Union
from ..application.assembler import Assembler
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
from .dto import (
    APIGatewayBlacklistItemDTO,
    APIGatewayRequestDTO,
    BootstrapInfoDTO,
    ClusterConfigDTO,
    ClusterConfigDataDTO,
    ConditionDTO,
    DNSInventoryDTO,
    DatapipeDataInfoDTO,
    DatapipeServerInfoDTO,
    FileTemplateVariablesDTO,
    FilesTemplateVariablesDTO,
    InstanceCreationItemDTO,
    InstanceCreationRequestDTO,
    InstanceInfoDTO,
    InstanceUserSettingDTO,
    NodeInventoryDTO,
    OpenaiChatChoiceDTO,
    OpenaiChatInputDTO,
    OpenaiChatMessageDTO,
    OpenaiChatOutputDTO,
    OpenaiChatUsageDTO,
    OpenaiItemDTO,
    OpenaiRequestDTO,
    OpenaiResponseDTO,
    ProxyInfoDTO,
    RandomTemplateVariablesDTO,
    RecoverSettingDTO,
    SearchItemDTO,
    SearchRequestDTO,
    SearchResponseDTO,
    TaskDeleteRequestDTO,
    TaskDetailDTO,
    TaskItemDTO,
    TaskRequestDTO
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



class ConditionAssembler(Assembler):
    def to_entity(self, dto: ConditionDTO):
        return Condition(
            min_cpu_num = None if dto.min_cpu_num is None else UInt(dto.min_cpu_num),
            max_cpu_num = None if dto.max_cpu_num is None else UInt(dto.max_cpu_num),
            min_memory_size = None if dto.min_memory_size is None else UInt(dto.min_memory_size),
            max_memory_size = None if dto.max_memory_size is None else UInt(dto.max_memory_size),
            min_gpu_num = None if dto.min_gpu_num is None else UInt(dto.min_gpu_num),
            max_gpu_num = None if dto.max_gpu_num is None else UInt(dto.max_gpu_num),
            min_gpu_memory_size = None if dto.min_gpu_memory_size is None else UInt(dto.min_gpu_memory_size),
            max_gpu_memory_size = None if dto.max_gpu_memory_size is None else UInt(dto.max_gpu_memory_size)
        )
    def to_dto(self, x:Condition):
        return ConditionDTO(
            min_cpu_num = None if x.min_cpu_num is None else x.min_cpu_num.get_value(),
            max_cpu_num = None if x.max_cpu_num is None else x.max_cpu_num.get_value(),
            min_memory_size = None if x.min_memory_size is None else x.min_memory_size.get_value(),
            max_memory_size = None if x.max_memory_size is None else x.max_memory_size.get_value(),
            min_gpu_num = None if x.min_gpu_num is None else x.min_gpu_num.get_value(),
            max_gpu_num = None if x.max_gpu_num is None else x.max_gpu_num.get_value(),
            min_gpu_memory_size = None if x.min_gpu_memory_size is None else x.min_gpu_memory_size.get_value(),
            max_gpu_memory_size = None if x.max_gpu_memory_size is None else x.max_gpu_memory_size.get_value()
        )
condition_assembler=ConditionAssembler()



class DatapipeServerInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeServerInfoDTO):
        return DatapipeServerInfo(
            id = UStr(dto.id),
            secret = UStr(dto.secret),
            endpoint = UStr(dto.endpoint)
        )
    def to_dto(self, x:DatapipeServerInfo):
        return DatapipeServerInfoDTO(
            id = x.id.get_value(),
            secret = x.secret.get_value(),
            endpoint = x.endpoint.get_value()
        )
datapipe_server_info_assembler=DatapipeServerInfoAssembler()



class DatapipeDataInfoAssembler(Assembler):
    def to_entity(self, dto: DatapipeDataInfoDTO):
        return DatapipeDataInfo(
            bucket = UStr(dto.bucket),
            remote_path = UStr(dto.remote_path),
            local_path = UStr(dto.local_path),
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:DatapipeDataInfo):
        return DatapipeDataInfoDTO(
            bucket = x.bucket.get_value(),
            remote_path = x.remote_path.get_value(),
            local_path = x.local_path.get_value(),
            timeout = x.timeout.get_value()
        )
datapipe_data_info_assembler=DatapipeDataInfoAssembler()



class ClusterConfigDataAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDataDTO):
        return ClusterConfigData(
            data_server = datapipe_server_info_assembler.to_entity(dto.data_server),
            data = [datapipe_data_info_assembler.to_entity(m) for m in dto.data]
        )
    def to_dto(self, x:ClusterConfigData):
        return ClusterConfigDataDTO(
            data_server = datapipe_server_info_assembler.to_dto(x.data_server),
            data = [datapipe_data_info_assembler.to_dto(m) for m in x.data]
        )
cluster_config_data_assembler=ClusterConfigDataAssembler()



class ClusterConfigAssembler(Assembler):
    def to_entity(self, dto: ClusterConfigDTO):
        return ClusterConfig(
            cluster_name = UStr(dto.cluster_name),
            region_id = UStr(dto.region_id),
            config_data = None if dto.config_data is None else cluster_config_data_assembler.to_entity(dto.config_data),
            entry_point = None if dto.entry_point is None else [UStr(m) for m in dto.entry_point],
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:ClusterConfig):
        return ClusterConfigDTO(
            cluster_name = x.cluster_name.get_value(),
            region_id = x.region_id.get_value(),
            config_data = None if x.config_data is None else cluster_config_data_assembler.to_dto(x.config_data),
            entry_point = None if x.entry_point is None else [m.get_value() for m in x.entry_point],
            timeout = x.timeout.get_value()
        )
cluster_config_assembler=ClusterConfigAssembler()



class BootstrapInfoAssembler(Assembler):
    def to_entity(self, dto: BootstrapInfoDTO):
        return BootstrapInfo(
            cluster_config = cluster_config_assembler.to_entity(dto.cluster_config),
            template = UStr(dto.template),
            platform = UStr(dto.platform),
            patch_setting = None if dto.patch_setting is None else UDict(dto.patch_setting)
        )
    def to_dto(self, x:BootstrapInfo):
        return BootstrapInfoDTO(
            cluster_config = cluster_config_assembler.to_dto(x.cluster_config),
            template = x.template.get_value(),
            platform = x.platform.get_value(),
            patch_setting = None if x.patch_setting is None else x.patch_setting.get_value()
        )
bootstrap_info_assembler=BootstrapInfoAssembler()



class RandomTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: RandomTemplateVariablesDTO):
        return RandomTemplateVariables(
            variables = [UStr(m) for m in dto.variables],
            lengths = None if dto.lengths is None else [UInt(m) for m in dto.lengths]
        )
    def to_dto(self, x:RandomTemplateVariables):
        return RandomTemplateVariablesDTO(
            variables = [m.get_value() for m in x.variables],
            lengths = None if x.lengths is None else [m.get_value() for m in x.lengths]
        )
random_template_variables_assembler=RandomTemplateVariablesAssembler()



class FileTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: FileTemplateVariablesDTO):
        return FileTemplateVariables(
            variables = None if dto.variables is None else [UStr(m) for m in dto.variables],
            path = UStr(dto.path)
        )
    def to_dto(self, x:FileTemplateVariables):
        return FileTemplateVariablesDTO(
            variables = None if x.variables is None else [m.get_value() for m in x.variables],
            path = x.path.get_value()
        )
file_template_variables_assembler=FileTemplateVariablesAssembler()



class FilesTemplateVariablesAssembler(Assembler):
    def to_entity(self, dto: FilesTemplateVariablesDTO):
        return FilesTemplateVariables(
            variables = [UStr(m) for m in dto.variables],
            paths = [UStr(m) for m in dto.paths]
        )
    def to_dto(self, x:FilesTemplateVariables):
        return FilesTemplateVariablesDTO(
            variables = [m.get_value() for m in x.variables],
            paths = [m.get_value() for m in x.paths]
        )
files_template_variables_assembler=FilesTemplateVariablesAssembler()



class APIGatewayRequestAssembler(Assembler):
    def to_entity(self, dto: APIGatewayRequestDTO):
        return APIGatewayRequest(
            service_name = UStr(dto.service_name),
            method = UStr(dto.method),
            ip = None if dto.ip is None else UStr(dto.ip),
            port = None if dto.port is None else UInt(dto.port),
            route = None if dto.route is None else UStr(dto.route),
            action = None if dto.action is None else UStr(dto.action),
            auth = None if dto.auth is None else UDict(dto.auth),
            data = None if dto.data is None else UDict(dto.data)
        )
    def to_dto(self, x:APIGatewayRequest):
        return APIGatewayRequestDTO(
            service_name = x.service_name.get_value(),
            method = x.method.get_value(),
            ip = None if x.ip is None else x.ip.get_value(),
            port = None if x.port is None else x.port.get_value(),
            route = None if x.route is None else x.route.get_value(),
            action = None if x.action is None else x.action.get_value(),
            auth = None if x.auth is None else x.auth.get_value(),
            data = None if x.data is None else x.data.get_value()
        )
api_gateway_request_assembler=APIGatewayRequestAssembler()



class APIGatewayBlacklistItemAssembler(Assembler):
    def to_entity(self, dto: APIGatewayBlacklistItemDTO):
        return APIGatewayBlacklistItem(
            ip = UStr(dto.ip),
            creation_time = UStr(dto.creation_time),
            limit_time = UInt(dto.limit_time),
            limit_reason = UStr(dto.limit_reason)
        )
    def to_dto(self, x:APIGatewayBlacklistItem):
        return APIGatewayBlacklistItemDTO(
            ip = x.ip.get_value(),
            creation_time = x.creation_time.get_value(),
            limit_time = x.limit_time.get_value(),
            limit_reason = x.limit_reason.get_value()
        )
api_gateway_blacklist_item_assembler=APIGatewayBlacklistItemAssembler()



class TaskRequestAssembler(Assembler):
    def to_entity(self, dto: TaskRequestDTO):
        return TaskRequest(
            task_name = UStr(dto.task_name),
            region_id = UStr(dto.region_id),
            condition = None if dto.condition is None else condition_assembler.to_entity(dto.condition),
            git_url = None if dto.git_url is None else UStr(dto.git_url),
            git_branch = None if dto.git_branch is None else UStr(dto.git_branch),
            task_type = None if dto.task_type is None else UStr(dto.task_type),
            task_template = None if dto.task_template is None else UStr(dto.task_template),
            task_env = None if dto.task_env is None else UDict(dto.task_env),
            task_command = None if dto.task_command is None else [UStr(m) for m in dto.task_command],
            task_arg = None if dto.task_arg is None else [UStr(m) for m in dto.task_arg],
            task_working_dir = None if dto.task_working_dir is None else UStr(dto.task_working_dir),
            task_image = None if dto.task_image is None else UStr(dto.task_image),
            task_start_time = None if dto.task_start_time is None else UStr(dto.task_start_time),
            priority = UInt(dto.priority),
            amount = UInt(dto.amount),
            duration = None if dto.duration is None else UInt(dto.duration),
            disk_size = None if dto.disk_size is None else UInt(dto.disk_size),
            end_style = UStr(dto.end_style),
            restart_policy = UStr(dto.restart_policy),
            timeout = UInt(dto.timeout),
            cluster_name = None if dto.cluster_name is None else UStr(dto.cluster_name)
        )
    def to_dto(self, x:TaskRequest):
        return TaskRequestDTO(
            task_name = x.task_name.get_value(),
            region_id = x.region_id.get_value(),
            condition = None if x.condition is None else condition_assembler.to_dto(x.condition),
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
task_request_assembler=TaskRequestAssembler()



class TaskDeleteRequestAssembler(Assembler):
    def to_entity(self, dto: TaskDeleteRequestDTO):
        return TaskDeleteRequest(
            task_name = None if dto.task_name is None else UStr(dto.task_name),
            task_id = None if dto.task_id is None else UStr(dto.task_id),
            delay = None if dto.delay is None else UInt(dto.delay)
        )
    def to_dto(self, x:TaskDeleteRequest):
        return TaskDeleteRequestDTO(
            task_name = None if x.task_name is None else x.task_name.get_value(),
            task_id = None if x.task_id is None else x.task_id.get_value(),
            delay = None if x.delay is None else x.delay.get_value()
        )
task_delete_request_assembler=TaskDeleteRequestAssembler()



class TaskDetailAssembler(Assembler):
    def to_entity(self, dto: TaskDetailDTO):
        return TaskDetail(
            detail_id = UStr(dto.detail_id),
            ip = UStr(dto.ip),
            node_status = None if dto.node_status is None else Status(dto.node_status),
            job_status = None if dto.job_status is None else Status(dto.job_status),
            exception = None if dto.exception is None else UStr(dto.exception)
        )
    def to_dto(self, x:TaskDetail):
        return TaskDetailDTO(
            detail_id = x.detail_id.get_value(),
            ip = x.ip.get_value(),
            node_status = None if x.node_status is None else x.node_status.get_value(),
            job_status = None if x.job_status is None else x.job_status.get_value(),
            exception = None if x.exception is None else x.exception.get_value()
        )
task_detail_assembler=TaskDetailAssembler()



class TaskItemAssembler(Assembler):
    def to_entity(self, dto: TaskItemDTO):
        return TaskItem(
            request = None if dto.request is None else task_request_assembler.to_entity(dto.request),
            delete_request = None if dto.delete_request is None else task_delete_request_assembler.to_entity(dto.delete_request),
            task_id = UStr(dto.task_id),
            creation_time = UDate(dto.creation_time),
            status = Status(dto.status),
            details = None if dto.details is None else [task_detail_assembler.to_entity(m) for m in dto.details],
            entry_time = None if dto.entry_time is None else UDate(dto.entry_time),
            exit_time = None if dto.exit_time is None else UDate(dto.exit_time),
            exception = None if dto.exception is None else UStr(dto.exception)
        )
    def to_dto(self, x:TaskItem):
        return TaskItemDTO(
            request = None if x.request is None else task_request_assembler.to_dto(x.request),
            delete_request = None if x.delete_request is None else task_delete_request_assembler.to_dto(x.delete_request),
            task_id = x.task_id.get_value(),
            creation_time = x.creation_time.get_value(),
            status = x.status.get_value(),
            details = None if x.details is None else [task_detail_assembler.to_dto(m) for m in x.details],
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            exception = None if x.exception is None else x.exception.get_value()
        )
task_item_assembler=TaskItemAssembler()



class NodeInventoryAssembler(Assembler):
    def to_entity(self, dto: NodeInventoryDTO):
        return NodeInventory(
            node_type = UStr(dto.node_type),
            amount = UInt(dto.amount)
        )
    def to_dto(self, x:NodeInventory):
        return NodeInventoryDTO(
            node_type = x.node_type.get_value(),
            amount = x.amount.get_value()
        )
node_inventory_assembler=NodeInventoryAssembler()



class DNSInventoryAssembler(Assembler):
    def to_entity(self, dto: DNSInventoryDTO):
        return DNSInventory(
            domain = UStr(dto.domain),
            subdomain = UStr(dto.subdomain),
            node_type = None if dto.node_type is None else K3SNodeType(dto.node_type),
            pod_name = None if dto.pod_name is None else UStr(dto.pod_name),
            namespace_name = None if dto.namespace_name is None else UStr(dto.namespace_name)
        )
    def to_dto(self, x:DNSInventory):
        return DNSInventoryDTO(
            domain = x.domain.get_value(),
            subdomain = x.subdomain.get_value(),
            node_type = None if x.node_type is None else x.node_type.get_value(),
            pod_name = None if x.pod_name is None else x.pod_name.get_value(),
            namespace_name = None if x.namespace_name is None else x.namespace_name.get_value()
        )
dns_inventory_assembler=DNSInventoryAssembler()



class RecoverSettingAssembler(Assembler):
    def to_entity(self, dto: RecoverSettingDTO):
        return RecoverSetting(
            node_inventory = None if dto.node_inventory is None else [node_inventory_assembler.to_entity(m) for m in dto.node_inventory],
            dns_inventory = None if dto.dns_inventory is None else [dns_inventory_assembler.to_entity(m) for m in dto.dns_inventory]
        )
    def to_dto(self, x:RecoverSetting):
        return RecoverSettingDTO(
            node_inventory = None if x.node_inventory is None else [node_inventory_assembler.to_dto(m) for m in x.node_inventory],
            dns_inventory = None if x.dns_inventory is None else [dns_inventory_assembler.to_dto(m) for m in x.dns_inventory]
        )
recover_setting_assembler=RecoverSettingAssembler()



class SearchRequestAssembler(Assembler):
    def to_entity(self, dto: SearchRequestDTO):
        return SearchRequest(
            keyword = UStr(dto.keyword),
            limit = UInt(dto.limit),
            timeout = UInt(dto.timeout),
            request_id = None if dto.request_id is None else UStr(dto.request_id),
            others = None if dto.others is None else UDict(dto.others)
        )
    def to_dto(self, x:SearchRequest):
        return SearchRequestDTO(
            keyword = x.keyword.get_value(),
            limit = x.limit.get_value(),
            timeout = x.timeout.get_value(),
            request_id = None if x.request_id is None else x.request_id.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
search_request_assembler=SearchRequestAssembler()



class SearchResponseAssembler(Assembler):
    def to_entity(self, dto: SearchResponseDTO):
        return SearchResponse(
            status = Status(dto.status),
            exception = None if dto.exception is None else UStr(dto.exception),
            result = None if dto.result is None else UDict(dto.result),
            others = None if dto.others is None else UDict(dto.others)
        )
    def to_dto(self, x:SearchResponse):
        return SearchResponseDTO(
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            result = None if x.result is None else x.result.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
search_response_assembler=SearchResponseAssembler()



class SearchItemAssembler(Assembler):
    def to_entity(self, dto: SearchItemDTO):
        return SearchItem(
            item_id = UStr(dto.item_id),
            status = Status(dto.status),
            exception = None if dto.exception is None else UStr(dto.exception),
            request = None if dto.request is None else search_request_assembler.to_entity(dto.request),
            response = None if dto.response is None else search_response_assembler.to_entity(dto.response),
            entry_time = None if dto.entry_time is None else UDate(dto.entry_time),
            exit_time = None if dto.exit_time is None else UDate(dto.exit_time),
            create_time = None if dto.create_time is None else UDate(dto.create_time),
            failure_times = UInt(dto.failure_times)
        )
    def to_dto(self, x:SearchItem):
        return SearchItemDTO(
            item_id = x.item_id.get_value(),
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            request = None if x.request is None else search_request_assembler.to_dto(x.request),
            response = None if x.response is None else search_response_assembler.to_dto(x.response),
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            create_time = None if x.create_time is None else x.create_time.get_value(),
            failure_times = x.failure_times.get_value()
        )
search_item_assembler=SearchItemAssembler()



class ProxyInfoAssembler(Assembler):
    def to_entity(self, dto: ProxyInfoDTO):
        return ProxyInfo(
            ip = UStr(dto.ip),
            port = UInt(dto.port),
            protocol = UStr(dto.protocol),
            auth = None if dto.auth is None else UDict(dto.auth)
        )
    def to_dto(self, x:ProxyInfo):
        return ProxyInfoDTO(
            ip = x.ip.get_value(),
            port = x.port.get_value(),
            protocol = x.protocol.get_value(),
            auth = None if x.auth is None else x.auth.get_value()
        )
proxy_info_assembler=ProxyInfoAssembler()



class InstanceUserSettingAssembler(Assembler):
    def to_entity(self, dto: InstanceUserSettingDTO):
        return InstanceUserSetting(
            name = UStr(dto.name),
            region_id = UStr(dto.region_id),
            image_id = None if dto.image_id is None else UStr(dto.image_id),
            internet_pay_type = None if dto.internet_pay_type is None else UStr(dto.internet_pay_type),
            key_name = UStr(dto.key_name),
            password = UStr(dto.password),
            amount = UStr(dto.amount),
            bandwidth_in = UInt(dto.bandwidth_in),
            bandwidth_out = UInt(dto.bandwidth_out),
            user_data = None if dto.user_data is None else UStr(dto.user_data),
            disk_size = UInt(dto.disk_size),
            exclude_instance_types = [UStr(m) for m in dto.exclude_instance_types],
            inner_connection = UBool(dto.inner_connection)
        )
    def to_dto(self, x:InstanceUserSetting):
        return InstanceUserSettingDTO(
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
instance_user_setting_assembler=InstanceUserSettingAssembler()



class InstanceCreationRequestAssembler(Assembler):
    def to_entity(self, dto: InstanceCreationRequestDTO):
        return InstanceCreationRequest(
            instance_user_setting = instance_user_setting_assembler.to_entity(dto.instance_user_setting),
            condition = condition_assembler.to_entity(dto.condition),
            priority = UInt(dto.priority),
            timeout = UInt(dto.timeout)
        )
    def to_dto(self, x:InstanceCreationRequest):
        return InstanceCreationRequestDTO(
            instance_user_setting = instance_user_setting_assembler.to_dto(x.instance_user_setting),
            condition = condition_assembler.to_dto(x.condition),
            priority = x.priority.get_value(),
            timeout = x.timeout.get_value()
        )
instance_creation_request_assembler=InstanceCreationRequestAssembler()



class InstanceInfoAssembler(Assembler):
    def to_entity(self, dto: InstanceInfoDTO):
        return InstanceInfo(
            id = UStr(dto.id),
            instance_type = UStr(dto.instance_type),
            create_time = UDate(dto.create_time),
            name = UStr(dto.name),
            hostname = UStr(dto.hostname),
            pay_type = UStr(dto.pay_type),
            public_ip = [UStr(m) for m in dto.public_ip],
            private_ip = None if dto.private_ip is None else UStr(dto.private_ip),
            os_name = UStr(dto.os_name),
            price = UFloat(dto.price),
            image_id = UStr(dto.image_id),
            region_id = UStr(dto.region_id),
            zone_id = UStr(dto.zone_id),
            internet_pay_type = UStr(dto.internet_pay_type),
            bandwidth_in = UStr(dto.bandwidth_in),
            bandwidth_out = UStr(dto.bandwidth_out),
            status = UStr(dto.status),
            key_name = UStr(dto.key_name),
            security_group_id = [UStr(m) for m in dto.security_group_id],
            instance_expired_time = None if dto.instance_expired_time is None else UStr(dto.instance_expired_time),
            auto_release_time = None if dto.auto_release_time is None else UStr(dto.auto_release_time),
            _life_time = UInt(dto._life_time)
        )
    def to_dto(self, x:InstanceInfo):
        return InstanceInfoDTO(
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
instance_info_assembler=InstanceInfoAssembler()



class InstanceCreationItemAssembler(Assembler):
    def to_entity(self, dto: InstanceCreationItemDTO):
        return InstanceCreationItem(
            id = UStr(dto.id),
            instance_creation_request = None if dto.instance_creation_request is None else instance_creation_request_assembler.to_entity(dto.instance_creation_request),
            status = UStr(dto.status),
            creation_time = UDate(dto.creation_time),
            details = None if dto.details is None else [instance_info_assembler.to_entity(m) for m in dto.details],
            entry_time = None if dto.entry_time is None else UDate(dto.entry_time),
            exit_time = None if dto.exit_time is None else UDate(dto.exit_time),
            exception = None if dto.exception is None else UStr(dto.exception),
            _life_time = UStr(dto._life_time)
        )
    def to_dto(self, x:InstanceCreationItem):
        return InstanceCreationItemDTO(
            id = x.id.get_value(),
            instance_creation_request = None if x.instance_creation_request is None else instance_creation_request_assembler.to_dto(x.instance_creation_request),
            status = x.status.get_value(),
            creation_time = x.creation_time.get_value(),
            details = None if x.details is None else [instance_info_assembler.to_dto(m) for m in x.details],
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            _life_time = x._life_time.get_value()
        )
instance_creation_item_assembler=InstanceCreationItemAssembler()



class OpenaiChatMessageAssembler(Assembler):
    def to_entity(self, dto: OpenaiChatMessageDTO):
        return OpenaiChatMessage(
            content = UStr(dto.content),
            role = UStr(dto.role)
        )
    def to_dto(self, x:OpenaiChatMessage):
        return OpenaiChatMessageDTO(
            content = x.content.get_value(),
            role = x.role.get_value()
        )
openai_chat_message_assembler=OpenaiChatMessageAssembler()



class OpenaiChatInputAssembler(Assembler):
    def to_entity(self, dto: OpenaiChatInputDTO):
        return OpenaiChatInput(
            messages = [openai_chat_message_assembler.to_entity(m) for m in dto.messages],
            model = UStr(dto.model),
            temperature = UInt(dto.temperature),
            top_p = UInt(dto.top_p),
            n = UInt(dto.n),
            stream = UBool(dto.stream),
            stop = None if dto.stop is None else UStr(dto.stop),
            max_tokens = UInt(dto.max_tokens),
            presence_penalty = UFloat(dto.presence_penalty),
            frequency_penalty = UFloat(dto.frequency_penalty),
            logit_bias = UDict(dto.logit_bias),
            user = UStr(dto.user)
        )
    def to_dto(self, x:OpenaiChatInput):
        return OpenaiChatInputDTO(
            messages = [openai_chat_message_assembler.to_dto(m) for m in x.messages],
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
openai_chat_input_assembler=OpenaiChatInputAssembler()



class OpenaiChatUsageAssembler(Assembler):
    def to_entity(self, dto: OpenaiChatUsageDTO):
        return OpenaiChatUsage(
            prompt_tokens = UInt(dto.prompt_tokens),
            completion_tokens = UInt(dto.completion_tokens),
            total_tokens = UInt(dto.total_tokens)
        )
    def to_dto(self, x:OpenaiChatUsage):
        return OpenaiChatUsageDTO(
            prompt_tokens = x.prompt_tokens.get_value(),
            completion_tokens = x.completion_tokens.get_value(),
            total_tokens = x.total_tokens.get_value()
        )
openai_chat_usage_assembler=OpenaiChatUsageAssembler()



class OpenaiChatChoiceAssembler(Assembler):
    def to_entity(self, dto: OpenaiChatChoiceDTO):
        return OpenaiChatChoice(
            message = openai_chat_message_assembler.to_entity(dto.message),
            finish_reason = None if dto.finish_reason is None else UStr(dto.finish_reason),
            index = UInt(dto.index)
        )
    def to_dto(self, x:OpenaiChatChoice):
        return OpenaiChatChoiceDTO(
            message = openai_chat_message_assembler.to_dto(x.message),
            finish_reason = None if x.finish_reason is None else x.finish_reason.get_value(),
            index = x.index.get_value()
        )
openai_chat_choice_assembler=OpenaiChatChoiceAssembler()



class OpenaiChatOutputAssembler(Assembler):
    def to_entity(self, dto: OpenaiChatOutputDTO):
        return OpenaiChatOutput(
            id = UStr(dto.id),
            object = UStr(dto.object),
            created = UStr(dto.created),
            model = UStr(dto.model),
            usage = openai_chat_usage_assembler.to_entity(dto.usage),
            choices = [openai_chat_choice_assembler.to_entity(m) for m in dto.choices]
        )
    def to_dto(self, x:OpenaiChatOutput):
        return OpenaiChatOutputDTO(
            id = x.id.get_value(),
            object = x.object.get_value(),
            created = x.created.get_value(),
            model = x.model.get_value(),
            usage = openai_chat_usage_assembler.to_dto(x.usage),
            choices = [openai_chat_choice_assembler.to_dto(m) for m in x.choices]
        )
openai_chat_output_assembler=OpenaiChatOutputAssembler()



class OpenaiRequestAssembler(Assembler):
    def to_entity(self, dto: OpenaiRequestDTO):
        return OpenaiRequest(
            input = openai_chat_input_assembler.to_entity(dto.input),
            job_timeout = UInt(dto.job_timeout),
            timeout = UInt(dto.timeout),
            request_id = None if dto.request_id is None else UStr(dto.request_id),
            others = None if dto.others is None else UDict(dto.others)
        )
    def to_dto(self, x:OpenaiRequest):
        return OpenaiRequestDTO(
            input = openai_chat_input_assembler.to_dto(x.input),
            job_timeout = x.job_timeout.get_value(),
            timeout = x.timeout.get_value(),
            request_id = None if x.request_id is None else x.request_id.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
openai_request_assembler=OpenaiRequestAssembler()



class OpenaiResponseAssembler(Assembler):
    def to_entity(self, dto: OpenaiResponseDTO):
        return OpenaiResponse(
            status = Status(dto.status),
            exception = None if dto.exception is None else UStr(dto.exception),
            result = None if dto.result is None else UDict(dto.result),
            others = None if dto.others is None else UDict(dto.others)
        )
    def to_dto(self, x:OpenaiResponse):
        return OpenaiResponseDTO(
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            result = None if x.result is None else x.result.get_value(),
            others = None if x.others is None else x.others.get_value()
        )
openai_response_assembler=OpenaiResponseAssembler()



class OpenaiItemAssembler(Assembler):
    def to_entity(self, dto: OpenaiItemDTO):
        return OpenaiItem(
            item_id = UStr(dto.item_id),
            status = Status(dto.status),
            exception = None if dto.exception is None else UStr(dto.exception),
            request = None if dto.request is None else openai_request_assembler.to_entity(dto.request),
            response = None if dto.response is None else openai_response_assembler.to_entity(dto.response),
            entry_time = None if dto.entry_time is None else UDate(dto.entry_time),
            exit_time = None if dto.exit_time is None else UDate(dto.exit_time),
            create_time = None if dto.create_time is None else UDate(dto.create_time),
            failure_times = UInt(dto.failure_times)
        )
    def to_dto(self, x:OpenaiItem):
        return OpenaiItemDTO(
            item_id = x.item_id.get_value(),
            status = x.status.get_value(),
            exception = None if x.exception is None else x.exception.get_value(),
            request = None if x.request is None else openai_request_assembler.to_dto(x.request),
            response = None if x.response is None else openai_response_assembler.to_dto(x.response),
            entry_time = None if x.entry_time is None else x.entry_time.get_value(),
            exit_time = None if x.exit_time is None else x.exit_time.get_value(),
            create_time = None if x.create_time is None else x.create_time.get_value(),
            failure_times = x.failure_times.get_value()
        )
openai_item_assembler=OpenaiItemAssembler()
