
from logging import Logger
from logging import getLogger

from hasiihelper.SemanticVersion import SemanticVersion

from versionoverlord.Common import Slugs

from versionoverlord.DisplayVersions import DisplayVersions
from versionoverlord.DisplayVersions import SlugVersion
from versionoverlord.DisplayVersions import SlugVersions
from versionoverlord.GitHubAdapter import GitHubAdapter

from versionoverlord.exceptions.NoGitHubAccessTokenException import NoGitHubAccessTokenException
from versionoverlord.exceptions.UnknownGitHubRepositoryException import UnknownGitHubRepositoryException


class SlugHandler:
    def __init__(self, slugs: Slugs):

        self.logger: Logger = getLogger(__name__)
        self._slugs: Slugs  = slugs

    def handleSlugs(self):
        try:
            gitHubAdapter: GitHubAdapter = GitHubAdapter()

            slugVersions: SlugVersions = SlugVersions([])
            for slug in self._slugs:
                version: SemanticVersion = gitHubAdapter.getLatestVersionNumber(slug)
                slugVersion: SlugVersion = SlugVersion(slug=slug, version=str(version))
                slugVersions.append(slugVersion)

            displayVersions: DisplayVersions = DisplayVersions()
            displayVersions.displaySlugs(slugVersions=slugVersions)
        except NoGitHubAccessTokenException:
            print(f'Your must provide a GitHub access token via the environment variable `GITHUB_ACCESS_TOKEN`')
        except UnknownGitHubRepositoryException as e:
            print(f'Unknown GitHub Repository: `{e.repositorySlug}`')
        except (ValueError, Exception) as e:
            print(f'{e}')
