from typing import Any, Union
from atri_core import AtriComponent



class RadioCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.name: Union[Any, None] = state["name"] if state != None and "name" in state else None
		self.label: Union[Any, None] = state["label"] if state != None and "label" in state else None
		self.checked: Union[Any, None] = state["checked"] if state != None and "checked" in state else None
		self.radius: Union[Any, None] = state["radius"] if state != None and "radius" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def name(self):
		self._getter_access_tracker["name"] = {}
		return self._name
	@name.setter
	def name(self, state):
		self._setter_access_tracker["name"] = {}
		self._name = state
	@property
	def label(self):
		self._getter_access_tracker["label"] = {}
		return self._label
	@label.setter
	def label(self, state):
		self._setter_access_tracker["label"] = {}
		self._label = state
	@property
	def checked(self):
		self._getter_access_tracker["checked"] = {}
		return self._checked
	@checked.setter
	def checked(self, state):
		self._setter_access_tracker["checked"] = {}
		self._checked = state
	@property
	def radius(self):
		self._getter_access_tracker["radius"] = {}
		return self._radius
	@radius.setter
	def radius(self, state):
		self._setter_access_tracker["radius"] = {}
		self._radius = state

	def _to_json_fields(self):
		return {
			"name": self._name,
			"label": self._label,
			"checked": self._checked,
			"radius": self._radius
			}


class Radio(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Radio"
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
		self._custom = RadioCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}