from typing import Any, Union
from atri_core import AtriComponent



class DatePickerCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.picker: Union[Any, None] = state["picker"] if state != None and "picker" in state else None
		self.showTime: Union[Any, None] = state["showTime"] if state != None and "showTime" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def picker(self):
		self._getter_access_tracker["picker"] = {}
		return self._picker
	@picker.setter
	def picker(self, state):
		self._setter_access_tracker["picker"] = {}
		self._picker = state
	@property
	def showTime(self):
		self._getter_access_tracker["showTime"] = {}
		return self._showTime
	@showTime.setter
	def showTime(self, state):
		self._setter_access_tracker["showTime"] = {}
		self._showTime = state
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
			"picker": self._picker,
			"showTime": self._showTime,
			"disabled": self._disabled
			}


class DatePicker(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "DatePicker"
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
		self._custom = DatePickerCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}