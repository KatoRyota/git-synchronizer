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
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)
            ))

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
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)
            ))

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
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), True)
            ))

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
                (os.path.abspath(os.path.join("git-synchronizer", "gitsynchronizer", "log")), False)
            ))

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

    def test_check_option_parse(self):
        self.fail()

    def test_check_repo_file_load(self):
        self.fail()

    def test_check_synchronize(self):
        self.fail()

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


if __name__ == "__main__":
    unittest.main()
