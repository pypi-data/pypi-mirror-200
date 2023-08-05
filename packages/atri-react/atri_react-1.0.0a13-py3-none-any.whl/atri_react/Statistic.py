from typing import Any, Union
from atri_core import AtriComponent



class StatisticCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.title: Union[Any, None] = state["title"] if state != None and "title" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.groupSeparator: Union[Any, None] = state["groupSeparator"] if state != None and "groupSeparator" in state else None
		self.decimalSeparator: Union[Any, None] = state["decimalSeparator"] if state != None and "decimalSeparator" in state else None
		self.precision: Union[Any, None] = state["precision"] if state != None and "precision" in state else None
		self.prefix: Union[Any, None] = state["prefix"] if state != None and "prefix" in state else None
		self.prefixIcon: Union[Any, None] = state["prefixIcon"] if state != None and "prefixIcon" in state else None
		self.suffix: Union[Any, None] = state["suffix"] if state != None and "suffix" in state else None
		self.suffixIcon: Union[Any, None] = state["suffixIcon"] if state != None and "suffixIcon" in state else None
		self.loading: Union[Any, None] = state["loading"] if state != None and "loading" in state else None
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
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def groupSeparator(self):
		self._getter_access_tracker["groupSeparator"] = {}
		return self._groupSeparator
	@groupSeparator.setter
	def groupSeparator(self, state):
		self._setter_access_tracker["groupSeparator"] = {}
		self._groupSeparator = state
	@property
	def decimalSeparator(self):
		self._getter_access_tracker["decimalSeparator"] = {}
		return self._decimalSeparator
	@decimalSeparator.setter
	def decimalSeparator(self, state):
		self._setter_access_tracker["decimalSeparator"] = {}
		self._decimalSeparator = state
	@property
	def precision(self):
		self._getter_access_tracker["precision"] = {}
		return self._precision
	@precision.setter
	def precision(self, state):
		self._setter_access_tracker["precision"] = {}
		self._precision = state
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
	@property
	def loading(self):
		self._getter_access_tracker["loading"] = {}
		return self._loading
	@loading.setter
	def loading(self, state):
		self._setter_access_tracker["loading"] = {}
		self._loading = state

	def _to_json_fields(self):
		return {
			"title": self._title,
			"value": self._value,
			"groupSeparator": self._groupSeparator,
			"decimalSeparator": self._decimalSeparator,
			"precision": self._precision,
			"prefix": self._prefix,
			"prefixIcon": self._prefixIcon,
			"suffix": self._suffix,
			"suffixIcon": self._suffixIcon,
			"loading": self._loading
			}


class Statistic(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Statistic"
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
		self._custom = StatisticCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}