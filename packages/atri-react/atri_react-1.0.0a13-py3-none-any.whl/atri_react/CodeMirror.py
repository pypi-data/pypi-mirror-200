from typing import Any, Union
from atri_core import AtriComponent



class CodeMirrorCustomClass():
	def __init__(self, state: Union[Any, None]):
		self._setter_access_tracker = {}
		
		self.extensions: Union[Any, None] = state["extensions"] if state != None and "extensions" in state else None
		self.value: Union[Any, None] = state["value"] if state != None and "value" in state else None
		self.theme: Union[Any, None] = state["theme"] if state != None and "theme" in state else None
		self.autoFocus: Union[Any, None] = state["autoFocus"] if state != None and "autoFocus" in state else None
		self.editable: Union[Any, None] = state["editable"] if state != None and "editable" in state else None
		self.placeholder: Union[Any, None] = state["placeholder"] if state != None and "placeholder" in state else None
		self.lineNumbers: Union[Any, None] = state["lineNumbers"] if state != None and "lineNumbers" in state else None
		self.highlightActiveLineGutter: Union[Any, None] = state["highlightActiveLineGutter"] if state != None and "highlightActiveLineGutter" in state else None
		self.highlightSpecialChars: Union[Any, None] = state["highlightSpecialChars"] if state != None and "highlightSpecialChars" in state else None
		self.history: Union[Any, None] = state["history"] if state != None and "history" in state else None
		self.foldGutter: Union[Any, None] = state["foldGutter"] if state != None and "foldGutter" in state else None
		self.drawSelection: Union[Any, None] = state["drawSelection"] if state != None and "drawSelection" in state else None
		self.dropCursor: Union[Any, None] = state["dropCursor"] if state != None and "dropCursor" in state else None
		self.allowMultipleSelections: Union[Any, None] = state["allowMultipleSelections"] if state != None and "allowMultipleSelections" in state else None
		self.indentOnInput: Union[Any, None] = state["indentOnInput"] if state != None and "indentOnInput" in state else None
		self.syntaxHighlighting: Union[Any, None] = state["syntaxHighlighting"] if state != None and "syntaxHighlighting" in state else None
		self.bracketMatching: Union[Any, None] = state["bracketMatching"] if state != None and "bracketMatching" in state else None
		self.closeBrackets: Union[Any, None] = state["closeBrackets"] if state != None and "closeBrackets" in state else None
		self.autocompletion: Union[Any, None] = state["autocompletion"] if state != None and "autocompletion" in state else None
		self.rectangularSelection: Union[Any, None] = state["rectangularSelection"] if state != None and "rectangularSelection" in state else None
		self.crosshairCursor: Union[Any, None] = state["crosshairCursor"] if state != None and "crosshairCursor" in state else None
		self.highlightActiveLine: Union[Any, None] = state["highlightActiveLine"] if state != None and "highlightActiveLine" in state else None
		self.highlightSelectionMatches: Union[Any, None] = state["highlightSelectionMatches"] if state != None and "highlightSelectionMatches" in state else None
		self.closeBracketsKeymap: Union[Any, None] = state["closeBracketsKeymap"] if state != None and "closeBracketsKeymap" in state else None
		self.defaultKeymap: Union[Any, None] = state["defaultKeymap"] if state != None and "defaultKeymap" in state else None
		self.searchKeymap: Union[Any, None] = state["searchKeymap"] if state != None and "searchKeymap" in state else None
		self.historyKeymap: Union[Any, None] = state["historyKeymap"] if state != None and "historyKeymap" in state else None
		self.foldKeymap: Union[Any, None] = state["foldKeymap"] if state != None and "foldKeymap" in state else None
		self.completionKeymap: Union[Any, None] = state["completionKeymap"] if state != None and "completionKeymap" in state else None
		self.lintKeymap: Union[Any, None] = state["lintKeymap"] if state != None and "lintKeymap" in state else None
		self._setter_access_tracker = {}
		self._getter_access_tracker = {}

	@property
	def extensions(self):
		self._getter_access_tracker["extensions"] = {}
		return self._extensions
	@extensions.setter
	def extensions(self, state):
		self._setter_access_tracker["extensions"] = {}
		self._extensions = state
	@property
	def value(self):
		self._getter_access_tracker["value"] = {}
		return self._value
	@value.setter
	def value(self, state):
		self._setter_access_tracker["value"] = {}
		self._value = state
	@property
	def theme(self):
		self._getter_access_tracker["theme"] = {}
		return self._theme
	@theme.setter
	def theme(self, state):
		self._setter_access_tracker["theme"] = {}
		self._theme = state
	@property
	def autoFocus(self):
		self._getter_access_tracker["autoFocus"] = {}
		return self._autoFocus
	@autoFocus.setter
	def autoFocus(self, state):
		self._setter_access_tracker["autoFocus"] = {}
		self._autoFocus = state
	@property
	def editable(self):
		self._getter_access_tracker["editable"] = {}
		return self._editable
	@editable.setter
	def editable(self, state):
		self._setter_access_tracker["editable"] = {}
		self._editable = state
	@property
	def placeholder(self):
		self._getter_access_tracker["placeholder"] = {}
		return self._placeholder
	@placeholder.setter
	def placeholder(self, state):
		self._setter_access_tracker["placeholder"] = {}
		self._placeholder = state
	@property
	def lineNumbers(self):
		self._getter_access_tracker["lineNumbers"] = {}
		return self._lineNumbers
	@lineNumbers.setter
	def lineNumbers(self, state):
		self._setter_access_tracker["lineNumbers"] = {}
		self._lineNumbers = state
	@property
	def highlightActiveLineGutter(self):
		self._getter_access_tracker["highlightActiveLineGutter"] = {}
		return self._highlightActiveLineGutter
	@highlightActiveLineGutter.setter
	def highlightActiveLineGutter(self, state):
		self._setter_access_tracker["highlightActiveLineGutter"] = {}
		self._highlightActiveLineGutter = state
	@property
	def highlightSpecialChars(self):
		self._getter_access_tracker["highlightSpecialChars"] = {}
		return self._highlightSpecialChars
	@highlightSpecialChars.setter
	def highlightSpecialChars(self, state):
		self._setter_access_tracker["highlightSpecialChars"] = {}
		self._highlightSpecialChars = state
	@property
	def history(self):
		self._getter_access_tracker["history"] = {}
		return self._history
	@history.setter
	def history(self, state):
		self._setter_access_tracker["history"] = {}
		self._history = state
	@property
	def foldGutter(self):
		self._getter_access_tracker["foldGutter"] = {}
		return self._foldGutter
	@foldGutter.setter
	def foldGutter(self, state):
		self._setter_access_tracker["foldGutter"] = {}
		self._foldGutter = state
	@property
	def drawSelection(self):
		self._getter_access_tracker["drawSelection"] = {}
		return self._drawSelection
	@drawSelection.setter
	def drawSelection(self, state):
		self._setter_access_tracker["drawSelection"] = {}
		self._drawSelection = state
	@property
	def dropCursor(self):
		self._getter_access_tracker["dropCursor"] = {}
		return self._dropCursor
	@dropCursor.setter
	def dropCursor(self, state):
		self._setter_access_tracker["dropCursor"] = {}
		self._dropCursor = state
	@property
	def allowMultipleSelections(self):
		self._getter_access_tracker["allowMultipleSelections"] = {}
		return self._allowMultipleSelections
	@allowMultipleSelections.setter
	def allowMultipleSelections(self, state):
		self._setter_access_tracker["allowMultipleSelections"] = {}
		self._allowMultipleSelections = state
	@property
	def indentOnInput(self):
		self._getter_access_tracker["indentOnInput"] = {}
		return self._indentOnInput
	@indentOnInput.setter
	def indentOnInput(self, state):
		self._setter_access_tracker["indentOnInput"] = {}
		self._indentOnInput = state
	@property
	def syntaxHighlighting(self):
		self._getter_access_tracker["syntaxHighlighting"] = {}
		return self._syntaxHighlighting
	@syntaxHighlighting.setter
	def syntaxHighlighting(self, state):
		self._setter_access_tracker["syntaxHighlighting"] = {}
		self._syntaxHighlighting = state
	@property
	def bracketMatching(self):
		self._getter_access_tracker["bracketMatching"] = {}
		return self._bracketMatching
	@bracketMatching.setter
	def bracketMatching(self, state):
		self._setter_access_tracker["bracketMatching"] = {}
		self._bracketMatching = state
	@property
	def closeBrackets(self):
		self._getter_access_tracker["closeBrackets"] = {}
		return self._closeBrackets
	@closeBrackets.setter
	def closeBrackets(self, state):
		self._setter_access_tracker["closeBrackets"] = {}
		self._closeBrackets = state
	@property
	def autocompletion(self):
		self._getter_access_tracker["autocompletion"] = {}
		return self._autocompletion
	@autocompletion.setter
	def autocompletion(self, state):
		self._setter_access_tracker["autocompletion"] = {}
		self._autocompletion = state
	@property
	def rectangularSelection(self):
		self._getter_access_tracker["rectangularSelection"] = {}
		return self._rectangularSelection
	@rectangularSelection.setter
	def rectangularSelection(self, state):
		self._setter_access_tracker["rectangularSelection"] = {}
		self._rectangularSelection = state
	@property
	def crosshairCursor(self):
		self._getter_access_tracker["crosshairCursor"] = {}
		return self._crosshairCursor
	@crosshairCursor.setter
	def crosshairCursor(self, state):
		self._setter_access_tracker["crosshairCursor"] = {}
		self._crosshairCursor = state
	@property
	def highlightActiveLine(self):
		self._getter_access_tracker["highlightActiveLine"] = {}
		return self._highlightActiveLine
	@highlightActiveLine.setter
	def highlightActiveLine(self, state):
		self._setter_access_tracker["highlightActiveLine"] = {}
		self._highlightActiveLine = state
	@property
	def highlightSelectionMatches(self):
		self._getter_access_tracker["highlightSelectionMatches"] = {}
		return self._highlightSelectionMatches
	@highlightSelectionMatches.setter
	def highlightSelectionMatches(self, state):
		self._setter_access_tracker["highlightSelectionMatches"] = {}
		self._highlightSelectionMatches = state
	@property
	def closeBracketsKeymap(self):
		self._getter_access_tracker["closeBracketsKeymap"] = {}
		return self._closeBracketsKeymap
	@closeBracketsKeymap.setter
	def closeBracketsKeymap(self, state):
		self._setter_access_tracker["closeBracketsKeymap"] = {}
		self._closeBracketsKeymap = state
	@property
	def defaultKeymap(self):
		self._getter_access_tracker["defaultKeymap"] = {}
		return self._defaultKeymap
	@defaultKeymap.setter
	def defaultKeymap(self, state):
		self._setter_access_tracker["defaultKeymap"] = {}
		self._defaultKeymap = state
	@property
	def searchKeymap(self):
		self._getter_access_tracker["searchKeymap"] = {}
		return self._searchKeymap
	@searchKeymap.setter
	def searchKeymap(self, state):
		self._setter_access_tracker["searchKeymap"] = {}
		self._searchKeymap = state
	@property
	def historyKeymap(self):
		self._getter_access_tracker["historyKeymap"] = {}
		return self._historyKeymap
	@historyKeymap.setter
	def historyKeymap(self, state):
		self._setter_access_tracker["historyKeymap"] = {}
		self._historyKeymap = state
	@property
	def foldKeymap(self):
		self._getter_access_tracker["foldKeymap"] = {}
		return self._foldKeymap
	@foldKeymap.setter
	def foldKeymap(self, state):
		self._setter_access_tracker["foldKeymap"] = {}
		self._foldKeymap = state
	@property
	def completionKeymap(self):
		self._getter_access_tracker["completionKeymap"] = {}
		return self._completionKeymap
	@completionKeymap.setter
	def completionKeymap(self, state):
		self._setter_access_tracker["completionKeymap"] = {}
		self._completionKeymap = state
	@property
	def lintKeymap(self):
		self._getter_access_tracker["lintKeymap"] = {}
		return self._lintKeymap
	@lintKeymap.setter
	def lintKeymap(self, state):
		self._setter_access_tracker["lintKeymap"] = {}
		self._lintKeymap = state

	def _to_json_fields(self):
		return {
			"extensions": self._extensions,
			"value": self._value,
			"theme": self._theme,
			"autoFocus": self._autoFocus,
			"editable": self._editable,
			"placeholder": self._placeholder,
			"lineNumbers": self._lineNumbers,
			"highlightActiveLineGutter": self._highlightActiveLineGutter,
			"highlightSpecialChars": self._highlightSpecialChars,
			"history": self._history,
			"foldGutter": self._foldGutter,
			"drawSelection": self._drawSelection,
			"dropCursor": self._dropCursor,
			"allowMultipleSelections": self._allowMultipleSelections,
			"indentOnInput": self._indentOnInput,
			"syntaxHighlighting": self._syntaxHighlighting,
			"bracketMatching": self._bracketMatching,
			"closeBrackets": self._closeBrackets,
			"autocompletion": self._autocompletion,
			"rectangularSelection": self._rectangularSelection,
			"crosshairCursor": self._crosshairCursor,
			"highlightActiveLine": self._highlightActiveLine,
			"highlightSelectionMatches": self._highlightSelectionMatches,
			"closeBracketsKeymap": self._closeBracketsKeymap,
			"defaultKeymap": self._defaultKeymap,
			"searchKeymap": self._searchKeymap,
			"historyKeymap": self._historyKeymap,
			"foldKeymap": self._foldKeymap,
			"completionKeymap": self._completionKeymap,
			"lintKeymap": self._lintKeymap
			}


class CodeMirror(AtriComponent):
	def __init__(self, state: Union[Any, None]):
		super().__init__(state)
		self._setter_access_tracker = {}
		
		self.compKey = "CodeMirror"
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
		self._custom = CodeMirrorCustomClass(state)

	def _to_json_fields(self):
		return {
			"styles": self._styles,
			"custom": self._custom,
			}