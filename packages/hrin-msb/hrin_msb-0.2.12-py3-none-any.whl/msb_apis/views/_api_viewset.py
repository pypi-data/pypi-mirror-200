from django.db.models import QuerySet

from msb_dataclasses import SearchParameter
from msb_http import (RestResponse)
from msb_validation import DefaultRules, validate_against, InvalidPayloadException, ValidationSchema
from ._api_view import ApiView
from ._constants import (CrudActions, CRUD_URL_PK_NAME)
from ._exceptions import CrudApiExceptions
from ._funcs import MsbApiRoutes
from ..services import ApiService


class ApiViewset(ApiView, MsbApiRoutes):
	service_class: ApiService = None
	validation_schema_class = None
	search_parameter_class: SearchParameter = SearchParameter
	pk_name: str = CRUD_URL_PK_NAME

	def __validate_crud_request(self, action: str, inp=None, unknown=True, bulk=False, rule=None):
		if self.validation_schema_class is None:
			raise CrudApiExceptions.SchemaValidationClassNotDefined
		_validation_rule = rule if isinstance(rule, ValidationSchema) else \
			self.validation_schema_class.get(action, default=ValidationSchema())
		if (validation_errors := validate_against(schema=_validation_rule, inp=inp, unknown=unknown, bulk=bulk)) is not None:
			raise InvalidPayloadException(errors=validation_errors)

	def api_not_found(self, request, *args, **kwargs) -> RestResponse:
		return self.api_response.not_found()

	def create(self, *args, **kwargs) -> RestResponse:
		try:
			is_bulk = not isinstance(self.payload, dict)
			self.__validate_crud_request(CrudActions.create, inp=self.payload, unknown=False, bulk=is_bulk)
			_create_payload = [self.payload] if not is_bulk else self.payload

			if not (result := self.service_class.create(*_create_payload)):
				raise CrudApiExceptions.CreateOperationFailed
			return self.api_response.success()

		except Exception as e:
			return self.api_response.exception(e)

	def retrieve(self, *args, **kwargs) -> RestResponse:
		try:
			self.__validate_crud_request(CrudActions.retrieve, inp=kwargs)
			_pk = kwargs.get(self.pk_name)
			result = self.service_class.retrieve(pk=_pk)
			return self.api_response.success(data=self.serializer(data=[result]))
		except Exception as e:
			return self.api_response.exception(e=e)

	def list(self, *args, **kwargs) -> RestResponse:
		try:
			limit = self.params.get('limit')
			offset = self.params.get('offset')
			query_data = self.service_class.list(limit=limit, offset=offset)
			if isinstance(query_data, QuerySet):
				query_data = [data.list_fields for data in query_data]

			return self.api_response.success(data=query_data)
		except Exception as e:
			return self.api_response.exception(e=e)

	def update(self, *args, **kwargs) -> RestResponse:
		try:
			_rule = DefaultRules.pk_validation_rule(self.pk_name)
			_pk = kwargs.get(self.pk_name)
			_update_data = self.payload
			self.__validate_crud_request(CrudActions.update, inp=kwargs, rule=_rule)
			self.__validate_crud_request(CrudActions.update, inp=_update_data)
			result = self.service_class.update(pk=_pk, **_update_data)
			if not (result):
				raise CrudApiExceptions.UpdateOperationFailed
			return self.api_response.success()
		except Exception as e:
			return self.api_response.exception(e=e)

	def bulk_update(self, *args, **kwargs) -> RestResponse:
		try:
			_payload_list = [self.payload] if isinstance(self.payload, dict) else self.payload
			self.__validate_crud_request(CrudActions.update, inp=_payload_list, bulk=True)
			for _payload in _payload_list:
				if (_pk := _payload.get(self.pk_name)) is not None:
					del _payload[self.pk_name]
					self.service_class.update(pk=_pk, **_payload)
			return self.api_response.success()
		except Exception as e:
			return self.api_response.exception(e=e)

	def delete(self, *args, **kwargs) -> RestResponse:
		try:
			_rule = DefaultRules.pk_validation_rule(self.pk_name)
			_pk = kwargs.get(self.pk_name)
			self.__validate_crud_request(CrudActions.delete, inp=kwargs, rule=_rule)
			if not (result := self.service_class.delete(pk=_pk)):
				raise CrudApiExceptions.DeleteOperationFailed
			return self.api_response.success()
		except Exception as e:
			return self.api_response.exception(e=e)

	def bulk_delete(self, *args, **kwargs) -> RestResponse:
		try:
			_rule = DefaultRules.pk_validation_rule(self.pk_name)
			_payload = [self.payload] if isinstance(self.payload, dict) else self.payload
			self.__validate_crud_request(CrudActions.delete, inp=_payload, rule=_rule, bulk=True)
			for pk_details in _payload:
				_pk = pk_details.get(self.pk_name)
				self.service_class.delete(pk=_pk)
			return self.api_response.success()
		except Exception as e:
			return self.api_response.exception(e=e)

	def search(self, *args, **kwargs):
		try:
			_rule = DefaultRules.search_validation_rule()
			self.__validate_crud_request(CrudActions.search, inp=self.payload, rule=_rule)

			_search_parameters = self.search_parameter_class(**self.payload)
			result = self.service_class.search(params=_search_parameters)
			return self.api_response.success(data=self.serializer(data=result))
		except Exception as e:
			return self.api_response.exception(e)
