__author__ = 'alex'

from PyQt5 import QtGui, QtWidgets, QtCore
from AwfulGUI.AwfulThread import AwfulThreadDocker as DockingThread
from AwfulGUI.AwfulForum import AwfulForumsList, AwfulThreadList
from AwfulGUI import AwfulForum
from AwfulGUI.AwfulSlots import AwfulSlots



class AwfulIndex(QtWidgets.QMainWindow):
	def __init__(self, awful_py):
		super().__init__()
		self.awful_py = awful_py

		self.root = QtWidgets.QWidget(self)
		self.setMinimumSize(500, 500)
		self.root.setMinimumSize(500, 500)
		self.hbox_main = QtWidgets.QHBoxLayout(self.root)

		self.vbox_lists = _Vbox_Lists(awful_py)
		self.vbox_console = _Vbox_Console()

		self.size_policy = QtWidgets.QSizePolicy(
			QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

		self.organize_layout()
		self.setup_sizes()

		self.slots = AwfulSlots(self)

	def setup_sizes(self):
		self.setSizePolicy(self.size_policy)
		self.root.setSizePolicy(self.size_policy)

		self.vbox_console.setSizePolicy(self.size_policy)
		self.vbox_console.grid_threads.setSizePolicy(self.size_policy)


	def organize_layout(self):
		self.hbox_main.addWidget(self.vbox_lists)
		self.hbox_main.addWidget(self.vbox_console)



class _Gridbox_Threads(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.root = QtWidgets.QWidget(self)

		self.setMinimumSize(500, 500)
		self.layout = QtWidgets.QGridLayout(self.root)


class _Vbox_Lists(QtWidgets.QWidget):
	def __init__(self, awful_py):
		super().__init__()
		self.size_policy = QtWidgets.QSizePolicy()
		self.layout = QtWidgets.QVBoxLayout(self)

		self.list_forums = AwfulForumsList(awful_py.index)
		self.list_threads = AwfulThreadList(awful_py.index.forums['202'])

		self.setup_sizes()

		self.layout.addWidget(self.list_forums)
		self.layout.addWidget(self.list_threads)

	def setup_sizes(self):
		self.setMinimumWidth(240)
		self.setMaximumWidth(240)

		#self.list_forums.setMaximumHeight(300)
		#self.list_threads.setMaximumHeight(300)

		self.size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Maximum)
		self.size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)

		self.setSizePolicy(self.size_policy)
		self.list_forums.setSizePolicy(self.size_policy)
		self.list_threads.setSizePolicy(self.size_policy)

class _Vbox_Console(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QtWidgets.QVBoxLayout(self)
		self.grid_threads = _Gridbox_Threads()
		self.button = AwfulPost()

		self.layout.addWidget(self.grid_threads)
		self.layout.addWidget(self.button)

class AwfulPost(QtWidgets.QWidget):
	def __init__(self):
		super().__init__()
		self.setMaximumHeight(100)
		self.layout = QtWidgets.QHBoxLayout(self)
		self.text_box = QtWidgets.QPlainTextEdit(self)
		self.post_button = QtWidgets.QPushButton('Post', self)

		self.layout.addWidget(self.text_box)
		self.layout.addWidget(self.post_button)