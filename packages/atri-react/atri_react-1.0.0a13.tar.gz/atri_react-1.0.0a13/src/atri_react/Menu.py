from typing import Any, Union
from atri_core import AtriComponent



class MenuCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.mode: Union[Any, None] = state["mode"] if state != None and "mode" in state else None
		self.theme: Union[Any, None] = state["theme"] if state != None and "theme" in state else None
		self.multiple: Union[Any, None] = state["multiple"] if state != None and "multiple" in state else None
		self.selectable: Union[Any, None] = state["selectable"] if state != None and "selectable" in state else None
		self.selectedKeys: Union[Any, None] = state["selectedKeys"] if state != None and "selectedKeys" in state else None
		self.defaultOpenKeys: Union[Any, None] = state["defaultOpenKeys"] if state != None and "defaultOpenKeys" in state else None
		self.defaultSelectedKeys: Union[Any, None] = state["defaultSelectedKeys"] if state != None and "defaultSelectedKeys" in state else None
		self.expandIcon: Union[Any, None] = state["expandIcon"] if state != None and "expandIcon" in state else None
		self.openKeys: Union[Any, None] = state["openKeys"] if state != None and "openKeys" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def mode(self):
		self._getter_access_tracker["mode"] = {}
		return self._mode
	@mode.setter
	def mode(self, state):
		self._setter_access_tracker["mode"] = {}
		self._mode = state
	@property
	def theme(self):
		self._getter_access_tracker["theme"] = {}
		return self._theme
	@theme.setter
	def theme(self, state):
		self._setter_access_tracker["theme"] = {}
		self._theme = state
	@property
	def multiple(self):
		self._getter_access_tracker["multiple"] = {}
		return self._multiple
	@multiple.setter
	def multiple(self, state):
		self._setter_access_tracker["multiple"] = {}
		self._multiple = state
	@property
	def selectable(self):
		self._getter_access_tracker["selectable"] = {}
		return self._selectable
	@selectable.setter
	def selectable(self, state):
		self._setter_access_tracker["selectable"] = {}
		self._selectable = state
	@property
	def selectedKeys(self):
		self._getter_access_tracker["selectedKeys"] = {}
		return self._selectedKeys
	@selectedKeys.setter
	def selectedKeys(self, state):
		self._setter_access_tracker["selectedKeys"] = {}
		self._selectedKeys = state
	@property
	def defaultOpenKeys(self):
		self._getter_access_tracker["defaultOpenKeys"] = {}
		return self._defaultOpenKeys
	@defaultOpenKeys.setter
	def defaultOpenKeys(self, state):
		self._setter_access_tracker["defaultOpenKeys"] = {}
		self._defaultOpenKeys = state
	@property
	def defaultSelectedKeys(self):
		self._getter_access_tracker["defaultSelectedKeys"] = {}
		return self._defaultSelectedKeys
	@defaultSelectedKeys.setter
	def defaultSelectedKeys(self, state):
		self._setter_access_tracker["defaultSelectedKeys"] = {}
		self._defaultSelectedKeys = state
	@property
	def expandIcon(self):
		self._getter_access_tracker["expandIcon"] = {}
		return self._expandIcon
	@expandIcon.setter
	def expandIcon(self, state):
		self._setter_access_tracker["expandIcon"] = {}
		self._expandIcon = state
	@property
	def openKeys(self):
		self._getter_access_tracker["openKeys"] = {}
		return self._openKeys
	@openKeys.setter
	def openKeys(self, state):
		self._setter_access_tracker["openKeys"] = {}
		self._openKeys = state
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
			"mode": self._mode,
			"theme": self._theme,
			"multiple": self._multiple,
			"selectable": self._selectable,
			"selectedKeys": self._selectedKeys,
			"defaultOpenKeys": self._defaultOpenKeys,
			"defaultSelectedKeys": self._defaultSelectedKeys,
			"expandIcon": self._expandIcon,
			"openKeys": self._openKeys,
			"items": self._items
			}


class Menu(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Menu"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
		self.onOpenChange = False
		self.onSelect = False
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
		self._custom = MenuCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}