from typing import Any, Union
from atri_core import AtriComponent



class CountupCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.itemCount: Union[Any, None] = state["itemCount"] if state != None and "itemCount" in state else None
		self.duration: Union[Any, None] = state["duration"] if state != None and "duration" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def itemCount(self):
		self._getter_access_tracker["itemCount"] = {}
		return self._itemCount
	@itemCount.setter
	def itemCount(self, state):
		self._setter_access_tracker["itemCount"] = {}
		self._itemCount = state
	@property
	def duration(self):
		self._getter_access_tracker["duration"] = {}
		return self._duration
	@duration.setter
	def duration(self, state):
		self._setter_access_tracker["duration"] = {}
		self._duration = state

	def _to_json_fields(self):
		return {
			"itemCount": self._itemCount,
			"duration": self._duration
			}


class Countup(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Countup"
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
		self._custom = CountupCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}