import json
import keyboard
import PySimpleGUIQt as sg
import sys

class Diacritic:

	# primary and secondary hotkeys
	primary_hotkey = None
	secondary_hotkeys = []
	config_json = None
	current_configuration = None


	# Constructor
	def __init__(self):
		self.secondary_hotkeys = []
		self.primary = keyboard.add_hotkey('ctrl+alt', self.listenForSecondKey)

		self.refreshConfigurations()


	# refresh configurations from config.json
	def refreshConfigurations(self):
		# read the config json from the file
		f = open('config.json', encoding='utf-8')
		config_json = json.load(f)
		f.close()

		# set the current configuration to be the first one in the list
		self.current_configuration = config_json["configurations"][0]

		# if we're already listening for the second hotkey, re-apply them using the new configuration
		if len(self.secondary_hotkeys) > 0:
			self.listenForSecondKey()


	# Called after the user presses the primary hotkey, followed by a secondary hotkey
	def sendKey(self, *keys):
		# send the character preceded by backspace
		keyboard.write('\b' + ''.join(keys))

		# remove secondary hotkeys
		for hotkey in self.secondary_hotkeys:
			keyboard.remove_hotkey(hotkey)
		self.secondary_hotkeys = []


	# Called after the user presses the primary hotkey in order to register the secondary hotkeys
	def listenForSecondKey(self):
		for hotkey in self.secondary_hotkeys:
			keyboard.remove_hotkey(hotkey)

		self.secondary_hotkeys = []
		for hotkey_key in self.current_configuration["keys"].keys():
			self.secondary_hotkeys.append(keyboard.add_hotkey(hotkey_key, self.sendKey, args=self.current_configuration["keys"][hotkey_key]))


	# Create a system tray application
	def setupTrayApplication(self):
		return sg.SystemTray(menu = [
			'BLANK',
			[
				'&Refresh Config',
				'E&xit'
			]
		],
		filename=r'app.ico')


	# Handles an option from the tray menu being selected by the user
	def handleTrayMenuOption(self, option):
		if (option == "Exit"):
			sys.exit()

		elif (option == "Refresh Config"):
			self.refreshConfigurations()

		# unknown option if we've reached this point
		else:
			assert False, "Unsupported option " + option


# running standalone
if __name__ == "__main__":

	# set up the app logic
	app = Diacritic()

	# set up the tray menu
	tray = app.setupTrayApplication()

	# main application loop
	while True:
		app.handleTrayMenuOption(tray.read())