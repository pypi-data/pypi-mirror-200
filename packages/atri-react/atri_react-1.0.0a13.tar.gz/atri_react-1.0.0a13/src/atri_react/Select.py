from typing import Any, Union
from atri_core import AtriComponent



class SelectCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.options: Union[Any, None] = state["options"] if state != None and "options" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def defaultValue(self):
		self._getter_access_tracker["defaultValue"] = {}
		return self._defaultValue
	@defaultValue.setter
	def defaultValue(self, state):
		self._setter_access_tracker["defaultValue"] = {}
		self._defaultValue = state
	@property
	def options(self):
		self._getter_access_tracker["options"] = {}
		return self._options
	@options.setter
	def options(self, state):
		self._setter_access_tracker["options"] = {}
		self._options = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state

	def _to_json_fields(self):
		return {
			"placeholder": self._placeholder,
			"defaultValue": self._defaultValue,
			"options": self._options,
			"disabled": self._disabled
			}


class Select(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Select"
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
		self._custom = SelectCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}