###
### Main
###
import argparse
import importlib
import logging
import os
import sys

PATH_CONSOLE = os.path.join("core","console")
PATH_LIBRARY = os.path.join("core","lib")

###
### Command class
###
class Command(object):

    ### Configure arguments
    def configure(self, parser):
        pass

    ### Execute command
    def execute(self, input, output):
        pass

###
### call module
###
def call(name, args):
    logging.debug("> %s %s" % (name, args))

    # Update module path
    sys.path.append(PATH_CONSOLE)

    # Import module
    module = importlib.import_module(name)
    command = module.Command()

    # Generate logger
    output = logging.getLogger(name)

    # Parse arguments
    parser = argparse.ArgumentParser()
    command.configure(parser)
    input = parser.parse_args(args)

    # Run main part
    command.execute(input=input, output=output)

###
### Main
###
if __name__ == "__main__":

    # Add lib module path
    sys.path.append(PATH_LIBRARY)

    #
    # Load project config
    #
    import config
    config.init()

    #
    # Configure logging
    #
    _logLevel = int( config.getOrElse("logging.level", logging.INFO) )
    _logFormat = config.getOrElse("logging.format", "[%(name)s@%(levelname)s] %(message)s")
    _logDate = config.getOrElse("logging.date", None)
    logging.basicConfig(level=_logLevel, format=_logFormat, datefmt=_logDate)

    #
    # Notify user
    # 
    logging.debug("console: %s" % PATH_CONSOLE)
    logging.debug("library: %s" % PATH_LIBRARY)

    #
    # call command
    #
    if len(sys.argv) > 1:
        module = sys.argv[1]
        args = sys.argv[2:]
    else:
        module = "help"
        args = []

    # IF module IS in simple notation.
    if module.find('.') < 0:
        module += '.main'
    
    # Call module
    call(name=module, args=args)
