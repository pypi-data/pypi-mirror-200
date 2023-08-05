from typing import Any, Union
from atri_core import AtriComponent



class TestimonialCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.startTile: Union[Any, None] = state["startTile"] if state != None and "startTile" in state else None
		self.intervalTime: Union[Any, None] = state["intervalTime"] if state != None and "intervalTime" in state else None
		self.testimonials: Union[Any, None] = state["testimonials"] if state != None and "testimonials" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def startTile(self):
		self._getter_access_tracker["startTile"] = {}
		return self._startTile
	@startTile.setter
	def startTile(self, state):
		self._setter_access_tracker["startTile"] = {}
		self._startTile = state
	@property
	def intervalTime(self):
		self._getter_access_tracker["intervalTime"] = {}
		return self._intervalTime
	@intervalTime.setter
	def intervalTime(self, state):
		self._setter_access_tracker["intervalTime"] = {}
		self._intervalTime = state
	@property
	def testimonials(self):
		self._getter_access_tracker["testimonials"] = {}
		return self._testimonials
	@testimonials.setter
	def testimonials(self, state):
		self._setter_access_tracker["testimonials"] = {}
		self._testimonials = state

	def _to_json_fields(self):
		return {
			"startTile": self._startTile,
			"intervalTime": self._intervalTime,
			"testimonials": self._testimonials
			}


class Testimonial(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Testimonial"
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
		self._custom = TestimonialCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}