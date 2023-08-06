'''
# Vibe-io CDK-Extensions EC2 Construct Library

The @cdk-extensions/ec2 package contains advanced constructs and patterns for
setting up networking and instances. The constructs presented here are intended
to be replacements for equivalent AWS constructs in the CDK EC2 module, but with
additional features included.

[AWS CDK EC2 API Reference](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_ec2-readme.html)

To import and use this module within your CDK project:

```python
import * as ec2 from 'cdk-extensions/ec2';
```

## VPC Flow Logs

VPC Flow Logs is a feature that enables you to capture information about the IP
traffic going to and from network interfaces in your VPC. Flow log data can be
published to Amazon CloudWatch Logs and Amazon S3. After you've created a flow
log, you can retrieve and view its data in the chosen destination.
[AWS VPC Flow Logs User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
[AWS VPC Flow Logs CFN Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html)

For this construct, by default a S3 bucket will be created as the Flow Logs
destination. It will also include a Glue table with the same schema as the
configured FlowLogFormat, as well as prepared Athena queries.

### Usage

You can create a flow log like this:

```python
new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc)
})
```

You can also add multiple flow logs with different destinations.

```python
const bucket = new s3.Bucket(this, 'MyCustomBucket');

new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  destination: ec2.FlowLogDestination.toS3(bucket)
});

new ec2.FlowLog(this, 'FlowLogCloudWatch', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  trafficType: ec2.FlowLogTrafficType.REJECT,
  maxAggregationInterval: FlowLogMaxAggregationInterval.ONE_MINUTE,
});
```

### Additional Features

The main advantage that this module has over the official AWS CDK module is that
you can specific the log format at the time of FlowLog creation like this:

```python
new ec2.FlowLog(this, 'FlowLog', {
  resourceType: ec2.FlowLogResourceType.fromVpc(myVpc),
  format: ec2.FlowLogFormat.V3,
})
```

There are several formats that are included as part of the module, and each one
will define the fields included in the flow log records. Each one acts similarly
to a log level (Info, Debug, etc), with each level providing increasingly more
detail in the logs (like region or AZ details, or AWS service details).

The formats and descriptions are as follows:

* ec2.FlowLogFormat.V2: The default format if none is specified. Includes common
  basic details like log status, account ID, source and
  destination.
* ec2.FlowLogFormat.V3: Includes all fields from V2, as well as information on
  the specific AWS resources associated with the traffic
  like Vpc, subnet and instance IDs.
* ec2.FlowLogFormat.V4: Includes all fields from V3, as well as information about
  the region and AZ associated with the traffic.
* ec2.FlowLogFormat.V5: Includes all fields from V4, as well as information that
  provides visibility on packet routing.

### Caveats

With the offical AWS CDK VPC construct, you can normally add a Flow Log to a VPC
by using the addFlowLog() method like this:

```python
const vpc = new ec2.Vpc(this, 'Vpc');

vpc.addFlowLog('FlowLog');
```

However, this will not include the additional FlowLogFormat functionality
provided by the FlowLog construct in this module.
'''
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
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ..ram import (
    ISharedPrincipal as _ISharedPrincipal_9cde791b,
    ResourceShare as _ResourceShare_f0180713,
)


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.CustomerGatewayAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway_id": "customerGatewayId",
        "bgp_asn": "bgpAsn",
        "ip_address": "ipAddress",
    },
)
class CustomerGatewayAttributes:
    def __init__(
        self,
        *,
        customer_gateway_id: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Attributes used to import an existing customer gateway.

        :param customer_gateway_id: The ID of the existing customer gateway being imported.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35eab003d889c662b910b407f8e02c5f1e0c594802680266f3389251bf5ac9d3)
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
            check_type(argname="argument bgp_asn", value=bgp_asn, expected_type=type_hints["bgp_asn"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_id": customer_gateway_id,
        }
        if bgp_asn is not None:
            self._values["bgp_asn"] = bgp_asn
        if ip_address is not None:
            self._values["ip_address"] = ip_address

    @builtins.property
    def customer_gateway_id(self) -> builtins.str:
        '''The ID of the existing customer gateway being imported.'''
        result = self._values.get("customer_gateway_id")
        assert result is not None, "Required property 'customer_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bgp_asn(self) -> typing.Optional[jsii.Number]:
        '''For devices that support BGP, the customer gateway's BGP ASN.'''
        result = self._values.get("bgp_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The Internet-routable IP address for the customer gateway's outside interface.

        The address must be static.
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerGatewayAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.CustomerGatewayProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "ip_address": "ipAddress",
        "bgp_asn": "bgpAsn",
        "connection_type": "connectionType",
    },
)
class CustomerGatewayProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        ip_address: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional["VpnConnectionType"] = None,
    ) -> None:
        '''Configuration for the CustomerGateway resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param connection_type: The type of VPN connection that this customer gateway supports.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e250ab0ff20773956eb3b2131200a7ee56b455ba85d22729b69f588d369a8193)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument bgp_asn", value=bgp_asn, expected_type=type_hints["bgp_asn"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ip_address": ip_address,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if bgp_asn is not None:
            self._values["bgp_asn"] = bgp_asn
        if connection_type is not None:
            self._values["connection_type"] = connection_type

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
    def ip_address(self) -> builtins.str:
        '''The Internet-routable IP address for the customer gateway's outside interface.

        The address must be static.

        :see: `CustomerGateway IpAddress <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-ipaddress>`_
        '''
        result = self._values.get("ip_address")
        assert result is not None, "Required property 'ip_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bgp_asn(self) -> typing.Optional[jsii.Number]:
        '''For devices that support BGP, the customer gateway's BGP ASN.

        :see: `CustomerGateway BgpAsn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-bgpasn>`_
        '''
        result = self._values.get("bgp_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def connection_type(self) -> typing.Optional["VpnConnectionType"]:
        '''The type of VPN connection that this customer gateway supports.

        :see: `CustomerGateway Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-type>`_
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional["VpnConnectionType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomerGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FlowLog(
    _aws_cdk_aws_ec2_ceddda9d.FlowLog,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLog",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        resource_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        flow_log_name: typing.Optional[builtins.str] = None,
        log_format: typing.Optional["FlowLogFormat"] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the FlowLog class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param resource_type: Details for the resource from which flow logs will be captured.
        :param destination: The location where flow logs should be delivered.
        :param flow_log_name: The name of the FlowLog.
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. For a list of available fields, see {@link FlowLogField}.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.
        :param traffic_type: The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685f60b23d7e8e561b55bc9dca121799b9d63919b8e78b372a1fa549c234455e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FlowLogProps(
            resource_type=resource_type,
            destination=destination,
            flow_log_name=flow_log_name,
            log_format=log_format,
            max_aggregation_interval=max_aggregation_interval,
            traffic_type=traffic_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> _aws_cdk_aws_ec2_ceddda9d.FlowLogDestination:
        '''The location where flow logs should be delivered.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination, jsii.get(self, "destination"))

    @builtins.property
    @jsii.member(jsii_name="logFormat")
    def log_format(self) -> "FlowLogFormat":
        '''The fields to include in the flow log record, in the order in which they should appear.

        For a list of available fields, see {@link FlowLogField}.

        :see: `FlowLog LogFormat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logformat>`_
        :group: Inputs
        '''
        return typing.cast("FlowLogFormat", jsii.get(self, "logFormat"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnFlowLog:
        '''The underlying FlowLog CloudFormation resource.

        :see: `AWS::EC2::FlowLog <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnFlowLog, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType:
        '''Details for the resource from which flow logs will be captured.

        :see: `FlowLog ResourceType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourcetype>`_
        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType, jsii.get(self, "resourceType"))

    @builtins.property
    @jsii.member(jsii_name="trafficType")
    def traffic_type(self) -> _aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType:
        '''The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).

        :see: `FlowLog TrafficType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-traffictype>`_
        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType, jsii.get(self, "trafficType"))

    @builtins.property
    @jsii.member(jsii_name="flowLogName")
    def flow_log_name(self) -> typing.Optional[builtins.str]:
        '''The name of the FlowLog.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flowLogName"))

    @builtins.property
    @jsii.member(jsii_name="maxAggregationInterval")
    def max_aggregation_interval(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :see: `FlowLog MaxAggregationInterval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-maxaggregationinterval>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval], jsii.get(self, "maxAggregationInterval"))


@jsii.enum(jsii_type="cdk-extensions.ec2.FlowLogDataType")
class FlowLogDataType(enum.Enum):
    INT_32 = "INT_32"
    '''32 bit signed int.'''
    INT_64 = "INT_64"
    '''64 bit signed int.'''
    STRING = "STRING"
    '''UTF-8 encoded character string.'''


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogDestinationConfig",
    jsii_struct_bases=[],
    name_mapping={
        "destination_type": "destinationType",
        "bucket": "bucket",
        "destination_options": "destinationOptions",
        "log_group": "logGroup",
        "role": "role",
        "s3_path": "s3Path",
    },
)
class FlowLogDestinationConfig:
    def __init__(
        self,
        *,
        destination_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogDestinationType,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        destination_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        s3_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''A configuration object providing the details necessary to set up log delivery to a given destination.

        :param destination_type: The type of destination for the flow log data.
        :param bucket: An S3 bucket where logs should be delivered.
        :param destination_options: Additional options that control the format and behavior of logs delivered to the destination.
        :param log_group: A CloudWatch LogGroup where logs should be delivered.
        :param role: The ARN of the IAM role that allows Amazon EC2 to publish flow logs in your account.
        :param s3_path: An Amazon Resource Name (ARN) for the S3 destination where log files are to be delivered. If a custom prefix is being added the ARN should reflect that prefix.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b243acaaaa5840cda314f12b7b4d009805f9002ef9847296dedc4c734cfaa8)
            check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument destination_options", value=destination_options, expected_type=type_hints["destination_options"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_type": destination_type,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if destination_options is not None:
            self._values["destination_options"] = destination_options
        if log_group is not None:
            self._values["log_group"] = log_group
        if role is not None:
            self._values["role"] = role
        if s3_path is not None:
            self._values["s3_path"] = s3_path

    @builtins.property
    def destination_type(self) -> _aws_cdk_aws_ec2_ceddda9d.FlowLogDestinationType:
        '''The type of destination for the flow log data.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        '''
        result = self._values.get("destination_type")
        assert result is not None, "Required property 'destination_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLogDestinationType, result)

    @builtins.property
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''An S3 bucket where logs should be delivered.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def destination_options(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''Additional options that control the format and behavior of logs delivered to the destination.'''
        result = self._values.get("destination_options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''A CloudWatch LogGroup where logs should be delivered.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The ARN of the IAM role that allows Amazon EC2 to publish flow logs in your account.

        :see: `FlowLog DeliverLogsPermissionArn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-deliverlogspermissionarn>`_
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def s3_path(self) -> typing.Optional[builtins.str]:
        '''An Amazon Resource Name (ARN) for the S3 destination where log files are to be delivered.

        If a custom prefix is being added the ARN should reflect that prefix.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("s3_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogDestinationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FlowLogField(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLogField",
):
    def __init__(self, name: builtins.str, type: FlowLogDataType) -> None:
        '''Creates a new instance of the FlowLogField class.

        :param name: The name of the Flow Log field, as it should be used when building a format string.
        :param type: The data type of the field as it would appear in Parquet. For information on the type for various files, see documentation on the `available fields <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields>`_.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52a7eb2a067a774b7223df31becb41f1517c9aa30eb3b326b26ad7504939a991)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        jsii.create(self.__class__, self, [name, type])

    @jsii.member(jsii_name="lookupField")
    @builtins.classmethod
    def lookup_field(cls, name: builtins.str) -> typing.Optional["FlowLogField"]:
        '''Tries to retieve full flow log field data for a log field based on name.

        Returns undefined if the field name is not recognized.

        :param name: The name of the FlowLogField to look up.

        :return:

        The FlowLogField data for a field with the given name if one is
        found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__186041c191f59ab5a16d388d89fb358a9ce5c7c993bd90eb9e6479e368341acd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(typing.Optional["FlowLogField"], jsii.sinvoke(cls, "lookupField", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCOUNT_ID")
    def ACCOUNT_ID(cls) -> "FlowLogField":
        '''The AWS account ID of the owner of the source network interface for which traffic is recorded.

        If the network interface is created by an
        AWS service, for example when creating a VPC endpoint or Network Load
        Balancer, the record might display unknown for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "ACCOUNT_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACTION")
    def ACTION(cls) -> "FlowLogField":
        '''The action that is associated with the traffic:.

        ACCEPT: The recorded traffic was permitted by the security groups and
        network ACLs.
        REJECT: The recorded traffic was not permitted by the security groups
        or network ACLs.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "ACTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AZ_ID")
    def AZ_ID(cls) -> "FlowLogField":
        '''The ID of the Availability Zone that contains the network interface for which traffic is recorded.

        If the traffic is from a sublocation, the
        record displays a '-' symbol for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "AZ_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BYTES")
    def BYTES(cls) -> "FlowLogField":
        '''The number of bytes transferred during the flow.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "BYTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DSTADDR")
    def DSTADDR(cls) -> "FlowLogField":
        '''The destination address for outgoing traffic, or the IPv4 or IPv6 address of the network interface for incoming traffic on the network interface.

        The IPv4 address of the network interface is always its
        private IPv4 address.

        See also:
        {@link FlowLogField.PKT_DSTADDR | PKT_DSTADDR}
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "DSTADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DSTPORT")
    def DSTPORT(cls) -> "FlowLogField":
        '''The destination port of the traffic.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "DSTPORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="END")
    def END(cls) -> "FlowLogField":
        '''The time, in Unix seconds, when the last packet of the flow was received within the aggregation interval.

        This might be up to 60
        seconds after the packet was transmitted or received on the network
        interface.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "END"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOW_DIRECTION")
    def FLOW_DIRECTION(cls) -> "FlowLogField":
        '''The direction of the flow with respect to the interface where traffic is captured.

        The possible values are: ingress | egress.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "FLOW_DIRECTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INSTANCE_ID")
    def INSTANCE_ID(cls) -> "FlowLogField":
        '''The ID of the instance that's associated with network interface for which the traffic is recorded, if the instance is owned by you.

        Returns
        a '-' symbol for a requester-managed network interface; for example,
        the network interface for a NAT gateway.

        See also:
        `Request-managed ENI <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/requester-managed-eni.html>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "INSTANCE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INTERFACE_ID")
    def INTERFACE_ID(cls) -> "FlowLogField":
        '''The ID of the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "INTERFACE_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOG_STATUS")
    def LOG_STATUS(cls) -> "FlowLogField":
        '''The logging status of the flow log:.

        OK: Data is logging normally to the chosen destinations.
        NODATA: There was no network traffic to or from the network interface
        during the aggregation interval.
        SKIPDATA — Some flow log records were skipped during the aggregation
        interval. This might be because of an internal capacity constraint, or
        an internal error.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "LOG_STATUS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PACKETS")
    def PACKETS(cls) -> "FlowLogField":
        '''The number of packets transferred during the flow.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "PACKETS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_DST_AWS_SERVICE")
    def PKT_DST_AWS_SERVICE(cls) -> "FlowLogField":
        '''The name of the subset of IP address ranges for the pkt-dstaddr field, if the destination IP address is for an AWS service.

        For a list of
        possible values, see the {@link FlowLogField.PKT_SRC_AWS_SERVICE | PKT_SRC_AWS_SERVICE} field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_DST_AWS_SERVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_DSTADDR")
    def PKT_DSTADDR(cls) -> "FlowLogField":
        '''The packet-level (original) destination IP address for the traffic.

        Use
        this field with the dstaddr field to distinguish between the IP address
        of an intermediate layer through which traffic flows, and the final
        destination IP address of the traffic. For example, when traffic flows
        through a network interface for a NAT gateway, or where the IP address
        of a pod in Amazon EKS is different from the IP address of the network
        interface of the instance node on which the pod is running (for
        communication within a VPC).

        See also:
        `Flow Log Example NAT <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-nat>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_DSTADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_SRC_AWS_SERVICE")
    def PKT_SRC_AWS_SERVICE(cls) -> "FlowLogField":
        '''The name of the subset of IP address ranges for the pkt-srcaddr field, if the source IP address is for an AWS service.

        The possible values
        are: AMAZON | AMAZON_APPFLOW | AMAZON_CONNECT | API_GATEWAY |
        CHIME_MEETINGS | CHIME_VOICECONNECTOR | CLOUD9 | CLOUDFRONT |
        CODEBUILD | DYNAMODB | EBS | EC2 | EC2_INSTANCE_CONNECT |
        GLOBALACCELERATOR | KINESIS_VIDEO_STREAMS | ROUTE53 |
        ROUTE53_HEALTHCHECKS | ROUTE53_HEALTHCHECKS_PUBLISHING |
        ROUTE53_RESOLVER | S3 | WORKSPACES_GATEWAYS.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_SRC_AWS_SERVICE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PKT_SRCADDR")
    def PKT_SRCADDR(cls) -> "FlowLogField":
        '''The packet-level (original) source IP address of the traffic.

        Use this
        field with the srcaddr field to distinguish between the IP address of
        an intermediate layer through which traffic flows, and the original
        source IP address of the traffic. For example, when traffic flows
        through a network interface for a NAT gateway, or where the IP address
        of a pod in Amazon EKS is different from the IP address of the network
        interface of the instance node on which the pod is running (for
        communication within a VPC).

        See also:
        `Flow Log Example NAT <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-nat>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PKT_SRCADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROTOCOL")
    def PROTOCOL(cls) -> "FlowLogField":
        '''The IANA protocol number of the traffic.

        See also:
        `Assigned Internet Protocol Numbers <http://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml>`_.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "PROTOCOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGION")
    def REGION(cls) -> "FlowLogField":
        '''The Region that contains the network interface for which traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "REGION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SRCADDR")
    def SRCADDR(cls) -> "FlowLogField":
        '''The source address for incoming traffic, or the IPv4 or IPv6 address of the network interface for outgoing traffic on the network interface.

        The IPv4 address of the network interface is always its private IPv4
        address.

        See also:
        {@link FlowLogField.PKT_SRCADDR | PKT_SRCADDR}
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SRCADDR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SRCPORT")
    def SRCPORT(cls) -> "FlowLogField":
        '''The source port of the traffic.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "SRCPORT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="START")
    def START(cls) -> "FlowLogField":
        '''The time, in Unix seconds, when the first packet of the flow was received within the aggregation interval.

        This might be up to 60
        seconds after the packet was transmitted or received on the network
        interface.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "START"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBLOCATION_ID")
    def SUBLOCATION_ID(cls) -> "FlowLogField":
        '''The ID of the sublocation that contains the network interface for which traffic is recorded.

        If the traffic is not from a sublocation, the
        record displays a '-' symbol for this field.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBLOCATION_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBLOCATION_TYPE")
    def SUBLOCATION_TYPE(cls) -> "FlowLogField":
        '''The type of sublocation that's returned in the sublocation-id field.

        The possible values are: wavelength | outpost | localzone. If the
        traffic is not from a sublocation, the record displays a '-' symbol
        for this field.

        See also:
        `Wavelength <https://aws.amazon.com/wavelength/>`_
        `Outposts <https://docs.aws.amazon.com/outposts/latest/userguide/>`_
        `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBLOCATION_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SUBNET_ID")
    def SUBNET_ID(cls) -> "FlowLogField":
        '''The ID of the subnet that contains the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "SUBNET_ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TCP_FLAGS")
    def TCP_FLAGS(cls) -> "FlowLogField":
        '''The bitmask value for the following TCP flags:.

        FIN: 1
        SYN: 2
        RST: 4
        PSH: 8
        ACK: 16
        SYN-ACK: 18
        URG: 32

        When a flow log entry consists of only ACK packets, the flag value is
        0, not 16.

        TCP flags can be OR-ed during the aggregation interval. For short
        connections, the flags might be set on the same line in the flow log
        record, for example, 19 for SYN-ACK and FIN, and 3 for SYN and FIN.

        See also:
        `TCP Segment Structure <https://en.wikipedia.org/wiki/Transmission_Control_Protocol#TCP_segment_structure>`_
        `TCP Flag Sequence <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-tcp-flag>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TCP_FLAGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRAFFIC_PATH")
    def TRAFFIC_PATH(cls) -> "FlowLogField":
        '''The path that egress traffic takes to the destination.

        To determine
        whether the traffic is egress traffic, check the flow-direction field.
        The possible values are as follows. If none of the values apply, the
        field is set to -.

        1: Through another resource in the same VPC
        2: Through an internet gateway or a gateway VPC endpoint
        3: Through a virtual private gateway
        4: Through an intra-region VPC peering connection
        5: Through an inter-region VPC peering connection
        6: Through a local gateway
        7: Through a gateway VPC endpoint (Nitro-based instances only)
        8: Through an internet gateway (Nitro-based instances only)
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TRAFFIC_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TYPE")
    def TYPE(cls) -> "FlowLogField":
        '''The type of traffic. The possible values are: IPv4 | IPv6 | EFA.

        See also:
        `Elastic Fabric Adapter <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html>`_
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> "FlowLogField":
        '''The VPC Flow Logs version.

        If you use the default format, the version
        is 2. If you use a custom format, the version is the highest version
        among the specified fields. For example, if you specify only fields
        from version 2, the version is 2. If you specify a mixture of fields
        from versions 2, 3, and 4, the version is 4.
        '''
        return typing.cast("FlowLogField", jsii.sget(cls, "VERSION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ID")
    def VPC_ID(cls) -> "FlowLogField":
        '''The ID of the VPC that contains the network interface for which the traffic is recorded.'''
        return typing.cast("FlowLogField", jsii.sget(cls, "VPC_ID"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Flow Log field, as it should be used when building a format string.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> FlowLogDataType:
        '''The data type of the field as it would appear in Parquet.

        For
        information on the type for various files, see documentation on the
        `available fields <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields>`_.
        '''
        return typing.cast(FlowLogDataType, jsii.get(self, "type"))


@jsii.enum(jsii_type="cdk-extensions.ec2.FlowLogFileFormat")
class FlowLogFileFormat(enum.Enum):
    '''The file format options for flow log files delivered to S3.

    :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
    '''

    PARQUET = "PARQUET"
    '''Apache Parquet is a columnar data format.

    Queries on data in Parquet
    format are 10 to 100 times faster compared to queries on data in plain
    text. Data in Parquet format with Gzip compression takes 20 percent less
    storage space than plain text with Gzip compression.
    '''
    PLAIN_TEXT = "PLAIN_TEXT"
    '''Plain text.

    This is the default format.
    '''


class FlowLogFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.FlowLogFormat",
):
    def __init__(self, *fields: FlowLogField) -> None:
        '''Creates a new instance of the FlowLogFormat class.

        :param fields: The fields that should be included in the flow log output.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__011095d32393e36e81237f11a84f5543e965a7ff361a20975a530a17197f4a8e)
            check_type(argname="argument fields", value=fields, expected_type=typing.Tuple[type_hints["fields"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*fields])

    @jsii.member(jsii_name="fromTemplate")
    @builtins.classmethod
    def from_template(cls, template: builtins.str) -> "FlowLogFormat":
        '''Parses a flow log format template string to create a new FlowLogFormat object.

        :param template: A flow log template string to parse.

        :return: A FlowLogFormat object representing the passed template.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cb1f7019aee739ea8276bab9a93a7e6f40b4ebf40d15497239b2c6b1676033e)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        return typing.cast("FlowLogFormat", jsii.sinvoke(cls, "fromTemplate", [template]))

    @jsii.member(jsii_name="addField")
    def add_field(self, field: FlowLogField) -> None:
        '''Adds a new field to the flow log output.

        New fields are added at the
        end of a log entry after all the other fields that came before it.

        :param field: The field to add to the FlowLogFormat.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cf487bf8fa03e8840d7c2097f578bf3849b50872d93bdad4cc33d93380f5cd)
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast(None, jsii.invoke(self, "addField", [field]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2")
    def V2(cls) -> "FlowLogFormat":
        '''The basic set of fields included in most flow logs.

        This is the default
        format that is used when new flow logs are created without specifying a
        custom format.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V2"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3")
    def V3(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V2.

        Adds fields to help identify
        AWS resources associated with traffic as well as fields that give
        greater visibility into protocol specific details.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V3"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V4")
    def V4(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V3.

        Adds fields for identifying
        the region and availabilty zone associated with flows, as well as
        details related to extended zones such as Wavelength, Outputs, and
        Local Zones.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V4"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V5")
    def V5(cls) -> "FlowLogFormat":
        '''Includes all the fields available in V4.

        Adds fields to help identify
        related AWS services and improve visibility into packet routing.
        '''
        return typing.cast("FlowLogFormat", jsii.sget(cls, "V5"))

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(self) -> typing.List[FlowLogField]:
        '''The fields that make up the flow log format, in the order that they should appear in the log entries.'''
        return typing.cast(typing.List[FlowLogField], jsii.get(self, "fields"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        '''The rendered format string in the format expected by AWS when creating a new Flow Log.'''
        return typing.cast(builtins.str, jsii.get(self, "template"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "resource_type": "resourceType",
        "destination": "destination",
        "flow_log_name": "flowLogName",
        "log_format": "logFormat",
        "max_aggregation_interval": "maxAggregationInterval",
        "traffic_type": "trafficType",
    },
)
class FlowLogProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        resource_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType,
        destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
        flow_log_name: typing.Optional[builtins.str] = None,
        log_format: typing.Optional[FlowLogFormat] = None,
        max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
        traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    ) -> None:
        '''Configuration for the FlowLog class.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param resource_type: Details for the resource from which flow logs will be captured.
        :param destination: The location where flow logs should be delivered.
        :param flow_log_name: The name of the FlowLog.
        :param log_format: The fields to include in the flow log record, in the order in which they should appear. For a list of available fields, see {@link FlowLogField}.
        :param max_aggregation_interval: The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.
        :param traffic_type: The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab60db00df2ad42cfdeb4bac9052956c6ceecbdc94e94e83e7a5b1a8d4db724f)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument flow_log_name", value=flow_log_name, expected_type=type_hints["flow_log_name"])
            check_type(argname="argument log_format", value=log_format, expected_type=type_hints["log_format"])
            check_type(argname="argument max_aggregation_interval", value=max_aggregation_interval, expected_type=type_hints["max_aggregation_interval"])
            check_type(argname="argument traffic_type", value=traffic_type, expected_type=type_hints["traffic_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_type": resource_type,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if destination is not None:
            self._values["destination"] = destination
        if flow_log_name is not None:
            self._values["flow_log_name"] = flow_log_name
        if log_format is not None:
            self._values["log_format"] = log_format
        if max_aggregation_interval is not None:
            self._values["max_aggregation_interval"] = max_aggregation_interval
        if traffic_type is not None:
            self._values["traffic_type"] = traffic_type

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
    def resource_type(self) -> _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType:
        '''Details for the resource from which flow logs will be captured.

        :see: `FlowLog ResourceType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourcetype>`_
        :group: Inputs
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType, result)

    @builtins.property
    def destination(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination]:
        '''The location where flow logs should be delivered.

        :see: `FlowLog LogDestinationType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype>`_
        :group: Inputs
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination], result)

    @builtins.property
    def flow_log_name(self) -> typing.Optional[builtins.str]:
        '''The name of the FlowLog.

        :group: Inputs
        '''
        result = self._values.get("flow_log_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_format(self) -> typing.Optional[FlowLogFormat]:
        '''The fields to include in the flow log record, in the order in which they should appear.

        For a list of available fields, see {@link FlowLogField}.

        :see: `FlowLog LogFormat <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logformat>`_
        :group: Inputs
        '''
        result = self._values.get("log_format")
        return typing.cast(typing.Optional[FlowLogFormat], result)

    @builtins.property
    def max_aggregation_interval(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval]:
        '''The maximum interval of time during which a flow of packets is captured and aggregated into a flow log record.

        :see: `FlowLog MaxAggregationInterval <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-maxaggregationinterval>`_
        :group: Inputs
        '''
        result = self._values.get("max_aggregation_interval")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval], result)

    @builtins.property
    def traffic_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType]:
        '''The type of traffic to monitor (accepted traffic, rejected traffic, or all traffic).

        :see: `FlowLog TrafficType <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-traffictype>`_
        :group: Inputs
        '''
        result = self._values.get("traffic_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.FlowLogS3Options",
    jsii_struct_bases=[],
    name_mapping={
        "file_format": "fileFormat",
        "hive_compatible_partitions": "hiveCompatiblePartitions",
        "key_prefix": "keyPrefix",
        "per_hour_partition": "perHourPartition",
    },
)
class FlowLogS3Options:
    def __init__(
        self,
        *,
        file_format: typing.Optional[FlowLogFileFormat] = None,
        hive_compatible_partitions: typing.Optional[builtins.bool] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        per_hour_partition: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param file_format: The file format in which flow logs should be delivered to S3.
        :param hive_compatible_partitions: Controls the format of partitions ("folders") when the flow logs are delivered to S3. By default, flow logs are delivered partitioned such that each part of the S3 path represents a values pertaining to details of the log. When hive compatible partitions are enabled, partitions will be structured such that keys declaring the partition name are added at each level. An example of standard partitioning:: /us-east-1/2020/03/08/log.tar.gz An example with Hive compatible partitions:: /region=us-east-1/year=2020/month=03/day=08/log.tar.gz
        :param key_prefix: An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.
        :param per_hour_partition: Indicates whether to partition the flow log per hour. By default, flow logs are partitioned (organized into S3 "folders") by day. Setting this to true will add an extra layer of directories splitting flow log files by the hour in which they were delivered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e005d34fc5ab0b60e83479b723ba4e2e86a135e05fd16b18daaac30743245ed)
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument hive_compatible_partitions", value=hive_compatible_partitions, expected_type=type_hints["hive_compatible_partitions"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument per_hour_partition", value=per_hour_partition, expected_type=type_hints["per_hour_partition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_format is not None:
            self._values["file_format"] = file_format
        if hive_compatible_partitions is not None:
            self._values["hive_compatible_partitions"] = hive_compatible_partitions
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if per_hour_partition is not None:
            self._values["per_hour_partition"] = per_hour_partition

    @builtins.property
    def file_format(self) -> typing.Optional[FlowLogFileFormat]:
        '''The file format in which flow logs should be delivered to S3.

        :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[FlowLogFileFormat], result)

    @builtins.property
    def hive_compatible_partitions(self) -> typing.Optional[builtins.bool]:
        '''Controls the format of partitions ("folders") when the flow logs are delivered to S3.

        By default, flow logs are delivered partitioned such that each part of
        the S3 path represents a values pertaining to details of the log.

        When hive compatible partitions are enabled, partitions will be
        structured such that keys declaring the partition name are added at
        each level.

        An example of standard partitioning::

           /us-east-1/2020/03/08/log.tar.gz

        An example with Hive compatible partitions::

           /region=us-east-1/year=2020/month=03/day=08/log.tar.gz

        :see: `AWS Big Data Blog <https://aws.amazon.com/blogs/big-data/optimize-performance-and-reduce-costs-for-network-analytics-with-vpc-flow-logs-in-apache-parquet-format/>`_
        '''
        result = self._values.get("hive_compatible_partitions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        '''An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.

        :see: `FlowLog LogDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination>`_
        '''
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def per_hour_partition(self) -> typing.Optional[builtins.bool]:
        '''Indicates whether to partition the flow log per hour.

        By default, flow logs are partitioned (organized into S3 "folders") by
        day.

        Setting this to true will add an extra layer of directories splitting
        flow log files by the hour in which they were delivered.

        :see: `Flow log files <https://docs.aws.amazon.com/vpc/latest/tgw/flow-logs-s3.html#flow-logs-s3-path>`_
        '''
        result = self._values.get("per_hour_partition")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlowLogS3Options(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-extensions.ec2.ICustomerGateway")
class ICustomerGateway(typing_extensions.Protocol):
    '''Represents a customer gateway in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        '''The BGP ASN of the customer gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        '''The ID of the customer gateway.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> builtins.str:
        '''The IP address of the customer gateway.'''
        ...


class _ICustomerGatewayProxy:
    '''Represents a customer gateway in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ICustomerGateway"

    @builtins.property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        '''The BGP ASN of the customer gateway.'''
        return typing.cast(jsii.Number, jsii.get(self, "customerGatewayAsn"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        '''The ID of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> builtins.str:
        '''The IP address of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayIp"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICustomerGateway).__jsii_proxy_class__ = lambda : _ICustomerGatewayProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ILocalVpnEndpoint")
class ILocalVpnEndpoint(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> "LocalVpnEndpointConfiguration":
        '''Produces a configuration that can be used when configuring the local end of a VPN connection.

        :param scope: The construct configuring the VPN connection that will be referencing the local endpoint.
        '''
        ...


class _ILocalVpnEndpointProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ILocalVpnEndpoint"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> "LocalVpnEndpointConfiguration":
        '''Produces a configuration that can be used when configuring the local end of a VPN connection.

        :param scope: The construct configuring the VPN connection that will be referencing the local endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f7fbf7fd0e305a60cc72790e4c2e467542eeb749b6ca114948036c7e283f4e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("LocalVpnEndpointConfiguration", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILocalVpnEndpoint).__jsii_proxy_class__ = lambda : _ILocalVpnEndpointProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ILogDestination")
class ILogDestination(typing_extensions.Protocol):
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> FlowLogDestinationConfig:
        '''
        :param scope: -
        '''
        ...


class _ILogDestinationProxy:
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ILogDestination"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> FlowLogDestinationConfig:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e7dac1ec2cefa56a83155a4b3ff82206bfe5b1607d5af572c5d16cf98aba7a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(FlowLogDestinationConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILogDestination).__jsii_proxy_class__ = lambda : _ILogDestinationProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.IRemoteVpnEndpoint")
class IRemoteVpnEndpoint(typing_extensions.Protocol):
    '''An object that can be used to retrieve the details for the remote end of a VPN connection.'''

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> "RemoteVpnEndpointConfiguration":
        '''Produces a configuration that can be used when configuring the remote end of a VPN connection.

        :param scope: The construct configuring the VPN connection that will be referencing the remote endpoint.
        '''
        ...


class _IRemoteVpnEndpointProxy:
    '''An object that can be used to retrieve the details for the remote end of a VPN connection.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.IRemoteVpnEndpoint"

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> "RemoteVpnEndpointConfiguration":
        '''Produces a configuration that can be used when configuring the remote end of a VPN connection.

        :param scope: The construct configuring the VPN connection that will be referencing the remote endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c8cc16017de426ad6eb532d21e5db4c058f7a279485763c47026f54ff6b02a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("RemoteVpnEndpointConfiguration", jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRemoteVpnEndpoint).__jsii_proxy_class__ = lambda : _IRemoteVpnEndpointProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ITransitGateway")
class ITransitGateway(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Represents a transit gateway in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="addRouteTable")
    def add_route_table(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayRouteTable":
        '''
        :param name: 
        '''
        ...

    @jsii.member(jsii_name="addVpn")
    def add_vpn(
        self,
        id: builtins.str,
        *,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union["TunnelOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "VpnConnection":
        '''
        :param id: -
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 
        '''
        ...

    @jsii.member(jsii_name="attachVpc")
    def attach_vpc(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        *,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "TransitGatewayAttachment":
        '''
        :param vpc: -
        :param name: 
        :param subnets: 
        '''
        ...


class _ITransitGatewayProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Represents a transit gateway in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ITransitGateway"

    @builtins.property
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayId"))

    @jsii.member(jsii_name="addRouteTable")
    def add_route_table(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayRouteTable":
        '''
        :param name: 
        '''
        options = TransitGatewayRouteTableOptions(name=name)

        return typing.cast("TransitGatewayRouteTable", jsii.invoke(self, "addRouteTable", [options]))

    @jsii.member(jsii_name="addVpn")
    def add_vpn(
        self,
        id: builtins.str,
        *,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union["TunnelOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "VpnConnection":
        '''
        :param id: -
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c530d4e033cb58d409cbdec91a29a99e796c6b5949a8fe0b776e9a57ebda677)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = VpnAttachmentOptions(
            remote_endpoint=remote_endpoint,
            connection_type=connection_type,
            static_routes_only=static_routes_only,
            tunnel_configurations=tunnel_configurations,
        )

        return typing.cast("VpnConnection", jsii.invoke(self, "addVpn", [id, options]))

    @jsii.member(jsii_name="attachVpc")
    def attach_vpc(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        *,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "TransitGatewayAttachment":
        '''
        :param vpc: -
        :param name: 
        :param subnets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e51602274287d74df7ba0b1c9462a003ef4081742f553f9fccc7d78f9e0f591)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        options = VpcAttachmentOptions(name=name, subnets=subnets)

        return typing.cast("TransitGatewayAttachment", jsii.invoke(self, "attachVpc", [vpc, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransitGateway).__jsii_proxy_class__ = lambda : _ITransitGatewayProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ITransitGatewayAttachment")
class ITransitGatewayAttachment(typing_extensions.Protocol):
    '''Represents a Transit Gateway Attachment in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of the transit gateway attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of the transit gateway attachment.'''
        ...

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        cidr: builtins.str,
        route_table: "ITransitGatewayRouteTable",
    ) -> "ITransitGatewayRoute":
        '''Adds a route that directs traffic to this transit gateway attachment.

        :param cidr: CIDR range that should be routed to this attachment.
        :param route_table: The transit gateway route table where the route should be added.

        :return: The TransitGatewayRoute that was added.
        '''
        ...


class _ITransitGatewayAttachmentProxy:
    '''Represents a Transit Gateway Attachment in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ITransitGatewayAttachment"

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of the transit gateway attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of the transit gateway attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        cidr: builtins.str,
        route_table: "ITransitGatewayRouteTable",
    ) -> "ITransitGatewayRoute":
        '''Adds a route that directs traffic to this transit gateway attachment.

        :param cidr: CIDR range that should be routed to this attachment.
        :param route_table: The transit gateway route table where the route should be added.

        :return: The TransitGatewayRoute that was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b44f941842017d2d4c6c21860f08701108fc8a70636475b6b9ab6eb37332692)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
        return typing.cast("ITransitGatewayRoute", jsii.invoke(self, "addRoute", [cidr, route_table]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransitGatewayAttachment).__jsii_proxy_class__ = lambda : _ITransitGatewayAttachmentProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ITransitGatewayPeeringAttachment")
class ITransitGatewayPeeringAttachment(
    ITransitGatewayAttachment,
    typing_extensions.Protocol,
):
    '''Represents a transit gateway route table in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentCreationTime")
    def transit_gateway_attachment_creation_time(self) -> builtins.str:
        '''The time the transit gateway peering attachment was created.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentState")
    def transit_gateway_attachment_state(self) -> builtins.str:
        '''The state of the transit gateway peering attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatus")
    def transit_gateway_attachment_status(self) -> builtins.str:
        '''The status of the transit gateway peering attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusCode")
    def transit_gateway_attachment_status_code(self) -> builtins.str:
        '''The status code for the current status of the attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusMessage")
    def transit_gateway_attachment_status_message(self) -> builtins.str:
        '''The status message for the current status of the attachment.'''
        ...


class _ITransitGatewayPeeringAttachmentProxy(
    jsii.proxy_for(ITransitGatewayAttachment), # type: ignore[misc]
):
    '''Represents a transit gateway route table in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ITransitGatewayPeeringAttachment"

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentCreationTime")
    def transit_gateway_attachment_creation_time(self) -> builtins.str:
        '''The time the transit gateway peering attachment was created.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentState")
    def transit_gateway_attachment_state(self) -> builtins.str:
        '''The state of the transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentState"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatus")
    def transit_gateway_attachment_status(self) -> builtins.str:
        '''The status of the transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatus"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusCode")
    def transit_gateway_attachment_status_code(self) -> builtins.str:
        '''The status code for the current status of the attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatusCode"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusMessage")
    def transit_gateway_attachment_status_message(self) -> builtins.str:
        '''The status message for the current status of the attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatusMessage"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransitGatewayPeeringAttachment).__jsii_proxy_class__ = lambda : _ITransitGatewayPeeringAttachmentProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ITransitGatewayRoute")
class ITransitGatewayRoute(typing_extensions.Protocol):
    '''Represents a Transit Gateway Route in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteId")
    def transit_gateway_route_id(self) -> builtins.str:
        '''The ID of the Transit Gateway Route.'''
        ...


class _ITransitGatewayRouteProxy:
    '''Represents a Transit Gateway Route in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ITransitGatewayRoute"

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteId")
    def transit_gateway_route_id(self) -> builtins.str:
        '''The ID of the Transit Gateway Route.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransitGatewayRoute).__jsii_proxy_class__ = lambda : _ITransitGatewayRouteProxy


@jsii.interface(jsii_type="cdk-extensions.ec2.ITransitGatewayRouteTable")
class ITransitGatewayRouteTable(typing_extensions.Protocol):
    '''Represents a transit gateway route table in AWS.'''

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableArn")
    def transit_gateway_route_table_arn(self) -> builtins.str:
        '''The ARN of the transit gateway route table.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> builtins.str:
        '''The ID of the transit gateway route table.'''
        ...

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        *,
        cidr: builtins.str,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayRoute":
        '''Adds a route to this transit gateway route table.

        :param cidr: The CIDR range to match for the route.
        :param attachment: The transit gateway attachment where matched traffic should be routed.
        :param blackhole: Whether the traffic should be black holed (discarded) rather than being routed to an attachment.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        ...


class _ITransitGatewayRouteTableProxy:
    '''Represents a transit gateway route table in AWS.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.ec2.ITransitGatewayRouteTable"

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableArn")
    def transit_gateway_route_table_arn(self) -> builtins.str:
        '''The ARN of the transit gateway route table.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteTableArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> builtins.str:
        '''The ID of the transit gateway route table.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteTableId"))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        *,
        cidr: builtins.str,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayRoute":
        '''Adds a route to this transit gateway route table.

        :param cidr: The CIDR range to match for the route.
        :param attachment: The transit gateway attachment where matched traffic should be routed.
        :param blackhole: Whether the traffic should be black holed (discarded) rather than being routed to an attachment.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        options = TransitGatewayRouteOptions(
            cidr=cidr,
            attachment=attachment,
            blackhole=blackhole,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("TransitGatewayRoute", jsii.invoke(self, "addRoute", [options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITransitGatewayRouteTable).__jsii_proxy_class__ = lambda : _ITransitGatewayRouteTableProxy


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.LocalVpnEndpointConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "transit_gateway_id": "transitGatewayId",
        "vpn_gateway_id": "vpnGatewayId",
    },
)
class LocalVpnEndpointConfiguration:
    def __init__(
        self,
        *,
        transit_gateway_id: typing.Optional[builtins.str] = None,
        vpn_gateway_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration object containing the vlues needed to configure the local end of a VPN connection.

        :param transit_gateway_id: The ID of the transit gateway that serves as the local end of the VPN connection.
        :param vpn_gateway_id: The ID of the VPN gateway that serves as the local end of the VPN connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c283c95ccb48c40fb03d7fffd4f63ce7927ef657d47052d65ed9aa32cbd6609a)
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
            check_type(argname="argument vpn_gateway_id", value=vpn_gateway_id, expected_type=type_hints["vpn_gateway_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if transit_gateway_id is not None:
            self._values["transit_gateway_id"] = transit_gateway_id
        if vpn_gateway_id is not None:
            self._values["vpn_gateway_id"] = vpn_gateway_id

    @builtins.property
    def transit_gateway_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the transit gateway that serves as the local end of the VPN connection.'''
        result = self._values.get("transit_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_gateway_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPN gateway that serves as the local end of the VPN connection.'''
        result = self._values.get("vpn_gateway_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalVpnEndpointConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NatProvider(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.ec2.NatProvider"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="gateway")
    @builtins.classmethod
    def gateway(
        cls,
        *,
        eip_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        '''
        :param eip_allocation_ids: EIP allocation IDs for the NAT gateways. Default: - No fixed EIPs allocated for the NAT gateways
        '''
        props = _aws_cdk_aws_ec2_ceddda9d.NatGatewayProps(
            eip_allocation_ids=eip_allocation_ids
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.sinvoke(cls, "gateway", [props]))

    @jsii.member(jsii_name="instance")
    @builtins.classmethod
    def instance(
        cls,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        default_allowed_traffic: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.NatTrafficDirection] = None,
        key_name: typing.Optional[builtins.str] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    ) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        '''
        :param instance_type: Instance type of the NAT instance.
        :param default_allowed_traffic: Direction to allow all traffic through the NAT instance by default. By default, inbound and outbound traffic is allowed. If you set this to another value than INBOUND_AND_OUTBOUND, you must configure the NAT instance's security groups in another way, either by passing in a fully configured Security Group using the ``securityGroup`` property, or by configuring it using the ``.securityGroup`` or ``.connections`` members after passing the NAT Instance Provider to a Vpc. Default: NatTrafficDirection.INBOUND_AND_OUTBOUND
        :param key_name: Name of SSH keypair to grant access to instance. Default: - No SSH access will be possible.
        :param machine_image: The machine image (AMI) to use. By default, will do an AMI lookup for the latest NAT instance image. If you have a specific AMI ID you want to use, pass a ``GenericLinuxImage``. For example:: ec2.NatProvider.instance({ instanceType: new ec2.InstanceType('t3.micro'), machineImage: new ec2.GenericLinuxImage({ 'us-east-2': 'ami-0f9c61b5a562a16af' }) }) Default: - Latest NAT instance image
        :param security_group: Security Group for NAT instances. Default: - A new security group will be created
        '''
        props = _aws_cdk_aws_ec2_ceddda9d.NatInstanceProps(
            instance_type=instance_type,
            default_allowed_traffic=default_allowed_traffic,
            key_name=key_name,
            machine_image=machine_image,
            security_group=security_group,
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.sinvoke(cls, "instance", [props]))

    @jsii.member(jsii_name="transitGateway")
    @builtins.classmethod
    def transit_gateway(
        cls,
        *,
        transit_gateway: ITransitGateway,
    ) -> _aws_cdk_aws_ec2_ceddda9d.NatProvider:
        '''
        :param transit_gateway: 
        '''
        props = TransitGatewayNatProviderOptions(transit_gateway=transit_gateway)

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.NatProvider, jsii.sinvoke(cls, "transitGateway", [props]))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.RemoteVpnEndpointConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway_asn": "customerGatewayAsn",
        "customer_gateway_id": "customerGatewayId",
        "customer_gateway_ip": "customerGatewayIp",
    },
)
class RemoteVpnEndpointConfiguration:
    def __init__(
        self,
        *,
        customer_gateway_asn: jsii.Number,
        customer_gateway_id: builtins.str,
        customer_gateway_ip: builtins.str,
    ) -> None:
        '''Configuration object containing the vlues needed to configure the remote end of a VPN connection.

        :param customer_gateway_asn: The BGP ASN of the customer gateway which is configured with the details of the remote endpoint device.
        :param customer_gateway_id: The ID of the customer gateway which is configured with the details of the remote endpoint device.
        :param customer_gateway_ip: The IP address of the customer gateway which is configured with the details of the remote endpoint device.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8914f39fbdc8cc3e17d3f0de803ae8f59bb0822173529944b495b0fe17106662)
            check_type(argname="argument customer_gateway_asn", value=customer_gateway_asn, expected_type=type_hints["customer_gateway_asn"])
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
            check_type(argname="argument customer_gateway_ip", value=customer_gateway_ip, expected_type=type_hints["customer_gateway_ip"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "customer_gateway_asn": customer_gateway_asn,
            "customer_gateway_id": customer_gateway_id,
            "customer_gateway_ip": customer_gateway_ip,
        }

    @builtins.property
    def customer_gateway_asn(self) -> jsii.Number:
        '''The BGP ASN of the customer gateway which is configured with the details of the remote endpoint device.'''
        result = self._values.get("customer_gateway_asn")
        assert result is not None, "Required property 'customer_gateway_asn' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def customer_gateway_id(self) -> builtins.str:
        '''The ID of the customer gateway which is configured with the details of the remote endpoint device.'''
        result = self._values.get("customer_gateway_id")
        assert result is not None, "Required property 'customer_gateway_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_gateway_ip(self) -> builtins.str:
        '''The IP address of the customer gateway which is configured with the details of the remote endpoint device.'''
        result = self._values.get("customer_gateway_ip")
        assert result is not None, "Required property 'customer_gateway_ip' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteVpnEndpointConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.SharingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_external_principals": "allowExternalPrincipals",
        "auto_discover_accounts": "autoDiscoverAccounts",
        "principals": "principals",
    },
)
class SharingOptions:
    def __init__(
        self,
        *,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_discover_accounts: typing.Optional[builtins.bool] = None,
        principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> None:
        '''
        :param allow_external_principals: 
        :param auto_discover_accounts: 
        :param principals: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d7430c10280f3e429f967b91e374da316928ba959b852656888cb4465f871ab)
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument auto_discover_accounts", value=auto_discover_accounts, expected_type=type_hints["auto_discover_accounts"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if auto_discover_accounts is not None:
            self._values["auto_discover_accounts"] = auto_discover_accounts
        if principals is not None:
            self._values["principals"] = principals

    @builtins.property
    def allow_external_principals(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_discover_accounts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_discover_accounts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[_ISharedPrincipal_9cde791b]]:
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[_ISharedPrincipal_9cde791b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SharingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IIpAddresses)
class TieredSubnets(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TieredSubnets",
):
    def __init__(self, options: "TieredSubnetsOptions") -> None:
        '''
        :param options: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8e89adfc6dfc2ac55a0bed117d1dc5d9b5bc0bcf75bb19367a28bd1c914be4e)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="allocateSubnetsCidr")
    def allocate_subnets_cidr(
        self,
        *,
        requested_subnets: typing.Sequence[typing.Union[_aws_cdk_aws_ec2_ceddda9d.RequestedSubnet, typing.Dict[builtins.str, typing.Any]]],
        vpc_cidr: builtins.str,
    ) -> _aws_cdk_aws_ec2_ceddda9d.SubnetIpamOptions:
        '''Called by the VPC to retrieve Subnet options from the Ipam

Don't call this directly, the VPC will call it automatically.

        :param requested_subnets: The Subnets to be allocated.
        :param vpc_cidr: The IPv4 CIDR block for this Vpc.
        '''
        input = _aws_cdk_aws_ec2_ceddda9d.AllocateCidrRequest(
            requested_subnets=requested_subnets, vpc_cidr=vpc_cidr
        )

        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetIpamOptions, jsii.invoke(self, "allocateSubnetsCidr", [input]))

    @jsii.member(jsii_name="allocateVpcCidr")
    def allocate_vpc_cidr(self) -> _aws_cdk_aws_ec2_ceddda9d.VpcIpamOptions:
        '''Called by the VPC to retrieve VPC options from the Ipam

Don't call this directly, the VPC will call it automatically.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.VpcIpamOptions, jsii.invoke(self, "allocateVpcCidr", []))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="tierMask")
    def tier_mask(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierMask"))


class TieredSubnetsOptions(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TieredSubnetsOptions",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="tierMask")
    def tier_mask(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tierMask"))


@jsii.implements(ITransitGateway)
class TransitGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGateway",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
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
    ) -> None:
        '''Creates a new instance of the Database class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
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
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b0aca7557ca99e67ff904b7cb9edf704abd3cf24b45ecad18d9ccffdb7fcdc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayProps(
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

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTransitGatewayId")
    @builtins.classmethod
    def from_transit_gateway_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        transit_gateway_id: builtins.str,
    ) -> ITransitGateway:
        '''
        :param scope: -
        :param id: -
        :param transit_gateway_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46c3cc263035d23bc511197c75afb01d4a672fd46f5af176fbea6a400bccd00b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_id", value=transit_gateway_id, expected_type=type_hints["transit_gateway_id"])
        return typing.cast(ITransitGateway, jsii.sinvoke(cls, "fromTransitGatewayId", [scope, id, transit_gateway_id]))

    @jsii.member(jsii_name="addCidrBlock")
    def add_cidr_block(self, cidr: builtins.str) -> None:
        '''
        :param cidr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2efd1666acd64cb987a354787ffd07add5920ed5de7e64ad3a01aa00619b7310)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
        return typing.cast(None, jsii.invoke(self, "addCidrBlock", [cidr]))

    @jsii.member(jsii_name="addRouteTable")
    def add_route_table(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayRouteTable":
        '''Creates a new Transit Gateway Route Table for this Transit Gateway.

        :param name: 

        :return: The newly created Transit Gateway Route Table.
        '''
        options = TransitGatewayRouteTableOptions(name=name)

        return typing.cast("TransitGatewayRouteTable", jsii.invoke(self, "addRouteTable", [options]))

    @jsii.member(jsii_name="addVpn")
    def add_vpn(
        self,
        id: builtins.str,
        *,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union["TunnelOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "VpnConnection":
        '''Creates a new VPN connection that terminates on the AWS side at this Transit Gateway.

        :param id: A unique identifier for this VPN connection. Must be unique within the context of scope.
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 

        :return: The VPN connection that was created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9989ffc3141ccddce9a6e8246aa4b31bd76f3ad0a11bbc1cbee86d607e50200d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = VpnAttachmentOptions(
            remote_endpoint=remote_endpoint,
            connection_type=connection_type,
            static_routes_only=static_routes_only,
            tunnel_configurations=tunnel_configurations,
        )

        return typing.cast("VpnConnection", jsii.invoke(self, "addVpn", [id, options]))

    @jsii.member(jsii_name="attachPeer")
    def attach_peer(
        self,
        peer: ITransitGateway,
        *,
        name: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> "TransitGatewayPeeringAttachment":
        '''Creates a new transit gateway peering attachment for this transit gateway.

        :param peer: The remote transit gateway to create the peering connection with.
        :param name: The name of the transit gateway peering attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param peer_account_id: The account that contains the transit gateway being peered with.
        :param peer_region: The region that contains the transit gateway being peered with.

        :return: The newly created TransitGatewayPeeringAttachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fca635a725c4277e8db84123074663ecf20e88af86d11cb8f03c6390d8b7bc8)
            check_type(argname="argument peer", value=peer, expected_type=type_hints["peer"])
        options = TransitGatewayPeeringAttachmentOptions(
            name=name, peer_account_id=peer_account_id, peer_region=peer_region
        )

        return typing.cast("TransitGatewayPeeringAttachment", jsii.invoke(self, "attachPeer", [peer, options]))

    @jsii.member(jsii_name="attachVpc")
    def attach_vpc(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        *,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> "TransitGatewayAttachment":
        '''Creates a new VPC transit gateway attachment for this transit gateway.

        :param vpc: The VPC to connect to this Transit Gateway.
        :param name: 
        :param subnets: 

        :return: The newly created TransitGatewayAttachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac3f5d6f3de4328a56c1673d48d7168afe72b9b6c52725fb46ee3d5121211524)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        options = VpcAttachmentOptions(name=name, subnets=subnets)

        return typing.cast("TransitGatewayAttachment", jsii.invoke(self, "attachVpc", [vpc, options]))

    @jsii.member(jsii_name="enableSharing")
    def enable_sharing(
        self,
        *,
        allow_external_principals: typing.Optional[builtins.bool] = None,
        auto_discover_accounts: typing.Optional[builtins.bool] = None,
        principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
    ) -> _ResourceShare_f0180713:
        '''
        :param allow_external_principals: 
        :param auto_discover_accounts: 
        :param principals: 
        '''
        options = SharingOptions(
            allow_external_principals=allow_external_principals,
            auto_discover_accounts=auto_discover_accounts,
            principals=principals,
        )

        return typing.cast(_ResourceShare_f0180713, jsii.invoke(self, "enableSharing", [options]))

    @builtins.property
    @jsii.member(jsii_name="autoAcceptSharedAttachments")
    def auto_accept_shared_attachments(self) -> builtins.bool:
        '''Enable or disable automatic acceptance of attachment requests.

        When enabled any new transit gateway attachments that are created in other
        accounts via a resource share will be accepted automatically. Otherwise,
        manual intervention will be required to approve all new attachments.

        This is disabled by default to maintain the highest levels of security,
        however enabling should be strongly considered as without this full
        automation of infrastructure will not be possible for cross account
        setups.

        :see: `Accept a shared attachment <https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html#tgw-accept-shared-attachment>`_
        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "autoAcceptSharedAttachments"))

    @builtins.property
    @jsii.member(jsii_name="defaultRouteTableAssociation")
    def default_route_table_association(self) -> builtins.bool:
        '''Enable or disable automatic association with the default association route table.

        When enabled, all new attachments that are accepted will be automatically
        associated with the default association route table. By default this is
        the route table that is created automatically when the transit gateway is
        created.

        :see: `TransitGateway.DefaultRouteTableAssociation <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-defaultroutetableassociation>`_
        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "defaultRouteTableAssociation"))

    @builtins.property
    @jsii.member(jsii_name="defaultRouteTablePropagation")
    def default_route_table_propagation(self) -> builtins.bool:
        '''Enable or disable automatic propagation of routes to the default propagation route table.

        When a new attachment is accepted, the routes associated with that
        attachment will automatically be added to the default propagation route
        table. By default this is the route table that is created automatically
        when the transit gateway is created.

        :see: `Route propagation <https://docs.aws.amazon.com/vpc/latest/tgw/how-transit-gateways-work.html#tgw-route-propagation-overview>`_
        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "defaultRouteTablePropagation"))

    @builtins.property
    @jsii.member(jsii_name="dnsSupport")
    def dns_support(self) -> builtins.bool:
        '''Enable or disable DNS support.

        When DNS support is enabled on a transit gateway, VPC DNS resolution in
        attached VPC's will automatically resolve public IP addresses from other
        VPC's to their provate IP address equivalent.

        :see: `Create a transit gateway <https://docs.aws.amazon.com/vpc/latest/tgw/tgw-transit-gateways.html#create-tgw>`_
        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "dnsSupport"))

    @builtins.property
    @jsii.member(jsii_name="multicastSupport")
    def multicast_support(self) -> builtins.bool:
        '''Indicates whether multicast is enabled on the transit gateway.

        :see: `Multicast reference architectures <https://d1.awsstatic.com/architecture-diagrams/ArchitectureDiagrams/transitgateway_multicast_ra.pdf?did=wp_card&trk=wp_card>`_
        :group: Inputs
        '''
        return typing.cast(builtins.bool, jsii.get(self, "multicastSupport"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway:
        '''The underlying TransitGateway CloudFormation resource.

        :see: `AWS::EC2::TransitGateway <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGateway, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayArn")
    def transit_gateway_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> builtins.str:
        '''The ID of this Transit Gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="amazonSideAsn")
    def amazon_side_asn(self) -> typing.Optional[jsii.Number]:
        '''A private Autonomous System Number (ASN) for the Amazon side of a BGP session.

        The range is 64512 to 65534 for 16-bit ASNs.

        :see: `TransitGateway.AmazonSideAsn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-amazonsideasn>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "amazonSideAsn"))

    @builtins.property
    @jsii.member(jsii_name="defaultRouteTable")
    def default_route_table(self) -> typing.Optional[ITransitGatewayRouteTable]:
        '''The default route table that got created along with the Transit Gateway.

        This information is not exposed by CloudFormation. As such, this resource
        will only be available if the default reoute table ID is passed in.

        :group: Resources
        '''
        return typing.cast(typing.Optional[ITransitGatewayRouteTable], jsii.get(self, "defaultRouteTable"))

    @builtins.property
    @jsii.member(jsii_name="defaultRouteTableId")
    def default_route_table_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the default route table that was created with the transit gateway.

        This route table is critical to some transit gateway architectures and is
        not exposed by CloudFormation.

        Passing in the ID of the default route table will make an object available
        that represents it and can be used for further operations.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultRouteTableId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the transit gateway.

        :see: `TransitGateway.Description <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-description>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway.

        Used to tag the transit gateway with a name that will be displayed in the
        AWS VPC console.

        :see: `TransitGateway.Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-tags>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="resourceShare")
    def resource_share(self) -> typing.Optional[_ResourceShare_f0180713]:
        '''The RAM resource share that is used for sharing the transit gateway with other accounts.

        :group: Resources
        '''
        return typing.cast(typing.Optional[_ResourceShare_f0180713], jsii.get(self, "resourceShare"))

    @builtins.property
    @jsii.member(jsii_name="vpnEcmpSupport")
    def vpn_ecmp_support(self) -> typing.Optional[builtins.bool]:
        '''Enable or disable Equal Cost Multipath Protocol support.

        :see: `Achieve ECMP with multiple VPN tunnels <https://aws.amazon.com/premiumsupport/knowledge-center/transit-gateway-ecmp-multiple-tunnels/>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "vpnEcmpSupport"))


@jsii.implements(ITransitGatewayAttachment)
class TransitGatewayAttachmentBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.ec2.TransitGatewayAttachmentBase",
):
    '''A base class providing common functionality between created and imported Transit Gateway Attachments.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b49d47ed81c7ffb2a1650ef26c6a7262dbfbe5b02d6a33f4521aaba40facd96b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        cidr: builtins.str,
        route_table: ITransitGatewayRouteTable,
    ) -> ITransitGatewayRoute:
        '''Adds a route that directs traffic to this transit gateway attachment.

        :param cidr: CIDR range that should be routed to this attachment.
        :param route_table: The transit gateway route table where the route should be added.

        :return: The TransitGatewayRoute that was added.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4b8aae9fc7113caa263f0a78c3a90cd7457571433a27e89da36b0ae99fc4c6)
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
        return typing.cast(ITransitGatewayRoute, jsii.invoke(self, "addRoute", [cidr, route_table]))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    @abc.abstractmethod
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway Attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    @abc.abstractmethod
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The name of this Transit Gateway Attachment.'''
        ...


class _TransitGatewayAttachmentBaseProxy(
    TransitGatewayAttachmentBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The name of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TransitGatewayAttachmentBase).__jsii_proxy_class__ = lambda : _TransitGatewayAttachmentBaseProxy


class TransitGatewayAttachmentResource(
    TransitGatewayAttachmentBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.ec2.TransitGatewayAttachmentResource",
):
    '''Attaches a VPC to a transit gateway.

    If you attach a VPC with a CIDR range that overlaps the CIDR range of a VPC
    that is already attached, the new VPC CIDR range is not propagated to the
    default propagation route table.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        transit_gateway: ITransitGateway,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        appliance_mode_support: typing.Optional[builtins.bool] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        ipv6_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayAttachment class.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway: The transit gateway for which the attachment should be created.
        :param vpc: The VPC where the attachment should be created.
        :param appliance_mode_support: Enables appliance mode on the attachment. When appliance mode is enabled, all traffic flowing between attachments is forwarded to an appliance in a shared VPC to be inspected and processed.
        :param dns_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param ipv6_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param name: The name of the Transit Gateway Attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param subnets: The subnets where the attachment should be created. Can select up to one subnet per Availability Zone.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06c53aa420590eceea4fb9b075681a4977d93106ad928386f59f565ada883d5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayAttachmentResourceProps(
            transit_gateway=transit_gateway,
            vpc=vpc,
            appliance_mode_support=appliance_mode_support,
            dns_support=dns_support,
            ipv6_support=ipv6_support,
            name=name,
            subnets=subnets,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="translateBoolean")
    def _translate_boolean(
        self,
        val: typing.Optional[builtins.bool] = None,
    ) -> typing.Optional[builtins.str]:
        '''Translates a boolean input into the strings used by the transit gateway attachment resource to implement boolean values.

        :param val: The input value to translate.

        :return:

        The string used to reprersent the input boolean or undefined if
        the input boolean is undefined.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9616ce11448deda7c7f7a6abcc3dc7343fd9d23bf7197f988d750a4ed8ab7b9)
            check_type(argname="argument val", value=val, expected_type=type_hints["val"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "translateBoolean", [val]))

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''The subnets where the attachment should be created.

        Can select up to one subnet per Availability Zone.

        :see: `TransitGatewayVpcAttachment SubnetIds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-subnetids>`_
        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, jsii.get(self, "subnets"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway for which the attachment should be created.

        :group: Inputs
        '''
        return typing.cast(ITransitGateway, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    @abc.abstractmethod
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway Attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    @abc.abstractmethod
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of this Transit Gateway Attachment.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC where the attachment should be created.

        :see: `TransitGatewayVpcAttachment VpcId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-vpcid>`_
        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="applianceModeSupport")
    def appliance_mode_support(self) -> typing.Optional[builtins.bool]:
        '''Enables appliance mode on the attachment.

        When appliance mode is enabled, all traffic flowing between attachments is
        forwarded to an appliance in a shared VPC to be inspected and processed.

        :see: `Appliance in a shared services VPC <https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "applianceModeSupport"))

    @builtins.property
    @jsii.member(jsii_name="dnsSupport")
    def dns_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `TransitGatewayVpcAttachment DnsSupport <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-transitgatewayvpcattachment-options.html#cfn-ec2-transitgatewayvpcattachment-options-dnssupport>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "dnsSupport"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Support")
    def ipv6_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `IPv6 connectivity with TransitGateway <https://docs.aws.amazon.com/whitepapers/latest/ipv6-on-aws/amazon-vpc-connectivity-options-for-ipv6.html#ipv6-connectivity-with-transit-gateway>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ipv6Support"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Transit Gateway Attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayVpcAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-tags>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))


class _TransitGatewayAttachmentResourceProxy(
    TransitGatewayAttachmentResource,
    jsii.proxy_for(TransitGatewayAttachmentBase), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TransitGatewayAttachmentResource).__jsii_proxy_class__ = lambda : _TransitGatewayAttachmentResourceProxy


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayAttachmentResourceProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "transit_gateway": "transitGateway",
        "vpc": "vpc",
        "appliance_mode_support": "applianceModeSupport",
        "dns_support": "dnsSupport",
        "ipv6_support": "ipv6Support",
        "name": "name",
        "subnets": "subnets",
    },
)
class TransitGatewayAttachmentResourceProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        transit_gateway: ITransitGateway,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        appliance_mode_support: typing.Optional[builtins.bool] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        ipv6_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration for TransitGatewayAttachmentResource resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param transit_gateway: The transit gateway for which the attachment should be created.
        :param vpc: The VPC where the attachment should be created.
        :param appliance_mode_support: Enables appliance mode on the attachment. When appliance mode is enabled, all traffic flowing between attachments is forwarded to an appliance in a shared VPC to be inspected and processed.
        :param dns_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param ipv6_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param name: The name of the Transit Gateway Attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param subnets: The subnets where the attachment should be created. Can select up to one subnet per Availability Zone.
        '''
        if isinstance(subnets, dict):
            subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d1c15189bbc90871ac0f1cb7928d7a06dc7a543bed65a3917a78189021d8767)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument appliance_mode_support", value=appliance_mode_support, expected_type=type_hints["appliance_mode_support"])
            check_type(argname="argument dns_support", value=dns_support, expected_type=type_hints["dns_support"])
            check_type(argname="argument ipv6_support", value=ipv6_support, expected_type=type_hints["ipv6_support"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway": transit_gateway,
            "vpc": vpc,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if appliance_mode_support is not None:
            self._values["appliance_mode_support"] = appliance_mode_support
        if dns_support is not None:
            self._values["dns_support"] = dns_support
        if ipv6_support is not None:
            self._values["ipv6_support"] = ipv6_support
        if name is not None:
            self._values["name"] = name
        if subnets is not None:
            self._values["subnets"] = subnets

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
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway for which the attachment should be created.

        :see: `TransitGatewayVpcAttachment TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-transitgatewayid>`_
        '''
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC where the attachment should be created.

        :see: `TransitGatewayVpcAttachment VpcId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-vpcid>`_
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def appliance_mode_support(self) -> typing.Optional[builtins.bool]:
        '''Enables appliance mode on the attachment.

        When appliance mode is enabled, all traffic flowing between attachments is
        forwarded to an appliance in a shared VPC to be inspected and processed.

        :see: `Appliance in a shared services VPC <https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html>`_
        '''
        result = self._values.get("appliance_mode_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dns_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `TransitGatewayVpcAttachment DnsSupport <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-transitgatewayvpcattachment-options.html#cfn-ec2-transitgatewayvpcattachment-options-dnssupport>`_
        '''
        result = self._values.get("dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipv6_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `IPv6 connectivity with TransitGateway <https://docs.aws.amazon.com/whitepapers/latest/ipv6-on-aws/amazon-vpc-connectivity-options-for-ipv6.html#ipv6-connectivity-with-transit-gateway>`_
        '''
        result = self._values.get("ipv6_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Transit Gateway Attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayVpcAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-tags>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The subnets where the attachment should be created.

        Can select up to one subnet per Availability Zone.

        :see: `TransitGatewayVpcAttachment SubnetIds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-subnetids>`_
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayAttachmentResourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ILocalVpnEndpoint)
class TransitGatewayLocalVpnEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayLocalVpnEndpoint",
):
    '''Specifies a VPN connection endpoint which routes to a transit gateway on the AWS side.'''

    def __init__(self, transit_gateway: ITransitGateway) -> None:
        '''Creates a new instance of the TransitGatewayLocalVpnEndpoint class.

        :param transit_gateway: The transit gateway that serves as the local end of a VPN connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__085d2039b0a4b4caf19e1943608efeb5e97be1be7d732ad9e6c87845449f8c0e)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
        jsii.create(self.__class__, self, [transit_gateway])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> LocalVpnEndpointConfiguration:
        '''Produces a configuration that can be used when configuring the local end of a VPN connection.

        :param _scope: The construct configuring the VPN connection that will be referencing the local endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1649477704b8d5959bab11d00a58a0814e904ca0755f79fc92c902b7548831e8)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(LocalVpnEndpointConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway that serves as the local end of a VPN connection.

        :group: Inputs
        '''
        return typing.cast(ITransitGateway, jsii.get(self, "transitGateway"))


class TransitGatewayNatProvider(
    _aws_cdk_aws_ec2_ceddda9d.NatProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayNatProvider",
):
    def __init__(self, *, transit_gateway: ITransitGateway) -> None:
        '''
        :param transit_gateway: 
        '''
        options = TransitGatewayNatProviderOptions(transit_gateway=transit_gateway)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="configureNat")
    def configure_nat(
        self,
        *,
        nat_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PublicSubnet],
        private_subnets: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.PrivateSubnet],
        vpc: _aws_cdk_aws_ec2_ceddda9d.Vpc,
    ) -> None:
        '''Called by the VPC to configure NAT

Don't call this directly, the VPC will call it automatically.

        :param nat_subnets: The public subnets where the NAT providers need to be placed.
        :param private_subnets: The private subnets that need to route through the NAT providers. There may be more private subnets than public subnets with NAT providers.
        :param vpc: The VPC we're configuring NAT for.
        '''
        options = _aws_cdk_aws_ec2_ceddda9d.ConfigureNatOptions(
            nat_subnets=nat_subnets, private_subnets=private_subnets, vpc=vpc
        )

        return typing.cast(None, jsii.invoke(self, "configureNat", [options]))

    @jsii.member(jsii_name="configureSubnet")
    def configure_subnet(self, subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet) -> None:
        '''Configures subnet with the gateway

Don't call this directly, the VPC will call it automatically.

        :param subnet: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce5b6c12f42e572c0fd8116f08202bd45321782d0dface0d78758e8ae4afce0)
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        return typing.cast(None, jsii.invoke(self, "configureSubnet", [subnet]))

    @builtins.property
    @jsii.member(jsii_name="configuredGateways")
    def configured_gateways(
        self,
    ) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig]:
        '''Return list of gateways spawned by the provider.'''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.GatewayConfig], jsii.get(self, "configuredGateways"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> ITransitGateway:
        return typing.cast(ITransitGateway, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachment")
    def transit_gateway_attachment(self) -> typing.Optional["TransitGatewayAttachment"]:
        return typing.cast(typing.Optional["TransitGatewayAttachment"], jsii.get(self, "transitGatewayAttachment"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayNatProviderOptions",
    jsii_struct_bases=[],
    name_mapping={"transit_gateway": "transitGateway"},
)
class TransitGatewayNatProviderOptions:
    def __init__(self, *, transit_gateway: ITransitGateway) -> None:
        '''
        :param transit_gateway: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d866260e3cfdb20c411a4b77ce2ef5ed9046a68ea0356988681824395af2b48)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway": transit_gateway,
        }

    @builtins.property
    def transit_gateway(self) -> ITransitGateway:
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayNatProviderOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITransitGatewayPeeringAttachment)
class TransitGatewayPeeringAttachment(
    TransitGatewayAttachmentBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayPeeringAttachment",
):
    '''Requests a transit gateway peering attachment between the specified transit gateway (requester) and a peer transit gateway (accepter).

    The peer transit
    gateway can be in your account or a different AWS account.

    After you create the peering attachment, the owner of the accepter transit
    gateway must accept the attachment request.

    :see: `AWS::EC2::TransitGatewayPeeringAttachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html>`_
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        local_transit_gateway: ITransitGateway,
        peer_transit_gateway: ITransitGateway,
        name: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayPeeringAttachment class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param local_transit_gateway: The local side of the transit gateway peering connection.
        :param peer_transit_gateway: The remote transit gateway being peered with.
        :param name: The name of the transit gateway peering attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param peer_account_id: The account that contains the transit gateway being peered with.
        :param peer_region: The region that contains the transit gateway being peered with.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094bd3c738b0a006e2a59600942e6cb57ce41b066d2acabef2f32729f9b6c14c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayPeeringAttachmentProps(
            local_transit_gateway=local_transit_gateway,
            peer_transit_gateway=peer_transit_gateway,
            name=name,
            peer_account_id=peer_account_id,
            peer_region=peer_region,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTransitGatewayPeeringAttachmentArn")
    @builtins.classmethod
    def from_transit_gateway_peering_attachment_arn(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        arn: builtins.str,
    ) -> ITransitGatewayPeeringAttachment:
        '''Imports an existing transit gateway peering attachment using its ARN.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param arn: The Amazon Resource Name (ARN) of the resource being imported.

        :return:

        An object representing the imported transit gateway peering
        attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64bc0ce43e9c832901d2f4073f54276e12b588a41c623026825482bf1d43c63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(ITransitGatewayPeeringAttachment, jsii.sinvoke(cls, "fromTransitGatewayPeeringAttachmentArn", [scope, id, arn]))

    @jsii.member(jsii_name="fromTransitGatewayPeeringAttachmentAttributes")
    @builtins.classmethod
    def from_transit_gateway_peering_attachment_attributes(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        arn: typing.Optional[builtins.str] = None,
        attachment_id: typing.Optional[builtins.str] = None,
        creation_time: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
        status_message: typing.Optional[builtins.str] = None,
    ) -> ITransitGatewayPeeringAttachment:
        '''Imports an existing transit gateway peering attachment by defining its components.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param arn: The ARN of this Transit Gateway Attachment.
        :param attachment_id: The ID of this Transit Gateway Attachment.
        :param creation_time: The time the transit gateway peering attachment was created.
        :param state: The state of the transit gateway peering attachment.
        :param status: The status of the transit gateway peering attachment.
        :param status_code: The status code for the current status of the attachment.
        :param status_message: The status message for the current status of the attachment.

        :return:

        An object representing the imported transit gateway peering
        attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b9ddfaf131e6a5091a636a0dad2dd2579ae4140b68c99fe5fee2e2506d45105)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = TransitGatewayPeeringAttachmentImportAttributes(
            arn=arn,
            attachment_id=attachment_id,
            creation_time=creation_time,
            state=state,
            status=status,
            status_code=status_code,
            status_message=status_message,
        )

        return typing.cast(ITransitGatewayPeeringAttachment, jsii.sinvoke(cls, "fromTransitGatewayPeeringAttachmentAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromTransitGatewayPeeringAttachmentId")
    @builtins.classmethod
    def from_transit_gateway_peering_attachment_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        attachment_id: builtins.str,
    ) -> ITransitGatewayPeeringAttachment:
        '''Imports an existing transit gateway peering attachment using its attachment ID.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param attachment_id: The ID of the resource being imported.

        :return:

        An object representing the imported transit gateway peering
        attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe35553be2f81ae71d207839c426c22b6542d57d2604a744dec33a748b8631f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
        return typing.cast(ITransitGatewayPeeringAttachment, jsii.sinvoke(cls, "fromTransitGatewayPeeringAttachmentId", [scope, id, attachment_id]))

    @builtins.property
    @jsii.member(jsii_name="localTransitGateway")
    def local_transit_gateway(self) -> ITransitGateway:
        '''The local side of the transit gateway peering connection.

        :see: `TransitGatewayPeeringAttachment TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-transitgatewayid>`_
        :group: Inputs
        '''
        return typing.cast(ITransitGateway, jsii.get(self, "localTransitGateway"))

    @builtins.property
    @jsii.member(jsii_name="peerTransitGateway")
    def peer_transit_gateway(self) -> ITransitGateway:
        '''The remote transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerTransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peertransitgatewayid>`_
        :group: Inputs
        '''
        return typing.cast(ITransitGateway, jsii.get(self, "peerTransitGateway"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayPeeringAttachment:
        '''The underlying TransitGatewayRouteTable CloudFormation resource.

        :see: `AWS::EC2::TransitGatewayRouteTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayPeeringAttachment, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentCreationTime")
    def transit_gateway_attachment_creation_time(self) -> builtins.str:
        '''The time the transit gateway peering attachment was created.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of this transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentState")
    def transit_gateway_attachment_state(self) -> builtins.str:
        '''The state of the transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentState"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatus")
    def transit_gateway_attachment_status(self) -> builtins.str:
        '''The status of the transit gateway peering attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatus"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusCode")
    def transit_gateway_attachment_status_code(self) -> builtins.str:
        '''The status code for the current status of the attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatusCode"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentStatusMessage")
    def transit_gateway_attachment_status_message(self) -> builtins.str:
        '''The status message for the current status of the attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway peering attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayPeeringAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-tags>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="peerAccountId")
    def peer_account_id(self) -> typing.Optional[builtins.str]:
        '''The account that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerAccountId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peeraccountid>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerAccountId"))

    @builtins.property
    @jsii.member(jsii_name="peerRegion")
    def peer_region(self) -> typing.Optional[builtins.str]:
        '''The region that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerRegion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peerregion>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerRegion"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayPeeringAttachmentImportAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "attachment_id": "attachmentId",
        "creation_time": "creationTime",
        "state": "state",
        "status": "status",
        "status_code": "statusCode",
        "status_message": "statusMessage",
    },
)
class TransitGatewayPeeringAttachmentImportAttributes:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        attachment_id: typing.Optional[builtins.str] = None,
        creation_time: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[builtins.str] = None,
        status_message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration options for importing a transit gateway peering attachment.

        :param arn: The ARN of this Transit Gateway Attachment.
        :param attachment_id: The ID of this Transit Gateway Attachment.
        :param creation_time: The time the transit gateway peering attachment was created.
        :param state: The state of the transit gateway peering attachment.
        :param status: The status of the transit gateway peering attachment.
        :param status_code: The status code for the current status of the attachment.
        :param status_message: The status message for the current status of the attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17eab9c1c0483a81bcbc3cfb19dfc9cd1902962956a39306a77b2b041a6f2182)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
            check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument status_message", value=status_message, expected_type=type_hints["status_message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if attachment_id is not None:
            self._values["attachment_id"] = attachment_id
        if creation_time is not None:
            self._values["creation_time"] = creation_time
        if state is not None:
            self._values["state"] = state
        if status is not None:
            self._values["status"] = status
        if status_code is not None:
            self._values["status_code"] = status_code
        if status_message is not None:
            self._values["status_message"] = status_message

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of this Transit Gateway Attachment.'''
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def attachment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of this Transit Gateway Attachment.'''
        result = self._values.get("attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def creation_time(self) -> typing.Optional[builtins.str]:
        '''The time the transit gateway peering attachment was created.'''
        result = self._values.get("creation_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the transit gateway peering attachment.'''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the transit gateway peering attachment.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''The status code for the current status of the attachment.'''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_message(self) -> typing.Optional[builtins.str]:
        '''The status message for the current status of the attachment.'''
        result = self._values.get("status_message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayPeeringAttachmentImportAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayPeeringAttachmentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "peer_account_id": "peerAccountId",
        "peer_region": "peerRegion",
    },
)
class TransitGatewayPeeringAttachmentOptions:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Optional configuration for TransitGatewayPeeringAttachment resource.

        :param name: The name of the transit gateway peering attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param peer_account_id: The account that contains the transit gateway being peered with.
        :param peer_region: The region that contains the transit gateway being peered with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25aee8c8ebebcfa519a0f5706458a5669157c84f5af528e93a86402ac7c50aae)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_account_id", value=peer_account_id, expected_type=type_hints["peer_account_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if peer_account_id is not None:
            self._values["peer_account_id"] = peer_account_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway peering attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayPeeringAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-tags>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_account_id(self) -> typing.Optional[builtins.str]:
        '''The account that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerAccountId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peeraccountid>`_
        '''
        result = self._values.get("peer_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        '''The region that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerRegion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peerregion>`_
        '''
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayPeeringAttachmentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayPeeringAttachmentProps",
    jsii_struct_bases=[
        TransitGatewayPeeringAttachmentOptions, _aws_cdk_ceddda9d.ResourceProps
    ],
    name_mapping={
        "name": "name",
        "peer_account_id": "peerAccountId",
        "peer_region": "peerRegion",
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "local_transit_gateway": "localTransitGateway",
        "peer_transit_gateway": "peerTransitGateway",
    },
)
class TransitGatewayPeeringAttachmentProps(
    TransitGatewayPeeringAttachmentOptions,
    _aws_cdk_ceddda9d.ResourceProps,
):
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        peer_account_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        local_transit_gateway: ITransitGateway,
        peer_transit_gateway: ITransitGateway,
    ) -> None:
        '''Configuration for TransitGatewayPeeringAttachment resource.

        :param name: The name of the transit gateway peering attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param peer_account_id: The account that contains the transit gateway being peered with.
        :param peer_region: The region that contains the transit gateway being peered with.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param local_transit_gateway: The local side of the transit gateway peering connection.
        :param peer_transit_gateway: The remote transit gateway being peered with.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b477916bc8b985cd2d6731bf57489e1a7c94f20fccf7711617cdf0d1bd25beb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument peer_account_id", value=peer_account_id, expected_type=type_hints["peer_account_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument local_transit_gateway", value=local_transit_gateway, expected_type=type_hints["local_transit_gateway"])
            check_type(argname="argument peer_transit_gateway", value=peer_transit_gateway, expected_type=type_hints["peer_transit_gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_transit_gateway": local_transit_gateway,
            "peer_transit_gateway": peer_transit_gateway,
        }
        if name is not None:
            self._values["name"] = name
        if peer_account_id is not None:
            self._values["peer_account_id"] = peer_account_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway peering attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayPeeringAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-tags>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_account_id(self) -> typing.Optional[builtins.str]:
        '''The account that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerAccountId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peeraccountid>`_
        '''
        result = self._values.get("peer_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        '''The region that contains the transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerRegion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peerregion>`_
        '''
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

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
    def local_transit_gateway(self) -> ITransitGateway:
        '''The local side of the transit gateway peering connection.

        :see: `TransitGatewayPeeringAttachment TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-transitgatewayid>`_
        '''
        result = self._values.get("local_transit_gateway")
        assert result is not None, "Required property 'local_transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    @builtins.property
    def peer_transit_gateway(self) -> ITransitGateway:
        '''The remote transit gateway being peered with.

        :see: `TransitGatewayPeeringAttachment PeerTransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewaypeeringattachment.html#cfn-ec2-transitgatewaypeeringattachment-peertransitgatewayid>`_
        '''
        result = self._values.get("peer_transit_gateway")
        assert result is not None, "Required property 'peer_transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayPeeringAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "amazon_side_asn": "amazonSideAsn",
        "auto_accept_shared_attachments": "autoAcceptSharedAttachments",
        "cidr_blocks": "cidrBlocks",
        "default_route_table_association": "defaultRouteTableAssociation",
        "default_route_table_id": "defaultRouteTableId",
        "default_route_table_propagation": "defaultRouteTablePropagation",
        "description": "description",
        "dns_support": "dnsSupport",
        "multicast_support": "multicastSupport",
        "name": "name",
        "vpn_ecmp_support": "vpnEcmpSupport",
    },
)
class TransitGatewayProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
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
    ) -> None:
        '''Configuration for TransitGateway resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
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
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34be88b6da81fce37f3376e8b1fd1aff7e222c4b2fb4ab8e879c634868d58a81)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument amazon_side_asn", value=amazon_side_asn, expected_type=type_hints["amazon_side_asn"])
            check_type(argname="argument auto_accept_shared_attachments", value=auto_accept_shared_attachments, expected_type=type_hints["auto_accept_shared_attachments"])
            check_type(argname="argument cidr_blocks", value=cidr_blocks, expected_type=type_hints["cidr_blocks"])
            check_type(argname="argument default_route_table_association", value=default_route_table_association, expected_type=type_hints["default_route_table_association"])
            check_type(argname="argument default_route_table_id", value=default_route_table_id, expected_type=type_hints["default_route_table_id"])
            check_type(argname="argument default_route_table_propagation", value=default_route_table_propagation, expected_type=type_hints["default_route_table_propagation"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dns_support", value=dns_support, expected_type=type_hints["dns_support"])
            check_type(argname="argument multicast_support", value=multicast_support, expected_type=type_hints["multicast_support"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpn_ecmp_support", value=vpn_ecmp_support, expected_type=type_hints["vpn_ecmp_support"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if amazon_side_asn is not None:
            self._values["amazon_side_asn"] = amazon_side_asn
        if auto_accept_shared_attachments is not None:
            self._values["auto_accept_shared_attachments"] = auto_accept_shared_attachments
        if cidr_blocks is not None:
            self._values["cidr_blocks"] = cidr_blocks
        if default_route_table_association is not None:
            self._values["default_route_table_association"] = default_route_table_association
        if default_route_table_id is not None:
            self._values["default_route_table_id"] = default_route_table_id
        if default_route_table_propagation is not None:
            self._values["default_route_table_propagation"] = default_route_table_propagation
        if description is not None:
            self._values["description"] = description
        if dns_support is not None:
            self._values["dns_support"] = dns_support
        if multicast_support is not None:
            self._values["multicast_support"] = multicast_support
        if name is not None:
            self._values["name"] = name
        if vpn_ecmp_support is not None:
            self._values["vpn_ecmp_support"] = vpn_ecmp_support

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
    def amazon_side_asn(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("amazon_side_asn")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def auto_accept_shared_attachments(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("auto_accept_shared_attachments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_route_table_association(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("default_route_table_association")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def default_route_table_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default_route_table_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_route_table_propagation(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("default_route_table_propagation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def multicast_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("multicast_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpn_ecmp_support(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("vpn_ecmp_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TransitGatewayRoute(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayRoute",
):
    '''Adds a routing rule for a transit gateway route table.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cidr: builtins.str,
        route_table: ITransitGatewayRouteTable,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayAttachment class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param cidr: 
        :param route_table: 
        :param attachment: 
        :param blackhole: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472f0a715c24828891d913514782594fd48e540d0192f96901c525a6f2c9845f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayRouteProps(
            cidr=cidr,
            route_table=route_table,
            attachment=attachment,
            blackhole=blackhole,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTransitGatewayRouteId")
    @builtins.classmethod
    def from_transit_gateway_route_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        transit_gateway_route_id: builtins.str,
    ) -> ITransitGatewayRoute:
        '''Imports an existing Transit Gateway Route using its route ID.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway_route_id: The ID of the Transit Gateway route being imported.

        :return: An object representing the imported Transit Gateway route.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e915393403cdd527b11e940ce216647c74d6e6b709f726e821e12fa1b470873d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_route_id", value=transit_gateway_route_id, expected_type=type_hints["transit_gateway_route_id"])
        return typing.cast(ITransitGatewayRoute, jsii.sinvoke(cls, "fromTransitGatewayRouteId", [scope, id, transit_gateway_route_id]))

    @builtins.property
    @jsii.member(jsii_name="cidr")
    def cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidr"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayRoute:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayRoute, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="routeTable")
    def route_table(self) -> ITransitGatewayRouteTable:
        return typing.cast(ITransitGatewayRouteTable, jsii.get(self, "routeTable"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteId")
    def transit_gateway_route_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteId"))

    @builtins.property
    @jsii.member(jsii_name="attachment")
    def attachment(self) -> typing.Optional[ITransitGatewayAttachment]:
        return typing.cast(typing.Optional[ITransitGatewayAttachment], jsii.get(self, "attachment"))

    @builtins.property
    @jsii.member(jsii_name="blackhole")
    def blackhole(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "blackhole"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayRouteOptions",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cidr": "cidr",
        "attachment": "attachment",
        "blackhole": "blackhole",
    },
)
class TransitGatewayRouteOptions(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cidr: builtins.str,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Options for adding a route to a transit gateway route table.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cidr: The CIDR range to match for the route.
        :param attachment: The transit gateway attachment where matched traffic should be routed.
        :param blackhole: Whether the traffic should be black holed (discarded) rather than being routed to an attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac305487ec828686fdbbd312914a754c55ca742068c194f48ac724cf9aef071)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument attachment", value=attachment, expected_type=type_hints["attachment"])
            check_type(argname="argument blackhole", value=blackhole, expected_type=type_hints["blackhole"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if attachment is not None:
            self._values["attachment"] = attachment
        if blackhole is not None:
            self._values["blackhole"] = blackhole

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
    def cidr(self) -> builtins.str:
        '''The CIDR range to match for the route.'''
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attachment(self) -> typing.Optional[ITransitGatewayAttachment]:
        '''The transit gateway attachment where matched traffic should be routed.'''
        result = self._values.get("attachment")
        return typing.cast(typing.Optional[ITransitGatewayAttachment], result)

    @builtins.property
    def blackhole(self) -> typing.Optional[builtins.bool]:
        '''Whether the traffic should be black holed (discarded) rather than being routed to an attachment.'''
        result = self._values.get("blackhole")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayRouteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayRouteProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "cidr": "cidr",
        "route_table": "routeTable",
        "attachment": "attachment",
        "blackhole": "blackhole",
    },
)
class TransitGatewayRouteProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        cidr: builtins.str,
        route_table: ITransitGatewayRouteTable,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Configuration for TransitGatewayRoute resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param cidr: 
        :param route_table: 
        :param attachment: 
        :param blackhole: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f603e48c36f0aabd623aee3c75f3f94dcd322957a71fb2d3539585045d2c00)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
            check_type(argname="argument route_table", value=route_table, expected_type=type_hints["route_table"])
            check_type(argname="argument attachment", value=attachment, expected_type=type_hints["attachment"])
            check_type(argname="argument blackhole", value=blackhole, expected_type=type_hints["blackhole"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cidr": cidr,
            "route_table": route_table,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if attachment is not None:
            self._values["attachment"] = attachment
        if blackhole is not None:
            self._values["blackhole"] = blackhole

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
    def cidr(self) -> builtins.str:
        result = self._values.get("cidr")
        assert result is not None, "Required property 'cidr' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_table(self) -> ITransitGatewayRouteTable:
        result = self._values.get("route_table")
        assert result is not None, "Required property 'route_table' is missing"
        return typing.cast(ITransitGatewayRouteTable, result)

    @builtins.property
    def attachment(self) -> typing.Optional[ITransitGatewayAttachment]:
        result = self._values.get("attachment")
        return typing.cast(typing.Optional[ITransitGatewayAttachment], result)

    @builtins.property
    def blackhole(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("blackhole")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayRouteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITransitGatewayRouteTable)
class TransitGatewayRouteTable(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayRouteTable",
):
    '''Creates a route table for traffic being processed by a transit gateway.

    When traffic is routed to a transit gateway via an attachment, the route
    table associated with that attachment is used when evaluating how the
    inbound traffic should be routed.

    :see: `AWS::EC2::TransitGatewayRouteTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html>`_
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        transit_gateway: ITransitGateway,
        name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayRouteTable class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway: The transit gateway for which the route table should be created.
        :param name: The name of the transit gateway route table. Used to tag the route table with a name that will be displayed in the AWS VPC console.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf9f0e3a9c51ac3498209cf81371557e5b56db1c03ff409740d882fde1cacda7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayRouteTableProps(
            transit_gateway=transit_gateway,
            name=name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTransitGatewayRouteTableId")
    @builtins.classmethod
    def from_transit_gateway_route_table_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        transit_gateway_route_table_id: builtins.str,
    ) -> ITransitGatewayRouteTable:
        '''Imports an existing transit gateway route table using its route table ID.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway_route_table_id: The attachment ID of the transit gateway route table being imported.

        :return: An object representing the imported transit gateway route table.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ddc972512f9b73360cad75e0fd028f815d92130c441ed49e42d40f77ebd8fff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_route_table_id", value=transit_gateway_route_table_id, expected_type=type_hints["transit_gateway_route_table_id"])
        return typing.cast(ITransitGatewayRouteTable, jsii.sinvoke(cls, "fromTransitGatewayRouteTableId", [scope, id, transit_gateway_route_table_id]))

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        *,
        cidr: builtins.str,
        attachment: typing.Optional[ITransitGatewayAttachment] = None,
        blackhole: typing.Optional[builtins.bool] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> TransitGatewayRoute:
        '''Adds a route to this transit gateway route table.

        :param cidr: The CIDR range to match for the route.
        :param attachment: The transit gateway attachment where matched traffic should be routed.
        :param blackhole: Whether the traffic should be black holed (discarded) rather than being routed to an attachment.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return: The TransitGatewayRoute that was added.
        '''
        options = TransitGatewayRouteOptions(
            cidr=cidr,
            attachment=attachment,
            blackhole=blackhole,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast(TransitGatewayRoute, jsii.invoke(self, "addRoute", [options]))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayRouteTable:
        '''The underlying TransitGatewayRouteTable CloudFormation resource.

        :see: `AWS::EC2::TransitGatewayRouteTable <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayRouteTable, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="transitGateway")
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway for which the route table should be created.

        :see: `TransitGatewayRouteTable TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-transitgatewayid>`_
        :group: Inputs
        '''
        return typing.cast(ITransitGateway, jsii.get(self, "transitGateway"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableArn")
    def transit_gateway_route_table_arn(self) -> builtins.str:
        '''The ARN of this transit gateway route table.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteTableArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> builtins.str:
        '''The ID of this transit gateway route table.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayRouteTableId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway route table.

        Used to tag the route table with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayRouteTable Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-tags>`_
        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayRouteTableOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class TransitGatewayRouteTableOptions:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba42798c9102c3419b7c375a3d8ce27fef028001fb7cc17a2798c1aad61854ff)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayRouteTableOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayRouteTableProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "transit_gateway": "transitGateway",
        "name": "name",
    },
)
class TransitGatewayRouteTableProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        transit_gateway: ITransitGateway,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Configuration for TransitGatewayRouteTable resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param transit_gateway: The transit gateway for which the route table should be created.
        :param name: The name of the transit gateway route table. Used to tag the route table with a name that will be displayed in the AWS VPC console.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae02cfe78ce98fb4f7880816162efbcf405d70470d3f4d83605632beeb8a6f7)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
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
        if name is not None:
            self._values["name"] = name

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
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway for which the route table should be created.

        :see: `TransitGatewayRouteTable TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-transitgatewayid>`_
        '''
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the transit gateway route table.

        Used to tag the route table with a name that will be displayed in the AWS
        VPC console.

        :see: `TransitGatewayRouteTable Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-tags>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayRouteTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TunnelOptions",
    jsii_struct_bases=[],
    name_mapping={"inside_cidr": "insideCidr", "pre_shared_key": "preSharedKey"},
)
class TunnelOptions:
    def __init__(
        self,
        *,
        inside_cidr: typing.Optional[builtins.str] = None,
        pre_shared_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    ) -> None:
        '''
        :param inside_cidr: 
        :param pre_shared_key: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4312d41d9a05862a91818a278fa16d6a73ff75dcd46ad08d731c98c54086e195)
            check_type(argname="argument inside_cidr", value=inside_cidr, expected_type=type_hints["inside_cidr"])
            check_type(argname="argument pre_shared_key", value=pre_shared_key, expected_type=type_hints["pre_shared_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inside_cidr is not None:
            self._values["inside_cidr"] = inside_cidr
        if pre_shared_key is not None:
            self._values["pre_shared_key"] = pre_shared_key

    @builtins.property
    def inside_cidr(self) -> typing.Optional[builtins.str]:
        result = self._values.get("inside_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_shared_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        result = self._values.get("pre_shared_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.VpcAttachmentOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "subnets": "subnets"},
)
class VpcAttachmentOptions:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: 
        :param subnets: 
        '''
        if isinstance(subnets, dict):
            subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dff1261f60aa49a2037d280e97af162d26181faeabf698640e4139891619042)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if subnets is not None:
            self._values["subnets"] = subnets

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcAttachmentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.VpnAttachmentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "remote_endpoint": "remoteEndpoint",
        "connection_type": "connectionType",
        "static_routes_only": "staticRoutesOnly",
        "tunnel_configurations": "tunnelConfigurations",
    },
)
class VpnAttachmentOptions:
    def __init__(
        self,
        *,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68fcd54ad9cdc22e3838841971cc60da339a1c6b65f45abf9839c71f80a1ad8)
            check_type(argname="argument remote_endpoint", value=remote_endpoint, expected_type=type_hints["remote_endpoint"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tunnel_configurations", value=tunnel_configurations, expected_type=type_hints["tunnel_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "remote_endpoint": remote_endpoint,
        }
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tunnel_configurations is not None:
            self._values["tunnel_configurations"] = tunnel_configurations

    @builtins.property
    def remote_endpoint(self) -> IRemoteVpnEndpoint:
        result = self._values.get("remote_endpoint")
        assert result is not None, "Required property 'remote_endpoint' is missing"
        return typing.cast(IRemoteVpnEndpoint, result)

    @builtins.property
    def connection_type(self) -> typing.Optional["VpnConnectionType"]:
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional["VpnConnectionType"], result)

    @builtins.property
    def static_routes_only(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tunnel_configurations(self) -> typing.Optional[typing.List[TunnelOptions]]:
        result = self._values.get("tunnel_configurations")
        return typing.cast(typing.Optional[typing.List[TunnelOptions]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnAttachmentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IVpnConnection)
class VpnConnection(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.VpnConnection",
):
    '''Specifies a VPN connection between a virtual private gateway and a VPN customer gateway or a transit gateway and a VPN customer gateway.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        local_endpoint: ILocalVpnEndpoint,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayAttachment class.

        :param scope: A CDK Construct that will serve as this stack's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param local_endpoint: 
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1711f2c24c8b7a52cb1e23aa7c00f2ee31a53d068176d8b694ba413b49c85e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VpnConnectionProps(
            local_endpoint=local_endpoint,
            remote_endpoint=remote_endpoint,
            connection_type=connection_type,
            static_routes_only=static_routes_only,
            tunnel_configurations=tunnel_configurations,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addTunnelConfiguration")
    def add_tunnel_configuration(
        self,
        *,
        inside_cidr: typing.Optional[builtins.str] = None,
        pre_shared_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    ) -> None:
        '''
        :param inside_cidr: 
        :param pre_shared_key: 
        '''
        options = TunnelOptions(inside_cidr=inside_cidr, pre_shared_key=pre_shared_key)

        return typing.cast(None, jsii.invoke(self, "addTunnelConfiguration", [options]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''Return the given named metric for this VPNConnection.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1943d41246b0671229072a9d9650d8d0f9f66aaf7b458b59f96ab84ad35da3)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The bytes received through the VPN tunnel.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTunnelDataIn", [props]))

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The bytes sent through the VPN tunnel.

        Sum over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTunnelDataOut", [props]))

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''The state of the tunnel.

        0 indicates DOWN and 1 indicates UP.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTunnelState", [props]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> "VpnConnectionType":
        return typing.cast("VpnConnectionType", jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        '''The ASN of the customer gateway.'''
        return typing.cast(jsii.Number, jsii.get(self, "customerGatewayAsn"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        '''The id of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> builtins.str:
        '''The ip address of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayIp"))

    @builtins.property
    @jsii.member(jsii_name="localEndpoint")
    def local_endpoint(self) -> ILocalVpnEndpoint:
        return typing.cast(ILocalVpnEndpoint, jsii.get(self, "localEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="remoteEndpoint")
    def remote_endpoint(self) -> IRemoteVpnEndpoint:
        return typing.cast(IRemoteVpnEndpoint, jsii.get(self, "remoteEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnVPNConnection:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnVPNConnection, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="tunnelConfigurations")
    def tunnel_configurations(self) -> typing.List[TunnelOptions]:
        return typing.cast(typing.List[TunnelOptions], jsii.get(self, "tunnelConfigurations"))

    @builtins.property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> builtins.str:
        '''The id of the VPN connection.'''
        return typing.cast(builtins.str, jsii.get(self, "vpnId"))

    @builtins.property
    @jsii.member(jsii_name="staticRoutesOnly")
    def static_routes_only(self) -> typing.Optional[builtins.bool]:
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "staticRoutesOnly"))


class VpnConnectionLocalEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.VpnConnectionLocalEndpoint",
):
    '''Provides options for specifying the local side of a VPN connection.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromTransitGateway")
    @builtins.classmethod
    def from_transit_gateway(
        cls,
        transit_gateway: ITransitGateway,
    ) -> TransitGatewayLocalVpnEndpoint:
        '''
        :param transit_gateway: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ddda611ef5d00d1dbfb980664aaf365a9109585805083204f9dd201f73b937)
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
        return typing.cast(TransitGatewayLocalVpnEndpoint, jsii.sinvoke(cls, "fromTransitGateway", [transit_gateway]))

    @jsii.member(jsii_name="fromVpnGateway")
    @builtins.classmethod
    def from_vpn_gateway(
        cls,
        vpn_gateway: _aws_cdk_aws_ec2_ceddda9d.IVpnGateway,
    ) -> "VpnGatewayLocalVpnEndpoint":
        '''
        :param vpn_gateway: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255c4f2f88d39694addb3404e05f43b66d5900dda0a83d02497e7579af1e9f87)
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
        return typing.cast("VpnGatewayLocalVpnEndpoint", jsii.sinvoke(cls, "fromVpnGateway", [vpn_gateway]))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.VpnConnectionProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "local_endpoint": "localEndpoint",
        "remote_endpoint": "remoteEndpoint",
        "connection_type": "connectionType",
        "static_routes_only": "staticRoutesOnly",
        "tunnel_configurations": "tunnelConfigurations",
    },
)
class VpnConnectionProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        local_endpoint: ILocalVpnEndpoint,
        remote_endpoint: IRemoteVpnEndpoint,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        static_routes_only: typing.Optional[builtins.bool] = None,
        tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Configuration for the VpnConnection resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param local_endpoint: 
        :param remote_endpoint: 
        :param connection_type: 
        :param static_routes_only: 
        :param tunnel_configurations: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f1ecffd701acc1acc5674e16c0bca0e65f2e2327e74bfb0fe4021722919ad1)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument local_endpoint", value=local_endpoint, expected_type=type_hints["local_endpoint"])
            check_type(argname="argument remote_endpoint", value=remote_endpoint, expected_type=type_hints["remote_endpoint"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument static_routes_only", value=static_routes_only, expected_type=type_hints["static_routes_only"])
            check_type(argname="argument tunnel_configurations", value=tunnel_configurations, expected_type=type_hints["tunnel_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "local_endpoint": local_endpoint,
            "remote_endpoint": remote_endpoint,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if static_routes_only is not None:
            self._values["static_routes_only"] = static_routes_only
        if tunnel_configurations is not None:
            self._values["tunnel_configurations"] = tunnel_configurations

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
    def local_endpoint(self) -> ILocalVpnEndpoint:
        result = self._values.get("local_endpoint")
        assert result is not None, "Required property 'local_endpoint' is missing"
        return typing.cast(ILocalVpnEndpoint, result)

    @builtins.property
    def remote_endpoint(self) -> IRemoteVpnEndpoint:
        result = self._values.get("remote_endpoint")
        assert result is not None, "Required property 'remote_endpoint' is missing"
        return typing.cast(IRemoteVpnEndpoint, result)

    @builtins.property
    def connection_type(self) -> typing.Optional["VpnConnectionType"]:
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional["VpnConnectionType"], result)

    @builtins.property
    def static_routes_only(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("static_routes_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tunnel_configurations(self) -> typing.Optional[typing.List[TunnelOptions]]:
        result = self._values.get("tunnel_configurations")
        return typing.cast(typing.Optional[typing.List[TunnelOptions]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpnConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VpnConnectionRemoteEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.VpnConnectionRemoteEndpoint",
):
    '''Provides options for specifying the remote side of a VPN connection.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromConfiguration")
    @builtins.classmethod
    def from_configuration(
        cls,
        *,
        ip_address: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional["VpnConnectionType"] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "CustomerGatewayConfigurationRemoteVpnEndpoint":
        '''Creates a remote connection using the configuration details provided.

        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param connection_type: The type of VPN connection that this customer gateway supports.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        :return: A configuration object representing a remote VPN destination.
        '''
        configuration = CustomerGatewayProps(
            ip_address=ip_address,
            bgp_asn=bgp_asn,
            connection_type=connection_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("CustomerGatewayConfigurationRemoteVpnEndpoint", jsii.sinvoke(cls, "fromConfiguration", [configuration]))

    @jsii.member(jsii_name="fromCustomerGateway")
    @builtins.classmethod
    def from_customer_gateway(
        cls,
        customer_gateway: ICustomerGateway,
    ) -> "CustomerGatewayRemoteVpnEndpoint":
        '''Creates a remote connection using a customer gateway.

        :param customer_gateway: The customer gateway that is configured for the remote endpoint device.

        :return: A configuration object representing a remote VPN destination.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec3ce1dacbcb72f74a7ad181d5838d1e71517bb5fc661cee673e3d13cf35dbe)
            check_type(argname="argument customer_gateway", value=customer_gateway, expected_type=type_hints["customer_gateway"])
        return typing.cast("CustomerGatewayRemoteVpnEndpoint", jsii.sinvoke(cls, "fromCustomerGateway", [customer_gateway]))


class VpnConnectionType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.VpnConnectionType",
):
    '''Represents a VPN protocol that can be used to establish a connection.'''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "VpnConnectionType":
        '''An escape hatch method that allows defining custom VPN protocols.

        :param name: The name of the VPN protocol.

        :return: A VpnConnectionType object representing the specified protocol.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c531bfa20e4b82501cd1840a34d989b2593246657ad35703dfdd6156ae409b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("VpnConnectionType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IPSEC_1")
    def IPSEC_1(cls) -> "VpnConnectionType":
        '''The ipsec.1 VPN protocol.'''
        return typing.cast("VpnConnectionType", jsii.sget(cls, "IPSEC_1"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the VPN protocol.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.implements(ILocalVpnEndpoint)
class VpnGatewayLocalVpnEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.VpnGatewayLocalVpnEndpoint",
):
    '''Specifies a VPN connection endpoint which routes to a VPN gateway on the AWS side.'''

    def __init__(self, vpn_gateway: _aws_cdk_aws_ec2_ceddda9d.IVpnGateway) -> None:
        '''Creates a new instance of the VpnGatewayLocalVpnEndpoint class.

        :param vpn_gateway: The VPN gateway that serves as the local end of a VPN connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c9d0488d52533eda0e8e013c7c8dc98375bf35fbfb4d0119edfc6dafc3add2)
            check_type(argname="argument vpn_gateway", value=vpn_gateway, expected_type=type_hints["vpn_gateway"])
        jsii.create(self.__class__, self, [vpn_gateway])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> LocalVpnEndpointConfiguration:
        '''Produces a configuration that can be used when configuring the local end of a VPN connection.

        :param _scope: The construct configuring the VPN connection that will be referencing the local endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b034f4493a7f4e0ef9f3e966d78f68321b168b61b98dda5c4dace5477a2b5d5e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(LocalVpnEndpointConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="vpnGateway")
    def vpn_gateway(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpnGateway:
        '''The VPN gateway that serves as the local end of a VPN connection.

        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpnGateway, jsii.get(self, "vpnGateway"))


@jsii.implements(ICustomerGateway)
class CustomerGateway(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.CustomerGateway",
):
    '''Specifies thje details of a remote endpoint that can serve as an endpoint for connections to AWS.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ip_address: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional[VpnConnectionType] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the CustomerGateway class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param connection_type: The type of VPN connection that this customer gateway supports.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7814523b269d29ae5e2e42aa21c1f81bdc5a471fe5e300b0768c03a21b6a6f91)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CustomerGatewayProps(
            ip_address=ip_address,
            bgp_asn=bgp_asn,
            connection_type=connection_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromCustomerGatewayAttributes")
    @builtins.classmethod
    def from_customer_gateway_attributes(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        customer_gateway_id: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        ip_address: typing.Optional[builtins.str] = None,
    ) -> ICustomerGateway:
        '''Imports an existing custom gateway by specifying its details.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param customer_gateway_id: The ID of the existing customer gateway being imported.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.

        :return: An object representing the imported customer gateway.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cee3aaa3f8d41d377b44df84c1bd31404fc3c74c1f3d4d50f41733f5ceaeaba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attributes = CustomerGatewayAttributes(
            customer_gateway_id=customer_gateway_id,
            bgp_asn=bgp_asn,
            ip_address=ip_address,
        )

        return typing.cast(ICustomerGateway, jsii.sinvoke(cls, "fromCustomerGatewayAttributes", [scope, id, attributes]))

    @jsii.member(jsii_name="fromCustomerGatewayId")
    @builtins.classmethod
    def from_customer_gateway_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        customer_gateway_id: builtins.str,
    ) -> ICustomerGateway:
        '''Imports an existing custom gateway using its CustomerGatewayId.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param customer_gateway_id: The ID of the existing customer gateway being imported.

        :return: An object representing the imported customer gateway.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__745b377e3c9abac41a861ca1050cfc8012b832cecc7ce152fed229d86ee5e4ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument customer_gateway_id", value=customer_gateway_id, expected_type=type_hints["customer_gateway_id"])
        return typing.cast(ICustomerGateway, jsii.sinvoke(cls, "fromCustomerGatewayId", [scope, id, customer_gateway_id]))

    @builtins.property
    @jsii.member(jsii_name="bgpAsn")
    def bgp_asn(self) -> jsii.Number:
        '''For devices that support BGP, the customer gateway's BGP ASN.

        :see: `CustomerGateway BgpAsn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-bgpasn>`_
        :group: Inputs
        '''
        return typing.cast(jsii.Number, jsii.get(self, "bgpAsn"))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def connection_type(self) -> VpnConnectionType:
        '''The type of VPN connection that this customer gateway supports.

        :see: `CustomerGateway Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-type>`_
        :group: Inputs
        '''
        return typing.cast(VpnConnectionType, jsii.get(self, "connectionType"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        '''The BGP ASN of the customer gateway.'''
        return typing.cast(jsii.Number, jsii.get(self, "customerGatewayAsn"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> builtins.str:
        '''The ID of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayId"))

    @builtins.property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> builtins.str:
        '''The IP address of the customer gateway.'''
        return typing.cast(builtins.str, jsii.get(self, "customerGatewayIp"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        '''The Internet-routable IP address for the customer gateway's outside interface.

        The address must be static.

        :see: `CustomerGateway IpAddress <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html#cfn-ec2-customergateway-ipaddress>`_
        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway:
        '''The underlying CustomerGateway CloudFormation resource.

        :see: `AWS::EC2::CustomerGateway <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customergateway.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnCustomerGateway, jsii.get(self, "resource"))


@jsii.implements(IRemoteVpnEndpoint)
class CustomerGatewayConfigurationRemoteVpnEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.CustomerGatewayConfigurationRemoteVpnEndpoint",
):
    '''Specifies a remote VPN endpoint device by directly specifyingits details.'''

    def __init__(
        self,
        *,
        ip_address: builtins.str,
        bgp_asn: typing.Optional[jsii.Number] = None,
        connection_type: typing.Optional[VpnConnectionType] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the CustomerGatewayConfigurationRemoteVpnEndpoint class.

        :param ip_address: The Internet-routable IP address for the customer gateway's outside interface. The address must be static.
        :param bgp_asn: For devices that support BGP, the customer gateway's BGP ASN.
        :param connection_type: The type of VPN connection that this customer gateway supports.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        configuration = CustomerGatewayProps(
            ip_address=ip_address,
            bgp_asn=bgp_asn,
            connection_type=connection_type,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [configuration])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
    ) -> RemoteVpnEndpointConfiguration:
        '''Produces a configuration that can be used when configuring the remote end of a VPN connection.

        :param scope: The construct configuring the VPN connection that will be referencing the remote endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376ae140d941de56c115f01c627b230e0ffb07b7247eb9a061e389e071218f36)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(RemoteVpnEndpointConfiguration, jsii.invoke(self, "bind", [scope]))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> CustomerGatewayProps:
        '''The details of the device on the remote end of the VPN connection.

        :group: Inputs
        '''
        return typing.cast(CustomerGatewayProps, jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="customerGateway")
    def customer_gateway(self) -> typing.Optional[CustomerGateway]:
        '''The customer gateway that was created to represent the device on the remote end of the VPN connection.

        :group: Resources
        '''
        return typing.cast(typing.Optional[CustomerGateway], jsii.get(self, "customerGateway"))


@jsii.implements(IRemoteVpnEndpoint)
class CustomerGatewayRemoteVpnEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.CustomerGatewayRemoteVpnEndpoint",
):
    '''Specifies a remote VPN endpoint device that has its details configured in an existing customer gateway.'''

    def __init__(self, customer_gateway: ICustomerGateway) -> None:
        '''Creates a new instance of the CustomerGatewayRemoteVpnEndpoint class.

        :param customer_gateway: The customer gateway that is configured with the details of the remote endpoint device.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39f263303ec59ccc7954f0b56dc5825a43956cfa48fc4648959c032c858f8a2f)
            check_type(argname="argument customer_gateway", value=customer_gateway, expected_type=type_hints["customer_gateway"])
        jsii.create(self.__class__, self, [customer_gateway])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> RemoteVpnEndpointConfiguration:
        '''Produces a configuration that can be used when configuring the remote end of a VPN connection.

        :param _scope: The construct configuring the VPN connection that will be referencing the remote endpoint.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd8797d122fda919f703e603d2c593c1fe151dbc800704673ccc25360cdf5d3e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(RemoteVpnEndpointConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="customerGateway")
    def customer_gateway(self) -> ICustomerGateway:
        '''The customer gateway that is configured with the details of the remote endpoint device.

        :group: Inputs
        '''
        return typing.cast(ICustomerGateway, jsii.get(self, "customerGateway"))


@jsii.implements(ILogDestination)
class FlowLogDestination(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.ec2.FlowLogDestination",
):
    '''Represents a resource that can act as a deliver endpoint for captured flow logs.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toCloudWatchLogs")
    @builtins.classmethod
    def to_cloud_watch_logs(
        cls,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> "FlowLogDestination":
        '''Represents a CloudWatch log group that will serve as the endpoint where flow logs should be delivered.

        :param log_group: The CloudWatch LogGroup where flow logs should be delivered.
        :param role: An IAM role that allows Amazon EC2 to publish flow logs to a CloudWatch Logs log group in your account.

        :return:

        A configuration object containing details on how to set up
        logging to the log group.

        :see: `Publish flow logs to CloudWatch Logs <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-cwl.html>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5daa8ff9c63f8f6617139a25d0c2042756ce3ab0da13e5f5a51634e4b9f7ab0c)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast("FlowLogDestination", jsii.sinvoke(cls, "toCloudWatchLogs", [log_group, role]))

    @jsii.member(jsii_name="toS3")
    @builtins.classmethod
    def to_s3(
        cls,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        *,
        file_format: typing.Optional[FlowLogFileFormat] = None,
        hive_compatible_partitions: typing.Optional[builtins.bool] = None,
        key_prefix: typing.Optional[builtins.str] = None,
        per_hour_partition: typing.Optional[builtins.bool] = None,
    ) -> "FlowLogDestination":
        '''Represents a CloudWatch log group that will serve as the endpoint where flow logs should be delivered.

        :param bucket: The S3 Bucket where flow logs should be delivered.
        :param file_format: The file format in which flow logs should be delivered to S3.
        :param hive_compatible_partitions: Controls the format of partitions ("folders") when the flow logs are delivered to S3. By default, flow logs are delivered partitioned such that each part of the S3 path represents a values pertaining to details of the log. When hive compatible partitions are enabled, partitions will be structured such that keys declaring the partition name are added at each level. An example of standard partitioning:: /us-east-1/2020/03/08/log.tar.gz An example with Hive compatible partitions:: /region=us-east-1/year=2020/month=03/day=08/log.tar.gz
        :param key_prefix: An optional prefix that will be added to the start of all flow log files delivered to the S3 bucket.
        :param per_hour_partition: Indicates whether to partition the flow log per hour. By default, flow logs are partitioned (organized into S3 "folders") by day. Setting this to true will add an extra layer of directories splitting flow log files by the hour in which they were delivered.

        :return:

        A configuration object containing details on how to set up
        logging to the bucket.

        :see: `Publish flow logs to Amazon S3 <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html>`_
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d11b43c926a884fe3a73d0b44332cd0342bba0c0e2d7bcac16489f068e1191b)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        options = FlowLogS3Options(
            file_format=file_format,
            hive_compatible_partitions=hive_compatible_partitions,
            key_prefix=key_prefix,
            per_hour_partition=per_hour_partition,
        )

        return typing.cast("FlowLogDestination", jsii.sinvoke(cls, "toS3", [bucket, options]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> FlowLogDestinationConfig:
        '''Returns a configuration object with all the fields and resources needed to configure a flow log to write to the destination.

        :param scope: The CDK Construct that will be consuming the configuration and using it to configure a flow log.
        '''
        ...


class _FlowLogDestinationProxy(FlowLogDestination):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> FlowLogDestinationConfig:
        '''Returns a configuration object with all the fields and resources needed to configure a flow log to write to the destination.

        :param scope: The CDK Construct that will be consuming the configuration and using it to configure a flow log.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6be248e60a194fe1d0bcf9dc9398b94b088ef8e6ca462c0c85ef25246e79057)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(FlowLogDestinationConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FlowLogDestination).__jsii_proxy_class__ = lambda : _FlowLogDestinationProxy


class TransitGatewayAttachment(
    TransitGatewayAttachmentResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.ec2.TransitGatewayAttachment",
):
    '''Attaches a VPC to a transit gateway.

    If you attach a VPC with a CIDR range that overlaps the CIDR range of a VPC
    that is already attached, the new VPC CIDR range is not propagated to the
    default propagation route table.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        transit_gateway: ITransitGateway,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        appliance_mode_support: typing.Optional[builtins.bool] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        ipv6_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the TransitGatewayAttachment class.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway: The transit gateway for which the attachment should be created.
        :param vpc: The VPC where the attachment should be created.
        :param appliance_mode_support: Enables appliance mode on the attachment. When appliance mode is enabled, all traffic flowing between attachments is forwarded to an appliance in a shared VPC to be inspected and processed.
        :param dns_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param ipv6_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param name: The name of the Transit Gateway Attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param subnets: The subnets where the attachment should be created. Can select up to one subnet per Availability Zone.
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27ee6909fddcfad51f5ddc3aee4e522d6f5fdeab0a0272e67e7d62c063924d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TransitGatewayAttachmentProps(
            transit_gateway=transit_gateway,
            vpc=vpc,
            appliance_mode_support=appliance_mode_support,
            dns_support=dns_support,
            ipv6_support=ipv6_support,
            name=name,
            subnets=subnets,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTransitGatewayAttachmentId")
    @builtins.classmethod
    def from_transit_gateway_attachment_id(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        transit_gateway_attachment_id: builtins.str,
    ) -> ITransitGatewayAttachment:
        '''Imports an existing Transit Gateway Attachment using its attachment ID.

        :param scope: A CDK Construct that will serve as this resources's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param transit_gateway_attachment_id: The attachment ID of the Transit Gateway attachment being imported.

        :return: An object representing the imported transit gateway attachment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__135a7b7bec5b4b7974ff32ebff887b94cc20f2b37d6736525ec2c4e7c4b5c542)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument transit_gateway_attachment_id", value=transit_gateway_attachment_id, expected_type=type_hints["transit_gateway_attachment_id"])
        return typing.cast(ITransitGatewayAttachment, jsii.sinvoke(cls, "fromTransitGatewayAttachmentId", [scope, id, transit_gateway_attachment_id]))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayAttachment:
        '''The underlying NamedQuery CloudFormation resource.

        :see: `AWS::EC2::TransitGatewayVpcAttachment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html>`_
        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.CfnTransitGatewayAttachment, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentArn")
    def transit_gateway_attachment_arn(self) -> builtins.str:
        '''The ARN of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentArn"))

    @builtins.property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> builtins.str:
        '''The ID of this Transit Gateway Attachment.'''
        return typing.cast(builtins.str, jsii.get(self, "transitGatewayAttachmentId"))


@jsii.data_type(
    jsii_type="cdk-extensions.ec2.TransitGatewayAttachmentProps",
    jsii_struct_bases=[TransitGatewayAttachmentResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "transit_gateway": "transitGateway",
        "vpc": "vpc",
        "appliance_mode_support": "applianceModeSupport",
        "dns_support": "dnsSupport",
        "ipv6_support": "ipv6Support",
        "name": "name",
        "subnets": "subnets",
    },
)
class TransitGatewayAttachmentProps(TransitGatewayAttachmentResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        transit_gateway: ITransitGateway,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        appliance_mode_support: typing.Optional[builtins.bool] = None,
        dns_support: typing.Optional[builtins.bool] = None,
        ipv6_support: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration for TransitGatewayAttachment resource.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param transit_gateway: The transit gateway for which the attachment should be created.
        :param vpc: The VPC where the attachment should be created.
        :param appliance_mode_support: Enables appliance mode on the attachment. When appliance mode is enabled, all traffic flowing between attachments is forwarded to an appliance in a shared VPC to be inspected and processed.
        :param dns_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param ipv6_support: Enables DNS support for the attachment. With DNS Support enabled public DNS names that resolve to a connected VPC will be translated to private IP addresses when resolved in a connected VPC.
        :param name: The name of the Transit Gateway Attachment. Used to tag the attachment with a name that will be displayed in the AWS EC2 console.
        :param subnets: The subnets where the attachment should be created. Can select up to one subnet per Availability Zone.
        '''
        if isinstance(subnets, dict):
            subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d1defbd3f98b5d681f7a4e30d69288e6cdc5223fef0fed304547c78510a96e2)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument transit_gateway", value=transit_gateway, expected_type=type_hints["transit_gateway"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument appliance_mode_support", value=appliance_mode_support, expected_type=type_hints["appliance_mode_support"])
            check_type(argname="argument dns_support", value=dns_support, expected_type=type_hints["dns_support"])
            check_type(argname="argument ipv6_support", value=ipv6_support, expected_type=type_hints["ipv6_support"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "transit_gateway": transit_gateway,
            "vpc": vpc,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if appliance_mode_support is not None:
            self._values["appliance_mode_support"] = appliance_mode_support
        if dns_support is not None:
            self._values["dns_support"] = dns_support
        if ipv6_support is not None:
            self._values["ipv6_support"] = ipv6_support
        if name is not None:
            self._values["name"] = name
        if subnets is not None:
            self._values["subnets"] = subnets

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
    def transit_gateway(self) -> ITransitGateway:
        '''The transit gateway for which the attachment should be created.

        :see: `TransitGatewayVpcAttachment TransitGatewayId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-transitgatewayid>`_
        '''
        result = self._values.get("transit_gateway")
        assert result is not None, "Required property 'transit_gateway' is missing"
        return typing.cast(ITransitGateway, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC where the attachment should be created.

        :see: `TransitGatewayVpcAttachment VpcId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-vpcid>`_
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def appliance_mode_support(self) -> typing.Optional[builtins.bool]:
        '''Enables appliance mode on the attachment.

        When appliance mode is enabled, all traffic flowing between attachments is
        forwarded to an appliance in a shared VPC to be inspected and processed.

        :see: `Appliance in a shared services VPC <https://docs.aws.amazon.com/vpc/latest/tgw/transit-gateway-appliance-scenario.html>`_
        '''
        result = self._values.get("appliance_mode_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dns_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `TransitGatewayVpcAttachment DnsSupport <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-transitgatewayvpcattachment-options.html#cfn-ec2-transitgatewayvpcattachment-options-dnssupport>`_
        '''
        result = self._values.get("dns_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ipv6_support(self) -> typing.Optional[builtins.bool]:
        '''Enables DNS support for the attachment.

        With DNS Support enabled public DNS names that resolve to a connected VPC
        will be translated to private IP addresses when resolved in a connected VPC.

        :see: `IPv6 connectivity with TransitGateway <https://docs.aws.amazon.com/whitepapers/latest/ipv6-on-aws/amazon-vpc-connectivity-options-for-ipv6.html#ipv6-connectivity-with-transit-gateway>`_
        '''
        result = self._values.get("ipv6_support")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Transit Gateway Attachment.

        Used to tag the attachment with a name that will be displayed in the AWS
        EC2 console.

        :see: `TransitGatewayVpcAttachment Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-tags>`_
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The subnets where the attachment should be created.

        Can select up to one subnet per Availability Zone.

        :see: `TransitGatewayVpcAttachment SubnetIds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayvpcattachment.html#cfn-ec2-transitgatewayvpcattachment-subnetids>`_
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransitGatewayAttachmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CustomerGateway",
    "CustomerGatewayAttributes",
    "CustomerGatewayConfigurationRemoteVpnEndpoint",
    "CustomerGatewayProps",
    "CustomerGatewayRemoteVpnEndpoint",
    "FlowLog",
    "FlowLogDataType",
    "FlowLogDestination",
    "FlowLogDestinationConfig",
    "FlowLogField",
    "FlowLogFileFormat",
    "FlowLogFormat",
    "FlowLogProps",
    "FlowLogS3Options",
    "ICustomerGateway",
    "ILocalVpnEndpoint",
    "ILogDestination",
    "IRemoteVpnEndpoint",
    "ITransitGateway",
    "ITransitGatewayAttachment",
    "ITransitGatewayPeeringAttachment",
    "ITransitGatewayRoute",
    "ITransitGatewayRouteTable",
    "LocalVpnEndpointConfiguration",
    "NatProvider",
    "RemoteVpnEndpointConfiguration",
    "SharingOptions",
    "TieredSubnets",
    "TieredSubnetsOptions",
    "TransitGateway",
    "TransitGatewayAttachment",
    "TransitGatewayAttachmentBase",
    "TransitGatewayAttachmentProps",
    "TransitGatewayAttachmentResource",
    "TransitGatewayAttachmentResourceProps",
    "TransitGatewayLocalVpnEndpoint",
    "TransitGatewayNatProvider",
    "TransitGatewayNatProviderOptions",
    "TransitGatewayPeeringAttachment",
    "TransitGatewayPeeringAttachmentImportAttributes",
    "TransitGatewayPeeringAttachmentOptions",
    "TransitGatewayPeeringAttachmentProps",
    "TransitGatewayProps",
    "TransitGatewayRoute",
    "TransitGatewayRouteOptions",
    "TransitGatewayRouteProps",
    "TransitGatewayRouteTable",
    "TransitGatewayRouteTableOptions",
    "TransitGatewayRouteTableProps",
    "TunnelOptions",
    "VpcAttachmentOptions",
    "VpnAttachmentOptions",
    "VpnConnection",
    "VpnConnectionLocalEndpoint",
    "VpnConnectionProps",
    "VpnConnectionRemoteEndpoint",
    "VpnConnectionType",
    "VpnGatewayLocalVpnEndpoint",
]

publication.publish()

def _typecheckingstub__35eab003d889c662b910b407f8e02c5f1e0c594802680266f3389251bf5ac9d3(
    *,
    customer_gateway_id: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e250ab0ff20773956eb3b2131200a7ee56b455ba85d22729b69f588d369a8193(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    ip_address: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    connection_type: typing.Optional[VpnConnectionType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685f60b23d7e8e561b55bc9dca121799b9d63919b8e78b372a1fa549c234455e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    resource_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    flow_log_name: typing.Optional[builtins.str] = None,
    log_format: typing.Optional[FlowLogFormat] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b243acaaaa5840cda314f12b7b4d009805f9002ef9847296dedc4c734cfaa8(
    *,
    destination_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogDestinationType,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    destination_options: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    s3_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52a7eb2a067a774b7223df31becb41f1517c9aa30eb3b326b26ad7504939a991(
    name: builtins.str,
    type: FlowLogDataType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__186041c191f59ab5a16d388d89fb358a9ce5c7c993bd90eb9e6479e368341acd(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011095d32393e36e81237f11a84f5543e965a7ff361a20975a530a17197f4a8e(
    *fields: FlowLogField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cb1f7019aee739ea8276bab9a93a7e6f40b4ebf40d15497239b2c6b1676033e(
    template: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cf487bf8fa03e8840d7c2097f578bf3849b50872d93bdad4cc33d93380f5cd(
    field: FlowLogField,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab60db00df2ad42cfdeb4bac9052956c6ceecbdc94e94e83e7a5b1a8d4db724f(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_type: _aws_cdk_aws_ec2_ceddda9d.FlowLogResourceType,
    destination: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogDestination] = None,
    flow_log_name: typing.Optional[builtins.str] = None,
    log_format: typing.Optional[FlowLogFormat] = None,
    max_aggregation_interval: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogMaxAggregationInterval] = None,
    traffic_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.FlowLogTrafficType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e005d34fc5ab0b60e83479b723ba4e2e86a135e05fd16b18daaac30743245ed(
    *,
    file_format: typing.Optional[FlowLogFileFormat] = None,
    hive_compatible_partitions: typing.Optional[builtins.bool] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    per_hour_partition: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f7fbf7fd0e305a60cc72790e4c2e467542eeb749b6ca114948036c7e283f4e3(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e7dac1ec2cefa56a83155a4b3ff82206bfe5b1607d5af572c5d16cf98aba7a(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c8cc16017de426ad6eb532d21e5db4c058f7a279485763c47026f54ff6b02a(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c530d4e033cb58d409cbdec91a29a99e796c6b5949a8fe0b776e9a57ebda677(
    id: builtins.str,
    *,
    remote_endpoint: IRemoteVpnEndpoint,
    connection_type: typing.Optional[VpnConnectionType] = None,
    static_routes_only: typing.Optional[builtins.bool] = None,
    tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e51602274287d74df7ba0b1c9462a003ef4081742f553f9fccc7d78f9e0f591(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    *,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b44f941842017d2d4c6c21860f08701108fc8a70636475b6b9ab6eb37332692(
    cidr: builtins.str,
    route_table: ITransitGatewayRouteTable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c283c95ccb48c40fb03d7fffd4f63ce7927ef657d47052d65ed9aa32cbd6609a(
    *,
    transit_gateway_id: typing.Optional[builtins.str] = None,
    vpn_gateway_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8914f39fbdc8cc3e17d3f0de803ae8f59bb0822173529944b495b0fe17106662(
    *,
    customer_gateway_asn: jsii.Number,
    customer_gateway_id: builtins.str,
    customer_gateway_ip: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d7430c10280f3e429f967b91e374da316928ba959b852656888cb4465f871ab(
    *,
    allow_external_principals: typing.Optional[builtins.bool] = None,
    auto_discover_accounts: typing.Optional[builtins.bool] = None,
    principals: typing.Optional[typing.Sequence[_ISharedPrincipal_9cde791b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8e89adfc6dfc2ac55a0bed117d1dc5d9b5bc0bcf75bb19367a28bd1c914be4e(
    options: TieredSubnetsOptions,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b0aca7557ca99e67ff904b7cb9edf704abd3cf24b45ecad18d9ccffdb7fcdc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
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
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c3cc263035d23bc511197c75afb01d4a672fd46f5af176fbea6a400bccd00b(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    transit_gateway_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2efd1666acd64cb987a354787ffd07add5920ed5de7e64ad3a01aa00619b7310(
    cidr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9989ffc3141ccddce9a6e8246aa4b31bd76f3ad0a11bbc1cbee86d607e50200d(
    id: builtins.str,
    *,
    remote_endpoint: IRemoteVpnEndpoint,
    connection_type: typing.Optional[VpnConnectionType] = None,
    static_routes_only: typing.Optional[builtins.bool] = None,
    tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fca635a725c4277e8db84123074663ecf20e88af86d11cb8f03c6390d8b7bc8(
    peer: ITransitGateway,
    *,
    name: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac3f5d6f3de4328a56c1673d48d7168afe72b9b6c52725fb46ee3d5121211524(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    *,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b49d47ed81c7ffb2a1650ef26c6a7262dbfbe5b02d6a33f4521aaba40facd96b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4b8aae9fc7113caa263f0a78c3a90cd7457571433a27e89da36b0ae99fc4c6(
    cidr: builtins.str,
    route_table: ITransitGatewayRouteTable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06c53aa420590eceea4fb9b075681a4977d93106ad928386f59f565ada883d5b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    transit_gateway: ITransitGateway,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    appliance_mode_support: typing.Optional[builtins.bool] = None,
    dns_support: typing.Optional[builtins.bool] = None,
    ipv6_support: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9616ce11448deda7c7f7a6abcc3dc7343fd9d23bf7197f988d750a4ed8ab7b9(
    val: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1c15189bbc90871ac0f1cb7928d7a06dc7a543bed65a3917a78189021d8767(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    transit_gateway: ITransitGateway,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    appliance_mode_support: typing.Optional[builtins.bool] = None,
    dns_support: typing.Optional[builtins.bool] = None,
    ipv6_support: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__085d2039b0a4b4caf19e1943608efeb5e97be1be7d732ad9e6c87845449f8c0e(
    transit_gateway: ITransitGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1649477704b8d5959bab11d00a58a0814e904ca0755f79fc92c902b7548831e8(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce5b6c12f42e572c0fd8116f08202bd45321782d0dface0d78758e8ae4afce0(
    subnet: _aws_cdk_aws_ec2_ceddda9d.PrivateSubnet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d866260e3cfdb20c411a4b77ce2ef5ed9046a68ea0356988681824395af2b48(
    *,
    transit_gateway: ITransitGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094bd3c738b0a006e2a59600942e6cb57ce41b066d2acabef2f32729f9b6c14c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    local_transit_gateway: ITransitGateway,
    peer_transit_gateway: ITransitGateway,
    name: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64bc0ce43e9c832901d2f4073f54276e12b588a41c623026825482bf1d43c63(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b9ddfaf131e6a5091a636a0dad2dd2579ae4140b68c99fe5fee2e2506d45105(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    arn: typing.Optional[builtins.str] = None,
    attachment_id: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
    status_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe35553be2f81ae71d207839c426c22b6542d57d2604a744dec33a748b8631f6(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    attachment_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17eab9c1c0483a81bcbc3cfb19dfc9cd1902962956a39306a77b2b041a6f2182(
    *,
    arn: typing.Optional[builtins.str] = None,
    attachment_id: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[builtins.str] = None,
    status_message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25aee8c8ebebcfa519a0f5706458a5669157c84f5af528e93a86402ac7c50aae(
    *,
    name: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b477916bc8b985cd2d6731bf57489e1a7c94f20fccf7711617cdf0d1bd25beb(
    *,
    name: typing.Optional[builtins.str] = None,
    peer_account_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    local_transit_gateway: ITransitGateway,
    peer_transit_gateway: ITransitGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34be88b6da81fce37f3376e8b1fd1aff7e222c4b2fb4ab8e879c634868d58a81(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
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
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472f0a715c24828891d913514782594fd48e540d0192f96901c525a6f2c9845f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cidr: builtins.str,
    route_table: ITransitGatewayRouteTable,
    attachment: typing.Optional[ITransitGatewayAttachment] = None,
    blackhole: typing.Optional[builtins.bool] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e915393403cdd527b11e940ce216647c74d6e6b709f726e821e12fa1b470873d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    transit_gateway_route_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac305487ec828686fdbbd312914a754c55ca742068c194f48ac724cf9aef071(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    cidr: builtins.str,
    attachment: typing.Optional[ITransitGatewayAttachment] = None,
    blackhole: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f603e48c36f0aabd623aee3c75f3f94dcd322957a71fb2d3539585045d2c00(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    cidr: builtins.str,
    route_table: ITransitGatewayRouteTable,
    attachment: typing.Optional[ITransitGatewayAttachment] = None,
    blackhole: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf9f0e3a9c51ac3498209cf81371557e5b56db1c03ff409740d882fde1cacda7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    transit_gateway: ITransitGateway,
    name: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ddc972512f9b73360cad75e0fd028f815d92130c441ed49e42d40f77ebd8fff(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    transit_gateway_route_table_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba42798c9102c3419b7c375a3d8ce27fef028001fb7cc17a2798c1aad61854ff(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae02cfe78ce98fb4f7880816162efbcf405d70470d3f4d83605632beeb8a6f7(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    transit_gateway: ITransitGateway,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4312d41d9a05862a91818a278fa16d6a73ff75dcd46ad08d731c98c54086e195(
    *,
    inside_cidr: typing.Optional[builtins.str] = None,
    pre_shared_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dff1261f60aa49a2037d280e97af162d26181faeabf698640e4139891619042(
    *,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68fcd54ad9cdc22e3838841971cc60da339a1c6b65f45abf9839c71f80a1ad8(
    *,
    remote_endpoint: IRemoteVpnEndpoint,
    connection_type: typing.Optional[VpnConnectionType] = None,
    static_routes_only: typing.Optional[builtins.bool] = None,
    tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1711f2c24c8b7a52cb1e23aa7c00f2ee31a53d068176d8b694ba413b49c85e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    local_endpoint: ILocalVpnEndpoint,
    remote_endpoint: IRemoteVpnEndpoint,
    connection_type: typing.Optional[VpnConnectionType] = None,
    static_routes_only: typing.Optional[builtins.bool] = None,
    tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1943d41246b0671229072a9d9650d8d0f9f66aaf7b458b59f96ab84ad35da3(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ddda611ef5d00d1dbfb980664aaf365a9109585805083204f9dd201f73b937(
    transit_gateway: ITransitGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255c4f2f88d39694addb3404e05f43b66d5900dda0a83d02497e7579af1e9f87(
    vpn_gateway: _aws_cdk_aws_ec2_ceddda9d.IVpnGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f1ecffd701acc1acc5674e16c0bca0e65f2e2327e74bfb0fe4021722919ad1(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    local_endpoint: ILocalVpnEndpoint,
    remote_endpoint: IRemoteVpnEndpoint,
    connection_type: typing.Optional[VpnConnectionType] = None,
    static_routes_only: typing.Optional[builtins.bool] = None,
    tunnel_configurations: typing.Optional[typing.Sequence[typing.Union[TunnelOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec3ce1dacbcb72f74a7ad181d5838d1e71517bb5fc661cee673e3d13cf35dbe(
    customer_gateway: ICustomerGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c531bfa20e4b82501cd1840a34d989b2593246657ad35703dfdd6156ae409b(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c9d0488d52533eda0e8e013c7c8dc98375bf35fbfb4d0119edfc6dafc3add2(
    vpn_gateway: _aws_cdk_aws_ec2_ceddda9d.IVpnGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b034f4493a7f4e0ef9f3e966d78f68321b168b61b98dda5c4dace5477a2b5d5e(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7814523b269d29ae5e2e42aa21c1f81bdc5a471fe5e300b0768c03a21b6a6f91(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ip_address: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    connection_type: typing.Optional[VpnConnectionType] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cee3aaa3f8d41d377b44df84c1bd31404fc3c74c1f3d4d50f41733f5ceaeaba(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    customer_gateway_id: builtins.str,
    bgp_asn: typing.Optional[jsii.Number] = None,
    ip_address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__745b377e3c9abac41a861ca1050cfc8012b832cecc7ce152fed229d86ee5e4ae(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    customer_gateway_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__376ae140d941de56c115f01c627b230e0ffb07b7247eb9a061e389e071218f36(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39f263303ec59ccc7954f0b56dc5825a43956cfa48fc4648959c032c858f8a2f(
    customer_gateway: ICustomerGateway,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd8797d122fda919f703e603d2c593c1fe151dbc800704673ccc25360cdf5d3e(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5daa8ff9c63f8f6617139a25d0c2042756ce3ab0da13e5f5a51634e4b9f7ab0c(
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d11b43c926a884fe3a73d0b44332cd0342bba0c0e2d7bcac16489f068e1191b(
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    *,
    file_format: typing.Optional[FlowLogFileFormat] = None,
    hive_compatible_partitions: typing.Optional[builtins.bool] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    per_hour_partition: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6be248e60a194fe1d0bcf9dc9398b94b088ef8e6ca462c0c85ef25246e79057(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27ee6909fddcfad51f5ddc3aee4e522d6f5fdeab0a0272e67e7d62c063924d6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    transit_gateway: ITransitGateway,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    appliance_mode_support: typing.Optional[builtins.bool] = None,
    dns_support: typing.Optional[builtins.bool] = None,
    ipv6_support: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135a7b7bec5b4b7974ff32ebff887b94cc20f2b37d6736525ec2c4e7c4b5c542(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    transit_gateway_attachment_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1defbd3f98b5d681f7a4e30d69288e6cdc5223fef0fed304547c78510a96e2(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    transit_gateway: ITransitGateway,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    appliance_mode_support: typing.Optional[builtins.bool] = None,
    dns_support: typing.Optional[builtins.bool] = None,
    ipv6_support: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
