from typing import Any, Union
from atri_core import AtriComponent



class CardCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.type: Union[Any, None] = state["type"] if state != None and "type" in state else None
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.description: Union[Any, None] = state["description"] if state != None and "description" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.hoverable: Union[Any, None] = state["hoverable"] if state != None and "hoverable" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.cover: Union[Any, None] = state["cover"] if state != None and "cover" in state else None
		self.avatar: Union[Any, None] = state["avatar"] if state != None and "avatar" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def type(self):
		self._getter_access_tracker["type"] = {}
		return self._type
	@type.setter
	def type(self, state):
		self._setter_access_tracker["type"] = {}
		self._type = state
	@property
	def text(self):
		self._getter_access_tracker["text"] = {}
		return self._text
	@text.setter
	def text(self, state):
		self._setter_access_tracker["text"] = {}
		self._text = state
	@property
	def description(self):
		self._getter_access_tracker["description"] = {}
		return self._description
	@description.setter
	def description(self, state):
		self._setter_access_tracker["description"] = {}
		self._description = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def hoverable(self):
		self._getter_access_tracker["hoverable"] = {}
		return self._hoverable
	@hoverable.setter
	def hoverable(self, state):
		self._setter_access_tracker["hoverable"] = {}
		self._hoverable = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def cover(self):
		self._getter_access_tracker["cover"] = {}
		return self._cover
	@cover.setter
	def cover(self, state):
		self._setter_access_tracker["cover"] = {}
		self._cover = state
	@property
	def avatar(self):
		self._getter_access_tracker["avatar"] = {}
		return self._avatar
	@avatar.setter
	def avatar(self, state):
		self._setter_access_tracker["avatar"] = {}
		self._avatar = state

	def _to_json_fields(self):
		return {
			"type": self._type,
			"text": self._text,
			"description": self._description,
			"size": self._size,
			"hoverable": self._hoverable,
			"bordered": self._bordered,
			"cover": self._cover,
			"avatar": self._avatar
			}


class Card(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Card"
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
		self._custom = CardCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}