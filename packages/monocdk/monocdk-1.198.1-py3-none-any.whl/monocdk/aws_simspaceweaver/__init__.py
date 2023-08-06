'''
# AWS::SimSpaceWeaver Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as simspaceweaver
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for SimSpaceWeaver construct libraries](https://constructs.dev/search?q=simspaceweaver)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::SimSpaceWeaver resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SimSpaceWeaver.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::SimSpaceWeaver](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_SimSpaceWeaver.html).

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
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnSimulation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_simspaceweaver.CfnSimulation",
):
    '''A CloudFormation ``AWS::SimSpaceWeaver::Simulation``.

    Use the ``AWS::SimSpaceWeaver::Simulation`` resource to specify a simulation that AWS CloudFormation starts in the AWS Cloud , in your AWS account . In the resource properties section of your template, provide the name of an existing IAM role configured with the proper permissions, and the name of an existing Amazon S3 bucket. Your account must have permissions to read the Amazon S3 bucket. The Amazon S3 bucket must contain a valid schema. The schema must refer to simulation assets that are already uploaded to the AWS Cloud . For more information, see the `detailed tutorial <https://docs.aws.amazon.com/simspaceweaver/latest/userguide/getting-started_detailed.html>`_ in the *AWS SimSpace Weaver User Guide* .

    :cloudformationResource: AWS::SimSpaceWeaver::Simulation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_simspaceweaver as simspaceweaver
        
        cfn_simulation = simspaceweaver.CfnSimulation(self, "MyCfnSimulation",
            name="name",
            role_arn="roleArn",
            schema_s3_location=simspaceweaver.CfnSimulation.S3LocationProperty(
                bucket_name="bucketName",
                object_key="objectKey"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schema_s3_location: typing.Optional[typing.Union[typing.Union["CfnSimulation.S3LocationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::SimSpaceWeaver::Simulation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the simulation.
        :param role_arn: The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param schema_s3_location: The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ). For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b71fa43684da9b98634594132f15a5bb4ffca872713f252c19c1b19c6f66faa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSimulationProps(
            name=name, role_arn=role_arn, schema_s3_location=schema_s3_location
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f4ab008c3f017687497a1ce1878456b9e4802e09c1eed0bb922d8a30bda40f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29da83a840d9f7c09e769ef6f93ab8137c8c60e2fc8c3976599174e09d16fd29)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDescribePayload")
    def attr_describe_payload(self) -> builtins.str:
        '''The JSON blob that the `DescribeSimulation <https://docs.aws.amazon.com/simspaceweaver/latest/APIReference/API_DescribeSimulation.html>`_ action returns.

        :cloudformationAttribute: DescribePayload
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDescribePayload"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the simulation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b211b484b0eca0244ee201582e2db3d925f50cd7b38a92f151e5ff54f031e086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3916cb1226e0f7e03469394a0061595547c3cf537f1d54b201757dfb15248de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="schemaS3Location")
    def schema_s3_location(
        self,
    ) -> typing.Optional[typing.Union["CfnSimulation.S3LocationProperty", _IResolvable_a771d0ef]]:
        '''The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ).

        For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-schemas3location
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSimulation.S3LocationProperty", _IResolvable_a771d0ef]], jsii.get(self, "schemaS3Location"))

    @schema_s3_location.setter
    def schema_s3_location(
        self,
        value: typing.Optional[typing.Union["CfnSimulation.S3LocationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fae925c3d30e5c9a95ca573c7a8e4b131d728b12101edd914c18ccce5988924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schemaS3Location", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_simspaceweaver.CfnSimulation.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "object_key": "objectKey"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            object_key: builtins.str,
        ) -> None:
            '''A location in Amazon Simple Storage Service ( Amazon S3 ) where SimSpace Weaver stores simulation data, such as your app .zip files and schema file. For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

            :param bucket_name: The name of an Amazon S3 bucket. For more information about buckets, see `Creating, configuring, and working with Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html>`_ in the *Amazon Simple Storage Service User Guide* .
            :param object_key: The key name of an object in Amazon S3 . For more information about Amazon S3 objects and object keys, see `Uploading, downloading, and working with objects in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-downloading-objects.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_simspaceweaver as simspaceweaver
                
                s3_location_property = simspaceweaver.CfnSimulation.S3LocationProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f0f35bb6b2455cbc6614990329bb20ca33af649cba96ba81a590addbc5f72cf)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "object_key": object_key,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of an Amazon S3 bucket.

            For more information about buckets, see `Creating, configuring, and working with Amazon S3 buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-buckets-s3.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html#cfn-simspaceweaver-simulation-s3location-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_key(self) -> builtins.str:
            '''The key name of an object in Amazon S3 .

            For more information about Amazon S3 objects and object keys, see `Uploading, downloading, and working with objects in Amazon S3 <https://docs.aws.amazon.com/AmazonS3/latest/userguide/uploading-downloading-objects.html>`_ in the *Amazon Simple Storage Service User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-simspaceweaver-simulation-s3location.html#cfn-simspaceweaver-simulation-s3location-objectkey
            '''
            result = self._values.get("object_key")
            assert result is not None, "Required property 'object_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_simspaceweaver.CfnSimulationProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "role_arn": "roleArn",
        "schema_s3_location": "schemaS3Location",
    },
)
class CfnSimulationProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schema_s3_location: typing.Optional[typing.Union[typing.Union[CfnSimulation.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSimulation``.

        :param name: The name of the simulation.
        :param role_arn: The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .
        :param schema_s3_location: The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ). For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_simspaceweaver as simspaceweaver
            
            cfn_simulation_props = simspaceweaver.CfnSimulationProps(
                name="name",
                role_arn="roleArn",
                schema_s3_location=simspaceweaver.CfnSimulation.S3LocationProperty(
                    bucket_name="bucketName",
                    object_key="objectKey"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb77f42934bf03ee4109b581a1735e30daa13c07d44b0333a0df4851587f1d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schema_s3_location", value=schema_s3_location, expected_type=type_hints["schema_s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schema_s3_location is not None:
            self._values["schema_s3_location"] = schema_s3_location

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the simulation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role that the simulation assumes to perform actions.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* . For more information about IAM roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *AWS Identity and Access Management User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_s3_location(
        self,
    ) -> typing.Optional[typing.Union[CfnSimulation.S3LocationProperty, _IResolvable_a771d0ef]]:
        '''The location of the simulation schema in Amazon Simple Storage Service ( Amazon S3 ).

        For more information about Amazon S3 , see the `*Amazon Simple Storage Service User Guide* <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-simspaceweaver-simulation.html#cfn-simspaceweaver-simulation-schemas3location
        '''
        result = self._values.get("schema_s3_location")
        return typing.cast(typing.Optional[typing.Union[CfnSimulation.S3LocationProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSimulationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSimulation",
    "CfnSimulationProps",
]

publication.publish()

def _typecheckingstub__9b71fa43684da9b98634594132f15a5bb4ffca872713f252c19c1b19c6f66faa(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schema_s3_location: typing.Optional[typing.Union[typing.Union[CfnSimulation.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f4ab008c3f017687497a1ce1878456b9e4802e09c1eed0bb922d8a30bda40f(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29da83a840d9f7c09e769ef6f93ab8137c8c60e2fc8c3976599174e09d16fd29(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b211b484b0eca0244ee201582e2db3d925f50cd7b38a92f151e5ff54f031e086(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3916cb1226e0f7e03469394a0061595547c3cf537f1d54b201757dfb15248de5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fae925c3d30e5c9a95ca573c7a8e4b131d728b12101edd914c18ccce5988924(
    value: typing.Optional[typing.Union[CfnSimulation.S3LocationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f0f35bb6b2455cbc6614990329bb20ca33af649cba96ba81a590addbc5f72cf(
    *,
    bucket_name: builtins.str,
    object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb77f42934bf03ee4109b581a1735e30daa13c07d44b0333a0df4851587f1d2(
    *,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schema_s3_location: typing.Optional[typing.Union[typing.Union[CfnSimulation.S3LocationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass
