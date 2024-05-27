from gpiozero import Button
from signal import pause
import datetime
import time
import subprocess

class KioskPlayer:
	def __init__(self):
		self.GPIO_PIN = 17
		self.MEDIA_PLAYER = "mplayer"
		self.MEDIA_FILE = "long-media.mp3"
		#
		self._player = None
		self._playCounter = 0
		self._running = False

	def play_file(self):
		self._playCounter = self._playCounter + 1
		self._print("Ready to play instance {}".format(self._playCounter))
		self._player = subprocess.Popen([self.MEDIA_PLAYER, self.MEDIA_FILE], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	def _print(self, message):
		now = datetime.datetime.now()
		print("[{}] {}".format(now, message))

	def isPlayerRunning(self):
		self._print("Checking if player running")
		if self._player is None:
			return False
		self._print("Poll check")
		return self._player.poll() == None

	def stop_player(self):
		self._print("Stopping player")
		self._player.stdin.write("{}\n".format("q").encode('utf-8'))
		self._player.stdin.flush()

	def run(self):
		self._running = True
		button = Button(self.GPIO_PIN, bounce_time = 0.05)
		while self._running:
			button.when_pressed = self.play_stop
			pause()

	def say_hello(self, button):
		self._print("Hello")

	def play_stop(self, button):
		if self is None :
			return
		if self.isPlayerRunning():
			self.stop_player()
		else:
			self.play_file()


if __name__ == '__main__':
	print("Starting...")
	kioskPlayer = KioskPlayer()
	kioskPlayer.run()
