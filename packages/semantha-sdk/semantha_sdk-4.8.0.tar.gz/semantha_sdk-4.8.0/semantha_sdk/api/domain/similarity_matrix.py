from io import IOBase
from typing import Optional, List

from semantha_sdk import RestClient
from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.matrix_row import MatrixRow, MatrixRowSchema

class SimilarityMatrixCluster(SemanthaAPIEndpoint):
    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)

    @property
    def _endpoint(self):
        return f"{self._parent_endpoint}/cluster"

    def post(self, rows: List[MatrixRow]):
        endpoint = self._endpoint + "/similaritymatrix/cluster"
        matrix = MatrixRowSchema().dump(rows, many=True)
        return self._session.post(endpoint, json=matrix).execute().to(MatrixRowSchema)


class SimilarityMatrix(SemanthaAPIEndpoint):

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)

    @property
    def _endpoint(self):
        return f"{self._parent_endpoint}/similaritymatrix"

    def post(
            self,
            file: Optional[IOBase] = None,
            tags: Optional[str] = None,
            sourcetags: Optional[str] = None,
            documentids: Optional[List[str]] = None,
            sourcedocumentids: Optional[List[str]] = None,
            similaritythreshold: Optional[float] = None,
            language: Optional[str] = None,
            mode: Optional[str] = None,
            documenttype: Optional[str] = None,
            considertexttype: Optional[bool] = None
    ) -> list[MatrixRow]:
        endpoint = self._endpoint + "/similaritymatrix"
        return self._session.post(endpoint, {
            "file": file,
            "tags": tags,
            "sourcetags": sourcetags,
            "documentids": documentids,
            "sourcedocumentids": sourcedocumentids,
            "similaritythreshold": similaritythreshold,
            "language": language,
            "mode": mode,
            "documenttype": documenttype,
            "considertexttype": considertexttype
        }).execute().to(MatrixRowSchema)

    @property
    def cluster(self):
        return SimilarityMatrixCluster(self._session, self._endpoint)
