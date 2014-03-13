from bs4 import BeautifulSoup

class SAObj(object):
	def __init__(self, id=None, session=None, content=None, parent=None,
	             name=None, url=None, **properties):
		super(SAObj, self).__init__()
		self.content = content
		self.session = session
		self.id = id
		self.name = name
		self.parent = parent

		self.unread = True
		self.url = url
		self.base_url = ""

		self.__dont_rely_on_this(properties)

	def read(self, pg=1):
		if self.unread:
			self.unread = False

	def __dont_rely_on_this(self, properties):
		""""This will be factored out"""
		for name, attr in properties.items():
			if name in self.__dict__:
				setattr(self, name, attr)


class SAListObj(SAObj):
	def __init__(self, *args, **properties):
		super(SAListObj, self).__init__(*args, **properties)
		self.page = None
		self.pages = None
		self.navi = None
		self.children = None

		self._collection = None
		self._content = None

	def read(self, pg=1):
		super(SAListObj, self).read(pg)

		url = self.url + '&pagenumber=' + str(pg)
		request = self.session.get(url)
		self._content = BeautifulSoup(request.text)

		if not self.navi:
			navi = self._content.find('div', 'pages')
			self.navi = SAPageNav(content=navi, parent=self)

		self.navi.read(pg)


class SAPageNav(SAObj):
	def __init__(self, **properties):
		super(SAPageNav, self).__init__(**properties)
		self.page = 1
		self.pages = 1

	def read(self, pg=1):
		super(SAPageNav, self).read(pg)
		self.page = pg
		page_selector = self.content.find_all('option')
		if len(page_selector):
			self.pages = page_selector[-1].text
		else:
			self.pages = 1

		self._modify_parent()

	def _modify_parent(self):
		self.parent.page = self.page
		self.parent.pages = self.pages

