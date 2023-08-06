'''
# AWS::SystemsManagerSAP Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as systemsmanagersap
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SystemsManagerSAP construct libraries](https://constructs.dev/search?q=systemsmanagersap)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SystemsManagerSAP resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SystemsManagerSAP.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SystemsManagerSAP](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SystemsManagerSAP.html).

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
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_systemsmanagersap.CfnApplication",
):
    '''A CloudFormation ``AWS::SystemsManagerSAP::Application``.

    An SAP application registered with AWS Systems Manager for SAP.

    :cloudformationResource: AWS::SystemsManagerSAP::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_systemsmanagersap as systemsmanagersap
        
        cfn_application = systemsmanagersap.CfnApplication(self, "MyCfnApplication",
            application_id="applicationId",
            application_type="applicationType",
        
            # the properties below are optional
            credentials=[systemsmanagersap.CfnApplication.CredentialProperty(
                credential_type="credentialType",
                database_name="databaseName",
                secret_id="secretId"
            )],
            instances=["instances"],
            sap_instance_number="sapInstanceNumber",
            sid="sid",
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
        application_id: builtins.str,
        application_type: builtins.str,
        credentials: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnApplication.CredentialProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        sap_instance_number: typing.Optional[builtins.str] = None,
        sid: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SystemsManagerSAP::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The ID of the application.
        :param application_type: The type of the application.
        :param credentials: The credentials of the SAP application.
        :param instances: The Amazon EC2 instances on which your SAP application is running.
        :param sap_instance_number: The SAP instance number of the application.
        :param sid: The System ID of the application.
        :param tags: The tags on the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b853a731a6c76f7401dc9f2cc34f6495cf426d56dea0216bab7d36c25a735e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            application_id=application_id,
            application_type=application_type,
            credentials=credentials,
            instances=instances,
            sap_instance_number=sap_instance_number,
            sid=sid,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d59ff7523a74695f0e33c6eed4defcece68c708a979bf54949913a28215c597)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e1dc6b4b161229886f89fd4a64c2542a24e40952e3f2524d35236a5bcb703a0)
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
        '''The Amazon Resource Name of the SAP application.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags on the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ab7e715600a793d325ae8d9fb524139241d587718221cdbfc2ac8773b0c290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="applicationType")
    def application_type(self) -> builtins.str:
        '''The type of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationType"))

    @application_type.setter
    def application_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcb76b2161ca2dcd7366e08c4be09d4b7231e67a1819943cdf86a244ab5525fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationType", value)

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.CredentialProperty", _IResolvable_a771d0ef]]]]:
        '''The credentials of the SAP application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-credentials
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.CredentialProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "credentials"))

    @credentials.setter
    def credentials(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApplication.CredentialProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df0ac35f2aa7e3d8f918e9a2905da62793162999f0f057c497ec87f3c3c19b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "credentials", value)

    @builtins.property
    @jsii.member(jsii_name="instances")
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon EC2 instances on which your SAP application is running.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-instances
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "instances"))

    @instances.setter
    def instances(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2142b8e454504627a9bee470c76fbdd846dd0de0df45140d572be8813e394f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instances", value)

    @builtins.property
    @jsii.member(jsii_name="sapInstanceNumber")
    def sap_instance_number(self) -> typing.Optional[builtins.str]:
        '''The SAP instance number of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sapinstancenumber
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sapInstanceNumber"))

    @sap_instance_number.setter
    def sap_instance_number(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__872aa228b4a51ef30cfe897efdc84a3bdef94931312b964c71ae754165828fd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sapInstanceNumber", value)

    @builtins.property
    @jsii.member(jsii_name="sid")
    def sid(self) -> typing.Optional[builtins.str]:
        '''The System ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sid"))

    @sid.setter
    def sid(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2073f03ed9f29c0b18bb2913e70758769b878f6b45301d545327ae6f40cf3551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sid", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_systemsmanagersap.CfnApplication.CredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential_type": "credentialType",
            "database_name": "databaseName",
            "secret_id": "secretId",
        },
    )
    class CredentialProperty:
        def __init__(
            self,
            *,
            credential_type: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The credentials of your SAP application.

            :param credential_type: The type of the application credentials.
            :param database_name: The name of the SAP HANA database.
            :param secret_id: The secret ID created in AWS Secrets Manager to store the credentials of the SAP application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_systemsmanagersap as systemsmanagersap
                
                credential_property = systemsmanagersap.CfnApplication.CredentialProperty(
                    credential_type="credentialType",
                    database_name="databaseName",
                    secret_id="secretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73a589607ca4f3aa1aed98cd52ead977d950bda5ab956c30617b3e2be124f977)
                check_type(argname="argument credential_type", value=credential_type, expected_type=type_hints["credential_type"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credential_type is not None:
                self._values["credential_type"] = credential_type
            if database_name is not None:
                self._values["database_name"] = database_name
            if secret_id is not None:
                self._values["secret_id"] = secret_id

        @builtins.property
        def credential_type(self) -> typing.Optional[builtins.str]:
            '''The type of the application credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-credentialtype
            '''
            result = self._values.get("credential_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the SAP HANA database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_id(self) -> typing.Optional[builtins.str]:
            '''The secret ID created in AWS Secrets Manager to store the credentials of the SAP application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-secretid
            '''
            result = self._values.get("secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_systemsmanagersap.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "application_type": "applicationType",
        "credentials": "credentials",
        "instances": "instances",
        "sap_instance_number": "sapInstanceNumber",
        "sid": "sid",
        "tags": "tags",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        application_type: builtins.str,
        credentials: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApplication.CredentialProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        sap_instance_number: typing.Optional[builtins.str] = None,
        sid: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param application_id: The ID of the application.
        :param application_type: The type of the application.
        :param credentials: The credentials of the SAP application.
        :param instances: The Amazon EC2 instances on which your SAP application is running.
        :param sap_instance_number: The SAP instance number of the application.
        :param sid: The System ID of the application.
        :param tags: The tags on the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_systemsmanagersap as systemsmanagersap
            
            cfn_application_props = systemsmanagersap.CfnApplicationProps(
                application_id="applicationId",
                application_type="applicationType",
            
                # the properties below are optional
                credentials=[systemsmanagersap.CfnApplication.CredentialProperty(
                    credential_type="credentialType",
                    database_name="databaseName",
                    secret_id="secretId"
                )],
                instances=["instances"],
                sap_instance_number="sapInstanceNumber",
                sid="sid",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3b4e0e8ed4bce561d5fb850891003700650aef75307b4de512fa0ea0cc5a997)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument application_type", value=application_type, expected_type=type_hints["application_type"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument sap_instance_number", value=sap_instance_number, expected_type=type_hints["sap_instance_number"])
            check_type(argname="argument sid", value=sid, expected_type=type_hints["sid"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "application_type": application_type,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if instances is not None:
            self._values["instances"] = instances
        if sap_instance_number is not None:
            self._values["sap_instance_number"] = sap_instance_number
        if sid is not None:
            self._values["sid"] = sid
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_type(self) -> builtins.str:
        '''The type of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationtype
        '''
        result = self._values.get("application_type")
        assert result is not None, "Required property 'application_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.CredentialProperty, _IResolvable_a771d0ef]]]]:
        '''The credentials of the SAP application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-credentials
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.CredentialProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon EC2 instances on which your SAP application is running.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-instances
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sap_instance_number(self) -> typing.Optional[builtins.str]:
        '''The SAP instance number of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sapinstancenumber
        '''
        result = self._values.get("sap_instance_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sid(self) -> typing.Optional[builtins.str]:
        '''The System ID of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sid
        '''
        result = self._values.get("sid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags on the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
]

publication.publish()

def _typecheckingstub__91b853a731a6c76f7401dc9f2cc34f6495cf426d56dea0216bab7d36c25a735e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    application_type: builtins.str,
    credentials: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApplication.CredentialProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    sap_instance_number: typing.Optional[builtins.str] = None,
    sid: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d59ff7523a74695f0e33c6eed4defcece68c708a979bf54949913a28215c597(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1dc6b4b161229886f89fd4a64c2542a24e40952e3f2524d35236a5bcb703a0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ab7e715600a793d325ae8d9fb524139241d587718221cdbfc2ac8773b0c290(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcb76b2161ca2dcd7366e08c4be09d4b7231e67a1819943cdf86a244ab5525fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df0ac35f2aa7e3d8f918e9a2905da62793162999f0f057c497ec87f3c3c19b3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApplication.CredentialProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2142b8e454504627a9bee470c76fbdd846dd0de0df45140d572be8813e394f5d(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__872aa228b4a51ef30cfe897efdc84a3bdef94931312b964c71ae754165828fd9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2073f03ed9f29c0b18bb2913e70758769b878f6b45301d545327ae6f40cf3551(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a589607ca4f3aa1aed98cd52ead977d950bda5ab956c30617b3e2be124f977(
    *,
    credential_type: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3b4e0e8ed4bce561d5fb850891003700650aef75307b4de512fa0ea0cc5a997(
    *,
    application_id: builtins.str,
    application_type: builtins.str,
    credentials: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApplication.CredentialProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    sap_instance_number: typing.Optional[builtins.str] = None,
    sid: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
