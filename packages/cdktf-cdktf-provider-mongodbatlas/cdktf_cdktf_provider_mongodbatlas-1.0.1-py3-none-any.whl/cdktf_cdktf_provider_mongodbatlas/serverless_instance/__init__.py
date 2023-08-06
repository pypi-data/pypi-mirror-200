'''
# `mongodbatlas_serverless_instance`

Refer to the Terraform Registory for docs: [`mongodbatlas_serverless_instance`](https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance).
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


class ServerlessInstance(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.serverlessInstance.ServerlessInstance",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance mongodbatlas_serverless_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        project_id: builtins.str,
        provider_settings_backing_provider_name: builtins.str,
        provider_settings_provider_name: builtins.str,
        provider_settings_region_name: builtins.str,
        continuous_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServerlessInstanceLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        state_name: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance mongodbatlas_serverless_instance} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#name ServerlessInstance#name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#project_id ServerlessInstance#project_id}.
        :param provider_settings_backing_provider_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_backing_provider_name ServerlessInstance#provider_settings_backing_provider_name}.
        :param provider_settings_provider_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_provider_name ServerlessInstance#provider_settings_provider_name}.
        :param provider_settings_region_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_region_name ServerlessInstance#provider_settings_region_name}.
        :param continuous_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#continuous_backup_enabled ServerlessInstance#continuous_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#id ServerlessInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param links: links block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#links ServerlessInstance#links}
        :param state_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#state_name ServerlessInstance#state_name}.
        :param termination_protection_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#termination_protection_enabled ServerlessInstance#termination_protection_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1c57ab5b011d24125c06a18be4d15bbc071d39449a026fd18f346050a497c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServerlessInstanceConfig(
            name=name,
            project_id=project_id,
            provider_settings_backing_provider_name=provider_settings_backing_provider_name,
            provider_settings_provider_name=provider_settings_provider_name,
            provider_settings_region_name=provider_settings_region_name,
            continuous_backup_enabled=continuous_backup_enabled,
            id=id,
            links=links,
            state_name=state_name,
            termination_protection_enabled=termination_protection_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLinks")
    def put_links(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServerlessInstanceLinks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396849f0d3dee3ece1a4e003e33248b037ce40c28707911ee78934efe0c73fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLinks", [value]))

    @jsii.member(jsii_name="resetContinuousBackupEnabled")
    def reset_continuous_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContinuousBackupEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLinks")
    def reset_links(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinks", []))

    @jsii.member(jsii_name="resetStateName")
    def reset_state_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStateName", []))

    @jsii.member(jsii_name="resetTerminationProtectionEnabled")
    def reset_termination_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationProtectionEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringsPrivateEndpointSrv")
    def connection_strings_private_endpoint_srv(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectionStringsPrivateEndpointSrv"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringsStandardSrv")
    def connection_strings_standard_srv(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionStringsStandardSrv"))

    @builtins.property
    @jsii.member(jsii_name="createDate")
    def create_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createDate"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> "ServerlessInstanceLinksList":
        return typing.cast("ServerlessInstanceLinksList", jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="mongoDbVersion")
    def mongo_db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoDbVersion"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupEnabledInput")
    def continuous_backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "continuousBackupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="linksInput")
    def links_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServerlessInstanceLinks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServerlessInstanceLinks"]]], jsii.get(self, "linksInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerSettingsBackingProviderNameInput")
    def provider_settings_backing_provider_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerSettingsBackingProviderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerSettingsProviderNameInput")
    def provider_settings_provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerSettingsProviderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="providerSettingsRegionNameInput")
    def provider_settings_region_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerSettingsRegionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="stateNameInput")
    def state_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationProtectionEnabledInput")
    def termination_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminationProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="continuousBackupEnabled")
    def continuous_backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "continuousBackupEnabled"))

    @continuous_backup_enabled.setter
    def continuous_backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e3f5ea96006d48fd4b906c87141fe7726fa68713acbd2c215a7669d1d89d38b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "continuousBackupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c606b020bdfecaf59a3ce9d96716a15894441074a651b408516c1460facaaa5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e505a331d71cf9f4acde44506c66237b52aeb04dd0dcb6bf4f1005ca290feece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b385e3f377e90a68f60ff5b43865b88211856a7df0b5e680b99bdca022d81de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="providerSettingsBackingProviderName")
    def provider_settings_backing_provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerSettingsBackingProviderName"))

    @provider_settings_backing_provider_name.setter
    def provider_settings_backing_provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89dc00d25f82ad037f1b41412b6f0477cf913858333574c51a63b1915def5e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerSettingsBackingProviderName", value)

    @builtins.property
    @jsii.member(jsii_name="providerSettingsProviderName")
    def provider_settings_provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerSettingsProviderName"))

    @provider_settings_provider_name.setter
    def provider_settings_provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b57ea5da28d52b3392c81639326ca054eb41dffb6eaf2709a288fb49c46c958)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerSettingsProviderName", value)

    @builtins.property
    @jsii.member(jsii_name="providerSettingsRegionName")
    def provider_settings_region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerSettingsRegionName"))

    @provider_settings_region_name.setter
    def provider_settings_region_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78fb1b868364fd24c32b712a0788785e65c532e2154ee569c217ad80b4c7185c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerSettingsRegionName", value)

    @builtins.property
    @jsii.member(jsii_name="stateName")
    def state_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateName"))

    @state_name.setter
    def state_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a266b907e420455c7de96b08e9688c5cee4abc8e5830647a8a4b0a534c7e908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateName", value)

    @builtins.property
    @jsii.member(jsii_name="terminationProtectionEnabled")
    def termination_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminationProtectionEnabled"))

    @termination_protection_enabled.setter
    def termination_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244178e221e0033ab26f51f18071c0057a95f6f15eb170775fa69d27c770c371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationProtectionEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.serverlessInstance.ServerlessInstanceConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "project_id": "projectId",
        "provider_settings_backing_provider_name": "providerSettingsBackingProviderName",
        "provider_settings_provider_name": "providerSettingsProviderName",
        "provider_settings_region_name": "providerSettingsRegionName",
        "continuous_backup_enabled": "continuousBackupEnabled",
        "id": "id",
        "links": "links",
        "state_name": "stateName",
        "termination_protection_enabled": "terminationProtectionEnabled",
    },
)
class ServerlessInstanceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        project_id: builtins.str,
        provider_settings_backing_provider_name: builtins.str,
        provider_settings_provider_name: builtins.str,
        provider_settings_region_name: builtins.str,
        continuous_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServerlessInstanceLinks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        state_name: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#name ServerlessInstance#name}.
        :param project_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#project_id ServerlessInstance#project_id}.
        :param provider_settings_backing_provider_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_backing_provider_name ServerlessInstance#provider_settings_backing_provider_name}.
        :param provider_settings_provider_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_provider_name ServerlessInstance#provider_settings_provider_name}.
        :param provider_settings_region_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_region_name ServerlessInstance#provider_settings_region_name}.
        :param continuous_backup_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#continuous_backup_enabled ServerlessInstance#continuous_backup_enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#id ServerlessInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param links: links block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#links ServerlessInstance#links}
        :param state_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#state_name ServerlessInstance#state_name}.
        :param termination_protection_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#termination_protection_enabled ServerlessInstance#termination_protection_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bb064b62e5425052ea4f8350e3be376330b266d7fca40f882553f3e4ce453c8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument provider_settings_backing_provider_name", value=provider_settings_backing_provider_name, expected_type=type_hints["provider_settings_backing_provider_name"])
            check_type(argname="argument provider_settings_provider_name", value=provider_settings_provider_name, expected_type=type_hints["provider_settings_provider_name"])
            check_type(argname="argument provider_settings_region_name", value=provider_settings_region_name, expected_type=type_hints["provider_settings_region_name"])
            check_type(argname="argument continuous_backup_enabled", value=continuous_backup_enabled, expected_type=type_hints["continuous_backup_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument links", value=links, expected_type=type_hints["links"])
            check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
            "provider_settings_backing_provider_name": provider_settings_backing_provider_name,
            "provider_settings_provider_name": provider_settings_provider_name,
            "provider_settings_region_name": provider_settings_region_name,
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
        if continuous_backup_enabled is not None:
            self._values["continuous_backup_enabled"] = continuous_backup_enabled
        if id is not None:
            self._values["id"] = id
        if links is not None:
            self._values["links"] = links
        if state_name is not None:
            self._values["state_name"] = state_name
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#name ServerlessInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#project_id ServerlessInstance#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_settings_backing_provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_backing_provider_name ServerlessInstance#provider_settings_backing_provider_name}.'''
        result = self._values.get("provider_settings_backing_provider_name")
        assert result is not None, "Required property 'provider_settings_backing_provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_settings_provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_provider_name ServerlessInstance#provider_settings_provider_name}.'''
        result = self._values.get("provider_settings_provider_name")
        assert result is not None, "Required property 'provider_settings_provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_settings_region_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#provider_settings_region_name ServerlessInstance#provider_settings_region_name}.'''
        result = self._values.get("provider_settings_region_name")
        assert result is not None, "Required property 'provider_settings_region_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def continuous_backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#continuous_backup_enabled ServerlessInstance#continuous_backup_enabled}.'''
        result = self._values.get("continuous_backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#id ServerlessInstance#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def links(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServerlessInstanceLinks"]]]:
        '''links block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#links ServerlessInstance#links}
        '''
        result = self._values.get("links")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServerlessInstanceLinks"]]], result)

    @builtins.property
    def state_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#state_name ServerlessInstance#state_name}.'''
        result = self._values.get("state_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/serverless_instance#termination_protection_enabled ServerlessInstance#termination_protection_enabled}.'''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.serverlessInstance.ServerlessInstanceLinks",
    jsii_struct_bases=[],
    name_mapping={},
)
class ServerlessInstanceLinks:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerlessInstanceLinks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServerlessInstanceLinksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.serverlessInstance.ServerlessInstanceLinksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1776972ad46c16a9b754fb5fd7a4bb3f506d6f59c2f3eebd75f7dc0dd4952f1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServerlessInstanceLinksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e7f3c4c2f1845117fe40f8a46dedce32ac01eab096650ee47a7939eec4e7b69)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServerlessInstanceLinksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc600ce37be450559f518c60073bf9e2a04062be93283eaec18b1f154ca62d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cab0606c3534a09faca89779b39029cf9aa1558b6517f1857a2a086a8791f7e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5032028fe0c3682c40ff8e0e90b98eee7dfbb0ed1a1f3f57f8304abb92b42467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServerlessInstanceLinks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServerlessInstanceLinks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServerlessInstanceLinks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c5a7aacdbe254706b147652e2fed1be2b0f2c5926d94a9b5662a1ffbddb7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ServerlessInstanceLinksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.serverlessInstance.ServerlessInstanceLinksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e79d7a59c7783dd6f22d9aa82f6deaab94720007996ea121089dae503372148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="href")
    def href(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "href"))

    @builtins.property
    @jsii.member(jsii_name="rel")
    def rel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rel"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ServerlessInstanceLinks, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ServerlessInstanceLinks, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ServerlessInstanceLinks, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2be551512726498eb2723ad0a989b77d9f2225f7f53608d9a7f555066b3e1638)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ServerlessInstance",
    "ServerlessInstanceConfig",
    "ServerlessInstanceLinks",
    "ServerlessInstanceLinksList",
    "ServerlessInstanceLinksOutputReference",
]

publication.publish()

def _typecheckingstub__4e1c57ab5b011d24125c06a18be4d15bbc071d39449a026fd18f346050a497c7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    project_id: builtins.str,
    provider_settings_backing_provider_name: builtins.str,
    provider_settings_provider_name: builtins.str,
    provider_settings_region_name: builtins.str,
    continuous_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServerlessInstanceLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    state_name: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__396849f0d3dee3ece1a4e003e33248b037ce40c28707911ee78934efe0c73fc6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServerlessInstanceLinks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e3f5ea96006d48fd4b906c87141fe7726fa68713acbd2c215a7669d1d89d38b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c606b020bdfecaf59a3ce9d96716a15894441074a651b408516c1460facaaa5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e505a331d71cf9f4acde44506c66237b52aeb04dd0dcb6bf4f1005ca290feece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b385e3f377e90a68f60ff5b43865b88211856a7df0b5e680b99bdca022d81de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89dc00d25f82ad037f1b41412b6f0477cf913858333574c51a63b1915def5e28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b57ea5da28d52b3392c81639326ca054eb41dffb6eaf2709a288fb49c46c958(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78fb1b868364fd24c32b712a0788785e65c532e2154ee569c217ad80b4c7185c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a266b907e420455c7de96b08e9688c5cee4abc8e5830647a8a4b0a534c7e908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244178e221e0033ab26f51f18071c0057a95f6f15eb170775fa69d27c770c371(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb064b62e5425052ea4f8350e3be376330b266d7fca40f882553f3e4ce453c8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    project_id: builtins.str,
    provider_settings_backing_provider_name: builtins.str,
    provider_settings_provider_name: builtins.str,
    provider_settings_region_name: builtins.str,
    continuous_backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    links: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServerlessInstanceLinks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    state_name: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1776972ad46c16a9b754fb5fd7a4bb3f506d6f59c2f3eebd75f7dc0dd4952f1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e7f3c4c2f1845117fe40f8a46dedce32ac01eab096650ee47a7939eec4e7b69(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc600ce37be450559f518c60073bf9e2a04062be93283eaec18b1f154ca62d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cab0606c3534a09faca89779b39029cf9aa1558b6517f1857a2a086a8791f7e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5032028fe0c3682c40ff8e0e90b98eee7dfbb0ed1a1f3f57f8304abb92b42467(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c5a7aacdbe254706b147652e2fed1be2b0f2c5926d94a9b5662a1ffbddb7b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServerlessInstanceLinks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e79d7a59c7783dd6f22d9aa82f6deaab94720007996ea121089dae503372148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be551512726498eb2723ad0a989b77d9f2225f7f53608d9a7f555066b3e1638(
    value: typing.Optional[typing.Union[ServerlessInstanceLinks, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
