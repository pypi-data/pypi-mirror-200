import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

DATA_FILES = [
    ('versionoverlord/resources', ['versionoverlord/resources/loggingConfiguration.json']),
]

setup(
    name="versionoverlord",
    version="0.5.6",
    author='Humberto A. Sanchez II',
    author_email='humberto.a.sanchez.ii@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='Dependency Manager',
    long_description=README,
    long_description_content_type="text/markdown",
    license=LICENSE,
    url="https://github.com/versionoverlord",
    data_files=DATA_FILES,
    packages=[
        'versionoverlord',
        'versionoverlord.circleci',
        'versionoverlord.commands',
        'versionoverlord.exceptions',
        'versionoverlord.requirements',
        'versionoverlord.resources',
        'versionoverlord.setup'
    ],
    include_package_data=True,
    install_requires=[
        'PyGithub==1.58.0',
        'click~=8.1.3',
        'hasiihelper~=0.1.0',
    ],
    entry_points={
        "console_scripts": [
            "querySlugs=versionoverlord.commands.QuerySlugs:commandHandler",
            "createSpec=versionoverlord.commands.CreateSpecification:commandHandler",
            "updateDeps=versionoverlord.commands.UpdateDependencies:commandHandler",
        ]
    },
)
