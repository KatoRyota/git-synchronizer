# coding: utf-8
import logging
import os
from logging import Logger


class Context(object):
    __slots__ = (
        "__logger",
        "subprocesses",
        "repo_file",
        "dst_dir",
        "project_dir",
        "project",
        "repositories",
        "stash_repositories",
        "success_repositories",
        "fail_repositories"
    )

    def __init__(self):
        # type: () -> None

        super(Context, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.subprocesses = []  # type: list
        self.repo_file = ""  # type: str
        self.dst_dir = ""  # type: str
        self.project_dir = u""  # type: unicode
        self.project = u""  # type: unicode
        self.repositories = []  # type: list
        self.stash_repositories = []  # type: list
        self.success_repositories = []  # type: list
        self.fail_repositories = []  # type: list

    def check_state_after_parse_option(self):
        # type: () -> bool

        if not os.path.isfile(self.repo_file):
            return False
        if type(self.repo_file) is not str:
            return False

        if not os.path.isdir(self.dst_dir):
            return False
        if type(self.dst_dir) is not str:
            return False

        return True

    def check_state_after_load_repo_file(self):
        # type: () -> bool

        if not self.project:
            return False
        if type(self.project) is not unicode:
            return False

        if not self.repositories:
            return False
        if type(self.repositories) is not list:
            return False

        if not self.project_dir:
            return False
        if type(self.project_dir) is not unicode:
            return False

        return True

    def check_state_after_synchronize(self):
        # type: () -> bool

        if type(self.subprocesses) is not list:
            return False

        if type(self.stash_repositories) is not list:
            return False

        if type(self.success_repositories) is not list:
            return False

        if type(self.fail_repositories) is not list:
            return False

        return True
