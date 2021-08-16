# coding: utf-8
import logging
import os
from datetime import datetime
from logging import Logger
from subprocess import Popen, PIPE, STDOUT

from ..context.context import Context


class Synchronizer(object):
    __slots__ = (
        "__logger",
        "__context",
        "__repository_count"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(Synchronizer, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context
        self.__repository_count = 0  # type: int

    def execute(self):
        # type: () -> None

        logger = self.__logger
        context = self.__context

        org_cwd = os.getcwd()

        if not os.path.isdir(context.project_dir):
            logger.debug("Make directories. -> " + context.project_dir)
            os.makedirs(context.project_dir)

        for self.__repository_count, repository in enumerate(context.repositories):  # type: (int, str)
            repo_dir = os.path.abspath(os.path.join(context.project_dir, repository))

            if not os.path.isdir(repo_dir):
                logger.debug("Change directory. -> " + context.project_dir)
                os.chdir(context.project_dir)

                if not self._git_clone(repository):
                    continue

            logger.debug("Change directory. -> " + repo_dir)
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

            context.success_repositories.append(repository)
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Succeeded synchronization.", self.__repository_count + 1,
                len(context.repositories))

        os.chdir(org_cwd)

    def _git_clone(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context
        config = self.__context.config

        uri = config.get("repository", "uri").format(project=context.project, repository=repository)
        command = ["git", "clone", uri]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            context.fail_repositories.append(repository)
            logger.error("[%s] %s" % (self._display_of(repository), "Failed git clone."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git clone.", self.__repository_count + 1,
                len(context.repositories))

        return process.returncode == 0

    def _git_diff_with_working_directory(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context

        command = ["git", "diff", "--exit-code", "--quiet"]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        return process.returncode == 1

    def _git_stash_save(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context

        now = datetime.today().strftime("[%Y-%m-%d %H:%M:%S]")
        stash_message = "%s saved by `git-synchronizer`." % now
        command = ["git", "stash", "save", "-u", stash_message]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            context.fail_repositories.append(repository)
            logger.error("[%s] %s" % (self._display_of(repository), "Failed git stash save."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git stash save.", self.__repository_count + 1,
                len(context.repositories))

        context.stash_repositories.append(repository)

        return process.returncode == 0

    def _git_checkout(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context

        command = ["git", "checkout", "main"]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            context.fail_repositories.append(repository)
            logger.error("[%s] %s" % (self._display_of(repository), "Failed git checkout."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git checkout.", self.__repository_count + 1,
                len(context.repositories))

        return process.returncode == 0

    def _git_fetch(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context

        command = ["git", "fetch", "--all", "-pt"]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            context.fail_repositories.append(repository)
            logger.error("[%s] %s" % (self._display_of(repository), "Failed git fetch."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git fetch.", self.__repository_count + 1,
                len(context.repositories))

        return process.returncode == 0

    def _git_merge(self, repository):
        # type: (str) -> bool

        logger = self.__logger
        context = self.__context

        command = ["git", "merge", "origin/main"]
        logger.debug("[%s] %s" % (self._display_of(repository), " ".join(command)))

        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        context.subprocesses.append(process)
        stdout = process.communicate()[0].decode("utf-8")
        logger.debug("[%s] %s" % (self._display_of(repository), stdout))

        if process.returncode != 0:
            context.fail_repositories.append(repository)
            logger.error("[%s] %s" % (self._display_of(repository), "Failed git merge."))
            print "[%s] %s - - - %s/%s" % (
                self._display_of(repository), "Failed git merge.", self.__repository_count + 1,
                len(context.repositories))

        return process.returncode == 0

    @staticmethod
    def _display_of(repository):
        # type: (str) -> str

        space = " " * (33 - len(repository.decode("utf-8")))
        return repository + space