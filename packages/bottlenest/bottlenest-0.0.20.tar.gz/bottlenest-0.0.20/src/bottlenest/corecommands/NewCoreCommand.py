from bottlenest.transports.cli import Command, CommandArgument
from bottlenest.utils.FileUtils import FileUtils


@Command(
    name="new",
    description="Create a new project",
)
class NewCoreCommand:
    __name__ = 'NewCoreCommand'

    # context is the provider Context
    def __init__(self, context):
        self.context = context

    def run(self, context, args):
        print(
            f"Creating project '{args.name}' from template '{args.template}'...")
        exampleFolder = f"templates/{args.template}"
        # copy exampleFolder to current folder
        FileUtils.copyDir(FileUtils.absPath(exampleFolder), f"./{args.name}")
        print(f"Project '{args.name}' created!")

    @CommandArgument(
        name="name",
        help="Project name",
        optional=True,
    )
    def nameArg(self, value):
        return value

    @CommandArgument(
        name="--template",
        dest="template",
        help="The template to use",
        default="helloworld",
        optional=True,
    )
    def templateArg(self, value):
        return value
