from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from requests.models import Response
from rest_framework import request as drf_request
from rest_framework.request import Request as RestRequest

from msb_config import Config
from msb_const import const_http
from msb_dataclasses import Singleton
from ._exceptions import ApiRequestExceptions


class HostUrlsConfig(metaclass=Singleton):
	__config_key = "{service_name}_SERVICE_URL"

	def __get_service_host(self, service_name: str):
		_config_name = self.__config_key.format(service_name=service_name.upper())
		return Config.get(_config_name).as_str(default=None)

	def using(self, request_path: str):
		_remote_service_url, *_service_url = (None, [])

		# Separate base service and url from main url
		_service_name, *_service_url = request_path.lstrip("/").split("/")
		_remote_service_url = self.__get_service_host(service_name=_service_name)

		if Config.is_local_env():
			print(f"{_remote_service_url = }")

		return _remote_service_url, "/".join(_service_url)


class ApiRequestData:

	@property
	def request_is_valid(self) -> bool:
		return True

	@property
	def request_is_json(self) -> bool:
		return self.headers.get(const_http.HEADER_NAME_CONTENT_TYPE) == const_http.CONTENT_TYPE_APPLICATION_JSON

	@property
	def request_verify_certificate(self) -> bool:
		return False

	@property
	def request_method(self):
		return self.method

	@property
	def request_headers(self):
		return self.headers

	@property
	def request_query(self):
		return self.query_params

	@property
	def request_url(self):
		return f"{self.endpoint}"

	@property
	def request_cookies(self):
		return self.cookies

	@property
	def request_data(self):
		return self.data

	def __set_endpoint(self, endpoint: str):
		self.endpoint = endpoint.rstrip("/")
		return self

	def set_api_host(self, host: str):
		self.api_host = host if isinstance(host, str) and len(host) > 0 else None
		return self

	def add_header(self, name: str, value: str):
		self.headers[name] = value
		return self

	def set_data(self, data: [list, dict]):
		self.data = data
		return self

	def set_query_params(self, params: [list, dict]):
		_query_params = ""
		if (params_type := type(params)) in [list, dict]:
			if params_type == dict:
				_query_params = "&".join([f"{k}={v}" for k, v in params.items()])
			else:
				_query_params = "/".join(params)
		self.query_params = _query_params
		return self

	def set_cookies(self, cookies):
		self.cookies = cookies
		return self

	def set_request_method(self, method: str):
		self.method = method
		return self

	def __init__(self, endpoint: str, request: RestRequest = None):
		self.method = None
		self.__set_endpoint(endpoint)
		self.set_query_params([])
		self.set_data({})
		self.headers = request.headers if isinstance(request, RestRequest) else dict()
		self.cookies = request.META.get('HTTP_COOKIE') if isinstance(request, RestRequest) else None


class ApiResponseWrapper:
	__response: Response

	@property
	def response(self) -> Response:
		return self.__response

	def __init__(self, response: Response):
		self.__response = response

	def to_json(self) -> dict:
		if self.__response.headers.get(const_http.HEADER_NAME_CONTENT_TYPE) == const_http.CONTENT_TYPE_APPLICATION_JSON:
			return self.__response.json()

		if self.__response.status_code in [404]:
			raise ApiRequestExceptions.ResourceNotFound


@dataclass
class RequestWrapper:
	request: Union[drf_request.Request] = None

	@property
	def meta(self) -> dict:
		return self.request.META or {}

	@property
	def headers(self) -> dict:
		return self.request.headers or {}

	@property
	def cookie(self):
		return self.meta.get('HTTP_COOKIE')

	@property
	def path(self) -> str:
		return self.meta.get('PATH_INFO')

	@property
	def ip(self):
		return self.headers.get('X-Real-Ip')  or self.meta.get('REMOTE_ADDR')

	@property
	def method(self) -> str:
		return self.meta.get('REQUEST_METHOD')

	@property
	def script(self) -> str:
		return self.meta.get('SCRIPT_NAME')

	@property
	def server(self) -> str:
		return self.meta.get('SERVER_NAME')

	@property
	def port(self) -> int:
		return int(self.meta.get('SERVER_PORT'))

	@property
	def protocol(self) -> str:
		return self.meta.get('SERVER_PROTOCOL')

	@property
	def content_type(self) -> str:
		return self.meta.get('CONTENT_TYPE')

	@property
	def query_string(self) -> str:
		return self.meta.get('QUERY_STRING')

	@property
	def authorization(self) -> str:
		return self.meta.get('HTTP_AUTHORIZATION')

	@property
	def user_agent(self) -> str:
		return self.headers.get('User-Agent')
