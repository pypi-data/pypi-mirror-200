from papermerge_restapi_client.paths.api_nodes_id_.get import ApiForget
from papermerge_restapi_client.paths.api_nodes_id_.delete import ApiFordelete
from papermerge_restapi_client.paths.api_nodes_id_.patch import ApiForpatch


class ApiNodesId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
