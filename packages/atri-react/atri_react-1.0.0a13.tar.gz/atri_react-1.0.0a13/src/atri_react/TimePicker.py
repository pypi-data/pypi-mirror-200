from typing import Any, Union
from atri_core import AtriComponent



class TimePickerCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.use12Hours: Union[Any, None] = state["use12Hours"] if state != None and "use12Hours" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.format: Union[Any, None] = state["format"] if state != None and "format" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.status: Union[Any, None] = state["status"] if state != None and "status" in state else None
		self.range: Union[Any, None] = state["range"] if state != None and "range" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def use12Hours(self):
		self._getter_access_tracker["use12Hours"] = {}
		return self._use12Hours
	@use12Hours.setter
	def use12Hours(self, state):
		self._setter_access_tracker["use12Hours"] = {}
		self._use12Hours = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def format(self):
		self._getter_access_tracker["format"] = {}
		return self._format
	@format.setter
	def format(self, state):
		self._setter_access_tracker["format"] = {}
		self._format = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def status(self):
		self._getter_access_tracker["status"] = {}
		return self._status
	@status.setter
	def status(self, state):
		self._setter_access_tracker["status"] = {}
		self._status = state
	@property
	def range(self):
		self._getter_access_tracker["range"] = {}
		return self._range
	@range.setter
	def range(self, state):
		self._setter_access_tracker["range"] = {}
		self._range = state

	def _to_json_fields(self):
		return {
			"use12Hours": self._use12Hours,
			"size": self._size,
			"format": self._format,
			"bordered": self._bordered,
			"disabled": self._disabled,
			"status": self._status,
			"range": self._range
			}


class TimePicker(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "TimePicker"
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
		self._custom = TimePickerCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}