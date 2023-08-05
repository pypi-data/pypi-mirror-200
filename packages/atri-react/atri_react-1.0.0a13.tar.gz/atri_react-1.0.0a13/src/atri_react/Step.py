from typing import Any, Union
from atri_core import AtriComponent



class StepCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.current: Union[Any, None] = state["current"] if state != None and "current" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.direction: Union[Any, None] = state["direction"] if state != None and "direction" in state else None
		self.dotStyle: Union[Any, None] = state["dotStyle"] if state != None and "dotStyle" in state else None
		self.clickable: Union[Any, None] = state["clickable"] if state != None and "clickable" in state else None
		self.type: Union[Any, None] = state["type"] if state != None and "type" in state else None
		self.percent: Union[Any, None] = state["percent"] if state != None and "percent" in state else None
		self.labelPlacement: Union[Any, None] = state["labelPlacement"] if state != None and "labelPlacement" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def current(self):
		self._getter_access_tracker["current"] = {}
		return self._current
	@current.setter
	def current(self, state):
		self._setter_access_tracker["current"] = {}
		self._current = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def direction(self):
		self._getter_access_tracker["direction"] = {}
		return self._direction
	@direction.setter
	def direction(self, state):
		self._setter_access_tracker["direction"] = {}
		self._direction = state
	@property
	def dotStyle(self):
		self._getter_access_tracker["dotStyle"] = {}
		return self._dotStyle
	@dotStyle.setter
	def dotStyle(self, state):
		self._setter_access_tracker["dotStyle"] = {}
		self._dotStyle = state
	@property
	def clickable(self):
		self._getter_access_tracker["clickable"] = {}
		return self._clickable
	@clickable.setter
	def clickable(self, state):
		self._setter_access_tracker["clickable"] = {}
		self._clickable = state
	@property
	def type(self):
		self._getter_access_tracker["type"] = {}
		return self._type
	@type.setter
	def type(self, state):
		self._setter_access_tracker["type"] = {}
		self._type = state
	@property
	def percent(self):
		self._getter_access_tracker["percent"] = {}
		return self._percent
	@percent.setter
	def percent(self, state):
		self._setter_access_tracker["percent"] = {}
		self._percent = state
	@property
	def labelPlacement(self):
		self._getter_access_tracker["labelPlacement"] = {}
		return self._labelPlacement
	@labelPlacement.setter
	def labelPlacement(self, state):
		self._setter_access_tracker["labelPlacement"] = {}
		self._labelPlacement = state
	@property
	def items(self):
		self._getter_access_tracker["items"] = {}
		return self._items
	@items.setter
	def items(self, state):
		self._setter_access_tracker["items"] = {}
		self._items = state

	def _to_json_fields(self):
		return {
			"current": self._current,
			"size": self._size,
			"direction": self._direction,
			"dotStyle": self._dotStyle,
			"clickable": self._clickable,
			"type": self._type,
			"percent": self._percent,
			"labelPlacement": self._labelPlacement,
			"items": self._items
			}


class Step(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Step"
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
		self._custom = StepCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}