from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.rest.rest_client import RestClient
from semantha_sdk.model.synonym import Synonym as SynonymDTO, SynonymSchema


class SynonymEndpoint(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._id}"

    def get(self) -> SynonymDTO:
        """ Get the synonym """
        return self._session.get(self._endpoint).execute().to(SynonymSchema)

    def put_word(self, word: str, synonym: str, tags: list[str] = None) -> SynonymDTO:
        """ Update a synonym replacement rule: the word will be replaced by the synonym for semantic matching.

        Args:
            word (str): the updated word that should be replaced by the synonym (ignored if a regex is provided)
            synonym (str): the synonym that replaces the word or the regex
            tags (list[str]): the updated list of tags the synonym should be attached to
        """
        return self._session.put(
            url=self._endpoint,
            json={
                "word": word,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(SynonymSchema)

    def put_regex(self, regex: str, synonym: str, tags: list[str] = None) -> SynonymDTO:
        """ Update a synonym replacement rule: the regex (if matched in a document) will be replaced by the synonym for
        semantic matching.

        Args:
            regex (str): the updated regex that should be replaced by the synonym
            synonym (str): the synonym that replaces the word or the regex
            tags (list[str]): the updated list of tags the synonym should be attached to
        """
        return self._session.put(
            url=self._endpoint,
            json={
                "regex": regex,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(SynonymSchema)

    def delete(self):
        """ Delete the synonym """
        self._session.delete(self._endpoint).execute()


class SynonymsEndpoint(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/synonyms"

    def get(self) -> list[SynonymDTO]:
        """ Get all synonyms that are defined for the domain """
        return self._session.get(self._endpoint).execute().to(SynonymSchema)

    def post_word(self, word: str, synonym: str, tags: list[str] = None) -> SynonymDTO:
        """ Create a synonym replacement rule: the word will be replaced by the synonym for semantic matching.

        Args:
            word (str): the word that should be replaced by the synonym (ignored if a regex is provided)
            synonym (str): the synonym that replaces the word
            tags (list[str]): list of tags the synonym should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "word": word,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(SynonymSchema)

    def post_regex(self, regex: str, synonym: str, tags: list[str] = None) -> SynonymDTO:
        """ Create a synonym replacement rule: the regex (if matched in a document) will be replaced by the synonym for
        semantic matching.

        Args:
            regex (str): the regex that should be replaced by the synonym
            synonym (str): the synonym that replaces the regex
            tags (list[str]): list of tags the synonym should be attached to
        """
        return self._session.post(
            url=self._endpoint,
            json={
                "regex": regex,
                "synonym": synonym,
                "tags": tags
            }
        ).execute().to(SynonymSchema)

    def delete(self):
        """ Delete all synonyms """
        self._session.delete(self._endpoint).execute()

    def __call__(self, id: str):
        return SynonymEndpoint(self._session, self._endpoint, id)
