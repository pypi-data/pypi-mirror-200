from typing import Any, Union
from atri_core import AtriComponent



class SliderCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.range: Union[Any, None] = state["range"] if state != None and "range" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.min: Union[Any, None] = state["min"] if state != None and "min" in state else None
		self.max: Union[Any, None] = state["max"] if state != None and "max" in state else None
		self.defaultValue: Union[Any, None] = state["defaultValue"] if state != None and "defaultValue" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self.vertical: Union[Any, None] = state["vertical"] if state != None and "vertical" in state else None
		self.draggableTrack: Union[Any, None] = state["draggableTrack"] if state != None and "draggableTrack" in state else None
		self.reverse: Union[Any, None] = state["reverse"] if state != None and "reverse" in state else None
		self.marks: Union[Any, None] = state["marks"] if state != None and "marks" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def range(self):
		self._getter_access_tracker["range"] = {}
		return self._range
	@range.setter
	def range(self, state):
		self._setter_access_tracker["range"] = {}
		self._range = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def min(self):
		self._getter_access_tracker["min"] = {}
		return self._min
	@min.setter
	def min(self, state):
		self._setter_access_tracker["min"] = {}
		self._min = state
	@property
	def max(self):
		self._getter_access_tracker["max"] = {}
		return self._max
	@max.setter
	def max(self, state):
		self._setter_access_tracker["max"] = {}
		self._max = state
	@property
	def defaultValue(self):
		self._getter_access_tracker["defaultValue"] = {}
		return self._defaultValue
	@defaultValue.setter
	def defaultValue(self, state):
		self._setter_access_tracker["defaultValue"] = {}
		self._defaultValue = state
	@property
	def disabled(self):
		self._getter_access_tracker["disabled"] = {}
		return self._disabled
	@disabled.setter
	def disabled(self, state):
		self._setter_access_tracker["disabled"] = {}
		self._disabled = state
	@property
	def vertical(self):
		self._getter_access_tracker["vertical"] = {}
		return self._vertical
	@vertical.setter
	def vertical(self, state):
		self._setter_access_tracker["vertical"] = {}
		self._vertical = state
	@property
	def draggableTrack(self):
		self._getter_access_tracker["draggableTrack"] = {}
		return self._draggableTrack
	@draggableTrack.setter
	def draggableTrack(self, state):
		self._setter_access_tracker["draggableTrack"] = {}
		self._draggableTrack = state
	@property
	def reverse(self):
		self._getter_access_tracker["reverse"] = {}
		return self._reverse
	@reverse.setter
	def reverse(self, state):
		self._setter_access_tracker["reverse"] = {}
		self._reverse = state
	@property
	def marks(self):
		self._getter_access_tracker["marks"] = {}
		return self._marks
	@marks.setter
	def marks(self, state):
		self._setter_access_tracker["marks"] = {}
		self._marks = state

	def _to_json_fields(self):
		return {
			"range": self._range,
			"value": self._value,
			"min": self._min,
			"max": self._max,
			"defaultValue": self._defaultValue,
			"disabled": self._disabled,
			"vertical": self._vertical,
			"draggableTrack": self._draggableTrack,
			"reverse": self._reverse,
			"marks": self._marks
			}


class Slider(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Slider"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
		self.onAfterChange = False
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
		self._custom = SliderCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}