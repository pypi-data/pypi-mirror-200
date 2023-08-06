'''
# AWS::VpcLattice Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as vpclattice
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for VpcLattice construct libraries](https://constructs.dev/search?q=vpclattice)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::VpcLattice resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VpcLattice.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::VpcLattice](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VpcLattice.html).

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
class CfnAccessLogSubscription(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnAccessLogSubscription",
):
    '''A CloudFormation ``AWS::VpcLattice::AccessLogSubscription``.

    :cloudformationResource: AWS::VpcLattice::AccessLogSubscription
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_access_log_subscription = vpclattice.CfnAccessLogSubscription(self, "MyCfnAccessLogSubscription",
            destination_arn="destinationArn",
        
            # the properties below are optional
            resource_identifier="resourceIdentifier",
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
        destination_arn: builtins.str,
        resource_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::AccessLogSubscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: ``AWS::VpcLattice::AccessLogSubscription.DestinationArn``.
        :param resource_identifier: ``AWS::VpcLattice::AccessLogSubscription.ResourceIdentifier``.
        :param tags: ``AWS::VpcLattice::AccessLogSubscription.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2554a5601956dd41564578a3b8a446d5383ffe0ad4f07b56d0527b43b3972aad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessLogSubscriptionProps(
            destination_arn=destination_arn,
            resource_identifier=resource_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6d6ba72b861a52dd99be6234aaa874f7cd84cfb8d7e78e58b9aad7d7c5063c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0b646175739ec0dbf2ea344e518f9307479d050e3927fc8516554310d6b5402)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceId")
    def attr_resource_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::AccessLogSubscription.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''``AWS::VpcLattice::AccessLogSubscription.DestinationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-destinationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2e08d2dec7e7f7e53aa09ffc506ca3df40a3ff9f7a466ca16b745c18a4bfc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceIdentifier")
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::AccessLogSubscription.ResourceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-resourceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdentifier"))

    @resource_identifier.setter
    def resource_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be5d18217d19eedd701793852cf6eb730ba0c89c8d9e1de1a23e8e538674dd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIdentifier", value)


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnAccessLogSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "resource_identifier": "resourceIdentifier",
        "tags": "tags",
    },
)
class CfnAccessLogSubscriptionProps:
    def __init__(
        self,
        *,
        destination_arn: builtins.str,
        resource_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessLogSubscription``.

        :param destination_arn: ``AWS::VpcLattice::AccessLogSubscription.DestinationArn``.
        :param resource_identifier: ``AWS::VpcLattice::AccessLogSubscription.ResourceIdentifier``.
        :param tags: ``AWS::VpcLattice::AccessLogSubscription.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_access_log_subscription_props = vpclattice.CfnAccessLogSubscriptionProps(
                destination_arn="destinationArn",
            
                # the properties below are optional
                resource_identifier="resourceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7081ac6eeae148c3cfe9e0eda14f91a76e586e86c63a0aee58fd7e311798e0a)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
        }
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''``AWS::VpcLattice::AccessLogSubscription.DestinationArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-destinationarn
        '''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::AccessLogSubscription.ResourceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::AccessLogSubscription.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessLogSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAuthPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnAuthPolicy",
):
    '''A CloudFormation ``AWS::VpcLattice::AuthPolicy``.

    :cloudformationResource: AWS::VpcLattice::AuthPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        # policy: Any
        
        cfn_auth_policy = vpclattice.CfnAuthPolicy(self, "MyCfnAuthPolicy",
            policy=policy,
            resource_identifier="resourceIdentifier"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy: typing.Any,
        resource_identifier: builtins.str,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::AuthPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: ``AWS::VpcLattice::AuthPolicy.Policy``.
        :param resource_identifier: ``AWS::VpcLattice::AuthPolicy.ResourceIdentifier``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb07d80bcb2006dcce0a495882667cff6639e05f6d436c406a31f89bd541ed92)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAuthPolicyProps(
            policy=policy, resource_identifier=resource_identifier
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b3145968a18d173c12730fb8d3c1811676f0ade5d11793bc7f0e5dd1e501e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d841630368f87db25dd04aa10f18571cd808a6aeddf35cf6144a2682fd4e5ae)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''``AWS::VpcLattice::AuthPolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e7577cf43460ca5058735b3a896fa64eba1fb0d2c1dbe0d86c5803199b3ee72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="resourceIdentifier")
    def resource_identifier(self) -> builtins.str:
        '''``AWS::VpcLattice::AuthPolicy.ResourceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-resourceidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceIdentifier"))

    @resource_identifier.setter
    def resource_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8831fdd266e45ece0d675a2d8a4887e935cfc21da31aa85ceb0a24306a8c2c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIdentifier", value)


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnAuthPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_identifier": "resourceIdentifier"},
)
class CfnAuthPolicyProps:
    def __init__(
        self,
        *,
        policy: typing.Any,
        resource_identifier: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnAuthPolicy``.

        :param policy: ``AWS::VpcLattice::AuthPolicy.Policy``.
        :param resource_identifier: ``AWS::VpcLattice::AuthPolicy.ResourceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            # policy: Any
            
            cfn_auth_policy_props = vpclattice.CfnAuthPolicyProps(
                policy=policy,
                resource_identifier="resourceIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb83fd0815d0bf2d1ff7452cc8a482ce5f2275b83bad256969f2f337b285800)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "resource_identifier": resource_identifier,
        }

    @builtins.property
    def policy(self) -> typing.Any:
        '''``AWS::VpcLattice::AuthPolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_identifier(self) -> builtins.str:
        '''``AWS::VpcLattice::AuthPolicy.ResourceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        assert result is not None, "Required property 'resource_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnListener(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnListener",
):
    '''A CloudFormation ``AWS::VpcLattice::Listener``.

    :cloudformationResource: AWS::VpcLattice::Listener
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_listener = vpclattice.CfnListener(self, "MyCfnListener",
            default_action=vpclattice.CfnListener.DefaultActionProperty(
                forward=vpclattice.CfnListener.ForwardProperty(
                    target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
        
                        # the properties below are optional
                        weight=123
                    )]
                )
            ),
            protocol="protocol",
        
            # the properties below are optional
            name="name",
            port=123,
            service_identifier="serviceIdentifier",
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
        default_action: typing.Union[typing.Union["CfnListener.DefaultActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        protocol: builtins.str,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: ``AWS::VpcLattice::Listener.DefaultAction``.
        :param protocol: ``AWS::VpcLattice::Listener.Protocol``.
        :param name: ``AWS::VpcLattice::Listener.Name``.
        :param port: ``AWS::VpcLattice::Listener.Port``.
        :param service_identifier: ``AWS::VpcLattice::Listener.ServiceIdentifier``.
        :param tags: ``AWS::VpcLattice::Listener.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e57a2f8baf2dc402cfc5f688e6924c41f139df5febcd34ee1930966f7d5d4f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnListenerProps(
            default_action=default_action,
            protocol=protocol,
            name=name,
            port=port,
            service_identifier=service_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdbf3a5218b7e4dacd8e75e9394a7552e6b187f38d32b2f5d551236e6989ff1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52239813405069c083582b66c87a4c1d5303aaa7f8999025384fff2a6ee602b9)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceId")
    def attr_service_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::Listener.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(
        self,
    ) -> typing.Union["CfnListener.DefaultActionProperty", _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Listener.DefaultAction``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-defaultaction
        '''
        return typing.cast(typing.Union["CfnListener.DefaultActionProperty", _IResolvable_a771d0ef], jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(
        self,
        value: typing.Union["CfnListener.DefaultActionProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6fb621c98dd7bec66a46cdf17faef2b11ac731510ec3ba157dd78bdfa92e11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''``AWS::VpcLattice::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2afec20cc8c3409afbfb1fd7540444751897cfc3bf8f7c3fbc64e8c6b1f441)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Listener.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f45d51511465e0932e0908c9ceadbfcffcb935f33d005cb1dbedb35d1403483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::VpcLattice::Listener.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e54de6a5e277c1324dd2aaf09b8f3b5f52006a3c686503a8b8696c65ee51419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Listener.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41cdaa2e7a75522b5c699d72dc9a266e6e62e254db38ded8f7f6e2dda669733b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnListener.DefaultActionProperty",
        jsii_struct_bases=[],
        name_mapping={"forward": "forward"},
    )
    class DefaultActionProperty:
        def __init__(
            self,
            *,
            forward: typing.Union[typing.Union["CfnListener.ForwardProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param forward: ``CfnListener.DefaultActionProperty.Forward``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                default_action_property = vpclattice.CfnListener.DefaultActionProperty(
                    forward=vpclattice.CfnListener.ForwardProperty(
                        target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                
                            # the properties below are optional
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0252509a3c889dc05db1aef9ed4389592ed4f590fc11d15a5650f9d29fb825c4)
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "forward": forward,
            }

        @builtins.property
        def forward(
            self,
        ) -> typing.Union["CfnListener.ForwardProperty", _IResolvable_a771d0ef]:
            '''``CfnListener.DefaultActionProperty.Forward``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html#cfn-vpclattice-listener-defaultaction-forward
            '''
            result = self._values.get("forward")
            assert result is not None, "Required property 'forward' is missing"
            return typing.cast(typing.Union["CfnListener.ForwardProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnListener.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnListener.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param target_groups: ``CfnListener.ForwardProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                forward_property = vpclattice.CfnListener.ForwardProperty(
                    target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                
                        # the properties below are optional
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c561c073b6867961d18d77790bb70f811011df3eb483c8759abd5a4694544fb)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_groups": target_groups,
            }

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnListener.WeightedTargetGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnListener.ForwardProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html#cfn-vpclattice-listener-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            assert result is not None, "Required property 'target_groups' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnListener.WeightedTargetGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnListener.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: builtins.str,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param target_group_identifier: ``CfnListener.WeightedTargetGroupProperty.TargetGroupIdentifier``.
            :param weight: ``CfnListener.WeightedTargetGroupProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                weighted_target_group_property = vpclattice.CfnListener.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                
                    # the properties below are optional
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efdb89a0279d863b1be6b0d89dd10798c4ed609509c5853df65339315a501680)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_group_identifier": target_group_identifier,
            }
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> builtins.str:
            '''``CfnListener.WeightedTargetGroupProperty.TargetGroupIdentifier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            assert result is not None, "Required property 'target_group_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnListener.WeightedTargetGroupProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "protocol": "protocol",
        "name": "name",
        "port": "port",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        default_action: typing.Union[typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        protocol: builtins.str,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnListener``.

        :param default_action: ``AWS::VpcLattice::Listener.DefaultAction``.
        :param protocol: ``AWS::VpcLattice::Listener.Protocol``.
        :param name: ``AWS::VpcLattice::Listener.Name``.
        :param port: ``AWS::VpcLattice::Listener.Port``.
        :param service_identifier: ``AWS::VpcLattice::Listener.ServiceIdentifier``.
        :param tags: ``AWS::VpcLattice::Listener.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_listener_props = vpclattice.CfnListenerProps(
                default_action=vpclattice.CfnListener.DefaultActionProperty(
                    forward=vpclattice.CfnListener.ForwardProperty(
                        target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
            
                            # the properties below are optional
                            weight=123
                        )]
                    )
                ),
                protocol="protocol",
            
                # the properties below are optional
                name="name",
                port=123,
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753de3496ca524f6276658112b1710f0523b4bccf67e669ddf4d33d7859b5550)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "protocol": protocol,
        }
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_action(
        self,
    ) -> typing.Union[CfnListener.DefaultActionProperty, _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Listener.DefaultAction``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-defaultaction
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[CfnListener.DefaultActionProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''``AWS::VpcLattice::Listener.Protocol``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Listener.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''``AWS::VpcLattice::Listener.Port``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Listener.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::Listener.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourcePolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::VpcLattice::ResourcePolicy``.

    :cloudformationResource: AWS::VpcLattice::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        # policy: Any
        
        cfn_resource_policy = vpclattice.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy=policy,
            resource_arn="resourceArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy: typing.Any,
        resource_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: ``AWS::VpcLattice::ResourcePolicy.Policy``.
        :param resource_arn: ``AWS::VpcLattice::ResourcePolicy.ResourceArn``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ce89b3ef1aa5fbb08e8f9c4a9e1d596cc9b773f355ea0a2bfe9eba21b47a4ef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(policy=policy, resource_arn=resource_arn)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f893f163cb5e4b02423f38f38fd1cd1478732e32fe01e6965337cb0b01eb440f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abda21fae02d084e19222facf5cf893309a7bfaf031dcacead69e4375b9c1816)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''``AWS::VpcLattice::ResourcePolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2f4f4d6448a92cdb65f320f3c29f32e412ff77d6820a2f0644c5d0436f96ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''``AWS::VpcLattice::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91885fef6306744a0b8075b5430c824bb0563ed3d4021ce926df2401439595ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyProps:
    def __init__(self, *, policy: typing.Any, resource_arn: builtins.str) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy: ``AWS::VpcLattice::ResourcePolicy.Policy``.
        :param resource_arn: ``AWS::VpcLattice::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            # policy: Any
            
            cfn_resource_policy_props = vpclattice.CfnResourcePolicyProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c1b7d5cdc8b7f52784d878256f55937b88d12e555b4b18c4df94857f40c3ac)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def policy(self) -> typing.Any:
        '''``AWS::VpcLattice::ResourcePolicy.Policy``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''``AWS::VpcLattice::ResourcePolicy.ResourceArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnRule",
):
    '''A CloudFormation ``AWS::VpcLattice::Rule``.

    :cloudformationResource: AWS::VpcLattice::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_rule = vpclattice.CfnRule(self, "MyCfnRule",
            action=vpclattice.CfnRule.ActionProperty(
                forward=vpclattice.CfnRule.ForwardProperty(
                    target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
        
                        # the properties below are optional
                        weight=123
                    )]
                )
            ),
            match=vpclattice.CfnRule.MatchProperty(
                http_match=vpclattice.CfnRule.HttpMatchProperty(
                    header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                        match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name",
        
                        # the properties below are optional
                        case_sensitive=False
                    )],
                    method="method",
                    path_match=vpclattice.CfnRule.PathMatchProperty(
                        match=vpclattice.CfnRule.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        ),
        
                        # the properties below are optional
                        case_sensitive=False
                    )
                )
            ),
            priority=123,
        
            # the properties below are optional
            listener_identifier="listenerIdentifier",
            name="name",
            service_identifier="serviceIdentifier",
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
        action: typing.Union[typing.Union["CfnRule.ActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        match: typing.Union[typing.Union["CfnRule.MatchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        priority: jsii.Number,
        listener_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: ``AWS::VpcLattice::Rule.Action``.
        :param match: ``AWS::VpcLattice::Rule.Match``.
        :param priority: ``AWS::VpcLattice::Rule.Priority``.
        :param listener_identifier: ``AWS::VpcLattice::Rule.ListenerIdentifier``.
        :param name: ``AWS::VpcLattice::Rule.Name``.
        :param service_identifier: ``AWS::VpcLattice::Rule.ServiceIdentifier``.
        :param tags: ``AWS::VpcLattice::Rule.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8240a735fccff0620b38fc8ebdbc7b615bf7b319e2d9ae03f03ce22561a8b78f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            action=action,
            match=match,
            priority=priority,
            listener_identifier=listener_identifier,
            name=name,
            service_identifier=service_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4364971c8f3f34add9b2b66527abb15dfd2335ac18f19dea0fdf9a0c2fd2130)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc5d2b9b46112e95daee749154874669ceabad5cf28a137645124ba8bb836b60)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
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
        '''``AWS::VpcLattice::Rule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> typing.Union["CfnRule.ActionProperty", _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Rule.Action``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-action
        '''
        return typing.cast(typing.Union["CfnRule.ActionProperty", _IResolvable_a771d0ef], jsii.get(self, "action"))

    @action.setter
    def action(
        self,
        value: typing.Union["CfnRule.ActionProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43642ea6e9c01e23121f001f44c678a63c3f78b7743c6e1b35b6f0a5263bbe64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> typing.Union["CfnRule.MatchProperty", _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Rule.Match``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-match
        '''
        return typing.cast(typing.Union["CfnRule.MatchProperty", _IResolvable_a771d0ef], jsii.get(self, "match"))

    @match.setter
    def match(
        self,
        value: typing.Union["CfnRule.MatchProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3166d97e60639e21e94630fa3cc9f9fda195b09056ee2fc43932f1154e82bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''``AWS::VpcLattice::Rule.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-priority
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24476ac48ce7b629f842694fe54812be2280c58eb2ba9ec58298a4e5db3a045a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="listenerIdentifier")
    def listener_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.ListenerIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-listeneridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listenerIdentifier"))

    @listener_identifier.setter
    def listener_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361861a1ef123a92c505e4fe6bcfadf99c1ad710c455ccf1a26ee99461a0fe85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b666e2f4b92316c5cdb48369f995905eb4d118d42c8d214bcae872372300c3f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd9926e91251cb971e16b2e95052584d02106f69c20e1b8e6dd2dddededc163)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"forward": "forward"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            forward: typing.Union[typing.Union["CfnRule.ForwardProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param forward: ``CfnRule.ActionProperty.Forward``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                action_property = vpclattice.CfnRule.ActionProperty(
                    forward=vpclattice.CfnRule.ForwardProperty(
                        target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                
                            # the properties below are optional
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90934aa721146c72092663878ab7f5b9b2215b037e28e506cf0caf786a00aa34)
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "forward": forward,
            }

        @builtins.property
        def forward(
            self,
        ) -> typing.Union["CfnRule.ForwardProperty", _IResolvable_a771d0ef]:
            '''``CfnRule.ActionProperty.Forward``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html#cfn-vpclattice-rule-action-forward
            '''
            result = self._values.get("forward")
            assert result is not None, "Required property 'forward' is missing"
            return typing.cast(typing.Union["CfnRule.ForwardProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''
            :param target_groups: ``CfnRule.ForwardProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                forward_property = vpclattice.CfnRule.ForwardProperty(
                    target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                
                        # the properties below are optional
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46b8fb0c063ed901b59262efccab6c5cd9a778d0bc81fc0c523436d6a4648966)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_groups": target_groups,
            }

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.WeightedTargetGroupProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRule.ForwardProperty.TargetGroups``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html#cfn-vpclattice-rule-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            assert result is not None, "Required property 'target_groups' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.WeightedTargetGroupProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.HeaderMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "match": "match",
            "name": "name",
            "case_sensitive": "caseSensitive",
        },
    )
    class HeaderMatchProperty:
        def __init__(
            self,
            *,
            match: typing.Union[typing.Union["CfnRule.HeaderMatchTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            name: builtins.str,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param match: ``CfnRule.HeaderMatchProperty.Match``.
            :param name: ``CfnRule.HeaderMatchProperty.Name``.
            :param case_sensitive: ``CfnRule.HeaderMatchProperty.CaseSensitive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                header_match_property = vpclattice.CfnRule.HeaderMatchProperty(
                    match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                        contains="contains",
                        exact="exact",
                        prefix="prefix"
                    ),
                    name="name",
                
                    # the properties below are optional
                    case_sensitive=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbdd9049dc7ebd2af91548140bb5475636008747d12cfd5b911f41cb841e4d1e)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "match": match,
                "name": name,
            }
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def match(
            self,
        ) -> typing.Union["CfnRule.HeaderMatchTypeProperty", _IResolvable_a771d0ef]:
            '''``CfnRule.HeaderMatchProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union["CfnRule.HeaderMatchTypeProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''``CfnRule.HeaderMatchProperty.Name``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnRule.HeaderMatchProperty.CaseSensitive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.HeaderMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"contains": "contains", "exact": "exact", "prefix": "prefix"},
    )
    class HeaderMatchTypeProperty:
        def __init__(
            self,
            *,
            contains: typing.Optional[builtins.str] = None,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param contains: ``CfnRule.HeaderMatchTypeProperty.Contains``.
            :param exact: ``CfnRule.HeaderMatchTypeProperty.Exact``.
            :param prefix: ``CfnRule.HeaderMatchTypeProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                header_match_type_property = vpclattice.CfnRule.HeaderMatchTypeProperty(
                    contains="contains",
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc3f1fdbcb5c27e52a3f2368b5b1f43583fa38e937f56d6f47062e449ac7e0e3)
                check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contains is not None:
                self._values["contains"] = contains
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def contains(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.HeaderMatchTypeProperty.Contains``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-contains
            '''
            result = self._values.get("contains")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.HeaderMatchTypeProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.HeaderMatchTypeProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.HttpMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_matches": "headerMatches",
            "method": "method",
            "path_match": "pathMatch",
        },
    )
    class HttpMatchProperty:
        def __init__(
            self,
            *,
            header_matches: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRule.HeaderMatchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path_match: typing.Optional[typing.Union[typing.Union["CfnRule.PathMatchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param header_matches: ``CfnRule.HttpMatchProperty.HeaderMatches``.
            :param method: ``CfnRule.HttpMatchProperty.Method``.
            :param path_match: ``CfnRule.HttpMatchProperty.PathMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                http_match_property = vpclattice.CfnRule.HttpMatchProperty(
                    header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                        match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name",
                
                        # the properties below are optional
                        case_sensitive=False
                    )],
                    method="method",
                    path_match=vpclattice.CfnRule.PathMatchProperty(
                        match=vpclattice.CfnRule.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        ),
                
                        # the properties below are optional
                        case_sensitive=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7abd4b5c738e79e42f72bc89907970866f95c9d800d38dc6d7c2cc4bc940a3af)
                check_type(argname="argument header_matches", value=header_matches, expected_type=type_hints["header_matches"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path_match", value=path_match, expected_type=type_hints["path_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_matches is not None:
                self._values["header_matches"] = header_matches
            if method is not None:
                self._values["method"] = method
            if path_match is not None:
                self._values["path_match"] = path_match

        @builtins.property
        def header_matches(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.HeaderMatchProperty", _IResolvable_a771d0ef]]]]:
            '''``CfnRule.HttpMatchProperty.HeaderMatches``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-headermatches
            '''
            result = self._values.get("header_matches")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRule.HeaderMatchProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.HttpMatchProperty.Method``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path_match(
            self,
        ) -> typing.Optional[typing.Union["CfnRule.PathMatchProperty", _IResolvable_a771d0ef]]:
            '''``CfnRule.HttpMatchProperty.PathMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-pathmatch
            '''
            result = self._values.get("path_match")
            return typing.cast(typing.Optional[typing.Union["CfnRule.PathMatchProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.MatchProperty",
        jsii_struct_bases=[],
        name_mapping={"http_match": "httpMatch"},
    )
    class MatchProperty:
        def __init__(
            self,
            *,
            http_match: typing.Union[typing.Union["CfnRule.HttpMatchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''
            :param http_match: ``CfnRule.MatchProperty.HttpMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                match_property = vpclattice.CfnRule.MatchProperty(
                    http_match=vpclattice.CfnRule.HttpMatchProperty(
                        header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                            match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name",
                
                            # the properties below are optional
                            case_sensitive=False
                        )],
                        method="method",
                        path_match=vpclattice.CfnRule.PathMatchProperty(
                            match=vpclattice.CfnRule.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            ),
                
                            # the properties below are optional
                            case_sensitive=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__348a24f4538e62bc51bb7b0814f9e8c325ecd9e6650ac3055e4778e2b320f610)
                check_type(argname="argument http_match", value=http_match, expected_type=type_hints["http_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "http_match": http_match,
            }

        @builtins.property
        def http_match(
            self,
        ) -> typing.Union["CfnRule.HttpMatchProperty", _IResolvable_a771d0ef]:
            '''``CfnRule.MatchProperty.HttpMatch``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html#cfn-vpclattice-rule-match-httpmatch
            '''
            result = self._values.get("http_match")
            assert result is not None, "Required property 'http_match' is missing"
            return typing.cast(typing.Union["CfnRule.HttpMatchProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.PathMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match", "case_sensitive": "caseSensitive"},
    )
    class PathMatchProperty:
        def __init__(
            self,
            *,
            match: typing.Union[typing.Union["CfnRule.PathMatchTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param match: ``CfnRule.PathMatchProperty.Match``.
            :param case_sensitive: ``CfnRule.PathMatchProperty.CaseSensitive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                path_match_property = vpclattice.CfnRule.PathMatchProperty(
                    match=vpclattice.CfnRule.PathMatchTypeProperty(
                        exact="exact",
                        prefix="prefix"
                    ),
                
                    # the properties below are optional
                    case_sensitive=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11ef53120248a507c7416131012cabdb0b1c6de72f9af82664d200df298dbb60)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "match": match,
            }
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def match(
            self,
        ) -> typing.Union["CfnRule.PathMatchTypeProperty", _IResolvable_a771d0ef]:
            '''``CfnRule.PathMatchProperty.Match``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union["CfnRule.PathMatchTypeProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnRule.PathMatchProperty.CaseSensitive``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.PathMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "prefix": "prefix"},
    )
    class PathMatchTypeProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param exact: ``CfnRule.PathMatchTypeProperty.Exact``.
            :param prefix: ``CfnRule.PathMatchTypeProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                path_match_type_property = vpclattice.CfnRule.PathMatchTypeProperty(
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f89caf9885c1dbeee065db52aeba75b5f168b78740f9e09d4a4f985af59aa111)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.PathMatchTypeProperty.Exact``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''``CfnRule.PathMatchTypeProperty.Prefix``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnRule.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: builtins.str,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param target_group_identifier: ``CfnRule.WeightedTargetGroupProperty.TargetGroupIdentifier``.
            :param weight: ``CfnRule.WeightedTargetGroupProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                weighted_target_group_property = vpclattice.CfnRule.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                
                    # the properties below are optional
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d265463585d6b065a1de455451f7b7bb2ba049f34f05a31c82350d9f4d9cbaa)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_group_identifier": target_group_identifier,
            }
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> builtins.str:
            '''``CfnRule.WeightedTargetGroupProperty.TargetGroupIdentifier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            assert result is not None, "Required property 'target_group_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''``CfnRule.WeightedTargetGroupProperty.Weight``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "priority": "priority",
        "listener_identifier": "listenerIdentifier",
        "name": "name",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        action: typing.Union[typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        match: typing.Union[typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        priority: jsii.Number,
        listener_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param action: ``AWS::VpcLattice::Rule.Action``.
        :param match: ``AWS::VpcLattice::Rule.Match``.
        :param priority: ``AWS::VpcLattice::Rule.Priority``.
        :param listener_identifier: ``AWS::VpcLattice::Rule.ListenerIdentifier``.
        :param name: ``AWS::VpcLattice::Rule.Name``.
        :param service_identifier: ``AWS::VpcLattice::Rule.ServiceIdentifier``.
        :param tags: ``AWS::VpcLattice::Rule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_rule_props = vpclattice.CfnRuleProps(
                action=vpclattice.CfnRule.ActionProperty(
                    forward=vpclattice.CfnRule.ForwardProperty(
                        target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
            
                            # the properties below are optional
                            weight=123
                        )]
                    )
                ),
                match=vpclattice.CfnRule.MatchProperty(
                    http_match=vpclattice.CfnRule.HttpMatchProperty(
                        header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                            match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name",
            
                            # the properties below are optional
                            case_sensitive=False
                        )],
                        method="method",
                        path_match=vpclattice.CfnRule.PathMatchProperty(
                            match=vpclattice.CfnRule.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            ),
            
                            # the properties below are optional
                            case_sensitive=False
                        )
                    )
                ),
                priority=123,
            
                # the properties below are optional
                listener_identifier="listenerIdentifier",
                name="name",
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3073ffc8a7f7dd9923bcfe2007af749e7d2c1665348effe3cc6d090d76228968)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument listener_identifier", value=listener_identifier, expected_type=type_hints["listener_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
            "priority": priority,
        }
        if listener_identifier is not None:
            self._values["listener_identifier"] = listener_identifier
        if name is not None:
            self._values["name"] = name
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(self) -> typing.Union[CfnRule.ActionProperty, _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Rule.Action``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[CfnRule.ActionProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def match(self) -> typing.Union[CfnRule.MatchProperty, _IResolvable_a771d0ef]:
        '''``AWS::VpcLattice::Rule.Match``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-match
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(typing.Union[CfnRule.MatchProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''``AWS::VpcLattice::Rule.Priority``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def listener_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.ListenerIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-listeneridentifier
        '''
        result = self._values.get("listener_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Rule.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::Rule.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnService(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnService",
):
    '''A CloudFormation ``AWS::VpcLattice::Service``.

    :cloudformationResource: AWS::VpcLattice::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_service = vpclattice.CfnService(self, "MyCfnService",
            auth_type="authType",
            certificate_arn="certificateArn",
            custom_domain_name="customDomainName",
            dns_entry=vpclattice.CfnService.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
            ),
            name="name",
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
        auth_type: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        dns_entry: typing.Optional[typing.Union[typing.Union["CfnService.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: ``AWS::VpcLattice::Service.AuthType``.
        :param certificate_arn: ``AWS::VpcLattice::Service.CertificateArn``.
        :param custom_domain_name: ``AWS::VpcLattice::Service.CustomDomainName``.
        :param dns_entry: ``AWS::VpcLattice::Service.DnsEntry``.
        :param name: ``AWS::VpcLattice::Service.Name``.
        :param tags: ``AWS::VpcLattice::Service.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fcbfe9a57cb7fbb69daab37f506e8a9268653e9a4112fe6ecf9c6e35f519465)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            auth_type=auth_type,
            certificate_arn=certificate_arn,
            custom_domain_name=custom_domain_name,
            dns_entry=dns_entry,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9597e4482a993c7336064a297ca42923344765ef98c10594a71ec1ffa7b704ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b127fe09b6c0f2be9afc632d66d84bab382d26f5e45e13268e22bffa9e3b1186)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryDomainName")
    def attr_dns_entry_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsEntry.DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryHostedZoneId")
    def attr_dns_entry_hosted_zone_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsEntry.HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::Service.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.AuthType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-authtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecfc61495a1a68609d5d2f22c8e4f173678de06dafac2780678612f1dac54dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.CertificateArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-certificatearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28cd1cfc49b06cd85163d0f86c1a20143f549a076fe17f503c74d35c4b1054bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="customDomainName")
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.CustomDomainName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-customdomainname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainName"))

    @custom_domain_name.setter
    def custom_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0417acf01d508244fb3d96f756159dff0d7d131bdec77a125cb82178ab02a9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="dnsEntry")
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union["CfnService.DnsEntryProperty", _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::Service.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-dnsentry
        '''
        return typing.cast(typing.Optional[typing.Union["CfnService.DnsEntryProperty", _IResolvable_a771d0ef]], jsii.get(self, "dnsEntry"))

    @dns_entry.setter
    def dns_entry(
        self,
        value: typing.Optional[typing.Union["CfnService.DnsEntryProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88cfa202905521feb3fb8c2bbfc50027eda2db166d2d2ade4973dd30b8b65d46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEntry", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb93d156711b0d632638472287e087a8e7b050391fd7436e62c8033564a4015)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnService.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param domain_name: ``CfnService.DnsEntryProperty.DomainName``.
            :param hosted_zone_id: ``CfnService.DnsEntryProperty.HostedZoneId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                dns_entry_property = vpclattice.CfnService.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d16a5fd039b3f3ee47579ba39d262dad79cac59db488fa6abb602f57d587a6c)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnService.DnsEntryProperty.DomainName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnService.DnsEntryProperty.HostedZoneId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceNetwork(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetwork",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetwork``.

    :cloudformationResource: AWS::VpcLattice::ServiceNetwork
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_service_network = vpclattice.CfnServiceNetwork(self, "MyCfnServiceNetwork",
            auth_type="authType",
            name="name",
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
        auth_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: ``AWS::VpcLattice::ServiceNetwork.AuthType``.
        :param name: ``AWS::VpcLattice::ServiceNetwork.Name``.
        :param tags: ``AWS::VpcLattice::ServiceNetwork.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a18fbf5ff3afc8b2abed1a9ff6c12b40a8584858569b35f1ce9719fcfc4cf0cc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkProps(auth_type=auth_type, name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ddbb440dae09ad8371697981fa5b463424142f967a8fb44736bf07f20589a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dc59b10470e77e88f0df66ea7d360e2d3074b1d59fc652bd6a8ddbb5f20a1c0)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::ServiceNetwork.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetwork.AuthType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-authtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a16283be238959ca373c50bf9651fd5680d93907a26be93f39c688fd1fc76033)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetwork.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd512d52eab6ec539476c5e0dae4c8acebe2991da62b3e92f110c15f7ee26d18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType", "name": "name", "tags": "tags"},
)
class CfnServiceNetworkProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetwork``.

        :param auth_type: ``AWS::VpcLattice::ServiceNetwork.AuthType``.
        :param name: ``AWS::VpcLattice::ServiceNetwork.Name``.
        :param tags: ``AWS::VpcLattice::ServiceNetwork.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_service_network_props = vpclattice.CfnServiceNetworkProps(
                auth_type="authType",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71820a4d50bc92645bc6be5695e652be45690861e3e1f992930474ade6170a46)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetwork.AuthType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetwork.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::ServiceNetwork.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceNetworkServiceAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkServiceAssociation",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetworkServiceAssociation``.

    :cloudformationResource: AWS::VpcLattice::ServiceNetworkServiceAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_service_network_service_association = vpclattice.CfnServiceNetworkServiceAssociation(self, "MyCfnServiceNetworkServiceAssociation",
            dns_entry=vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
            ),
            service_identifier="serviceIdentifier",
            service_network_identifier="serviceNetworkIdentifier",
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
        dns_entry: typing.Optional[typing.Union[typing.Union["CfnServiceNetworkServiceAssociation.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetworkServiceAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dns_entry: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.
        :param service_identifier: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceIdentifier``.
        :param service_network_identifier: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceNetworkIdentifier``.
        :param tags: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.Tags``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ceb02176d7edd764a98a047dba66216ea070b9a71640194dfe6370708f1df5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkServiceAssociationProps(
            dns_entry=dns_entry,
            service_identifier=service_identifier,
            service_network_identifier=service_network_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97bf8bb8a029a01904d62730227c86c7ffabc2ecd238600ae422e7d06c0f386)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a9eb6338c88b599d3524ed85f74defb93b55a4995be953ac58929d821850ae)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryDomainName")
    def attr_dns_entry_domain_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsEntry.DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryHostedZoneId")
    def attr_dns_entry_hosted_zone_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: DnsEntry.HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceId")
    def attr_service_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceName")
    def attr_service_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceName"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkArn")
    def attr_service_network_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkId")
    def attr_service_network_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkName")
    def attr_service_network_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dnsEntry")
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union["CfnServiceNetworkServiceAssociation.DnsEntryProperty", _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry
        '''
        return typing.cast(typing.Optional[typing.Union["CfnServiceNetworkServiceAssociation.DnsEntryProperty", _IResolvable_a771d0ef]], jsii.get(self, "dnsEntry"))

    @dns_entry.setter
    def dns_entry(
        self,
        value: typing.Optional[typing.Union["CfnServiceNetworkServiceAssociation.DnsEntryProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ace60e310fbac0bfb45fbde1ff30ac1c619be1bf0947a77a3024ccba61c9b16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEntry", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52c463aec548dbce191036be94223c02eaf27834b7584060ab188d1ef983efd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceNetworkIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-servicenetworkidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkIdentifier"))

    @service_network_identifier.setter
    def service_network_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f825206eb119213e21a2bda6d5682c65d6cb08ce025dec51a3bbc126c4deddb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNetworkIdentifier", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param domain_name: ``CfnServiceNetworkServiceAssociation.DnsEntryProperty.DomainName``.
            :param hosted_zone_id: ``CfnServiceNetworkServiceAssociation.DnsEntryProperty.HostedZoneId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                dns_entry_property = vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4be12217428cf0352571601ea113e394b7e94c437734aa78e0ec1d085ab09974)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''``CfnServiceNetworkServiceAssociation.DnsEntryProperty.DomainName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''``CfnServiceNetworkServiceAssociation.DnsEntryProperty.HostedZoneId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkServiceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_entry": "dnsEntry",
        "service_identifier": "serviceIdentifier",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
    },
)
class CfnServiceNetworkServiceAssociationProps:
    def __init__(
        self,
        *,
        dns_entry: typing.Optional[typing.Union[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetworkServiceAssociation``.

        :param dns_entry: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.
        :param service_identifier: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceIdentifier``.
        :param service_network_identifier: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceNetworkIdentifier``.
        :param tags: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_service_network_service_association_props = vpclattice.CfnServiceNetworkServiceAssociationProps(
                dns_entry=vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                service_identifier="serviceIdentifier",
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195672ca6c5a3d1311c7df0aa9158bc14d6c794fc4784644e8e7ac8a0878b9fd)
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.ServiceNetworkIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkServiceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceNetworkVpcAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkVpcAssociation",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetworkVpcAssociation``.

    :cloudformationResource: AWS::VpcLattice::ServiceNetworkVpcAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_service_network_vpc_association = vpclattice.CfnServiceNetworkVpcAssociation(self, "MyCfnServiceNetworkVpcAssociation",
            security_group_ids=["securityGroupIds"],
            service_network_identifier="serviceNetworkIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_identifier="vpcIdentifier"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetworkVpcAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param security_group_ids: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.SecurityGroupIds``.
        :param service_network_identifier: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.ServiceNetworkIdentifier``.
        :param tags: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.Tags``.
        :param vpc_identifier: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.VpcIdentifier``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bde7832dca0a870017d0a0356f5b4bc1f210467b7d8d9b65b3b5b7f5276f0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkVpcAssociationProps(
            security_group_ids=security_group_ids,
            service_network_identifier=service_network_identifier,
            tags=tags,
            vpc_identifier=vpc_identifier,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc25495f54b893b03021a7e5b6fd8fd660c93f88cc24ce10d8cac6093a597af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c0e56119ce247a39f25d8d5708c2651f22abffffd4838654e7730e6ed314c4f)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkArn")
    def attr_service_network_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkId")
    def attr_service_network_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkName")
    def attr_service_network_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: ServiceNetworkName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcId")
    def attr_vpc_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VpcId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.SecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c3e6da3d29a532566c4ffc9b79c44ccbb3219c9177bc56f98573fa0601c9926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.ServiceNetworkIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-servicenetworkidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkIdentifier"))

    @service_network_identifier.setter
    def service_network_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dac839902a82bb3249d5f914796f31854a699e9d66d4cd8e02c1bd2933993d3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNetworkIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="vpcIdentifier")
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.VpcIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-vpcidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdentifier"))

    @vpc_identifier.setter
    def vpc_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4267f6a81a7401eae8224cb588cbffe02d42753ff0ea473056b355a21fb1d329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcIdentifier", value)


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnServiceNetworkVpcAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
        "vpc_identifier": "vpcIdentifier",
    },
)
class CfnServiceNetworkVpcAssociationProps:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetworkVpcAssociation``.

        :param security_group_ids: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.SecurityGroupIds``.
        :param service_network_identifier: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.ServiceNetworkIdentifier``.
        :param tags: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.Tags``.
        :param vpc_identifier: ``AWS::VpcLattice::ServiceNetworkVpcAssociation.VpcIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_service_network_vpc_association_props = vpclattice.CfnServiceNetworkVpcAssociationProps(
                security_group_ids=["securityGroupIds"],
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_identifier="vpcIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecefdc024efce90061ee7f6e2b40bb0e7e66392dbee262219c69367899d09824)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_identifier is not None:
            self._values["vpc_identifier"] = vpc_identifier

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.SecurityGroupIds``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.ServiceNetworkIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::ServiceNetworkVpcAssociation.VpcIdentifier``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-vpcidentifier
        '''
        result = self._values.get("vpc_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkVpcAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "certificate_arn": "certificateArn",
        "custom_domain_name": "customDomainName",
        "dns_entry": "dnsEntry",
        "name": "name",
        "tags": "tags",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        dns_entry: typing.Optional[typing.Union[typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param auth_type: ``AWS::VpcLattice::Service.AuthType``.
        :param certificate_arn: ``AWS::VpcLattice::Service.CertificateArn``.
        :param custom_domain_name: ``AWS::VpcLattice::Service.CustomDomainName``.
        :param dns_entry: ``AWS::VpcLattice::Service.DnsEntry``.
        :param name: ``AWS::VpcLattice::Service.Name``.
        :param tags: ``AWS::VpcLattice::Service.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_service_props = vpclattice.CfnServiceProps(
                auth_type="authType",
                certificate_arn="certificateArn",
                custom_domain_name="customDomainName",
                dns_entry=vpclattice.CfnService.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83955652e8f60816a8dfc860d362d24cd9074558e5203ce65e93dacbdedbb79b)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.AuthType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.CertificateArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.CustomDomainName``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-customdomainname
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[CfnService.DnsEntryProperty, _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::Service.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[CfnService.DnsEntryProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::Service.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::Service.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnTargetGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_vpclattice.CfnTargetGroup",
):
    '''A CloudFormation ``AWS::VpcLattice::TargetGroup``.

    :cloudformationResource: AWS::VpcLattice::TargetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_vpclattice as vpclattice
        
        cfn_target_group = vpclattice.CfnTargetGroup(self, "MyCfnTargetGroup",
            type="type",
        
            # the properties below are optional
            config=vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                port=123,
                protocol="protocol",
                vpc_identifier="vpcIdentifier",
        
                # the properties below are optional
                health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    unhealthy_threshold_count=123
                ),
                protocol_version="protocolVersion"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            targets=[vpclattice.CfnTargetGroup.TargetProperty(
                id="id",
        
                # the properties below are optional
                port=123
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        type: builtins.str,
        config: typing.Optional[typing.Union[typing.Union["CfnTargetGroup.TargetGroupConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnTargetGroup.TargetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::TargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: ``AWS::VpcLattice::TargetGroup.Type``.
        :param config: ``AWS::VpcLattice::TargetGroup.Config``.
        :param name: ``AWS::VpcLattice::TargetGroup.Name``.
        :param tags: ``AWS::VpcLattice::TargetGroup.Tags``.
        :param targets: ``AWS::VpcLattice::TargetGroup.Targets``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831966a8f55d0144a4358728a952d06cf95b5399e516ee872c302d8698d69c53)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTargetGroupProps(
            type=type, config=config, name=name, tags=tags, targets=targets
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__655795269ce7e147137744f2ba1e083e7eedba22de79237575ee8b005cf1a82a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7eaf62da566be90a00e237dd4d46a0fb26aadc72a2586fdb4d8873781b893503)
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
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''
        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::VpcLattice::TargetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''``AWS::VpcLattice::TargetGroup.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee59f0de8e5f69faf86583d91674fc59f83c2a6365a55c7a721c0ed84f200a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Optional[typing.Union["CfnTargetGroup.TargetGroupConfigProperty", _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::TargetGroup.Config``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-config
        '''
        return typing.cast(typing.Optional[typing.Union["CfnTargetGroup.TargetGroupConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Optional[typing.Union["CfnTargetGroup.TargetGroupConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e1bb18f327eb29dcafe2aa90eab61a7b68351195c67c29916c38a6151fbe5e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::TargetGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7a8a49e7cd68e1297d8d98437b4a10873219a363d11a17693f7feaf2575ea6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTargetGroup.TargetProperty", _IResolvable_a771d0ef]]]]:
        '''``AWS::VpcLattice::TargetGroup.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-targets
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTargetGroup.TargetProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnTargetGroup.TargetProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2374214bf7e9a7565156cdfc96bb38aa15e6f611bc54c6a7d7b1051c29df5834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnTargetGroup.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "health_check_interval_seconds": "healthCheckIntervalSeconds",
            "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
            "healthy_threshold_count": "healthyThresholdCount",
            "matcher": "matcher",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "unhealthy_threshold_count": "unhealthyThresholdCount",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            health_check_interval_seconds: typing.Optional[jsii.Number] = None,
            health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
            healthy_threshold_count: typing.Optional[jsii.Number] = None,
            matcher: typing.Optional[typing.Union[typing.Union["CfnTargetGroup.MatcherProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param enabled: ``CfnTargetGroup.HealthCheckConfigProperty.Enabled``.
            :param health_check_interval_seconds: ``CfnTargetGroup.HealthCheckConfigProperty.HealthCheckIntervalSeconds``.
            :param health_check_timeout_seconds: ``CfnTargetGroup.HealthCheckConfigProperty.HealthCheckTimeoutSeconds``.
            :param healthy_threshold_count: ``CfnTargetGroup.HealthCheckConfigProperty.HealthyThresholdCount``.
            :param matcher: ``CfnTargetGroup.HealthCheckConfigProperty.Matcher``.
            :param path: ``CfnTargetGroup.HealthCheckConfigProperty.Path``.
            :param port: ``CfnTargetGroup.HealthCheckConfigProperty.Port``.
            :param protocol: ``CfnTargetGroup.HealthCheckConfigProperty.Protocol``.
            :param unhealthy_threshold_count: ``CfnTargetGroup.HealthCheckConfigProperty.UnhealthyThresholdCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                health_check_config_property = vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    unhealthy_threshold_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6013b6d96d1ec944dde0718d402a1bf9e7f793b85d5e51b92f7276d9d5a25773)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
                check_type(argname="argument health_check_timeout_seconds", value=health_check_timeout_seconds, expected_type=type_hints["health_check_timeout_seconds"])
                check_type(argname="argument healthy_threshold_count", value=healthy_threshold_count, expected_type=type_hints["healthy_threshold_count"])
                check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument unhealthy_threshold_count", value=unhealthy_threshold_count, expected_type=type_hints["unhealthy_threshold_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if health_check_interval_seconds is not None:
                self._values["health_check_interval_seconds"] = health_check_interval_seconds
            if health_check_timeout_seconds is not None:
                self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
            if healthy_threshold_count is not None:
                self._values["healthy_threshold_count"] = healthy_threshold_count
            if matcher is not None:
                self._values["matcher"] = matcher
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if unhealthy_threshold_count is not None:
                self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.Enabled``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.HealthCheckIntervalSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthcheckintervalseconds
            '''
            result = self._values.get("health_check_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.HealthCheckTimeoutSeconds``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthchecktimeoutseconds
            '''
            result = self._values.get("health_check_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.HealthyThresholdCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthythresholdcount
            '''
            result = self._values.get("healthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def matcher(
            self,
        ) -> typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_a771d0ef]]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.Matcher``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-matcher
            '''
            result = self._values.get("matcher")
            return typing.cast(typing.Optional[typing.Union["CfnTargetGroup.MatcherProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.HealthCheckConfigProperty.UnhealthyThresholdCount``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-unhealthythresholdcount
            '''
            result = self._values.get("unhealthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnTargetGroup.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(self, *, http_code: builtins.str) -> None:
            '''
            :param http_code: ``CfnTargetGroup.MatcherProperty.HttpCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                matcher_property = vpclattice.CfnTargetGroup.MatcherProperty(
                    http_code="httpCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__284ae2bcc13971b5919ae3941428b3f2a1fd4e96d88bbe7701002c71654975f6)
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "http_code": http_code,
            }

        @builtins.property
        def http_code(self) -> builtins.str:
            '''``CfnTargetGroup.MatcherProperty.HttpCode``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html#cfn-vpclattice-targetgroup-matcher-httpcode
            '''
            result = self._values.get("http_code")
            assert result is not None, "Required property 'http_code' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatcherProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnTargetGroup.TargetGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "protocol": "protocol",
            "vpc_identifier": "vpcIdentifier",
            "health_check": "healthCheck",
            "protocol_version": "protocolVersion",
        },
    )
    class TargetGroupConfigProperty:
        def __init__(
            self,
            *,
            port: jsii.Number,
            protocol: builtins.str,
            vpc_identifier: builtins.str,
            health_check: typing.Optional[typing.Union[typing.Union["CfnTargetGroup.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            protocol_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param port: ``CfnTargetGroup.TargetGroupConfigProperty.Port``.
            :param protocol: ``CfnTargetGroup.TargetGroupConfigProperty.Protocol``.
            :param vpc_identifier: ``CfnTargetGroup.TargetGroupConfigProperty.VpcIdentifier``.
            :param health_check: ``CfnTargetGroup.TargetGroupConfigProperty.HealthCheck``.
            :param protocol_version: ``CfnTargetGroup.TargetGroupConfigProperty.ProtocolVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                target_group_config_property = vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                    port=123,
                    protocol="protocol",
                    vpc_identifier="vpcIdentifier",
                
                    # the properties below are optional
                    health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        unhealthy_threshold_count=123
                    ),
                    protocol_version="protocolVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__980cd558564c88e8d9bf8084b1b7d33d6b49b0488f6f513a0d8a24d59c9859a1)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "port": port,
                "protocol": protocol,
                "vpc_identifier": vpc_identifier,
            }
            if health_check is not None:
                self._values["health_check"] = health_check
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version

        @builtins.property
        def port(self) -> jsii.Number:
            '''``CfnTargetGroup.TargetGroupConfigProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''``CfnTargetGroup.TargetGroupConfigProperty.Protocol``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc_identifier(self) -> builtins.str:
            '''``CfnTargetGroup.TargetGroupConfigProperty.VpcIdentifier``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-vpcidentifier
            '''
            result = self._values.get("vpc_identifier")
            assert result is not None, "Required property 'vpc_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union["CfnTargetGroup.HealthCheckConfigProperty", _IResolvable_a771d0ef]]:
            '''``CfnTargetGroup.TargetGroupConfigProperty.HealthCheck``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union["CfnTargetGroup.HealthCheckConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''``CfnTargetGroup.TargetGroupConfigProperty.ProtocolVersion``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_vpclattice.CfnTargetGroup.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "port": "port"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param id: ``CfnTargetGroup.TargetProperty.Id``.
            :param port: ``CfnTargetGroup.TargetProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_vpclattice as vpclattice
                
                target_property = vpclattice.CfnTargetGroup.TargetProperty(
                    id="id",
                
                    # the properties below are optional
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57e7f89194dd9c1b857ab2bed6b8f3a6c3a562ad1a9002fa439ffa8dbe1ee1f5)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def id(self) -> builtins.str:
            '''``CfnTargetGroup.TargetProperty.Id``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''``CfnTargetGroup.TargetProperty.Port``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_vpclattice.CfnTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "config": "config",
        "name": "name",
        "tags": "tags",
        "targets": "targets",
    },
)
class CfnTargetGroupProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        config: typing.Optional[typing.Union[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTargetGroup``.

        :param type: ``AWS::VpcLattice::TargetGroup.Type``.
        :param config: ``AWS::VpcLattice::TargetGroup.Config``.
        :param name: ``AWS::VpcLattice::TargetGroup.Name``.
        :param tags: ``AWS::VpcLattice::TargetGroup.Tags``.
        :param targets: ``AWS::VpcLattice::TargetGroup.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_vpclattice as vpclattice
            
            cfn_target_group_props = vpclattice.CfnTargetGroupProps(
                type="type",
            
                # the properties below are optional
                config=vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                    port=123,
                    protocol="protocol",
                    vpc_identifier="vpcIdentifier",
            
                    # the properties below are optional
                    health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        unhealthy_threshold_count=123
                    ),
                    protocol_version="protocolVersion"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                targets=[vpclattice.CfnTargetGroup.TargetProperty(
                    id="id",
            
                    # the properties below are optional
                    port=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072993e9cc2983f81da64b85cae6e0152e3064869bf26f3a1a0008495fe35317)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if config is not None:
            self._values["config"] = config
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def type(self) -> builtins.str:
        '''``AWS::VpcLattice::TargetGroup.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, _IResolvable_a771d0ef]]:
        '''``AWS::VpcLattice::TargetGroup.Config``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''``AWS::VpcLattice::TargetGroup.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::VpcLattice::TargetGroup.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTargetGroup.TargetProperty, _IResolvable_a771d0ef]]]]:
        '''``AWS::VpcLattice::TargetGroup.Targets``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTargetGroup.TargetProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessLogSubscription",
    "CfnAccessLogSubscriptionProps",
    "CfnAuthPolicy",
    "CfnAuthPolicyProps",
    "CfnListener",
    "CfnListenerProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnService",
    "CfnServiceNetwork",
    "CfnServiceNetworkProps",
    "CfnServiceNetworkServiceAssociation",
    "CfnServiceNetworkServiceAssociationProps",
    "CfnServiceNetworkVpcAssociation",
    "CfnServiceNetworkVpcAssociationProps",
    "CfnServiceProps",
    "CfnTargetGroup",
    "CfnTargetGroupProps",
]

publication.publish()

def _typecheckingstub__2554a5601956dd41564578a3b8a446d5383ffe0ad4f07b56d0527b43b3972aad(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_arn: builtins.str,
    resource_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6d6ba72b861a52dd99be6234aaa874f7cd84cfb8d7e78e58b9aad7d7c5063c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b646175739ec0dbf2ea344e518f9307479d050e3927fc8516554310d6b5402(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2e08d2dec7e7f7e53aa09ffc506ca3df40a3ff9f7a466ca16b745c18a4bfc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5d18217d19eedd701793852cf6eb730ba0c89c8d9e1de1a23e8e538674dd8f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7081ac6eeae148c3cfe9e0eda14f91a76e586e86c63a0aee58fd7e311798e0a(
    *,
    destination_arn: builtins.str,
    resource_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb07d80bcb2006dcce0a495882667cff6639e05f6d436c406a31f89bd541ed92(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy: typing.Any,
    resource_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b3145968a18d173c12730fb8d3c1811676f0ade5d11793bc7f0e5dd1e501e5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d841630368f87db25dd04aa10f18571cd808a6aeddf35cf6144a2682fd4e5ae(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e7577cf43460ca5058735b3a896fa64eba1fb0d2c1dbe0d86c5803199b3ee72(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8831fdd266e45ece0d675a2d8a4887e935cfc21da31aa85ceb0a24306a8c2c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb83fd0815d0bf2d1ff7452cc8a482ce5f2275b83bad256969f2f337b285800(
    *,
    policy: typing.Any,
    resource_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e57a2f8baf2dc402cfc5f688e6924c41f139df5febcd34ee1930966f7d5d4f0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    default_action: typing.Union[typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    protocol: builtins.str,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbf3a5218b7e4dacd8e75e9394a7552e6b187f38d32b2f5d551236e6989ff1b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52239813405069c083582b66c87a4c1d5303aaa7f8999025384fff2a6ee602b9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6fb621c98dd7bec66a46cdf17faef2b11ac731510ec3ba157dd78bdfa92e11d(
    value: typing.Union[CfnListener.DefaultActionProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2afec20cc8c3409afbfb1fd7540444751897cfc3bf8f7c3fbc64e8c6b1f441(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f45d51511465e0932e0908c9ceadbfcffcb935f33d005cb1dbedb35d1403483(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e54de6a5e277c1324dd2aaf09b8f3b5f52006a3c686503a8b8696c65ee51419(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41cdaa2e7a75522b5c699d72dc9a266e6e62e254db38ded8f7f6e2dda669733b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0252509a3c889dc05db1aef9ed4389592ed4f590fc11d15a5650f9d29fb825c4(
    *,
    forward: typing.Union[typing.Union[CfnListener.ForwardProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c561c073b6867961d18d77790bb70f811011df3eb483c8759abd5a4694544fb(
    *,
    target_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnListener.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdb89a0279d863b1be6b0d89dd10798c4ed609509c5853df65339315a501680(
    *,
    target_group_identifier: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753de3496ca524f6276658112b1710f0523b4bccf67e669ddf4d33d7859b5550(
    *,
    default_action: typing.Union[typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    protocol: builtins.str,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ce89b3ef1aa5fbb08e8f9c4a9e1d596cc9b773f355ea0a2bfe9eba21b47a4ef(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f893f163cb5e4b02423f38f38fd1cd1478732e32fe01e6965337cb0b01eb440f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abda21fae02d084e19222facf5cf893309a7bfaf031dcacead69e4375b9c1816(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2f4f4d6448a92cdb65f320f3c29f32e412ff77d6820a2f0644c5d0436f96ed(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91885fef6306744a0b8075b5430c824bb0563ed3d4021ce926df2401439595ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c1b7d5cdc8b7f52784d878256f55937b88d12e555b4b18c4df94857f40c3ac(
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8240a735fccff0620b38fc8ebdbc7b615bf7b319e2d9ae03f03ce22561a8b78f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    action: typing.Union[typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    match: typing.Union[typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    priority: jsii.Number,
    listener_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4364971c8f3f34add9b2b66527abb15dfd2335ac18f19dea0fdf9a0c2fd2130(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5d2b9b46112e95daee749154874669ceabad5cf28a137645124ba8bb836b60(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43642ea6e9c01e23121f001f44c678a63c3f78b7743c6e1b35b6f0a5263bbe64(
    value: typing.Union[CfnRule.ActionProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3166d97e60639e21e94630fa3cc9f9fda195b09056ee2fc43932f1154e82bf4(
    value: typing.Union[CfnRule.MatchProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24476ac48ce7b629f842694fe54812be2280c58eb2ba9ec58298a4e5db3a045a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361861a1ef123a92c505e4fe6bcfadf99c1ad710c455ccf1a26ee99461a0fe85(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b666e2f4b92316c5cdb48369f995905eb4d118d42c8d214bcae872372300c3f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd9926e91251cb971e16b2e95052584d02106f69c20e1b8e6dd2dddededc163(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90934aa721146c72092663878ab7f5b9b2215b037e28e506cf0caf786a00aa34(
    *,
    forward: typing.Union[typing.Union[CfnRule.ForwardProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b8fb0c063ed901b59262efccab6c5cd9a778d0bc81fc0c523436d6a4648966(
    *,
    target_groups: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdd9049dc7ebd2af91548140bb5475636008747d12cfd5b911f41cb841e4d1e(
    *,
    match: typing.Union[typing.Union[CfnRule.HeaderMatchTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: builtins.str,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3f1fdbcb5c27e52a3f2368b5b1f43583fa38e937f56d6f47062e449ac7e0e3(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd4b5c738e79e42f72bc89907970866f95c9d800d38dc6d7c2cc4bc940a3af(
    *,
    header_matches: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRule.HeaderMatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path_match: typing.Optional[typing.Union[typing.Union[CfnRule.PathMatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348a24f4538e62bc51bb7b0814f9e8c325ecd9e6650ac3055e4778e2b320f610(
    *,
    http_match: typing.Union[typing.Union[CfnRule.HttpMatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ef53120248a507c7416131012cabdb0b1c6de72f9af82664d200df298dbb60(
    *,
    match: typing.Union[typing.Union[CfnRule.PathMatchTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89caf9885c1dbeee065db52aeba75b5f168b78740f9e09d4a4f985af59aa111(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d265463585d6b065a1de455451f7b7bb2ba049f34f05a31c82350d9f4d9cbaa(
    *,
    target_group_identifier: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3073ffc8a7f7dd9923bcfe2007af749e7d2c1665348effe3cc6d090d76228968(
    *,
    action: typing.Union[typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    match: typing.Union[typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    priority: jsii.Number,
    listener_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fcbfe9a57cb7fbb69daab37f506e8a9268653e9a4112fe6ecf9c6e35f519465(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    dns_entry: typing.Optional[typing.Union[typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9597e4482a993c7336064a297ca42923344765ef98c10594a71ec1ffa7b704ff(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b127fe09b6c0f2be9afc632d66d84bab382d26f5e45e13268e22bffa9e3b1186(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecfc61495a1a68609d5d2f22c8e4f173678de06dafac2780678612f1dac54dfb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cd1cfc49b06cd85163d0f86c1a20143f549a076fe17f503c74d35c4b1054bc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0417acf01d508244fb3d96f756159dff0d7d131bdec77a125cb82178ab02a9e5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88cfa202905521feb3fb8c2bbfc50027eda2db166d2d2ade4973dd30b8b65d46(
    value: typing.Optional[typing.Union[CfnService.DnsEntryProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb93d156711b0d632638472287e087a8e7b050391fd7436e62c8033564a4015(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d16a5fd039b3f3ee47579ba39d262dad79cac59db488fa6abb602f57d587a6c(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a18fbf5ff3afc8b2abed1a9ff6c12b40a8584858569b35f1ce9719fcfc4cf0cc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    auth_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ddbb440dae09ad8371697981fa5b463424142f967a8fb44736bf07f20589a0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc59b10470e77e88f0df66ea7d360e2d3074b1d59fc652bd6a8ddbb5f20a1c0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16283be238959ca373c50bf9651fd5680d93907a26be93f39c688fd1fc76033(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd512d52eab6ec539476c5e0dae4c8acebe2991da62b3e92f110c15f7ee26d18(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71820a4d50bc92645bc6be5695e652be45690861e3e1f992930474ade6170a46(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ceb02176d7edd764a98a047dba66216ea070b9a71640194dfe6370708f1df5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    dns_entry: typing.Optional[typing.Union[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97bf8bb8a029a01904d62730227c86c7ffabc2ecd238600ae422e7d06c0f386(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a9eb6338c88b599d3524ed85f74defb93b55a4995be953ac58929d821850ae(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ace60e310fbac0bfb45fbde1ff30ac1c619be1bf0947a77a3024ccba61c9b16(
    value: typing.Optional[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c463aec548dbce191036be94223c02eaf27834b7584060ab188d1ef983efd1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f825206eb119213e21a2bda6d5682c65d6cb08ce025dec51a3bbc126c4deddb6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4be12217428cf0352571601ea113e394b7e94c437734aa78e0ec1d085ab09974(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195672ca6c5a3d1311c7df0aa9158bc14d6c794fc4784644e8e7ac8a0878b9fd(
    *,
    dns_entry: typing.Optional[typing.Union[typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bde7832dca0a870017d0a0356f5b4bc1f210467b7d8d9b65b3b5b7f5276f0b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc25495f54b893b03021a7e5b6fd8fd660c93f88cc24ce10d8cac6093a597af(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0e56119ce247a39f25d8d5708c2651f22abffffd4838654e7730e6ed314c4f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3e6da3d29a532566c4ffc9b79c44ccbb3219c9177bc56f98573fa0601c9926(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac839902a82bb3249d5f914796f31854a699e9d66d4cd8e02c1bd2933993d3e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4267f6a81a7401eae8224cb588cbffe02d42753ff0ea473056b355a21fb1d329(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecefdc024efce90061ee7f6e2b40bb0e7e66392dbee262219c69367899d09824(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83955652e8f60816a8dfc860d362d24cd9074558e5203ce65e93dacbdedbb79b(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    dns_entry: typing.Optional[typing.Union[typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831966a8f55d0144a4358728a952d06cf95b5399e516ee872c302d8698d69c53(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    type: builtins.str,
    config: typing.Optional[typing.Union[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__655795269ce7e147137744f2ba1e083e7eedba22de79237575ee8b005cf1a82a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eaf62da566be90a00e237dd4d46a0fb26aadc72a2586fdb4d8873781b893503(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee59f0de8e5f69faf86583d91674fc59f83c2a6365a55c7a721c0ed84f200a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e1bb18f327eb29dcafe2aa90eab61a7b68351195c67c29916c38a6151fbe5e4(
    value: typing.Optional[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7a8a49e7cd68e1297d8d98437b4a10873219a363d11a17693f7feaf2575ea6a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2374214bf7e9a7565156cdfc96bb38aa15e6f611bc54c6a7d7b1051c29df5834(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnTargetGroup.TargetProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6013b6d96d1ec944dde0718d402a1bf9e7f793b85d5e51b92f7276d9d5a25773(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
    healthy_threshold_count: typing.Optional[jsii.Number] = None,
    matcher: typing.Optional[typing.Union[typing.Union[CfnTargetGroup.MatcherProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284ae2bcc13971b5919ae3941428b3f2a1fd4e96d88bbe7701002c71654975f6(
    *,
    http_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980cd558564c88e8d9bf8084b1b7d33d6b49b0488f6f513a0d8a24d59c9859a1(
    *,
    port: jsii.Number,
    protocol: builtins.str,
    vpc_identifier: builtins.str,
    health_check: typing.Optional[typing.Union[typing.Union[CfnTargetGroup.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    protocol_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e7f89194dd9c1b857ab2bed6b8f3a6c3a562ad1a9002fa439ffa8dbe1ee1f5(
    *,
    id: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072993e9cc2983f81da64b85cae6e0152e3064869bf26f3a1a0008495fe35317(
    *,
    type: builtins.str,
    config: typing.Optional[typing.Union[typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    targets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
