from bottlenest.core.NestModuleContext import NestModuleContext
from bottlenest.core.NestLogger import NestLogger
import sys
import inquirer
import argparse


class CommandFactory:
    __name__ = 'CommandFactory'

    __commands__ = {}
    # __args__ = None
    # __currentCommand__ = None
    # __args__ = sys.argv[1:]
    # __module__ = None
    # __container__ = None

    @staticmethod
    def run(module):
        """This run will be called from whithin main.py"""
        # initial setup
        logger = NestLogger()
        container = CommandFactory.__buildContainer()
        container.set('module', module)
        container.set('logger', logger)
        container.set('inquirer', inquirer)
        # load module

        def __setupModuleContext(module, logger):
            moduleContext = NestModuleContext()
            moduleContext.set('module', module)
            moduleContext.set('logger', logger)
            moduleContext.module = module  # TODO: move this
            return moduleContext
        moduleContext = __setupModuleContext(
            module=module,
            logger=logger,
        )
        module.enableModule()
        # TODO: review this
        module.setupModule(
            moduleContext,
            container,
        )
        # parse initial command line arguments
        # and set __currentCommand__
        rawCommandName = sys.argv[1]
        # CommandFactory.__module__ = module
        # CommandFactory.__container__ = container
        # run command
        CommandFactory.__runCommand(container, rawCommandName)

    @staticmethod
    def __buildContainer():
        context = NestModuleContext()
        parser = argparse.ArgumentParser(
            prog="Program Name",
            description="Program Description",
            epilog="Program Epilog",
        )
        # TODO:GIOVANNEFEITOSA
        parser.add_argument("command", help="command to run")
        # parser.add_argument("args", nargs=argparse.REMAINDER)
        # augment context
        context.parser = parser
        context.inquirer = inquirer
        return context

    @staticmethod
    def __runCommand(context, commandName):
        """This runCommand will be called from whithin NestCommand"""
        print("CommandFactory runCommand ", commandName)
        # parse command line arguments
        # parser = CommandFactory.__buildParser(context)
        # help command
        if commandName == 'help':
            context.parser.print_help()
            return
        # run command
        command = CommandFactory.__commands__[commandName]
        command.parseArguments(context.parser)
        commandArgs = context.parser.parse_args()
        command.cls.run(command, context, commandArgs)

    @staticmethod
    def register(nestCommand):
        """This register will be called from whithin NestCommand"""
        print("CommandFactory register ", nestCommand.commandName)
        CommandFactory.__commands__[nestCommand.commandName] = nestCommand
