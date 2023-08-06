'''
# AWS::IVSChat Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ivschat as ivschat
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLoggingConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfiguration",
):
    '''A CloudFormation ``AWS::IVSChat::LoggingConfiguration``.

    The ``AWS::IVSChat::LoggingConfiguration`` resource specifies an  logging configuration that allows clients to store and record sent messages. For more information, see `CreateLoggingConfiguration <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateLoggingConfiguration.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :cloudformationResource: AWS::IVSChat::LoggingConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivschat as ivschat
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        destination_configuration: typing.Union[typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVSChat::LoggingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_configuration: The DestinationConfiguration is a complex type that contains information about where chat content will be logged.
        :param name: Logging-configuration name. The value does not need to be unique.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcdec1ce6b231f7fa9df5597fb2f4e67a22d8ba9d96daf131d4df0873c6e231)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggingConfigurationProps(
            destination_configuration=destination_configuration, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c195596a8ae55fd22f6aa7eb35eb905dd4685c97d6d7b38cfe1a3edcbef53378)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c3efe98185959e7d21c269adf4f69c5ced8a2f07e2a6cb870029f3f29320258)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfiguration")
    def destination_configuration(
        self,
    ) -> typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The DestinationConfiguration is a complex type that contains information about where chat content will be logged.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration
        '''
        return typing.cast(typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "destinationConfiguration"))

    @destination_configuration.setter
    def destination_configuration(
        self,
        value: typing.Union["CfnLoggingConfiguration.DestinationConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74b829a27ba07de31a0d9e72a211797b08f14cdade445747c0592dd73928571)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a1f97ff7b4b46f897b639d9076ffe5c930d44f09737da9232b08f506fa874b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty",
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
                import aws_cdk.aws_ivschat as ivschat
                
                cloud_watch_logs_destination_configuration_property = ivschat.CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty(
                    log_group_name="logGroupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a09b93e9bf6d2178dd96bd1a9c2f96f089c8039a855c7880dbe50e740e45edc)
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
        jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfiguration.DestinationConfigurationProperty",
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
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggingConfiguration.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
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
                import aws_cdk.aws_ivschat as ivschat
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__1f84761e27fb851dd4604760df79d4db7bec959044ce9b87dd3bf0578b6be824)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty"]]:
            '''An Amazon CloudWatch Logs destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty"]]:
            '''An Amazon Kinesis Data Firehose destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.S3DestinationConfigurationProperty"]]:
            '''An Amazon S3 destination configuration where chat activity will be logged.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivschat-loggingconfiguration-destinationconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.S3DestinationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty",
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
                import aws_cdk.aws_ivschat as ivschat
                
                firehose_destination_configuration_property = ivschat.CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty(
                    delivery_stream_name="deliveryStreamName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03cea8fd041646d3999d4b7feba2e52f4f638674dda27c48e3734fbc082bb55f)
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
        jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty",
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
                import aws_cdk.aws_ivschat as ivschat
                
                s3_destination_configuration_property = ivschat.CfnLoggingConfiguration.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6a1949ccd95a9e11d69d37cb05ee59c330f35134d193c82649e01c782c9deed)
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
    jsii_type="@aws-cdk/aws-ivschat.CfnLoggingConfigurationProps",
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
        destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_ivschat as ivschat
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5c52295cb8d04faf6b2b8a6f50bb56ccdb977399e2f057442e7ca3209e60f50)
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
    ) -> typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The DestinationConfiguration is a complex type that contains information about where chat content will be logged.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        assert result is not None, "Required property 'destination_configuration' is missing"
        return typing.cast(typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Logging-configuration name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-loggingconfiguration.html#cfn-ivschat-loggingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRoom(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivschat.CfnRoom",
):
    '''A CloudFormation ``AWS::IVSChat::Room``.

    The ``AWS::IVSChat::Room`` resource specifies an  room that allows clients to connect and pass messages. For more information, see `CreateRoom <https://docs.aws.amazon.com/ivs/latest/ChatAPIReference/API_CreateRoom.html>`_ in the *Amazon Interactive Video Service Chat API Reference* .

    :cloudformationResource: AWS::IVSChat::Room
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivschat as ivschat
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
        maximum_message_length: typing.Optional[jsii.Number] = None,
        maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
        message_review_handler: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRoom.MessageReviewHandlerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__94aef24ab07f03ea7ccf4db91fad3a637da581817c74ff8508d99bd52aaf977b)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5adffeb4b2a06bfc269969ff3c9acb9fa649c6f6f189792cdbb6aa3285c1e5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4378bccf0a6ed9754ddb7e66664489f78f55a114a0aeb2a858f17e2155462c)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__dfea2df7a9ba7cf1ba347a1d9c81a0fe33dfaefd55eb65e784bd29fd8bdda22b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b51e84fe23ad38f5c65c0b0c009f7efd80181658d0deecc205c9f9f42c264e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abdd3be961e03f4e0f4ec0852711ea5dded5461a9dfeb7ed980ae4261198b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumMessageRatePerSecond", value)

    @builtins.property
    @jsii.member(jsii_name="messageReviewHandler")
    def message_review_handler(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoom.MessageReviewHandlerProperty"]]:
        '''Configuration information for optional review of messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-messagereviewhandler
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoom.MessageReviewHandlerProperty"]], jsii.get(self, "messageReviewHandler"))

    @message_review_handler.setter
    def message_review_handler(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRoom.MessageReviewHandlerProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a64cee2fc0236d9b217da88a4732a2462f7ebc83b8181cdc8a80377ab9ebbbd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e6c6a037c3007163af4d9a543d2bcd414ecc3c43b9c6b3436ffdfbfc694b17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivschat.CfnRoom.MessageReviewHandlerProperty",
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
                import aws_cdk.aws_ivschat as ivschat
                
                message_review_handler_property = ivschat.CfnRoom.MessageReviewHandlerProperty(
                    fallback_result="fallbackResult",
                    uri="uri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f582c56bc0c8e348c773dc9503f5ef00763ebd4b527b804e1ebdeefec6f420a7)
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
    jsii_type="@aws-cdk/aws-ivschat.CfnRoomProps",
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
        message_review_handler: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_ivschat as ivschat
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__05d4dbf126e419a0a27a409ef253a8c8bc5f7fde21491b98ed7c6a5a7092002b)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoom.MessageReviewHandlerProperty]]:
        '''Configuration information for optional review of messages.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-messagereviewhandler
        '''
        result = self._values.get("message_review_handler")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoom.MessageReviewHandlerProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Room name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivschat-room.html#cfn-ivschat-room-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

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

def _typecheckingstub__cdcdec1ce6b231f7fa9df5597fb2f4e67a22d8ba9d96daf131d4df0873c6e231(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c195596a8ae55fd22f6aa7eb35eb905dd4685c97d6d7b38cfe1a3edcbef53378(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c3efe98185959e7d21c269adf4f69c5ced8a2f07e2a6cb870029f3f29320258(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74b829a27ba07de31a0d9e72a211797b08f14cdade445747c0592dd73928571(
    value: typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1f97ff7b4b46f897b639d9076ffe5c930d44f09737da9232b08f506fa874b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a09b93e9bf6d2178dd96bd1a9c2f96f089c8039a855c7880dbe50e740e45edc(
    *,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f84761e27fb851dd4604760df79d4db7bec959044ce9b87dd3bf0578b6be824(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.CloudWatchLogsDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.FirehoseDestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cea8fd041646d3999d4b7feba2e52f4f638674dda27c48e3734fbc082bb55f(
    *,
    delivery_stream_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6a1949ccd95a9e11d69d37cb05ee59c330f35134d193c82649e01c782c9deed(
    *,
    bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c52295cb8d04faf6b2b8a6f50bb56ccdb977399e2f057442e7ca3209e60f50(
    *,
    destination_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94aef24ab07f03ea7ccf4db91fad3a637da581817c74ff8508d99bd52aaf977b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_message_length: typing.Optional[jsii.Number] = None,
    maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
    message_review_handler: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5adffeb4b2a06bfc269969ff3c9acb9fa649c6f6f189792cdbb6aa3285c1e5a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4378bccf0a6ed9754ddb7e66664489f78f55a114a0aeb2a858f17e2155462c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfea2df7a9ba7cf1ba347a1d9c81a0fe33dfaefd55eb65e784bd29fd8bdda22b(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b51e84fe23ad38f5c65c0b0c009f7efd80181658d0deecc205c9f9f42c264e3(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abdd3be961e03f4e0f4ec0852711ea5dded5461a9dfeb7ed980ae4261198b6a(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a64cee2fc0236d9b217da88a4732a2462f7ebc83b8181cdc8a80377ab9ebbbd0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRoom.MessageReviewHandlerProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e6c6a037c3007163af4d9a543d2bcd414ecc3c43b9c6b3436ffdfbfc694b17(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f582c56bc0c8e348c773dc9503f5ef00763ebd4b527b804e1ebdeefec6f420a7(
    *,
    fallback_result: typing.Optional[builtins.str] = None,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d4dbf126e419a0a27a409ef253a8c8bc5f7fde21491b98ed7c6a5a7092002b(
    *,
    logging_configuration_identifiers: typing.Optional[typing.Sequence[builtins.str]] = None,
    maximum_message_length: typing.Optional[jsii.Number] = None,
    maximum_message_rate_per_second: typing.Optional[jsii.Number] = None,
    message_review_handler: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRoom.MessageReviewHandlerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
