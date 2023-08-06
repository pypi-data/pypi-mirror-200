from json import dump as json_dump

from ._client import ApiRequestClient
from ._dataclasses import ApiRequestData, RestRequest


class ApiRouter(ApiRequestData):

	def _get_payload(self, request: RestRequest):
		if self.method.lower() in ['get']:
			return None

		return json_dump((request.data if type(request.data) in [list, dict] else {}))

	def __init__(self, request: RestRequest):
		super(ApiRouter, self).__init__(request=request)
		self.set_request_method(request.method)
		self.set_data(self._get_payload(request))


class MsbIntraServiceRequest:
	api_host: str
	__request_url_pattern: str = "{host}/v{version}/{endpoint}"
	__version: int
	__request_obj: RestRequest

	def __get_endpoint(self, endpoint):
		return self.__request_url_pattern.format(
			host=str(self.api_host).rstrip("/"),
			version=self.__version, endpoint=endpoint
		).rstrip("/")

	def __init__(self, version: int = 1):
		self.__version = version
		self.__request_obj = None

	def _api_request_instance(self, endpoint: str) -> ApiRequestClient:
		return ApiRequestClient(endpoint=self.__get_endpoint(endpoint=endpoint), request=self.__request_obj)

	def using(self, request: RestRequest):
		self.__request_obj = request
		return self
