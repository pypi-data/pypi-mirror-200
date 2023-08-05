from typing import Any, Union
from atri_core import AtriComponent



class DropdownCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.selectedValue: Union[Any, None] = state["selectedValue"] if state != None and "selectedValue" in state else None
		self.dropdownItems: Union[Any, None] = state["dropdownItems"] if state != None and "dropdownItems" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def selectedValue(self):
		self._getter_access_tracker["selectedValue"] = {}
		return self._selectedValue
	@selectedValue.setter
	def selectedValue(self, state):
		self._setter_access_tracker["selectedValue"] = {}
		self._selectedValue = state
	@property
	def dropdownItems(self):
		self._getter_access_tracker["dropdownItems"] = {}
		return self._dropdownItems
	@dropdownItems.setter
	def dropdownItems(self, state):
		self._setter_access_tracker["dropdownItems"] = {}
		self._dropdownItems = state

	def _to_json_fields(self):
		return {
			"selectedValue": self._selectedValue,
			"dropdownItems": self._dropdownItems
			}


class Dropdown(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Dropdown"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
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
		self._custom = DropdownCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}