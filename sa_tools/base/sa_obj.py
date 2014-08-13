from sa_tools.base.dynamic import DynamicMixin
from sa_tools.base.magic import MagicMixin
from sa_tools.base.descriptors import IntOrNone


class SAObj(MagicMixin, DynamicMixin):
    id = IntOrNone()
    _base_url = 'http://forums.somethingawful.com/'

    def __init__(self, parent, id=None, content=None, name=None, url=None, **properties):
        super(SAObj, self).__init__(parent, **properties)
        self.id = id
        self.session = self.parent.session
        self._content = content
        self.name = name
        self.url = url if url else self._base_url

        self.unread = True
        self._reads = 0

        self._dynamic_attr()

    def _fetch(self, url=None, params=None):
        if not url:
            url = self.url

        if not params:
            params = dict()

        response = self.session.get(url, params=params)

        if not response.ok:
            raise Exception(("There was an error with your request ",
                             url, response.status_code, response.reason))

        self._content = response.content



    def read(self, pg=1):
        """
        Call _dynamic_attr() and _delete_extra() for full
        sa_obj interop.

        If unread, call them at the end of your overridden read()
        """
        if self.unread:
            self.unread = False

        self._reads += 1

    def _apply_attr_dict(self, results, condition_map=None):
        return apply_parsed_results(self, results, condition_map)


def apply_parsed_results(parent, results, condition_map=None):
    if not condition_map:
        condition_map = dict()

    for key, val in results.items():
        if key in condition_map:
            condition_map[key](val)

        setattr(parent, key, val)