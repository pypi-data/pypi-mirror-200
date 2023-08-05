from typing import Any, Union
from atri_core import AtriComponent



class BadgeCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.title: Union[Any, None] = state["title"] if state != None and "title" in state else None
		self.status: Union[Any, None] = state["status"] if state != None and "status" in state else None
		self.color: Union[Any, None] = state["color"] if state != None and "color" in state else None
		self.dot: Union[Any, None] = state["dot"] if state != None and "dot" in state else None
		self.count: Union[Any, None] = state["count"] if state != None and "count" in state else None
		self.countIcon: Union[Any, None] = state["countIcon"] if state != None and "countIcon" in state else None
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.showZero: Union[Any, None] = state["showZero"] if state != None and "showZero" in state else None
		self.overflowCount: Union[Any, None] = state["overflowCount"] if state != None and "overflowCount" in state else None
		self.ribbon: Union[Any, None] = state["ribbon"] if state != None and "ribbon" in state else None
		self.ribbonText: Union[Any, None] = state["ribbonText"] if state != None and "ribbonText" in state else None
		self.ribbonPlacement: Union[Any, None] = state["ribbonPlacement"] if state != None and "ribbonPlacement" in state else None
		self.ribbonColor: Union[Any, None] = state["ribbonColor"] if state != None and "ribbonColor" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def title(self):
		self._getter_access_tracker["title"] = {}
		return self._title
	@title.setter
	def title(self, state):
		self._setter_access_tracker["title"] = {}
		self._title = state
	@property
	def status(self):
		self._getter_access_tracker["status"] = {}
		return self._status
	@status.setter
	def status(self, state):
		self._setter_access_tracker["status"] = {}
		self._status = state
	@property
	def color(self):
		self._getter_access_tracker["color"] = {}
		return self._color
	@color.setter
	def color(self, state):
		self._setter_access_tracker["color"] = {}
		self._color = state
	@property
	def dot(self):
		self._getter_access_tracker["dot"] = {}
		return self._dot
	@dot.setter
	def dot(self, state):
		self._setter_access_tracker["dot"] = {}
		self._dot = state
	@property
	def count(self):
		self._getter_access_tracker["count"] = {}
		return self._count
	@count.setter
	def count(self, state):
		self._setter_access_tracker["count"] = {}
		self._count = state
	@property
	def countIcon(self):
		self._getter_access_tracker["countIcon"] = {}
		return self._countIcon
	@countIcon.setter
	def countIcon(self, state):
		self._setter_access_tracker["countIcon"] = {}
		self._countIcon = state
	@property
	def text(self):
		self._getter_access_tracker["text"] = {}
		return self._text
	@text.setter
	def text(self, state):
		self._setter_access_tracker["text"] = {}
		self._text = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def showZero(self):
		self._getter_access_tracker["showZero"] = {}
		return self._showZero
	@showZero.setter
	def showZero(self, state):
		self._setter_access_tracker["showZero"] = {}
		self._showZero = state
	@property
	def overflowCount(self):
		self._getter_access_tracker["overflowCount"] = {}
		return self._overflowCount
	@overflowCount.setter
	def overflowCount(self, state):
		self._setter_access_tracker["overflowCount"] = {}
		self._overflowCount = state
	@property
	def ribbon(self):
		self._getter_access_tracker["ribbon"] = {}
		return self._ribbon
	@ribbon.setter
	def ribbon(self, state):
		self._setter_access_tracker["ribbon"] = {}
		self._ribbon = state
	@property
	def ribbonText(self):
		self._getter_access_tracker["ribbonText"] = {}
		return self._ribbonText
	@ribbonText.setter
	def ribbonText(self, state):
		self._setter_access_tracker["ribbonText"] = {}
		self._ribbonText = state
	@property
	def ribbonPlacement(self):
		self._getter_access_tracker["ribbonPlacement"] = {}
		return self._ribbonPlacement
	@ribbonPlacement.setter
	def ribbonPlacement(self, state):
		self._setter_access_tracker["ribbonPlacement"] = {}
		self._ribbonPlacement = state
	@property
	def ribbonColor(self):
		self._getter_access_tracker["ribbonColor"] = {}
		return self._ribbonColor
	@ribbonColor.setter
	def ribbonColor(self, state):
		self._setter_access_tracker["ribbonColor"] = {}
		self._ribbonColor = state

	def _to_json_fields(self):
		return {
			"title": self._title,
			"status": self._status,
			"color": self._color,
			"dot": self._dot,
			"count": self._count,
			"countIcon": self._countIcon,
			"text": self._text,
			"size": self._size,
			"showZero": self._showZero,
			"overflowCount": self._overflowCount,
			"ribbon": self._ribbon,
			"ribbonText": self._ribbonText,
			"ribbonPlacement": self._ribbonPlacement,
			"ribbonColor": self._ribbonColor
			}


class Badge(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Badge"
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
		self._custom = BadgeCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}