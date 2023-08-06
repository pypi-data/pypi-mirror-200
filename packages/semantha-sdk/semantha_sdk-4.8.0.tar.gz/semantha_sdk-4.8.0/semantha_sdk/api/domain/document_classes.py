from __future__ import annotations

from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import Document, DocumentSchema
from semantha_sdk.model.document_class import DocumentClass as DocumentClassDTO, DocumentClassSchema, \
    CreateDocumentClass


class DocumentClassEndpoint(SemanthaAPIEndpoint):
    class _InnerDocumentClasses(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/documentclasses"

        def get(self) -> list[DocumentClassDTO]:
            """ Get all document classes

                Note:
                    * Only shows top-level classes, but not subclasses.
            """
            return self._session.get(self._endpoint).execute().to(DocumentClassSchema)

        def post(self, documentclass: DocumentClassDTO) -> DocumentClassDTO:
            """ Create a document class

                Limitations:
                    * Posting classes with unpublished subclasses won't publish them.
                    * Can only post a single class at once.
                    * Posting classes with subclasses doesn't work.
            """
            request = self._session.post(
                url=self._endpoint,
                json=DocumentClassSchema().dump(documentclass)
            )
            return request.execute().to(DocumentClassSchema)

    class _InnerReferenceDocuments(SemanthaAPIEndpoint):

        @property
        def _endpoint(self):
            return self._parent_endpoint + "/referencedocuments"

        def get(self) -> list[Document]:
            """ Get all library documents belonging to the document class """
            return self._session.get(self._endpoint).execute().to(DocumentSchema)

        def delete(self, documentids: list[str]) -> None:
            """ Delete all library documents belonging to the document class """
            self._session.delete(
                url=self._endpoint,
                json=documentids
            ).execute()

        def patch(self, documentids: list[str]) -> None:
            """ Link library documents to a document class identified by id """
            self._session.patch(
                url=self._endpoint,
                json=documentids
            ).execute()

    def __init__(self, session: RestClient, parent_endpoint: str, id: str):
        super().__init__(session, parent_endpoint)
        self._id = id
        self.__child_document_classes = DocumentClassEndpoint._InnerDocumentClasses(session, self._endpoint)
        self.__child_reference_documents = DocumentClassEndpoint._InnerReferenceDocuments(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._id}"

    @property
    def documentclasses(self):
        return self.__child_document_classes

    @property
    def referencedocuments(self):
        return self.__child_reference_documents

    def get(self) -> DocumentClassDTO:
        """ Get a specific document class """
        return self._session.get(url=self._endpoint).execute().to(DocumentClassSchema)

    def put(self, newcls: DocumentClassDTO) -> DocumentClassDTO:
        """ Overwrite attributes of an existing document class by providing a replacement """
        request = self._session.put(
            url=self._endpoint,
            json=DocumentClassSchema().dump(newcls)
        )
        return request.execute().to(DocumentClassSchema)

    def delete(self) -> None:
        """ Delete the document class """
        self._session.delete(url=self._endpoint).execute()


class DocumentClassesEndpoint(SemanthaAPIEndpoint):
    """ DocumentClasses endpoint, used to categorize documents from your library.
        Note: Document classes are called categories in the UI.
    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documentclasses"

    def get(self) -> list[DocumentClassDTO]:
        """ Get all document classes

            Note:
                * Only shows top-level classes, but not subclasses.
        """
        return self._session.get(self._endpoint).execute().to(DocumentClassSchema)

    def post(self, documentclass: CreateDocumentClass) -> DocumentClassDTO:
        """ Create a document class

            Limitations:
                * Posting classes with unpublished subclasses won't publish them.
                * Can only post a single class at once.
                * Posting classes with subclasses doesn't work.
        """
        request = self._session.post(
            url=self._endpoint,
            json=DocumentClassSchema().dump(documentclass)
        )

        return request.execute().to(DocumentClassSchema)

    def delete(self) -> None:
        """ Deletes all document classes """
        self._session.delete(self._endpoint).execute()

    def __call__(self, id: str):
        return DocumentClassEndpoint(self._session, self._endpoint, id)
