from msb_const.http import RequestMethod
from ._dataclasses import ApiRequestData
from ._dataclasses import ApiResponseWrapper
from ._utils import make_api_request


class ApiRequestClient(ApiRequestData):

	def __str__(self):
		return f"<{self.__class__.__name__} '{self.request_url}' >"

	def __repr__(self):
		return self.__str__()

	def GET(self, query_params: [list, dict] = None) -> ApiResponseWrapper:
		return self.set_query_params(query_params).set_request_method(RequestMethod.GET).execute()

	def POST(self, data=None, query_params: [list, dict] = None) -> ApiResponseWrapper:
		return self.set_query_params(query_params).set_request_method(RequestMethod.POST).set_data(data).execute()

	def PUT(self, data=None, query_params: [list, dict] = None) -> ApiResponseWrapper:
		return self.set_query_params(query_params).set_request_method(RequestMethod.PUT).set_data(data).execute()

	def DELETE(self, data=None, query_params: [list, dict] = None) -> ApiResponseWrapper:
		return self.set_query_params(query_params).set_request_method(RequestMethod.DELETE).set_data(data).execute()

	def execute(self) -> ApiResponseWrapper:
		return make_api_request(self)
