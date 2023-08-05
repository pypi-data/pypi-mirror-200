from typing import Any, Union
from atri_core import AtriComponent



class UnorderedListCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.size: Union[Any, None] = state["size"] if state != None and "size" in state else None
		self.itemLayout: Union[Any, None] = state["itemLayout"] if state != None and "itemLayout" in state else None
		self.bordered: Union[Any, None] = state["bordered"] if state != None and "bordered" in state else None
		self.split: Union[Any, None] = state["split"] if state != None and "split" in state else None
		self.items: Union[Any, None] = state["items"] if state != None and "items" in state else None
		self.actionAdd: Union[Any, None] = state["actionAdd"] if state != None and "actionAdd" in state else None
		self.actionUpdate: Union[Any, None] = state["actionUpdate"] if state != None and "actionUpdate" in state else None
		self.actionDelete: Union[Any, None] = state["actionDelete"] if state != None and "actionDelete" in state else None
		self.pagination: Union[Any, None] = state["pagination"] if state != None and "pagination" in state else None
		self.paginationPosition: Union[Any, None] = state["paginationPosition"] if state != None and "paginationPosition" in state else None
		self.paginationAlign: Union[Any, None] = state["paginationAlign"] if state != None and "paginationAlign" in state else None
		self.grid: Union[Any, None] = state["grid"] if state != None and "grid" in state else None
		self.gutter: Union[Any, None] = state["gutter"] if state != None and "gutter" in state else None
		self.column: Union[Any, None] = state["column"] if state != None and "column" in state else None
		self.xs: Union[Any, None] = state["xs"] if state != None and "xs" in state else None
		self.sm: Union[Any, None] = state["sm"] if state != None and "sm" in state else None
		self.md: Union[Any, None] = state["md"] if state != None and "md" in state else None
		self.lg: Union[Any, None] = state["lg"] if state != None and "lg" in state else None
		self.xl: Union[Any, None] = state["xl"] if state != None and "xl" in state else None
		self.xxl: Union[Any, None] = state["xxl"] if state != None and "xxl" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def size(self):
		self._getter_access_tracker["size"] = {}
		return self._size
	@size.setter
	def size(self, state):
		self._setter_access_tracker["size"] = {}
		self._size = state
	@property
	def itemLayout(self):
		self._getter_access_tracker["itemLayout"] = {}
		return self._itemLayout
	@itemLayout.setter
	def itemLayout(self, state):
		self._setter_access_tracker["itemLayout"] = {}
		self._itemLayout = state
	@property
	def bordered(self):
		self._getter_access_tracker["bordered"] = {}
		return self._bordered
	@bordered.setter
	def bordered(self, state):
		self._setter_access_tracker["bordered"] = {}
		self._bordered = state
	@property
	def split(self):
		self._getter_access_tracker["split"] = {}
		return self._split
	@split.setter
	def split(self, state):
		self._setter_access_tracker["split"] = {}
		self._split = state
	@property
	def items(self):
		self._getter_access_tracker["items"] = {}
		return self._items
	@items.setter
	def items(self, state):
		self._setter_access_tracker["items"] = {}
		self._items = state
	@property
	def actionAdd(self):
		self._getter_access_tracker["actionAdd"] = {}
		return self._actionAdd
	@actionAdd.setter
	def actionAdd(self, state):
		self._setter_access_tracker["actionAdd"] = {}
		self._actionAdd = state
	@property
	def actionUpdate(self):
		self._getter_access_tracker["actionUpdate"] = {}
		return self._actionUpdate
	@actionUpdate.setter
	def actionUpdate(self, state):
		self._setter_access_tracker["actionUpdate"] = {}
		self._actionUpdate = state
	@property
	def actionDelete(self):
		self._getter_access_tracker["actionDelete"] = {}
		return self._actionDelete
	@actionDelete.setter
	def actionDelete(self, state):
		self._setter_access_tracker["actionDelete"] = {}
		self._actionDelete = state
	@property
	def pagination(self):
		self._getter_access_tracker["pagination"] = {}
		return self._pagination
	@pagination.setter
	def pagination(self, state):
		self._setter_access_tracker["pagination"] = {}
		self._pagination = state
	@property
	def paginationPosition(self):
		self._getter_access_tracker["paginationPosition"] = {}
		return self._paginationPosition
	@paginationPosition.setter
	def paginationPosition(self, state):
		self._setter_access_tracker["paginationPosition"] = {}
		self._paginationPosition = state
	@property
	def paginationAlign(self):
		self._getter_access_tracker["paginationAlign"] = {}
		return self._paginationAlign
	@paginationAlign.setter
	def paginationAlign(self, state):
		self._setter_access_tracker["paginationAlign"] = {}
		self._paginationAlign = state
	@property
	def grid(self):
		self._getter_access_tracker["grid"] = {}
		return self._grid
	@grid.setter
	def grid(self, state):
		self._setter_access_tracker["grid"] = {}
		self._grid = state
	@property
	def gutter(self):
		self._getter_access_tracker["gutter"] = {}
		return self._gutter
	@gutter.setter
	def gutter(self, state):
		self._setter_access_tracker["gutter"] = {}
		self._gutter = state
	@property
	def column(self):
		self._getter_access_tracker["column"] = {}
		return self._column
	@column.setter
	def column(self, state):
		self._setter_access_tracker["column"] = {}
		self._column = state
	@property
	def xs(self):
		self._getter_access_tracker["xs"] = {}
		return self._xs
	@xs.setter
	def xs(self, state):
		self._setter_access_tracker["xs"] = {}
		self._xs = state
	@property
	def sm(self):
		self._getter_access_tracker["sm"] = {}
		return self._sm
	@sm.setter
	def sm(self, state):
		self._setter_access_tracker["sm"] = {}
		self._sm = state
	@property
	def md(self):
		self._getter_access_tracker["md"] = {}
		return self._md
	@md.setter
	def md(self, state):
		self._setter_access_tracker["md"] = {}
		self._md = state
	@property
	def lg(self):
		self._getter_access_tracker["lg"] = {}
		return self._lg
	@lg.setter
	def lg(self, state):
		self._setter_access_tracker["lg"] = {}
		self._lg = state
	@property
	def xl(self):
		self._getter_access_tracker["xl"] = {}
		return self._xl
	@xl.setter
	def xl(self, state):
		self._setter_access_tracker["xl"] = {}
		self._xl = state
	@property
	def xxl(self):
		self._getter_access_tracker["xxl"] = {}
		return self._xxl
	@xxl.setter
	def xxl(self, state):
		self._setter_access_tracker["xxl"] = {}
		self._xxl = state

	def _to_json_fields(self):
		return {
			"size": self._size,
			"itemLayout": self._itemLayout,
			"bordered": self._bordered,
			"split": self._split,
			"items": self._items,
			"actionAdd": self._actionAdd,
			"actionUpdate": self._actionUpdate,
			"actionDelete": self._actionDelete,
			"pagination": self._pagination,
			"paginationPosition": self._paginationPosition,
			"paginationAlign": self._paginationAlign,
			"grid": self._grid,
			"gutter": self._gutter,
			"column": self._column,
			"xs": self._xs,
			"sm": self._sm,
			"md": self._md,
			"lg": self._lg,
			"xl": self._xl,
			"xxl": self._xxl
			}


class UnorderedList(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "UnorderedList"
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
		self._custom = UnorderedListCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}