from typing import Any, Union
from atri_core import AtriComponent



class RatingCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.allowHalf: Union[Any, None] = state["allowHalf"] if state != None and "allowHalf" in state else None
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.allowClear: Union[Any, None] = state["allowClear"] if state != None and "allowClear" in state else None
		self.character: Union[Any, None] = state["character"] if state != None and "character" in state else None
		self.toolTipInfo: Union[Any, None] = state["toolTipInfo"] if state != None and "toolTipInfo" in state else None
		self.count: Union[Any, None] = state["count"] if state != None and "count" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def allowHalf(self):
		self._getter_access_tracker["allowHalf"] = {}
		return self._allowHalf
	@allowHalf.setter
	def allowHalf(self, state):
		self._setter_access_tracker["allowHalf"] = {}
		self._allowHalf = state
	@property
	def defaultValue(self):
		self._getter_access_tracker["defaultValue"] = {}
		return self._defaultValue
	@defaultValue.setter
	def defaultValue(self, state):
		self._setter_access_tracker["defaultValue"] = {}
		self._defaultValue = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def allowClear(self):
		self._getter_access_tracker["allowClear"] = {}
		return self._allowClear
	@allowClear.setter
	def allowClear(self, state):
		self._setter_access_tracker["allowClear"] = {}
		self._allowClear = state
	@property
	def character(self):
		self._getter_access_tracker["character"] = {}
		return self._character
	@character.setter
	def character(self, state):
		self._setter_access_tracker["character"] = {}
		self._character = state
	@property
	def toolTipInfo(self):
		self._getter_access_tracker["toolTipInfo"] = {}
		return self._toolTipInfo
	@toolTipInfo.setter
	def toolTipInfo(self, state):
		self._setter_access_tracker["toolTipInfo"] = {}
		self._toolTipInfo = state
	@property
	def count(self):
		self._getter_access_tracker["count"] = {}
		return self._count
	@count.setter
	def count(self, state):
		self._setter_access_tracker["count"] = {}
		self._count = state

	def _to_json_fields(self):
		return {
			"allowHalf": self._allowHalf,
			"defaultValue": self._defaultValue,
			"disabled": self._disabled,
			"allowClear": self._allowClear,
			"character": self._character,
			"toolTipInfo": self._toolTipInfo,
			"count": self._count
			}


class Rating(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Rating"
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
		self._custom = RatingCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}