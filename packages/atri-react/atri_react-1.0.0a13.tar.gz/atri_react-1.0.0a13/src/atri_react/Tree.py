from typing import Any, Union
from atri_core import AtriComponent



class TreeCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.treeData: Union[Any, None] = state["treeData"] if state != None and "treeData" in state else None
		self.checkable: Union[Any, None] = state["checkable"] if state != None and "checkable" in state else None
		self.showLine: Union[Any, None] = state["showLine"] if state != None and "showLine" in state else None
		self.multiple: Union[Any, None] = state["multiple"] if state != None and "multiple" in state else None
		self.defaultExpandAll: Union[Any, None] = state["defaultExpandAll"] if state != None and "defaultExpandAll" in state else None
		self.defaultExpandParent: Union[Any, None] = state["defaultExpandParent"] if state != None and "defaultExpandParent" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def treeData(self):
		self._getter_access_tracker["treeData"] = {}
		return self._treeData
	@treeData.setter
	def treeData(self, state):
		self._setter_access_tracker["treeData"] = {}
		self._treeData = state
	@property
	def checkable(self):
		self._getter_access_tracker["checkable"] = {}
		return self._checkable
	@checkable.setter
	def checkable(self, state):
		self._setter_access_tracker["checkable"] = {}
		self._checkable = state
	@property
	def showLine(self):
		self._getter_access_tracker["showLine"] = {}
		return self._showLine
	@showLine.setter
	def showLine(self, state):
		self._setter_access_tracker["showLine"] = {}
		self._showLine = state
	@property
	def multiple(self):
		self._getter_access_tracker["multiple"] = {}
		return self._multiple
	@multiple.setter
	def multiple(self, state):
		self._setter_access_tracker["multiple"] = {}
		self._multiple = state
	@property
	def defaultExpandAll(self):
		self._getter_access_tracker["defaultExpandAll"] = {}
		return self._defaultExpandAll
	@defaultExpandAll.setter
	def defaultExpandAll(self, state):
		self._setter_access_tracker["defaultExpandAll"] = {}
		self._defaultExpandAll = state
	@property
	def defaultExpandParent(self):
		self._getter_access_tracker["defaultExpandParent"] = {}
		return self._defaultExpandParent
	@defaultExpandParent.setter
	def defaultExpandParent(self, state):
		self._setter_access_tracker["defaultExpandParent"] = {}
		self._defaultExpandParent = state

	def _to_json_fields(self):
		return {
			"treeData": self._treeData,
			"checkable": self._checkable,
			"showLine": self._showLine,
			"multiple": self._multiple,
			"defaultExpandAll": self._defaultExpandAll,
			"defaultExpandParent": self._defaultExpandParent
			}


class Tree(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Tree"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onCheck = False
		self.onExpand = False
		self.onRightClick = False
		self.onSelect = False
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
		self._custom = TreeCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}