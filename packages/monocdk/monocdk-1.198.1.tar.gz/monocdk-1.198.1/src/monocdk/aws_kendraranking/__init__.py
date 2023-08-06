'''
# AWS::KendraRanking Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as kendraranking
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for KendraRanking construct libraries](https://constructs.dev/search?q=kendraranking)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::KendraRanking resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KendraRanking.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::KendraRanking](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KendraRanking.html).

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
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnExecutionPlan(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_kendraranking.CfnExecutionPlan",
):
    '''A CloudFormation ``AWS::KendraRanking::ExecutionPlan``.

    Creates a rescore execution plan. A rescore execution plan is an Amazon Kendra Intelligent Ranking resource used for provisioning the ``Rescore`` API. You set the number of capacity units that you require for Amazon Kendra Intelligent Ranking to rescore or re-rank a search service's results.

    For an example of using the ``CreateRescoreExecutionPlan`` API, including using the Python and Java SDKs, see `Semantically ranking a search service's results <https://docs.aws.amazon.com/kendra/latest/dg/search-service-rerank.html>`_ .

    :cloudformationResource: AWS::KendraRanking::ExecutionPlan
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_kendraranking as kendraranking
        
        cfn_execution_plan = kendraranking.CfnExecutionPlan(self, "MyCfnExecutionPlan",
            name="name",
        
            # the properties below are optional
            capacity_units=kendraranking.CfnExecutionPlan.CapacityUnitsConfigurationProperty(
                rescore_capacity_units=123
            ),
            description="description",
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
        name: builtins.str,
        capacity_units: typing.Optional[typing.Union[typing.Union["CfnExecutionPlan.CapacityUnitsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::KendraRanking::ExecutionPlan``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the rescore execution plan.
        :param capacity_units: You can set additional capacity units to meet the needs of your rescore execution plan. You are given a single capacity unit by default. If you want to use the default capacity, you don't set additional capacity units. For more information on the default capacity and additional capacity units, see `Adjusting capacity <https://docs.aws.amazon.com/kendra/latest/dg/adjusting-capacity.html>`_ .
        :param description: A description for the rescore execution plan.
        :param tags: A list of key-value pairs that identify or categorize your rescore execution plan. You can also use tags to help control access to the rescore execution plan. Tag keys and values can consist of Unicode letters, digits, white space. They can also consist of underscore, period, colon, equal, plus, and asperand.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5efc9ecc5ddaa7d517d616a368383d360596eae9697703383765f602378ce807)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnExecutionPlanProps(
            name=name,
            capacity_units=capacity_units,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf82b9eb4e36789c928cb4456f43a87c928372d86bc3fa5afeca6ee6f2d835e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4b3a7df725fa1f98d5e9141e2ba9da30e6ee6bb3f4551d8541034ecda7ae4a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the rescore execution plan.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier of the rescore execution plan.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of key-value pairs that identify or categorize your rescore execution plan.

        You can also use tags to help control access to the rescore execution plan. Tag keys and values can consist of Unicode letters, digits, white space. They can also consist of underscore, period, colon, equal, plus, and asperand.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the rescore execution plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2bbc545c7d554c74ffed6ec2db556e8f75fdbb517d73245e586d20c077cb4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="capacityUnits")
    def capacity_units(
        self,
    ) -> typing.Optional[typing.Union["CfnExecutionPlan.CapacityUnitsConfigurationProperty", _IResolvable_a771d0ef]]:
        '''You can set additional capacity units to meet the needs of your rescore execution plan.

        You are given a single capacity unit by default. If you want to use the default capacity, you don't set additional capacity units. For more information on the default capacity and additional capacity units, see `Adjusting capacity <https://docs.aws.amazon.com/kendra/latest/dg/adjusting-capacity.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-capacityunits
        '''
        return typing.cast(typing.Optional[typing.Union["CfnExecutionPlan.CapacityUnitsConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "capacityUnits"))

    @capacity_units.setter
    def capacity_units(
        self,
        value: typing.Optional[typing.Union["CfnExecutionPlan.CapacityUnitsConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c789bc5a4213ba91ca3b651330f59df32293945cc6a4c34e713200c9fc6c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityUnits", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the rescore execution plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1663a783ee26610a329c59e7a50a296090969cafe082f21c29a5058d07d96529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_kendraranking.CfnExecutionPlan.CapacityUnitsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"rescore_capacity_units": "rescoreCapacityUnits"},
    )
    class CapacityUnitsConfigurationProperty:
        def __init__(self, *, rescore_capacity_units: jsii.Number) -> None:
            '''Sets additional capacity units configured for your rescore execution plan.

            A rescore execution plan is an Amazon Kendra Intelligent Ranking resource used for provisioning the ``Rescore`` API. You can add and remove capacity units to fit your usage requirements.

            :param rescore_capacity_units: The amount of extra capacity for your rescore execution plan. A single extra capacity unit for a rescore execution plan provides 0.01 rescore requests per second. You can add up to 1000 extra capacity units.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendraranking-executionplan-capacityunitsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_kendraranking as kendraranking
                
                capacity_units_configuration_property = kendraranking.CfnExecutionPlan.CapacityUnitsConfigurationProperty(
                    rescore_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c56ae59223c18b2a752fdda7b49eba78eced629583054d017b133edfd8c65810)
                check_type(argname="argument rescore_capacity_units", value=rescore_capacity_units, expected_type=type_hints["rescore_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rescore_capacity_units": rescore_capacity_units,
            }

        @builtins.property
        def rescore_capacity_units(self) -> jsii.Number:
            '''The amount of extra capacity for your rescore execution plan.

            A single extra capacity unit for a rescore execution plan provides 0.01 rescore requests per second. You can add up to 1000 extra capacity units.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendraranking-executionplan-capacityunitsconfiguration.html#cfn-kendraranking-executionplan-capacityunitsconfiguration-rescorecapacityunits
            '''
            result = self._values.get("rescore_capacity_units")
            assert result is not None, "Required property 'rescore_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityUnitsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_kendraranking.CfnExecutionPlanProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "capacity_units": "capacityUnits",
        "description": "description",
        "tags": "tags",
    },
)
class CfnExecutionPlanProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        capacity_units: typing.Optional[typing.Union[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnExecutionPlan``.

        :param name: A name for the rescore execution plan.
        :param capacity_units: You can set additional capacity units to meet the needs of your rescore execution plan. You are given a single capacity unit by default. If you want to use the default capacity, you don't set additional capacity units. For more information on the default capacity and additional capacity units, see `Adjusting capacity <https://docs.aws.amazon.com/kendra/latest/dg/adjusting-capacity.html>`_ .
        :param description: A description for the rescore execution plan.
        :param tags: A list of key-value pairs that identify or categorize your rescore execution plan. You can also use tags to help control access to the rescore execution plan. Tag keys and values can consist of Unicode letters, digits, white space. They can also consist of underscore, period, colon, equal, plus, and asperand.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_kendraranking as kendraranking
            
            cfn_execution_plan_props = kendraranking.CfnExecutionPlanProps(
                name="name",
            
                # the properties below are optional
                capacity_units=kendraranking.CfnExecutionPlan.CapacityUnitsConfigurationProperty(
                    rescore_capacity_units=123
                ),
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca21e3c8b0ebcffe7c641850061f9c5db7d5223b7f253f3eef125ba9355caca7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if capacity_units is not None:
            self._values["capacity_units"] = capacity_units
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the rescore execution plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_units(
        self,
    ) -> typing.Optional[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, _IResolvable_a771d0ef]]:
        '''You can set additional capacity units to meet the needs of your rescore execution plan.

        You are given a single capacity unit by default. If you want to use the default capacity, you don't set additional capacity units. For more information on the default capacity and additional capacity units, see `Adjusting capacity <https://docs.aws.amazon.com/kendra/latest/dg/adjusting-capacity.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-capacityunits
        '''
        result = self._values.get("capacity_units")
        return typing.cast(typing.Optional[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the rescore execution plan.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of key-value pairs that identify or categorize your rescore execution plan.

        You can also use tags to help control access to the rescore execution plan. Tag keys and values can consist of Unicode letters, digits, white space. They can also consist of underscore, period, colon, equal, plus, and asperand.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendraranking-executionplan.html#cfn-kendraranking-executionplan-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExecutionPlanProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnExecutionPlan",
    "CfnExecutionPlanProps",
]

publication.publish()

def _typecheckingstub__5efc9ecc5ddaa7d517d616a368383d360596eae9697703383765f602378ce807(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    capacity_units: typing.Optional[typing.Union[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf82b9eb4e36789c928cb4456f43a87c928372d86bc3fa5afeca6ee6f2d835e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4b3a7df725fa1f98d5e9141e2ba9da30e6ee6bb3f4551d8541034ecda7ae4a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2bbc545c7d554c74ffed6ec2db556e8f75fdbb517d73245e586d20c077cb4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c789bc5a4213ba91ca3b651330f59df32293945cc6a4c34e713200c9fc6c8c(
    value: typing.Optional[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1663a783ee26610a329c59e7a50a296090969cafe082f21c29a5058d07d96529(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56ae59223c18b2a752fdda7b49eba78eced629583054d017b133edfd8c65810(
    *,
    rescore_capacity_units: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca21e3c8b0ebcffe7c641850061f9c5db7d5223b7f253f3eef125ba9355caca7(
    *,
    name: builtins.str,
    capacity_units: typing.Optional[typing.Union[typing.Union[CfnExecutionPlan.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
