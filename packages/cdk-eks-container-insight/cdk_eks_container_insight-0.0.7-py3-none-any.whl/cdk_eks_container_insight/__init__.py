'''
# CDK EKS Container Insight

This construct configures the necessary dependencies and installs [Amazon CloudWatch Container Insight](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ContainerInsights.html)
on an EKS cluster managed by AWS CDK.

## Using

In your CDK project, initialize a new Container Insight construct for your EKS cluster, like this:

```python
const cluster = new Cluster(this, 'testCluster', {
  vpc: vpc,
  role: clusterRole,
  version: KubernetesVersion.V1_24,
  kubectlLayer: new KubectlV24Layer(this, 'KubectlLayer'),
  defaultCapacity: 1
});

new ContainerInsight(this, 'ContainerInsight', {
  cluster: cluster,
});
```

This will install and configure Container Insight on EC2 managed nodes in your cluster.

## Testing

This construct adds a custom task to [projen](https://projen.io/), so you can test a full deployment
of an EKS cluster with CloudWatch Container Insight installed as specified in `test/integ.containerinsight.ts` by running the
following:

```sh
export CDK_DEFAULT_REGION=<aws region>
export CDK_DEFAULT_ACCOUNT=<account id>
npx projen test:deploy
```

And you can valid the construct installation by login in CloudWatch console to

![](images/pic.png)

As the above will create a cluster. And the Container Insight will show your how cluster information in CloudWatch.

You can clean things up by deleting the deployment and the CDK test stack:

```sh
npx projen test:destroy
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk.aws_eks as _aws_cdk_aws_eks_ceddda9d
import constructs as _constructs_77d1e7e8


class ContainerInsight(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eks-container-insight.ContainerInsight",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        adot_namespace: typing.Optional[builtins.str] = None,
        cloudwatch_namespace: typing.Optional[builtins.str] = None,
        fargate_namespace: typing.Optional[builtins.str] = None,
        fargate_support_mode: typing.Optional["FargateSupportMode"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: The EKS Cluster to attach to.
        :param adot_namespace: The Kubernetes namespace to install ADOT to. Default: amazon-metrics
        :param cloudwatch_namespace: The Kubernetes namespace to install CloudWatch agent to. Default: - amazon-cloudwatch
        :param fargate_namespace: Fargate container insight namepsace. Default: - fargate-container-insights
        :param fargate_support_mode: Fargate support mode for NO/ONLY/BOTH. Default: - NO
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1810d2765637dcaf5b2a0d40bf3112b58c6d9f76625ba083f162b5575ec78ed)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ContainerInsightProps(
            cluster=cluster,
            adot_namespace=adot_namespace,
            cloudwatch_namespace=cloudwatch_namespace,
            fargate_namespace=fargate_namespace,
            fargate_support_mode=fargate_support_mode,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="adotNamespace")
    def adot_namespace(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adotNamespace"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchNamespace")
    def cloudwatch_namespace(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudwatchNamespace"))

    @builtins.property
    @jsii.member(jsii_name="fargateNamespace")
    def fargate_namespace(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fargateNamespace"))

    @builtins.property
    @jsii.member(jsii_name="fargateSupportMode")
    def fargate_support_mode(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fargateSupportMode"))


@jsii.data_type(
    jsii_type="cdk-eks-container-insight.ContainerInsightProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "adot_namespace": "adotNamespace",
        "cloudwatch_namespace": "cloudwatchNamespace",
        "fargate_namespace": "fargateNamespace",
        "fargate_support_mode": "fargateSupportMode",
    },
)
class ContainerInsightProps:
    def __init__(
        self,
        *,
        cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
        adot_namespace: typing.Optional[builtins.str] = None,
        cloudwatch_namespace: typing.Optional[builtins.str] = None,
        fargate_namespace: typing.Optional[builtins.str] = None,
        fargate_support_mode: typing.Optional["FargateSupportMode"] = None,
    ) -> None:
        '''
        :param cluster: The EKS Cluster to attach to.
        :param adot_namespace: The Kubernetes namespace to install ADOT to. Default: amazon-metrics
        :param cloudwatch_namespace: The Kubernetes namespace to install CloudWatch agent to. Default: - amazon-cloudwatch
        :param fargate_namespace: Fargate container insight namepsace. Default: - fargate-container-insights
        :param fargate_support_mode: Fargate support mode for NO/ONLY/BOTH. Default: - NO
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2051979947c97162cc2b0082dce5c2758bcc3eaba8f6c447edbd9f27d6892ae3)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument adot_namespace", value=adot_namespace, expected_type=type_hints["adot_namespace"])
            check_type(argname="argument cloudwatch_namespace", value=cloudwatch_namespace, expected_type=type_hints["cloudwatch_namespace"])
            check_type(argname="argument fargate_namespace", value=fargate_namespace, expected_type=type_hints["fargate_namespace"])
            check_type(argname="argument fargate_support_mode", value=fargate_support_mode, expected_type=type_hints["fargate_support_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
        }
        if adot_namespace is not None:
            self._values["adot_namespace"] = adot_namespace
        if cloudwatch_namespace is not None:
            self._values["cloudwatch_namespace"] = cloudwatch_namespace
        if fargate_namespace is not None:
            self._values["fargate_namespace"] = fargate_namespace
        if fargate_support_mode is not None:
            self._values["fargate_support_mode"] = fargate_support_mode

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_eks_ceddda9d.Cluster:
        '''The EKS Cluster to attach to.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.Cluster, result)

    @builtins.property
    def adot_namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace to install ADOT to.

        :default: amazon-metrics
        '''
        result = self._values.get("adot_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloudwatch_namespace(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes namespace to install CloudWatch agent to.

        :default: - amazon-cloudwatch
        '''
        result = self._values.get("cloudwatch_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fargate_namespace(self) -> typing.Optional[builtins.str]:
        '''Fargate container insight namepsace.

        :default: - fargate-container-insights
        '''
        result = self._values.get("fargate_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fargate_support_mode(self) -> typing.Optional["FargateSupportMode"]:
        '''Fargate support mode for NO/ONLY/BOTH.

        :default: - NO
        '''
        result = self._values.get("fargate_support_mode")
        return typing.cast(typing.Optional["FargateSupportMode"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerInsightProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eks-container-insight.FargateSupportMode")
class FargateSupportMode(enum.Enum):
    NO = "NO"
    '''No support for Fargate profile only support EC2.'''
    ONLY = "ONLY"
    '''Only support for Fargate profile no EC2.'''
    BOTH = "BOTH"
    '''Both support Fargate profile and EC2.'''


__all__ = [
    "ContainerInsight",
    "ContainerInsightProps",
    "FargateSupportMode",
]

publication.publish()

def _typecheckingstub__e1810d2765637dcaf5b2a0d40bf3112b58c6d9f76625ba083f162b5575ec78ed(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    adot_namespace: typing.Optional[builtins.str] = None,
    cloudwatch_namespace: typing.Optional[builtins.str] = None,
    fargate_namespace: typing.Optional[builtins.str] = None,
    fargate_support_mode: typing.Optional[FargateSupportMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2051979947c97162cc2b0082dce5c2758bcc3eaba8f6c447edbd9f27d6892ae3(
    *,
    cluster: _aws_cdk_aws_eks_ceddda9d.Cluster,
    adot_namespace: typing.Optional[builtins.str] = None,
    cloudwatch_namespace: typing.Optional[builtins.str] = None,
    fargate_namespace: typing.Optional[builtins.str] = None,
    fargate_support_mode: typing.Optional[FargateSupportMode] = None,
) -> None:
    """Type checking stubs"""
    pass
