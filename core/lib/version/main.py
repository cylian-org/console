import config
from console import Command

### Constants
CONFIG_VERSION = 'console.version'

### Command
class Command(Command):

    def configure(self, parser):
        self._version = config.get(CONFIG_VERSION)

    def execute(self, input, output):
        output.info("Console v%s" % self._version)