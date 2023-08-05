from typing import Any, Union
from atri_core import AtriComponent



class CarouselCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.autoplay: Union[Any, None] = state["autoplay"] if state != None and "autoplay" in state else None
		self.dots: Union[Any, None] = state["dots"] if state != None and "dots" in state else None
		self.dotPosition: Union[Any, None] = state["dotPosition"] if state != None and "dotPosition" in state else None
		self.effect: Union[Any, None] = state["effect"] if state != None and "effect" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def autoplay(self):
		self._getter_access_tracker["autoplay"] = {}
		return self._autoplay
	@autoplay.setter
	def autoplay(self, state):
		self._setter_access_tracker["autoplay"] = {}
		self._autoplay = state
	@property
	def dots(self):
		self._getter_access_tracker["dots"] = {}
		return self._dots
	@dots.setter
	def dots(self, state):
		self._setter_access_tracker["dots"] = {}
		self._dots = state
	@property
	def dotPosition(self):
		self._getter_access_tracker["dotPosition"] = {}
		return self._dotPosition
	@dotPosition.setter
	def dotPosition(self, state):
		self._setter_access_tracker["dotPosition"] = {}
		self._dotPosition = state
	@property
	def effect(self):
		self._getter_access_tracker["effect"] = {}
		return self._effect
	@effect.setter
	def effect(self, state):
		self._setter_access_tracker["effect"] = {}
		self._effect = state
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
			"autoplay": self._autoplay,
			"dots": self._dots,
			"dotPosition": self._dotPosition,
			"effect": self._effect,
			"items": self._items
			}


class Carousel(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Carousel"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onClick = False
		self.beforeChange = False
		self.afterChange = False
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
		self._custom = CarouselCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}