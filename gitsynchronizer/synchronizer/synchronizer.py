# coding: utf-8
import logging
import os
from ConfigParser import SafeConfigParser
from datetime import datetime
from logging import Logger
from subprocess import Popen, PIPE, STDOUT

from ..context.context import Context


class Synchronizer(object):
    __slots__ = (
        "__logger",
        "__context",
        "__config",
        "__repository_count"
    )

    def __init__(self, config, context):
        # type: (SafeConfigParser, Context) -> None

        super(Synchronizer, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__config = config  # type: SafeConfigParser
        self.__context = context  # type: Context
        self.__repository_count = 0  # type: int

    def execute(self):
        # type: () -> None

        org_cwd = os.getcwd()

        if not os.path.isdir(self.__context.project_dir):
            self.__logger.debug("Make directories. -> " + self.__context.project_dir)
            os.makedirs(self.__context.project_dir)

        for self.__repository_count, repository in enumerate(self.__context.repositories):  # type: (int, str)
            repo_dir = os.path.abspath(os.path.join(self.__context.project_dir, repository))

            if not os.path.isdir(repo_dir):
                self.__logger.debug("Change directory. -> " + self.__context.project_dir)
                os.chdir(self.__context.project_dir)

                if not self._git_clone(repository):
                    continue

            self.__logger.debug("Change directory. -> " + repo_dir)
            os.chdir(repo_dir)

            if self._git_diff_with_working_directory(repository):
                if not self._git_stash_save(repository):
                    continue

            if not self._git_checkout(repository):
                continue

            if not self._git_fetch(repository):
                continue

            if not self._git_merge(repository):
                continue

            self.__context.success_repositories.append(repository)
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Succeeded synchronization.", self.__repository_count + 1,
                len(self.__context.repositories))

        os.chdir(org_cwd)

    def _git_clone(self, repository):
        # type: (str) -> bool

        uri = self.__config.get("repository", "uri").format(project=self.__context.project, repository=repository)
        command = ["git", "clone", uri]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            self.__context.fail_repositories.append(repository)
            self.__logger.error("[%s] %s" % (self._display_of(repository), "Failed git clone."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git clone.", self.__repository_count + 1,
                len(self.__context.repositories))

        return process.returncode == 0

    def _git_diff_with_working_directory(self, repository):
        # type: (str) -> bool

        command = ["git", "diff", "--exit-code", "--quiet"]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        return process.returncode == 1

    def _git_stash_save(self, repository):
        # type: (str) -> bool

        now = datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")
        stash_message = "%s saved by `git-synchronizer`." % now
        command = ["git", "stash", "save", "-u", stash_message]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            self.__context.fail_repositories.append(repository)
            self.__logger.error("[%s] %s" % (self._display_of(repository), "Failed git stash save."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git stash save.", self.__repository_count + 1,
                len(self.__context.repositories))

        self.__context.stash_repositories.append(repository)

        return process.returncode == 0

    def _git_checkout(self, repository):
        # type: (str) -> bool

        command = ["git", "checkout", "main"]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            self.__context.fail_repositories.append(repository)
            self.__logger.error("[%s] %s" % (self._display_of(repository), "Failed git checkout."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git checkout.", self.__repository_count + 1,
                len(self.__context.repositories))

        return process.returncode == 0

    def _git_fetch(self, repository):
        # type: (str) -> bool

        command = ["git", "fetch", "--all", "-pt"]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            self.__context.fail_repositories.append(repository)
            self.__logger.error("[%s] %s" % (self._display_of(repository), "Failed git fetch."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git fetch.", self.__repository_count + 1,
                len(self.__context.repositories))

        return process.returncode == 0

    def _git_merge(self, repository):
        # type: (str) -> bool

        command = ["git", "merge", "origin/main"]
        self.__logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.__context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        self.__logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            self.__context.fail_repositories.append(repository)
            self.__logger.error("[%s] %s" % (self._display_of(repository), "Failed git merge."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git merge.", self.__repository_count + 1,
                len(self.__context.repositories))

        return process.returncode == 0

    @staticmethod
    def _display_of(repository):
        # type: (str) -> str

        space = " " * (33 - len(repository.decode("utf-8")))
        return repository + space
