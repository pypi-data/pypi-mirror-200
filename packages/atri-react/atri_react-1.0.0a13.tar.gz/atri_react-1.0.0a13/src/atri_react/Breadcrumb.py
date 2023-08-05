from typing import Any, Union
from atri_core import AtriComponent



class BreadcrumbCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.separator: Union[Any, None] = state["separator"] if state != None and "separator" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def separator(self):
		self._getter_access_tracker["separator"] = {}
		return self._separator
	@separator.setter
	def separator(self, state):
		self._setter_access_tracker["separator"] = {}
		self._separator = state
	@property
	def items(self):
		self._getter_access_tracker["items"] = {}
		return self._items
	@items.setter
	def items(self, state):
		self._setter_access_tracker["items"] = {}
		self._items = state

	def _to_json_fields(self):
		return {
			"separator": self._separator,
			"items": self._items
			}


class Breadcrumb(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Breadcrumb"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
		self.custom = state["custom"] if state != None and "custom" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def custom(self):
		self._getter_access_tracker["custom"] = {}
		return self._custom
	@custom.setter
	def custom(self, state):
		self._setter_access_tracker["custom"] = {}
		self._custom = BreadcrumbCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}