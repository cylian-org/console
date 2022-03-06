#!/usr/bin/env python3
import argparse
import importlib
import logging
import os
import sys

###
### Constants
###

### Config
CONSOLE_CONFIG_BASE_KEY = 'CONSOLE__BASE'

### System
CONSOLE_SYSTEM_BASE = os.getenv(CONSOLE_CONFIG_BASE_KEY, os.path.dirname(sys.argv[0]))
CONSOLE_SYSTEM_PATH = [
    os.path.abspath(os.path.join('console')),
    os.path.abspath(os.path.join(CONSOLE_SYSTEM_BASE,'core','lib')),
]

### Logging
CONSOLE_LOGGING_LEVEL_KEY = 'logging.level'
CONSOLE_LOGGING_LEVEL_DEF = logging.INFO
CONSOLE_LOGGING_FORMAT_KEY = 'logging.format'
CONSOLE_LOGGING_FORMAT_DEF = '[%(name)s@%(levelname)s] %(message)s'
CONSOLE_LOGGING_DATE_KEY = 'logging.date'
CONSOLE_LOGGING_DATE_DEF = None

### Module
CONSOLE_MODULE_DEFAULT_SEPARATOR = '.'
CONSOLE_MODULE_DEFAULT_SUFFIX = CONSOLE_MODULE_DEFAULT_SEPARATOR + 'main'
CONSOLE_MODULE_DEFAULT_CMD = 'help' + CONSOLE_MODULE_DEFAULT_SUFFIX
CONSOLE_MODULE_DEFAULT_ARG = []

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

    # Update system path
    for path in CONSOLE_SYSTEM_PATH:
        if os.path.isdir(path):
            sys.path.append(path)

    ### Load project config
    import config
    config.init()

    ### Configure logging
    _logLevel = int( config.getOrElse(CONSOLE_LOGGING_LEVEL_KEY, CONSOLE_LOGGING_LEVEL_DEF) )
    _logFormat = config.getOrElse(CONSOLE_LOGGING_FORMAT_KEY, CONSOLE_LOGGING_FORMAT_DEF)
    _logDate = config.getOrElse(CONSOLE_LOGGING_DATE_KEY, CONSOLE_LOGGING_DATE_DEF)
    logging.basicConfig(level=_logLevel, format=_logFormat, datefmt=_logDate)

    ### Notify user
    if logging.getLogger().isEnabledFor(logging.DEBUG):

        # Dump library path
        logging.debug("Python library path:")
        for path in sys.path:
            logging.debug("- %s" % path)

        # Dump config
        logging.debug("Console config:")
        config.dump()

    #
    # call command
    #
    if len(sys.argv) > 1:
        module = sys.argv[1]
        args = sys.argv[2:]
    else:
        module = CONSOLE_MODULE_DEFAULT_CMD
        args = CONSOLE_MODULE_DEFAULT_ARG

    # IF module IS in simple notation.
    if module.find(CONSOLE_MODULE_DEFAULT_SEPARATOR) < 0:
        module += CONSOLE_MODULE_DEFAULT_SUFFIX
    
    # Call module
    call(name=module, args=args)
