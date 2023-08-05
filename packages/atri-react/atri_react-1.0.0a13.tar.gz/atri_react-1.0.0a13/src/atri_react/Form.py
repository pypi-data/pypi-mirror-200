from typing import Any, Union
from atri_core import AtriComponent



class FormCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.autocomplete: Union[Any, None] = state["autocomplete"] if state != None and "autocomplete" in state else None
		self.form: Union[Any, None] = state["form"] if state != None and "form" in state else None
		self.showSubmitButton: Union[Any, None] = state["showSubmitButton"] if state != None and "showSubmitButton" in state else None
		self.showResetButton: Union[Any, None] = state["showResetButton"] if state != None and "showResetButton" in state else None
		self.submitButtonBgColor: Union[Any, None] = state["submitButtonBgColor"] if state != None and "submitButtonBgColor" in state else None
		self.submitButtonColor: Union[Any, None] = state["submitButtonColor"] if state != None and "submitButtonColor" in state else None
		self.resetButtonBgColor: Union[Any, None] = state["resetButtonBgColor"] if state != None and "resetButtonBgColor" in state else None
		self.resetButtonColor: Union[Any, None] = state["resetButtonColor"] if state != None and "resetButtonColor" in state else None
		self.target: Union[Any, None] = state["target"] if state != None and "target" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def autocomplete(self):
		self._getter_access_tracker["autocomplete"] = {}
		return self._autocomplete
	@autocomplete.setter
	def autocomplete(self, state):
		self._setter_access_tracker["autocomplete"] = {}
		self._autocomplete = state
	@property
	def form(self):
		self._getter_access_tracker["form"] = {}
		return self._form
	@form.setter
	def form(self, state):
		self._setter_access_tracker["form"] = {}
		self._form = state
	@property
	def showSubmitButton(self):
		self._getter_access_tracker["showSubmitButton"] = {}
		return self._showSubmitButton
	@showSubmitButton.setter
	def showSubmitButton(self, state):
		self._setter_access_tracker["showSubmitButton"] = {}
		self._showSubmitButton = state
	@property
	def showResetButton(self):
		self._getter_access_tracker["showResetButton"] = {}
		return self._showResetButton
	@showResetButton.setter
	def showResetButton(self, state):
		self._setter_access_tracker["showResetButton"] = {}
		self._showResetButton = state
	@property
	def submitButtonBgColor(self):
		self._getter_access_tracker["submitButtonBgColor"] = {}
		return self._submitButtonBgColor
	@submitButtonBgColor.setter
	def submitButtonBgColor(self, state):
		self._setter_access_tracker["submitButtonBgColor"] = {}
		self._submitButtonBgColor = state
	@property
	def submitButtonColor(self):
		self._getter_access_tracker["submitButtonColor"] = {}
		return self._submitButtonColor
	@submitButtonColor.setter
	def submitButtonColor(self, state):
		self._setter_access_tracker["submitButtonColor"] = {}
		self._submitButtonColor = state
	@property
	def resetButtonBgColor(self):
		self._getter_access_tracker["resetButtonBgColor"] = {}
		return self._resetButtonBgColor
	@resetButtonBgColor.setter
	def resetButtonBgColor(self, state):
		self._setter_access_tracker["resetButtonBgColor"] = {}
		self._resetButtonBgColor = state
	@property
	def resetButtonColor(self):
		self._getter_access_tracker["resetButtonColor"] = {}
		return self._resetButtonColor
	@resetButtonColor.setter
	def resetButtonColor(self, state):
		self._setter_access_tracker["resetButtonColor"] = {}
		self._resetButtonColor = state
	@property
	def target(self):
		self._getter_access_tracker["target"] = {}
		return self._target
	@target.setter
	def target(self, state):
		self._setter_access_tracker["target"] = {}
		self._target = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state

	def _to_json_fields(self):
		return {
			"autocomplete": self._autocomplete,
			"form": self._form,
			"showSubmitButton": self._showSubmitButton,
			"showResetButton": self._showResetButton,
			"submitButtonBgColor": self._submitButtonBgColor,
			"submitButtonColor": self._submitButtonColor,
			"resetButtonBgColor": self._resetButtonBgColor,
			"resetButtonColor": self._resetButtonColor,
			"target": self._target,
			"disabled": self._disabled
			}


class Form(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Form"
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
		self._custom = FormCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}