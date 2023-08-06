'''
# SNS Notification OpsGenie

This repository contains [AWS CDK](https://aws.amazon.com/cdk/) constructs which can be used for sns to notify to Opsgenie using [projen](https://github.com/projen/projen) + [jsii](https://github.com/aws/jsii) and publishing it to [npm](https://www.npmjs.com/) and [pypi](https://pypi.org/) repositories..

## Table of Contents

* [About projen](#about-projen)
* [About jsii](#about-jsii)
* [How to Use](#how-to-use)

## About projen

[projen](https://github.com/projen/projen) is a tool to write your project configuration using code instead of managing it yourself.projen synthesizes project configuration files such as package.json, tsconfig.json, .gitignore, GitHub Workflows, eslint, jest, etc from a well-typed definition written in JavaScript.

## About jsii

[jsii](https://aws.github.io/jsii/) allows code in any language to naturally interact with JavaScript classes. It is the technology that enables the [AWS CDK](https://aws.amazon.com/cdk/) to deliver polyglot libraries from a single codebase!

## Steps For using a `sns-notification-opsgenie` in your cdk Construct

1. Install the package based on your language:

   If you are using python, use below comand in your terminal:

   ```shell
    pip install sns-notification-opsgenie
   ```

   If you are using Typescript, use below comand in your terminal:

   ```shell
    npm i sns-notification-opsgenie
   ```
2. Next,import the package in your cdk construct based on your language:

   for Python:

   ```shell
    from sns-notification-opsgenie import SnsNotifyOpsgenie
   ```

   for Typescript:

   ```shell
    import { SnsNotifcationOpsgenie } from sns-notification-opsgenie
   ```
3. Use the method `getOpgsgenieTopicArn` by passing `AWS AcccountId`, `OpsGenie Priority` and optionally `AWS Region`. In case you do not pass any region, default region will be `eu-west-1`.
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

import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="sns-notification-opsgenie.ISnsNotifyOpsgenieProps")
class ISnsNotifyOpsgenieProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> typing.Optional[builtins.str]:
        ...

    @qualifier.setter
    def qualifier(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISnsNotifyOpsgeniePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "sns-notification-opsgenie.ISnsNotifyOpsgenieProps"

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75488f3a2d376155d6362d6129a2b76e1120f9ac6600f43c367352cda9f2c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISnsNotifyOpsgenieProps).__jsii_proxy_class__ = lambda : _ISnsNotifyOpsgeniePropsProxy


@jsii.enum(jsii_type="sns-notification-opsgenie.Priority")
class Priority(enum.Enum):
    '''Enumeration of priority for Alarms.

    The ``Priority`` enum is used to represent the priority of an Alarm. It has five possible values.
    '''

    CRITICAL = "CRITICAL"
    '''indicates that the alarm is of the highest priority and requires immediate attention.'''
    HIGH = "HIGH"
    '''indicates that the alarm is of high priority and should be addressed as soon as possible.'''
    MEDIUM = "MEDIUM"
    '''indicates that the alarm is of medium priority and can be addressed in due course.'''
    LOW = "LOW"
    '''indicates that the alarm is of low priority and can be addressed at a later time.'''
    INFORMATION = "INFORMATION"
    '''indicates that the alarm is of the lowest priority and can be addressed at a later time.'''


class SnsNotifyOpsgenie(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="sns-notification-opsgenie.SnsNotifyOpsgenie",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Optional[ISnsNotifyOpsgenieProps] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319977398ad42fb092f8108ce5466a2521ff5cf0b0b8b2721a3eed9336f66666)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getOpgsgenieTopicArn")
    def get_opgsgenie_topic_arn(
        self,
        account_id: builtins.str,
        priority: Priority,
        region: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''Returns an sns.Topic object that represents an SNS topic in AWS. The topic ARN is constructed based on the accountId, priority, and region parameters.

        :param account_id: The AWS account ID where the topic is located.
        :param priority: The priority of the topic. Must be one of
        :param region: The AWS region where the topic is located. If not specified, defaults to eu-west-1.

        :return: An sns.Topic object that represents an SNS topic in AWS.

        :enum: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac97967a10f6c801f2d4430a4a2460b154e79b3005c888c44e300ad0fc96e122)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, jsii.invoke(self, "getOpgsgenieTopicArn", [account_id, priority, region]))


__all__ = [
    "ISnsNotifyOpsgenieProps",
    "Priority",
    "SnsNotifyOpsgenie",
]

publication.publish()

def _typecheckingstub__d75488f3a2d376155d6362d6129a2b76e1120f9ac6600f43c367352cda9f2c16(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319977398ad42fb092f8108ce5466a2521ff5cf0b0b8b2721a3eed9336f66666(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Optional[ISnsNotifyOpsgenieProps] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac97967a10f6c801f2d4430a4a2460b154e79b3005c888c44e300ad0fc96e122(
    account_id: builtins.str,
    priority: Priority,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
