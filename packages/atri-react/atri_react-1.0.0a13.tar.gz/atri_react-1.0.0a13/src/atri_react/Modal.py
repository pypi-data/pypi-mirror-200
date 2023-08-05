from typing import Any, Union
from atri_core import AtriComponent



class ModalCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.content: Union[Any, None] = state["content"] if state != None and "content" in state else None
		self.cancelText: Union[Any, None] = state["cancelText"] if state != None and "cancelText" in state else None
		self.okText: Union[Any, None] = state["okText"] if state != None and "okText" in state else None
		self.centered: Union[Any, None] = state["centered"] if state != None and "centered" in state else None
		self.icon: Union[Any, None] = state["icon"] if state != None and "icon" in state else None
		self.closable: Union[Any, None] = state["closable"] if state != None and "closable" in state else None
		self.closeIcon: Union[Any, None] = state["closeIcon"] if state != None and "closeIcon" in state else None
		self.destroyOnClose: Union[Any, None] = state["destroyOnClose"] if state != None and "destroyOnClose" in state else None
		self.keyboard: Union[Any, None] = state["keyboard"] if state != None and "keyboard" in state else None
		self.mask: Union[Any, None] = state["mask"] if state != None and "mask" in state else None
		self.maskClosable: Union[Any, None] = state["maskClosable"] if state != None and "maskClosable" in state else None
		self.zIndex: Union[Any, None] = state["zIndex"] if state != None and "zIndex" in state else None
		self.open: Union[Any, None] = state["open"] if state != None and "open" in state else None
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
	def content(self):
		self._getter_access_tracker["content"] = {}
		return self._content
	@content.setter
	def content(self, state):
		self._setter_access_tracker["content"] = {}
		self._content = state
	@property
	def cancelText(self):
		self._getter_access_tracker["cancelText"] = {}
		return self._cancelText
	@cancelText.setter
	def cancelText(self, state):
		self._setter_access_tracker["cancelText"] = {}
		self._cancelText = state
	@property
	def okText(self):
		self._getter_access_tracker["okText"] = {}
		return self._okText
	@okText.setter
	def okText(self, state):
		self._setter_access_tracker["okText"] = {}
		self._okText = state
	@property
	def centered(self):
		self._getter_access_tracker["centered"] = {}
		return self._centered
	@centered.setter
	def centered(self, state):
		self._setter_access_tracker["centered"] = {}
		self._centered = state
	@property
	def icon(self):
		self._getter_access_tracker["icon"] = {}
		return self._icon
	@icon.setter
	def icon(self, state):
		self._setter_access_tracker["icon"] = {}
		self._icon = state
	@property
	def closable(self):
		self._getter_access_tracker["closable"] = {}
		return self._closable
	@closable.setter
	def closable(self, state):
		self._setter_access_tracker["closable"] = {}
		self._closable = state
	@property
	def closeIcon(self):
		self._getter_access_tracker["closeIcon"] = {}
		return self._closeIcon
	@closeIcon.setter
	def closeIcon(self, state):
		self._setter_access_tracker["closeIcon"] = {}
		self._closeIcon = state
	@property
	def destroyOnClose(self):
		self._getter_access_tracker["destroyOnClose"] = {}
		return self._destroyOnClose
	@destroyOnClose.setter
	def destroyOnClose(self, state):
		self._setter_access_tracker["destroyOnClose"] = {}
		self._destroyOnClose = state
	@property
	def keyboard(self):
		self._getter_access_tracker["keyboard"] = {}
		return self._keyboard
	@keyboard.setter
	def keyboard(self, state):
		self._setter_access_tracker["keyboard"] = {}
		self._keyboard = state
	@property
	def mask(self):
		self._getter_access_tracker["mask"] = {}
		return self._mask
	@mask.setter
	def mask(self, state):
		self._setter_access_tracker["mask"] = {}
		self._mask = state
	@property
	def maskClosable(self):
		self._getter_access_tracker["maskClosable"] = {}
		return self._maskClosable
	@maskClosable.setter
	def maskClosable(self, state):
		self._setter_access_tracker["maskClosable"] = {}
		self._maskClosable = state
	@property
	def zIndex(self):
		self._getter_access_tracker["zIndex"] = {}
		return self._zIndex
	@zIndex.setter
	def zIndex(self, state):
		self._setter_access_tracker["zIndex"] = {}
		self._zIndex = state
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
			"text": self._text,
			"content": self._content,
			"cancelText": self._cancelText,
			"okText": self._okText,
			"centered": self._centered,
			"icon": self._icon,
			"closable": self._closable,
			"closeIcon": self._closeIcon,
			"destroyOnClose": self._destroyOnClose,
			"keyboard": self._keyboard,
			"mask": self._mask,
			"maskClosable": self._maskClosable,
			"zIndex": self._zIndex,
			"open": self._open
			}


class Modal(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Modal"
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
		self._custom = ModalCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}