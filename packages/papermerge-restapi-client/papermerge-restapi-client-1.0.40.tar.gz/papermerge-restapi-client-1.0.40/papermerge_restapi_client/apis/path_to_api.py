import typing_extensions

from papermerge_restapi_client.paths import PathValues
from papermerge_restapi_client.apis.paths.api_auth_login_ import ApiAuthLogin
from papermerge_restapi_client.apis.paths.api_auth_logout_ import ApiAuthLogout
from papermerge_restapi_client.apis.paths.api_auth_logoutall_ import ApiAuthLogoutall
from papermerge_restapi_client.apis.paths.api_document_versions_id_ import ApiDocumentVersionsId
from papermerge_restapi_client.apis.paths.api_document_versions_id_download_ import ApiDocumentVersionsIdDownload
from papermerge_restapi_client.apis.paths.api_documents_ import ApiDocuments
from papermerge_restapi_client.apis.paths.api_documents_document_id_upload_file_name import ApiDocumentsDocumentIdUploadFileName
from papermerge_restapi_client.apis.paths.api_documents_id_ import ApiDocumentsId
from papermerge_restapi_client.apis.paths.api_documents_id_ocr_text import ApiDocumentsIdOcrText
from papermerge_restapi_client.apis.paths.api_documents_merge_ import ApiDocumentsMerge
from papermerge_restapi_client.apis.paths.api_folders_ import ApiFolders
from papermerge_restapi_client.apis.paths.api_folders_id_ import ApiFoldersId
from papermerge_restapi_client.apis.paths.api_groups_ import ApiGroups
from papermerge_restapi_client.apis.paths.api_groups_id_ import ApiGroupsId
from papermerge_restapi_client.apis.paths.api_nodes_ import ApiNodes
from papermerge_restapi_client.apis.paths.api_nodes_id_ import ApiNodesId
from papermerge_restapi_client.apis.paths.api_nodes_id_tags_ import ApiNodesIdTags
from papermerge_restapi_client.apis.paths.api_nodes_download_ import ApiNodesDownload
from papermerge_restapi_client.apis.paths.api_nodes_inboxcount_ import ApiNodesInboxcount
from papermerge_restapi_client.apis.paths.api_nodes_move_ import ApiNodesMove
from papermerge_restapi_client.apis.paths.api_ocr_ import ApiOcr
from papermerge_restapi_client.apis.paths.api_pages_ import ApiPages
from papermerge_restapi_client.apis.paths.api_pages_id_ import ApiPagesId
from papermerge_restapi_client.apis.paths.api_pages_move_to_document_ import ApiPagesMoveToDocument
from papermerge_restapi_client.apis.paths.api_pages_move_to_folder_ import ApiPagesMoveToFolder
from papermerge_restapi_client.apis.paths.api_pages_reorder_ import ApiPagesReorder
from papermerge_restapi_client.apis.paths.api_pages_rotate_ import ApiPagesRotate
from papermerge_restapi_client.apis.paths.api_permissions_ import ApiPermissions
from papermerge_restapi_client.apis.paths.api_preferences_ import ApiPreferences
from papermerge_restapi_client.apis.paths.api_preferences_id_ import ApiPreferencesId
from papermerge_restapi_client.apis.paths.api_preferences_bulk_ import ApiPreferencesBulk
from papermerge_restapi_client.apis.paths.api_schema_ import ApiSchema
from papermerge_restapi_client.apis.paths.api_search_ import ApiSearch
from papermerge_restapi_client.apis.paths.api_tags_ import ApiTags
from papermerge_restapi_client.apis.paths.api_tags_id_ import ApiTagsId
from papermerge_restapi_client.apis.paths.api_tokens_ import ApiTokens
from papermerge_restapi_client.apis.paths.api_tokens_digest_ import ApiTokensDigest
from papermerge_restapi_client.apis.paths.api_users_ import ApiUsers
from papermerge_restapi_client.apis.paths.api_users_id_ import ApiUsersId
from papermerge_restapi_client.apis.paths.api_users_id_change_password_ import ApiUsersIdChangePassword
from papermerge_restapi_client.apis.paths.api_users_me_ import ApiUsersMe
from papermerge_restapi_client.apis.paths.api_version_ import ApiVersion

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_AUTH_LOGIN_: ApiAuthLogin,
        PathValues.API_AUTH_LOGOUT_: ApiAuthLogout,
        PathValues.API_AUTH_LOGOUTALL_: ApiAuthLogoutall,
        PathValues.API_DOCUMENTVERSIONS_ID_: ApiDocumentVersionsId,
        PathValues.API_DOCUMENTVERSIONS_ID_DOWNLOAD_: ApiDocumentVersionsIdDownload,
        PathValues.API_DOCUMENTS_: ApiDocuments,
        PathValues.API_DOCUMENTS_DOCUMENT_ID_UPLOAD_FILE_NAME: ApiDocumentsDocumentIdUploadFileName,
        PathValues.API_DOCUMENTS_ID_: ApiDocumentsId,
        PathValues.API_DOCUMENTS_ID_OCRTEXT: ApiDocumentsIdOcrText,
        PathValues.API_DOCUMENTS_MERGE_: ApiDocumentsMerge,
        PathValues.API_FOLDERS_: ApiFolders,
        PathValues.API_FOLDERS_ID_: ApiFoldersId,
        PathValues.API_GROUPS_: ApiGroups,
        PathValues.API_GROUPS_ID_: ApiGroupsId,
        PathValues.API_NODES_: ApiNodes,
        PathValues.API_NODES_ID_: ApiNodesId,
        PathValues.API_NODES_ID_TAGS_: ApiNodesIdTags,
        PathValues.API_NODES_DOWNLOAD_: ApiNodesDownload,
        PathValues.API_NODES_INBOXCOUNT_: ApiNodesInboxcount,
        PathValues.API_NODES_MOVE_: ApiNodesMove,
        PathValues.API_OCR_: ApiOcr,
        PathValues.API_PAGES_: ApiPages,
        PathValues.API_PAGES_ID_: ApiPagesId,
        PathValues.API_PAGES_MOVETODOCUMENT_: ApiPagesMoveToDocument,
        PathValues.API_PAGES_MOVETOFOLDER_: ApiPagesMoveToFolder,
        PathValues.API_PAGES_REORDER_: ApiPagesReorder,
        PathValues.API_PAGES_ROTATE_: ApiPagesRotate,
        PathValues.API_PERMISSIONS_: ApiPermissions,
        PathValues.API_PREFERENCES_: ApiPreferences,
        PathValues.API_PREFERENCES_ID_: ApiPreferencesId,
        PathValues.API_PREFERENCES_BULK_: ApiPreferencesBulk,
        PathValues.API_SCHEMA_: ApiSchema,
        PathValues.API_SEARCH_: ApiSearch,
        PathValues.API_TAGS_: ApiTags,
        PathValues.API_TAGS_ID_: ApiTagsId,
        PathValues.API_TOKENS_: ApiTokens,
        PathValues.API_TOKENS_DIGEST_: ApiTokensDigest,
        PathValues.API_USERS_: ApiUsers,
        PathValues.API_USERS_ID_: ApiUsersId,
        PathValues.API_USERS_ID_CHANGEPASSWORD_: ApiUsersIdChangePassword,
        PathValues.API_USERS_ME_: ApiUsersMe,
        PathValues.API_VERSION_: ApiVersion,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_AUTH_LOGIN_: ApiAuthLogin,
        PathValues.API_AUTH_LOGOUT_: ApiAuthLogout,
        PathValues.API_AUTH_LOGOUTALL_: ApiAuthLogoutall,
        PathValues.API_DOCUMENTVERSIONS_ID_: ApiDocumentVersionsId,
        PathValues.API_DOCUMENTVERSIONS_ID_DOWNLOAD_: ApiDocumentVersionsIdDownload,
        PathValues.API_DOCUMENTS_: ApiDocuments,
        PathValues.API_DOCUMENTS_DOCUMENT_ID_UPLOAD_FILE_NAME: ApiDocumentsDocumentIdUploadFileName,
        PathValues.API_DOCUMENTS_ID_: ApiDocumentsId,
        PathValues.API_DOCUMENTS_ID_OCRTEXT: ApiDocumentsIdOcrText,
        PathValues.API_DOCUMENTS_MERGE_: ApiDocumentsMerge,
        PathValues.API_FOLDERS_: ApiFolders,
        PathValues.API_FOLDERS_ID_: ApiFoldersId,
        PathValues.API_GROUPS_: ApiGroups,
        PathValues.API_GROUPS_ID_: ApiGroupsId,
        PathValues.API_NODES_: ApiNodes,
        PathValues.API_NODES_ID_: ApiNodesId,
        PathValues.API_NODES_ID_TAGS_: ApiNodesIdTags,
        PathValues.API_NODES_DOWNLOAD_: ApiNodesDownload,
        PathValues.API_NODES_INBOXCOUNT_: ApiNodesInboxcount,
        PathValues.API_NODES_MOVE_: ApiNodesMove,
        PathValues.API_OCR_: ApiOcr,
        PathValues.API_PAGES_: ApiPages,
        PathValues.API_PAGES_ID_: ApiPagesId,
        PathValues.API_PAGES_MOVETODOCUMENT_: ApiPagesMoveToDocument,
        PathValues.API_PAGES_MOVETOFOLDER_: ApiPagesMoveToFolder,
        PathValues.API_PAGES_REORDER_: ApiPagesReorder,
        PathValues.API_PAGES_ROTATE_: ApiPagesRotate,
        PathValues.API_PERMISSIONS_: ApiPermissions,
        PathValues.API_PREFERENCES_: ApiPreferences,
        PathValues.API_PREFERENCES_ID_: ApiPreferencesId,
        PathValues.API_PREFERENCES_BULK_: ApiPreferencesBulk,
        PathValues.API_SCHEMA_: ApiSchema,
        PathValues.API_SEARCH_: ApiSearch,
        PathValues.API_TAGS_: ApiTags,
        PathValues.API_TAGS_ID_: ApiTagsId,
        PathValues.API_TOKENS_: ApiTokens,
        PathValues.API_TOKENS_DIGEST_: ApiTokensDigest,
        PathValues.API_USERS_: ApiUsers,
        PathValues.API_USERS_ID_: ApiUsersId,
        PathValues.API_USERS_ID_CHANGEPASSWORD_: ApiUsersIdChangePassword,
        PathValues.API_USERS_ME_: ApiUsersMe,
        PathValues.API_VERSION_: ApiVersion,
    }
)
