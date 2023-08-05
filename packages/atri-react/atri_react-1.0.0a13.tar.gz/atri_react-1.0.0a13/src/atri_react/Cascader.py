from typing import Any, Union
from atri_core import AtriComponent



class CascaderCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.options: Union[Any, None] = state["options"] if state != None and "options" in state else None
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.allowClear: Union[Any, None] = state["allowClear"] if state != None and "allowClear" in state else None
		self.multiple: Union[Any, None] = state["multiple"] if state != None and "multiple" in state else None
		self.showCheckedStrategy: Union[Any, None] = state["showCheckedStrategy"] if state != None and "showCheckedStrategy" in state else None
		self.maxTagCount: Union[Any, None] = state["maxTagCount"] if state != None and "maxTagCount" in state else None
		self.maxTagTextLength: Union[Any, None] = state["maxTagTextLength"] if state != None and "maxTagTextLength" in state else None
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.showSearch: Union[Any, None] = state["showSearch"] if state != None and "showSearch" in state else None
		self.open: Union[Any, None] = state["open"] if state != None and "open" in state else None
		self.placement: Union[Any, None] = state["placement"] if state != None and "placement" in state else None
		self.suffixIcon: Union[Any, None] = state["suffixIcon"] if state != None and "suffixIcon" in state else None
		self.removeIcon: Union[Any, None] = state["removeIcon"] if state != None and "removeIcon" in state else None
		self.clearIcon: Union[Any, None] = state["clearIcon"] if state != None and "clearIcon" in state else None
		self.expandIcon: Union[Any, None] = state["expandIcon"] if state != None and "expandIcon" in state else None
		self.expandTrigger: Union[Any, None] = state["expandTrigger"] if state != None and "expandTrigger" in state else None
		self.status: Union[Any, None] = state["status"] if state != None and "status" in state else None
		self.notFoundContent: Union[Any, None] = state["notFoundContent"] if state != None and "notFoundContent" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def options(self):
		self._getter_access_tracker["options"] = {}
		return self._options
	@options.setter
	def options(self, state):
		self._setter_access_tracker["options"] = {}
		self._options = state
	@property
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def allowClear(self):
		self._getter_access_tracker["allowClear"] = {}
		return self._allowClear
	@allowClear.setter
	def allowClear(self, state):
		self._setter_access_tracker["allowClear"] = {}
		self._allowClear = state
	@property
	def multiple(self):
		self._getter_access_tracker["multiple"] = {}
		return self._multiple
	@multiple.setter
	def multiple(self, state):
		self._setter_access_tracker["multiple"] = {}
		self._multiple = state
	@property
	def showCheckedStrategy(self):
		self._getter_access_tracker["showCheckedStrategy"] = {}
		return self._showCheckedStrategy
	@showCheckedStrategy.setter
	def showCheckedStrategy(self, state):
		self._setter_access_tracker["showCheckedStrategy"] = {}
		self._showCheckedStrategy = state
	@property
	def maxTagCount(self):
		self._getter_access_tracker["maxTagCount"] = {}
		return self._maxTagCount
	@maxTagCount.setter
	def maxTagCount(self, state):
		self._setter_access_tracker["maxTagCount"] = {}
		self._maxTagCount = state
	@property
	def maxTagTextLength(self):
		self._getter_access_tracker["maxTagTextLength"] = {}
		return self._maxTagTextLength
	@maxTagTextLength.setter
	def maxTagTextLength(self, state):
		self._setter_access_tracker["maxTagTextLength"] = {}
		self._maxTagTextLength = state
	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def showSearch(self):
		self._getter_access_tracker["showSearch"] = {}
		return self._showSearch
	@showSearch.setter
	def showSearch(self, state):
		self._setter_access_tracker["showSearch"] = {}
		self._showSearch = state
	@property
	def open(self):
		self._getter_access_tracker["open"] = {}
		return self._open
	@open.setter
	def open(self, state):
		self._setter_access_tracker["open"] = {}
		self._open = state
	@property
	def placement(self):
		self._getter_access_tracker["placement"] = {}
		return self._placement
	@placement.setter
	def placement(self, state):
		self._setter_access_tracker["placement"] = {}
		self._placement = state
	@property
	def suffixIcon(self):
		self._getter_access_tracker["suffixIcon"] = {}
		return self._suffixIcon
	@suffixIcon.setter
	def suffixIcon(self, state):
		self._setter_access_tracker["suffixIcon"] = {}
		self._suffixIcon = state
	@property
	def removeIcon(self):
		self._getter_access_tracker["removeIcon"] = {}
		return self._removeIcon
	@removeIcon.setter
	def removeIcon(self, state):
		self._setter_access_tracker["removeIcon"] = {}
		self._removeIcon = state
	@property
	def clearIcon(self):
		self._getter_access_tracker["clearIcon"] = {}
		return self._clearIcon
	@clearIcon.setter
	def clearIcon(self, state):
		self._setter_access_tracker["clearIcon"] = {}
		self._clearIcon = state
	@property
	def expandIcon(self):
		self._getter_access_tracker["expandIcon"] = {}
		return self._expandIcon
	@expandIcon.setter
	def expandIcon(self, state):
		self._setter_access_tracker["expandIcon"] = {}
		self._expandIcon = state
	@property
	def expandTrigger(self):
		self._getter_access_tracker["expandTrigger"] = {}
		return self._expandTrigger
	@expandTrigger.setter
	def expandTrigger(self, state):
		self._setter_access_tracker["expandTrigger"] = {}
		self._expandTrigger = state
	@property
	def status(self):
		self._getter_access_tracker["status"] = {}
		return self._status
	@status.setter
	def status(self, state):
		self._setter_access_tracker["status"] = {}
		self._status = state
	@property
	def notFoundContent(self):
		self._getter_access_tracker["notFoundContent"] = {}
		return self._notFoundContent
	@notFoundContent.setter
	def notFoundContent(self, state):
		self._setter_access_tracker["notFoundContent"] = {}
		self._notFoundContent = state

	def _to_json_fields(self):
		return {
			"options": self._options,
			"placeholder": self._placeholder,
			"allowClear": self._allowClear,
			"multiple": self._multiple,
			"showCheckedStrategy": self._showCheckedStrategy,
			"maxTagCount": self._maxTagCount,
			"maxTagTextLength": self._maxTagTextLength,
			"size": self._size,
			"disabled": self._disabled,
			"bordered": self._bordered,
			"showSearch": self._showSearch,
			"open": self._open,
			"placement": self._placement,
			"suffixIcon": self._suffixIcon,
			"removeIcon": self._removeIcon,
			"clearIcon": self._clearIcon,
			"expandIcon": self._expandIcon,
			"expandTrigger": self._expandTrigger,
			"status": self._status,
			"notFoundContent": self._notFoundContent
			}


class Cascader(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Cascader"
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
		self._custom = CascaderCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}