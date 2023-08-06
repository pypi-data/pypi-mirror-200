# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from papermerge_restapi_client.apis.tag_to_api import tag_to_api

import enum


class TagValues(str, enum.Enum):
    AUTH = "auth"
    DOCUMENTVERSIONS = "document-versions"
    DOCUMENTS = "documents"
    FOLDERS = "folders"
    GROUPS = "groups"
    NODES = "nodes"
    OCR = "ocr"
    PAGES = "pages"
    PERMISSIONS = "permissions"
    PREFERENCES = "preferences"
    SCHEMA = "schema"
    SEARCH = "search"
    TAGS = "tags"
    TOKENS = "tokens"
    USERS = "users"
    VERSION = "version"
