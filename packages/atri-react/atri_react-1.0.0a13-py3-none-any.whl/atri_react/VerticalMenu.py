from typing import Any, Union
from atri_core import AtriComponent



class VerticalMenuCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.menuItems: Union[Any, None] = state["menuItems"] if state != None and "menuItems" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def menuItems(self):
		self._getter_access_tracker["menuItems"] = {}
		return self._menuItems
	@menuItems.setter
	def menuItems(self, state):
		self._setter_access_tracker["menuItems"] = {}
		self._menuItems = state

	def _to_json_fields(self):
		return {
			"menuItems": self._menuItems
			}


class VerticalMenu(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "VerticalMenu"
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
		self._custom = VerticalMenuCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}