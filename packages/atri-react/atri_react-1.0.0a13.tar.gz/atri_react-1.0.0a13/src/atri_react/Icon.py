from typing import Any, Union
from atri_core import AtriComponent



class IconCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.svg: Union[Any, None] = state["svg"] if state != None and "svg" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def svg(self):
		self._getter_access_tracker["svg"] = {}
		return self._svg
	@svg.setter
	def svg(self, state):
		self._setter_access_tracker["svg"] = {}
		self._svg = state

	def _to_json_fields(self):
		return {
			"svg": self._svg
			}


class Icon(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Icon"
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
		self._custom = IconCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}