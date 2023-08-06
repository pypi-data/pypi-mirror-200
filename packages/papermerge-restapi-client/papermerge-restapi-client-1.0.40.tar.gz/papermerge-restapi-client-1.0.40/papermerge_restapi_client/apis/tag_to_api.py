import typing_extensions

from papermerge_restapi_client.apis.tags import TagValues
from papermerge_restapi_client.apis.tags.auth_api import AuthApi
from papermerge_restapi_client.apis.tags.document_versions_api import DocumentVersionsApi
from papermerge_restapi_client.apis.tags.documents_api import DocumentsApi
from papermerge_restapi_client.apis.tags.folders_api import FoldersApi
from papermerge_restapi_client.apis.tags.groups_api import GroupsApi
from papermerge_restapi_client.apis.tags.nodes_api import NodesApi
from papermerge_restapi_client.apis.tags.ocr_api import OcrApi
from papermerge_restapi_client.apis.tags.pages_api import PagesApi
from papermerge_restapi_client.apis.tags.permissions_api import PermissionsApi
from papermerge_restapi_client.apis.tags.preferences_api import PreferencesApi
from papermerge_restapi_client.apis.tags.schema_api import SchemaApi
from papermerge_restapi_client.apis.tags.search_api import SearchApi
from papermerge_restapi_client.apis.tags.tags_api import TagsApi
from papermerge_restapi_client.apis.tags.tokens_api import TokensApi
from papermerge_restapi_client.apis.tags.users_api import UsersApi
from papermerge_restapi_client.apis.tags.version_api import VersionApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.AUTH: AuthApi,
        TagValues.DOCUMENTVERSIONS: DocumentVersionsApi,
        TagValues.DOCUMENTS: DocumentsApi,
        TagValues.FOLDERS: FoldersApi,
        TagValues.GROUPS: GroupsApi,
        TagValues.NODES: NodesApi,
        TagValues.OCR: OcrApi,
        TagValues.PAGES: PagesApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.PREFERENCES: PreferencesApi,
        TagValues.SCHEMA: SchemaApi,
        TagValues.SEARCH: SearchApi,
        TagValues.TAGS: TagsApi,
        TagValues.TOKENS: TokensApi,
        TagValues.USERS: UsersApi,
        TagValues.VERSION: VersionApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.AUTH: AuthApi,
        TagValues.DOCUMENTVERSIONS: DocumentVersionsApi,
        TagValues.DOCUMENTS: DocumentsApi,
        TagValues.FOLDERS: FoldersApi,
        TagValues.GROUPS: GroupsApi,
        TagValues.NODES: NodesApi,
        TagValues.OCR: OcrApi,
        TagValues.PAGES: PagesApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.PREFERENCES: PreferencesApi,
        TagValues.SCHEMA: SchemaApi,
        TagValues.SEARCH: SearchApi,
        TagValues.TAGS: TagsApi,
        TagValues.TOKENS: TokensApi,
        TagValues.USERS: UsersApi,
        TagValues.VERSION: VersionApi,
    }
)
