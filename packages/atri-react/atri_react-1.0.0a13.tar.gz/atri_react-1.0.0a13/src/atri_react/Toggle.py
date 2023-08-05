from typing import Any, Union
from atri_core import AtriComponent



class ToggleCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.active: Union[Any, None] = state["active"] if state != None and "active" in state else None
		self.activeColor: Union[Any, None] = state["activeColor"] if state != None and "activeColor" in state else None
		self.inactiveColor: Union[Any, None] = state["inactiveColor"] if state != None and "inactiveColor" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def active(self):
		self._getter_access_tracker["active"] = {}
		return self._active
	@active.setter
	def active(self, state):
		self._setter_access_tracker["active"] = {}
		self._active = state
	@property
	def activeColor(self):
		self._getter_access_tracker["activeColor"] = {}
		return self._activeColor
	@activeColor.setter
	def activeColor(self, state):
		self._setter_access_tracker["activeColor"] = {}
		self._activeColor = state
	@property
	def inactiveColor(self):
		self._getter_access_tracker["inactiveColor"] = {}
		return self._inactiveColor
	@inactiveColor.setter
	def inactiveColor(self, state):
		self._setter_access_tracker["inactiveColor"] = {}
		self._inactiveColor = state

	def _to_json_fields(self):
		return {
			"active": self._active,
			"activeColor": self._activeColor,
			"inactiveColor": self._inactiveColor
			}


class Toggle(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Toggle"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
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
		self._custom = ToggleCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}