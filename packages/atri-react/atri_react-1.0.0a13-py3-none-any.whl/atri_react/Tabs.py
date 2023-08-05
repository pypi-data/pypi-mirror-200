from typing import Any, Union
from atri_core import AtriComponent



class TabsCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.centered: Union[Any, None] = state["centered"] if state != None and "centered" in state else None
		self.animated: Union[Any, None] = state["animated"] if state != None and "animated" in state else None
		self.addIcon: Union[Any, None] = state["addIcon"] if state != None and "addIcon" in state else None
		self.tabPosition: Union[Any, None] = state["tabPosition"] if state != None and "tabPosition" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.type: Union[Any, None] = state["type"] if state != None and "type" in state else None
		self.activeTabColor: Union[Any, None] = state["activeTabColor"] if state != None and "activeTabColor" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def centered(self):
		self._getter_access_tracker["centered"] = {}
		return self._centered
	@centered.setter
	def centered(self, state):
		self._setter_access_tracker["centered"] = {}
		self._centered = state
	@property
	def animated(self):
		self._getter_access_tracker["animated"] = {}
		return self._animated
	@animated.setter
	def animated(self, state):
		self._setter_access_tracker["animated"] = {}
		self._animated = state
	@property
	def addIcon(self):
		self._getter_access_tracker["addIcon"] = {}
		return self._addIcon
	@addIcon.setter
	def addIcon(self, state):
		self._setter_access_tracker["addIcon"] = {}
		self._addIcon = state
	@property
	def tabPosition(self):
		self._getter_access_tracker["tabPosition"] = {}
		return self._tabPosition
	@tabPosition.setter
	def tabPosition(self, state):
		self._setter_access_tracker["tabPosition"] = {}
		self._tabPosition = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def type(self):
		self._getter_access_tracker["type"] = {}
		return self._type
	@type.setter
	def type(self, state):
		self._setter_access_tracker["type"] = {}
		self._type = state
	@property
	def activeTabColor(self):
		self._getter_access_tracker["activeTabColor"] = {}
		return self._activeTabColor
	@activeTabColor.setter
	def activeTabColor(self, state):
		self._setter_access_tracker["activeTabColor"] = {}
		self._activeTabColor = state
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
			"centered": self._centered,
			"animated": self._animated,
			"addIcon": self._addIcon,
			"tabPosition": self._tabPosition,
			"size": self._size,
			"type": self._type,
			"activeTabColor": self._activeTabColor,
			"items": self._items
			}


class Tabs(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Tabs"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onTabClick = False
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
		self._custom = TabsCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}