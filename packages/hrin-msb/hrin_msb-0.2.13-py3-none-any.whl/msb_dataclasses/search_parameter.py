from dataclasses import dataclass

from msb_cipher import Cipher
from msb_db._constants import (DEFAULT_QUERY_OFFSET, DEFAULT_QUERY_LIMIT)


@dataclass
class SearchParameter:
	_model_filters: dict
	_fields: list = None
	_order_by: str = None
	_limit: int = None
	_offset: int = None
	_order_field: str = None
	_filters = dict()
	_model_filter_map = dict()
	_auto_decrypt_filters = list()

	def get_query(self, for_model=None):
		self._init_model_filters(model=for_model)
		query_set = for_model.objects.filter(**self.filters)
		if self.fields:
			query_set = query_set.only(*self.fields)
		if self.order_field:
			query_set = query_set.order_by(self.order_field)
		return query_set

	def _init_model_filters(self, model=None):
		for key, value in self._filters.items():
			value = self.__parse_value(key=key, value=value, model=model)
			if key in self._model_filter_map.keys():
				self.add_filters(self._model_filter_map[key], value)
			elif hasattr(model, key):
				self.add_filters(key, value)

	def __parse_value(self, key, value, model):
		if key in self.auto_decrypt_fields_list(model):
			return Cipher.decrypt_list_items(*value) if isinstance(value, list) else Cipher.decrypt(value)
		return value

	def __init__(self, **kwargs):
		self._model_filters = dict()
		self._fields = kwargs.get('fields') or []
		self._order_by = kwargs.get('order_by') or 'ASC'
		self._limit = kwargs.get('limit') or DEFAULT_QUERY_LIMIT
		self._offset = kwargs.get('offset') or DEFAULT_QUERY_OFFSET
		self.order_field = kwargs.get('order_field')
		self._filters = kwargs.get('filters') or dict()

	def add_filters(self, key: str, value):
		if (isinstance(key, str) and value is not None) or (isinstance(value, list) and len(value) > 0):
			self._model_filters[key] = value

	def auto_decrypt_fields_list(self, model):
		_secure_field_list = self._auto_decrypt_filters if isinstance(self._auto_decrypt_filters, list) else []
		_secure_field_list.append(model._meta.pk.attname)
		_private_fields = getattr(model, "_private_fields", [])
		if isinstance(_private_fields, list):
			_secure_field_list.extend(_private_fields)
		return _secure_field_list

	@property
	def filters(self) -> dict:
		return self._model_filters

	@property
	def fields(self) -> list:
		return self._fields if isinstance(self._fields, list) and len(self._fields) > 0 else None

	@property
	def order_by(self) -> str:
		return self._order_by

	@property
	def limit(self) -> int:
		try:
			return int(self._limit) if int(self._limit) > 0 else DEFAULT_QUERY_LIMIT
		except Exception:
			return 0

	@property
	def offset(self) -> int:
		try:
			return int(self._offset) if int(self._offset) >= 0 else DEFAULT_QUERY_OFFSET
		except Exception:
			return 0

	@property
	def order_field(self) -> str:
		return self._order_field

	@order_field.setter
	def order_field(self, value):
		if value is not None:
			if self.order_by != 'ASC':
				self._order_field = f"-{value}"
			else:
				self._order_field = value
