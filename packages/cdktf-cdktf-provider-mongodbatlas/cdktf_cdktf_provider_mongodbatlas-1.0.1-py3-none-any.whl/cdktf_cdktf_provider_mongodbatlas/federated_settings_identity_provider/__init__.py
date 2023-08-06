'''
# `mongodbatlas_federated_settings_identity_provider`

Refer to the Terraform Registory for docs: [`mongodbatlas_federated_settings_identity_provider`](https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider).
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


class FederatedSettingsIdentityProvider(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.federatedSettingsIdentityProvider.FederatedSettingsIdentityProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider mongodbatlas_federated_settings_identity_provider}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        federation_settings_id: builtins.str,
        issuer_uri: builtins.str,
        name: builtins.str,
        request_binding: builtins.str,
        response_signature_algorithm: builtins.str,
        sso_debug_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sso_url: builtins.str,
        status: builtins.str,
        associated_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider mongodbatlas_federated_settings_identity_provider} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param federation_settings_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#federation_settings_id FederatedSettingsIdentityProvider#federation_settings_id}.
        :param issuer_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#issuer_uri FederatedSettingsIdentityProvider#issuer_uri}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#name FederatedSettingsIdentityProvider#name}.
        :param request_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#request_binding FederatedSettingsIdentityProvider#request_binding}.
        :param response_signature_algorithm: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#response_signature_algorithm FederatedSettingsIdentityProvider#response_signature_algorithm}.
        :param sso_debug_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_debug_enabled FederatedSettingsIdentityProvider#sso_debug_enabled}.
        :param sso_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_url FederatedSettingsIdentityProvider#sso_url}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#status FederatedSettingsIdentityProvider#status}.
        :param associated_domains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#associated_domains FederatedSettingsIdentityProvider#associated_domains}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#id FederatedSettingsIdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17941229f54c7ceeceddec79fffa7c81243fabd0b62845a69d2db9f71579a4a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FederatedSettingsIdentityProviderConfig(
            federation_settings_id=federation_settings_id,
            issuer_uri=issuer_uri,
            name=name,
            request_binding=request_binding,
            response_signature_algorithm=response_signature_algorithm,
            sso_debug_enabled=sso_debug_enabled,
            sso_url=sso_url,
            status=status,
            associated_domains=associated_domains,
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

    @jsii.member(jsii_name="resetAssociatedDomains")
    def reset_associated_domains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAssociatedDomains", []))

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
    @jsii.member(jsii_name="oktaIdpId")
    def okta_idp_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "oktaIdpId"))

    @builtins.property
    @jsii.member(jsii_name="associatedDomainsInput")
    def associated_domains_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "associatedDomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="federationSettingsIdInput")
    def federation_settings_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "federationSettingsIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerUriInput")
    def issuer_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerUriInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requestBindingInput")
    def request_binding_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "requestBindingInput"))

    @builtins.property
    @jsii.member(jsii_name="responseSignatureAlgorithmInput")
    def response_signature_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "responseSignatureAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoDebugEnabledInput")
    def sso_debug_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ssoDebugEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ssoUrlInput")
    def sso_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssoUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="associatedDomains")
    def associated_domains(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "associatedDomains"))

    @associated_domains.setter
    def associated_domains(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661e763dce3dd959f990476525ffe3f820266c8c1c70328921a59eab26aa0879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "associatedDomains", value)

    @builtins.property
    @jsii.member(jsii_name="federationSettingsId")
    def federation_settings_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "federationSettingsId"))

    @federation_settings_id.setter
    def federation_settings_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5427f540d6b43d68eb26e46af3109238b9c620773fa09bf44b5b61f5f2c7d538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "federationSettingsId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b51c9064661b5352acd93a5235cc1c34de4c1700bde2c73de4608134e89a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="issuerUri")
    def issuer_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerUri"))

    @issuer_uri.setter
    def issuer_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688a0ede3ab273f8511e70d7cedadb085d49e76a4cd843b5a8fcd2945634802c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuerUri", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fc45fedb7e6a32563cd33703e819a7a6faceb7b4c6e98e9ca3410373b62a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="requestBinding")
    def request_binding(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "requestBinding"))

    @request_binding.setter
    def request_binding(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08f02f1fd96ecc7ed9671987688a23e0500af175d6356ba531bbaf3e0c3a685)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requestBinding", value)

    @builtins.property
    @jsii.member(jsii_name="responseSignatureAlgorithm")
    def response_signature_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "responseSignatureAlgorithm"))

    @response_signature_algorithm.setter
    def response_signature_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d39e354ce62f9c9389c4dc06c79acbdb16ff38a2d570997fa73cd283a3ec4a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "responseSignatureAlgorithm", value)

    @builtins.property
    @jsii.member(jsii_name="ssoDebugEnabled")
    def sso_debug_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssoDebugEnabled"))

    @sso_debug_enabled.setter
    def sso_debug_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd951848dda0858bde6f85505a5c95dd3e846d9cd858e0793fa7222fd8979063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoDebugEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="ssoUrl")
    def sso_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssoUrl"))

    @sso_url.setter
    def sso_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c73b3a57ea1ec172ac61c11b885bfd6678d126ec154873178ae90a6d5a1dec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssoUrl", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682894cfcce3aaebb259cdc36285e0e50cafc62824c48edd3bdd9f370ca2343a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.federatedSettingsIdentityProvider.FederatedSettingsIdentityProviderConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "federation_settings_id": "federationSettingsId",
        "issuer_uri": "issuerUri",
        "name": "name",
        "request_binding": "requestBinding",
        "response_signature_algorithm": "responseSignatureAlgorithm",
        "sso_debug_enabled": "ssoDebugEnabled",
        "sso_url": "ssoUrl",
        "status": "status",
        "associated_domains": "associatedDomains",
        "id": "id",
    },
)
class FederatedSettingsIdentityProviderConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        federation_settings_id: builtins.str,
        issuer_uri: builtins.str,
        name: builtins.str,
        request_binding: builtins.str,
        response_signature_algorithm: builtins.str,
        sso_debug_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        sso_url: builtins.str,
        status: builtins.str,
        associated_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param federation_settings_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#federation_settings_id FederatedSettingsIdentityProvider#federation_settings_id}.
        :param issuer_uri: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#issuer_uri FederatedSettingsIdentityProvider#issuer_uri}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#name FederatedSettingsIdentityProvider#name}.
        :param request_binding: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#request_binding FederatedSettingsIdentityProvider#request_binding}.
        :param response_signature_algorithm: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#response_signature_algorithm FederatedSettingsIdentityProvider#response_signature_algorithm}.
        :param sso_debug_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_debug_enabled FederatedSettingsIdentityProvider#sso_debug_enabled}.
        :param sso_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_url FederatedSettingsIdentityProvider#sso_url}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#status FederatedSettingsIdentityProvider#status}.
        :param associated_domains: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#associated_domains FederatedSettingsIdentityProvider#associated_domains}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#id FederatedSettingsIdentityProvider#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724d6f038136fd09e291f5dfb0b6551e08bfd4cce334e87342a45858976fc596)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument federation_settings_id", value=federation_settings_id, expected_type=type_hints["federation_settings_id"])
            check_type(argname="argument issuer_uri", value=issuer_uri, expected_type=type_hints["issuer_uri"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_binding", value=request_binding, expected_type=type_hints["request_binding"])
            check_type(argname="argument response_signature_algorithm", value=response_signature_algorithm, expected_type=type_hints["response_signature_algorithm"])
            check_type(argname="argument sso_debug_enabled", value=sso_debug_enabled, expected_type=type_hints["sso_debug_enabled"])
            check_type(argname="argument sso_url", value=sso_url, expected_type=type_hints["sso_url"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument associated_domains", value=associated_domains, expected_type=type_hints["associated_domains"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "federation_settings_id": federation_settings_id,
            "issuer_uri": issuer_uri,
            "name": name,
            "request_binding": request_binding,
            "response_signature_algorithm": response_signature_algorithm,
            "sso_debug_enabled": sso_debug_enabled,
            "sso_url": sso_url,
            "status": status,
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
        if associated_domains is not None:
            self._values["associated_domains"] = associated_domains
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
    def federation_settings_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#federation_settings_id FederatedSettingsIdentityProvider#federation_settings_id}.'''
        result = self._values.get("federation_settings_id")
        assert result is not None, "Required property 'federation_settings_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def issuer_uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#issuer_uri FederatedSettingsIdentityProvider#issuer_uri}.'''
        result = self._values.get("issuer_uri")
        assert result is not None, "Required property 'issuer_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#name FederatedSettingsIdentityProvider#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_binding(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#request_binding FederatedSettingsIdentityProvider#request_binding}.'''
        result = self._values.get("request_binding")
        assert result is not None, "Required property 'request_binding' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def response_signature_algorithm(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#response_signature_algorithm FederatedSettingsIdentityProvider#response_signature_algorithm}.'''
        result = self._values.get("response_signature_algorithm")
        assert result is not None, "Required property 'response_signature_algorithm' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sso_debug_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_debug_enabled FederatedSettingsIdentityProvider#sso_debug_enabled}.'''
        result = self._values.get("sso_debug_enabled")
        assert result is not None, "Required property 'sso_debug_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def sso_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#sso_url FederatedSettingsIdentityProvider#sso_url}.'''
        result = self._values.get("sso_url")
        assert result is not None, "Required property 'sso_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#status FederatedSettingsIdentityProvider#status}.'''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def associated_domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#associated_domains FederatedSettingsIdentityProvider#associated_domains}.'''
        result = self._values.get("associated_domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/mongodbatlas/r/federated_settings_identity_provider#id FederatedSettingsIdentityProvider#id}.

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
        return "FederatedSettingsIdentityProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FederatedSettingsIdentityProvider",
    "FederatedSettingsIdentityProviderConfig",
]

publication.publish()

def _typecheckingstub__17941229f54c7ceeceddec79fffa7c81243fabd0b62845a69d2db9f71579a4a4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    federation_settings_id: builtins.str,
    issuer_uri: builtins.str,
    name: builtins.str,
    request_binding: builtins.str,
    response_signature_algorithm: builtins.str,
    sso_debug_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sso_url: builtins.str,
    status: builtins.str,
    associated_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__661e763dce3dd959f990476525ffe3f820266c8c1c70328921a59eab26aa0879(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5427f540d6b43d68eb26e46af3109238b9c620773fa09bf44b5b61f5f2c7d538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b51c9064661b5352acd93a5235cc1c34de4c1700bde2c73de4608134e89a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688a0ede3ab273f8511e70d7cedadb085d49e76a4cd843b5a8fcd2945634802c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fc45fedb7e6a32563cd33703e819a7a6faceb7b4c6e98e9ca3410373b62a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08f02f1fd96ecc7ed9671987688a23e0500af175d6356ba531bbaf3e0c3a685(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39e354ce62f9c9389c4dc06c79acbdb16ff38a2d570997fa73cd283a3ec4a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd951848dda0858bde6f85505a5c95dd3e846d9cd858e0793fa7222fd8979063(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c73b3a57ea1ec172ac61c11b885bfd6678d126ec154873178ae90a6d5a1dec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682894cfcce3aaebb259cdc36285e0e50cafc62824c48edd3bdd9f370ca2343a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724d6f038136fd09e291f5dfb0b6551e08bfd4cce334e87342a45858976fc596(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    federation_settings_id: builtins.str,
    issuer_uri: builtins.str,
    name: builtins.str,
    request_binding: builtins.str,
    response_signature_algorithm: builtins.str,
    sso_debug_enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    sso_url: builtins.str,
    status: builtins.str,
    associated_domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
