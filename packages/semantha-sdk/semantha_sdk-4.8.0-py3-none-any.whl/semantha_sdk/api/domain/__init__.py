from __future__ import annotations

from io import IOBase
from typing import Optional, List, Union

from semantha_sdk import RestClient
from semantha_sdk.api.domain.document_annotations import DocumentAnnotationsEndpoint
from semantha_sdk.api.domain.document_classes import DocumentClassesEndpoint
from semantha_sdk.api.domain.comparison import DocumentComparisonsEndpoint
from semantha_sdk.api.domain.documents import DocumentsEndpoint
from semantha_sdk.api.domain.reference_documents import ReferenceDocumentsEndpoint
from semantha_sdk.api.domain.references import ReferencesEndpoint
from semantha_sdk.api.domain.settings import DomainSettingsEndpoint
from semantha_sdk.api.domain.tags import DomainTagsEndpoint
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model import Domain
from semantha_sdk.model.domain import DomainSchema
from semantha_sdk.model.domain_configuration import DomainConfiguration, DomainConfigurationSchema
from semantha_sdk.model.language import LanguageSchema
from semantha_sdk.model.matrix_row import MatrixRow, MatrixRowSchema
from semantha_sdk.model.model_class import ModelClassSchema
from semantha_sdk.model.model_instance import ModelInstance, ModelInstanceSchema
from semantha_sdk.model.semantic_model import SemanticModel, SemanticModelSchema


class DomainEndpoint(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: documents, documentannotations, documentclasses, documentcomparisons,
            modelclasses, modelinstances, referencedocuments, references,
            settings, stopwords, similaritymatrix, tags and validation.
    """
    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__documents = DocumentsEndpoint(session, self._endpoint)
        self.__document_annotations = DocumentAnnotationsEndpoint(session, self._endpoint)
        self.__document_classes = DocumentClassesEndpoint(session, self._endpoint)
        self.__document_comparisons = DocumentComparisonsEndpoint(session, self._endpoint)
        self.__reference_documents = ReferenceDocumentsEndpoint(session, self._endpoint)
        self.__domain_settings = DomainSettingsEndpoint(session, self._endpoint)
        self.__references = ReferencesEndpoint(session, self._endpoint)
        self.__tags = DomainTagsEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def documents(self):
        return self.__documents

    @property
    def documentannotations(self):
        return self.__document_annotations

    @property
    def documentclasses(self):
        return self.__document_classes

    @property
    def documentcomparisons(self):
        return self.__document_comparisons

    @property
    def referencedocuments(self) -> ReferenceDocumentsEndpoint:
        return self.__reference_documents

    @property
    def references(self) -> ReferencesEndpoint:
        return self.__references

    @property
    def settings(self) -> DomainSettingsEndpoint:
        return self.__domain_settings

    @property
    def tags(self) -> DomainTagsEndpoint:
        return self.__tags

    def modelclasses(self):
        return self._session.get(self._endpoint + "/modelclasses").execute().to(ModelClassSchema)

    def validation(self, file: IOBase) -> SemanticModel:
        endpoint = f"{self._endpoint}/validation"
        return self._session.post(endpoint, body={
            "file": file
        }).execute().to(SemanticModelSchema)

    def modelinstances(self, model: SemanticModel):
        model = SemanticModelSchema().dump(model)
        return self._session.post(self._endpoint, json=model).execute().to(ModelInstanceSchema)

    def modelinstances_form(self, file: IOBase, documentextractor: Optional[str] = None, withdocument: Optional[bool] = False):
        endpoint = f"{self._endpoint}/modelinstances"
        return self._session.post(
            endpoint,
            body={
                "file": file,
                "documentextractor": documentextractor,
            },
            q_params={
                "withdocument": withdocument
            }
        ).execute().to(ModelInstanceSchema)

    def get(self) -> DomainConfiguration:
        """Get the domain configuration"""
        return self._session.get(self._endpoint).execute().to(DomainConfigurationSchema)


# TODO: Add docstrings, comments, type hints and error handling.
class DomainsEndpoint(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def get(self) -> list[Domain]:
        """ Get all available domains """
        return self._session.get(self._endpoint).execute().to(DomainSchema)

    def __call__(self, domain_name: str) -> DomainEndpoint:
        return DomainEndpoint(self._session, self._endpoint, domain_name)
