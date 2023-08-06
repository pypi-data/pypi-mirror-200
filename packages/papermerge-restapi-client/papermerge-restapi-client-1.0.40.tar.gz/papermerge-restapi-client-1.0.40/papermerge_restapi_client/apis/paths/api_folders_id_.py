from papermerge_restapi_client.paths.api_folders_id_.get import ApiForget
from papermerge_restapi_client.paths.api_folders_id_.delete import ApiFordelete
from papermerge_restapi_client.paths.api_folders_id_.patch import ApiForpatch


class ApiFoldersId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
