import json
import keyboard
import PySimpleGUIQt as sg
import sys

class Diacritic:

	CHECKMARK_PREFIX = "✓ "

	# primary and secondary hotkeys
	primary_hotkey = None
	secondary_hotkeys = []
	config_json = None
	current_configuration_name = None
	sys_tray = None


	# Constructor
	def __init__(self):
		self.secondary_hotkeys = []
		self.primary = keyboard.add_hotkey('ctrl+alt', self.listenForSecondKey)

		self.refreshConfigurations()


	# refresh configurations from config.json
	def refreshConfigurations(self):
		# read the config json from the file
		f = open('config.json', encoding='utf-8')
		self.config_json = json.load(f)
		f.close()

		# set the current configuration to be the first one in the list (if we don't already have one or it no longer exists in the config data)
		if self.current_configuration_name == None or self.getConfigByName(self.current_configuration_name) == None:
			self.current_configuration_name = self.config_json["configurations"][0]["name"]

		# update the configurations listed in the system tray (if the system tray has already been configured)
		if self.sys_tray != None:
			self.sys_tray.update(menu = self.constructSysTrayMenuOptions())

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
		current_configuration = self.getConfigByName(self.current_configuration_name)
		for hotkey_key in current_configuration["keys"].keys():
			self.secondary_hotkeys.append(keyboard.add_hotkey(hotkey_key, self.sendKey, args=current_configuration["keys"][hotkey_key]))


	# Create a system tray application
	def setupTrayApplication(self):
		self.sys_tray = sg.SystemTray(menu = self.constructSysTrayMenuOptions(), filename=r'app.ico')
		return self.sys_tray


	# Handles an option from the tray menu being selected by the user
	def handleTrayMenuOption(self, option):
		if (option == "Exit"):
			sys.exit()

		elif (option == "Reload Configurations"):
			self.refreshConfigurations()

		else:
			# this might be a configuration name being selected. Make sure to strip out the checkmark first...
			config_name = option.replace(self.CHECKMARK_PREFIX, "")
			
			# get the configuration by the name we were given
			config = self.getConfigByName(config_name)

			# if we managed to retrieve the configuration by its name
			if config != None:
				# store its name as our current configuration
				self.current_configuration_name = config_name

				# refresh the tray menu
				if self.sys_tray != None:
					self.sys_tray.update(menu = self.constructSysTrayMenuOptions())

			# we did not find a configuration with the given name...
			else:
				assert False, "Unsupported option " + option


	# Constructs a menu configuration for the sys tray
	def constructSysTrayMenuOptions(self):
		configurations = []
		if self.config_json != None:
			for config in self.config_json["configurations"]:
				if config["name"] == self.current_configuration_name:
					configurations.append(self.CHECKMARK_PREFIX + config["name"])
				else:
					configurations.append(config["name"])

		return [
			'BLANK',
			[
				"Configurations",
				[
					configurations
				],
				'&Reload Configurations',
				'E&xit'
			]
		]

	
	# Gets the specified configuration by name
	def getConfigByName(self, config_name):
		for config in self.config_json["configurations"]:
			if config["name"] == config_name:
				return config

		# if we couldn't find the configuration, throw an assert
		assert False, "Unknown configuration " + self.current_configuration_name + " was requested"


# running standalone
if __name__ == "__main__":

	# set up the app logic
	app = Diacritic()

	# set up the tray menu
	tray = app.setupTrayApplication()

	# main application loop
	while True:
		app.handleTrayMenuOption(tray.read())