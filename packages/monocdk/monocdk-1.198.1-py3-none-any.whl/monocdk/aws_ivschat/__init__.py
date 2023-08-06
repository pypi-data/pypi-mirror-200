'''
# AWS::IVSChat Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as ivschat
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IVSChat construct libraries](https://constructs.dev/search?q=ivschat)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IVSChat resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IVSChat.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IVSChat](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IVSChat.html).

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
class CfnLoggingConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivschat.CfnLoggingConfiguration",
):
    '''A CloudFormation ``AWS::IVSChat::LoggingConfiguration``.

    The ``AWS::IVSChat::LoggingConfiguration`` resource specifies an  logging configuration that allows clients to store and record sent messages. For more information, see `CreateLoggingConfiguration <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateLoggingConfiguration.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :cloudformationResource: AWS::IVSChat::LoggingConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ivschat as ivschat
        
        cfn_logging_configuration = ivschat.CfnLoggingConfiguration(self, "MyCfnLoggingConfiguration",
            destination_configuration=ivschat.CfnLoggingConfiguration.DestinationConfigurationProperty(
                cloud_watch_logs=ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty(
                    log_group_name="logGroupName"
                ),
                firehose=ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty(
                    delivery_stream_name="deliveryStreamName"
                ),
                s3=ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            ),
        
            # the properties below are optional
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
        destination_configuration: typing.Union[typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVSChat::LoggingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_configuration: The DestinationConfiguration is a complex type that contains information about where chat content will be logged.
        :param name: Logging-configuration name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fbaaa5dbbd0350a9e6486c6834c644c8414fa90fef0d3a26ba872a5a4457d62)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggingConfigurationProps(
            destination_configuration=destination_configuration, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b39f400e04041bfb96462d883a218c4f731cb87c67948e146c62998baea302)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44630c63c70bc87f02b3d5c99b70196102cdffc3b53bb0c49a1fc2e5559b6480)
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
        '''The logging-configuration ARN.

        For example: ``arn:aws:ivschat:us-west-2:123456789012:logging-configuration/abcdABCDefgh``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The logging-configuration ID.

        For example: ``abcdABCDefgh``

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Indicates the current state of the logging configuration.

        When the state is ``ACTIVE`` , the configuration is ready to log a chat session. Valid values: ``CREATING`` | ``CREATE_FAILED`` | ``DELETING`` | ``DELETE_FAILED`` | ``UPDATING`` | ``UPDATE_FAILED`` | ``ACTIVE`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfiguration")
    def destination_configuration(
        self,
    ) -> typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _IResolvable_a771d0ef]:
        '''The DestinationConfiguration is a complex type that contains information about where chat content will be logged.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration
        '''
        return typing.cast(typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "destinationConfiguration"))

    @destination_configuration.setter
    def destination_configuration(
        self,
        value: typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1577cf4d288c6e7470016131c4c5c0252892b9fb5e9c74ad57e2a6e7a40b81c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Logging-configuration name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc5f36bd82543ca2ea797d8e284ee605e732b69765caf5aa907010acc236273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_name": "logGroupName"},
    )
    class CloudWatchLogsDestinationConfigurationProperty:
        def __init__(self, *, log_group_name: builtins.str) -> None:
            '''The CloudWatchLogsDestinationConfiguration property type specifies a CloudWatch Logs location where chat logs will be stored.

            :param log_group_name: Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_ivschat as ivschat
                
                cloud_watch_logs_destination_configuration_property = ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96259338c6174b78a28bb434f49bf9b9e46a0a90474e0ae16e51046a7aa30f56)
                check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_name": log_group_name,
            }

        @builtins.property
        def log_group_name(self) -> builtins.str:
            '''Name of the Amazon Cloudwatch Logs destination where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration.html#cfn-ivschat-loggingconfiguration-cloudwatchlogsdestinationconfiguration-loggroupname
            '''
            result = self._values.get("log_group_name")
            assert result is not None, "Required property 'log_group_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_ivschat.CfnLoggingConfiguration.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[typing.Union["CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            firehose: typing.Optional[typing.Union[typing.Union["CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            s3: typing.Optional[typing.Union[typing.Union["CfnLoggingConfiguration.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The DestinationConfiguration property type describes a location where chat logs will be stored.

            Each member represents the configuration of one log destination. For logging, you define only one type of destination.

            :param cloud_watch_logs: An Amazon CloudWatch Logs destination configuration where chat activity will be logged.
            :param firehose: An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.
            :param s3: An Amazon S3 destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_ivschat as ivschat
                
                destination_configuration_property = ivschat.CfnLoggingConfiguration.DestinationConfigurationProperty(
                    cloud_watch_logs=ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty(
                        log_group_name="logGroupName"
                    ),
                    firehose=ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty(
                        delivery_stream_name="deliveryStreamName"
                    ),
                    s3=ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c372cd31a531e9da627831dba49c0ab22a79ea2b259835a3600c6218b30f7ca)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if firehose is not None:
                self._values["firehose"] = firehose
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union["CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An Amazon CloudWatch Logs destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union["CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union["CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union["CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union["CfnLoggingConfiguration.S3DestinationConfigurationProperty", _IResolvable_a771d0ef]]:
            '''An Amazon S3 destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union["CfnLoggingConfiguration.S3DestinationConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream_name": "deliveryStreamName"},
    )
    class FirehoseDestinationConfigurationProperty:
        def __init__(self, *, delivery_stream_name: builtins.str) -> None:
            '''The FirehoseDestinationConfiguration property type specifies a Kinesis Firehose location where chat logs will be stored.

            :param delivery_stream_name: Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-firehosedestinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_ivschat as ivschat
                
                firehose_destination_configuration_property = ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty(
                    delivery_stream_name="deliveryStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e55fea53fa4928ee42fb54ac3c414feb723f6174228157df1d5eeb23fe5b5ed)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream_name": delivery_stream_name,
            }

        @builtins.property
        def delivery_stream_name(self) -> builtins.str:
            '''Name of the Amazon Kinesis Firehose delivery stream where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-firehosedestinationconfiguration.html#cfn-ivschat-loggingconfiguration-firehosedestinationconfiguration-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            assert result is not None, "Required property 'delivery_stream_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseDestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class S3DestinationConfigurationProperty:
        def __init__(self, *, bucket_name: builtins.str) -> None:
            '''The S3DestinationConfiguration property type specifies an S3 location where chat logs will be stored.

            :param bucket_name: Name of the Amazon S3 bucket where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_ivschat as ivschat
                
                s3_destination_configuration_property = ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e357f2dbea7a446be6dace2107075dadfaad1ee427ee6a89a818309af45998c)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''Name of the Amazon S3 bucket where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-s3destinationconfiguration.html#cfn-ivschat-loggingconfiguration-s3destinationconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_ivschat.CfnLoggingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_configuration": "destinationConfiguration",
        "name": "name",
        "tags": "tags",
    },
)
class CfnLoggingConfigurationProps:
    def __init__(
        self,
        *,
        destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLoggingConfiguration``.

        :param destination_configuration: The DestinationConfiguration is a complex type that contains information about where chat content will be logged.
        :param name: Logging-configuration name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ivschat as ivschat
            
            cfn_logging_configuration_props = ivschat.CfnLoggingConfigurationProps(
                destination_configuration=ivschat.CfnLoggingConfiguration.DestinationConfigurationProperty(
                    cloud_watch_logs=ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty(
                        log_group_name="logGroupName"
                    ),
                    firehose=ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty(
                        delivery_stream_name="deliveryStreamName"
                    ),
                    s3=ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                ),
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f377563a8a60647d0146e2bc6db79ecfb3d337406a17a5dca262af716bb210)
            check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_configuration": destination_configuration,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_configuration(
        self,
    ) -> typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _IResolvable_a771d0ef]:
        '''The DestinationConfiguration is a complex type that contains information about where chat content will be logged.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        assert result is not None, "Required property 'destination_configuration' is missing"
        return typing.cast(typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Logging-configuration name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRoom(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_ivschat.CfnRoom",
):
    '''A CloudFormation ``AWS::IVSChat::Room``.

    The ``AWS::IVSChat::Room`` resource specifies an  room that allows clients to connect and pass messages. For more information, see `CreateRoom <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateRoom.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :cloudformationResource: AWS::IVSChat::Room
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ivschat as ivschat
        
        cfn_room = ivschat.CfnRoom(self, "MyCfnRoom",
            logging_configuration_identifiers=["loggingConfigurationIdentifiers"],
            maximum_message_length=123,
            maximum_message_rate_per_second=123,
            message_review_handler=ivschat.CfnRoom.MessageReviewHandlerProperty(
                fallback_result="fallbackResult",
                uri="uri"
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
        logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_message_length: typing.Optional[jsii.Number] = None,
        maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
        message_review_handler: typing.Optional[typing.Union[typing.Union["CfnRoom.MessageReviewHandlerProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVSChat::Room``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param logging_configuration_identifiers: List of logging-configuration identifiers attached to the room.
        :param maximum_message_length: Maximum number of characters in a single message. Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes.
        :param maximum_message_rate_per_second: Maximum number of messages per second that can be sent to the room (by all clients).
        :param message_review_handler: Configuration information for optional review of messages.
        :param name: Room name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c32af733907d63af30b8fc5f22922508faa9c387d47b799c6d835fc5f2d19b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoomProps(
            logging_configuration_identifiers=logging_configuration_identifiers,
            maximum_message_length=maximum_message_length,
            maximum_message_rate_per_second=maximum_message_rate_per_second,
            message_review_handler=message_review_handler,
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
            type_hints = typing.get_type_hints(_typecheckingstub__c06bcc22abc884dcee60067b390457f7d56393b47c3d79ae3584a022fd0d5370)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f874bdd1624c8e09142225d3c284d8d49f85b1b470b7749f5fd1c2262672084a)
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
        '''The room ARN.

        For example: ``arn:aws:ivschat:us-west-2:123456789012:room/abcdABCDefgh``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The room ID.

        For example: ``abcdABCDefgh``

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="loggingConfigurationIdentifiers")
    def logging_configuration_identifiers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of logging-configuration identifiers attached to the room.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-loggingconfigurationidentifiers
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loggingConfigurationIdentifiers"))

    @logging_configuration_identifiers.setter
    def logging_configuration_identifiers(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326c722acab585dc0a06d12747b3a86db2867b23b3278a0b6076fc4b25c0a231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfigurationIdentifiers", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMessageLength")
    def maximum_message_length(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of characters in a single message.

        Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessagelength
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumMessageLength"))

    @maximum_message_length.setter
    def maximum_message_length(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0eb125413cf91319bb1dcd7256db8f1aa64c420ec34e77d5a7fee58ab3e0a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumMessageLength", value)

    @builtins.property
    @jsii.member(jsii_name="maximumMessageRatePerSecond")
    def maximum_message_rate_per_second(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of messages per second that can be sent to the room (by all clients).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessageratepersecond
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumMessageRatePerSecond"))

    @maximum_message_rate_per_second.setter
    def maximum_message_rate_per_second(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__077751704546c2453aaec4627c73c944554126b072f10673e0baebb735773708)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumMessageRatePerSecond", value)

    @builtins.property
    @jsii.member(jsii_name="messageReviewHandler")
    def message_review_handler(
        self,
    ) -> typing.Optional[typing.Union["CfnRoom.MessageReviewHandlerProperty", _IResolvable_a771d0ef]]:
        '''Configuration information for optional review of messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-messagereviewhandler
        '''
        return typing.cast(typing.Optional[typing.Union["CfnRoom.MessageReviewHandlerProperty", _IResolvable_a771d0ef]], jsii.get(self, "messageReviewHandler"))

    @message_review_handler.setter
    def message_review_handler(
        self,
        value: typing.Optional[typing.Union["CfnRoom.MessageReviewHandlerProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__584189d2e77bb56c29c48bf01e0bbff4dfc43f7393ad6becc70a968f403074b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageReviewHandler", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Room name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdd51c3d1dd841cb12fe317fa1030ce2a3ddd3b18705d322f62b4d95713f08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_ivschat.CfnRoom.MessageReviewHandlerProperty",
        jsii_struct_bases=[],
        name_mapping={"fallback_result": "fallbackResult", "uri": "uri"},
    )
    class MessageReviewHandlerProperty:
        def __init__(
            self,
            *,
            fallback_result: typing.Optional[builtins.str] = None,
            uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The MessageReviewHandler property type specifies configuration information for optional message review.

            :param fallback_result: Specifies the fallback behavior (whether the message is allowed or denied) if the handler does not return a valid response, encounters an error, or times out. (For the timeout period, see `Service Quotas <https://docs.aws.amazon.com/ivs/latest/userguide/service-quotas.html>`_ .) If allowed, the message is delivered with returned content to all users connected to the room. If denied, the message is not delivered to any user. *Default* : ``ALLOW``
            :param uri: Identifier of the message review handler. Currently this must be an ARN of a lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_ivschat as ivschat
                
                message_review_handler_property = ivschat.CfnRoom.MessageReviewHandlerProperty(
                    fallback_result="fallbackResult",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c11e85b52d992ac76a2435fe1cbdaea421de3ece0d4b53407e3f324c75d0ef87)
                check_type(argname="argument fallback_result", value=fallback_result, expected_type=type_hints["fallback_result"])
                check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fallback_result is not None:
                self._values["fallback_result"] = fallback_result
            if uri is not None:
                self._values["uri"] = uri

        @builtins.property
        def fallback_result(self) -> typing.Optional[builtins.str]:
            '''Specifies the fallback behavior (whether the message is allowed or denied) if the handler does not return a valid response, encounters an error, or times out.

            (For the timeout period, see `Service Quotas <https://docs.aws.amazon.com/ivs/latest/userguide/service-quotas.html>`_ .) If allowed, the message is delivered with returned content to all users connected to the room. If denied, the message is not delivered to any user.

            *Default* : ``ALLOW``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html#cfn-ivschat-room-messagereviewhandler-fallbackresult
            '''
            result = self._values.get("fallback_result")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uri(self) -> typing.Optional[builtins.str]:
            '''Identifier of the message review handler.

            Currently this must be an ARN of a lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-room-messagereviewhandler.html#cfn-ivschat-room-messagereviewhandler-uri
            '''
            result = self._values.get("uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageReviewHandlerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_ivschat.CfnRoomProps",
    jsii_struct_bases=[],
    name_mapping={
        "logging_configuration_identifiers": "loggingConfigurationIdentifiers",
        "maximum_message_length": "maximumMessageLength",
        "maximum_message_rate_per_second": "maximumMessageRatePerSecond",
        "message_review_handler": "messageReviewHandler",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRoomProps:
    def __init__(
        self,
        *,
        logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_message_length: typing.Optional[jsii.Number] = None,
        maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
        message_review_handler: typing.Optional[typing.Union[typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRoom``.

        :param logging_configuration_identifiers: List of logging-configuration identifiers attached to the room.
        :param maximum_message_length: Maximum number of characters in a single message. Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes.
        :param maximum_message_rate_per_second: Maximum number of messages per second that can be sent to the room (by all clients).
        :param message_review_handler: Configuration information for optional review of messages.
        :param name: Room name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ivschat as ivschat
            
            cfn_room_props = ivschat.CfnRoomProps(
                logging_configuration_identifiers=["loggingConfigurationIdentifiers"],
                maximum_message_length=123,
                maximum_message_rate_per_second=123,
                message_review_handler=ivschat.CfnRoom.MessageReviewHandlerProperty(
                    fallback_result="fallbackResult",
                    uri="uri"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fba89be56208290c9beefb645895b5eb1b5a1ca91b9b1e1e2289b4c65e9ba2)
            check_type(argname="argument logging_configuration_identifiers", value=logging_configuration_identifiers, expected_type=type_hints["logging_configuration_identifiers"])
            check_type(argname="argument maximum_message_length", value=maximum_message_length, expected_type=type_hints["maximum_message_length"])
            check_type(argname="argument maximum_message_rate_per_second", value=maximum_message_rate_per_second, expected_type=type_hints["maximum_message_rate_per_second"])
            check_type(argname="argument message_review_handler", value=message_review_handler, expected_type=type_hints["message_review_handler"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if logging_configuration_identifiers is not None:
            self._values["logging_configuration_identifiers"] = logging_configuration_identifiers
        if maximum_message_length is not None:
            self._values["maximum_message_length"] = maximum_message_length
        if maximum_message_rate_per_second is not None:
            self._values["maximum_message_rate_per_second"] = maximum_message_rate_per_second
        if message_review_handler is not None:
            self._values["message_review_handler"] = message_review_handler
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def logging_configuration_identifiers(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''List of logging-configuration identifiers attached to the room.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-loggingconfigurationidentifiers
        '''
        result = self._values.get("logging_configuration_identifiers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def maximum_message_length(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of characters in a single message.

        Messages are expected to be UTF-8 encoded and this limit applies specifically to rune/code-point count, not number of bytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessagelength
        '''
        result = self._values.get("maximum_message_length")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_message_rate_per_second(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of messages per second that can be sent to the room (by all clients).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-maximummessageratepersecond
        '''
        result = self._values.get("maximum_message_rate_per_second")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_review_handler(
        self,
    ) -> typing.Optional[typing.Union[CfnRoom.MessageReviewHandlerProperty, _IResolvable_a771d0ef]]:
        '''Configuration information for optional review of messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-messagereviewhandler
        '''
        result = self._values.get("message_review_handler")
        return typing.cast(typing.Optional[typing.Union[CfnRoom.MessageReviewHandlerProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Room name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoomProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLoggingConfiguration",
    "CfnLoggingConfigurationProps",
    "CfnRoom",
    "CfnRoomProps",
]

publication.publish()

def _typecheckingstub__4fbaaa5dbbd0350a9e6486c6834c644c8414fa90fef0d3a26ba872a5a4457d62(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b39f400e04041bfb96462d883a218c4f731cb87c67948e146c62998baea302(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44630c63c70bc87f02b3d5c99b70196102cdffc3b53bb0c49a1fc2e5559b6480(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1577cf4d288c6e7470016131c4c5c0252892b9fb5e9c74ad57e2a6e7a40b81c2(
    value: typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc5f36bd82543ca2ea797d8e284ee605e732b69765caf5aa907010acc236273(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96259338c6174b78a28bb434f49bf9b9e46a0a90474e0ae16e51046a7aa30f56(
    *,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c372cd31a531e9da627831dba49c0ab22a79ea2b259835a3600c6218b30f7ca(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[typing.Union[CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    firehose: typing.Optional[typing.Union[typing.Union[CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    s3: typing.Optional[typing.Union[typing.Union[CfnLoggingConfiguration.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e55fea53fa4928ee42fb54ac3c414feb723f6174228157df1d5eeb23fe5b5ed(
    *,
    delivery_stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e357f2dbea7a446be6dace2107075dadfaad1ee427ee6a89a818309af45998c(
    *,
    bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f377563a8a60647d0146e2bc6db79ecfb3d337406a17a5dca262af716bb210(
    *,
    destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c32af733907d63af30b8fc5f22922508faa9c387d47b799c6d835fc5f2d19b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_message_length: typing.Optional[jsii.Number] = None,
    maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
    message_review_handler: typing.Optional[typing.Union[typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06bcc22abc884dcee60067b390457f7d56393b47c3d79ae3584a022fd0d5370(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f874bdd1624c8e09142225d3c284d8d49f85b1b470b7749f5fd1c2262672084a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326c722acab585dc0a06d12747b3a86db2867b23b3278a0b6076fc4b25c0a231(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eb125413cf91319bb1dcd7256db8f1aa64c420ec34e77d5a7fee58ab3e0a57(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__077751704546c2453aaec4627c73c944554126b072f10673e0baebb735773708(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584189d2e77bb56c29c48bf01e0bbff4dfc43f7393ad6becc70a968f403074b7(
    value: typing.Optional[typing.Union[CfnRoom.MessageReviewHandlerProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdd51c3d1dd841cb12fe317fa1030ce2a3ddd3b18705d322f62b4d95713f08b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11e85b52d992ac76a2435fe1cbdaea421de3ece0d4b53407e3f324c75d0ef87(
    *,
    fallback_result: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fba89be56208290c9beefb645895b5eb1b5a1ca91b9b1e1e2289b4c65e9ba2(
    *,
    logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_message_length: typing.Optional[jsii.Number] = None,
    maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
    message_review_handler: typing.Optional[typing.Union[typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
