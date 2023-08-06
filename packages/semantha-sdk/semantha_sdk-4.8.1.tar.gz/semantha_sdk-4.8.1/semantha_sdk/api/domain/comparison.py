from __future__ import annotations

from io import IOBase
from typing import Optional

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.metadata import Metadata


class DocumentComparisonsEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/documentcomparisons"

    def post(
            self,
            file: IOBase,
            referencedocument: IOBase,
            similaritythreshold: Optional[float] = None,
            synonymousthreshold: Optional[float] = None,
            marknomatch: Optional[bool] = None,
            withreferencetext: Optional[bool] = None,
            documenttype: Optional[str] = None,
            metadata: Optional[list[Metadata]] = None,
            considertexttype: Optional[bool] = None
    ):
        """ (Not yet implemented) Determine references (for temporary data)

        Args:
            file (IOBase): Input document (left document).
            referencedocument (IOBase): Reference document(s) to be used instead of the documents in the domain's library.
            similaritythreshold (float): Threshold for the similarity score.
                semantha will not deliver results with a sentence score lower than the threshold.
                In general, the higher the threshold, the more precise the results.
            synonymousthreshold (float): Threshold for good matches.
            marknomatch (bool): Marks paragraphs that have not matched.
            withreferencetext (bool): Provide the reference text in the result document.
                If set to false, you have to query the library to resolve the references yourself.
            documenttype (str): Specifies the document type that is to be used by semantha when reading the uploaded document in 'file'.
            metadata (list[Metadata]): Specify document types for files uploaded in 'referencedocuments'.
            considertexttype (bool): Use this parameter to ensure that only paragraphs of the same type are compared with each other.
                The parameter is of type boolean and is set to false by default.
        """
        raise NotImplementedError()
        # return self._session.post(
        #     self._endpoint,
        #     body={
        #         "file": file,
        #         "referencedocument": referencedocument,
        #         "similaritythreshold": str(similaritythreshold),
        #         "synonymousthreshold": str(synonymousthreshold),
        #         "marknomatch": str(marknomatch),
        #         "withreferencetext": str(withreferencetext),
        #         "documenttype": documenttype,
        #         "metadata": metadata,
        #         "considertexttype": str(considertexttype)
        #     }).execute()