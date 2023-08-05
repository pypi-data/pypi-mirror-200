from typing import Any, Union
from atri_core import AtriComponent



class ImageCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.alt: Union[Any, None] = state["alt"] if state != None and "alt" in state else None
		self.src: Union[Any, None] = state["src"] if state != None and "src" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def alt(self):
		self._getter_access_tracker["alt"] = {}
		return self._alt
	@alt.setter
	def alt(self, state):
		self._setter_access_tracker["alt"] = {}
		self._alt = state
	@property
	def src(self):
		self._getter_access_tracker["src"] = {}
		return self._src
	@src.setter
	def src(self, state):
		self._setter_access_tracker["src"] = {}
		self._src = state

	def _to_json_fields(self):
		return {
			"alt": self._alt,
			"src": self._src
			}


class Image(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Image"
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
		self._custom = ImageCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}