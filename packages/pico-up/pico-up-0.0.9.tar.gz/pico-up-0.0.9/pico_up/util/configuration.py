import configparser

from termcolor import cprint


class Configuration:
    class ConfigurationDevice:
        address = 'auto'

    class ConfigurationPush:
        ignores = []
        modules = []

    push = ConfigurationPush()
    device = ConfigurationDevice()

    def __init__(self, parsed_configuration: configparser.ConfigParser):
        # Extract device address
        try:
            self.device.address = parsed_configuration['device']['address']
        except KeyError:
            pass
        # Extract ignores
        try:
            test = parsed_configuration['push']['ignores']
            self.push.ignores = list(filter(lambda x: x != '', test.split('\n')))
        except KeyError:
            pass
        # Extract modules
        try:
            test = parsed_configuration['push']['modules']
            self.push.modules = list(filter(lambda x: x != '', test.split('\n')))
        except KeyError:
            pass


def load_configuration():
    try:
        parsed_configuration = configparser.ConfigParser()
        parsed_configuration.read('.pico-up.ini')
        return Configuration(parsed_configuration)
    except FileNotFoundError:
        cprint('no configuration file found', 'red')
        quit(100)
