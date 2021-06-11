# coding: utf-8
import logging
import os
from logging import Logger

from ..context.context import Context


class Printer(object):
    __slots__ = (
        "__logger",
        "__context"
    )

    def __init__(self, context):
        # type: (Context) -> None

        super(Printer, self).__init__()
        self.__logger = logging.getLogger(__name__)  # type: Logger
        self.__context = context  # type: Context

    def execute(self):
        # type: () -> None

        message = ""
        message += "-------------------------------------------------------------------------------\n"
        message += u"【結果レポート】\n"
        message += "\n"

        if not self.__context.fail_repositories:
            message += u"全てのリポジトリの同期に成功しました。\n"
        else:
            message += u"同期に失敗したリポジトリがあります。\n"

        message += u"以下のディレクトリ配下のリポジトリの同期を行いました。\n"
        message += os.path.abspath(self.__context.project_dir) + "\n"
        message += "\n"

        message += u"--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---\n"

        if not self.__context.stash_repositories:
            message += u"　　・なし\n"
        else:
            for stash_repository in self.__context.stash_repositories:  # type: str
                message += u"　　・" + stash_repository + "\n"

        message += "\n"

        message += u"--- 同期に失敗したリポジトリ ---\n"

        if not self.__context.fail_repositories:
            message += u"　　・なし\n"
        else:
            for fail_repository in self.__context.fail_repositories:  # type: str
                message += u"　　・" + fail_repository + "\n"

        message += "\n"

        message += u"--- 同期に成功したリポジトリ ---\n"

        if not self.__context.success_repositories:
            message += u"　　・なし\n"
        else:
            for success_repository in self.__context.success_repositories:  # type: str
                message += u"　　・" + success_repository + "\n"

        print message.encode("utf-8")
