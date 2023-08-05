from typing import Any, Union
from atri_core import AtriComponent



class AccordionCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.expandIconPosition: Union[Any, None] = state["expandIconPosition"] if state != None and "expandIconPosition" in state else None
		self.collapse: Union[Any, None] = state["collapse"] if state != None and "collapse" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.ghost: Union[Any, None] = state["ghost"] if state != None and "ghost" in state else None
		self.defaultActiveKey: Union[Any, None] = state["defaultActiveKey"] if state != None and "defaultActiveKey" in state else None
		self.expandIcon: Union[Any, None] = state["expandIcon"] if state != None and "expandIcon" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def expandIconPosition(self):
		self._getter_access_tracker["expandIconPosition"] = {}
		return self._expandIconPosition
	@expandIconPosition.setter
	def expandIconPosition(self, state):
		self._setter_access_tracker["expandIconPosition"] = {}
		self._expandIconPosition = state
	@property
	def collapse(self):
		self._getter_access_tracker["collapse"] = {}
		return self._collapse
	@collapse.setter
	def collapse(self, state):
		self._setter_access_tracker["collapse"] = {}
		self._collapse = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def ghost(self):
		self._getter_access_tracker["ghost"] = {}
		return self._ghost
	@ghost.setter
	def ghost(self, state):
		self._setter_access_tracker["ghost"] = {}
		self._ghost = state
	@property
	def defaultActiveKey(self):
		self._getter_access_tracker["defaultActiveKey"] = {}
		return self._defaultActiveKey
	@defaultActiveKey.setter
	def defaultActiveKey(self, state):
		self._setter_access_tracker["defaultActiveKey"] = {}
		self._defaultActiveKey = state
	@property
	def expandIcon(self):
		self._getter_access_tracker["expandIcon"] = {}
		return self._expandIcon
	@expandIcon.setter
	def expandIcon(self, state):
		self._setter_access_tracker["expandIcon"] = {}
		self._expandIcon = state
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
			"size": self._size,
			"expandIconPosition": self._expandIconPosition,
			"collapse": self._collapse,
			"bordered": self._bordered,
			"ghost": self._ghost,
			"defaultActiveKey": self._defaultActiveKey,
			"expandIcon": self._expandIcon,
			"items": self._items
			}


class Accordion(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Accordion"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
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
		self._custom = AccordionCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}