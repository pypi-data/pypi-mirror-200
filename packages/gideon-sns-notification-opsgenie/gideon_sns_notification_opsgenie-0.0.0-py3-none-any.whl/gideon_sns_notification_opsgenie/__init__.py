'''
# SNS Notification OpsGenie

This repository contains [AWS CDK](https://aws.amazon.com/cdk/) constructs which can be used for sns to notify to Opsgenie using [projen](https://github.com/projen/projen) + [jsii](https://github.com/aws/jsii) and publishing it to [npm](https://www.npmjs.com/) and [pypi](https://pypi.org/) repositories.

## Table of Contents

* [About projen](#about-projen)
* [About jsii](#about-jsii)
* [How to Use](#how-to-use)
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


@jsii.interface(jsii_type="gideon-sns-notification-opsgenie.ISnsNotifyOpsgenieProps")
class ISnsNotifyOpsgenieProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> typing.Optional[builtins.str]:
        ...

    @qualifier.setter
    def qualifier(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ISnsNotifyOpsgeniePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "gideon-sns-notification-opsgenie.ISnsNotifyOpsgenieProps"

    @builtins.property
    @jsii.member(jsii_name="qualifier")
    def qualifier(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "qualifier"))

    @qualifier.setter
    def qualifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95fded0edf0189996f8d749075c2d25fe642036dae9a5f8b492a389218ee22ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "qualifier", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISnsNotifyOpsgenieProps).__jsii_proxy_class__ = lambda : _ISnsNotifyOpsgeniePropsProxy


@jsii.enum(jsii_type="gideon-sns-notification-opsgenie.Priority")
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
    jsii_type="gideon-sns-notification-opsgenie.SnsNotifyOpsgenie",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d94569c0d083cad8c5541624a5e8f966ad4908545acf5f9cdd9e67c0b1effd6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a24b78c7ddadfece76dde331eeb5781fdf95b778c8bf77e1939423b5b3dda2)
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

def _typecheckingstub__95fded0edf0189996f8d749075c2d25fe642036dae9a5f8b492a389218ee22ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94569c0d083cad8c5541624a5e8f966ad4908545acf5f9cdd9e67c0b1effd6b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Optional[ISnsNotifyOpsgenieProps] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a24b78c7ddadfece76dde331eeb5781fdf95b778c8bf77e1939423b5b3dda2(
    account_id: builtins.str,
    priority: Priority,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
