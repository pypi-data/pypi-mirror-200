import py_compile
from bottlenest.transports.cli import Command, CommandArgument


@Command(
    name="build",
    description="Generates a build of the project",
)
class BuildCoreCommand:
    __name__ = 'BuildCoreCommand'

    def __init__(self, context):
        self.context = context

    def run(self, context, args):
        print(f"{self.__name__}.run:")
        print(f"{args.path} --> {args.output}")
        py_compile.compile(args.path, args.output)

    @CommandArgument(
        name="--path",
        dest="path",
        help="The path to the file to compile",
        default="examples/clitool/main.py",
        optional=True,
    )
    def pathArg(self, value):
        return value

    @CommandArgument(
        name="--output",
        dest="output",
        help="The output file",
        default="compiled.pyc",
        optional=True,
    )
    def outputArg(self, value):
        return value
