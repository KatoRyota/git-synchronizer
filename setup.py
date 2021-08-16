# coding: utf-8
from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name="git-synchronizer",
    version="0.0.1",
    description="git-synchronizer",
    url="https://github.com/KatoRyota/git-synchronizer",
    license="",
    long_description="",
    keywords="",
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    author="Kato Ryota",
    author_email="example@com",
    packages=find_packages(include=('gitsynchronizer', 'gitsynchronizer.*')),
    include_package_data=True,
    install_requires=install_requirements,
    entry_points={
        "console_scripts": [
            "gitsynchronizer=gitsynchronizer.git_synchronizer:GitSynchronizer.main",
        ]
    },
    test_suite="tests",
)
