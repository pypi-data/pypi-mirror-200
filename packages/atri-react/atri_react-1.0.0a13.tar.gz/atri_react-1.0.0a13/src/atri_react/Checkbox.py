from typing import Any, Union
from atri_core import AtriComponent



class CheckboxCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.checked: Union[Any, None] = state["checked"] if state != None and "checked" in state else None
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def checked(self):
		self._getter_access_tracker["checked"] = {}
		return self._checked
	@checked.setter
	def checked(self, state):
		self._setter_access_tracker["checked"] = {}
		self._checked = state
	@property
	def text(self):
		self._getter_access_tracker["text"] = {}
		return self._text
	@text.setter
	def text(self, state):
		self._setter_access_tracker["text"] = {}
		self._text = state

	def _to_json_fields(self):
		return {
			"checked": self._checked,
			"text": self._text
			}


class Checkbox(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Checkbox"
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
		self._custom = CheckboxCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}