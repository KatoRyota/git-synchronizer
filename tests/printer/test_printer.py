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
            context = self._default_context()

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

    @staticmethod
    def _default_context():
        # type: () -> Context

        context = Context()
        context.project_dir = os.path.join("dst_dir", "project")
        context.success_repositories = ["db-client", "git-synchronizer", "experimental-tools"]
        context.fail_repositories = []
        context.stash_repositories = []
        return context


if __name__ == "__main__":
    unittest.main()
