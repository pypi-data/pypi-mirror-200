
from typing import cast
from typing import Tuple

from click import clear
from click import command
from click import option
from click import version_option

from versionoverlord.Common import setUpLogging
from versionoverlord.Common import __version__

from versionoverlord.SlugHandler import SlugHandler
from versionoverlord.SlugHandler import Slugs


@command()
@version_option(version=f'{__version__}', message='%(version)s')
@option('--slugs', '-s',  multiple=True, required=False, help='GitHub slugs to query')
def commandHandler(slugs: Tuple[str]):
    """
        \b
        This command reads the repository for each input slug and displays
        their latest release version

        It uses the following environment variables:

        \b
        GITHUB_ACCESS_TOKEN - A personal GitHub access token necessary to read repository
                              release information
    """
    slugHandler: SlugHandler = SlugHandler(slugs=cast(Slugs, slugs))
    slugHandler.handleSlugs()


if __name__ == "__main__":
    setUpLogging()
    commandHandler()
