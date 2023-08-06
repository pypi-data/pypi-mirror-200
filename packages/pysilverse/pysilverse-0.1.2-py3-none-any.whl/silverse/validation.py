from ctypes import POINTER, c_void_p
import json
from typing import Callable

from cerver.types import String

from cerver.http import http_request_get_body

def silverse_handle_body_input (
	request: c_void_p, handle_body_input: Callable [[dict, dict], dict], errors: dict
) -> dict:
	values = None

	body_json: POINTER (String) = http_request_get_body (request)

	if (body_json is not None):
		loaded_json: dict = json.loads (body_json.contents.str)

		values = handle_body_input (loaded_json, errors)

	else:
		errors["body"] = "Request body input is required!"

	return values
