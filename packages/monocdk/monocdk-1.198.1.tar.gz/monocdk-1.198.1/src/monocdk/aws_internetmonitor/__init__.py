'''
# AWS::InternetMonitor Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as internetmonitor
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for InternetMonitor construct libraries](https://constructs.dev/search?q=internetmonitor)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::InternetMonitor resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_InternetMonitor.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::InternetMonitor](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_InternetMonitor.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnMonitor(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_internetmonitor.CfnMonitor",
):
    '''A CloudFormation ``AWS::InternetMonitor::Monitor``.

    The ``AWS::InternetMonitor::Monitor`` resource is an Internet Monitor resource type that contains information about how you create a monitor in Amazon CloudWatch Internet Monitor. A monitor in Internet Monitor provides visibility into performance and availability between your applications hosted on AWS and your end users, using a traffic profile that it creates based on the application resources that you add: Virtual Private Clouds (VPCs), Amazon CloudFront distributions, or WorkSpaces directories.

    Internet Monitor also alerts you to internet issues that impact your application in the city-networks (geographies and networks) where your end users use it. With Internet Monitor, you can quickly pinpoint the locations and providers that are affected, so that you can address the issue.

    For more information, see `Using Amazon CloudWatch Internet Monitor <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-InternetMonitor.html>`_ in the *Amazon CloudWatch User Guide* .

    :cloudformationResource: AWS::InternetMonitor::Monitor
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_internetmonitor as internetmonitor
        
        cfn_monitor = internetmonitor.CfnMonitor(self, "MyCfnMonitor",
            max_city_networks_to_monitor=123,
            monitor_name="monitorName",
            resources=["resources"],
            resources_to_add=["resourcesToAdd"],
            resources_to_remove=["resourcesToRemove"],
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::InternetMonitor::Monitor``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param max_city_networks_to_monitor: The maximum number of city-networks to monitor for your resources. A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through. For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .
        :param monitor_name: The name of the monitor. A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).
        :param resources: The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs).
        :param resources_to_add: The resources to add to a monitor, which you provide as a set of Amazon Resource Names (ARNs). You can add a combination of Virtual Private Clouds (VPCs) and Amazon CloudFront distributions, or you can add WorkSpaces directories. You can't add all three types of resources. .. epigraph:: If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity.
        :param resources_to_remove: The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs).
        :param status: The status of a monitor. The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .
        :param tags: The tags for a monitor, listed as a set of *key:value* pairs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8288214d0e139e75c8eb3f24837ffbaeae7c9f3ceab8f77b89e624a2dc83dab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMonitorProps(
            max_city_networks_to_monitor=max_city_networks_to_monitor,
            monitor_name=monitor_name,
            resources=resources,
            resources_to_add=resources_to_add,
            resources_to_remove=resources_to_remove,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89df1235bee67bd3c56a8eed020e69c69151fbc34d06e305a4df4556e9db8ec4)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__833bdfca48b5fe64af911a43ee57490566fd19677d299b79db5d572b62945f8f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time when the monitor was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''The last time that the monitor was modified.

        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrMonitorArn")
    def attr_monitor_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the monitor.

        :cloudformationAttribute: MonitorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMonitorArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProcessingStatus")
    def attr_processing_status(self) -> builtins.str:
        '''The health of data processing for the monitor.

        For more information, see ``ProcessingStatus`` under `MonitorListMember <https://docs.aws.amazon.com/internet-monitor/latest/api/API_MonitorListMember.html>`_ in the *Amazon CloudWatch Internet Monitor API Reference* .

        :cloudformationAttribute: ProcessingStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProcessingStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrProcessingStatusInfo")
    def attr_processing_status_info(self) -> builtins.str:
        '''Additional information about the health of the data processing for the monitor.

        :cloudformationAttribute: ProcessingStatusInfo
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProcessingStatusInfo"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags for a monitor, listed as a set of *key:value* pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="maxCityNetworksToMonitor")
    def max_city_networks_to_monitor(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of city-networks to monitor for your resources.

        A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through.

        For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-maxcitynetworkstomonitor
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCityNetworksToMonitor"))

    @max_city_networks_to_monitor.setter
    def max_city_networks_to_monitor(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadd37c4bed7d8a132e06303f8cb9e0b31e2686df470ac19a37c54628e7555b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCityNetworksToMonitor", value)

    @builtins.property
    @jsii.member(jsii_name="monitorName")
    def monitor_name(self) -> typing.Optional[builtins.str]:
        '''The name of the monitor.

        A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-monitorname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorName"))

    @monitor_name.setter
    def monitor_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2baf8f977cdd40e329ee18d87a027f5d73cb15e7121918c32acf6aa82aa1866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorName", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resources
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be877ea1ed5cee094e537200311a05c129f78825232517ca375503ef834fc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)

    @builtins.property
    @jsii.member(jsii_name="resourcesToAdd")
    def resources_to_add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to add to a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        You can add a combination of Virtual Private Clouds (VPCs) and Amazon CloudFront distributions, or you can add WorkSpaces directories. You can't add all three types of resources.
        .. epigraph::

           If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoadd
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesToAdd"))

    @resources_to_add.setter
    def resources_to_add(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f4b12fa48ed3cc60ae2db6782916978ea0388e4b766565e2afc88e1aeb0dc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcesToAdd", value)

    @builtins.property
    @jsii.member(jsii_name="resourcesToRemove")
    def resources_to_remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoremove
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesToRemove"))

    @resources_to_remove.setter
    def resources_to_remove(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dad63f15cf40f42ac862dfeb1ab32aa7f74d5c8a9fb980c2653e6e2f8d61af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcesToRemove", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of a monitor.

        The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__790ac62ed1e114ec5c2cf265ad795f65b513369344c76a1dfcce7fef3d86b752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="monocdk.aws_internetmonitor.CfnMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_city_networks_to_monitor": "maxCityNetworksToMonitor",
        "monitor_name": "monitorName",
        "resources": "resources",
        "resources_to_add": "resourcesToAdd",
        "resources_to_remove": "resourcesToRemove",
        "status": "status",
        "tags": "tags",
    },
)
class CfnMonitorProps:
    def __init__(
        self,
        *,
        max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
        monitor_name: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnMonitor``.

        :param max_city_networks_to_monitor: The maximum number of city-networks to monitor for your resources. A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through. For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .
        :param monitor_name: The name of the monitor. A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).
        :param resources: The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs).
        :param resources_to_add: The resources to add to a monitor, which you provide as a set of Amazon Resource Names (ARNs). You can add a combination of Virtual Private Clouds (VPCs) and Amazon CloudFront distributions, or you can add WorkSpaces directories. You can't add all three types of resources. .. epigraph:: If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity.
        :param resources_to_remove: The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs).
        :param status: The status of a monitor. The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .
        :param tags: The tags for a monitor, listed as a set of *key:value* pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_internetmonitor as internetmonitor
            
            cfn_monitor_props = internetmonitor.CfnMonitorProps(
                max_city_networks_to_monitor=123,
                monitor_name="monitorName",
                resources=["resources"],
                resources_to_add=["resourcesToAdd"],
                resources_to_remove=["resourcesToRemove"],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d178222fe74cf3fd31c0441237b28575604b4f1b919abe01019ccb378d5118c8)
            check_type(argname="argument max_city_networks_to_monitor", value=max_city_networks_to_monitor, expected_type=type_hints["max_city_networks_to_monitor"])
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument resources_to_add", value=resources_to_add, expected_type=type_hints["resources_to_add"])
            check_type(argname="argument resources_to_remove", value=resources_to_remove, expected_type=type_hints["resources_to_remove"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_city_networks_to_monitor is not None:
            self._values["max_city_networks_to_monitor"] = max_city_networks_to_monitor
        if monitor_name is not None:
            self._values["monitor_name"] = monitor_name
        if resources is not None:
            self._values["resources"] = resources
        if resources_to_add is not None:
            self._values["resources_to_add"] = resources_to_add
        if resources_to_remove is not None:
            self._values["resources_to_remove"] = resources_to_remove
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def max_city_networks_to_monitor(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of city-networks to monitor for your resources.

        A city-network is the location (city) where clients access your application resources from and the network, such as an internet service provider, that clients access the resources through.

        For more information, see `Choosing a city-network maximum value <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/IMCityNetworksMaximum.html>`_ in *Using Amazon CloudWatch Internet Monitor* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-maxcitynetworkstomonitor
        '''
        result = self._values.get("max_city_networks_to_monitor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_name(self) -> typing.Optional[builtins.str]:
        '''The name of the monitor.

        A monitor name can contain only alphanumeric characters, dashes (-), periods (.), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-monitorname
        '''
        result = self._values.get("monitor_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources that have been added for the monitor, listed by their Amazon Resource Names (ARNs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources_to_add(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to add to a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        You can add a combination of Virtual Private Clouds (VPCs) and Amazon CloudFront distributions, or you can add WorkSpaces directories. You can't add all three types of resources.
        .. epigraph::

           If you add only VPC resources, at least one VPC must have an Internet Gateway attached to it, to make sure that it has internet connectivity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoadd
        '''
        result = self._values.get("resources_to_add")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources_to_remove(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources to remove from a monitor, which you provide as a set of Amazon Resource Names (ARNs).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-resourcestoremove
        '''
        result = self._values.get("resources_to_remove")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of a monitor.

        The accepted values that you can specify for ``Status`` are ``ACTIVE`` and ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags for a monitor, listed as a set of *key:value* pairs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-internetmonitor-monitor.html#cfn-internetmonitor-monitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMonitor",
    "CfnMonitorProps",
]

publication.publish()

def _typecheckingstub__b8288214d0e139e75c8eb3f24837ffbaeae7c9f3ceab8f77b89e624a2dc83dab(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
    monitor_name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89df1235bee67bd3c56a8eed020e69c69151fbc34d06e305a4df4556e9db8ec4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833bdfca48b5fe64af911a43ee57490566fd19677d299b79db5d572b62945f8f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadd37c4bed7d8a132e06303f8cb9e0b31e2686df470ac19a37c54628e7555b6(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2baf8f977cdd40e329ee18d87a027f5d73cb15e7121918c32acf6aa82aa1866(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be877ea1ed5cee094e537200311a05c129f78825232517ca375503ef834fc42(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f4b12fa48ed3cc60ae2db6782916978ea0388e4b766565e2afc88e1aeb0dc2(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dad63f15cf40f42ac862dfeb1ab32aa7f74d5c8a9fb980c2653e6e2f8d61af(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__790ac62ed1e114ec5c2cf265ad795f65b513369344c76a1dfcce7fef3d86b752(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d178222fe74cf3fd31c0441237b28575604b4f1b919abe01019ccb378d5118c8(
    *,
    max_city_networks_to_monitor: typing.Optional[jsii.Number] = None,
    monitor_name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_add: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_to_remove: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
