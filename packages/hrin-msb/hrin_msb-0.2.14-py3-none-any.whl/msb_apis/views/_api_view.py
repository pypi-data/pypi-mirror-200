from rest_framework import (viewsets, serializers)

from msb_auth import TokenUser, LoginRequiredPermission
from ._constants import DEFAULT_LOGGER_NAME
from msb_http import (ApiResponse, RequestInfo, RequestHeaders)

from typing import Union


def api_details(request=None, ver='', name=''):
	return ApiResponse.success(
		data=dict(method=request.method, version=ver, name=name)
	)


class ApiView(viewsets.GenericViewSet):
	permission_classes = (LoginRequiredPermission,)
	serializer_class = serializers.Serializer
	default_logger: str = DEFAULT_LOGGER_NAME

	"""
	TODO : implement following code :
	
	@staticmethod
	@renderer_classes((JSONRenderer))
	def my_exception_handler(exc, context):
		# response = exception_handler(exc, context)  # <-- this is the default exception_handler
		import logging
		logging.exception(exc)
		return ApiResponse.internal_server_error()

	def get_exception_handler(self):
		return self.my_exception_handler
	"""

	@property
	def request_info(self) -> RequestInfo:
		return RequestInfo(meta=self.request.META)

	@property
	def request_headers(self) -> RequestHeaders:
		return RequestHeaders(headers=self.request.headers)

	@property
	def user(self) -> TokenUser:
		return self.request.user

	@property
	def payload(self) -> dict | list:
		return self.request.data if type(self.request.data) in [list, dict] else {}

	@property
	def params(self)->dict:
		return self.request.query_params.dict()

	@property
	def logger(self):
		import logging
		return logging.getLogger(self.default_logger)

	@property
	def api_response(self):
		return ApiResponse

	def serializer(self, data: Union[list, dict] = None) -> Union[list, dict]:
		from django.db.models import QuerySet
		if isinstance(data, dict):
			return data

		return (
			[item.dict() if hasattr(item, 'dict') else item for item in data]
		) if (type(data) in [list, QuerySet]) else []
