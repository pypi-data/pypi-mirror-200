from typing import Any, Union
from atri_core import AtriComponent



class AlertCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.text: Union[Any, None] = state["text"] if state != None and "text" in state else None
		self.description: Union[Any, None] = state["description"] if state != None and "description" in state else None
		self.alertType: Union[Any, None] = state["alertType"] if state != None and "alertType" in state else None
		self.showIcon: Union[Any, None] = state["showIcon"] if state != None and "showIcon" in state else None
		self.icon: Union[Any, None] = state["icon"] if state != None and "icon" in state else None
		self.isClosable: Union[Any, None] = state["isClosable"] if state != None and "isClosable" in state else None
		self.closeText: Union[Any, None] = state["closeText"] if state != None and "closeText" in state else None
		self.closeIcon: Union[Any, None] = state["closeIcon"] if state != None and "closeIcon" in state else None
		self.banner: Union[Any, None] = state["banner"] if state != None and "banner" in state else None
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
	def description(self):
		self._getter_access_tracker["description"] = {}
		return self._description
	@description.setter
	def description(self, state):
		self._setter_access_tracker["description"] = {}
		self._description = state
	@property
	def alertType(self):
		self._getter_access_tracker["alertType"] = {}
		return self._alertType
	@alertType.setter
	def alertType(self, state):
		self._setter_access_tracker["alertType"] = {}
		self._alertType = state
	@property
	def showIcon(self):
		self._getter_access_tracker["showIcon"] = {}
		return self._showIcon
	@showIcon.setter
	def showIcon(self, state):
		self._setter_access_tracker["showIcon"] = {}
		self._showIcon = state
	@property
	def icon(self):
		self._getter_access_tracker["icon"] = {}
		return self._icon
	@icon.setter
	def icon(self, state):
		self._setter_access_tracker["icon"] = {}
		self._icon = state
	@property
	def isClosable(self):
		self._getter_access_tracker["isClosable"] = {}
		return self._isClosable
	@isClosable.setter
	def isClosable(self, state):
		self._setter_access_tracker["isClosable"] = {}
		self._isClosable = state
	@property
	def closeText(self):
		self._getter_access_tracker["closeText"] = {}
		return self._closeText
	@closeText.setter
	def closeText(self, state):
		self._setter_access_tracker["closeText"] = {}
		self._closeText = state
	@property
	def closeIcon(self):
		self._getter_access_tracker["closeIcon"] = {}
		return self._closeIcon
	@closeIcon.setter
	def closeIcon(self, state):
		self._setter_access_tracker["closeIcon"] = {}
		self._closeIcon = state
	@property
	def banner(self):
		self._getter_access_tracker["banner"] = {}
		return self._banner
	@banner.setter
	def banner(self, state):
		self._setter_access_tracker["banner"] = {}
		self._banner = state

	def _to_json_fields(self):
		return {
			"text": self._text,
			"description": self._description,
			"alertType": self._alertType,
			"showIcon": self._showIcon,
			"icon": self._icon,
			"isClosable": self._isClosable,
			"closeText": self._closeText,
			"closeIcon": self._closeIcon,
			"banner": self._banner
			}


class Alert(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Alert"
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
		self._custom = AlertCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}