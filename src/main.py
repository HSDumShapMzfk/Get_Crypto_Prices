import asyncio
import sys
from PyQt6.QtWidgets import QApplication
from qasync import QEventLoop

from src.application.factory import ApplicationFactory

async def main():
	app = QApplication(sys.argv)
	window = ApplicationFactory().build()
	window.show()

	# Connection of async event loop to the Qt event loop
	loop = QEventLoop(app)
	asyncio.set_event_loop(loop)
	with loop: 
		loop.run_forever()

if __name__ == "__main__":
	asyncio.run(main())