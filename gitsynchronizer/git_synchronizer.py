# coding: utf-8
import json
import locale
import logging.config
import os
import platform
import re
import signal
import sys
import traceback
from logging import Logger
from optparse import OptionParser, OptParseError
from subprocess import Popen

from context.context import Context
from printer.printer import Printer
from synchronizer.synchronizer import Synchronizer


class GitSynchronizer(object):
    __slots__ = (
        "__logger",
        "__context"
    )

    def __init__(self):
        # type: () -> None

        # ---- アプリケーションの初期化処理 ----
        super(GitSynchronizer, self).__init__()

        if not os.environ.get("PYTHONIOENCODING") or \
                not re.match(r"^utf[\-_]?8$", os.environ.get("PYTHONIOENCODING"), re.IGNORECASE):
            raise StandardError(u"環境変数[PYTHONIOENCODING]が不正です。"
                                u"PYTHONIOENCODINGには、utf-8がセットされている必要があります。")

        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.__context = Context()  # type: Context
        context = self.__context

        context.root_dir = os.path.dirname(os.path.abspath(__file__))

        context.profile = os.environ.get("GITSYNCHRONIZER_PROFILE")

        if not context.profile:
            context.profile = "default"

        context.config_dir = os.path.join(context.root_dir, "config", context.profile)

        if not os.path.isdir(context.config_dir):
            raise StandardError(u"環境変数[GITSYNCHRONIZER_PROFILE]が不正です。"
                                u"GITSYNCHRONIZER_PROFILEには、`%s`直下のディレクトリ名がセットされている必要があります。" %
                                (os.path.join(context.root_dir, "config")))

        # アプリケーション設定ファイルの読み込み
        config = context.config
        config.read(os.path.join(context.config_dir, "application.conf"))

        # ロギング設定ファイルの読み込み
        context.log_dir = config.get("logging", "log_dir")

        if not context.log_dir:
            context.log_dir = os.path.join(context.root_dir, "log")

        context.log_dir = os.path.abspath(context.log_dir)

        if not os.path.isdir(context.log_dir):
            os.makedirs(context.log_dir)

        os.environ["LOG_DIR"] = context.log_dir
        logging.config.fileConfig(os.path.join(context.config_dir, "logging.conf"))
        self.__logger = logging.getLogger(__name__)  # type: Logger

        if not context.check_application_initialize():
            raise StandardError(u"アプリケーションの初期化処理に失敗しました。")

    @staticmethod
    def main():
        # type: () -> None

        GitSynchronizer().execute()

    def execute(self):
        # type: () -> None

        logger = self.__logger
        context = self.__context
        option_parser = OptionParser()

        # noinspection PyBroadException
        try:
            logger.info("[Start] " + os.path.abspath(__file__))

            # ---- システム環境情報を出力 ----
            logger.debug("system/os name -> " + platform.system())
            logger.debug("[encoding] locale -> " + locale.getpreferredencoding())
            logger.debug("[encoding] default -> " + sys.getdefaultencoding())
            logger.debug("[encoding] filesystem -> " + sys.getfilesystemencoding())
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stdin -> " + sys.stdin.encoding)
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stdout -> " + sys.stdout.encoding)
            # noinspection PyUnresolvedReferences
            logger.debug("[encoding] stderr -> " + sys.stderr.encoding)
            logger.debug("アプリケーション設定ファイルパス -> " + os.path.join(context.config_dir, "application.conf"))
            logger.debug("ロギング設定ファイルパス -> " + os.path.join(context.config_dir, "logging.conf"))
            logger.debug("ログディレクトリ -> " + context.log_dir)

            # ---- 起動オプションのパース ----
            option_parser.set_usage("python -m gitsynchronizer [-h][-f ARG][-d ARG]")

            option_parser.add_option("-f", "--repo_file",
                                     help="Path of repository file to be synchronized. "
                                          "(e.g. config/repo-my-project.json)",
                                     metavar="ARG")

            option_parser.add_option("-d", "--dst_dir",
                                     help="Path of destination directory. "
                                          "(e.g. ~/repo/)",
                                     metavar="ARG")

            (options, args) = option_parser.parse_args()

            # ---- 起動オプションを元に、コンテキストオブジェクトを設定 ----
            # ---- repo_file ----
            if options.repo_file:
                context.repo_file = os.path.abspath(options.repo_file)

            # ---- dst_dir ----
            if options.dst_dir:
                context.dst_dir = os.path.abspath(options.dst_dir)

            # ---- 起動オプションをパースした後の、コンテキストオブジェクトの状態チェック ----
            if not context.check_option_parse():
                raise OptParseError(u"起動オプションが不正です。")

            # ---- シグナルハンドラーの設定 ----
            signal.signal(signal.SIGINT, self.terminate_subprocess)
            signal.signal(signal.SIGTERM, self.terminate_subprocess)
            if not platform.system() == "Windows":
                signal.signal(signal.SIGHUP, self.terminate_subprocess)
                signal.signal(signal.SIGQUIT, self.terminate_subprocess)

            # ---- 同期対象リポジトリファイルの読み込み ----
            with open(context.repo_file, "rb") as f:
                repo_json = f.read().decode("utf-8")

            context.loaded_repo_file = json.loads(repo_json)
            context.project = context.loaded_repo_file.keys()[0]
            context.repositories = context.loaded_repo_file.values()[0]
            context.project_dir = os.path.join(context.dst_dir, context.project)

            # ---- 同期対象リポジトリファイルを読み込んだ後の、コンテキストオブジェクトの状態チェック ----
            if not context.check_repo_file_load():
                raise StandardError(u"同期対象リポジトリファイルの内容が不正です。-> " + context.repo_file)

            # ---- gitコマンドの実行と、レポート出力 ----
            Synchronizer(context).execute()

            if not context.check_synchronize():
                raise StandardError(u"リポジトリの同期に失敗しました。")

            Printer(context).execute()

            logger.info("[End] " + os.path.abspath(__file__))

        except OptParseError:
            logger.exception(u"起動オプションが不正です。")
            traceback.print_exc()
            option_parser.print_help()
            sys.exit(1)

        except Exception:
            logger.exception(u"想定外のエラーが発生しました。")
            traceback.print_exc()
            sys.exit(1)

    def terminate_subprocess(self):
        # type: () -> None

        context = self.__context

        for popen in context.subprocesses:  # type: Popen
            if isinstance(popen, Popen):
                if popen.poll() is None:
                    popen.terminate()
