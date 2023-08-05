from typing import Any, Union
from atri_core import AtriComponent



class InputNumberCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.max: Union[Any, None] = state["max"] if state != None and "max" in state else None
		self.min: Union[Any, None] = state["min"] if state != None and "min" in state else None
		self.step: Union[Any, None] = state["step"] if state != None and "step" in state else None
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.status: Union[Any, None] = state["status"] if state != None and "status" in state else None
		self.addonAfter: Union[Any, None] = state["addonAfter"] if state != None and "addonAfter" in state else None
		self.addonBefore: Union[Any, None] = state["addonBefore"] if state != None and "addonBefore" in state else None
		self.prefix: Union[Any, None] = state["prefix"] if state != None and "prefix" in state else None
		self.suffix: Union[Any, None] = state["suffix"] if state != None and "suffix" in state else None
		self.keyboard: Union[Any, None] = state["keyboard"] if state != None and "keyboard" in state else None
		self.readOnly: Union[Any, None] = state["readOnly"] if state != None and "readOnly" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def defaultValue(self):
		self._getter_access_tracker["defaultValue"] = {}
		return self._defaultValue
	@defaultValue.setter
	def defaultValue(self, state):
		self._setter_access_tracker["defaultValue"] = {}
		self._defaultValue = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def max(self):
		self._getter_access_tracker["max"] = {}
		return self._max
	@max.setter
	def max(self, state):
		self._setter_access_tracker["max"] = {}
		self._max = state
	@property
	def min(self):
		self._getter_access_tracker["min"] = {}
		return self._min
	@min.setter
	def min(self, state):
		self._setter_access_tracker["min"] = {}
		self._min = state
	@property
	def step(self):
		self._getter_access_tracker["step"] = {}
		return self._step
	@step.setter
	def step(self, state):
		self._setter_access_tracker["step"] = {}
		self._step = state
	@property
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
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
	def addonAfter(self):
		self._getter_access_tracker["addonAfter"] = {}
		return self._addonAfter
	@addonAfter.setter
	def addonAfter(self, state):
		self._setter_access_tracker["addonAfter"] = {}
		self._addonAfter = state
	@property
	def addonBefore(self):
		self._getter_access_tracker["addonBefore"] = {}
		return self._addonBefore
	@addonBefore.setter
	def addonBefore(self, state):
		self._setter_access_tracker["addonBefore"] = {}
		self._addonBefore = state
	@property
	def prefix(self):
		self._getter_access_tracker["prefix"] = {}
		return self._prefix
	@prefix.setter
	def prefix(self, state):
		self._setter_access_tracker["prefix"] = {}
		self._prefix = state
	@property
	def suffix(self):
		self._getter_access_tracker["suffix"] = {}
		return self._suffix
	@suffix.setter
	def suffix(self, state):
		self._setter_access_tracker["suffix"] = {}
		self._suffix = state
	@property
	def keyboard(self):
		self._getter_access_tracker["keyboard"] = {}
		return self._keyboard
	@keyboard.setter
	def keyboard(self, state):
		self._setter_access_tracker["keyboard"] = {}
		self._keyboard = state
	@property
	def readOnly(self):
		self._getter_access_tracker["readOnly"] = {}
		return self._readOnly
	@readOnly.setter
	def readOnly(self, state):
		self._setter_access_tracker["readOnly"] = {}
		self._readOnly = state

	def _to_json_fields(self):
		return {
			"defaultValue": self._defaultValue,
			"value": self._value,
			"max": self._max,
			"min": self._min,
			"step": self._step,
			"placeholder": self._placeholder,
			"size": self._size,
			"bordered": self._bordered,
			"disabled": self._disabled,
			"status": self._status,
			"addonAfter": self._addonAfter,
			"addonBefore": self._addonBefore,
			"prefix": self._prefix,
			"suffix": self._suffix,
			"keyboard": self._keyboard,
			"readOnly": self._readOnly
			}


class InputNumber(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "InputNumber"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
		self.onPressEnter = False
		self.onStep = False
		self.parser = False
		self.formatter = False
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
		self._custom = InputNumberCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}