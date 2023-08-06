'''
# AWS::Omics Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as omics
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Omics construct libraries](https://constructs.dev/search?q=omics)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Omics resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Omics.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Omics](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Omics.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAnnotationStore(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnAnnotationStore",
):
    '''A CloudFormation ``AWS::Omics::AnnotationStore``.

    Creates an annotation store.

    :cloudformationResource: AWS::Omics::AnnotationStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        # schema: Any
        
        cfn_annotation_store = omics.CfnAnnotationStore(self, "MyCfnAnnotationStore",
            name="name",
            store_format="storeFormat",
        
            # the properties below are optional
            description="description",
            reference=omics.CfnAnnotationStore.ReferenceItemProperty(
                reference_arn="referenceArn"
            ),
            sse_config=omics.CfnAnnotationStore.SseConfigProperty(
                type="type",
        
                # the properties below are optional
                key_arn="keyArn"
            ),
            store_options=omics.CfnAnnotationStore.StoreOptionsProperty(
                tsv_store_options=omics.CfnAnnotationStore.TsvStoreOptionsProperty(
                    annotation_type="annotationType",
                    format_to_header={
                        "format_to_header_key": "formatToHeader"
                    },
                    schema=schema
                )
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        store_format: builtins.str,
        description: typing.Optional[builtins.str] = None,
        reference: typing.Optional[typing.Union[typing.Union["CfnAnnotationStore.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_config: typing.Optional[typing.Union[typing.Union["CfnAnnotationStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        store_options: typing.Optional[typing.Union[typing.Union["CfnAnnotationStore.StoreOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::AnnotationStore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the Annotation Store.
        :param store_format: The annotation file format of the store.
        :param description: A description for the store.
        :param reference: The genome reference for the store's annotations.
        :param sse_config: The store's server-side encryption (SSE) settings.
        :param store_options: File parsing options for the annotation store.
        :param tags: Tags for the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b4ae2ffa77c36ed1fa9592aaeab76900ec05ec67ab11c4af7fc4727f56a144d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAnnotationStoreProps(
            name=name,
            store_format=store_format,
            description=description,
            reference=reference,
            sse_config=sse_config,
            store_options=store_options,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959834183560fa8a26d8c72c86ee1e1ece4a5cd127fb3947a9c1dc12c4d24e7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aae7204020c44ed955f41659b4fccbef4c5b210377217f8c22dd0a7f53145f9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the store was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The store's ID.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The store's status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''The store's status message.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStoreArn")
    def attr_store_arn(self) -> builtins.str:
        '''The store's ARN.

        :cloudformationAttribute: StoreArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStoreArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStoreSizeBytes")
    def attr_store_size_bytes(self) -> _IResolvable_a771d0ef:
        '''The store's size in bytes.

        :cloudformationAttribute: StoreSizeBytes
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrStoreSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''When the store was updated.

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the Annotation Store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae3cc3c52237c6c85eb1e345d9aba18ba06d8537175d34575d6fb840af8887f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storeFormat")
    def store_format(self) -> builtins.str:
        '''The annotation file format of the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeformat
        '''
        return typing.cast(builtins.str, jsii.get(self, "storeFormat"))

    @store_format.setter
    def store_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0d68bc30808877b2a05c6e45a818af998111431191ac73455e29eddcb1c505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeFormat", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb52d7c171ec363bd21241d8d1d7b83ba390070a85fe2a1978d49b625a46def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(
        self,
    ) -> typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _IResolvable_a771d0ef]]:
        '''The genome reference for the store's annotations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-reference
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _IResolvable_a771d0ef]], jsii.get(self, "reference"))

    @reference.setter
    def reference(
        self,
        value: typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1e21ac28126977918057b96a4a20efc9a65b082970fa2596332487ba9b7cc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reference", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union["CfnAnnotationStore.SseConfigProperty", _IResolvable_a771d0ef]]:
        '''The store's server-side encryption (SSE) settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnnotationStore.SseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union["CfnAnnotationStore.SseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__698939df3768f6f06d68aaf5859ef486bf8bf98662d4f212bf2e041dc244d6f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="storeOptions")
    def store_options(
        self,
    ) -> typing.Optional[typing.Union["CfnAnnotationStore.StoreOptionsProperty", _IResolvable_a771d0ef]]:
        '''File parsing options for the annotation store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnnotationStore.StoreOptionsProperty", _IResolvable_a771d0ef]], jsii.get(self, "storeOptions"))

    @store_options.setter
    def store_options(
        self,
        value: typing.Optional[typing.Union["CfnAnnotationStore.StoreOptionsProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510610ce7dd94ac10ed4c972d72bb289119af0609275db39dba6525ab09a164a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeOptions", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnAnnotationStore.ReferenceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class ReferenceItemProperty:
        def __init__(self, *, reference_arn: builtins.str) -> None:
            '''A genome reference.

            :param reference_arn: The reference's ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-referenceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                reference_item_property = omics.CfnAnnotationStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__382b433547b1a0879c1fecf9f6f5988a2b8a561dc610c310c72c40fd6cc637ef)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "reference_arn": reference_arn,
            }

        @builtins.property
        def reference_arn(self) -> builtins.str:
            '''The reference's ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-referenceitem.html#cfn-omics-annotationstore-referenceitem-referencearn
            '''
            result = self._values.get("reference_arn")
            assert result is not None, "Required property 'reference_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnAnnotationStore.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "key_arn": "keyArn"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param type: The encryption type.
            :param key_arn: An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                sse_config_property = omics.CfnAnnotationStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__464cc5a0c13ed5ccd5549b513ac550553344a818e8829b653925e478124f4cdb)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''The encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html#cfn-omics-annotationstore-sseconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-sseconfig.html#cfn-omics-annotationstore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnAnnotationStore.StoreOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"tsv_store_options": "tsvStoreOptions"},
    )
    class StoreOptionsProperty:
        def __init__(
            self,
            *,
            tsv_store_options: typing.Union[typing.Union["CfnAnnotationStore.TsvStoreOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        ) -> None:
            '''The store's file parsing options.

            :param tsv_store_options: Formatting options for a TSV file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                # schema: Any
                
                store_options_property = omics.CfnAnnotationStore.StoreOptionsProperty(
                    tsv_store_options=omics.CfnAnnotationStore.TsvStoreOptionsProperty(
                        annotation_type="annotationType",
                        format_to_header={
                            "format_to_header_key": "formatToHeader"
                        },
                        schema=schema
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3eda8b007ef4afac56d0f10f706e514831b985b2d6f05812412f9e0e6056070c)
                check_type(argname="argument tsv_store_options", value=tsv_store_options, expected_type=type_hints["tsv_store_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "tsv_store_options": tsv_store_options,
            }

        @builtins.property
        def tsv_store_options(
            self,
        ) -> typing.Union["CfnAnnotationStore.TsvStoreOptionsProperty", _IResolvable_a771d0ef]:
            '''Formatting options for a TSV file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html#cfn-omics-annotationstore-storeoptions-tsvstoreoptions
            '''
            result = self._values.get("tsv_store_options")
            assert result is not None, "Required property 'tsv_store_options' is missing"
            return typing.cast(typing.Union["CfnAnnotationStore.TsvStoreOptionsProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StoreOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnAnnotationStore.TsvStoreOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "annotation_type": "annotationType",
            "format_to_header": "formatToHeader",
            "schema": "schema",
        },
    )
    class TsvStoreOptionsProperty:
        def __init__(
            self,
            *,
            annotation_type: typing.Optional[builtins.str] = None,
            format_to_header: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            schema: typing.Any = None,
        ) -> None:
            '''The store's parsing options.

            :param annotation_type: The store's annotation type.
            :param format_to_header: The store's header key to column name mapping.
            :param schema: The schema of an annotation store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                # schema: Any
                
                tsv_store_options_property = omics.CfnAnnotationStore.TsvStoreOptionsProperty(
                    annotation_type="annotationType",
                    format_to_header={
                        "format_to_header_key": "formatToHeader"
                    },
                    schema=schema
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab0c74161d26d7206a33274b4f50b99292a52d11269613171afca62fe4a96842)
                check_type(argname="argument annotation_type", value=annotation_type, expected_type=type_hints["annotation_type"])
                check_type(argname="argument format_to_header", value=format_to_header, expected_type=type_hints["format_to_header"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if annotation_type is not None:
                self._values["annotation_type"] = annotation_type
            if format_to_header is not None:
                self._values["format_to_header"] = format_to_header
            if schema is not None:
                self._values["schema"] = schema

        @builtins.property
        def annotation_type(self) -> typing.Optional[builtins.str]:
            '''The store's annotation type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-annotationtype
            '''
            result = self._values.get("annotation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format_to_header(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The store's header key to column name mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-formattoheader
            '''
            result = self._values.get("format_to_header")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def schema(self) -> typing.Any:
            '''The schema of an annotation store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TsvStoreOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnAnnotationStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "store_format": "storeFormat",
        "description": "description",
        "reference": "reference",
        "sse_config": "sseConfig",
        "store_options": "storeOptions",
        "tags": "tags",
    },
)
class CfnAnnotationStoreProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        store_format: builtins.str,
        description: typing.Optional[builtins.str] = None,
        reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        sse_config: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        store_options: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAnnotationStore``.

        :param name: The name of the Annotation Store.
        :param store_format: The annotation file format of the store.
        :param description: A description for the store.
        :param reference: The genome reference for the store's annotations.
        :param sse_config: The store's server-side encryption (SSE) settings.
        :param store_options: File parsing options for the annotation store.
        :param tags: Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            # schema: Any
            
            cfn_annotation_store_props = omics.CfnAnnotationStoreProps(
                name="name",
                store_format="storeFormat",
            
                # the properties below are optional
                description="description",
                reference=omics.CfnAnnotationStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                ),
                sse_config=omics.CfnAnnotationStore.SseConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    key_arn="keyArn"
                ),
                store_options=omics.CfnAnnotationStore.StoreOptionsProperty(
                    tsv_store_options=omics.CfnAnnotationStore.TsvStoreOptionsProperty(
                        annotation_type="annotationType",
                        format_to_header={
                            "format_to_header_key": "formatToHeader"
                        },
                        schema=schema
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b449c9d9f77398e03723ebc58a99b58c11a180c7b5979d68cf84817dbc2b354a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument store_format", value=store_format, expected_type=type_hints["store_format"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument store_options", value=store_options, expected_type=type_hints["store_options"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "store_format": store_format,
        }
        if description is not None:
            self._values["description"] = description
        if reference is not None:
            self._values["reference"] = reference
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if store_options is not None:
            self._values["store_options"] = store_options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Annotation Store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def store_format(self) -> builtins.str:
        '''The annotation file format of the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeformat
        '''
        result = self._values.get("store_format")
        assert result is not None, "Required property 'store_format' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference(
        self,
    ) -> typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _IResolvable_a771d0ef]]:
        '''The genome reference for the store's annotations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-reference
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[CfnAnnotationStore.SseConfigProperty, _IResolvable_a771d0ef]]:
        '''The store's server-side encryption (SSE) settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[CfnAnnotationStore.SseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def store_options(
        self,
    ) -> typing.Optional[typing.Union[CfnAnnotationStore.StoreOptionsProperty, _IResolvable_a771d0ef]]:
        '''File parsing options for the annotation store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeoptions
        '''
        result = self._values.get("store_options")
        return typing.cast(typing.Optional[typing.Union[CfnAnnotationStore.StoreOptionsProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAnnotationStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnReferenceStore(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnReferenceStore",
):
    '''A CloudFormation ``AWS::Omics::ReferenceStore``.

    Creates a reference store.

    :cloudformationResource: AWS::Omics::ReferenceStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        cfn_reference_store = omics.CfnReferenceStore(self, "MyCfnReferenceStore",
            name="name",
        
            # the properties below are optional
            description="description",
            sse_config=omics.CfnReferenceStore.SseConfigProperty(
                type="type",
        
                # the properties below are optional
                key_arn="keyArn"
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union["CfnReferenceStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::ReferenceStore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the store.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7922ae1af3bd4d4b6930642c215b96f6fda74750670db9c6ccb0bde6e80ece)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReferenceStoreProps(
            name=name, description=description, sse_config=sse_config, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1715d8278d0c230d245b24fb53dcaf78ec64c1a9fbc2d30fc7bd5a04bdc42360)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa44a155e4ead81fae400b1ccb8d365f1361bcafb64e63b64fc7d779330665b)
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
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the store was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrReferenceStoreId")
    def attr_reference_store_id(self) -> builtins.str:
        '''The store's ID.

        :cloudformationAttribute: ReferenceStoreId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrReferenceStoreId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42b5e8cda2d154445b678621def5f57162ea55aabf2782b0f66786b8d8dc5479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02873e31bc062781de7b5d6135b9a0cf3a459278a51edd5b33b1fceea0f2d956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union["CfnReferenceStore.SseConfigProperty", _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnReferenceStore.SseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union["CfnReferenceStore.SseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9daa879d238ffcc6acf3b1637fcb398f583c42943b4b7648e8097b9e6858c44e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnReferenceStore.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "key_arn": "keyArn"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param type: The encryption type.
            :param key_arn: An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                sse_config_property = omics.CfnReferenceStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46ac4ec2b83cdd38ca00a320b54dc63dde59bb041e175047331f39220c65d39e)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''The encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html#cfn-omics-referencestore-sseconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-referencestore-sseconfig.html#cfn-omics-referencestore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnReferenceStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnReferenceStoreProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnReferenceStore``.

        :param name: A name for the store.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            cfn_reference_store_props = omics.CfnReferenceStoreProps(
                name="name",
            
                # the properties below are optional
                description="description",
                sse_config=omics.CfnReferenceStore.SseConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    key_arn="keyArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c394288527a0c00cb36871495a72b69935baa02e21ac2ad7b7697e737e95242)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[CfnReferenceStore.SseConfigProperty, _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[CfnReferenceStore.SseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReferenceStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRunGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnRunGroup",
):
    '''A CloudFormation ``AWS::Omics::RunGroup``.

    Creates a run group.

    :cloudformationResource: AWS::Omics::RunGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        cfn_run_group = omics.CfnRunGroup(self, "MyCfnRunGroup",
            max_cpus=123,
            max_duration=123,
            max_runs=123,
            name="name",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        max_cpus: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[jsii.Number] = None,
        max_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::RunGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param max_cpus: The group's maximum CPU count setting.
        :param max_duration: The group's maximum duration setting in minutes.
        :param max_runs: The group's maximum concurrent run setting.
        :param name: The group's name.
        :param tags: Tags for the group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff12d522e3d9e50c959036770170bff6b20fc60eb1689826f9e1f244a7e6b26)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRunGroupProps(
            max_cpus=max_cpus,
            max_duration=max_duration,
            max_runs=max_runs,
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc30751426ab2800819a8118e6f2d882e70e52ef2fb152ebb8879936f76c8f42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0f7e01b29a72a8d40f376dee167c59cd71f3ac56634b8f05b75eea014a5ba42)
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
        '''The run group's ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the run group was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The run group's ID.

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
        '''Tags for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="maxCpus")
    def max_cpus(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum CPU count setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxcpus
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxCpus"))

    @max_cpus.setter
    def max_cpus(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ad1b81cec4630ee27f19983a82c771402fc18e285304702beb800cdf746dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxCpus", value)

    @builtins.property
    @jsii.member(jsii_name="maxDuration")
    def max_duration(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum duration setting in minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxduration
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDuration"))

    @max_duration.setter
    def max_duration(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c69ffdeb0fc69918c7e5905554fdcf0fc9b84cab006c40a136ac8cc4ff0113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDuration", value)

    @builtins.property
    @jsii.member(jsii_name="maxRuns")
    def max_runs(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum concurrent run setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxruns
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxRuns"))

    @max_runs.setter
    def max_runs(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03aa9033a6228e7feb6a31f2fffec6a859095d8a8e382d0c648f7ffc95028dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxRuns", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The group's name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243f79f0b77c1e29b376382d36492189acf9128295efae3dd7c9691651ad7ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnRunGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "max_cpus": "maxCpus",
        "max_duration": "maxDuration",
        "max_runs": "maxRuns",
        "name": "name",
        "tags": "tags",
    },
)
class CfnRunGroupProps:
    def __init__(
        self,
        *,
        max_cpus: typing.Optional[jsii.Number] = None,
        max_duration: typing.Optional[jsii.Number] = None,
        max_runs: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRunGroup``.

        :param max_cpus: The group's maximum CPU count setting.
        :param max_duration: The group's maximum duration setting in minutes.
        :param max_runs: The group's maximum concurrent run setting.
        :param name: The group's name.
        :param tags: Tags for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            cfn_run_group_props = omics.CfnRunGroupProps(
                max_cpus=123,
                max_duration=123,
                max_runs=123,
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92adff1094c60c83434f9c02adca4d4920817b2e868c7938d0b95df25ebf9c6c)
            check_type(argname="argument max_cpus", value=max_cpus, expected_type=type_hints["max_cpus"])
            check_type(argname="argument max_duration", value=max_duration, expected_type=type_hints["max_duration"])
            check_type(argname="argument max_runs", value=max_runs, expected_type=type_hints["max_runs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_cpus is not None:
            self._values["max_cpus"] = max_cpus
        if max_duration is not None:
            self._values["max_duration"] = max_duration
        if max_runs is not None:
            self._values["max_runs"] = max_runs
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def max_cpus(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum CPU count setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxcpus
        '''
        result = self._values.get("max_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_duration(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum duration setting in minutes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxduration
        '''
        result = self._values.get("max_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_runs(self) -> typing.Optional[jsii.Number]:
        '''The group's maximum concurrent run setting.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-maxruns
        '''
        result = self._values.get("max_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The group's name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRunGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSequenceStore(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnSequenceStore",
):
    '''A CloudFormation ``AWS::Omics::SequenceStore``.

    Creates a sequence store.

    :cloudformationResource: AWS::Omics::SequenceStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        cfn_sequence_store = omics.CfnSequenceStore(self, "MyCfnSequenceStore",
            name="name",
        
            # the properties below are optional
            description="description",
            sse_config=omics.CfnSequenceStore.SseConfigProperty(
                type="type",
        
                # the properties below are optional
                key_arn="keyArn"
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union["CfnSequenceStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::SequenceStore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the store.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72127bf162e017e5ceaafd51814917cbbc3d8e9ef21875acf83367f170322e82)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSequenceStoreProps(
            name=name, description=description, sse_config=sse_config, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4a17fcd15e15649ee1ccc79a6fba0daac9adc76491d450560e11495baff101)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1e99f08b8682c8f403fa871f90942263bacd1a0deb87bdbdcab1353a5cfe2c0)
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
        '''The store's ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the store was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrSequenceStoreId")
    def attr_sequence_store_id(self) -> builtins.str:
        '''The store's ID.

        :cloudformationAttribute: SequenceStoreId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSequenceStoreId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5721ce41fea1e093b05f8a2576ee8fca3aa82c10cf31916caa2797e240c48b53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76303d6d5bebe4e37dbab57f31a06264f85592a09e1edd1fe690c62d4214fcf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union["CfnSequenceStore.SseConfigProperty", _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnSequenceStore.SseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union["CfnSequenceStore.SseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5eec4b052bb8fef2887654a32385c9f9f0e3d43308884435be06083d82a449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnSequenceStore.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "key_arn": "keyArn"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param type: The encryption type.
            :param key_arn: An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                sse_config_property = omics.CfnSequenceStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e31330503e0b3fe9e21ba599e3bdccbd23ceefa8a8395252f7d9bc2e62bc5666)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''The encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html#cfn-omics-sequencestore-sseconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-sequencestore-sseconfig.html#cfn-omics-sequencestore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnSequenceStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnSequenceStoreProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSequenceStore``.

        :param name: A name for the store.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            cfn_sequence_store_props = omics.CfnSequenceStoreProps(
                name="name",
            
                # the properties below are optional
                description="description",
                sse_config=omics.CfnSequenceStore.SseConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    key_arn="keyArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e8e541bcdbc2d80a0e4c16173241610f58ad15c81a81ae308217937a13fa51)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[CfnSequenceStore.SseConfigProperty, _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[CfnSequenceStore.SseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSequenceStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnVariantStore(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnVariantStore",
):
    '''A CloudFormation ``AWS::Omics::VariantStore``.

    Create a store for variant data.

    :cloudformationResource: AWS::Omics::VariantStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        cfn_variant_store = omics.CfnVariantStore(self, "MyCfnVariantStore",
            name="name",
            reference=omics.CfnVariantStore.ReferenceItemProperty(
                reference_arn="referenceArn"
            ),
        
            # the properties below are optional
            description="description",
            sse_config=omics.CfnVariantStore.SseConfigProperty(
                type="type",
        
                # the properties below are optional
                key_arn="keyArn"
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        reference: typing.Union[typing.Union["CfnVariantStore.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union["CfnVariantStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::VariantStore``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the store.
        :param reference: The genome reference for the store's variants.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b032300d88bb7441fdc83a89e6044d1284f24f0d79a523c937916692e8054772)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVariantStoreProps(
            name=name,
            reference=reference,
            description=description,
            sse_config=sse_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778616839a46728bd04d4b713706098b939f1b244357f7947560a66925184057)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ad5ae6f69d88932487c185fae3665695797583bce7b8024d35899808b0cee8d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the store was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The store's ID.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The store's status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''The store's status message.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStoreArn")
    def attr_store_arn(self) -> builtins.str:
        '''The store's ARN.

        :cloudformationAttribute: StoreArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStoreArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStoreSizeBytes")
    def attr_store_size_bytes(self) -> _IResolvable_a771d0ef:
        '''The store's size in bytes.

        :cloudformationAttribute: StoreSizeBytes
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrStoreSizeBytes"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateTime")
    def attr_update_time(self) -> builtins.str:
        '''When the store was updated.

        :cloudformationAttribute: UpdateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91491f212b6788f80dae97baa7462c7777c04940ea8a23375c0feacfbe9eac06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(
        self,
    ) -> typing.Union["CfnVariantStore.ReferenceItemProperty", _IResolvable_a771d0ef]:
        '''The genome reference for the store's variants.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-reference
        '''
        return typing.cast(typing.Union["CfnVariantStore.ReferenceItemProperty", _IResolvable_a771d0ef], jsii.get(self, "reference"))

    @reference.setter
    def reference(
        self,
        value: typing.Union["CfnVariantStore.ReferenceItemProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70c0c3c2a1cf34d59ede2db95c4ce6ff7db2d99307e14d5e405de52fa6ee1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reference", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec939dd7591df2784b3ae690006d285bfb9c52b65e8e5c58d47713142f35357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union["CfnVariantStore.SseConfigProperty", _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnVariantStore.SseConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union["CfnVariantStore.SseConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777d66dc212f5c9f8d7133b6e59dff3ed9afeb807f51f850668da33ef4eb44ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnVariantStore.ReferenceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class ReferenceItemProperty:
        def __init__(self, *, reference_arn: builtins.str) -> None:
            '''The read set's genome reference ARN.

            :param reference_arn: The reference's ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-referenceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                reference_item_property = omics.CfnVariantStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__249707d6f7f409a6b6a3f323dd24792b0ea27b8e86b44c438e36411d22d99eea)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "reference_arn": reference_arn,
            }

        @builtins.property
        def reference_arn(self) -> builtins.str:
            '''The reference's ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-referenceitem.html#cfn-omics-variantstore-referenceitem-referencearn
            '''
            result = self._values.get("reference_arn")
            assert result is not None, "Required property 'reference_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnVariantStore.SseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "key_arn": "keyArn"},
    )
    class SseConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Server-side encryption (SSE) settings for a store.

            :param type: The encryption type.
            :param key_arn: An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                sse_config_property = omics.CfnVariantStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bdcaafe6afadc010c0af625a9300d090e500faf0bfef3def31d70781e831bd3b)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def type(self) -> builtins.str:
            '''The encryption type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html#cfn-omics-variantstore-sseconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''An encryption key ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-variantstore-sseconfig.html#cfn-omics-variantstore-sseconfig-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnVariantStoreProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "reference": "reference",
        "description": "description",
        "sse_config": "sseConfig",
        "tags": "tags",
    },
)
class CfnVariantStoreProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        reference: typing.Union[typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVariantStore``.

        :param name: A name for the store.
        :param reference: The genome reference for the store's variants.
        :param description: A description for the store.
        :param sse_config: Server-side encryption (SSE) settings for the store.
        :param tags: Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            cfn_variant_store_props = omics.CfnVariantStoreProps(
                name="name",
                reference=omics.CfnVariantStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                ),
            
                # the properties below are optional
                description="description",
                sse_config=omics.CfnVariantStore.SseConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    key_arn="keyArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7924d6821ca6c24f7ad473531ff2796faabf5de9b138517925ddde38d357a5f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument sse_config", value=sse_config, expected_type=type_hints["sse_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "reference": reference,
        }
        if description is not None:
            self._values["description"] = description
        if sse_config is not None:
            self._values["sse_config"] = sse_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference(
        self,
    ) -> typing.Union[CfnVariantStore.ReferenceItemProperty, _IResolvable_a771d0ef]:
        '''The genome reference for the store's variants.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-reference
        '''
        result = self._values.get("reference")
        assert result is not None, "Required property 'reference' is missing"
        return typing.cast(typing.Union[CfnVariantStore.ReferenceItemProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[CfnVariantStore.SseConfigProperty, _IResolvable_a771d0ef]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[CfnVariantStore.SseConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVariantStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnWorkflow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_omics.CfnWorkflow",
):
    '''A CloudFormation ``AWS::Omics::Workflow``.

    Creates a workflow.

    :cloudformationResource: AWS::Omics::Workflow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_omics as omics
        
        cfn_workflow = omics.CfnWorkflow(self, "MyCfnWorkflow",
            definition_uri="definitionUri",
            description="description",
            engine="engine",
            main="main",
            name="name",
            parameter_template={
                "parameter_template_key": omics.CfnWorkflow.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            },
            storage_capacity=123,
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        definition_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        main: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameter_template: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnWorkflow.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        storage_capacity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Omics::Workflow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition_uri: The URI of a definition for the workflow.
        :param description: The parameter's description.
        :param engine: An engine for the workflow.
        :param main: The path of the main definition file for the workflow.
        :param name: The workflow's name.
        :param parameter_template: The workflow's parameter template.
        :param storage_capacity: A storage capacity for the workflow in gigabytes.
        :param tags: Tags for the workflow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1923e31e65931083da057e69bb5d2b2407c75a0bb405d84882cccefc6cd21ae)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkflowProps(
            definition_uri=definition_uri,
            description=description,
            engine=engine,
            main=main,
            name=name,
            parameter_template=parameter_template,
            storage_capacity=storage_capacity,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b69adbc0920598da7f4905b850295fde0c18a51788da642d4466d0659400aa7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3500c4a8928cd69ba2290639f438319b737faa2170b506ed03096090734e6f70)
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
        '''The ARN for the workflow.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''When the workflow was created.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The workflow's ID.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The workflow's status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> builtins.str:
        '''The workflow's type.

        :cloudformationAttribute: Type
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Tags for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definitionUri")
    def definition_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of a definition for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-definitionuri
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "definitionUri"))

    @definition_uri.setter
    def definition_uri(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7aa09b851d5b876416a399558b80f2addbad3f28fd37291c97e1174140ef9e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definitionUri", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The parameter's description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee68a89b1e68297fba6ecfd78db97dfe8d757e5dd074c30d12f33359670eea11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[builtins.str]:
        '''An engine for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-engine
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engine"))

    @engine.setter
    def engine(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a437e3b0311c49d38cd4a7dd17f9e14ef7ea79a0b50bb97ad2ff677aac62d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="main")
    def main(self) -> typing.Optional[builtins.str]:
        '''The path of the main definition file for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-main
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "main"))

    @main.setter
    def main(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af2c388d102813737d76c12227bb069474917e048f01d7b8695b52140a093b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "main", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The workflow's name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c4d72ca02f5b3831a882e5093d2f634385df1cfcb7ee69fc612a4415a8bdb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameterTemplate")
    def parameter_template(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnWorkflow.WorkflowParameterProperty", _IResolvable_a771d0ef]]]]:
        '''The workflow's parameter template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplate
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnWorkflow.WorkflowParameterProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "parameterTemplate"))

    @parameter_template.setter
    def parameter_template(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnWorkflow.WorkflowParameterProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd61094242c9b6659ae601f6c5c07830392dc7c67803305f0661db466375b7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameterTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="storageCapacity")
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        '''A storage capacity for the workflow in gigabytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-storagecapacity
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "storageCapacity"))

    @storage_capacity.setter
    def storage_capacity(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc812a93fec3e47ce6810353548f9426f3b257c46e0c06d8b4d96c1421380272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCapacity", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_omics.CfnWorkflow.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "optional": "optional"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            optional: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A workflow parameter.

            :param description: The parameter's description.
            :param optional: Whether the parameter is optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_omics as omics
                
                workflow_parameter_property = omics.CfnWorkflow.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72649e68c878f8429aea70a9982805930fe94e27681415231be64d39c340f1f3)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if optional is not None:
                self._values["optional"] = optional

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The parameter's description.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html#cfn-omics-workflow-workflowparameter-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def optional(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether the parameter is optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html#cfn-omics-workflow-workflowparameter-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_omics.CfnWorkflowProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition_uri": "definitionUri",
        "description": "description",
        "engine": "engine",
        "main": "main",
        "name": "name",
        "parameter_template": "parameterTemplate",
        "storage_capacity": "storageCapacity",
        "tags": "tags",
    },
)
class CfnWorkflowProps:
    def __init__(
        self,
        *,
        definition_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        main: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameter_template: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        storage_capacity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkflow``.

        :param definition_uri: The URI of a definition for the workflow.
        :param description: The parameter's description.
        :param engine: An engine for the workflow.
        :param main: The path of the main definition file for the workflow.
        :param name: The workflow's name.
        :param parameter_template: The workflow's parameter template.
        :param storage_capacity: A storage capacity for the workflow in gigabytes.
        :param tags: Tags for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_omics as omics
            
            cfn_workflow_props = omics.CfnWorkflowProps(
                definition_uri="definitionUri",
                description="description",
                engine="engine",
                main="main",
                name="name",
                parameter_template={
                    "parameter_template_key": omics.CfnWorkflow.WorkflowParameterProperty(
                        description="description",
                        optional=False
                    )
                },
                storage_capacity=123,
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117d85ad66eb92caf5d6fbafed16b75cbeed43b73d4db8dede6edeeeb55af7fd)
            check_type(argname="argument definition_uri", value=definition_uri, expected_type=type_hints["definition_uri"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine", value=engine, expected_type=type_hints["engine"])
            check_type(argname="argument main", value=main, expected_type=type_hints["main"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameter_template", value=parameter_template, expected_type=type_hints["parameter_template"])
            check_type(argname="argument storage_capacity", value=storage_capacity, expected_type=type_hints["storage_capacity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if definition_uri is not None:
            self._values["definition_uri"] = definition_uri
        if description is not None:
            self._values["description"] = description
        if engine is not None:
            self._values["engine"] = engine
        if main is not None:
            self._values["main"] = main
        if name is not None:
            self._values["name"] = name
        if parameter_template is not None:
            self._values["parameter_template"] = parameter_template
        if storage_capacity is not None:
            self._values["storage_capacity"] = storage_capacity
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def definition_uri(self) -> typing.Optional[builtins.str]:
        '''The URI of a definition for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-definitionuri
        '''
        result = self._values.get("definition_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The parameter's description.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine(self) -> typing.Optional[builtins.str]:
        '''An engine for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-engine
        '''
        result = self._values.get("engine")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def main(self) -> typing.Optional[builtins.str]:
        '''The path of the main definition file for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-main
        '''
        result = self._values.get("main")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The workflow's name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_template(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnWorkflow.WorkflowParameterProperty, _IResolvable_a771d0ef]]]]:
        '''The workflow's parameter template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplate
        '''
        result = self._values.get("parameter_template")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnWorkflow.WorkflowParameterProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        '''A storage capacity for the workflow in gigabytes.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-storagecapacity
        '''
        result = self._values.get("storage_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAnnotationStore",
    "CfnAnnotationStoreProps",
    "CfnReferenceStore",
    "CfnReferenceStoreProps",
    "CfnRunGroup",
    "CfnRunGroupProps",
    "CfnSequenceStore",
    "CfnSequenceStoreProps",
    "CfnVariantStore",
    "CfnVariantStoreProps",
    "CfnWorkflow",
    "CfnWorkflowProps",
]

publication.publish()

def _typecheckingstub__0b4ae2ffa77c36ed1fa9592aaeab76900ec05ec67ab11c4af7fc4727f56a144d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    store_format: builtins.str,
    description: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    store_options: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959834183560fa8a26d8c72c86ee1e1ece4a5cd127fb3947a9c1dc12c4d24e7d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aae7204020c44ed955f41659b4fccbef4c5b210377217f8c22dd0a7f53145f9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae3cc3c52237c6c85eb1e345d9aba18ba06d8537175d34575d6fb840af8887f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0d68bc30808877b2a05c6e45a818af998111431191ac73455e29eddcb1c505(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb52d7c171ec363bd21241d8d1d7b83ba390070a85fe2a1978d49b625a46def(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1e21ac28126977918057b96a4a20efc9a65b082970fa2596332487ba9b7cc7(
    value: typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698939df3768f6f06d68aaf5859ef486bf8bf98662d4f212bf2e041dc244d6f9(
    value: typing.Optional[typing.Union[CfnAnnotationStore.SseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510610ce7dd94ac10ed4c972d72bb289119af0609275db39dba6525ab09a164a(
    value: typing.Optional[typing.Union[CfnAnnotationStore.StoreOptionsProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382b433547b1a0879c1fecf9f6f5988a2b8a561dc610c310c72c40fd6cc637ef(
    *,
    reference_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464cc5a0c13ed5ccd5549b513ac550553344a818e8829b653925e478124f4cdb(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eda8b007ef4afac56d0f10f706e514831b985b2d6f05812412f9e0e6056070c(
    *,
    tsv_store_options: typing.Union[typing.Union[CfnAnnotationStore.TsvStoreOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab0c74161d26d7206a33274b4f50b99292a52d11269613171afca62fe4a96842(
    *,
    annotation_type: typing.Optional[builtins.str] = None,
    format_to_header: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    schema: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b449c9d9f77398e03723ebc58a99b58c11a180c7b5979d68cf84817dbc2b354a(
    *,
    name: builtins.str,
    store_format: builtins.str,
    description: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    store_options: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7922ae1af3bd4d4b6930642c215b96f6fda74750670db9c6ccb0bde6e80ece(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1715d8278d0c230d245b24fb53dcaf78ec64c1a9fbc2d30fc7bd5a04bdc42360(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa44a155e4ead81fae400b1ccb8d365f1361bcafb64e63b64fc7d779330665b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b5e8cda2d154445b678621def5f57162ea55aabf2782b0f66786b8d8dc5479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02873e31bc062781de7b5d6135b9a0cf3a459278a51edd5b33b1fceea0f2d956(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daa879d238ffcc6acf3b1637fcb398f583c42943b4b7648e8097b9e6858c44e(
    value: typing.Optional[typing.Union[CfnReferenceStore.SseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ac4ec2b83cdd38ca00a320b54dc63dde59bb041e175047331f39220c65d39e(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c394288527a0c00cb36871495a72b69935baa02e21ac2ad7b7697e737e95242(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff12d522e3d9e50c959036770170bff6b20fc60eb1689826f9e1f244a7e6b26(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    max_cpus: typing.Optional[jsii.Number] = None,
    max_duration: typing.Optional[jsii.Number] = None,
    max_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc30751426ab2800819a8118e6f2d882e70e52ef2fb152ebb8879936f76c8f42(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0f7e01b29a72a8d40f376dee167c59cd71f3ac56634b8f05b75eea014a5ba42(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ad1b81cec4630ee27f19983a82c771402fc18e285304702beb800cdf746dca(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c69ffdeb0fc69918c7e5905554fdcf0fc9b84cab006c40a136ac8cc4ff0113(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03aa9033a6228e7feb6a31f2fffec6a859095d8a8e382d0c648f7ffc95028dfc(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243f79f0b77c1e29b376382d36492189acf9128295efae3dd7c9691651ad7ed0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92adff1094c60c83434f9c02adca4d4920817b2e868c7938d0b95df25ebf9c6c(
    *,
    max_cpus: typing.Optional[jsii.Number] = None,
    max_duration: typing.Optional[jsii.Number] = None,
    max_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72127bf162e017e5ceaafd51814917cbbc3d8e9ef21875acf83367f170322e82(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4a17fcd15e15649ee1ccc79a6fba0daac9adc76491d450560e11495baff101(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1e99f08b8682c8f403fa871f90942263bacd1a0deb87bdbdcab1353a5cfe2c0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5721ce41fea1e093b05f8a2576ee8fca3aa82c10cf31916caa2797e240c48b53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76303d6d5bebe4e37dbab57f31a06264f85592a09e1edd1fe690c62d4214fcf1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5eec4b052bb8fef2887654a32385c9f9f0e3d43308884435be06083d82a449(
    value: typing.Optional[typing.Union[CfnSequenceStore.SseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31330503e0b3fe9e21ba599e3bdccbd23ceefa8a8395252f7d9bc2e62bc5666(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e8e541bcdbc2d80a0e4c16173241610f58ad15c81a81ae308217937a13fa51(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b032300d88bb7441fdc83a89e6044d1284f24f0d79a523c937916692e8054772(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    reference: typing.Union[typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778616839a46728bd04d4b713706098b939f1b244357f7947560a66925184057(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad5ae6f69d88932487c185fae3665695797583bce7b8024d35899808b0cee8d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91491f212b6788f80dae97baa7462c7777c04940ea8a23375c0feacfbe9eac06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70c0c3c2a1cf34d59ede2db95c4ce6ff7db2d99307e14d5e405de52fa6ee1df(
    value: typing.Union[CfnVariantStore.ReferenceItemProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec939dd7591df2784b3ae690006d285bfb9c52b65e8e5c58d47713142f35357(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777d66dc212f5c9f8d7133b6e59dff3ed9afeb807f51f850668da33ef4eb44ce(
    value: typing.Optional[typing.Union[CfnVariantStore.SseConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__249707d6f7f409a6b6a3f323dd24792b0ea27b8e86b44c438e36411d22d99eea(
    *,
    reference_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdcaafe6afadc010c0af625a9300d090e500faf0bfef3def31d70781e831bd3b(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7924d6821ca6c24f7ad473531ff2796faabf5de9b138517925ddde38d357a5f(
    *,
    name: builtins.str,
    reference: typing.Union[typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1923e31e65931083da057e69bb5d2b2407c75a0bb405d84882cccefc6cd21ae(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b69adbc0920598da7f4905b850295fde0c18a51788da642d4466d0659400aa7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3500c4a8928cd69ba2290639f438319b737faa2170b506ed03096090734e6f70(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7aa09b851d5b876416a399558b80f2addbad3f28fd37291c97e1174140ef9e6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee68a89b1e68297fba6ecfd78db97dfe8d757e5dd074c30d12f33359670eea11(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a437e3b0311c49d38cd4a7dd17f9e14ef7ea79a0b50bb97ad2ff677aac62d77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2c388d102813737d76c12227bb069474917e048f01d7b8695b52140a093b8e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c4d72ca02f5b3831a882e5093d2f634385df1cfcb7ee69fc612a4415a8bdb3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd61094242c9b6659ae601f6c5c07830392dc7c67803305f0661db466375b7d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnWorkflow.WorkflowParameterProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc812a93fec3e47ce6810353548f9426f3b257c46e0c06d8b4d96c1421380272(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72649e68c878f8429aea70a9982805930fe94e27681415231be64d39c340f1f3(
    *,
    description: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117d85ad66eb92caf5d6fbafed16b75cbeed43b73d4db8dede6edeeeb55af7fd(
    *,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
