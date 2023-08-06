'''
[![NPM version](https://badge.fury.io/js/lambda-layer-version-cleaner.svg)](https://badge.fury.io/js/lambda-layer-version-cleaner)
[![PyPI version](https://badge.fury.io/py/lambda-layer-version-cleaner.svg)](https://badge.fury.io/py/lambda-layer-version-cleaner)
![Release](https://github.com/unirt/lambda-layer-version-cleaner/workflows/release/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# lambda-layer-version-cleaner

`lambda-layer-version-cleaner` is a CDK Construct that helps you manage and automatically clean up old versions of AWS Lambda Layers. It works with both JavaScript / TypeScript and Python CDK apps. Please note that this cleaner will only clean up versions of Lambda Layers in the region where it's deployed.

## Installation

For JavaScript / TypeScript projects:

```bash
npm install lambda-layer-version-cleaner
```

For Python projects:

```bash
pip install lambda-layer-version-cleaner
```

## Usage

To use the `LambdaLayerVersionCleaner` in your CDK project, simply import it and add it to your stack.

### JavaScript / TypeScript

```javascript
import * as cdk from 'aws-cdk-lib';
import * as events from 'aws-cdk-lib/aws-events';
import { LambdaLayerVersionCleaner } from 'lambda-layer-version-cleaner';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'ExampleStack');

new LambdaLayerVersionCleaner(stack, 'LambdaLayerVersionCleaner', {
  retainVersions: '5',
  layerCleanerSchedule: events.Schedule.rate(cdk.Duration.days(7)),
});
```

### Python

```python
from aws_cdk import core as cdk
from aws_cdk.aws_events import Schedule
from aws_cdk.core import Duration
from lambda_layer_version_cleaner import LambdaLayerVersionCleaner

app = cdk.App()
stack = cdk.Stack(app, "ExampleStack")

LambdaLayerVersionCleaner(stack, "LambdaLayerVersionCleaner",
    retain_versions="5",
    layer_cleaner_schedule=Schedule.rate(Duration.days(7))
)

app.synth()
```

## Configuration

The `LambdaLayerVersionCleaner` construct takes two optional parameters:

* `retainVersions` (default: `'5'`): The number of layer versions to retain, specified as a string containing a positive integer. The cleaner will delete older versions beyond this count. Note that this value should be a string, not a number. If not specified, the default is '5'. Note that if a Layer has only one version, it won't be deleted.
* `layerCleanerSchedule` (default: `events.Schedule.rate(cdk.Duration.days(1))`): The schedule for running the cleanup process. If not specified, the default is to run once per day.
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(
    jsii_type="lambda-layer-version-cleaner.ILambdaLayerVersionCleanerProps"
)
class ILambdaLayerVersionCleanerProps(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="layerCleanerSchedule")
    def layer_cleaner_schedule(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''
        :stability: experimental
        '''
        ...

    @layer_cleaner_schedule.setter
    def layer_cleaner_schedule(
        self,
        value: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="retainVersions")
    def retain_versions(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        ...

    @retain_versions.setter
    def retain_versions(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _ILambdaLayerVersionCleanerPropsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "lambda-layer-version-cleaner.ILambdaLayerVersionCleanerProps"

    @builtins.property
    @jsii.member(jsii_name="layerCleanerSchedule")
    def layer_cleaner_schedule(
        self,
    ) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], jsii.get(self, "layerCleanerSchedule"))

    @layer_cleaner_schedule.setter
    def layer_cleaner_schedule(
        self,
        value: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889aae22edc164118fdace848969daab57a171a9ff790b110ee4695b4110dd07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "layerCleanerSchedule", value)

    @builtins.property
    @jsii.member(jsii_name="retainVersions")
    def retain_versions(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retainVersions"))

    @retain_versions.setter
    def retain_versions(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336386c52fec3053b4e545d31dcc33300b95e9405e3f4c7dd964fc2cd528d610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainVersions", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILambdaLayerVersionCleanerProps).__jsii_proxy_class__ = lambda : _ILambdaLayerVersionCleanerPropsProxy


class LambdaLayerVersionCleaner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="lambda-layer-version-cleaner.LambdaLayerVersionCleaner",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Optional[ILambdaLayerVersionCleanerProps] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465fadc5f9415506f794eb4c0acec8e1448e11304b62382369129d986030dfad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.get(self, "rule"))


__all__ = [
    "ILambdaLayerVersionCleanerProps",
    "LambdaLayerVersionCleaner",
]

publication.publish()

def _typecheckingstub__889aae22edc164118fdace848969daab57a171a9ff790b110ee4695b4110dd07(
    value: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336386c52fec3053b4e545d31dcc33300b95e9405e3f4c7dd964fc2cd528d610(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465fadc5f9415506f794eb4c0acec8e1448e11304b62382369129d986030dfad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Optional[ILambdaLayerVersionCleanerProps] = None,
) -> None:
    """Type checking stubs"""
    pass
