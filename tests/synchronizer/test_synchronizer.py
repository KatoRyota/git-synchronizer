# coding: utf-8
import os
import unittest
from unittest import TestCase

import mock

from gitsynchronizer.context.context import Context
from gitsynchronizer.synchronizer.synchronizer import Synchronizer


class TestSynchronizer(TestCase):

    def test_execute(self):
        # type: () -> None

        # ---- ケース1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("os.chdir"), \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_clone"
                           ) as synchronizer__git_clone, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_diff_with_working_directory"
                           ) as synchronizer__git_diff_with_working_directory, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_stash_save"
                           ) as synchronizer__git_stash_save, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_checkout"
                           ) as synchronizer__git_checkout, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_fetch"
                           ) as synchronizer__git_fetch, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_merge"
                           ) as synchronizer__git_merge:
            # 前提条件
            synchronizer__git_clone.return_value = True
            synchronizer__git_diff_with_working_directory.return_value = True
            synchronizer__git_stash_save.return_value = True
            synchronizer__git_checkout.return_value = True
            synchronizer__git_fetch.return_value = True
            synchronizer__git_merge.return_value = True

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("dst_dir", "project")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "db-client")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "git-synchronizer")), False)
            ))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.repositories = ["db-client", "git-synchronizer"]

            # 実行
            Synchronizer(context).execute()

            # 検証
            actual = context.success_repositories
            expected = ["db-client", "git-synchronizer"]
            self.assertListEqual(expected, actual)

            makedirs.assert_called_once()

            actual = synchronizer__git_clone.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_diff_with_working_directory.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_stash_save.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_checkout.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_fetch.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_merge.call_count
            expected = 2
            self.assertEqual(expected, actual)

        # ---- ケース2.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("os.chdir"), \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_clone"
                           ) as synchronizer__git_clone, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_diff_with_working_directory"
                           ) as synchronizer__git_diff_with_working_directory, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_stash_save"
                           ) as synchronizer__git_stash_save, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_checkout"
                           ) as synchronizer__git_checkout, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_fetch"
                           ) as synchronizer__git_fetch, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_merge"
                           ) as synchronizer__git_merge:
            # 前提条件
            synchronizer__git_clone.return_value = False
            synchronizer__git_diff_with_working_directory.return_value = True
            synchronizer__git_stash_save.return_value = True
            synchronizer__git_checkout.return_value = True
            synchronizer__git_fetch.return_value = True
            synchronizer__git_merge.return_value = True

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("dst_dir", "project")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "db-client")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "git-synchronizer")), False)
            ))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.repositories = ["db-client", "git-synchronizer"]

            # 実行
            Synchronizer(context).execute()

            # 検証
            actual = context.success_repositories
            expected = []
            self.assertListEqual(expected, actual)

            makedirs.assert_called_once()

            actual = synchronizer__git_clone.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_diff_with_working_directory.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_stash_save.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_checkout.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_fetch.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_merge.call_count
            expected = 0
            self.assertEqual(expected, actual)

        # ---- ケース3.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("os.chdir"), \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_clone"
                           ) as synchronizer__git_clone, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_diff_with_working_directory"
                           ) as synchronizer__git_diff_with_working_directory, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_stash_save"
                           ) as synchronizer__git_stash_save, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_checkout"
                           ) as synchronizer__git_checkout, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_fetch"
                           ) as synchronizer__git_fetch, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_merge"
                           ) as synchronizer__git_merge:
            # 前提条件
            synchronizer__git_clone.return_value = True
            synchronizer__git_diff_with_working_directory.return_value = False
            synchronizer__git_stash_save.return_value = True
            synchronizer__git_checkout.return_value = True
            synchronizer__git_fetch.return_value = True
            synchronizer__git_merge.return_value = True

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("dst_dir", "project")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "db-client")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "git-synchronizer")), False)
            ))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.repositories = ["db-client", "git-synchronizer"]

            # 実行
            Synchronizer(context).execute()

            # 検証
            actual = context.success_repositories
            expected = ["db-client", "git-synchronizer"]
            self.assertListEqual(expected, actual)

            makedirs.assert_called_once()

            actual = synchronizer__git_clone.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_diff_with_working_directory.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_stash_save.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_checkout.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_fetch.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_merge.call_count
            expected = 2
            self.assertEqual(expected, actual)

        # ---- ケース4.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("os.chdir"), \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_clone"
                           ) as synchronizer__git_clone, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_diff_with_working_directory"
                           ) as synchronizer__git_diff_with_working_directory, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_stash_save"
                           ) as synchronizer__git_stash_save, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_checkout"
                           ) as synchronizer__git_checkout, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_fetch"
                           ) as synchronizer__git_fetch, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_merge"
                           ) as synchronizer__git_merge:
            # 前提条件
            synchronizer__git_clone.return_value = True
            synchronizer__git_diff_with_working_directory.return_value = True
            synchronizer__git_stash_save.return_value = False
            synchronizer__git_checkout.return_value = True
            synchronizer__git_fetch.return_value = True
            synchronizer__git_merge.return_value = True

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("dst_dir", "project")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "db-client")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "git-synchronizer")), False)
            ))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.repositories = ["db-client", "git-synchronizer"]

            # 実行
            Synchronizer(context).execute()

            # 検証
            actual = context.success_repositories
            expected = []
            self.assertListEqual(expected, actual)

            makedirs.assert_called_once()

            actual = synchronizer__git_clone.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_diff_with_working_directory.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_stash_save.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_checkout.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_fetch.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_merge.call_count
            expected = 0
            self.assertEqual(expected, actual)

        # ---- ケース5.1 ----
        with mock.patch("os.path.isdir") as isdir, \
                mock.patch("os.makedirs") as makedirs, \
                mock.patch("os.chdir"), \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_clone"
                           ) as synchronizer__git_clone, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_diff_with_working_directory"
                           ) as synchronizer__git_diff_with_working_directory, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_stash_save"
                           ) as synchronizer__git_stash_save, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_checkout"
                           ) as synchronizer__git_checkout, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_fetch"
                           ) as synchronizer__git_fetch, \
                mock.patch("gitsynchronizer.synchronizer.synchronizer.Synchronizer._git_merge"
                           ) as synchronizer__git_merge:
            # 前提条件
            synchronizer__git_clone.return_value = True
            synchronizer__git_diff_with_working_directory.return_value = True
            synchronizer__git_stash_save.return_value = True
            synchronizer__git_checkout.return_value = False
            synchronizer__git_fetch.return_value = True
            synchronizer__git_merge.return_value = True

            isdir.side_effect = self._isdir_side_effect((
                (os.path.abspath(os.path.join("dst_dir", "project")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "db-client")), False),
                (os.path.abspath(os.path.join("dst_dir", "project", "git-synchronizer")), False)
            ))

            context = Context()
            context.project_dir = os.path.abspath(os.path.join("dst_dir", "project"))
            context.repositories = ["db-client", "git-synchronizer"]

            # 実行
            Synchronizer(context).execute()

            # 検証
            actual = context.success_repositories
            expected = []
            self.assertListEqual(expected, actual)

            makedirs.assert_called_once()

            actual = synchronizer__git_clone.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_diff_with_working_directory.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_stash_save.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_checkout.call_count
            expected = 2
            self.assertEqual(expected, actual)

            actual = synchronizer__git_fetch.call_count
            expected = 0
            self.assertEqual(expected, actual)

            actual = synchronizer__git_merge.call_count
            expected = 0
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


if __name__ == "__main__":
    unittest.main()
