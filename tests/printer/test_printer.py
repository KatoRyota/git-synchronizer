# coding: utf-8
import os.path
import unittest
from io import BytesIO
from unittest import TestCase

import mock

from gitsynchronizer.context.context import Context
from gitsynchronizer.printer.printer import Printer


class TestPrinter(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.success_repositories = ["db-client", "git-synchronizer", "experimental-tools"]
            context.fail_repositories = []
            context.stash_repositories = []

            # 実行
            Printer(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
-------------------------------------------------------------------------------
【結果レポート】

全てのリポジトリの同期に成功しました。
以下のディレクトリ配下のリポジトリの同期を行いました。
.*dst_dir.project

--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---
　　・なし

--- 同期に失敗したリポジトリ ---
　　・なし

--- 同期に成功したリポジトリ ---
　　・db-client
　　・git-synchronizer
　　・experimental-tools

'''
            self.assertRegexpMatches(actual, expected)

        # ---- ケース2.1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.success_repositories = []
            context.fail_repositories = ["db-client", "git-synchronizer", "experimental-tools"]
            context.stash_repositories = []

            # 実行
            Printer(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
-------------------------------------------------------------------------------
【結果レポート】

同期に失敗したリポジトリがあります。
以下のディレクトリ配下のリポジトリの同期を行いました。
.*dst_dir.project

--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---
　　・なし

--- 同期に失敗したリポジトリ ---
　　・db-client
　　・git-synchronizer
　　・experimental-tools

--- 同期に成功したリポジトリ ---
　　・なし

'''
            self.assertRegexpMatches(actual, expected)

        # ---- ケース3.1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = ["experimental-tools"]
            context.stash_repositories = []

            # 実行
            Printer(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
-------------------------------------------------------------------------------
【結果レポート】

同期に失敗したリポジトリがあります。
以下のディレクトリ配下のリポジトリの同期を行いました。
.*dst_dir.project

--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---
　　・なし

--- 同期に失敗したリポジトリ ---
　　・experimental-tools

--- 同期に成功したリポジトリ ---
　　・db-client
　　・git-synchronizer

'''
            self.assertRegexpMatches(actual, expected)

        # ---- ケース4.1 ----
        with mock.patch("sys.stdout", new=BytesIO()) as stdout:
            # 前提条件
            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.success_repositories = ["db-client", "git-synchronizer"]
            context.fail_repositories = ["experimental-tools"]
            context.stash_repositories = ["db-client", "git-synchronizer"]

            # 実行
            Printer(context).execute()

            # 検証
            actual = stdout.getvalue().decode("utf-8")
            expected = u'''\
-------------------------------------------------------------------------------
【結果レポート】

同期に失敗したリポジトリがあります。
以下のディレクトリ配下のリポジトリの同期を行いました。
.*dst_dir.project

--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---
　　・db-client
　　・git-synchronizer

--- 同期に失敗したリポジトリ ---
　　・experimental-tools

--- 同期に成功したリポジトリ ---
　　・db-client
　　・git-synchronizer

'''
            self.assertRegexpMatches(actual, expected)


if __name__ == "__main__":
    unittest.main()
