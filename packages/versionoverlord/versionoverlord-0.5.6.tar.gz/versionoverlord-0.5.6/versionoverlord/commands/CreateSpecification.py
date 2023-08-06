from logging import Logger
from logging import getLogger
from typing import Tuple
from typing import cast

from click import command
from click import option
from click import version_option

from versionoverlord.Common import __version__
from versionoverlord.Common import Slugs
from versionoverlord.Common import setUpLogging
from versionoverlord.TemplateHandler import TemplateHandler


class CreateSpecification:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s',  multiple=True, required=False, help='Create package update specification')
def commandHandler(slugs: Tuple[str]):
    """
    \b
    This command creates .csv specification file
    It uses the following environment variables:
    \b
        GITHUB_ACCESS_TOKEN - A personal GitHub access token necessary to read repository release information
        PROJECTS_BASE -  The local directory where the python projects are based
        PROJECT       -  The name of the project;  It should be a directory name
    """

    if len(slugs) != 0:
        templateHandler: TemplateHandler = TemplateHandler(slugs=cast(Slugs, slugs))
        templateHandler.createSpecification()


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
