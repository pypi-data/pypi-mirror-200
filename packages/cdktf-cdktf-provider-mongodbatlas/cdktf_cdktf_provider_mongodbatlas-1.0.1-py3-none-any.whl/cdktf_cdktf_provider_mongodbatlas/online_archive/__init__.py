'''
# `mongodbatlas_online_archive`

Refer to the Terraform Registory for docs: [`mongodbatlas_online_archive`](https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive).
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


class OnlineArchive(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchive",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive mongodbatlas_online_archive}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        coll_name: builtins.str,
        criteria: typing.Union["OnlineArchiveCriteria", typing.Dict[builtins.str, typing.Any]],
        db_name: builtins.str,
        project_id: builtins.str,
        collection_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        partition_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnlineArchivePartitionFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive mongodbatlas_online_archive} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#cluster_name OnlineArchive#cluster_name}.
        :param coll_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#coll_name OnlineArchive#coll_name}.
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#criteria OnlineArchive#criteria}
        :param db_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#db_name OnlineArchive#db_name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#project_id OnlineArchive#project_id}.
        :param collection_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#collection_type OnlineArchive#collection_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#id OnlineArchive#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_fields: partition_fields block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#partition_fields OnlineArchive#partition_fields}
        :param paused: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#paused OnlineArchive#paused}.
        :param sync_creation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#sync_creation OnlineArchive#sync_creation}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd8d1ca11c164ab0d5dc5e06d9e71c8db190f43b7a833f46b312e4686fcae23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OnlineArchiveConfig(
            cluster_name=cluster_name,
            coll_name=coll_name,
            criteria=criteria,
            db_name=db_name,
            project_id=project_id,
            collection_type=collection_type,
            id=id,
            partition_fields=partition_fields,
            paused=paused,
            sync_creation=sync_creation,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCriteria")
    def put_criteria(
        self,
        *,
        type: builtins.str,
        date_field: typing.Optional[builtins.str] = None,
        date_format: typing.Optional[builtins.str] = None,
        expire_after_days: typing.Optional[jsii.Number] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#type OnlineArchive#type}.
        :param date_field: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_field OnlineArchive#date_field}.
        :param date_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_format OnlineArchive#date_format}.
        :param expire_after_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#expire_after_days OnlineArchive#expire_after_days}.
        :param query: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#query OnlineArchive#query}.
        '''
        value = OnlineArchiveCriteria(
            type=type,
            date_field=date_field,
            date_format=date_format,
            expire_after_days=expire_after_days,
            query=query,
        )

        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

    @jsii.member(jsii_name="putPartitionFields")
    def put_partition_fields(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnlineArchivePartitionFields", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e5606784d6acac975631ea2af1161f22ad81d1d668f072c7130ebae2a4b904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPartitionFields", [value]))

    @jsii.member(jsii_name="resetCollectionType")
    def reset_collection_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPartitionFields")
    def reset_partition_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPartitionFields", []))

    @jsii.member(jsii_name="resetPaused")
    def reset_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaused", []))

    @jsii.member(jsii_name="resetSyncCreation")
    def reset_sync_creation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyncCreation", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="archiveId")
    def archive_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "archiveId"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> "OnlineArchiveCriteriaOutputReference":
        return typing.cast("OnlineArchiveCriteriaOutputReference", jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="partitionFields")
    def partition_fields(self) -> "OnlineArchivePartitionFieldsList":
        return typing.cast("OnlineArchivePartitionFieldsList", jsii.get(self, "partitionFields"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionTypeInput")
    def collection_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="collNameInput")
    def coll_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collNameInput"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional["OnlineArchiveCriteria"]:
        return typing.cast(typing.Optional["OnlineArchiveCriteria"], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="dbNameInput")
    def db_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="partitionFieldsInput")
    def partition_fields_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnlineArchivePartitionFields"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnlineArchivePartitionFields"]]], jsii.get(self, "partitionFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="pausedInput")
    def paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pausedInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="syncCreationInput")
    def sync_creation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "syncCreationInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8ae41e4f876927ef6981d0b7733937af86ae48eef04c7e84176df670d4d407)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="collectionType")
    def collection_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionType"))

    @collection_type.setter
    def collection_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a4379a10167c092c00fdc988318e28f67ce2718a6a8ee77cd54add0ccfef334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionType", value)

    @builtins.property
    @jsii.member(jsii_name="collName")
    def coll_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collName"))

    @coll_name.setter
    def coll_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d037e4474bfd5c2e1333006f2df70dcdc006a9730cb12cdd7f93e621179f0d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collName", value)

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbName"))

    @db_name.setter
    def db_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__980c51108ac5c6046b9e7ac7aa2d3b50ff4e2a59f4017e3312afc6855606730c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ab4336f292487179519348dcc4aec8d86a3848384ded4433c07070dbce697d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="paused")
    def paused(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "paused"))

    @paused.setter
    def paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b151595b2c0db02b6ba933ac0f0af01ed2cae3b3e6a98c2c0b0cf315423aee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f015421bc7c023003d29dff1bf83dd6df11009d9f219d612275aa1c7cfd6c69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="syncCreation")
    def sync_creation(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "syncCreation"))

    @sync_creation.setter
    def sync_creation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6764ebedc8392745886f1bdf0cd6cf1c67bc0c1261d3de37bf3dcc4e6ac0163c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncCreation", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchiveConfig",
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
        "coll_name": "collName",
        "criteria": "criteria",
        "db_name": "dbName",
        "project_id": "projectId",
        "collection_type": "collectionType",
        "id": "id",
        "partition_fields": "partitionFields",
        "paused": "paused",
        "sync_creation": "syncCreation",
    },
)
class OnlineArchiveConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        coll_name: builtins.str,
        criteria: typing.Union["OnlineArchiveCriteria", typing.Dict[builtins.str, typing.Any]],
        db_name: builtins.str,
        project_id: builtins.str,
        collection_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        partition_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OnlineArchivePartitionFields", typing.Dict[builtins.str, typing.Any]]]]] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sync_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#cluster_name OnlineArchive#cluster_name}.
        :param coll_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#coll_name OnlineArchive#coll_name}.
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#criteria OnlineArchive#criteria}
        :param db_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#db_name OnlineArchive#db_name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#project_id OnlineArchive#project_id}.
        :param collection_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#collection_type OnlineArchive#collection_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#id OnlineArchive#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param partition_fields: partition_fields block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#partition_fields OnlineArchive#partition_fields}
        :param paused: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#paused OnlineArchive#paused}.
        :param sync_creation: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#sync_creation OnlineArchive#sync_creation}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(criteria, dict):
            criteria = OnlineArchiveCriteria(**criteria)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a399df69abc4c0e11be19164b166682ee8e362c29595e11f7e4a9e0c6c2ad7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument coll_name", value=coll_name, expected_type=type_hints["coll_name"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument db_name", value=db_name, expected_type=type_hints["db_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument collection_type", value=collection_type, expected_type=type_hints["collection_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument partition_fields", value=partition_fields, expected_type=type_hints["partition_fields"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument sync_creation", value=sync_creation, expected_type=type_hints["sync_creation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "coll_name": coll_name,
            "criteria": criteria,
            "db_name": db_name,
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
        if collection_type is not None:
            self._values["collection_type"] = collection_type
        if id is not None:
            self._values["id"] = id
        if partition_fields is not None:
            self._values["partition_fields"] = partition_fields
        if paused is not None:
            self._values["paused"] = paused
        if sync_creation is not None:
            self._values["sync_creation"] = sync_creation

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#cluster_name OnlineArchive#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def coll_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#coll_name OnlineArchive#coll_name}.'''
        result = self._values.get("coll_name")
        assert result is not None, "Required property 'coll_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def criteria(self) -> "OnlineArchiveCriteria":
        '''criteria block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#criteria OnlineArchive#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast("OnlineArchiveCriteria", result)

    @builtins.property
    def db_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#db_name OnlineArchive#db_name}.'''
        result = self._values.get("db_name")
        assert result is not None, "Required property 'db_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#project_id OnlineArchive#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def collection_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#collection_type OnlineArchive#collection_type}.'''
        result = self._values.get("collection_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#id OnlineArchive#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partition_fields(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnlineArchivePartitionFields"]]]:
        '''partition_fields block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#partition_fields OnlineArchive#partition_fields}
        '''
        result = self._values.get("partition_fields")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OnlineArchivePartitionFields"]]], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#paused OnlineArchive#paused}.'''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sync_creation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#sync_creation OnlineArchive#sync_creation}.'''
        result = self._values.get("sync_creation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnlineArchiveConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchiveCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "date_field": "dateField",
        "date_format": "dateFormat",
        "expire_after_days": "expireAfterDays",
        "query": "query",
    },
)
class OnlineArchiveCriteria:
    def __init__(
        self,
        *,
        type: builtins.str,
        date_field: typing.Optional[builtins.str] = None,
        date_format: typing.Optional[builtins.str] = None,
        expire_after_days: typing.Optional[jsii.Number] = None,
        query: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#type OnlineArchive#type}.
        :param date_field: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_field OnlineArchive#date_field}.
        :param date_format: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_format OnlineArchive#date_format}.
        :param expire_after_days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#expire_after_days OnlineArchive#expire_after_days}.
        :param query: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#query OnlineArchive#query}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9b0b18cf84be268a917e922a7b1486394bf8dcaa355159d231e29a3b09d8cb)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument date_field", value=date_field, expected_type=type_hints["date_field"])
            check_type(argname="argument date_format", value=date_format, expected_type=type_hints["date_format"])
            check_type(argname="argument expire_after_days", value=expire_after_days, expected_type=type_hints["expire_after_days"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if date_field is not None:
            self._values["date_field"] = date_field
        if date_format is not None:
            self._values["date_format"] = date_format
        if expire_after_days is not None:
            self._values["expire_after_days"] = expire_after_days
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#type OnlineArchive#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def date_field(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_field OnlineArchive#date_field}.'''
        result = self._values.get("date_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def date_format(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#date_format OnlineArchive#date_format}.'''
        result = self._values.get("date_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expire_after_days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#expire_after_days OnlineArchive#expire_after_days}.'''
        result = self._values.get("expire_after_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def query(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#query OnlineArchive#query}.'''
        result = self._values.get("query")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnlineArchiveCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnlineArchiveCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchiveCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f5d56d7afb608711f4001474fc1960b5ef61c1007b1880263ec771d518358a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDateField")
    def reset_date_field(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateField", []))

    @jsii.member(jsii_name="resetDateFormat")
    def reset_date_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDateFormat", []))

    @jsii.member(jsii_name="resetExpireAfterDays")
    def reset_expire_after_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpireAfterDays", []))

    @jsii.member(jsii_name="resetQuery")
    def reset_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuery", []))

    @builtins.property
    @jsii.member(jsii_name="dateFieldInput")
    def date_field_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateFieldInput"))

    @builtins.property
    @jsii.member(jsii_name="dateFormatInput")
    def date_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dateFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="expireAfterDaysInput")
    def expire_after_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expireAfterDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="dateField")
    def date_field(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateField"))

    @date_field.setter
    def date_field(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4e0ba20e5b0b862a63f04f8445b804f602e228975c1c15450e8de0f96e0bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateField", value)

    @builtins.property
    @jsii.member(jsii_name="dateFormat")
    def date_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dateFormat"))

    @date_format.setter
    def date_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ff4e23db3310b4c344d21b5fb85f472e39c27e390b512bcd36e2504b162226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dateFormat", value)

    @builtins.property
    @jsii.member(jsii_name="expireAfterDays")
    def expire_after_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expireAfterDays"))

    @expire_after_days.setter
    def expire_after_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b040cc2a804a0ef1028330d95e8f0aeb2ed271aed90dfcba97f5967358621638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expireAfterDays", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00641548134174b7ab92d5909d3ba34e512ae7f35d514f6e505c3411d03b06dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc035f2c577002ef8ff134389ae108e15bd730d2cae670cd5c9f8d162d84b59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OnlineArchiveCriteria]:
        return typing.cast(typing.Optional[OnlineArchiveCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[OnlineArchiveCriteria]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59393b6de332aac17ee2147a65ab972be7a7d450cebedc3e0d884aa56a461924)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchivePartitionFields",
    jsii_struct_bases=[],
    name_mapping={"field_name": "fieldName", "order": "order"},
)
class OnlineArchivePartitionFields:
    def __init__(self, *, field_name: builtins.str, order: jsii.Number) -> None:
        '''
        :param field_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#field_name OnlineArchive#field_name}.
        :param order: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#order OnlineArchive#order}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47523a901d278ea6b9c4e5ef4ba1d86916903ba0a9b473509ed58bde34c93066)
            check_type(argname="argument field_name", value=field_name, expected_type=type_hints["field_name"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "field_name": field_name,
            "order": order,
        }

    @builtins.property
    def field_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#field_name OnlineArchive#field_name}.'''
        result = self._values.get("field_name")
        assert result is not None, "Required property 'field_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/online_archive#order OnlineArchive#order}.'''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OnlineArchivePartitionFields(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OnlineArchivePartitionFieldsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchivePartitionFieldsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a22e5aeaa7d49a8304106c78c62dfbb591260920db5f5e1686e5833d2e102d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OnlineArchivePartitionFieldsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6d1f35898175c00aca4de2eea2708b960ab85fdb7c4fb52024b7d03a51c6ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OnlineArchivePartitionFieldsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4c9f82b054eeb30c8064ab3d12fb54690594cc9e0a082206af11c74e69fddc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db9dc27b42f707d926c6b3447c7a76f06e246aab5b8f48b59ce6fb840ec5196)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2386e9e4182df9872320ee0e4df089ddde504f3f4ef54846d7e92ff1cce0b87b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnlineArchivePartitionFields]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnlineArchivePartitionFields]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnlineArchivePartitionFields]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f02dba3058b1ca7823aa00ab2f579108d287a10642dd3b51b0f8308cdd7f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OnlineArchivePartitionFieldsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.onlineArchive.OnlineArchivePartitionFieldsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15485242bf225f68d9d49a65f30304a4e6056f995968594c12e96c49b82c270a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="fieldType")
    def field_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldType"))

    @builtins.property
    @jsii.member(jsii_name="fieldNameInput")
    def field_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fieldNameInput"))

    @builtins.property
    @jsii.member(jsii_name="orderInput")
    def order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "orderInput"))

    @builtins.property
    @jsii.member(jsii_name="fieldName")
    def field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fieldName"))

    @field_name.setter
    def field_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88d32d4cb751ba46749055e9da2d8888c8ff2d1d176fedf6f1d5dd40bde20586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fieldName", value)

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "order"))

    @order.setter
    def order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b40cc701819af6294c13317a2303fa116b2a03e8b58a3a5cb275920671240e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OnlineArchivePartitionFields, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OnlineArchivePartitionFields, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OnlineArchivePartitionFields, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09eec2ebd86060da8dd71e2d96c173356d482aa746a97c20e1ddc55383d9bd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OnlineArchive",
    "OnlineArchiveConfig",
    "OnlineArchiveCriteria",
    "OnlineArchiveCriteriaOutputReference",
    "OnlineArchivePartitionFields",
    "OnlineArchivePartitionFieldsList",
    "OnlineArchivePartitionFieldsOutputReference",
]

publication.publish()

def _typecheckingstub__1dd8d1ca11c164ab0d5dc5e06d9e71c8db190f43b7a833f46b312e4686fcae23(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    coll_name: builtins.str,
    criteria: typing.Union[OnlineArchiveCriteria, typing.Dict[builtins.str, typing.Any]],
    db_name: builtins.str,
    project_id: builtins.str,
    collection_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    partition_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnlineArchivePartitionFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__76e5606784d6acac975631ea2af1161f22ad81d1d668f072c7130ebae2a4b904(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnlineArchivePartitionFields, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8ae41e4f876927ef6981d0b7733937af86ae48eef04c7e84176df670d4d407(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a4379a10167c092c00fdc988318e28f67ce2718a6a8ee77cd54add0ccfef334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d037e4474bfd5c2e1333006f2df70dcdc006a9730cb12cdd7f93e621179f0d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980c51108ac5c6046b9e7ac7aa2d3b50ff4e2a59f4017e3312afc6855606730c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ab4336f292487179519348dcc4aec8d86a3848384ded4433c07070dbce697d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b151595b2c0db02b6ba933ac0f0af01ed2cae3b3e6a98c2c0b0cf315423aee(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f015421bc7c023003d29dff1bf83dd6df11009d9f219d612275aa1c7cfd6c69a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6764ebedc8392745886f1bdf0cd6cf1c67bc0c1261d3de37bf3dcc4e6ac0163c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a399df69abc4c0e11be19164b166682ee8e362c29595e11f7e4a9e0c6c2ad7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    coll_name: builtins.str,
    criteria: typing.Union[OnlineArchiveCriteria, typing.Dict[builtins.str, typing.Any]],
    db_name: builtins.str,
    project_id: builtins.str,
    collection_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    partition_fields: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OnlineArchivePartitionFields, typing.Dict[builtins.str, typing.Any]]]]] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sync_creation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9b0b18cf84be268a917e922a7b1486394bf8dcaa355159d231e29a3b09d8cb(
    *,
    type: builtins.str,
    date_field: typing.Optional[builtins.str] = None,
    date_format: typing.Optional[builtins.str] = None,
    expire_after_days: typing.Optional[jsii.Number] = None,
    query: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f5d56d7afb608711f4001474fc1960b5ef61c1007b1880263ec771d518358a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4e0ba20e5b0b862a63f04f8445b804f602e228975c1c15450e8de0f96e0bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ff4e23db3310b4c344d21b5fb85f472e39c27e390b512bcd36e2504b162226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b040cc2a804a0ef1028330d95e8f0aeb2ed271aed90dfcba97f5967358621638(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00641548134174b7ab92d5909d3ba34e512ae7f35d514f6e505c3411d03b06dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc035f2c577002ef8ff134389ae108e15bd730d2cae670cd5c9f8d162d84b59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59393b6de332aac17ee2147a65ab972be7a7d450cebedc3e0d884aa56a461924(
    value: typing.Optional[OnlineArchiveCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47523a901d278ea6b9c4e5ef4ba1d86916903ba0a9b473509ed58bde34c93066(
    *,
    field_name: builtins.str,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a22e5aeaa7d49a8304106c78c62dfbb591260920db5f5e1686e5833d2e102d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6d1f35898175c00aca4de2eea2708b960ab85fdb7c4fb52024b7d03a51c6ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4c9f82b054eeb30c8064ab3d12fb54690594cc9e0a082206af11c74e69fddc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db9dc27b42f707d926c6b3447c7a76f06e246aab5b8f48b59ce6fb840ec5196(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2386e9e4182df9872320ee0e4df089ddde504f3f4ef54846d7e92ff1cce0b87b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f02dba3058b1ca7823aa00ab2f579108d287a10642dd3b51b0f8308cdd7f19(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OnlineArchivePartitionFields]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15485242bf225f68d9d49a65f30304a4e6056f995968594c12e96c49b82c270a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88d32d4cb751ba46749055e9da2d8888c8ff2d1d176fedf6f1d5dd40bde20586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40cc701819af6294c13317a2303fa116b2a03e8b58a3a5cb275920671240e4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09eec2ebd86060da8dd71e2d96c173356d482aa746a97c20e1ddc55383d9bd09(
    value: typing.Optional[typing.Union[OnlineArchivePartitionFields, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
