class GorseAPI(object):
	"""docstring for GorseAPI"""
	def __init__(
		self,
		*,
		debug: bool = False,
		title: str = "GorseAPI",
		description: str = "",
		version: str = "0.1.0"
		) -> None:
		self.debug = debug
		self.title = title
		self.description = description
		self.version = version
		