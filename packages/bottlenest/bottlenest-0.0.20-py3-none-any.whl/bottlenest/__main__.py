from bottlenest.common import Module
from bottlenest.transports.cli import CommandFactory
from bottlenest.corecommands.NewCoreCommand import NewCoreCommand
from bottlenest.corecommands.BuildCoreCommand import BuildCoreCommand


@Module(
    providers=[NewCoreCommand, BuildCoreCommand],
)
class CoreCliModule:
    pass


def main():
    CommandFactory.run(CoreCliModule)


if __name__ == "__main__":
    main()
