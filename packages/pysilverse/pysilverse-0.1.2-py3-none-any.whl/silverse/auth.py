from ctypes import c_void_p, c_char_p
from ctypes import c_int, c_uint, c_int64, c_bool

from .lib import lib

SILVERSE_AUTH_TYPE_NONE = 0
SILVERSE_AUTH_TYPE_TOKEN = 1
SILVERSE_AUTH_TYPE_ACTION = 2
SILVERSE_AUTH_TYPE_ROLE = 3
SILVERSE_AUTH_TYPE_SERVICE = 4
SILVERSE_AUTH_TYPE_PERMISSIONS = 5
SILVERSE_AUTH_TYPE_MULTIPLE = 6
SILVERSE_AUTH_TYPE_COMPLETE = 7

SILVERSE_AUTH_SCOPE_NONE = 0
SILVERSE_AUTH_SCOPE_SINGLE = 1
SILVERSE_AUTH_SCOPE_MANAGEMENT = 2

silverse_auth_type_to_string = lib.silverse_auth_type_to_string
silverse_auth_type_to_string.argtypes = [c_int]
silverse_auth_type_to_string.restype = c_char_p

silverse_auth_scope_to_string = lib.silverse_auth_scope_to_string
silverse_auth_scope_to_string.argtypes = [c_int]
silverse_auth_scope_to_string.restype = c_char_p

silverse_auth_delete = lib.silverse_auth_delete
silverse_auth_delete.argtypes = [c_void_p]

silverse_auth_get_type = lib.silverse_auth_get_type
silverse_auth_get_type.argtypes = [c_void_p]
silverse_auth_get_type.restype = c_int

silverse_auth_get_scope = lib.silverse_auth_get_scope
silverse_auth_get_scope.argtypes = [c_void_p]
silverse_auth_get_scope.restype = c_int

silverse_auth_get_admin = lib.silverse_auth_get_admin
silverse_auth_get_admin.argtypes = [c_void_p]
silverse_auth_get_admin.restype = c_bool

silverse_auth_get_token_id = lib.silverse_auth_get_token_id
silverse_auth_get_token_id.argtypes = [c_void_p]
silverse_auth_get_token_id.restype = c_char_p

silverse_auth_get_token_type = lib.silverse_auth_get_token_type
silverse_auth_get_token_type.argtypes = [c_void_p]
silverse_auth_get_token_type.restype = c_int

silverse_auth_get_token_organization = lib.silverse_auth_get_token_organization
silverse_auth_get_token_organization.argtypes = [c_void_p]
silverse_auth_get_token_organization.restype = c_char_p

silverse_auth_get_token_permissions = lib.silverse_auth_get_token_permissions
silverse_auth_get_token_permissions.argtypes = [c_void_p]
silverse_auth_get_token_permissions.restype = c_char_p

silverse_auth_get_token_role = lib.silverse_auth_get_token_role
silverse_auth_get_token_role.argtypes = [c_void_p]
silverse_auth_get_token_role.restype = c_char_p

silverse_auth_get_token_user = lib.silverse_auth_get_token_user
silverse_auth_get_token_user.argtypes = [c_void_p]
silverse_auth_get_token_user.restype = c_char_p

silverse_auth_get_token_username = lib.silverse_auth_get_token_username
silverse_auth_get_token_username.argtypes = [c_void_p]
silverse_auth_get_token_username.restype = c_char_p

silverse_auth_get_mask = lib.silverse_auth_get_mask
silverse_auth_get_mask.argtypes = [c_void_p]
silverse_auth_get_mask.restype = c_int64

silverse_auth_create = lib.silverse_auth_create
silverse_auth_create.argtypes = [c_int]
silverse_auth_create.restype = c_void_p

silverse_auth_print_token = lib.silverse_auth_print_token
silverse_auth_print_token.argtypes = [c_void_p]

silverse_custom_authentication_handler = lib.silverse_custom_authentication_handler
silverse_custom_authentication_handler.argtypes = [c_void_p, c_void_p]
silverse_custom_authentication_handler.restype = c_uint
