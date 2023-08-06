'''
# `mongodbatlas_cloud_provider_snapshot_restore_job`

Refer to the Terraform Registory for docs: [`mongodbatlas_cloud_provider_snapshot_restore_job`](https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class CloudProviderSnapshotRestoreJob(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotRestoreJob.CloudProviderSnapshotRestoreJob",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job mongodbatlas_cloud_provider_snapshot_restore_job}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        project_id: builtins.str,
        snapshot_id: builtins.str,
        delivery_type: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        delivery_type_config: typing.Optional[typing.Union["CloudProviderSnapshotRestoreJobDeliveryTypeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job mongodbatlas_cloud_provider_snapshot_restore_job} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#cluster_name CloudProviderSnapshotRestoreJob#cluster_name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#project_id CloudProviderSnapshotRestoreJob#project_id}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#snapshot_id CloudProviderSnapshotRestoreJob#snapshot_id}.
        :param delivery_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type CloudProviderSnapshotRestoreJob#delivery_type}.
        :param delivery_type_config: delivery_type_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type_config CloudProviderSnapshotRestoreJob#delivery_type_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#id CloudProviderSnapshotRestoreJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb875b9afdf165e48fca2fab51b04c4606e08f56cc9de2f1c2008dfb9f3ebf1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudProviderSnapshotRestoreJobConfig(
            cluster_name=cluster_name,
            project_id=project_id,
            snapshot_id=snapshot_id,
            delivery_type=delivery_type,
            delivery_type_config=delivery_type_config,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDeliveryTypeConfig")
    def put_delivery_type_config(
        self,
        *,
        automated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oplog_inc: typing.Optional[jsii.Number] = None,
        oplog_ts: typing.Optional[jsii.Number] = None,
        point_in_time: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        point_in_time_utc_seconds: typing.Optional[jsii.Number] = None,
        target_cluster_name: typing.Optional[builtins.str] = None,
        target_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#automated CloudProviderSnapshotRestoreJob#automated}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#download CloudProviderSnapshotRestoreJob#download}.
        :param oplog_inc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_inc CloudProviderSnapshotRestoreJob#oplog_inc}.
        :param oplog_ts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_ts CloudProviderSnapshotRestoreJob#oplog_ts}.
        :param point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time CloudProviderSnapshotRestoreJob#point_in_time}.
        :param point_in_time_utc_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time_utc_seconds CloudProviderSnapshotRestoreJob#point_in_time_utc_seconds}.
        :param target_cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_cluster_name CloudProviderSnapshotRestoreJob#target_cluster_name}.
        :param target_project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_project_id CloudProviderSnapshotRestoreJob#target_project_id}.
        '''
        value = CloudProviderSnapshotRestoreJobDeliveryTypeConfig(
            automated=automated,
            download=download,
            oplog_inc=oplog_inc,
            oplog_ts=oplog_ts,
            point_in_time=point_in_time,
            point_in_time_utc_seconds=point_in_time_utc_seconds,
            target_cluster_name=target_cluster_name,
            target_project_id=target_project_id,
        )

        return typing.cast(None, jsii.invoke(self, "putDeliveryTypeConfig", [value]))

    @jsii.member(jsii_name="resetDeliveryType")
    def reset_delivery_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryType", []))

    @jsii.member(jsii_name="resetDeliveryTypeConfig")
    def reset_delivery_type_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeliveryTypeConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="cancelled")
    def cancelled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "cancelled"))

    @builtins.property
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="deliveryTypeConfig")
    def delivery_type_config(
        self,
    ) -> "CloudProviderSnapshotRestoreJobDeliveryTypeConfigOutputReference":
        return typing.cast("CloudProviderSnapshotRestoreJobDeliveryTypeConfigOutputReference", jsii.get(self, "deliveryTypeConfig"))

    @builtins.property
    @jsii.member(jsii_name="deliveryUrl")
    def delivery_url(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "deliveryUrl"))

    @builtins.property
    @jsii.member(jsii_name="expired")
    def expired(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "expired"))

    @builtins.property
    @jsii.member(jsii_name="expiresAt")
    def expires_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiresAt"))

    @builtins.property
    @jsii.member(jsii_name="finishedAt")
    def finished_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishedAt"))

    @builtins.property
    @jsii.member(jsii_name="snapshotRestoreJobId")
    def snapshot_restore_job_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotRestoreJobId"))

    @builtins.property
    @jsii.member(jsii_name="timestamp")
    def timestamp(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestamp"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryTypeConfigInput")
    def delivery_type_config_input(
        self,
    ) -> typing.Optional["CloudProviderSnapshotRestoreJobDeliveryTypeConfig"]:
        return typing.cast(typing.Optional["CloudProviderSnapshotRestoreJobDeliveryTypeConfig"], jsii.get(self, "deliveryTypeConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deliveryTypeInput")
    def delivery_type_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "deliveryTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="snapshotIdInput")
    def snapshot_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "snapshotIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd53447f28372f8a9220e6d7904ea6f5dc07cfbfae41d4ead51e8bf747f47d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="deliveryType")
    def delivery_type(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "deliveryType"))

    @delivery_type.setter
    def delivery_type(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ef4e65b9f15e9e2641e943d26b01fcf65dfaf5071bb91acc519644876268d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0750e7e7a473d3e6eec955f08b32d98eff7efe845489bcf99f697e5a6051ff67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecb5486cf42cb9c1559d1133008494bfc612eaf6a5323c1ba8d6dfc40243170)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotId")
    def snapshot_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "snapshotId"))

    @snapshot_id.setter
    def snapshot_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859a1ec1a88f87b7f9a6528404ae848561129d351bc31d24b62e4b140ba9ee0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snapshotId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotRestoreJob.CloudProviderSnapshotRestoreJobConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_name": "clusterName",
        "project_id": "projectId",
        "snapshot_id": "snapshotId",
        "delivery_type": "deliveryType",
        "delivery_type_config": "deliveryTypeConfig",
        "id": "id",
    },
)
class CloudProviderSnapshotRestoreJobConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        cluster_name: builtins.str,
        project_id: builtins.str,
        snapshot_id: builtins.str,
        delivery_type: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        delivery_type_config: typing.Optional[typing.Union["CloudProviderSnapshotRestoreJobDeliveryTypeConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#cluster_name CloudProviderSnapshotRestoreJob#cluster_name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#project_id CloudProviderSnapshotRestoreJob#project_id}.
        :param snapshot_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#snapshot_id CloudProviderSnapshotRestoreJob#snapshot_id}.
        :param delivery_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type CloudProviderSnapshotRestoreJob#delivery_type}.
        :param delivery_type_config: delivery_type_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type_config CloudProviderSnapshotRestoreJob#delivery_type_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#id CloudProviderSnapshotRestoreJob#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(delivery_type_config, dict):
            delivery_type_config = CloudProviderSnapshotRestoreJobDeliveryTypeConfig(**delivery_type_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2492ff3afc77d6fca6a83b57b5c9c2674258821b08ac60071f482476a24959ac)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument snapshot_id", value=snapshot_id, expected_type=type_hints["snapshot_id"])
            check_type(argname="argument delivery_type", value=delivery_type, expected_type=type_hints["delivery_type"])
            check_type(argname="argument delivery_type_config", value=delivery_type_config, expected_type=type_hints["delivery_type_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "project_id": project_id,
            "snapshot_id": snapshot_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if delivery_type is not None:
            self._values["delivery_type"] = delivery_type
        if delivery_type_config is not None:
            self._values["delivery_type_config"] = delivery_type_config
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#cluster_name CloudProviderSnapshotRestoreJob#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#project_id CloudProviderSnapshotRestoreJob#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def snapshot_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#snapshot_id CloudProviderSnapshotRestoreJob#snapshot_id}.'''
        result = self._values.get("snapshot_id")
        assert result is not None, "Required property 'snapshot_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delivery_type(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type CloudProviderSnapshotRestoreJob#delivery_type}.'''
        result = self._values.get("delivery_type")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def delivery_type_config(
        self,
    ) -> typing.Optional["CloudProviderSnapshotRestoreJobDeliveryTypeConfig"]:
        '''delivery_type_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#delivery_type_config CloudProviderSnapshotRestoreJob#delivery_type_config}
        '''
        result = self._values.get("delivery_type_config")
        return typing.cast(typing.Optional["CloudProviderSnapshotRestoreJobDeliveryTypeConfig"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#id CloudProviderSnapshotRestoreJob#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderSnapshotRestoreJobConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotRestoreJob.CloudProviderSnapshotRestoreJobDeliveryTypeConfig",
    jsii_struct_bases=[],
    name_mapping={
        "automated": "automated",
        "download": "download",
        "oplog_inc": "oplogInc",
        "oplog_ts": "oplogTs",
        "point_in_time": "pointInTime",
        "point_in_time_utc_seconds": "pointInTimeUtcSeconds",
        "target_cluster_name": "targetClusterName",
        "target_project_id": "targetProjectId",
    },
)
class CloudProviderSnapshotRestoreJobDeliveryTypeConfig:
    def __init__(
        self,
        *,
        automated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oplog_inc: typing.Optional[jsii.Number] = None,
        oplog_ts: typing.Optional[jsii.Number] = None,
        point_in_time: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        point_in_time_utc_seconds: typing.Optional[jsii.Number] = None,
        target_cluster_name: typing.Optional[builtins.str] = None,
        target_project_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param automated: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#automated CloudProviderSnapshotRestoreJob#automated}.
        :param download: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#download CloudProviderSnapshotRestoreJob#download}.
        :param oplog_inc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_inc CloudProviderSnapshotRestoreJob#oplog_inc}.
        :param oplog_ts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_ts CloudProviderSnapshotRestoreJob#oplog_ts}.
        :param point_in_time: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time CloudProviderSnapshotRestoreJob#point_in_time}.
        :param point_in_time_utc_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time_utc_seconds CloudProviderSnapshotRestoreJob#point_in_time_utc_seconds}.
        :param target_cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_cluster_name CloudProviderSnapshotRestoreJob#target_cluster_name}.
        :param target_project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_project_id CloudProviderSnapshotRestoreJob#target_project_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61dac1709ca4f9f0e9dff0fc0181b2730d0b4e0b103314e90a56240b898365d9)
            check_type(argname="argument automated", value=automated, expected_type=type_hints["automated"])
            check_type(argname="argument download", value=download, expected_type=type_hints["download"])
            check_type(argname="argument oplog_inc", value=oplog_inc, expected_type=type_hints["oplog_inc"])
            check_type(argname="argument oplog_ts", value=oplog_ts, expected_type=type_hints["oplog_ts"])
            check_type(argname="argument point_in_time", value=point_in_time, expected_type=type_hints["point_in_time"])
            check_type(argname="argument point_in_time_utc_seconds", value=point_in_time_utc_seconds, expected_type=type_hints["point_in_time_utc_seconds"])
            check_type(argname="argument target_cluster_name", value=target_cluster_name, expected_type=type_hints["target_cluster_name"])
            check_type(argname="argument target_project_id", value=target_project_id, expected_type=type_hints["target_project_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automated is not None:
            self._values["automated"] = automated
        if download is not None:
            self._values["download"] = download
        if oplog_inc is not None:
            self._values["oplog_inc"] = oplog_inc
        if oplog_ts is not None:
            self._values["oplog_ts"] = oplog_ts
        if point_in_time is not None:
            self._values["point_in_time"] = point_in_time
        if point_in_time_utc_seconds is not None:
            self._values["point_in_time_utc_seconds"] = point_in_time_utc_seconds
        if target_cluster_name is not None:
            self._values["target_cluster_name"] = target_cluster_name
        if target_project_id is not None:
            self._values["target_project_id"] = target_project_id

    @builtins.property
    def automated(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#automated CloudProviderSnapshotRestoreJob#automated}.'''
        result = self._values.get("automated")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def download(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#download CloudProviderSnapshotRestoreJob#download}.'''
        result = self._values.get("download")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def oplog_inc(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_inc CloudProviderSnapshotRestoreJob#oplog_inc}.'''
        result = self._values.get("oplog_inc")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oplog_ts(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#oplog_ts CloudProviderSnapshotRestoreJob#oplog_ts}.'''
        result = self._values.get("oplog_ts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def point_in_time(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time CloudProviderSnapshotRestoreJob#point_in_time}.'''
        result = self._values.get("point_in_time")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def point_in_time_utc_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#point_in_time_utc_seconds CloudProviderSnapshotRestoreJob#point_in_time_utc_seconds}.'''
        result = self._values.get("point_in_time_utc_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def target_cluster_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_cluster_name CloudProviderSnapshotRestoreJob#target_cluster_name}.'''
        result = self._values.get("target_cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_project_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_restore_job#target_project_id CloudProviderSnapshotRestoreJob#target_project_id}.'''
        result = self._values.get("target_project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderSnapshotRestoreJobDeliveryTypeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudProviderSnapshotRestoreJobDeliveryTypeConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotRestoreJob.CloudProviderSnapshotRestoreJobDeliveryTypeConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dc479e855bea7aab5b2fc746fb3ae43c726dcefab2c7210687dd01a1d5e094)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAutomated")
    def reset_automated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomated", []))

    @jsii.member(jsii_name="resetDownload")
    def reset_download(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDownload", []))

    @jsii.member(jsii_name="resetOplogInc")
    def reset_oplog_inc(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOplogInc", []))

    @jsii.member(jsii_name="resetOplogTs")
    def reset_oplog_ts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOplogTs", []))

    @jsii.member(jsii_name="resetPointInTime")
    def reset_point_in_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTime", []))

    @jsii.member(jsii_name="resetPointInTimeUtcSeconds")
    def reset_point_in_time_utc_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPointInTimeUtcSeconds", []))

    @jsii.member(jsii_name="resetTargetClusterName")
    def reset_target_cluster_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetClusterName", []))

    @jsii.member(jsii_name="resetTargetProjectId")
    def reset_target_project_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetProjectId", []))

    @builtins.property
    @jsii.member(jsii_name="automatedInput")
    def automated_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automatedInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadInput")
    def download_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "downloadInput"))

    @builtins.property
    @jsii.member(jsii_name="oplogIncInput")
    def oplog_inc_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oplogIncInput"))

    @builtins.property
    @jsii.member(jsii_name="oplogTsInput")
    def oplog_ts_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oplogTsInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeInput")
    def point_in_time_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pointInTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="pointInTimeUtcSecondsInput")
    def point_in_time_utc_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pointInTimeUtcSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetClusterNameInput")
    def target_cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetClusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="targetProjectIdInput")
    def target_project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetProjectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="automated")
    def automated(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automated"))

    @automated.setter
    def automated(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9792e399c04405d67e81f9cee8f7649cbd564a1cb79e64e732ffd74da20470e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automated", value)

    @builtins.property
    @jsii.member(jsii_name="download")
    def download(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "download"))

    @download.setter
    def download(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca5ef73d233021f5cb5568f4447bebda7a475e8bac4e51f47dd03f4874ee2b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "download", value)

    @builtins.property
    @jsii.member(jsii_name="oplogInc")
    def oplog_inc(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oplogInc"))

    @oplog_inc.setter
    def oplog_inc(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8368b2a4c40e49a668cd04373140a33790e4e5d2d605f08cb5e0b336ff30e00b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oplogInc", value)

    @builtins.property
    @jsii.member(jsii_name="oplogTs")
    def oplog_ts(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oplogTs"))

    @oplog_ts.setter
    def oplog_ts(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e64aeead95fd10ad4ead998366c8a623dfc6df22b7acdcd07211323e2d5da6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oplogTs", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTime")
    def point_in_time(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pointInTime"))

    @point_in_time.setter
    def point_in_time(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b10d20a38d94b32ed12fd6b2ed1be4a6749bca63d253192c266a8f153c8f3b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTime", value)

    @builtins.property
    @jsii.member(jsii_name="pointInTimeUtcSeconds")
    def point_in_time_utc_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pointInTimeUtcSeconds"))

    @point_in_time_utc_seconds.setter
    def point_in_time_utc_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca3605e62864da72ca965f293a805c1139883a7485e1b0b7a43ad2b0b497f3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pointInTimeUtcSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="targetClusterName")
    def target_cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetClusterName"))

    @target_cluster_name.setter
    def target_cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c7f6afa525b3242f2c99734d798d7a078b643fb2b30955773686639d972bc74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetClusterName", value)

    @builtins.property
    @jsii.member(jsii_name="targetProjectId")
    def target_project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetProjectId"))

    @target_project_id.setter
    def target_project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d76c239d9b303dd04b3ed7b1485868bffb9f32e3e06d0bbf67cbca8c255bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetProjectId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CloudProviderSnapshotRestoreJobDeliveryTypeConfig]:
        return typing.cast(typing.Optional[CloudProviderSnapshotRestoreJobDeliveryTypeConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudProviderSnapshotRestoreJobDeliveryTypeConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef179c6d0d557b10b912541ff17710dc30af1766870c049e1843417ee8ca0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudProviderSnapshotRestoreJob",
    "CloudProviderSnapshotRestoreJobConfig",
    "CloudProviderSnapshotRestoreJobDeliveryTypeConfig",
    "CloudProviderSnapshotRestoreJobDeliveryTypeConfigOutputReference",
]

publication.publish()

def _typecheckingstub__ebb875b9afdf165e48fca2fab51b04c4606e08f56cc9de2f1c2008dfb9f3ebf1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    project_id: builtins.str,
    snapshot_id: builtins.str,
    delivery_type: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    delivery_type_config: typing.Optional[typing.Union[CloudProviderSnapshotRestoreJobDeliveryTypeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd53447f28372f8a9220e6d7904ea6f5dc07cfbfae41d4ead51e8bf747f47d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ef4e65b9f15e9e2641e943d26b01fcf65dfaf5071bb91acc519644876268d6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0750e7e7a473d3e6eec955f08b32d98eff7efe845489bcf99f697e5a6051ff67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecb5486cf42cb9c1559d1133008494bfc612eaf6a5323c1ba8d6dfc40243170(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859a1ec1a88f87b7f9a6528404ae848561129d351bc31d24b62e4b140ba9ee0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2492ff3afc77d6fca6a83b57b5c9c2674258821b08ac60071f482476a24959ac(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    project_id: builtins.str,
    snapshot_id: builtins.str,
    delivery_type: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    delivery_type_config: typing.Optional[typing.Union[CloudProviderSnapshotRestoreJobDeliveryTypeConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61dac1709ca4f9f0e9dff0fc0181b2730d0b4e0b103314e90a56240b898365d9(
    *,
    automated: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    download: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oplog_inc: typing.Optional[jsii.Number] = None,
    oplog_ts: typing.Optional[jsii.Number] = None,
    point_in_time: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    point_in_time_utc_seconds: typing.Optional[jsii.Number] = None,
    target_cluster_name: typing.Optional[builtins.str] = None,
    target_project_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dc479e855bea7aab5b2fc746fb3ae43c726dcefab2c7210687dd01a1d5e094(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9792e399c04405d67e81f9cee8f7649cbd564a1cb79e64e732ffd74da20470e5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca5ef73d233021f5cb5568f4447bebda7a475e8bac4e51f47dd03f4874ee2b8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8368b2a4c40e49a668cd04373140a33790e4e5d2d605f08cb5e0b336ff30e00b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e64aeead95fd10ad4ead998366c8a623dfc6df22b7acdcd07211323e2d5da6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b10d20a38d94b32ed12fd6b2ed1be4a6749bca63d253192c266a8f153c8f3b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca3605e62864da72ca965f293a805c1139883a7485e1b0b7a43ad2b0b497f3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c7f6afa525b3242f2c99734d798d7a078b643fb2b30955773686639d972bc74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d76c239d9b303dd04b3ed7b1485868bffb9f32e3e06d0bbf67cbca8c255bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef179c6d0d557b10b912541ff17710dc30af1766870c049e1843417ee8ca0ac(
    value: typing.Optional[CloudProviderSnapshotRestoreJobDeliveryTypeConfig],
) -> None:
    """Type checking stubs"""
    pass
