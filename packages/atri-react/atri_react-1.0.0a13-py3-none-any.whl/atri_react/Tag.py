from typing import Any, Union
from atri_core import AtriComponent



class TagCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.closable: Union[Any, None] = state["closable"] if state != None and "closable" in state else None
		self.link: Union[Any, None] = state["link"] if state != None and "link" in state else None
		self.color: Union[Any, None] = state["color"] if state != None and "color" in state else None
		self.variant: Union[Any, None] = state["variant"] if state != None and "variant" in state else None
		self.icon: Union[Any, None] = state["icon"] if state != None and "icon" in state else None
		self.iconVariant: Union[Any, None] = state["iconVariant"] if state != None and "iconVariant" in state else None
		self.closeIcon: Union[Any, None] = state["closeIcon"] if state != None and "closeIcon" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def text(self):
		self._getter_access_tracker["text"] = {}
		return self._text
	@text.setter
	def text(self, state):
		self._setter_access_tracker["text"] = {}
		self._text = state
	@property
	def closable(self):
		self._getter_access_tracker["closable"] = {}
		return self._closable
	@closable.setter
	def closable(self, state):
		self._setter_access_tracker["closable"] = {}
		self._closable = state
	@property
	def link(self):
		self._getter_access_tracker["link"] = {}
		return self._link
	@link.setter
	def link(self, state):
		self._setter_access_tracker["link"] = {}
		self._link = state
	@property
	def color(self):
		self._getter_access_tracker["color"] = {}
		return self._color
	@color.setter
	def color(self, state):
		self._setter_access_tracker["color"] = {}
		self._color = state
	@property
	def variant(self):
		self._getter_access_tracker["variant"] = {}
		return self._variant
	@variant.setter
	def variant(self, state):
		self._setter_access_tracker["variant"] = {}
		self._variant = state
	@property
	def icon(self):
		self._getter_access_tracker["icon"] = {}
		return self._icon
	@icon.setter
	def icon(self, state):
		self._setter_access_tracker["icon"] = {}
		self._icon = state
	@property
	def iconVariant(self):
		self._getter_access_tracker["iconVariant"] = {}
		return self._iconVariant
	@iconVariant.setter
	def iconVariant(self, state):
		self._setter_access_tracker["iconVariant"] = {}
		self._iconVariant = state
	@property
	def closeIcon(self):
		self._getter_access_tracker["closeIcon"] = {}
		return self._closeIcon
	@closeIcon.setter
	def closeIcon(self, state):
		self._setter_access_tracker["closeIcon"] = {}
		self._closeIcon = state

	def _to_json_fields(self):
		return {
			"text": self._text,
			"closable": self._closable,
			"link": self._link,
			"color": self._color,
			"variant": self._variant,
			"icon": self._icon,
			"iconVariant": self._iconVariant,
			"closeIcon": self._closeIcon
			}


class Tag(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Tag"
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
		self._custom = TagCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}