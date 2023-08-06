'''
# `mongodbatlas_project`

Refer to the Terraform Registory for docs: [`mongodbatlas_project`](https://www.terraform.io/docs/providers/mongodbatlas/r/project).
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


class Project(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.project.Project",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project mongodbatlas_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        org_id: builtins.str,
        api_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectApiKeys", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_collect_database_specifics_statistics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_data_explorer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_performance_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_realtime_performance_panel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_schema_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_owner_id: typing.Optional[builtins.str] = None,
        region_usage_restrictions: typing.Optional[builtins.str] = None,
        teams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectTeams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        with_default_alerts_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project mongodbatlas_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#name Project#name}.
        :param org_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#org_id Project#org_id}.
        :param api_keys: api_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#api_keys Project#api_keys}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_collect_database_specifics_statistics_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_collect_database_specifics_statistics_enabled Project#is_collect_database_specifics_statistics_enabled}.
        :param is_data_explorer_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_data_explorer_enabled Project#is_data_explorer_enabled}.
        :param is_performance_advisor_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_performance_advisor_enabled Project#is_performance_advisor_enabled}.
        :param is_realtime_performance_panel_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_realtime_performance_panel_enabled Project#is_realtime_performance_panel_enabled}.
        :param is_schema_advisor_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_schema_advisor_enabled Project#is_schema_advisor_enabled}.
        :param project_owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#project_owner_id Project#project_owner_id}.
        :param region_usage_restrictions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#region_usage_restrictions Project#region_usage_restrictions}.
        :param teams: teams block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#teams Project#teams}
        :param with_default_alerts_settings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#with_default_alerts_settings Project#with_default_alerts_settings}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7a170c16ee3d7749a2e1a1597ff9942a4f15acab9c14e51e3e2c98f32c7ccd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectConfig(
            name=name,
            org_id=org_id,
            api_keys=api_keys,
            id=id,
            is_collect_database_specifics_statistics_enabled=is_collect_database_specifics_statistics_enabled,
            is_data_explorer_enabled=is_data_explorer_enabled,
            is_performance_advisor_enabled=is_performance_advisor_enabled,
            is_realtime_performance_panel_enabled=is_realtime_performance_panel_enabled,
            is_schema_advisor_enabled=is_schema_advisor_enabled,
            project_owner_id=project_owner_id,
            region_usage_restrictions=region_usage_restrictions,
            teams=teams,
            with_default_alerts_settings=with_default_alerts_settings,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putApiKeys")
    def put_api_keys(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectApiKeys", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1bc813b6a683664ce9ccea88b6c9296792510df59a5b1199d02da3ee75e08e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApiKeys", [value]))

    @jsii.member(jsii_name="putTeams")
    def put_teams(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectTeams", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62db4d9da517db2e656400e303bb2208dca445fbd3b89005ab2ff7b77edadfb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTeams", [value]))

    @jsii.member(jsii_name="resetApiKeys")
    def reset_api_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeys", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsCollectDatabaseSpecificsStatisticsEnabled")
    def reset_is_collect_database_specifics_statistics_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsCollectDatabaseSpecificsStatisticsEnabled", []))

    @jsii.member(jsii_name="resetIsDataExplorerEnabled")
    def reset_is_data_explorer_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsDataExplorerEnabled", []))

    @jsii.member(jsii_name="resetIsPerformanceAdvisorEnabled")
    def reset_is_performance_advisor_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsPerformanceAdvisorEnabled", []))

    @jsii.member(jsii_name="resetIsRealtimePerformancePanelEnabled")
    def reset_is_realtime_performance_panel_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsRealtimePerformancePanelEnabled", []))

    @jsii.member(jsii_name="resetIsSchemaAdvisorEnabled")
    def reset_is_schema_advisor_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsSchemaAdvisorEnabled", []))

    @jsii.member(jsii_name="resetProjectOwnerId")
    def reset_project_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectOwnerId", []))

    @jsii.member(jsii_name="resetRegionUsageRestrictions")
    def reset_region_usage_restrictions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegionUsageRestrictions", []))

    @jsii.member(jsii_name="resetTeams")
    def reset_teams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTeams", []))

    @jsii.member(jsii_name="resetWithDefaultAlertsSettings")
    def reset_with_default_alerts_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWithDefaultAlertsSettings", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="apiKeys")
    def api_keys(self) -> "ProjectApiKeysList":
        return typing.cast("ProjectApiKeysList", jsii.get(self, "apiKeys"))

    @builtins.property
    @jsii.member(jsii_name="clusterCount")
    def cluster_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clusterCount"))

    @builtins.property
    @jsii.member(jsii_name="created")
    def created(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "created"))

    @builtins.property
    @jsii.member(jsii_name="teams")
    def teams(self) -> "ProjectTeamsList":
        return typing.cast("ProjectTeamsList", jsii.get(self, "teams"))

    @builtins.property
    @jsii.member(jsii_name="apiKeysInput")
    def api_keys_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectApiKeys"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectApiKeys"]]], jsii.get(self, "apiKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isCollectDatabaseSpecificsStatisticsEnabledInput")
    def is_collect_database_specifics_statistics_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isCollectDatabaseSpecificsStatisticsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isDataExplorerEnabledInput")
    def is_data_explorer_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDataExplorerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isPerformanceAdvisorEnabledInput")
    def is_performance_advisor_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isPerformanceAdvisorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isRealtimePerformancePanelEnabledInput")
    def is_realtime_performance_panel_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isRealtimePerformancePanelEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="isSchemaAdvisorEnabledInput")
    def is_schema_advisor_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isSchemaAdvisorEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="orgIdInput")
    def org_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "orgIdInput"))

    @builtins.property
    @jsii.member(jsii_name="projectOwnerIdInput")
    def project_owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectOwnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionUsageRestrictionsInput")
    def region_usage_restrictions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionUsageRestrictionsInput"))

    @builtins.property
    @jsii.member(jsii_name="teamsInput")
    def teams_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectTeams"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectTeams"]]], jsii.get(self, "teamsInput"))

    @builtins.property
    @jsii.member(jsii_name="withDefaultAlertsSettingsInput")
    def with_default_alerts_settings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "withDefaultAlertsSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__399e6850bffe5e6e201a5caeaa4610600a46a4220a139607666633d3e6c2fdf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="isCollectDatabaseSpecificsStatisticsEnabled")
    def is_collect_database_specifics_statistics_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isCollectDatabaseSpecificsStatisticsEnabled"))

    @is_collect_database_specifics_statistics_enabled.setter
    def is_collect_database_specifics_statistics_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ed13b0c82fcbccc5f42317472fd6d38dd0564b0e676e0d4dbe7099d325c1279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isCollectDatabaseSpecificsStatisticsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="isDataExplorerEnabled")
    def is_data_explorer_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDataExplorerEnabled"))

    @is_data_explorer_enabled.setter
    def is_data_explorer_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b427bc1254e9875ed52737e822e9e5d4f117331f3e5f0203e09133789aa56f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDataExplorerEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="isPerformanceAdvisorEnabled")
    def is_performance_advisor_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isPerformanceAdvisorEnabled"))

    @is_performance_advisor_enabled.setter
    def is_performance_advisor_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53fd1f0422b4b11af7c55db4e45bfdad07101563662d39829d18a9d61e2a185e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isPerformanceAdvisorEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="isRealtimePerformancePanelEnabled")
    def is_realtime_performance_panel_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isRealtimePerformancePanelEnabled"))

    @is_realtime_performance_panel_enabled.setter
    def is_realtime_performance_panel_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a74741c03e52ff9f498c35e6d1efcabe03e14de861fda5409657fb75b487c66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isRealtimePerformancePanelEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="isSchemaAdvisorEnabled")
    def is_schema_advisor_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isSchemaAdvisorEnabled"))

    @is_schema_advisor_enabled.setter
    def is_schema_advisor_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2bebb280cb7cc531b4fe8d979dd24e0f9b86ba62f0235d71ff9bc7cb12b8c1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSchemaAdvisorEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9877c6d3de9b197338f85827372f832a76310c1cb3d1bde1200389329ce270c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="orgId")
    def org_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "orgId"))

    @org_id.setter
    def org_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fa63757c44a2d36b14586e0c85f6b8e2b3a4a5d3f1ef7927bd9a9e8322302a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgId", value)

    @builtins.property
    @jsii.member(jsii_name="projectOwnerId")
    def project_owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectOwnerId"))

    @project_owner_id.setter
    def project_owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17a62eb55e28fcf1d83f41eff2be9d9238606ead3c76bcd004c709a5df2be8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectOwnerId", value)

    @builtins.property
    @jsii.member(jsii_name="regionUsageRestrictions")
    def region_usage_restrictions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionUsageRestrictions"))

    @region_usage_restrictions.setter
    def region_usage_restrictions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a95b780805ec47b6f1f798a4705b303527259dbbbe62e7907fb6f4e01f9eedf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionUsageRestrictions", value)

    @builtins.property
    @jsii.member(jsii_name="withDefaultAlertsSettings")
    def with_default_alerts_settings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "withDefaultAlertsSettings"))

    @with_default_alerts_settings.setter
    def with_default_alerts_settings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35fa76ee4131e5c94898039410519ebaab4f5160f78c144f28b2f9250aab0240)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "withDefaultAlertsSettings", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectApiKeys",
    jsii_struct_bases=[],
    name_mapping={"api_key_id": "apiKeyId", "role_names": "roleNames"},
)
class ProjectApiKeys:
    def __init__(
        self,
        *,
        api_key_id: builtins.str,
        role_names: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param api_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#api_key_id Project#api_key_id}.
        :param role_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#role_names Project#role_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e9191e92a9d3bf2557c531df443a146812e04737452ba7db22d05297faacaa)
            check_type(argname="argument api_key_id", value=api_key_id, expected_type=type_hints["api_key_id"])
            check_type(argname="argument role_names", value=role_names, expected_type=type_hints["role_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_key_id": api_key_id,
            "role_names": role_names,
        }

    @builtins.property
    def api_key_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#api_key_id Project#api_key_id}.'''
        result = self._values.get("api_key_id")
        assert result is not None, "Required property 'api_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#role_names Project#role_names}.'''
        result = self._values.get("role_names")
        assert result is not None, "Required property 'role_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectApiKeys(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectApiKeysList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectApiKeysList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d82dfd0d1973d0e7d44cbbcac0175930a8d4f49e564939e80eaf87be3966c9a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProjectApiKeysOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25a6c3a32ebd9468983ebbd9a527046acd5dc27c674a6026846dc8532e0bcce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectApiKeysOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dea4ddc96564ca2cbbd761d00c20f565bc439a534d3cdbd59b8873f6d21db63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31bc00d756e3b22979ea725666cd6d21df59ed632d1201979afd97403cd3a975)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f60e849f0ec78dd746dac9944f2ef5d74111b35d8faae5c4c98acca46a131100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb29800822dabf39312e8108713f3033188d0b40c82e52e1dcec97c1839a0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProjectApiKeysOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectApiKeysOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4439604b8301c0ceeebb61a532f27b5bd8281065510e54486f9a488ad13c5a21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="apiKeyIdInput")
    def api_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNamesInput")
    def role_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roleNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyId")
    def api_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKeyId"))

    @api_key_id.setter
    def api_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e51fba7663763706a1f3e369bfffb44c35dc4a73b7be1d339529b821372c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="roleNames")
    def role_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roleNames"))

    @role_names.setter
    def role_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24c491dd6fbfde0b99129c198842cc1e6e304812bebbd67d5f2bf5bfa3e34e46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleNames", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectApiKeys, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectApiKeys, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectApiKeys, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958c7c856939e512c8f318972db2af67d34c2792a04f27837e5727a74596aa14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectConfig",
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
        "org_id": "orgId",
        "api_keys": "apiKeys",
        "id": "id",
        "is_collect_database_specifics_statistics_enabled": "isCollectDatabaseSpecificsStatisticsEnabled",
        "is_data_explorer_enabled": "isDataExplorerEnabled",
        "is_performance_advisor_enabled": "isPerformanceAdvisorEnabled",
        "is_realtime_performance_panel_enabled": "isRealtimePerformancePanelEnabled",
        "is_schema_advisor_enabled": "isSchemaAdvisorEnabled",
        "project_owner_id": "projectOwnerId",
        "region_usage_restrictions": "regionUsageRestrictions",
        "teams": "teams",
        "with_default_alerts_settings": "withDefaultAlertsSettings",
    },
)
class ProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        org_id: builtins.str,
        api_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectApiKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_collect_database_specifics_statistics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_data_explorer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_performance_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_realtime_performance_panel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        is_schema_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        project_owner_id: typing.Optional[builtins.str] = None,
        region_usage_restrictions: typing.Optional[builtins.str] = None,
        teams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectTeams", typing.Dict[builtins.str, typing.Any]]]]] = None,
        with_default_alerts_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#name Project#name}.
        :param org_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#org_id Project#org_id}.
        :param api_keys: api_keys block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#api_keys Project#api_keys}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_collect_database_specifics_statistics_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_collect_database_specifics_statistics_enabled Project#is_collect_database_specifics_statistics_enabled}.
        :param is_data_explorer_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_data_explorer_enabled Project#is_data_explorer_enabled}.
        :param is_performance_advisor_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_performance_advisor_enabled Project#is_performance_advisor_enabled}.
        :param is_realtime_performance_panel_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_realtime_performance_panel_enabled Project#is_realtime_performance_panel_enabled}.
        :param is_schema_advisor_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_schema_advisor_enabled Project#is_schema_advisor_enabled}.
        :param project_owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#project_owner_id Project#project_owner_id}.
        :param region_usage_restrictions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#region_usage_restrictions Project#region_usage_restrictions}.
        :param teams: teams block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#teams Project#teams}
        :param with_default_alerts_settings: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#with_default_alerts_settings Project#with_default_alerts_settings}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf13e3da8485dd62c5423ed6934179902dd00b10349679ad3b25dba465581cf5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument org_id", value=org_id, expected_type=type_hints["org_id"])
            check_type(argname="argument api_keys", value=api_keys, expected_type=type_hints["api_keys"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_collect_database_specifics_statistics_enabled", value=is_collect_database_specifics_statistics_enabled, expected_type=type_hints["is_collect_database_specifics_statistics_enabled"])
            check_type(argname="argument is_data_explorer_enabled", value=is_data_explorer_enabled, expected_type=type_hints["is_data_explorer_enabled"])
            check_type(argname="argument is_performance_advisor_enabled", value=is_performance_advisor_enabled, expected_type=type_hints["is_performance_advisor_enabled"])
            check_type(argname="argument is_realtime_performance_panel_enabled", value=is_realtime_performance_panel_enabled, expected_type=type_hints["is_realtime_performance_panel_enabled"])
            check_type(argname="argument is_schema_advisor_enabled", value=is_schema_advisor_enabled, expected_type=type_hints["is_schema_advisor_enabled"])
            check_type(argname="argument project_owner_id", value=project_owner_id, expected_type=type_hints["project_owner_id"])
            check_type(argname="argument region_usage_restrictions", value=region_usage_restrictions, expected_type=type_hints["region_usage_restrictions"])
            check_type(argname="argument teams", value=teams, expected_type=type_hints["teams"])
            check_type(argname="argument with_default_alerts_settings", value=with_default_alerts_settings, expected_type=type_hints["with_default_alerts_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "org_id": org_id,
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
        if api_keys is not None:
            self._values["api_keys"] = api_keys
        if id is not None:
            self._values["id"] = id
        if is_collect_database_specifics_statistics_enabled is not None:
            self._values["is_collect_database_specifics_statistics_enabled"] = is_collect_database_specifics_statistics_enabled
        if is_data_explorer_enabled is not None:
            self._values["is_data_explorer_enabled"] = is_data_explorer_enabled
        if is_performance_advisor_enabled is not None:
            self._values["is_performance_advisor_enabled"] = is_performance_advisor_enabled
        if is_realtime_performance_panel_enabled is not None:
            self._values["is_realtime_performance_panel_enabled"] = is_realtime_performance_panel_enabled
        if is_schema_advisor_enabled is not None:
            self._values["is_schema_advisor_enabled"] = is_schema_advisor_enabled
        if project_owner_id is not None:
            self._values["project_owner_id"] = project_owner_id
        if region_usage_restrictions is not None:
            self._values["region_usage_restrictions"] = region_usage_restrictions
        if teams is not None:
            self._values["teams"] = teams
        if with_default_alerts_settings is not None:
            self._values["with_default_alerts_settings"] = with_default_alerts_settings

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#name Project#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def org_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#org_id Project#org_id}.'''
        result = self._values.get("org_id")
        assert result is not None, "Required property 'org_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_keys(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]]:
        '''api_keys block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#api_keys Project#api_keys}
        '''
        result = self._values.get("api_keys")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#id Project#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_collect_database_specifics_statistics_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_collect_database_specifics_statistics_enabled Project#is_collect_database_specifics_statistics_enabled}.'''
        result = self._values.get("is_collect_database_specifics_statistics_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_data_explorer_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_data_explorer_enabled Project#is_data_explorer_enabled}.'''
        result = self._values.get("is_data_explorer_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_performance_advisor_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_performance_advisor_enabled Project#is_performance_advisor_enabled}.'''
        result = self._values.get("is_performance_advisor_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_realtime_performance_panel_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_realtime_performance_panel_enabled Project#is_realtime_performance_panel_enabled}.'''
        result = self._values.get("is_realtime_performance_panel_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def is_schema_advisor_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#is_schema_advisor_enabled Project#is_schema_advisor_enabled}.'''
        result = self._values.get("is_schema_advisor_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def project_owner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#project_owner_id Project#project_owner_id}.'''
        result = self._values.get("project_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region_usage_restrictions(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#region_usage_restrictions Project#region_usage_restrictions}.'''
        result = self._values.get("region_usage_restrictions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def teams(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectTeams"]]]:
        '''teams block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#teams Project#teams}
        '''
        result = self._values.get("teams")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectTeams"]]], result)

    @builtins.property
    def with_default_alerts_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#with_default_alerts_settings Project#with_default_alerts_settings}.'''
        result = self._values.get("with_default_alerts_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectTeams",
    jsii_struct_bases=[],
    name_mapping={"role_names": "roleNames", "team_id": "teamId"},
)
class ProjectTeams:
    def __init__(
        self,
        *,
        role_names: typing.Sequence[builtins.str],
        team_id: builtins.str,
    ) -> None:
        '''
        :param role_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#role_names Project#role_names}.
        :param team_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#team_id Project#team_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce41930cf839a0737fb23d79189594a8fac75bf267949ddb55ec67141b3f293f)
            check_type(argname="argument role_names", value=role_names, expected_type=type_hints["role_names"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role_names": role_names,
            "team_id": team_id,
        }

    @builtins.property
    def role_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#role_names Project#role_names}.'''
        result = self._values.get("role_names")
        assert result is not None, "Required property 'role_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def team_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/project#team_id Project#team_id}.'''
        result = self._values.get("team_id")
        assert result is not None, "Required property 'team_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectTeams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectTeamsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectTeamsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e32a9b286007d51f936d4285652c877b5e27743d30496a35c3f91a8127e7af05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProjectTeamsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b46ac6533125045a512953f5eb31f692ddf3ffa431d6d5d060a367e859f33e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectTeamsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60275064266cfe5ddf284d123b690718ff4c34fa7f620193cb7c03ff1ae4dfbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3722e8092c49e69acdf2817656cb9efabb9deebb214abbbcf48773e71331a2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0213c5db4458923d82ca1226f07621ef223bfc584ac4d7c2df5e7d4a2dad8208)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectTeams]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectTeams]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectTeams]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b136d533a3e072dbb8723fd0ba7720d58b9399a78e9c4df74e81411ed9e9c6bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProjectTeamsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.project.ProjectTeamsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48788858743b2f4f84d47ccc4a3e1ad2e56d97403aab5543c123cac30714974d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="roleNamesInput")
    def role_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roleNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="teamIdInput")
    def team_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "teamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="roleNames")
    def role_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roleNames"))

    @role_names.setter
    def role_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2dcbb7f00862d79c33529d3a7e8e5656c6127516bb1373d52d69359bfbbe010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleNames", value)

    @builtins.property
    @jsii.member(jsii_name="teamId")
    def team_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "teamId"))

    @team_id.setter
    def team_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b9d00a63f63cac3574aff0fb9aea85fbaa4ee172e1b5d087e0bbbc199507de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "teamId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectTeams, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectTeams, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectTeams, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c097efe0e029bb66d1f350cf0995c3998162dafebe9154970b041b531374933e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Project",
    "ProjectApiKeys",
    "ProjectApiKeysList",
    "ProjectApiKeysOutputReference",
    "ProjectConfig",
    "ProjectTeams",
    "ProjectTeamsList",
    "ProjectTeamsOutputReference",
]

publication.publish()

def _typecheckingstub__9d7a170c16ee3d7749a2e1a1597ff9942a4f15acab9c14e51e3e2c98f32c7ccd(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    org_id: builtins.str,
    api_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectApiKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_collect_database_specifics_statistics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_data_explorer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_performance_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_realtime_performance_panel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_schema_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_owner_id: typing.Optional[builtins.str] = None,
    region_usage_restrictions: typing.Optional[builtins.str] = None,
    teams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectTeams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    with_default_alerts_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__b1bc813b6a683664ce9ccea88b6c9296792510df59a5b1199d02da3ee75e08e7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectApiKeys, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62db4d9da517db2e656400e303bb2208dca445fbd3b89005ab2ff7b77edadfb7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectTeams, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__399e6850bffe5e6e201a5caeaa4610600a46a4220a139607666633d3e6c2fdf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed13b0c82fcbccc5f42317472fd6d38dd0564b0e676e0d4dbe7099d325c1279(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b427bc1254e9875ed52737e822e9e5d4f117331f3e5f0203e09133789aa56f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53fd1f0422b4b11af7c55db4e45bfdad07101563662d39829d18a9d61e2a185e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a74741c03e52ff9f498c35e6d1efcabe03e14de861fda5409657fb75b487c66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2bebb280cb7cc531b4fe8d979dd24e0f9b86ba62f0235d71ff9bc7cb12b8c1c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9877c6d3de9b197338f85827372f832a76310c1cb3d1bde1200389329ce270c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fa63757c44a2d36b14586e0c85f6b8e2b3a4a5d3f1ef7927bd9a9e8322302a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17a62eb55e28fcf1d83f41eff2be9d9238606ead3c76bcd004c709a5df2be8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a95b780805ec47b6f1f798a4705b303527259dbbbe62e7907fb6f4e01f9eedf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fa76ee4131e5c94898039410519ebaab4f5160f78c144f28b2f9250aab0240(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e9191e92a9d3bf2557c531df443a146812e04737452ba7db22d05297faacaa(
    *,
    api_key_id: builtins.str,
    role_names: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82dfd0d1973d0e7d44cbbcac0175930a8d4f49e564939e80eaf87be3966c9a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25a6c3a32ebd9468983ebbd9a527046acd5dc27c674a6026846dc8532e0bcce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dea4ddc96564ca2cbbd761d00c20f565bc439a534d3cdbd59b8873f6d21db63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31bc00d756e3b22979ea725666cd6d21df59ed632d1201979afd97403cd3a975(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60e849f0ec78dd746dac9944f2ef5d74111b35d8faae5c4c98acca46a131100(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb29800822dabf39312e8108713f3033188d0b40c82e52e1dcec97c1839a0a2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectApiKeys]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4439604b8301c0ceeebb61a532f27b5bd8281065510e54486f9a488ad13c5a21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e51fba7663763706a1f3e369bfffb44c35dc4a73b7be1d339529b821372c19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c491dd6fbfde0b99129c198842cc1e6e304812bebbd67d5f2bf5bfa3e34e46(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958c7c856939e512c8f318972db2af67d34c2792a04f27837e5727a74596aa14(
    value: typing.Optional[typing.Union[ProjectApiKeys, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf13e3da8485dd62c5423ed6934179902dd00b10349679ad3b25dba465581cf5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    org_id: builtins.str,
    api_keys: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectApiKeys, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_collect_database_specifics_statistics_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_data_explorer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_performance_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_realtime_performance_panel_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    is_schema_advisor_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    project_owner_id: typing.Optional[builtins.str] = None,
    region_usage_restrictions: typing.Optional[builtins.str] = None,
    teams: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectTeams, typing.Dict[builtins.str, typing.Any]]]]] = None,
    with_default_alerts_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce41930cf839a0737fb23d79189594a8fac75bf267949ddb55ec67141b3f293f(
    *,
    role_names: typing.Sequence[builtins.str],
    team_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32a9b286007d51f936d4285652c877b5e27743d30496a35c3f91a8127e7af05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b46ac6533125045a512953f5eb31f692ddf3ffa431d6d5d060a367e859f33e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60275064266cfe5ddf284d123b690718ff4c34fa7f620193cb7c03ff1ae4dfbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3722e8092c49e69acdf2817656cb9efabb9deebb214abbbcf48773e71331a2c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0213c5db4458923d82ca1226f07621ef223bfc584ac4d7c2df5e7d4a2dad8208(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b136d533a3e072dbb8723fd0ba7720d58b9399a78e9c4df74e81411ed9e9c6bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectTeams]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48788858743b2f4f84d47ccc4a3e1ad2e56d97403aab5543c123cac30714974d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2dcbb7f00862d79c33529d3a7e8e5656c6127516bb1373d52d69359bfbbe010(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b9d00a63f63cac3574aff0fb9aea85fbaa4ee172e1b5d087e0bbbc199507de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c097efe0e029bb66d1f350cf0995c3998162dafebe9154970b041b531374933e(
    value: typing.Optional[typing.Union[ProjectTeams, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
