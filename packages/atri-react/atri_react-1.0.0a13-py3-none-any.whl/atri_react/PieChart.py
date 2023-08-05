from typing import Any, Union
from atri_core import AtriComponent



class PieChartCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.data: Union[Any, None] = state["data"] if state != None and "data" in state else None
		self.options: Union[Any, None] = state["options"] if state != None and "options" in state else None
		self.toolTip: Union[Any, None] = state["toolTip"] if state != None and "toolTip" in state else None
		self.legend: Union[Any, None] = state["legend"] if state != None and "legend" in state else None
		self.keys: Union[Any, None] = state["keys"] if state != None and "keys" in state else None
		self.chartHeight: Union[Any, None] = state["chartHeight"] if state != None and "chartHeight" in state else None
		self.chartWidth: Union[Any, None] = state["chartWidth"] if state != None and "chartWidth" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def data(self):
		self._getter_access_tracker["data"] = {}
		return self._data
	@data.setter
	def data(self, state):
		self._setter_access_tracker["data"] = {}
		self._data = state
	@property
	def options(self):
		self._getter_access_tracker["options"] = {}
		return self._options
	@options.setter
	def options(self, state):
		self._setter_access_tracker["options"] = {}
		self._options = state
	@property
	def toolTip(self):
		self._getter_access_tracker["toolTip"] = {}
		return self._toolTip
	@toolTip.setter
	def toolTip(self, state):
		self._setter_access_tracker["toolTip"] = {}
		self._toolTip = state
	@property
	def legend(self):
		self._getter_access_tracker["legend"] = {}
		return self._legend
	@legend.setter
	def legend(self, state):
		self._setter_access_tracker["legend"] = {}
		self._legend = state
	@property
	def keys(self):
		self._getter_access_tracker["keys"] = {}
		return self._keys
	@keys.setter
	def keys(self, state):
		self._setter_access_tracker["keys"] = {}
		self._keys = state
	@property
	def chartHeight(self):
		self._getter_access_tracker["chartHeight"] = {}
		return self._chartHeight
	@chartHeight.setter
	def chartHeight(self, state):
		self._setter_access_tracker["chartHeight"] = {}
		self._chartHeight = state
	@property
	def chartWidth(self):
		self._getter_access_tracker["chartWidth"] = {}
		return self._chartWidth
	@chartWidth.setter
	def chartWidth(self, state):
		self._setter_access_tracker["chartWidth"] = {}
		self._chartWidth = state

	def _to_json_fields(self):
		return {
			"data": self._data,
			"options": self._options,
			"toolTip": self._toolTip,
			"legend": self._legend,
			"keys": self._keys,
			"chartHeight": self._chartHeight,
			"chartWidth": self._chartWidth
			}


class PieChart(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "PieChart"
		self.nodePkg = "@atrilabs/react-component-manifests"
		
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
		self._custom = PieChartCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}