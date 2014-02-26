class WebPageChangedError(Exception):
	description = 'ERROR: The structure of the web page has changed.'
	fix = 'FIX: Please update the xpaths in the source code.'

	def __init__(self, selector_name):
		self.message = (
			'ERROR: The ' +
			selector_name +
			' selector is an empty list.'
		)