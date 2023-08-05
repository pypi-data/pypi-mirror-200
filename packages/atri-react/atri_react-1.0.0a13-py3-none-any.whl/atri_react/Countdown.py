from typing import Any, Union
from atri_core import AtriComponent



class CountdownCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.title: Union[Any, None] = state["title"] if state != None and "title" in state else None
		self.format: Union[Any, None] = state["format"] if state != None and "format" in state else None
		self.inputType: Union[Any, None] = state["inputType"] if state != None and "inputType" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.prefix: Union[Any, None] = state["prefix"] if state != None and "prefix" in state else None
		self.prefixIcon: Union[Any, None] = state["prefixIcon"] if state != None and "prefixIcon" in state else None
		self.suffix: Union[Any, None] = state["suffix"] if state != None and "suffix" in state else None
		self.suffixIcon: Union[Any, None] = state["suffixIcon"] if state != None and "suffixIcon" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def title(self):
		self._getter_access_tracker["title"] = {}
		return self._title
	@title.setter
	def title(self, state):
		self._setter_access_tracker["title"] = {}
		self._title = state
	@property
	def format(self):
		self._getter_access_tracker["format"] = {}
		return self._format
	@format.setter
	def format(self, state):
		self._setter_access_tracker["format"] = {}
		self._format = state
	@property
	def inputType(self):
		self._getter_access_tracker["inputType"] = {}
		return self._inputType
	@inputType.setter
	def inputType(self, state):
		self._setter_access_tracker["inputType"] = {}
		self._inputType = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def prefix(self):
		self._getter_access_tracker["prefix"] = {}
		return self._prefix
	@prefix.setter
	def prefix(self, state):
		self._setter_access_tracker["prefix"] = {}
		self._prefix = state
	@property
	def prefixIcon(self):
		self._getter_access_tracker["prefixIcon"] = {}
		return self._prefixIcon
	@prefixIcon.setter
	def prefixIcon(self, state):
		self._setter_access_tracker["prefixIcon"] = {}
		self._prefixIcon = state
	@property
	def suffix(self):
		self._getter_access_tracker["suffix"] = {}
		return self._suffix
	@suffix.setter
	def suffix(self, state):
		self._setter_access_tracker["suffix"] = {}
		self._suffix = state
	@property
	def suffixIcon(self):
		self._getter_access_tracker["suffixIcon"] = {}
		return self._suffixIcon
	@suffixIcon.setter
	def suffixIcon(self, state):
		self._setter_access_tracker["suffixIcon"] = {}
		self._suffixIcon = state

	def _to_json_fields(self):
		return {
			"title": self._title,
			"format": self._format,
			"inputType": self._inputType,
			"value": self._value,
			"prefix": self._prefix,
			"prefixIcon": self._prefixIcon,
			"suffix": self._suffix,
			"suffixIcon": self._suffixIcon
			}


class Countdown(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Countdown"
		self.nodePkg = "@atrilabs/react-component-manifests"
		
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
		self._custom = CountdownCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}