from typing import Any, Union, TypeVar, Generic, List
from atri_core import AtriComponent

T = TypeVar("T")

class RepeatingCustomClass(Generic[T]):
	def __init__(self, state: Union[Any, None], WrapperClass: T):
		self._setter_access_tracker = {}
		self._WrapperClass = WrapperClass
		self.data: Union[List[T], None] = state["data"] if state != None and "data" in state else []
		self.start: Union[Any, None] = state["start"] if state != None and "start" in state else None
		self.end: Union[Any, None] = state["end"] if state != None and "end" in state else None
		self.image: Union[Any, None] = state["image"] if state != None and "image" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def data(self):
		self._getter_access_tracker["data"] = {}
		return self._data
	@data.setter
	def data(self, state):
		self._setter_access_tracker["data"] = {}
		if type(state) == "list":
			self._data = [self._WrapperClass(i) for i in state]
		else:
			self._data = []
	@property
	def start(self):
		self._getter_access_tracker["start"] = {}
		return self._start
	@start.setter
	def start(self, state):
		self._setter_access_tracker["start"] = {}
		self._start = state
	@property
	def end(self):
		self._getter_access_tracker["end"] = {}
		return self._end
	@end.setter
	def end(self, state):
		self._setter_access_tracker["end"] = {}
		self._end = state
	@property
	def image(self):
		self._getter_access_tracker["image"] = {}
		return self._image
	@image.setter
	def image(self, state):
		self._setter_access_tracker["image"] = {}
		self._image = state

	def _to_json_fields(self):
		return {
			"data": self._data,
			"start": self._start,
			"end": self._end,
			"image": self._image
			}


class Repeating(AtriComponent, Generic[T]):
	def __init__(self, state: Union[Any, None], WrapperClass: T):
		super().__init__(state)
		self._setter_access_tracker = {}
		self._WrapperClass = WrapperClass
		self.compKey = "Repeating"
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
		self._custom = RepeatingCustomClass[T](state, self._WrapperClass)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}