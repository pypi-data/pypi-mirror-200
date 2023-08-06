from io import IOBase
from typing import Optional

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.document import Document, DocumentSchema


class DocumentAnnotationsEndpoint(SemanthaAPIEndpoint):
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documentannotations"

    def post(
            self,
            file: IOBase,
            document: Optional[Document] = None,
            similaritythreshold: Optional[float] = None,
            synonymousthreshold: Optional[float] = None,
            marknomatch: Optional[bool] = None,
            withreferencetext: Optional[bool] = None
    ):
        """ (Not yet implemented) Download the original input document with the referenced document/library matches as
        annotated comments.

        Args:
            file (IOBase): Input document (left document).
            document (Document): ...
            similaritythreshold (float): Threshold for the similarity score.
                semantha will not deliver results with a sentence score lower than the threshold.
                In general, the higher the threshold, the more precise the results.
            synonymousthreshold (float): Threshold for good matches.
            marknomatch (bool): Marks paragraphs that have not matched.
            withreferencetext (bool): Provide the reference text in the result JSON.
                If set to false, you have to query the library to resolve the references yourself.
        """
        document = DocumentSchema().dumps(document)

        return self._session.post(
            self._endpoint,
            body={
                "file": file,
                "document": document,
                "similaritythreshold": similaritythreshold,
                "synonymousthreshold": synonymousthreshold,
                "marknomatch": marknomatch,
                "withreferencetext": withreferencetext
            }
        )
