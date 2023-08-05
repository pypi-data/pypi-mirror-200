from typing import Any, Union
from atri_core import AtriComponent



class AnchorCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.href: Union[Any, None] = state["href"] if state != None and "href" in state else None
		self.download: Union[Any, None] = state["download"] if state != None and "download" in state else None
		self.referrerPolicy: Union[Any, None] = state["referrerPolicy"] if state != None and "referrerPolicy" in state else None
		self.rel: Union[Any, None] = state["rel"] if state != None and "rel" in state else None
		self.target: Union[Any, None] = state["target"] if state != None and "target" in state else None
		self.hreflang: Union[Any, None] = state["hreflang"] if state != None and "hreflang" in state else None
		self.ping: Union[Any, None] = state["ping"] if state != None and "ping" in state else None
		self.type: Union[Any, None] = state["type"] if state != None and "type" in state else None
		self.disabled: Union[Any, None] = state["disabled"] if state != None and "disabled" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def href(self):
		self._getter_access_tracker["href"] = {}
		return self._href
	@href.setter
	def href(self, state):
		self._setter_access_tracker["href"] = {}
		self._href = state
	@property
	def download(self):
		self._getter_access_tracker["download"] = {}
		return self._download
	@download.setter
	def download(self, state):
		self._setter_access_tracker["download"] = {}
		self._download = state
	@property
	def referrerPolicy(self):
		self._getter_access_tracker["referrerPolicy"] = {}
		return self._referrerPolicy
	@referrerPolicy.setter
	def referrerPolicy(self, state):
		self._setter_access_tracker["referrerPolicy"] = {}
		self._referrerPolicy = state
	@property
	def rel(self):
		self._getter_access_tracker["rel"] = {}
		return self._rel
	@rel.setter
	def rel(self, state):
		self._setter_access_tracker["rel"] = {}
		self._rel = state
	@property
	def target(self):
		self._getter_access_tracker["target"] = {}
		return self._target
	@target.setter
	def target(self, state):
		self._setter_access_tracker["target"] = {}
		self._target = state
	@property
	def hreflang(self):
		self._getter_access_tracker["hreflang"] = {}
		return self._hreflang
	@hreflang.setter
	def hreflang(self, state):
		self._setter_access_tracker["hreflang"] = {}
		self._hreflang = state
	@property
	def ping(self):
		self._getter_access_tracker["ping"] = {}
		return self._ping
	@ping.setter
	def ping(self, state):
		self._setter_access_tracker["ping"] = {}
		self._ping = state
	@property
	def type(self):
		self._getter_access_tracker["type"] = {}
		return self._type
	@type.setter
	def type(self, state):
		self._setter_access_tracker["type"] = {}
		self._type = state
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
			"href": self._href,
			"download": self._download,
			"referrerPolicy": self._referrerPolicy,
			"rel": self._rel,
			"target": self._target,
			"hreflang": self._hreflang,
			"ping": self._ping,
			"type": self._type,
			"disabled": self._disabled
			}


class Anchor(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Anchor"
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
		self._custom = AnchorCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}