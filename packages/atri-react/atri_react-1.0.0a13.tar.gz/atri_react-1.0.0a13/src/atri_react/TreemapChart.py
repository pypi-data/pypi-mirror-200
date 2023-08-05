from typing import Any, Union
from atri_core import AtriComponent



class TreemapChartCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.data: Union[Any, None] = state["data"] if state != None and "data" in state else None
		self.treemap: Union[Any, None] = state["treemap"] if state != None and "treemap" in state else None
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
	def treemap(self):
		self._getter_access_tracker["treemap"] = {}
		return self._treemap
	@treemap.setter
	def treemap(self, state):
		self._setter_access_tracker["treemap"] = {}
		self._treemap = state
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
			"treemap": self._treemap,
			"chartHeight": self._chartHeight,
			"chartWidth": self._chartWidth
			}


class TreemapChart(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "TreemapChart"
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
		self._custom = TreemapChartCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}