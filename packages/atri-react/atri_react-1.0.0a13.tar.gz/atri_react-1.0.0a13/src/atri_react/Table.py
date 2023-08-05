from typing import Any, Union
from atri_core import AtriComponent



class TableCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.rows: Union[Any, None] = state["rows"] if state != None and "rows" in state else None
		self.cols: Union[Any, None] = state["cols"] if state != None and "cols" in state else None
		self.checkboxSelection: Union[Any, None] = state["checkboxSelection"] if state != None and "checkboxSelection" in state else None
		self.autoHeight: Union[Any, None] = state["autoHeight"] if state != None and "autoHeight" in state else None
		self.numRows: Union[Any, None] = state["numRows"] if state != None and "numRows" in state else None
		self.rowHeight: Union[Any, None] = state["rowHeight"] if state != None and "rowHeight" in state else None
		self.selection: Union[Any, None] = state["selection"] if state != None and "selection" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def rows(self):
		self._getter_access_tracker["rows"] = {}
		return self._rows
	@rows.setter
	def rows(self, state):
		self._setter_access_tracker["rows"] = {}
		self._rows = state
	@property
	def cols(self):
		self._getter_access_tracker["cols"] = {}
		return self._cols
	@cols.setter
	def cols(self, state):
		self._setter_access_tracker["cols"] = {}
		self._cols = state
	@property
	def checkboxSelection(self):
		self._getter_access_tracker["checkboxSelection"] = {}
		return self._checkboxSelection
	@checkboxSelection.setter
	def checkboxSelection(self, state):
		self._setter_access_tracker["checkboxSelection"] = {}
		self._checkboxSelection = state
	@property
	def autoHeight(self):
		self._getter_access_tracker["autoHeight"] = {}
		return self._autoHeight
	@autoHeight.setter
	def autoHeight(self, state):
		self._setter_access_tracker["autoHeight"] = {}
		self._autoHeight = state
	@property
	def numRows(self):
		self._getter_access_tracker["numRows"] = {}
		return self._numRows
	@numRows.setter
	def numRows(self, state):
		self._setter_access_tracker["numRows"] = {}
		self._numRows = state
	@property
	def rowHeight(self):
		self._getter_access_tracker["rowHeight"] = {}
		return self._rowHeight
	@rowHeight.setter
	def rowHeight(self, state):
		self._setter_access_tracker["rowHeight"] = {}
		self._rowHeight = state
	@property
	def selection(self):
		self._getter_access_tracker["selection"] = {}
		return self._selection
	@selection.setter
	def selection(self, state):
		self._setter_access_tracker["selection"] = {}
		self._selection = state

	def _to_json_fields(self):
		return {
			"rows": self._rows,
			"cols": self._cols,
			"checkboxSelection": self._checkboxSelection,
			"autoHeight": self._autoHeight,
			"numRows": self._numRows,
			"rowHeight": self._rowHeight,
			"selection": self._selection
			}


class Table(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Table"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onSelectionChange = False
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
		self._custom = TableCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}