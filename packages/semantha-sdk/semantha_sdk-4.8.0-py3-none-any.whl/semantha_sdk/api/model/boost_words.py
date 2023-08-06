from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.boost_word import Boostword, BoostwordSchema
from semantha_sdk.rest.rest_client import RestClient


class BoostwordEndpoint(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._id}"

    def get(self) -> Boostword:
        """ Get the boostword """
        return self._session.get(self._endpoint).execute().to(BoostwordSchema)

    def put_word(self, word: str, tags: list[str] = None) -> Boostword:
        """ Update a boostword as plain word (str).

        Args:
            word (str): the updated boostword
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.put(
            url=self._endpoint,
            json={
                "word": word,
                "tags": tags
            }
        ).execute().to(BoostwordSchema)

    def put_regex(self, regex: str, tags: list[str] = None) -> Boostword:
        """ Update a boostword as regex (regex represented as str).

        Args:
            regex (str): the updated boostword regex
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.put(
            url=self._endpoint,
            json={
                "regex": regex,
                "tags": tags
            }
        ).execute().to(BoostwordSchema)

    def delete(self):
        """ Delete the boostword """
        self._session.delete(self._endpoint).execute()


class BoostwordsEndpoint(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/boostwords"

    def get(self) -> list[Boostword]:
        """ Get all boostwords """
        return self._session.get(self._endpoint).execute().to(BoostwordSchema)

    def post_word(self, word: str, tags: list[str] = None) -> Boostword:
        """ Create a boostword as plain word (str).

        Args:
            word (str): the new boostword (ignored if a regex is provided)
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "word": word,
                "tags": tags
            }
        ).execute().to(BoostwordSchema)

    def post_regex(self, regex: str, tags: list[str] = None) -> Boostword:
        """ Create a boostword as regex (regex represented as str).

        Args:
            regex (str): the new boostword regex
            tags (list[str]): list of tags the boostword should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "regex": regex,
                "tags": tags
            }
        ).execute().to(BoostwordSchema)

    def delete(self):
        """ Delete all boostwords """
        self._session.delete(self._endpoint).execute()

    def __call__(self, id: str):
        return BoostwordEndpoint(self._session, self._endpoint, id)
