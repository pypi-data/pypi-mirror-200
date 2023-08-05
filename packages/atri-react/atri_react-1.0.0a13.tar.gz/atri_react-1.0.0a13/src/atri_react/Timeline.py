from typing import Any, Union
from atri_core import AtriComponent



class TimelineCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self.mode: Union[Any, None] = state["mode"] if state != None and "mode" in state else None
		self.pending: Union[Any, None] = state["pending"] if state != None and "pending" in state else None
		self.pendingDot: Union[Any, None] = state["pendingDot"] if state != None and "pendingDot" in state else None
		self.reverse: Union[Any, None] = state["reverse"] if state != None and "reverse" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def items(self):
		self._getter_access_tracker["items"] = {}
		return self._items
	@items.setter
	def items(self, state):
		self._setter_access_tracker["items"] = {}
		self._items = state
	@property
	def mode(self):
		self._getter_access_tracker["mode"] = {}
		return self._mode
	@mode.setter
	def mode(self, state):
		self._setter_access_tracker["mode"] = {}
		self._mode = state
	@property
	def pending(self):
		self._getter_access_tracker["pending"] = {}
		return self._pending
	@pending.setter
	def pending(self, state):
		self._setter_access_tracker["pending"] = {}
		self._pending = state
	@property
	def pendingDot(self):
		self._getter_access_tracker["pendingDot"] = {}
		return self._pendingDot
	@pendingDot.setter
	def pendingDot(self, state):
		self._setter_access_tracker["pendingDot"] = {}
		self._pendingDot = state
	@property
	def reverse(self):
		self._getter_access_tracker["reverse"] = {}
		return self._reverse
	@reverse.setter
	def reverse(self, state):
		self._setter_access_tracker["reverse"] = {}
		self._reverse = state

	def _to_json_fields(self):
		return {
			"items": self._items,
			"mode": self._mode,
			"pending": self._pending,
			"pendingDot": self._pendingDot,
			"reverse": self._reverse
			}


class Timeline(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Timeline"
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
		self._custom = TimelineCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}