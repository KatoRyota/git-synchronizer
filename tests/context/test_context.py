# coding: utf-8
import os
import unittest
from unittest import TestCase

import mock

from gitsynchronizer.context.context import Context


class TestContext(TestCase):

    def test_check_application_initialize(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = True
            self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), False),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), False),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), False)))

            context = Context()
            context.profile = "default"
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = None
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = ""
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "config", "default")), True),
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)))

            context = Context()
            context.profile = 1
            context.root_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer"))
            context.config_dir = os.path.abspath(
                os.path.join("git-synchronizer", "gitsynchronizer", "config", "default"))
            context.log_dir = os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log"))

            # 実行 & 検証
            actual = context.check_application_initialize()
            expected = False
            self.assertEqual(expected, actual)

    def test_check_option_parse(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.path.isfile") as isfile:
            # 前提条件
            isfile.side_effect = self._isfile_side_effect((
                (os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json")), True),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo")), True),))

            context = Context()
            context.repo_file = os.path.abspath(
                os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            context.dst_dir = os.path.abspath(os.path.join("home", "docker", "repo"))

            # 実行 & 検証
            actual = context.check_option_parse()
            expected = True
            self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.path.isfile") as isfile:
            # 前提条件
            isfile.side_effect = self._isfile_side_effect((
                (os.path.abspath(
                    os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json")), False),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo")), True),))

            context = Context()
            context.repo_file = os.path.abspath(
                os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            context.dst_dir = os.path.abspath(os.path.join("home", "docker", "repo"))

            # 実行 & 検証
            actual = context.check_option_parse()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.path.isfile") as isfile:
            # 前提条件
            isfile.side_effect = self._isfile_side_effect((
                (os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json")), True),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo")), False),))

            context = Context()
            context.repo_file = os.path.abspath(
                os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            context.dst_dir = os.path.abspath(os.path.join("home", "docker", "repo"))

            # 実行 & 検証
            actual = context.check_option_parse()
            expected = False
            self.assertEqual(expected, actual)

    def test_check_repo_file_load(self):
        # type: () -> None

        # ---- ケース1 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = True
        self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        # 前提条件
        context = Context()
        context.project = None
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.2 ----
        # 前提条件
        context = Context()
        context.project = ""
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース2.3 ----
        # 前提条件
        context = Context()
        context.project = 1
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = None
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = ""
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = 1
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース3.4 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "default_branch": "main"}]
        context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")).decode("utf-8")

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = None

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.2 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = ""

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

        # ---- ケース4.3 ----
        # 前提条件
        context = Context()
        context.project = "KatoRyota".decode("utf-8")
        context.repositories = [
            {"name": "db-client", "base_branch": "main"},
            {"name": "git-synchronizer", "base_branch": "main"}]
        context.project_dir = 1

        # 実行 & 検証
        actual = context.check_repo_file_load()
        expected = False
        self.assertEqual(expected, actual)

    def test_check_synchronize(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = True
            self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), False),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = None
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ""
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース3.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = 1
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = None
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース4.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = ""
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース4.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = 1
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース5.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = None
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース5.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ""
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース5.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = 1
            context.fail_repositories = []

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース6.1 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = None

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース6.2 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = ""

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

        # ---- ケース6.3 ----
        with mock.patch("os.path.isdir") as isdir:
            # 前提条件
            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota")), True),))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            context.subprocesses = ["subprocess_1", "subprocess_2"]
            context.stash_repositories = []
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = 1

            # 実行 & 検証
            actual = context.check_synchronize()
            expected = False
            self.assertEqual(expected, actual)

    @staticmethod
    def _isdir_side_effect(return_values):
        # type: (tuple) -> object

        def isdir(inner_path):
            # type: (str) -> bool

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] == inner_path:
                    return return_value_tuple[1]

            raise StandardError(u"引数が不正です。")

        return isdir

    @staticmethod
    def _isfile_side_effect(return_values):
        # type: (tuple) -> object

        def isfile(inner_path):
            # type: (str) -> bool

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] == inner_path:
                    return return_value_tuple[1]

            raise StandardError(u"引数が不正です。")

        return isfile


if __name__ == "__main__":
    unittest.main()
