'''
# `mongodbatlas_cloud_provider_snapshot_backup_policy`

Refer to the Terraform Registory for docs: [`mongodbatlas_cloud_provider_snapshot_backup_policy`](https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy).
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


class CloudProviderSnapshotBackupPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy mongodbatlas_cloud_provider_snapshot_backup_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderSnapshotBackupPolicyPolicies", typing.Dict[builtins.str, typing.Any]]]],
        project_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        reference_hour_of_day: typing.Optional[jsii.Number] = None,
        reference_minute_of_hour: typing.Optional[jsii.Number] = None,
        restore_window_days: typing.Optional[jsii.Number] = None,
        update_snapshots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy mongodbatlas_cloud_provider_snapshot_backup_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#cluster_name CloudProviderSnapshotBackupPolicy#cluster_name}.
        :param policies: policies block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#policies CloudProviderSnapshotBackupPolicy#policies}
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#project_id CloudProviderSnapshotBackupPolicy#project_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reference_hour_of_day: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_hour_of_day CloudProviderSnapshotBackupPolicy#reference_hour_of_day}.
        :param reference_minute_of_hour: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_minute_of_hour CloudProviderSnapshotBackupPolicy#reference_minute_of_hour}.
        :param restore_window_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#restore_window_days CloudProviderSnapshotBackupPolicy#restore_window_days}.
        :param update_snapshots: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#update_snapshots CloudProviderSnapshotBackupPolicy#update_snapshots}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b319eb65f74111acd1762dbfc7943e39184bb53538293de1011e34cac52322f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudProviderSnapshotBackupPolicyConfig(
            cluster_name=cluster_name,
            policies=policies,
            project_id=project_id,
            id=id,
            reference_hour_of_day=reference_hour_of_day,
            reference_minute_of_hour=reference_minute_of_hour,
            restore_window_days=restore_window_days,
            update_snapshots=update_snapshots,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPolicies")
    def put_policies(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderSnapshotBackupPolicyPolicies", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13fd468e2948df8648ba432d5c2fe660b7c4ff407984fc2d6c875b8bdda0178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicies", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReferenceHourOfDay")
    def reset_reference_hour_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceHourOfDay", []))

    @jsii.member(jsii_name="resetReferenceMinuteOfHour")
    def reset_reference_minute_of_hour(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReferenceMinuteOfHour", []))

    @jsii.member(jsii_name="resetRestoreWindowDays")
    def reset_restore_window_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRestoreWindowDays", []))

    @jsii.member(jsii_name="resetUpdateSnapshots")
    def reset_update_snapshots(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdateSnapshots", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="nextSnapshot")
    def next_snapshot(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nextSnapshot"))

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(self) -> "CloudProviderSnapshotBackupPolicyPoliciesList":
        return typing.cast("CloudProviderSnapshotBackupPolicyPoliciesList", jsii.get(self, "policies"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policiesInput")
    def policies_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPolicies"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPolicies"]]], jsii.get(self, "policiesInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceHourOfDayInput")
    def reference_hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "referenceHourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="referenceMinuteOfHourInput")
    def reference_minute_of_hour_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "referenceMinuteOfHourInput"))

    @builtins.property
    @jsii.member(jsii_name="restoreWindowDaysInput")
    def restore_window_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "restoreWindowDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="updateSnapshotsInput")
    def update_snapshots_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "updateSnapshotsInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0910df5d7c1ceb854c437a06bf12d710d06d6be6ede9decdd1f4b33f8ba7e140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d696c02c91b416a602577ad6f4474377d28e2296cef9a46858591a77bc5fe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47185e8c32776f667111cfa8aece9b4a510eb2087f884ff6ce56242950139b87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="referenceHourOfDay")
    def reference_hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "referenceHourOfDay"))

    @reference_hour_of_day.setter
    def reference_hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab7611c581c360bcb19fdb3f991ef5e57cbe6a2044670120c681e7fbd3fa95da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceHourOfDay", value)

    @builtins.property
    @jsii.member(jsii_name="referenceMinuteOfHour")
    def reference_minute_of_hour(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "referenceMinuteOfHour"))

    @reference_minute_of_hour.setter
    def reference_minute_of_hour(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98abb066d6cc15a881283ed2c46676567d6b6a2af483bd1f659a516cb71ca962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceMinuteOfHour", value)

    @builtins.property
    @jsii.member(jsii_name="restoreWindowDays")
    def restore_window_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "restoreWindowDays"))

    @restore_window_days.setter
    def restore_window_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675d04be3a23235fab8ab07a275ff94c999a22642604b368a7afe0f065019043)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "restoreWindowDays", value)

    @builtins.property
    @jsii.member(jsii_name="updateSnapshots")
    def update_snapshots(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "updateSnapshots"))

    @update_snapshots.setter
    def update_snapshots(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8395f97d3626b19c182bf91f8621d402feef647901405e71af8ae9b6844f0dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updateSnapshots", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyConfig",
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
        "policies": "policies",
        "project_id": "projectId",
        "id": "id",
        "reference_hour_of_day": "referenceHourOfDay",
        "reference_minute_of_hour": "referenceMinuteOfHour",
        "restore_window_days": "restoreWindowDays",
        "update_snapshots": "updateSnapshots",
    },
)
class CloudProviderSnapshotBackupPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderSnapshotBackupPolicyPolicies", typing.Dict[builtins.str, typing.Any]]]],
        project_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        reference_hour_of_day: typing.Optional[jsii.Number] = None,
        reference_minute_of_hour: typing.Optional[jsii.Number] = None,
        restore_window_days: typing.Optional[jsii.Number] = None,
        update_snapshots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#cluster_name CloudProviderSnapshotBackupPolicy#cluster_name}.
        :param policies: policies block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#policies CloudProviderSnapshotBackupPolicy#policies}
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#project_id CloudProviderSnapshotBackupPolicy#project_id}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param reference_hour_of_day: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_hour_of_day CloudProviderSnapshotBackupPolicy#reference_hour_of_day}.
        :param reference_minute_of_hour: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_minute_of_hour CloudProviderSnapshotBackupPolicy#reference_minute_of_hour}.
        :param restore_window_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#restore_window_days CloudProviderSnapshotBackupPolicy#restore_window_days}.
        :param update_snapshots: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#update_snapshots CloudProviderSnapshotBackupPolicy#update_snapshots}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feffa8d226c01d18be48de9ed32b8f5ba0989d63d4d100fbd6b2021cd08924e7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument reference_hour_of_day", value=reference_hour_of_day, expected_type=type_hints["reference_hour_of_day"])
            check_type(argname="argument reference_minute_of_hour", value=reference_minute_of_hour, expected_type=type_hints["reference_minute_of_hour"])
            check_type(argname="argument restore_window_days", value=restore_window_days, expected_type=type_hints["restore_window_days"])
            check_type(argname="argument update_snapshots", value=update_snapshots, expected_type=type_hints["update_snapshots"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "policies": policies,
            "project_id": project_id,
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
        if id is not None:
            self._values["id"] = id
        if reference_hour_of_day is not None:
            self._values["reference_hour_of_day"] = reference_hour_of_day
        if reference_minute_of_hour is not None:
            self._values["reference_minute_of_hour"] = reference_minute_of_hour
        if restore_window_days is not None:
            self._values["restore_window_days"] = restore_window_days
        if update_snapshots is not None:
            self._values["update_snapshots"] = update_snapshots

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#cluster_name CloudProviderSnapshotBackupPolicy#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPolicies"]]:
        '''policies block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#policies CloudProviderSnapshotBackupPolicy#policies}
        '''
        result = self._values.get("policies")
        assert result is not None, "Required property 'policies' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPolicies"]], result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#project_id CloudProviderSnapshotBackupPolicy#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_hour_of_day(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_hour_of_day CloudProviderSnapshotBackupPolicy#reference_hour_of_day}.'''
        result = self._values.get("reference_hour_of_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reference_minute_of_hour(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#reference_minute_of_hour CloudProviderSnapshotBackupPolicy#reference_minute_of_hour}.'''
        result = self._values.get("reference_minute_of_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def restore_window_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#restore_window_days CloudProviderSnapshotBackupPolicy#restore_window_days}.'''
        result = self._values.get("restore_window_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_snapshots(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#update_snapshots CloudProviderSnapshotBackupPolicy#update_snapshots}.'''
        result = self._values.get("update_snapshots")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderSnapshotBackupPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPolicies",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "policy_item": "policyItem"},
)
class CloudProviderSnapshotBackupPolicyPolicies:
    def __init__(
        self,
        *,
        id: builtins.str,
        policy_item: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_item: policy_item block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#policy_item CloudProviderSnapshotBackupPolicy#policy_item}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8bbde651bdcac286983a9c181b7a8a670c828ddb21129ba06e41d6b093d152)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_item", value=policy_item, expected_type=type_hints["policy_item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "policy_item": policy_item,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_item(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem"]]:
        '''policy_item block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#policy_item CloudProviderSnapshotBackupPolicy#policy_item}
        '''
        result = self._values.get("policy_item")
        assert result is not None, "Required property 'policy_item' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderSnapshotBackupPolicyPolicies(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudProviderSnapshotBackupPolicyPoliciesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPoliciesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facbfbbd32b3ffeb1963531f02e4e7cd52b261b4894f590f01dd70348c4f01c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudProviderSnapshotBackupPolicyPoliciesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c0a2a5dee5b0fca393e9fdcfa32fc234af3e9c4512c25fd4090417f7d0b71ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudProviderSnapshotBackupPolicyPoliciesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8215b4ea4a4dcdbd25099c4ecae45e7e4d9311185d5fffc84926c0fcbdaf3af8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__795a270a982deb0fea6ed8a1ac735e83f7727b832253c65348bdcd441264b34e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761aebeec56e767001365c3e83617906caa3d8815ef306f42fd2f9f5cdf0fa0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPolicies]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPolicies]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPolicies]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6afa8bbf312d423d779e719d564c991a523a085ccf671ca2a122568fc3ddc79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudProviderSnapshotBackupPolicyPoliciesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPoliciesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1cf728c037b2b56eaa173d01676bae592f68df089757b8503cc870614f1a4e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putPolicyItem")
    def put_policy_item(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22bf10171ff7d04f47ed840dd6abcfecfb8dafa777ff84e4c3477fcd05605391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyItem", [value]))

    @builtins.property
    @jsii.member(jsii_name="policyItem")
    def policy_item(self) -> "CloudProviderSnapshotBackupPolicyPoliciesPolicyItemList":
        return typing.cast("CloudProviderSnapshotBackupPolicyPoliciesPolicyItemList", jsii.get(self, "policyItem"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="policyItemInput")
    def policy_item_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderSnapshotBackupPolicyPoliciesPolicyItem"]]], jsii.get(self, "policyItemInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffb99afc6065938be852e7c48158ea2100caf36458fb833adcfdacec9d3cea73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e8d2703477b081be92b34197715a2d304f55eaa72c3c6b938de462033d334db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPoliciesPolicyItem",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "frequency_type": "frequencyType",
        "id": "id",
        "retention_unit": "retentionUnit",
        "retention_value": "retentionValue",
    },
)
class CloudProviderSnapshotBackupPolicyPoliciesPolicyItem:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        frequency_type: builtins.str,
        id: builtins.str,
        retention_unit: builtins.str,
        retention_value: jsii.Number,
    ) -> None:
        '''
        :param frequency_interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#frequency_interval CloudProviderSnapshotBackupPolicy#frequency_interval}.
        :param frequency_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#frequency_type CloudProviderSnapshotBackupPolicy#frequency_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param retention_unit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#retention_unit CloudProviderSnapshotBackupPolicy#retention_unit}.
        :param retention_value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#retention_value CloudProviderSnapshotBackupPolicy#retention_value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fbc9debb8e4573af8d407dcc9dce4740d9f73b9aaff11530738f85da8f1c92a)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument frequency_type", value=frequency_type, expected_type=type_hints["frequency_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument retention_unit", value=retention_unit, expected_type=type_hints["retention_unit"])
            check_type(argname="argument retention_value", value=retention_value, expected_type=type_hints["retention_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "frequency_type": frequency_type,
            "id": id,
            "retention_unit": retention_unit,
            "retention_value": retention_value,
        }

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#frequency_interval CloudProviderSnapshotBackupPolicy#frequency_interval}.'''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frequency_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#frequency_type CloudProviderSnapshotBackupPolicy#frequency_type}.'''
        result = self._values.get("frequency_type")
        assert result is not None, "Required property 'frequency_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#id CloudProviderSnapshotBackupPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#retention_unit CloudProviderSnapshotBackupPolicy#retention_unit}.'''
        result = self._values.get("retention_unit")
        assert result is not None, "Required property 'retention_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_value(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/cloud_provider_snapshot_backup_policy#retention_value CloudProviderSnapshotBackupPolicy#retention_value}.'''
        result = self._values.get("retention_value")
        assert result is not None, "Required property 'retention_value' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderSnapshotBackupPolicyPoliciesPolicyItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudProviderSnapshotBackupPolicyPoliciesPolicyItemList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPoliciesPolicyItemList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd526475af88d88e6188056194593e778462ab5c9c3c345b3aa4688cc71b762)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudProviderSnapshotBackupPolicyPoliciesPolicyItemOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09bbe9d29fc562ff71d803a466103619ce9af3324353d82c394fd37be7994257)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudProviderSnapshotBackupPolicyPoliciesPolicyItemOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce69c2820013c05ca0d861f7f8e2e454319538a6fe73f9d3d1038fec90cebb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19833c03afbc99263abe7c7d09601849ab64ca6eac6f01f3e930f76ead678b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edc4e1f3ded758baa656e96e5f905de7db8e53d947608ca79bd7525d4b56907d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316334f8a63f56bd76259177a4363c5ed33b14a37d3996575e77a870aa2287b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudProviderSnapshotBackupPolicyPoliciesPolicyItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderSnapshotBackupPolicy.CloudProviderSnapshotBackupPolicyPoliciesPolicyItemOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9e30ce82ef2f73022684066e761330d08d277602be86bcfca3828885e14ae9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyTypeInput")
    def frequency_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionUnitInput")
    def retention_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retentionUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionValueInput")
    def retention_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionValueInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbbdfbee08656c865e6725d2bf465fc0545496f52d7af5aaf21f4c10eb81ed1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="frequencyType")
    def frequency_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyType"))

    @frequency_type.setter
    def frequency_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002789a33ae3bbe350509ff9d3ac7b8225a68b9e21e9dae8c283d3cd4d03952d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1212d909062deb563af82543ceb9a46f9aef484436a8ecc386eebe7aa8acc8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="retentionUnit")
    def retention_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "retentionUnit"))

    @retention_unit.setter
    def retention_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbbaee9b5692d94607927285f3e1841a2bdcb9778ac286c2de9b15e7600b5125)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionUnit", value)

    @builtins.property
    @jsii.member(jsii_name="retentionValue")
    def retention_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionValue"))

    @retention_value.setter
    def retention_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0252afb4b2c3453ea2c03134b8d3c434533c818ef75516afea280320f56111a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionValue", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1c15f29f40bff48d5c7d326819c1b6fda47c31e6db27f0c010cd2dce3e46388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudProviderSnapshotBackupPolicy",
    "CloudProviderSnapshotBackupPolicyConfig",
    "CloudProviderSnapshotBackupPolicyPolicies",
    "CloudProviderSnapshotBackupPolicyPoliciesList",
    "CloudProviderSnapshotBackupPolicyPoliciesOutputReference",
    "CloudProviderSnapshotBackupPolicyPoliciesPolicyItem",
    "CloudProviderSnapshotBackupPolicyPoliciesPolicyItemList",
    "CloudProviderSnapshotBackupPolicyPoliciesPolicyItemOutputReference",
]

publication.publish()

def _typecheckingstub__9b319eb65f74111acd1762dbfc7943e39184bb53538293de1011e34cac52322f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, typing.Dict[builtins.str, typing.Any]]]],
    project_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    reference_hour_of_day: typing.Optional[jsii.Number] = None,
    reference_minute_of_hour: typing.Optional[jsii.Number] = None,
    restore_window_days: typing.Optional[jsii.Number] = None,
    update_snapshots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__a13fd468e2948df8648ba432d5c2fe660b7c4ff407984fc2d6c875b8bdda0178(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0910df5d7c1ceb854c437a06bf12d710d06d6be6ede9decdd1f4b33f8ba7e140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d696c02c91b416a602577ad6f4474377d28e2296cef9a46858591a77bc5fe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47185e8c32776f667111cfa8aece9b4a510eb2087f884ff6ce56242950139b87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab7611c581c360bcb19fdb3f991ef5e57cbe6a2044670120c681e7fbd3fa95da(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98abb066d6cc15a881283ed2c46676567d6b6a2af483bd1f659a516cb71ca962(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675d04be3a23235fab8ab07a275ff94c999a22642604b368a7afe0f065019043(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8395f97d3626b19c182bf91f8621d402feef647901405e71af8ae9b6844f0dad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feffa8d226c01d18be48de9ed32b8f5ba0989d63d4d100fbd6b2021cd08924e7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    policies: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, typing.Dict[builtins.str, typing.Any]]]],
    project_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
    reference_hour_of_day: typing.Optional[jsii.Number] = None,
    reference_minute_of_hour: typing.Optional[jsii.Number] = None,
    restore_window_days: typing.Optional[jsii.Number] = None,
    update_snapshots: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8bbde651bdcac286983a9c181b7a8a670c828ddb21129ba06e41d6b093d152(
    *,
    id: builtins.str,
    policy_item: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facbfbbd32b3ffeb1963531f02e4e7cd52b261b4894f590f01dd70348c4f01c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c0a2a5dee5b0fca393e9fdcfa32fc234af3e9c4512c25fd4090417f7d0b71ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8215b4ea4a4dcdbd25099c4ecae45e7e4d9311185d5fffc84926c0fcbdaf3af8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__795a270a982deb0fea6ed8a1ac735e83f7727b832253c65348bdcd441264b34e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761aebeec56e767001365c3e83617906caa3d8815ef306f42fd2f9f5cdf0fa0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6afa8bbf312d423d779e719d564c991a523a085ccf671ca2a122568fc3ddc79(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPolicies]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1cf728c037b2b56eaa173d01676bae592f68df089757b8503cc870614f1a4e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22bf10171ff7d04f47ed840dd6abcfecfb8dafa777ff84e4c3477fcd05605391(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffb99afc6065938be852e7c48158ea2100caf36458fb833adcfdacec9d3cea73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e8d2703477b081be92b34197715a2d304f55eaa72c3c6b938de462033d334db(
    value: typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPolicies, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbc9debb8e4573af8d407dcc9dce4740d9f73b9aaff11530738f85da8f1c92a(
    *,
    frequency_interval: jsii.Number,
    frequency_type: builtins.str,
    id: builtins.str,
    retention_unit: builtins.str,
    retention_value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd526475af88d88e6188056194593e778462ab5c9c3c345b3aa4688cc71b762(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09bbe9d29fc562ff71d803a466103619ce9af3324353d82c394fd37be7994257(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce69c2820013c05ca0d861f7f8e2e454319538a6fe73f9d3d1038fec90cebb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19833c03afbc99263abe7c7d09601849ab64ca6eac6f01f3e930f76ead678b7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc4e1f3ded758baa656e96e5f905de7db8e53d947608ca79bd7525d4b56907d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316334f8a63f56bd76259177a4363c5ed33b14a37d3996575e77a870aa2287b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9e30ce82ef2f73022684066e761330d08d277602be86bcfca3828885e14ae9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbbdfbee08656c865e6725d2bf465fc0545496f52d7af5aaf21f4c10eb81ed1d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002789a33ae3bbe350509ff9d3ac7b8225a68b9e21e9dae8c283d3cd4d03952d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1212d909062deb563af82543ceb9a46f9aef484436a8ecc386eebe7aa8acc8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbbaee9b5692d94607927285f3e1841a2bdcb9778ac286c2de9b15e7600b5125(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0252afb4b2c3453ea2c03134b8d3c434533c818ef75516afea280320f56111a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1c15f29f40bff48d5c7d326819c1b6fda47c31e6db27f0c010cd2dce3e46388(
    value: typing.Optional[typing.Union[CloudProviderSnapshotBackupPolicyPoliciesPolicyItem, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
