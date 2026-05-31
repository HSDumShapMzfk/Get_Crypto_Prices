from PyQt6.QtWidgets import QStackedWidget


class ScreenManager:

	def __init__(self, window: MainWindow):
		self.stack = QStackedWidget()
		self.window = window
		self.window.setCentralWidget(self.stack)

		# Screens
		self.entering = APIKeyEnteringScreen()
		self.content = ContentScreen()

		self.stack.addWidget(self.entering)
		self.stack.addWidget(self.content)

	def show_entering(self):
		self.stack.setCurrentWidget(self.entering)

	def show_content(self):
		self.stack.setCurrentWidget(self.content)