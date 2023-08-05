from typing import Any, Union
from atri_core import AtriComponent



class OverlayCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.closeOverlayAfter: Union[Any, None] = state["closeOverlayAfter"] if state != None and "closeOverlayAfter" in state else None
		self.open: Union[Any, None] = state["open"] if state != None and "open" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def closeOverlayAfter(self):
		self._getter_access_tracker["closeOverlayAfter"] = {}
		return self._closeOverlayAfter
	@closeOverlayAfter.setter
	def closeOverlayAfter(self, state):
		self._setter_access_tracker["closeOverlayAfter"] = {}
		self._closeOverlayAfter = state
	@property
	def open(self):
		self._getter_access_tracker["open"] = {}
		return self._open
	@open.setter
	def open(self, state):
		self._setter_access_tracker["open"] = {}
		self._open = state

	def _to_json_fields(self):
		return {
			"closeOverlayAfter": self._closeOverlayAfter,
			"open": self._open
			}


class Overlay(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Overlay"
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
		self._custom = OverlayCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}