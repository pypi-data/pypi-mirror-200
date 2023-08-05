from typing import Any, Union
from atri_core import AtriComponent



class TextareaCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.allowClear: Union[Any, None] = state["allowClear"] if state != None and "allowClear" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.id: Union[Any, None] = state["id"] if state != None and "id" in state else None
		self.maxLength: Union[Any, None] = state["maxLength"] if state != None and "maxLength" in state else None
		self.showCount: Union[Any, None] = state["showCount"] if state != None and "showCount" in state else None
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
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def allowClear(self):
		self._getter_access_tracker["allowClear"] = {}
		return self._allowClear
	@allowClear.setter
	def allowClear(self, state):
		self._setter_access_tracker["allowClear"] = {}
		self._allowClear = state
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
	def id(self):
		self._getter_access_tracker["id"] = {}
		return self._id
	@id.setter
	def id(self, state):
		self._setter_access_tracker["id"] = {}
		self._id = state
	@property
	def maxLength(self):
		self._getter_access_tracker["maxLength"] = {}
		return self._maxLength
	@maxLength.setter
	def maxLength(self, state):
		self._setter_access_tracker["maxLength"] = {}
		self._maxLength = state
	@property
	def showCount(self):
		self._getter_access_tracker["showCount"] = {}
		return self._showCount
	@showCount.setter
	def showCount(self, state):
		self._setter_access_tracker["showCount"] = {}
		self._showCount = state

	def _to_json_fields(self):
		return {
			"defaultValue": self._defaultValue,
			"placeholder": self._placeholder,
			"value": self._value,
			"size": self._size,
			"allowClear": self._allowClear,
			"bordered": self._bordered,
			"disabled": self._disabled,
			"id": self._id,
			"maxLength": self._maxLength,
			"showCount": self._showCount
			}


class Textarea(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Textarea"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
		self.onPressEnter = False
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
		self._custom = TextareaCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}