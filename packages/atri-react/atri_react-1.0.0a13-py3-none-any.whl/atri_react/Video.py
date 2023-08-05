from typing import Any, Union
from atri_core import AtriComponent



class VideoCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.playing: Union[Any, None] = state["playing"] if state != None and "playing" in state else None
		self.url: Union[Any, None] = state["url"] if state != None and "url" in state else None
		self.light: Union[Any, None] = state["light"] if state != None and "light" in state else None
		self.loop: Union[Any, None] = state["loop"] if state != None and "loop" in state else None
		self.controls: Union[Any, None] = state["controls"] if state != None and "controls" in state else None
		self.volume: Union[Any, None] = state["volume"] if state != None and "volume" in state else None
		self.muted: Union[Any, None] = state["muted"] if state != None and "muted" in state else None
		self.playbackRate: Union[Any, None] = state["playbackRate"] if state != None and "playbackRate" in state else None
		self.progressInterval: Union[Any, None] = state["progressInterval"] if state != None and "progressInterval" in state else None
		self.playsinline: Union[Any, None] = state["playsinline"] if state != None and "playsinline" in state else None
		self.playIcon: Union[Any, None] = state["playIcon"] if state != None and "playIcon" in state else None
		self.previewTabIndex: Union[Any, None] = state["previewTabIndex"] if state != None and "previewTabIndex" in state else None
		self.pip: Union[Any, None] = state["pip"] if state != None and "pip" in state else None
		self.stopOnUnmount: Union[Any, None] = state["stopOnUnmount"] if state != None and "stopOnUnmount" in state else None
		self.fallback: Union[Any, None] = state["fallback"] if state != None and "fallback" in state else None
		self.config: Union[Any, None] = state["config"] if state != None and "config" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def playing(self):
		self._getter_access_tracker["playing"] = {}
		return self._playing
	@playing.setter
	def playing(self, state):
		self._setter_access_tracker["playing"] = {}
		self._playing = state
	@property
	def url(self):
		self._getter_access_tracker["url"] = {}
		return self._url
	@url.setter
	def url(self, state):
		self._setter_access_tracker["url"] = {}
		self._url = state
	@property
	def light(self):
		self._getter_access_tracker["light"] = {}
		return self._light
	@light.setter
	def light(self, state):
		self._setter_access_tracker["light"] = {}
		self._light = state
	@property
	def loop(self):
		self._getter_access_tracker["loop"] = {}
		return self._loop
	@loop.setter
	def loop(self, state):
		self._setter_access_tracker["loop"] = {}
		self._loop = state
	@property
	def controls(self):
		self._getter_access_tracker["controls"] = {}
		return self._controls
	@controls.setter
	def controls(self, state):
		self._setter_access_tracker["controls"] = {}
		self._controls = state
	@property
	def volume(self):
		self._getter_access_tracker["volume"] = {}
		return self._volume
	@volume.setter
	def volume(self, state):
		self._setter_access_tracker["volume"] = {}
		self._volume = state
	@property
	def muted(self):
		self._getter_access_tracker["muted"] = {}
		return self._muted
	@muted.setter
	def muted(self, state):
		self._setter_access_tracker["muted"] = {}
		self._muted = state
	@property
	def playbackRate(self):
		self._getter_access_tracker["playbackRate"] = {}
		return self._playbackRate
	@playbackRate.setter
	def playbackRate(self, state):
		self._setter_access_tracker["playbackRate"] = {}
		self._playbackRate = state
	@property
	def progressInterval(self):
		self._getter_access_tracker["progressInterval"] = {}
		return self._progressInterval
	@progressInterval.setter
	def progressInterval(self, state):
		self._setter_access_tracker["progressInterval"] = {}
		self._progressInterval = state
	@property
	def playsinline(self):
		self._getter_access_tracker["playsinline"] = {}
		return self._playsinline
	@playsinline.setter
	def playsinline(self, state):
		self._setter_access_tracker["playsinline"] = {}
		self._playsinline = state
	@property
	def playIcon(self):
		self._getter_access_tracker["playIcon"] = {}
		return self._playIcon
	@playIcon.setter
	def playIcon(self, state):
		self._setter_access_tracker["playIcon"] = {}
		self._playIcon = state
	@property
	def previewTabIndex(self):
		self._getter_access_tracker["previewTabIndex"] = {}
		return self._previewTabIndex
	@previewTabIndex.setter
	def previewTabIndex(self, state):
		self._setter_access_tracker["previewTabIndex"] = {}
		self._previewTabIndex = state
	@property
	def pip(self):
		self._getter_access_tracker["pip"] = {}
		return self._pip
	@pip.setter
	def pip(self, state):
		self._setter_access_tracker["pip"] = {}
		self._pip = state
	@property
	def stopOnUnmount(self):
		self._getter_access_tracker["stopOnUnmount"] = {}
		return self._stopOnUnmount
	@stopOnUnmount.setter
	def stopOnUnmount(self, state):
		self._setter_access_tracker["stopOnUnmount"] = {}
		self._stopOnUnmount = state
	@property
	def fallback(self):
		self._getter_access_tracker["fallback"] = {}
		return self._fallback
	@fallback.setter
	def fallback(self, state):
		self._setter_access_tracker["fallback"] = {}
		self._fallback = state
	@property
	def config(self):
		self._getter_access_tracker["config"] = {}
		return self._config
	@config.setter
	def config(self, state):
		self._setter_access_tracker["config"] = {}
		self._config = state

	def _to_json_fields(self):
		return {
			"playing": self._playing,
			"url": self._url,
			"light": self._light,
			"loop": self._loop,
			"controls": self._controls,
			"volume": self._volume,
			"muted": self._muted,
			"playbackRate": self._playbackRate,
			"progressInterval": self._progressInterval,
			"playsinline": self._playsinline,
			"playIcon": self._playIcon,
			"previewTabIndex": self._previewTabIndex,
			"pip": self._pip,
			"stopOnUnmount": self._stopOnUnmount,
			"fallback": self._fallback,
			"config": self._config
			}


class Video(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "Video"
		self.nodePkg = "@atrilabs/react-component-manifests"
		self.onChange = False
		self.onPressEnter = False
		self.onReady = False
		self.onStart = False
		self.onPlay = False
		self.onPause = False
		self.onBuffer = False
		self.onBufferEnd = False
		self.onEnded = False
		self.onClickPreview = False
		self.onEnablePIP = False
		self.onDisablePIP = False
		self.onError = False
		self.onDuration = False
		self.onSeek = False
		self.onProgress = False
		self.getCurrentTime = False
		self.getSecondsLoaded = False
		self.getDuration = False
		self.getInternalPlayer = False
		self.showPreview = False
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
		self._custom = VideoCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}