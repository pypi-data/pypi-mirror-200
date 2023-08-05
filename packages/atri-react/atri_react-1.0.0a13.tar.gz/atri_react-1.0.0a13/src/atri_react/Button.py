from typing import Any, Union
from atri_core import AtriComponent



class ButtonCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.type: Union[Any, None] = state["type"] if state != None and "type" in state else None
		self.block: Union[Any, None] = state["block"] if state != None and "block" in state else None
		self.danger: Union[Any, None] = state["danger"] if state != None and "danger" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.icon: Union[Any, None] = state["icon"] if state != None and "icon" in state else None
		self.loading: Union[Any, None] = state["loading"] if state != None and "loading" in state else None
		self.shape: Union[Any, None] = state["shape"] if state != None and "shape" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
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
	def type(self):
		self._getter_access_tracker["type"] = {}
		return self._type
	@type.setter
	def type(self, state):
		self._setter_access_tracker["type"] = {}
		self._type = state
	@property
	def block(self):
		self._getter_access_tracker["block"] = {}
		return self._block
	@block.setter
	def block(self, state):
		self._setter_access_tracker["block"] = {}
		self._block = state
	@property
	def danger(self):
		self._getter_access_tracker["danger"] = {}
		return self._danger
	@danger.setter
	def danger(self, state):
		self._setter_access_tracker["danger"] = {}
		self._danger = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def icon(self):
		self._getter_access_tracker["icon"] = {}
		return self._icon
	@icon.setter
	def icon(self, state):
		self._setter_access_tracker["icon"] = {}
		self._icon = state
	@property
	def loading(self):
		self._getter_access_tracker["loading"] = {}
		return self._loading
	@loading.setter
	def loading(self, state):
		self._setter_access_tracker["loading"] = {}
		self._loading = state
	@property
	def shape(self):
		self._getter_access_tracker["shape"] = {}
		return self._shape
	@shape.setter
	def shape(self, state):
		self._setter_access_tracker["shape"] = {}
		self._shape = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state

	def _to_json_fields(self):
		return {
			"text": self._text,
			"type": self._type,
			"block": self._block,
			"danger": self._danger,
			"disabled": self._disabled,
			"icon": self._icon,
			"loading": self._loading,
			"shape": self._shape,
			"size": self._size
			}


class Button(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Button"
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
		self._custom = ButtonCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}