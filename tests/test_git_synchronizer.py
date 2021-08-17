# coding: utf-8
import os
import sys
import unittest
from unittest import TestCase

import mock

from gitsynchronizer.git_synchronizer import GitSynchronizer


class TestGitSynchronizer(TestCase):

    def test_execute(self):
        # type: () -> None

        before_stdin = sys.stdin
        before_stdout = sys.stdout
        before_stderr = sys.stderr

        reload(sys)
        sys.setdefaultencoding("utf-8")
        sys.stdin = before_stdin
        sys.stdout = before_stdout
        sys.stderr = before_stderr

        # ---- ケース1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("ConfigParser.RawConfigParser.read"), \
                mock.patch("ConfigParser.ConfigParser.get") as config_parser_get, \
                mock.patch("logging.config.fileConfig"), \
                mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("json.loads") as json_loads, \
                mock.patch("gitsynchronizer.context.context.Context.check_application_initialize"
                           ) as context_check_application_initialize, \
                mock.patch("gitsynchronizer.context.context.Context.check_option_parse"
                           ) as context_check_option_parse, \
                mock.patch("gitsynchronizer.context.context.Context.check_repo_file_load"
                           ) as context_check_repo_file_load, \
                mock.patch("gitsynchronizer.context.context.Context.check_synchronize") as context_check_synchronize, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer.execute") as synchronizer_execute, \
                mock.patch("gitsynchronizer.printer.printer.Printer.execute") as printer_execute:
            # 前提条件
            context_check_application_initialize.return_value = True
            context_check_option_parse.return_value = True
            context_check_repo_file_load.return_value = True
            context_check_synchronize.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect(
                (("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect(
                (("gitsynchronizer/config/default", True), ("gitsynchronizer/log", False)))

            json_loads.return_value = {
                "KatoRyota": [
                    "db-client",
                    "git-synchronizer",
                    "experimental-tools"
                ]
            }

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"
            sys.argv = ["git_synchronizer.py", "-f", "gitsynchronizer/config/default/repo-my-project.json",
                        "-d", "/home/docker/repo/"]

            # 実行
            db_client = GitSynchronizer()
            db_client.execute()
            # noinspection PyUnresolvedReferences
            context = db_client._GitSynchronizer__context

            # 検証
            actual = os.environ.get("GITSYNCHRONIZER_PROFILE")
            expected = None
            self.assertEqual(expected, actual)

            actual = os.environ.get("LOG_DIR")
            expected = "gitsynchronizer/log"
            self.assertIn(expected, actual)

            actual = os.environ.get("PYTHONIOENCODING")
            expected = "utf-8"
            self.assertEqual(expected, actual)

            actual = context.root_dir
            expected = "gitsynchronizer"
            self.assertIn(expected, actual)

            actual = context.profile
            expected = "default"
            self.assertEqual(expected, actual)

            actual = context.config_dir
            expected = "gitsynchronizer/config/default"
            self.assertIn(expected, actual)

            actual = context.log_dir
            expected = "gitsynchronizer/log"
            self.assertIn(expected, actual)

            actual = context.repo_file
            expected = os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json")
            self.assertIn(expected, actual)

            actual = context.dst_dir
            expected = os.path.join("home", "docker", "repo")
            self.assertIn(expected, actual)

            actual = context.project
            expected = "KatoRyota"
            self.assertEqual(expected, actual)

            actual = context.repositories
            expected = ["db-client", "git-synchronizer", "experimental-tools"]
            self.assertListEqual(expected, actual)

            actual = context.project_dir
            expected = os.path.join("home", "docker", "repo", "KatoRyota")
            self.assertIn(expected, actual)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_called_once()

    @staticmethod
    def _isdir_side_effect(return_values):
        # type: (tuple) -> object

        def isdir(inner_path):
            # type: (str) -> bool

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] in inner_path:
                    return return_value_tuple[1]

            raise StandardError(u"引数が不正です。")

        return isdir

    @staticmethod
    def _config_parser_get_side_effect(return_values):
        # type: (tuple) -> object

        def config_parser_get(inner_section, inner_option):
            # type: (str, str) -> str

            for return_value_tuple in return_values:  # type: tuple
                if return_value_tuple[0] == inner_section and return_value_tuple[1] == inner_option:
                    return return_value_tuple[2]

            raise StandardError(u"引数が不正です。")

        return config_parser_get


if __name__ == "__main__":
    unittest.main()
