from papermerge_restapi_client.paths.api_tags_id_.get import ApiForget
from papermerge_restapi_client.paths.api_tags_id_.delete import ApiFordelete
from papermerge_restapi_client.paths.api_tags_id_.patch import ApiForpatch


class ApiTagsId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
