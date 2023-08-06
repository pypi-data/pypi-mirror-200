import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import constructs as _constructs_77d1e7e8
from ..ec2 import (
    FlowLogFormat as _FlowLogFormat_b7c2ba34,
    ITransitGateway as _ITransitGateway_25936657,
    ITransitGatewayAttachment as _ITransitGatewayAttachment_64da8ffd,
    TransitGatewayProps as _TransitGatewayProps_10a60d21,
)
from ..ram import ISharedPrincipal as _ISharedPrincipal_9cde791b


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.AddSpokeNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class AddSpokeNetworkProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union["FlowLogOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048409c4bedb08ed8edc9dda9cec65cb4087822a3dcae95d57c194d4e0613116)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "FlowLogOptions"]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "FlowLogOptions"]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddSpokeNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FlowLogOptions",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions],
    name_mapping={
        "destination": "destination",
        "log_format": "logFormat",
        "max_aggregation_interval": "maxAggregationInterval",
        "traffic_type": "trafficType",
        "log_format_definition": "logFormatDefinition",
    },
)
class FlowLogOptions(_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions):
    def __init__(
        self,
        *,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
        log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    ) -> None:
        '''
        :param destination: Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3 Default: FlowLogDestinationType.toCloudWatchLogs()
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. If multiple fields are specified, they will be separated by spaces. For full control over the literal log format string, pass a single field constructed with ``LogFormat.custom()``. See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records Default: - default log format is used.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record. Default: FlowLogMaxAggregationInterval.TEN_MINUTES
        :param traffic_type: The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic. Default: ALL
        :param log_format_definition: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61356c6c988a747170b0fff518aeff55bb37140b2f2bb3a8395a7676df11d939)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
            check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
            check_type(argname="argument log_format_definition", value=log_format_definition, expected_type=type_hints["log_format_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if log_format is not None:
            self._values["log_format"] = log_format
        if max_aggregation_interval is not None:
            self._values["max_aggregation_interval"] = max_aggregation_interval
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type
        if log_format_definition is not None:
            self._values["log_format_definition"] = log_format_definition

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination]:
        '''Specifies the type of destination to which the flow log data is to be published.

        Flow log data can be published to CloudWatch Logs or Amazon S3

        :default: FlowLogDestinationType.toCloudWatchLogs()
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination], result)

    @builtins.property
    def log_format(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.LogFormat]]:
        '''The fields to include in the flow log record, in the order in which they should appear.

        If multiple fields are specified, they will be separated by spaces. For full control over the literal log format
        string, pass a single field constructed with ``LogFormat.custom()``.

        See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records

        :default: - default log format is used.
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.LogFormat]], result)

    @builtins.property
    def max_aggregation_interval(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :default: FlowLogMaxAggregationInterval.TEN_MINUTES
        '''
        result = self._values.get("max_aggregation_interval")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval], result)

    @builtins.property
    def traffic_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType]:
        '''The type of traffic to log.

        You can log traffic that the resource accepts or rejects, or all traffic.

        :default: ALL
        '''
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType], result)

    @builtins.property
    def log_format_definition(self) -> typing.Optional[_FlowLogFormat_b7c2ba34]:
        result = self._values.get("log_format_definition")
        return typing.cast(typing.Optional[_FlowLogFormat_b7c2ba34], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FourTierNetwork(
    _aws_cdk_aws_ec2_ceddda9d.Vpc,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetwork",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param nat_gateway_provider: 
        :param nat_gateways: 
        :param nat_gateway_subnets: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b54dda1f6044b8b90a294f4af2c53fd512620a5e619adafd6d687a35f35dc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            nat_gateway_provider=nat_gateway_provider,
            nat_gateways=nat_gateways,
            nat_gateway_subnets=nat_gateway_subnets,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addVpcFlowLog")
    def add_vpc_flow_log(
        self,
        id: builtins.str,
        *,
        log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.FlowLog:
        '''
        :param id: -
        :param log_format_definition: 
        :param destination: Specifies the type of destination to which the flow log data is to be published. Flow log data can be published to CloudWatch Logs or Amazon S3 Default: FlowLogDestinationType.toCloudWatchLogs()
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. If multiple fields are specified, they will be separated by spaces. For full control over the literal log format string, pass a single field constructed with ``LogFormat.custom()``. See https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-log-records Default: - default log format is used.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record. Default: FlowLogMaxAggregationInterval.TEN_MINUTES
        :param traffic_type: The type of traffic to log. You can log traffic that the resource accepts or rejects, or all traffic. Default: ALL
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb697f4884edaa9946bcf623d36e26bbc15cba6a321ac50f29f26b8fdef42b2a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = FlowLogOptions(
            log_format_definition=log_format_definition,
            destination=destination,
            log_format=log_format,
            max_aggregation_interval=max_aggregation_interval,
            traffic_type=traffic_type,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLog, jsii.invoke(self, "addVpcFlowLog", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="defaultInstanceTenancy")
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], jsii.get(self, "defaultInstanceTenancy"))

    @builtins.property
    @jsii.member(jsii_name="enableDnsHostnames")
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDnsHostnames"))

    @builtins.property
    @jsii.member(jsii_name="enableDnsSupport")
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableDnsSupport"))

    @builtins.property
    @jsii.member(jsii_name="maxAzs")
    def max_azs(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxAzs"))

    @builtins.property
    @jsii.member(jsii_name="vpcName")
    def vpc_name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcName"))


class FourTierNetworkHub(
    FourTierNetwork,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkHub",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        sharing: typing.Optional[typing.Union["FourTierNetworkShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param sharing: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ace25eaf0b1bdeb7c9833547b92ca28254092d01db9ebc9696fce2260b43d9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkHubProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            sharing=sharing,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addSpoke")
    def add_spoke(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "FourTierNetworkSpoke":
        '''
        :param scope: -
        :param id: -
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b427eb756711b9be0d1724b92283f7b8b658149d02d0860ddfaae4ca009451a6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddSpokeNetworkProps(
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
        )

        return typing.cast("FourTierNetworkSpoke", jsii.invoke(self, "addSpoke", [scope, id, props]))

    @jsii.member(jsii_name="enableTransitGateway")
    def enable_transit_gateway(
        self,
        *,
        amazon_side_asn: typing.Optional[jsii.Number] = None,
        auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
        cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_route_table_association: typing.Optional[builtins.bool] = None,
        default_route_table_id: typing.Optional[builtins.str] = None,
        default_route_table_propagation: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        multicast_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        vpn_ecmp_support: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> _ITransitGateway_25936657:
        '''
        :param amazon_side_asn: 
        :param auto_accept_shared_attachments: 
        :param cidr_blocks: 
        :param default_route_table_association: 
        :param default_route_table_id: 
        :param default_route_table_propagation: 
        :param description: 
        :param dns_support: 
        :param multicast_support: 
        :param name: 
        :param vpn_ecmp_support: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        props = _TransitGatewayProps_10a60d21(
            amazon_side_asn=amazon_side_asn,
            auto_accept_shared_attachments=auto_accept_shared_attachments,
            cidr_blocks=cidr_blocks,
            default_route_table_association=default_route_table_association,
            default_route_table_id=default_route_table_id,
            default_route_table_propagation=default_route_table_propagation,
            description=description,
            dns_support=dns_support,
            multicast_support=multicast_support,
            name=name,
            vpn_ecmp_support=vpn_ecmp_support,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast(_ITransitGateway_25936657, jsii.invoke(self, "enableTransitGateway", [props]))

    @builtins.property
    @jsii.member(jsii_name="sharing")
    def sharing(self) -> "FourTierNetworkShareProperties":
        return typing.cast("FourTierNetworkShareProperties", jsii.get(self, "sharing"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> typing.Optional[_ITransitGateway_25936657]:
        return typing.cast(typing.Optional[_ITransitGateway_25936657], jsii.get(self, "transitGateway"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkHubProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "sharing": "sharing",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkHubProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        sharing: typing.Optional[typing.Union["FourTierNetworkShareProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param sharing: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if isinstance(sharing, dict):
            sharing = FourTierNetworkShareProperties(**sharing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1e120a9a594264d414d234533b6a6694a2e18b423a355c83676f0931ec9be90)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument sharing", value=sharing, expected_type=type_hints["sharing"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if sharing is not None:
            self._values["sharing"] = sharing
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sharing(self) -> typing.Optional["FourTierNetworkShareProperties"]:
        result = self._values.get("sharing")
        return typing.cast(typing.Optional["FourTierNetworkShareProperties"], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkHubProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "nat_gateway_provider": "natGatewayProvider",
        "nat_gateways": "natGateways",
        "nat_gateway_subnets": "natGatewaySubnets",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkProps:
    def __init__(
        self,
        *,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
        nat_gateways: typing.Optional[jsii.Number] = None,
        nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param nat_gateway_provider: 
        :param nat_gateways: 
        :param nat_gateway_subnets: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if isinstance(nat_gateway_subnets, dict):
            nat_gateway_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**nat_gateway_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9f1c80c97704155becd995a7614b98797ff3dcfedcb6c14a3c861d8ffa5d99)
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument nat_gateway_provider", value=nat_gateway_provider, expected_type=type_hints["nat_gateway_provider"])
            check_type(argname="argument nat_gateways", value=nat_gateways, expected_type=type_hints["nat_gateways"])
            check_type(argname="argument nat_gateway_subnets", value=nat_gateway_subnets, expected_type=type_hints["nat_gateway_subnets"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if nat_gateway_provider is not None:
            self._values["nat_gateway_provider"] = nat_gateway_provider
        if nat_gateways is not None:
            self._values["nat_gateways"] = nat_gateways
        if nat_gateway_subnets is not None:
            self._values["nat_gateway_subnets"] = nat_gateway_subnets
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider]:
        result = self._values.get("nat_gateway_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider], result)

    @builtins.property
    def nat_gateways(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("nat_gateways")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def nat_gateway_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        result = self._values.get("nat_gateway_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkShareProperties",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "auto_add_accounts": "autoAddAccounts",
        "pricipals": "pricipals",
    },
)
class FourTierNetworkShareProperties:
    def __init__(
        self,
        *,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_add_accounts: typing.Optional[builtins.bool] = None,
        pricipals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> None:
        '''
        :param allow_external_principals: 
        :param auto_add_accounts: 
        :param pricipals: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba6d7153869452d0a1b515208e0e7160367751697fbee237f3d54f9f8411a28)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument auto_add_accounts", value=auto_add_accounts, expected_type=type_hints["auto_add_accounts"])
            check_type(argname="argument pricipals", value=pricipals, expected_type=type_hints["pricipals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if auto_add_accounts is not None:
            self._values["auto_add_accounts"] = auto_add_accounts
        if pricipals is not None:
            self._values["pricipals"] = pricipals

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_add_accounts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_add_accounts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pricipals(self) -> typing.Optional[typing.List[_ISharedPrincipal_9cde791b]]:
        result = self._values.get("pricipals")
        return typing.cast(typing.Optional[typing.List[_ISharedPrincipal_9cde791b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkShareProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FourTierNetworkSpoke(
    FourTierNetwork,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkSpoke",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        transit_gateway: _ITransitGateway_25936657,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param transit_gateway: 
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fc919bd6ebf5b551769cb4313098a0e49891c0d5e533cf159dc7f303b04473)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FourTierNetworkSpokeProps(
            transit_gateway=transit_gateway,
            availability_zones=availability_zones,
            cidr=cidr,
            default_instance_tenancy=default_instance_tenancy,
            enable_dns_hostnames=enable_dns_hostnames,
            enable_dns_support=enable_dns_support,
            flow_logs=flow_logs,
            gateway_endpoints=gateway_endpoints,
            max_azs=max_azs,
            vpc_name=vpc_name,
            vpn_connections=vpn_connections,
            vpn_gateway=vpn_gateway,
            vpn_gateway_asn=vpn_gateway_asn,
            vpn_route_propagation=vpn_route_propagation,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachment")
    def transit_gateway_attachment(self) -> _ITransitGatewayAttachment_64da8ffd:
        return typing.cast(_ITransitGatewayAttachment_64da8ffd, jsii.get(self, "transitGatewayAttachment"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.FourTierNetworkSpokeProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "transit_gateway": "transitGateway",
        "availability_zones": "availabilityZones",
        "cidr": "cidr",
        "default_instance_tenancy": "defaultInstanceTenancy",
        "enable_dns_hostnames": "enableDnsHostnames",
        "enable_dns_support": "enableDnsSupport",
        "flow_logs": "flowLogs",
        "gateway_endpoints": "gatewayEndpoints",
        "max_azs": "maxAzs",
        "vpc_name": "vpcName",
        "vpn_connections": "vpnConnections",
        "vpn_gateway": "vpnGateway",
        "vpn_gateway_asn": "vpnGatewayAsn",
        "vpn_route_propagation": "vpnRoutePropagation",
    },
)
class FourTierNetworkSpokeProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        transit_gateway: _ITransitGateway_25936657,
        availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
        cidr: typing.Optional[builtins.str] = None,
        default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
        enable_dns_hostnames: typing.Optional[builtins.bool] = None,
        enable_dns_support: typing.Optional[builtins.bool] = None,
        flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        max_azs: typing.Optional[jsii.Number] = None,
        vpc_name: typing.Optional[builtins.str] = None,
        vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_gateway: typing.Optional[builtins.bool] = None,
        vpn_gateway_asn: typing.Optional[jsii.Number] = None,
        vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param transit_gateway: 
        :param availability_zones: 
        :param cidr: 
        :param default_instance_tenancy: 
        :param enable_dns_hostnames: 
        :param enable_dns_support: 
        :param flow_logs: 
        :param gateway_endpoints: 
        :param max_azs: 
        :param vpc_name: 
        :param vpn_connections: 
        :param vpn_gateway: 
        :param vpn_gateway_asn: 
        :param vpn_route_propagation: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f20b71c01dce683a9711971685bfd423a84bb51b3ae70144ed170d14b6b7721)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument availability_zones", value=availability_zones, expected_type=type_hints["availability_zones"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument default_instance_tenancy", value=default_instance_tenancy, expected_type=type_hints["default_instance_tenancy"])
            check_type(argname="argument enable_dns_hostnames", value=enable_dns_hostnames, expected_type=type_hints["enable_dns_hostnames"])
            check_type(argname="argument enable_dns_support", value=enable_dns_support, expected_type=type_hints["enable_dns_support"])
            check_type(argname="argument flow_logs", value=flow_logs, expected_type=type_hints["flow_logs"])
            check_type(argname="argument gateway_endpoints", value=gateway_endpoints, expected_type=type_hints["gateway_endpoints"])
            check_type(argname="argument max_azs", value=max_azs, expected_type=type_hints["max_azs"])
            check_type(argname="argument vpc_name", value=vpc_name, expected_type=type_hints["vpc_name"])
            check_type(argname="argument vpn_connections", value=vpn_connections, expected_type=type_hints["vpn_connections"])
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
            check_type(argname="argument vpn_gateway_asn", value=vpn_gateway_asn, expected_type=type_hints["vpn_gateway_asn"])
            check_type(argname="argument vpn_route_propagation", value=vpn_route_propagation, expected_type=type_hints["vpn_route_propagation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway": transit_gateway,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if cidr is not None:
            self._values["cidr"] = cidr
        if default_instance_tenancy is not None:
            self._values["default_instance_tenancy"] = default_instance_tenancy
        if enable_dns_hostnames is not None:
            self._values["enable_dns_hostnames"] = enable_dns_hostnames
        if enable_dns_support is not None:
            self._values["enable_dns_support"] = enable_dns_support
        if flow_logs is not None:
            self._values["flow_logs"] = flow_logs
        if gateway_endpoints is not None:
            self._values["gateway_endpoints"] = gateway_endpoints
        if max_azs is not None:
            self._values["max_azs"] = max_azs
        if vpc_name is not None:
            self._values["vpc_name"] = vpc_name
        if vpn_connections is not None:
            self._values["vpn_connections"] = vpn_connections
        if vpn_gateway is not None:
            self._values["vpn_gateway"] = vpn_gateway
        if vpn_gateway_asn is not None:
            self._values["vpn_gateway_asn"] = vpn_gateway_asn
        if vpn_route_propagation is not None:
            self._values["vpn_route_propagation"] = vpn_route_propagation

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transit_gateway(self) -> _ITransitGateway_25936657:
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(_ITransitGateway_25936657, result)

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("availability_zones")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cidr(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_instance_tenancy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy]:
        result = self._values.get("default_instance_tenancy")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy], result)

    @builtins.property
    def enable_dns_hostnames(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_hostnames")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enable_dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flow_logs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]]:
        result = self._values.get("flow_logs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.FlowLogOptions]], result)

    @builtins.property
    def gateway_endpoints(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]]:
        result = self._values.get("gateway_endpoints")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions]], result)

    @builtins.property
    def max_azs(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_azs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("vpc_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_connections(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]]:
        result = self._values.get("vpn_connections")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions]], result)

    @builtins.property
    def vpn_gateway(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_gateway")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpn_gateway_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("vpn_gateway_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpn_route_propagation(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]]:
        result = self._values.get("vpn_route_propagation")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FourTierNetworkSpokeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.TransitGatewayHubConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external": "allowExternal",
        "auto_accept_shared_attachments": "autoAcceptSharedAttachments",
        "auto_discovery": "autoDiscovery",
        "default_route_table_id": "defaultRouteTableId",
        "principals": "principals",
    },
)
class TransitGatewayHubConfiguration:
    def __init__(
        self,
        *,
        allow_external: typing.Optional[builtins.bool] = None,
        auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
        auto_discovery: typing.Optional[builtins.bool] = None,
        default_route_table_id: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> None:
        '''
        :param allow_external: Allows Transit Gateway sharing with resources outside of the Transit Gateway owner account's AWS Organization. By default, resources cannot be shared with accounts outside of the organization.
        :param auto_accept_shared_attachments: Enable or disable automatic acceptance of attachment requests. When this is enabled, any transit gateway attachments created in other accounts where this transit gateway has been shared will be automatically created without manual intervention being needed in the account that did created the share.
        :param auto_discovery: Enables auto-discovery of AWS accounts via CDK resources. Account discovery uses stages and stacks to find all accounts that the CDK has resources for. Environment agnostic stages and stacks cannot be used for auto-discovery. With auto-discovery enabled, the stack containing the Transit Gateway will need to be updated before it will become available in newly added accounts. Because of this it is inferior to using grouping principals such as organizations or organizational units. If access to sharing via AWS OIrganizations is available, that should be preferred over auto-discovery. Transit gateway sharing will be anabled if either auto-discovery is enabled or principals are specified.
        :param default_route_table_id: The ID of the default Transit Gateway Route Table that got created for the Transit Gateway associated with this VPC. This is needed because the default route table is used for handling routing of all traffic within the organization but not exposed directly via CloudFormation. See `feature request <https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/180>`_ related to this in the AWS CloudFormation roadmap. This is only needed if the VPC is being configured to act as a hub for network traffic. Won't be available until after this stack has been deployed for the first time.
        :param principals: A list of principals which allow other accounts access to the Transit Gateway. With shared access, other accounts can create Attachments to facilitate cross account networking. Principals provided should not overlap with CDK resources if auto-discovery is enabled. Transit gateway sharing will be anabled if either auto-discovery is enabled or principals are specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6667797cf749d298a257c6c716db23d22c81c5c28b1dbf19334ef2de80ebcba5)
            check_type(argname="argument allow_external", value=allow_external, expected_type=type_hints["allow_external"])
            check_type(argname="argument auto_accept_shared_attachments", value=auto_accept_shared_attachments, expected_type=type_hints["auto_accept_shared_attachments"])
            check_type(argname="argument auto_discovery", value=auto_discovery, expected_type=type_hints["auto_discovery"])
            check_type(argname="argument default_route_table_id", value=default_route_table_id, expected_type=type_hints["default_route_table_id"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external is not None:
            self._values["allow_external"] = allow_external
        if auto_accept_shared_attachments is not None:
            self._values["auto_accept_shared_attachments"] = auto_accept_shared_attachments
        if auto_discovery is not None:
            self._values["auto_discovery"] = auto_discovery
        if default_route_table_id is not None:
            self._values["default_route_table_id"] = default_route_table_id
        if principals is not None:
            self._values["principals"] = principals

    @builtins.property
    def allow_external(self) -> typing.Optional[builtins.bool]:
        '''Allows Transit Gateway sharing with resources outside of the Transit Gateway owner account's AWS Organization.

        By default, resources cannot be shared with accounts outside of the organization.
        '''
        result = self._values.get("allow_external")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_accept_shared_attachments(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable automatic acceptance of attachment requests.

        When this is enabled, any transit gateway attachments created in other accounts where this
        transit gateway has been shared will be automatically created without manual intervention
        being needed in the account that did created the share.
        '''
        result = self._values.get("auto_accept_shared_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_discovery(self) -> typing.Optional[builtins.bool]:
        '''Enables auto-discovery of AWS accounts via CDK resources.

        Account discovery uses stages
        and stacks to find all accounts that the CDK has resources for.

        Environment agnostic stages and stacks cannot be used for auto-discovery.

        With auto-discovery enabled, the stack containing the Transit Gateway will need to be
        updated before it will become available in newly added accounts. Because of this it is
        inferior to using grouping principals such as organizations or organizational units.

        If access to sharing via AWS OIrganizations is available, that should be preferred over
        auto-discovery.

        Transit gateway sharing will be anabled if either auto-discovery is enabled or principals
        are specified.
        '''
        result = self._values.get("auto_discovery")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_route_table_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the default Transit Gateway Route Table that got created for the Transit Gateway associated with this VPC.

        This is needed because the default route table is used for handling routing of all traffic within
        the organization but not exposed directly via CloudFormation.

        See `feature request <https://github.com/aws-cloudformation/cloudformation-coverage-roadmap/issues/180>`_
        related to this in the AWS CloudFormation roadmap.

        This is only needed if the VPC is being configured to act as a hub for network traffic. Won't be
        available until after this stack has been deployed for the first time.
        '''
        result = self._values.get("default_route_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[_ISharedPrincipal_9cde791b]]:
        '''A list of principals which allow other accounts access to the Transit Gateway.

        With shared
        access, other accounts can create Attachments to facilitate cross account networking.

        Principals provided should not overlap with CDK resources if auto-discovery is enabled.

        Transit gateway sharing will be anabled if either auto-discovery is enabled or principals
        are specified.
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[_ISharedPrincipal_9cde791b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayHubConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2_patterns.TransitGatewaySpokeConfiguration",
    jsii_struct_bases=[],
    name_mapping={"transit_gateway_id": "transitGatewayId"},
)
class TransitGatewaySpokeConfiguration:
    def __init__(self, *, transit_gateway_id: builtins.str) -> None:
        '''
        :param transit_gateway_id: The ID of a Transit Gateway. This Transit Gateway may have been created by another VPC in the same account or shared by a VPC in another account. If this is passed then a Transit Gateway Attachment will be created for the specified Transit Gateway and a new one will not be created even if {@link TransitGatewayHubConfiguration.principal | principals} are provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a4c2c3e6825c2e1a0d5ead7abe49653b6e864843a82ccc9624945cfe7e9a77)
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway_id": transit_gateway_id,
        }

    @builtins.property
    def transit_gateway_id(self) -> builtins.str:
        '''The ID of a Transit Gateway.

        This Transit Gateway may have been created by another VPC in the
        same account or shared by a VPC in another account. If this is passed then a Transit Gateway
        Attachment will be created for the specified Transit Gateway and a new one will not be created
        even if {@link TransitGatewayHubConfiguration.principal | principals} are provided.
        '''
        result = self._values.get("transit_gateway_id")
        assert result is not None, "Required property 'transit_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewaySpokeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddSpokeNetworkProps",
    "FlowLogOptions",
    "FourTierNetwork",
    "FourTierNetworkHub",
    "FourTierNetworkHubProps",
    "FourTierNetworkProps",
    "FourTierNetworkShareProperties",
    "FourTierNetworkSpoke",
    "FourTierNetworkSpokeProps",
    "TransitGatewayHubConfiguration",
    "TransitGatewaySpokeConfiguration",
]

publication.publish()

def _typecheckingstub__048409c4bedb08ed8edc9dda9cec65cb4087822a3dcae95d57c194d4e0613116(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61356c6c988a747170b0fff518aeff55bb37140b2f2bb3a8395a7676df11d939(
    *,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b54dda1f6044b8b90a294f4af2c53fd512620a5e619adafd6d687a35f35dc3(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb697f4884edaa9946bcf623d36e26bbc15cba6a321ac50f29f26b8fdef42b2a(
    id: builtins.str,
    *,
    log_format_definition: typing.Optional[_FlowLogFormat_b7c2ba34] = None,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    log_format: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.LogFormat]] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ace25eaf0b1bdeb7c9833547b92ca28254092d01db9ebc9696fce2260b43d9(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    sharing: typing.Optional[typing.Union[FourTierNetworkShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b427eb756711b9be0d1724b92283f7b8b658149d02d0860ddfaae4ca009451a6(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1e120a9a594264d414d234533b6a6694a2e18b423a355c83676f0931ec9be90(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    sharing: typing.Optional[typing.Union[FourTierNetworkShareProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9f1c80c97704155becd995a7614b98797ff3dcfedcb6c14a3c861d8ffa5d99(
    *,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    nat_gateway_provider: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatProvider] = None,
    nat_gateways: typing.Optional[jsii.Number] = None,
    nat_gateway_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba6d7153869452d0a1b515208e0e7160367751697fbee237f3d54f9f8411a28(
    *,
    allow_external_principals: typing.Optional[builtins.bool] = None,
    auto_add_accounts: typing.Optional[builtins.bool] = None,
    pricipals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fc919bd6ebf5b551769cb4313098a0e49891c0d5e533cf159dc7f303b04473(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    transit_gateway: _ITransitGateway_25936657,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f20b71c01dce683a9711971685bfd423a84bb51b3ae70144ed170d14b6b7721(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    transit_gateway: _ITransitGateway_25936657,
    availability_zones: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidr: typing.Optional[builtins.str] = None,
    default_instance_tenancy: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.DefaultInstanceTenancy] = None,
    enable_dns_hostnames: typing.Optional[builtins.bool] = None,
    enable_dns_support: typing.Optional[builtins.bool] = None,
    flow_logs: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.FlowLogOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_endpoints: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpointOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_azs: typing.Optional[jsii.Number] = None,
    vpc_name: typing.Optional[builtins.str] = None,
    vpn_connections: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_ec2_ceddda9d.VpnConnectionOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_gateway: typing.Optional[builtins.bool] = None,
    vpn_gateway_asn: typing.Optional[jsii.Number] = None,
    vpn_route_propagation: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6667797cf749d298a257c6c716db23d22c81c5c28b1dbf19334ef2de80ebcba5(
    *,
    allow_external: typing.Optional[builtins.bool] = None,
    auto_accept_shared_attachments: typing.Optional[builtins.bool] = None,
    auto_discovery: typing.Optional[builtins.bool] = None,
    default_route_table_id: typing.Optional[builtins.str] = None,
    principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a4c2c3e6825c2e1a0d5ead7abe49653b6e864843a82ccc9624945cfe7e9a77(
    *,
    transit_gateway_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
