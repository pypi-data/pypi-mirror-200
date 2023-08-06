'''
# AWS::Omics Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_omics as omics
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAnnotationStore(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnAnnotationStore",
):
    '''A CloudFormation ``AWS::Omics::AnnotationStore``.

    Creates an annotation store.

    :cloudformationResource: AWS::Omics::AnnotationStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        store_format: builtins.str,
        description: typing.Optional[builtins.str] = None,
        reference: typing.Optional[typing.Union[typing.Union["CfnAnnotationStore.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAnnotationStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        store_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAnnotationStore.StoreOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__72f682fa301896371fe38279ac5738eb104d98a4fe62a47e953315c1951f1900)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aeb5728fdbd61e617b1255a8808261ab871bc7a31d20791912e614a361c5ebc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fda7a80559c0162e876b5823726e4c61e080623e5ea78b58504da5eeef03bf6f)
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
    def attr_store_size_bytes(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The store's size in bytes.

        :cloudformationAttribute: StoreSizeBytes
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrStoreSizeBytes"))

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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c85292ec5ff283a5e1a2b15537ffecd5908f48d3f121166dab1c61b85806c35e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4de4227a348d5b1286788ba6c26a21c7a285afcf5abc51d138a9f095e5ba8b4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4da4575951a3a161eca4e75d628a898fe4aa49dd8b393f98973968e010044e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(
        self,
    ) -> typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The genome reference for the store's annotations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-reference
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "reference"))

    @reference.setter
    def reference(
        self,
        value: typing.Optional[typing.Union["CfnAnnotationStore.ReferenceItemProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7e1897efb306aeb2d89068270f41c58ae000dc17131afb5681537bd9717a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reference", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.SseConfigProperty"]]:
        '''The store's server-side encryption (SSE) settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.SseConfigProperty"]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.SseConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21921780ecb77da47d5822d219397e7a71fb9eb5b0a8415035bcd5b4bc1e532a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="storeOptions")
    def store_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.StoreOptionsProperty"]]:
        '''File parsing options for the annotation store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.StoreOptionsProperty"]], jsii.get(self, "storeOptions"))

    @store_options.setter
    def store_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.StoreOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051ea7afc58dc00c80899b632900e5a96e026b65862a4b5014893e2b543be3c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storeOptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnAnnotationStore.ReferenceItemProperty",
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
                import aws_cdk.aws_omics as omics
                
                reference_item_property = omics.CfnAnnotationStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7ce989c23637945ecf1f8fedfcd263604dd2fc4c360974ac5fb4b815b4f0c56)
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
        jsii_type="@aws-cdk/aws-omics.CfnAnnotationStore.SseConfigProperty",
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
                import aws_cdk.aws_omics as omics
                
                sse_config_property = omics.CfnAnnotationStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83bf15ffb4231ed8109f19a2689e57eab1e286c1eeb459833439401207eef891)
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
        jsii_type="@aws-cdk/aws-omics.CfnAnnotationStore.StoreOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"tsv_store_options": "tsvStoreOptions"},
    )
    class StoreOptionsProperty:
        def __init__(
            self,
            *,
            tsv_store_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnAnnotationStore.TsvStoreOptionsProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The store's file parsing options.

            :param tsv_store_options: Formatting options for a TSV file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_omics as omics
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__5ca7bfeacbc32bcd7f21b96d98f1cc74618fd280ae521a4cc77dc9cfe9a6cb57)
                check_type(argname="argument tsv_store_options", value=tsv_store_options, expected_type=type_hints["tsv_store_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "tsv_store_options": tsv_store_options,
            }

        @builtins.property
        def tsv_store_options(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.TsvStoreOptionsProperty"]:
            '''Formatting options for a TSV file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-storeoptions.html#cfn-omics-annotationstore-storeoptions-tsvstoreoptions
            '''
            result = self._values.get("tsv_store_options")
            assert result is not None, "Required property 'tsv_store_options' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnAnnotationStore.TsvStoreOptionsProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StoreOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnAnnotationStore.TsvStoreOptionsProperty",
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
            format_to_header: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
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
                import aws_cdk.aws_omics as omics
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__b60c041e2891810900474cab15d7fb495c32bcaf079bd08eb0bbd0810acfb9bc)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The store's header key to column name mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-annotationstore-tsvstoreoptions.html#cfn-omics-annotationstore-tsvstoreoptions-formattoheader
            '''
            result = self._values.get("format_to_header")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

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
    jsii_type="@aws-cdk/aws-omics.CfnAnnotationStoreProps",
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
        reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        store_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d4ea62fba0c68cb8ab6ab43348d70941d200d9f195411efd20c56fea312930)
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
    ) -> typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The genome reference for the store's annotations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-reference
        '''
        result = self._values.get("reference")
        return typing.cast(typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.SseConfigProperty]]:
        '''The store's server-side encryption (SSE) settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.SseConfigProperty]], result)

    @builtins.property
    def store_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.StoreOptionsProperty]]:
        '''File parsing options for the annotation store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-annotationstore.html#cfn-omics-annotationstore-storeoptions
        '''
        result = self._values.get("store_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.StoreOptionsProperty]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReferenceStore(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnReferenceStore",
):
    '''A CloudFormation ``AWS::Omics::ReferenceStore``.

    Creates a reference store.

    :cloudformationResource: AWS::Omics::ReferenceStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReferenceStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9304170f0382828a9a413a6dd3ea14dbde7c3c8e120f143095140b02fa07c46)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReferenceStoreProps(
            name=name, description=description, sse_config=sse_config, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fafc1dcb49239a04550b22238e95d3567fcfed08158ed489c49c8af9a85f7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ff278bc2e286611efcf6d4b71f097134ed9d70c5f524d60e4adcaa7cd09133c)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b090a21fd8f4e61d5a40671eb2f1252e7eb2b17399ec25d3c86d7ac8c037b15b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c57583a6f44f73cbb6eed3b92d337d192778d8ffc01272824a1c4dce9c4184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReferenceStore.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReferenceStore.SseConfigProperty"]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReferenceStore.SseConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0e741b0fe98e25299c577cc35977d3a6c96c31c6ba4aea61e00be4e7fa64e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnReferenceStore.SseConfigProperty",
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
                import aws_cdk.aws_omics as omics
                
                sse_config_property = omics.CfnReferenceStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__558e0e5cbacc0609e725aebeb4157bc17f1cacd736b00e4a4464146d8aef9719)
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
    jsii_type="@aws-cdk/aws-omics.CfnReferenceStoreProps",
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
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__139e1cbac82aa7851bc5c623d42047011c0f4980f57ec321044169a54838e5c4)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReferenceStore.SseConfigProperty]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-referencestore.html#cfn-omics-referencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReferenceStore.SseConfigProperty]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRunGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnRunGroup",
):
    '''A CloudFormation ``AWS::Omics::RunGroup``.

    Creates a run group.

    :cloudformationResource: AWS::Omics::RunGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a9a5a98db6f89cebb6d3e3797a9d3e1ea583bb03127fce2f64de485a8e3c69e)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb99e995f8031f608ea1801028ebea25aef3b92b52861f04f9f971b244cd5d69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00d1c18ba8aebb855cae9239ed981579ae106de7e767f766053832f69a9807c)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-rungroup.html#cfn-omics-rungroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__50941fef6d08bf9cb27ca7d1ac9e08b181a41a7c1e0eb7efe411342f3ea36c90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5106f7ee671d49843d31e6d0ce7f236c2a8e128b6436a39234b536c4304aee9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed6c48bbc7f41e5f259a90b9bb50f3a2b1b5246dbf069227f67d5eea2fb01e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1d729fd0d69eae6b5b136a6916e8560950397b665d83e44b1341a8691acba23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-omics.CfnRunGroupProps",
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb728a0168039acc9581626f9ae80f778cb14db4224b78a0c6e214c5944ff260)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSequenceStore(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnSequenceStore",
):
    '''A CloudFormation ``AWS::Omics::SequenceStore``.

    Creates a sequence store.

    :cloudformationResource: AWS::Omics::SequenceStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSequenceStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__03a5a4ceeb77dcbdd9b9c68fe96176dd880a3880627fecddc5b9d21377b72d73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSequenceStoreProps(
            name=name, description=description, sse_config=sse_config, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d869538a0c9916f1a41207a6abbc1ffcceead331da67b728bf04b894caacbd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78e3f441ad37d65d76fcc984228f18e42818165bb04fb67fe91a70cb25b57ed9)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ff30e048a3f18708611975cc37ad399c0279d54056de31ce0599cf470612a749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d8b613f420622cafe6def57383d5e9dd3bb9e733d6fff9feb2e0dac7b7f759f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSequenceStore.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSequenceStore.SseConfigProperty"]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSequenceStore.SseConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de56e052e59f5c062cc6471f68e60aeeccdafebe9dcc134429d0dfee6394eb51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnSequenceStore.SseConfigProperty",
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
                import aws_cdk.aws_omics as omics
                
                sse_config_property = omics.CfnSequenceStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__434cb83a4335540890c65a2912cef2eb53f95f0620758d13b38e163b81b33abd)
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
    jsii_type="@aws-cdk/aws-omics.CfnSequenceStoreProps",
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
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9bec31558393fd84b2c62ba38dfbfbd035a8a120493f460a3a250394662ecf7)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSequenceStore.SseConfigProperty]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-sequencestore.html#cfn-omics-sequencestore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSequenceStore.SseConfigProperty]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVariantStore(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnVariantStore",
):
    '''A CloudFormation ``AWS::Omics::VariantStore``.

    Create a store for variant data.

    :cloudformationResource: AWS::Omics::VariantStore
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        reference: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVariantStore.ReferenceItemProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVariantStore.SseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2904d834bb9f47653f7877320e3fa45e28122e79474c8a8f37461205b4e088d)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42159fba815e68de19f316433e6b5a08347ebadb3e5817159e68a353f34c7daf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2885c3bd47cc2c995f72656d45f05dad90e80043b8aebd9342994e2a4924bafc)
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
    def attr_store_size_bytes(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''The store's size in bytes.

        :cloudformationAttribute: StoreSizeBytes
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrStoreSizeBytes"))

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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e0325c7a6540283d5262cbfdb3441839ab482805fabdcfda137b6131be8360f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.ReferenceItemProperty"]:
        '''The genome reference for the store's variants.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-reference
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.ReferenceItemProperty"], jsii.get(self, "reference"))

    @reference.setter
    def reference(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.ReferenceItemProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b094ed062b5d363c0ff7c905fe6e99b16c0746800f0ee709d9f97473fdee5b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2457dd9e007189579a10b21d6adf2744944d32249f27a499291f999e78fa52ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sseConfig")
    def sse_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.SseConfigProperty"]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-sseconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.SseConfigProperty"]], jsii.get(self, "sseConfig"))

    @sse_config.setter
    def sse_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVariantStore.SseConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca0ec5440b13cea48858f48b2b1b9454f36520b188c890b16502fad4cac75ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sseConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnVariantStore.ReferenceItemProperty",
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
                import aws_cdk.aws_omics as omics
                
                reference_item_property = omics.CfnVariantStore.ReferenceItemProperty(
                    reference_arn="referenceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e20e455412420272dca96c402da5b28e8a2a11c35ed26bee827097dfe1fb23b4)
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
        jsii_type="@aws-cdk/aws-omics.CfnVariantStore.SseConfigProperty",
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
                import aws_cdk.aws_omics as omics
                
                sse_config_property = omics.CfnVariantStore.SseConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__658ae7d77c40d079b27d0ecab9165eaacbcf4067e1dbcb14b25593a6cfc1dc84)
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
    jsii_type="@aws-cdk/aws-omics.CfnVariantStoreProps",
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
        reference: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
        sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d59b1eb164ac8933030aa62d9e42371885576487fe6cd2618978a296f6ee89)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.ReferenceItemProperty]:
        '''The genome reference for the store's variants.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-reference
        '''
        result = self._values.get("reference")
        assert result is not None, "Required property 'reference' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.ReferenceItemProperty], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.SseConfigProperty]]:
        '''Server-side encryption (SSE) settings for the store.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-variantstore.html#cfn-omics-variantstore-sseconfig
        '''
        result = self._values.get("sse_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.SseConfigProperty]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnWorkflow(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-omics.CfnWorkflow",
):
    '''A CloudFormation ``AWS::Omics::Workflow``.

    Creates a workflow.

    :cloudformationResource: AWS::Omics::Workflow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_omics as omics
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        definition_uri: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        engine: typing.Optional[builtins.str] = None,
        main: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parameter_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnWorkflow.WorkflowParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3159e4a9122909749859c0c2c9e98492d55e7494271ef99656fc75b72536b52)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382a909a732f5dc8030df9cfae68304b331309bd06aabee51c0772a9dc50bad4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b10bbe8bb2ba007eb376b26fe3f04295d4a5ebbcf72908da561a12ef1f71600)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags for the workflow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__27492828706c3922484d12b27a0cf4cd1ec0598bfe524f88c87c2f5faea8d706)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc58ee25c2af560ea957a10889505a7205632bb204a532b94bf5f5a1f0df7cce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f99fd0b2b543febe48fb99f20f6cdee9df3b3e0d316777a802cde213b47b6ce4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__309ababb84088222ba252fb6b2830bf01035d31ea9711edd1d26b07bdd531474)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d99be7150a8cbc99217505367e3dc16ab2b87e945cc3f17c282cc4c46454411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parameterTemplate")
    def parameter_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkflow.WorkflowParameterProperty"]]]]:
        '''The workflow's parameter template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplate
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkflow.WorkflowParameterProperty"]]]], jsii.get(self, "parameterTemplate"))

    @parameter_template.setter
    def parameter_template(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnWorkflow.WorkflowParameterProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd437918f91cc9abe6743e4fbc20db9b9be0f9f479b9cf19a12bcc06b5c5169)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f7da7b165be8531031f3a0c8510fbaeebeb8f7f4b02fb61aac50529cdaef278)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCapacity", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-omics.CfnWorkflow.WorkflowParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"description": "description", "optional": "optional"},
    )
    class WorkflowParameterProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''A workflow parameter.

            :param description: The parameter's description.
            :param optional: Whether the parameter is optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_omics as omics
                
                workflow_parameter_property = omics.CfnWorkflow.WorkflowParameterProperty(
                    description="description",
                    optional=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e582f58264cd9ee90ebee9bb5738c7cdb2b27acbd539c6761709b566256d0c1)
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
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Whether the parameter is optional.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-omics-workflow-workflowparameter.html#cfn-omics-workflow-workflowparameter-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-omics.CfnWorkflowProps",
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
        parameter_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            import aws_cdk.aws_omics as omics
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__457c31dd185891848f6c6b21f5196b024eb482a8259aaa5679ed9565940e8f06)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkflow.WorkflowParameterProperty]]]]:
        '''The workflow's parameter template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-omics-workflow.html#cfn-omics-workflow-parametertemplate
        '''
        result = self._values.get("parameter_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkflow.WorkflowParameterProperty]]]], result)

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

def _typecheckingstub__72f682fa301896371fe38279ac5738eb104d98a4fe62a47e953315c1951f1900(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    store_format: builtins.str,
    description: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    store_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aeb5728fdbd61e617b1255a8808261ab871bc7a31d20791912e614a361c5ebc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fda7a80559c0162e876b5823726e4c61e080623e5ea78b58504da5eeef03bf6f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c85292ec5ff283a5e1a2b15537ffecd5908f48d3f121166dab1c61b85806c35e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de4227a348d5b1286788ba6c26a21c7a285afcf5abc51d138a9f095e5ba8b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4da4575951a3a161eca4e75d628a898fe4aa49dd8b393f98973968e010044e1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7e1897efb306aeb2d89068270f41c58ae000dc17131afb5681537bd9717a04(
    value: typing.Optional[typing.Union[CfnAnnotationStore.ReferenceItemProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21921780ecb77da47d5822d219397e7a71fb9eb5b0a8415035bcd5b4bc1e532a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.SseConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051ea7afc58dc00c80899b632900e5a96e026b65862a4b5014893e2b543be3c2(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnAnnotationStore.StoreOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ce989c23637945ecf1f8fedfcd263604dd2fc4c360974ac5fb4b815b4f0c56(
    *,
    reference_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83bf15ffb4231ed8109f19a2689e57eab1e286c1eeb459833439401207eef891(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca7bfeacbc32bcd7f21b96d98f1cc74618fd280ae521a4cc77dc9cfe9a6cb57(
    *,
    tsv_store_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.TsvStoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60c041e2891810900474cab15d7fb495c32bcaf079bd08eb0bbd0810acfb9bc(
    *,
    annotation_type: typing.Optional[builtins.str] = None,
    format_to_header: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    schema: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d4ea62fba0c68cb8ab6ab43348d70941d200d9f195411efd20c56fea312930(
    *,
    name: builtins.str,
    store_format: builtins.str,
    description: typing.Optional[builtins.str] = None,
    reference: typing.Optional[typing.Union[typing.Union[CfnAnnotationStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    store_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnAnnotationStore.StoreOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9304170f0382828a9a413a6dd3ea14dbde7c3c8e120f143095140b02fa07c46(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fafc1dcb49239a04550b22238e95d3567fcfed08158ed489c49c8af9a85f7b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff278bc2e286611efcf6d4b71f097134ed9d70c5f524d60e4adcaa7cd09133c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b090a21fd8f4e61d5a40671eb2f1252e7eb2b17399ec25d3c86d7ac8c037b15b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c57583a6f44f73cbb6eed3b92d337d192778d8ffc01272824a1c4dce9c4184(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0e741b0fe98e25299c577cc35977d3a6c96c31c6ba4aea61e00be4e7fa64e1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReferenceStore.SseConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__558e0e5cbacc0609e725aebeb4157bc17f1cacd736b00e4a4464146d8aef9719(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139e1cbac82aa7851bc5c623d42047011c0f4980f57ec321044169a54838e5c4(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReferenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9a5a98db6f89cebb6d3e3797a9d3e1ea583bb03127fce2f64de485a8e3c69e(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__fb99e995f8031f608ea1801028ebea25aef3b92b52861f04f9f971b244cd5d69(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00d1c18ba8aebb855cae9239ed981579ae106de7e767f766053832f69a9807c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50941fef6d08bf9cb27ca7d1ac9e08b181a41a7c1e0eb7efe411342f3ea36c90(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5106f7ee671d49843d31e6d0ce7f236c2a8e128b6436a39234b536c4304aee9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed6c48bbc7f41e5f259a90b9bb50f3a2b1b5246dbf069227f67d5eea2fb01e0(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d729fd0d69eae6b5b136a6916e8560950397b665d83e44b1341a8691acba23(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb728a0168039acc9581626f9ae80f778cb14db4224b78a0c6e214c5944ff260(
    *,
    max_cpus: typing.Optional[jsii.Number] = None,
    max_duration: typing.Optional[jsii.Number] = None,
    max_runs: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03a5a4ceeb77dcbdd9b9c68fe96176dd880a3880627fecddc5b9d21377b72d73(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d869538a0c9916f1a41207a6abbc1ffcceead331da67b728bf04b894caacbd0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e3f441ad37d65d76fcc984228f18e42818165bb04fb67fe91a70cb25b57ed9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff30e048a3f18708611975cc37ad399c0279d54056de31ce0599cf470612a749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d8b613f420622cafe6def57383d5e9dd3bb9e733d6fff9feb2e0dac7b7f759f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de56e052e59f5c062cc6471f68e60aeeccdafebe9dcc134429d0dfee6394eb51(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSequenceStore.SseConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434cb83a4335540890c65a2912cef2eb53f95f0620758d13b38e163b81b33abd(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9bec31558393fd84b2c62ba38dfbfbd035a8a120493f460a3a250394662ecf7(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSequenceStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2904d834bb9f47653f7877320e3fa45e28122e79474c8a8f37461205b4e088d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    reference: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42159fba815e68de19f316433e6b5a08347ebadb3e5817159e68a353f34c7daf(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2885c3bd47cc2c995f72656d45f05dad90e80043b8aebd9342994e2a4924bafc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0325c7a6540283d5262cbfdb3441839ab482805fabdcfda137b6131be8360f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b094ed062b5d363c0ff7c905fe6e99b16c0746800f0ee709d9f97473fdee5b9(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.ReferenceItemProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2457dd9e007189579a10b21d6adf2744944d32249f27a499291f999e78fa52ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca0ec5440b13cea48858f48b2b1b9454f36520b188c890b16502fad4cac75ac(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVariantStore.SseConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e20e455412420272dca96c402da5b28e8a2a11c35ed26bee827097dfe1fb23b4(
    *,
    reference_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658ae7d77c40d079b27d0ecab9165eaacbcf4067e1dbcb14b25593a6cfc1dc84(
    *,
    type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d59b1eb164ac8933030aa62d9e42371885576487fe6cd2618978a296f6ee89(
    *,
    name: builtins.str,
    reference: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.ReferenceItemProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
    sse_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVariantStore.SseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3159e4a9122909749859c0c2c9e98492d55e7494271ef99656fc75b72536b52(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382a909a732f5dc8030df9cfae68304b331309bd06aabee51c0772a9dc50bad4(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b10bbe8bb2ba007eb376b26fe3f04295d4a5ebbcf72908da561a12ef1f71600(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27492828706c3922484d12b27a0cf4cd1ec0598bfe524f88c87c2f5faea8d706(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc58ee25c2af560ea957a10889505a7205632bb204a532b94bf5f5a1f0df7cce(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99fd0b2b543febe48fb99f20f6cdee9df3b3e0d316777a802cde213b47b6ce4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309ababb84088222ba252fb6b2830bf01035d31ea9711edd1d26b07bdd531474(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d99be7150a8cbc99217505367e3dc16ab2b87e945cc3f17c282cc4c46454411(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd437918f91cc9abe6743e4fbc20db9b9be0f9f479b9cf19a12bcc06b5c5169(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnWorkflow.WorkflowParameterProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f7da7b165be8531031f3a0c8510fbaeebeb8f7f4b02fb61aac50529cdaef278(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e582f58264cd9ee90ebee9bb5738c7cdb2b27acbd539c6761709b566256d0c1(
    *,
    description: typing.Optional[builtins.str] = None,
    optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457c31dd185891848f6c6b21f5196b024eb482a8259aaa5679ed9565940e8f06(
    *,
    definition_uri: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    engine: typing.Optional[builtins.str] = None,
    main: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parameter_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnWorkflow.WorkflowParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
