from SATools.SAForum import SAForum
from SATools.SASection import SASection
from bs4 import BeautifulSoup
from collections import OrderedDict as ordered

"""
<strike>next branch will have this revamped</strike>
revamped. 80ms vs 600ms start up time? yaes.
"""

class SAIndex(object):
	def __init__(self, sa_session):
		self.session = sa_session
		self.base_url = self.session.base_url

		self.forums = ordered()
		self.listings = ordered()
		self.sections = None

		self._get_sections()

	def _save(self, section_id, sa_section):
		self.forums[section_id] = sa_section
		self.listings[section_id] = sa_section.name

	def _get_json(self):
		url = self.base_url + '/json/forumtree'
		request = self.session.get(url)
		self.content = request.content
		self.json = request.json()

	def _get_sections(self):
		self.sections = next(self.__gen_from_json())

	def __gen_from_json(self, json=None, parent=None):
		if json is None:
			json = self.json

		children = json['children']
		id = json['forumid']
		title = json['title'] if 'title' in json else 'Index'

		parent = SAForum(id, self.session, name=title, parent=parent)
		sa_children = []

		for child in children:
			for sa_child in self._gen_from_json(child, parent):
				sa_children.append(sa_child)

		parent.children = sa_children
		self._save(parent.id, parent)

		yield parent



def main():
	pass


if __name__ == "__main__":
	main()