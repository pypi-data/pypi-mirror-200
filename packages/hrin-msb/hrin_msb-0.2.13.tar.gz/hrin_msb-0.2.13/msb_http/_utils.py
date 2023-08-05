import logging

from requests.models import Response

from msb_config import Config
from ._dataclasses import ApiRequestData, ApiResponseWrapper
from ._exceptions import ApiRequestExceptions


def make_api_request(request_data: ApiRequestData) -> ApiResponseWrapper:
	from requests import (api, ConnectionError)
	api_response = Response()
	try:

		api_response = api.request(
			method=request_data.request_method,
			url=request_data.request_url,
			verify=request_data.request_verify_certificate,
			cookies=request_data.request_cookies,
			data=request_data.request_data,
			headers=request_data.request_headers,
			json=request_data.request_is_json,
		)
	except ConnectionError as ce:
		if Config.is_local_env():
			logging.exception(ce)
		raise ApiRequestExceptions.ResourceNotFound
	except Exception as e:
		if Config.is_local_env():
			logging.exception(e)
		raise ApiRequestExceptions.InternalServerError

	return ApiResponseWrapper(api_response)
