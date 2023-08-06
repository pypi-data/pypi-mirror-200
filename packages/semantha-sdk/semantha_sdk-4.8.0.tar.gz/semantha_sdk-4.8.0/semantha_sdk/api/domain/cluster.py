from __future__ import annotations

from typing import Optional

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.cluster import DocumentCluster, DocumentClusterSchema, ClusterDocumentsResponse, \
    ClusterDocumentsResponseSchema


class DocumentClusterEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/clusters"

    def get(
            self,
            tags: Optional[str] = None,
            minclustersize: Optional[str] = None,
            clusteringstructure: Optional[str] = None
    ) -> ClusterDocumentsResponse:
        """ Get document clusters, i.e. a semantic clustering of the documents in the library. Clusters are named and
        have an integer ID. Note that a special cluster with ID '-1' is reserved for outliers, i.e. documents that could
        not have been assigned to a cluster.
        Args:
            tags: List of tags to filter the reference library. You can combine the tags using a comma (OR) and using a plus sign (AND).
            minclustersize: choose whether to require only a few documents to form a cluster or more. Choose from
                                     either 'LOW', 'MEDIUM' or 'HIGH'.
            clusteringstructure: the strategy the clustering algorithm uses to create the clustering space. Choose from
                                  either 'LOCAL', 'BALANCED' or 'GLOBAL' (default 'BALANCED') where LOCAL means that the
                                  model is able to better represent dense structure and GLOBAL means that more
                                  datapoints are considered and the model better represents the overall structure of the
                                  data but lacks details.

        Compatibility note: In future releases more parameters will be added to alter the clustering.
        """
        q_params = {}
        if tags is not None:
            q_params["tags"] = tags
        if minclustersize is not None:
            q_params["minclustersize"] = minclustersize
        if clusteringstructure is not None:
            q_params["clusteringstructure"] = clusteringstructure
        return self._session.get(
            self._endpoint,
            q_params=q_params
        ).execute().to(ClusterDocumentsResponseSchema)
