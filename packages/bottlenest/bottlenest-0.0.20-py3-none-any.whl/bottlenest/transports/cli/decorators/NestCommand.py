import inquirer
import argparse
from bottlenest.core.NestProvider import NestProvider
from bottlenest.transports.cli.decorators.NestCommandArgument import NestCommandArgument
import sys


class NestCommand(NestProvider):
    __name__ = 'NestCommand'

    def __init__(self, commandClass, moduleContext, commandName, description):
        self.commandName = commandName
        self.description = description
        self.providerClass = commandClass
        self.providerName = commandClass.__name__
        self.moduleContext = moduleContext
        # TODO: send moduleContext to gatewayClass(moduleContext)
        # conditionally
        try:
            self.provider = self.providerClass()
        except TypeError:
            self.provider = self.providerClass(moduleContext)

    def parseArguments(self, parser):
        # Adding this extra command because we are proxying
        # the command that was run
        parser.add_argument(
            'commandName',
            help="The name of the command to run",
        )
        # parsing extra params
        arguments = [ag for ag in dir(self.providerClass) if isinstance(
            getattr(self.providerClass, ag), NestCommandArgument)]
        for argumentName in arguments:
            argument = getattr(self.providerClass, argumentName)
            # print(f"argument: {argumentName} {argument}")
            if argument.optional is False:
                parser.add_argument(
                    argument.argumentName,
                    **argument.kwargs,
                    required=True,
                )
            parser.add_argument(
                argument.argumentName,
                **argument.kwargs,
            )

    # def setupProvider(self, module, context):
    #     self._setupProvider(module, context)
    #     # args = sys.argv[1:]
    #     # self.provider.run(inquirer, args)

    def listen(self, pool):
        rawCommandName = sys.argv[1]
        # only run if this is the command being run
        if rawCommandName != self.commandName:
            return

        print(f"NestCommand running command: {self.commandName}")

        def _startCommandServer():
            parser = argparse.ArgumentParser(
                description=self.description,
            )
            self.parseArguments(parser)
            args = parser.parse_args()
            self.provider.run(inquirer, args)
        pool.spawn(_startCommandServer)
