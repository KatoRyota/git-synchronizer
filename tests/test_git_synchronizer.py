# coding: utf-8
import os
import sys
import unittest
from io import BytesIO
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

        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        # ---- ケース1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            git_synchronizer = GitSynchronizer()
            git_synchronizer.execute()
            # noinspection PyUnresolvedReferences
            context = git_synchronizer._GitSynchronizer__context

            # 検証
            actual = os.environ.get("GITSYNCHRONIZER_PROFILE")
            expected = None
            self.assertEqual(expected, actual)

            actual = os.environ.get("LOG_DIR")
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = os.environ.get("PYTHONIOENCODING")
            expected = "utf-8"
            self.assertEqual(expected, actual)

            actual = context.root_dir
            expected = os.path.join(root_dir, "gitsynchronizer")
            self.assertEqual(expected, actual)

            actual = context.profile
            expected = "default"
            self.assertEqual(expected, actual)

            actual = context.config_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "config", "default")
            self.assertEqual(expected, actual)

            actual = context.log_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = context.repo_file
            expected = os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            self.assertEqual(expected, actual)

            actual = context.dst_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo"))
            self.assertEqual(expected, actual)

            actual = context.project
            expected = "KatoRyota"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("name")
            expected = "git-synchronizer"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("base_branch")
            expected = "main"
            self.assertEqual(expected, actual)

            actual = context.project_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            self.assertEqual(expected, actual)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_called_once()

        # ---- ケース2.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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
            context_check_application_initialize.return_value = False
            context_check_option_parse.return_value = True
            context_check_repo_file_load.return_value = True
            context_check_synchronize.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(StandardError) as e:
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = e.exception.message
            expected = u"アプリケーションの初期化処理に失敗しました。"
            self.assertEqual(expected, actual)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_not_called()
            json_loads.assert_not_called()
            context_check_repo_file_load.assert_not_called()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

        # ---- ケース3.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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
            context_check_option_parse.return_value = False
            context_check_repo_file_load.return_value = True
            context_check_synchronize.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(SystemExit):
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = stderr.getvalue().decode("utf-8")
            expected = u"起動オプションが不正です。\n"
            self.assertRegexpMatches(actual, expected)

            actual = stdout.getvalue().decode("utf-8")
            expected = u"Usage: python -m gitsynchronizer \\[-h]\\[-f ARG]\\[-d ARG]\n"
            self.assertRegexpMatches(actual, expected)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_not_called()
            context_check_repo_file_load.assert_not_called()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

        # ---- ケース4.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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
            context_check_repo_file_load.return_value = False
            context_check_synchronize.return_value = True

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(SystemExit):
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = stderr.getvalue().decode("utf-8")
            expected = u"同期対象リポジトリファイルの内容が不正です。-> .*\n"
            self.assertRegexpMatches(actual, expected)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

        # ---- ケース5.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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
            context_check_synchronize.return_value = False

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(SystemExit):
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = stderr.getvalue().decode("utf-8")
            expected = u"リポジトリの同期に失敗しました。\n"
            self.assertRegexpMatches(actual, expected)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_not_called()

        # ---- ケース6.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", os.path.join(root_dir, "log_dir")),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "log_dir"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            git_synchronizer = GitSynchronizer()
            git_synchronizer.execute()
            # noinspection PyUnresolvedReferences
            context = git_synchronizer._GitSynchronizer__context

            # 検証
            actual = os.environ.get("GITSYNCHRONIZER_PROFILE")
            expected = None
            self.assertEqual(expected, actual)

            actual = os.environ.get("LOG_DIR")
            expected = os.path.join(root_dir, "log_dir")
            self.assertEqual(expected, actual)

            actual = os.environ.get("PYTHONIOENCODING")
            expected = "utf-8"
            self.assertEqual(expected, actual)

            actual = context.root_dir
            expected = os.path.join(root_dir, "gitsynchronizer")
            self.assertEqual(expected, actual)

            actual = context.profile
            expected = "default"
            self.assertEqual(expected, actual)

            actual = context.config_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "config", "default")
            self.assertEqual(expected, actual)

            actual = context.log_dir
            expected = os.path.join(root_dir, "log_dir")
            self.assertEqual(expected, actual)

            actual = context.repo_file
            expected = os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            self.assertEqual(expected, actual)

            actual = context.dst_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo"))
            self.assertEqual(expected, actual)

            actual = context.project
            expected = "KatoRyota"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("name")
            expected = "git-synchronizer"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("base_branch")
            expected = "main"
            self.assertEqual(expected, actual)

            actual = context.project_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            self.assertEqual(expected, actual)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_called_once()

        # ---- ケース7.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), False),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(StandardError) as e:
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()
                # noinspection PyUnresolvedReferences
                context = git_synchronizer._GitSynchronizer__context

            # 検証
            actual = e.exception.message
            expected = u"環境変数[GITSYNCHRONIZER_PROFILE]が不正です。" \
                       u"GITSYNCHRONIZER_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" % \
                       (os.path.join(context.root_dir, "config"))
            self.assertEqual(expected, actual)

            makedirs.assert_not_called()
            context_check_application_initialize.assert_not_called()
            context_check_option_parse.assert_not_called()
            json_loads.assert_not_called()
            context_check_repo_file_load.assert_not_called()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

        # ---- ケース7.2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), True)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            git_synchronizer = GitSynchronizer()
            git_synchronizer.execute()
            # noinspection PyUnresolvedReferences
            context = git_synchronizer._GitSynchronizer__context

            # 検証
            actual = os.environ.get("GITSYNCHRONIZER_PROFILE")
            expected = None
            self.assertEqual(expected, actual)

            actual = os.environ.get("LOG_DIR")
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = os.environ.get("PYTHONIOENCODING")
            expected = "utf-8"
            self.assertEqual(expected, actual)

            actual = context.root_dir
            expected = os.path.join(root_dir, "gitsynchronizer")
            self.assertEqual(expected, actual)

            actual = context.profile
            expected = "default"
            self.assertEqual(expected, actual)

            actual = context.config_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "config", "default")
            self.assertEqual(expected, actual)

            actual = context.log_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = context.repo_file
            expected = os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            self.assertEqual(expected, actual)

            actual = context.dst_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo"))
            self.assertEqual(expected, actual)

            actual = context.project
            expected = "KatoRyota"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("name")
            expected = "git-synchronizer"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("base_branch")
            expected = "main"
            self.assertEqual(expected, actual)

            actual = context.project_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            self.assertEqual(expected, actual)

            makedirs.assert_not_called()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_called_once()

        # ---- ケース8.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "test"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            os.environ["GITSYNCHRONIZER_PROFILE"] = "test"
            os.environ["PYTHONIOENCODING"] = "utf-8"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            git_synchronizer = GitSynchronizer()
            git_synchronizer.execute()
            # noinspection PyUnresolvedReferences
            context = git_synchronizer._GitSynchronizer__context

            # 検証
            actual = os.environ.get("GITSYNCHRONIZER_PROFILE")
            expected = "test"
            self.assertEqual(expected, actual)

            actual = os.environ.get("LOG_DIR")
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = os.environ.get("PYTHONIOENCODING")
            expected = "utf-8"
            self.assertEqual(expected, actual)

            actual = context.root_dir
            expected = os.path.join(root_dir, "gitsynchronizer")
            self.assertEqual(expected, actual)

            actual = context.profile
            expected = "test"
            self.assertEqual(expected, actual)

            actual = context.config_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "config", "test")
            self.assertEqual(expected, actual)

            actual = context.log_dir
            expected = os.path.join(root_dir, "gitsynchronizer", "log")
            self.assertEqual(expected, actual)

            actual = context.repo_file
            expected = os.path.abspath(os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"))
            self.assertEqual(expected, actual)

            actual = context.dst_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo"))
            self.assertEqual(expected, actual)

            actual = context.project
            expected = "KatoRyota"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("name")
            expected = "git-synchronizer"
            self.assertEqual(expected, actual)

            actual = context.repositories[1].get("base_branch")
            expected = "main"
            self.assertEqual(expected, actual)

            actual = context.project_dir
            expected = os.path.abspath(os.path.join("home", "docker", "repo", "KatoRyota"))
            self.assertEqual(expected, actual)

            makedirs.assert_called_once()
            context_check_application_initialize.assert_called_once()
            context_check_option_parse.assert_called_once()
            json_loads.assert_called_once()
            context_check_repo_file_load.assert_called_once()
            synchronizer_execute.assert_called_once()
            context_check_synchronize.assert_called_once()
            printer_execute.assert_called_once()

        # ---- ケース9.1 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            if os.environ.get("PYTHONIOENCODING"):
                del os.environ["PYTHONIOENCODING"]

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(StandardError) as e:
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = e.exception.message
            expected = u"環境変数[PYTHONIOENCODING]が不正です。" \
                       u"PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            self.assertEqual(expected, actual)

            makedirs.assert_not_called()
            context_check_application_initialize.assert_not_called()
            context_check_option_parse.assert_not_called()
            json_loads.assert_not_called()
            context_check_repo_file_load.assert_not_called()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

        # ---- ケース9.2 ----
        with mock.patch("__builtin__.reload"), \
                mock.patch("__builtin__.open"), \
                mock.patch("sys.stdout", new=BytesIO()) as stdout, \
                mock.patch("sys.stderr", new=BytesIO()) as stderr, \
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

            config_parser_get.side_effect = self._config_parser_get_side_effect((
                ("logging", "log_dir", ""),))

            isdir.side_effect = self._isdir_side_effect((
                (os.path.join(root_dir, "gitsynchronizer", "config", "default"), True),
                (os.path.join(root_dir, "gitsynchronizer", "log"), False)))

            json_loads.return_value = {"KatoRyota": [
                {"name": "db-client", "base_branch": "main"},
                {"name": "git-synchronizer", "base_branch": "main"},
                {"name": "experimental-tools", "base_branch": "main"}]}

            if os.environ.get("GITSYNCHRONIZER_PROFILE"):
                del os.environ["GITSYNCHRONIZER_PROFILE"]

            os.environ["PYTHONIOENCODING"] = "euc-jp"

            sys.argv = ["git_synchronizer.py",
                        "-f", os.path.join("gitsynchronizer", "config", "default", "repo-my-project.json"),
                        "-d", os.path.join("home", "docker", "repo")]

            stdout.encoding = "utf-8"
            stderr.encoding = "utf-8"

            # 実行
            with self.assertRaises(StandardError) as e:
                git_synchronizer = GitSynchronizer()
                git_synchronizer.execute()

            # 検証
            actual = e.exception.message
            expected = u"環境変数[PYTHONIOENCODING]が不正です。" \
                       u"PYTHONIOENCODINGには、utf-8がセットされている必要があります。"
            self.assertEqual(expected, actual)

            makedirs.assert_not_called()
            context_check_application_initialize.assert_not_called()
            context_check_option_parse.assert_not_called()
            json_loads.assert_not_called()
            context_check_repo_file_load.assert_not_called()
            synchronizer_execute.assert_not_called()
            context_check_synchronize.assert_not_called()
            printer_execute.assert_not_called()

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
