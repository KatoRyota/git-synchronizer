# coding: utf-8
import logging
import os
from ConfigParser import SafeConfigParser
from logging import Logger


class Context(object):
    __slots__ = (
        "__logger",
        "config",
        "root_dir",
        "profile",
        "config_dir",
        "log_dir",
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
        self.config = SafeConfigParser()  # type: SafeConfigParser
        self.root_dir = ""  # type: str
        self.profile = ""  # type: str
        self.config_dir = ""  # type: str
        self.log_dir = ""  # type: str
        self.subprocesses = []  # type: list
        self.repo_file = ""  # type: str
        self.dst_dir = ""  # type: str
        self.project_dir = u""  # type: unicode
        self.project = u""  # type: unicode
        self.repositories = []  # type: list
        self.stash_repositories = []  # type: list
        self.success_repositories = []  # type: list
        self.fail_repositories = []  # type: list

    def check_application_initialize(self):
        # type: () -> bool

        if not isinstance(self.config, SafeConfigParser):
            return False

        if not self.root_dir:
            return False
        if type(self.root_dir) is not str:
            return False
        if not os.path.isdir(self.root_dir):
            return False

        if not self.profile:
            return False
        if type(self.profile) is not str:
            return False

        if not self.config_dir:
            return False
        if type(self.config_dir) is not str:
            return False
        if not os.path.isdir(self.config_dir):
            return False

        if not self.log_dir:
            return False
        if type(self.log_dir) is not str:
            return False
        if not os.path.isdir(self.log_dir):
            return False

        return True

    def check_option_parse(self):
        # type: () -> bool

        if not self.repo_file:
            return False
        if type(self.repo_file) is not str:
            return False
        if not os.path.isfile(self.repo_file):
            return False

        if not self.dst_dir:
            return False
        if type(self.dst_dir) is not str:
            return False
        if not os.path.isdir(self.dst_dir):
            return False

        return True

    def check_repo_file_load(self):
        # type: () -> bool

        if not self.project:
            return False
        if type(self.project) is not unicode:
            return False

        if not self.repositories:
            return False
        if type(self.repositories) is not list:
            return False

        for repository in self.repositories:  # type: dict
            if not repository.get("name"):
                return False
            if not repository.get("base_branch"):
                return False

        if not self.project_dir:
            return False
        if type(self.project_dir) is not unicode:
            return False

        return True

    def check_synchronize(self):
        # type: () -> bool

        if not os.path.isdir(self.project_dir):
            return False

        if type(self.subprocesses) is not list:
            return False

        if type(self.stash_repositories) is not list:
            return False

        if type(self.success_repositories) is not list:
            return False

        if type(self.fail_repositories) is not list:
            return False

        return True
