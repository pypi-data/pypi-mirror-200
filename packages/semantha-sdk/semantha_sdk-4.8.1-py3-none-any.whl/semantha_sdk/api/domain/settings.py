from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.domain_settings import DomainSettings, DomainSettingsSchema, PatchDomainSettings


class DomainSettingsEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/settings"

    def get(self) -> DomainSettings:
        """Get the domain settings"""
        return self._session.get(self._endpoint).execute().to(DomainSettingsSchema)

    def patch(
            self,
            domainsettings: PatchDomainSettings
    ) -> DomainSettings:
        """Patch one or more domain setting(s)"""
        #TODO: add Args description
        response = self._session.patch(
            self._endpoint,
            json=DomainSettingsSchema().dump(domainsettings)
        ).execute()
        return response.to(DomainSettingsSchema)
