from semantha_sdk import RestClient
from semantha_sdk.api.model.boost_words import BoostwordsEndpoint
from semantha_sdk.api.model.synonyms import SynonymsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class DomainModelEndpoint(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: attributes, backups, boostwords, classes, extractors,
            formatters, instances, metadata, namedentities, regexes, relations,
            rulefunctions, rules, synonyms
    """

    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__boostwords = BoostwordsEndpoint(session, self._endpoint)
        self.__synonyms = SynonymsEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def boostwords(self) -> BoostwordsEndpoint:
        return self.__boostwords

    @property
    def synonyms(self) -> SynonymsEndpoint:
        return self.__synonyms


class DomainModelsEndpoint(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def __call__(self, domain_name: str) -> DomainModelEndpoint:
        # Returns a Domain object for the given domainname, throws error if id doesn't exist
        return DomainModelEndpoint(self._session, self._endpoint, domain_name)
