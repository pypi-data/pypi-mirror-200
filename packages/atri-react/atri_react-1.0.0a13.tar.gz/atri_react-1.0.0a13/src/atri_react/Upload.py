from typing import Any, Union
from atri_core import AtriComponent



class UploadCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.listType: Union[Any, None] = state["listType"] if state != None and "listType" in state else None
		self.dragger: Union[Any, None] = state["dragger"] if state != None and "dragger" in state else None
		self.maxCount: Union[Any, None] = state["maxCount"] if state != None and "maxCount" in state else None
		self.multiple: Union[Any, None] = state["multiple"] if state != None and "multiple" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.directory: Union[Any, None] = state["directory"] if state != None and "directory" in state else None
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
	def listType(self):
		self._getter_access_tracker["listType"] = {}
		return self._listType
	@listType.setter
	def listType(self, state):
		self._setter_access_tracker["listType"] = {}
		self._listType = state
	@property
	def dragger(self):
		self._getter_access_tracker["dragger"] = {}
		return self._dragger
	@dragger.setter
	def dragger(self, state):
		self._setter_access_tracker["dragger"] = {}
		self._dragger = state
	@property
	def maxCount(self):
		self._getter_access_tracker["maxCount"] = {}
		return self._maxCount
	@maxCount.setter
	def maxCount(self, state):
		self._setter_access_tracker["maxCount"] = {}
		self._maxCount = state
	@property
	def multiple(self):
		self._getter_access_tracker["multiple"] = {}
		return self._multiple
	@multiple.setter
	def multiple(self, state):
		self._setter_access_tracker["multiple"] = {}
		self._multiple = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def directory(self):
		self._getter_access_tracker["directory"] = {}
		return self._directory
	@directory.setter
	def directory(self, state):
		self._setter_access_tracker["directory"] = {}
		self._directory = state

	def _to_json_fields(self):
		return {
			"text": self._text,
			"listType": self._listType,
			"dragger": self._dragger,
			"maxCount": self._maxCount,
			"multiple": self._multiple,
			"disabled": self._disabled,
			"directory": self._directory
			}


class Upload(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Upload"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
		self.beforeUpload = False
		self.onDrop = False
		self.onPreview = False
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
		self._custom = UploadCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}