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
from ConfigParser import SafeConfigParser
from optparse import OptionParser, OptParseError
from subprocess import Popen

from context.context import Context
from printer.printer import Printer
from synchronizer.synchronizer import Synchronizer

reload(sys)
sys.setdefaultencoding("utf-8")

config = SafeConfigParser()
config.read("config/application.conf")

if not os.path.isdir("./log"):
    os.makedirs("./log")

logging.config.fileConfig("config/logging.conf")
logger = logging.getLogger(__name__)

option_parser = OptionParser()
context = Context()


def terminate_subprocess():
    # type: () -> None

    for popen in context.subprocesses:  # type: Popen
        if isinstance(popen, Popen):
            if popen.poll() is None:
                popen.terminate()


# noinspection PyBroadException
try:
    logger.info("[Start] " + os.path.abspath(__file__))

    # ---- 環境変数[PYTHONIOENCODING]のチェック ----
    if os.getenv("PYTHONIOENCODING"):
        if not re.match(r"^utf[\-_]?8$", os.getenv("PYTHONIOENCODING"), re.IGNORECASE):
            raise StandardError(u"環境変数[PYTHONIOENCODING]が不正です。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")
    else:
        raise StandardError(u"環境変数[PYTHONIOENCODING]がセットされていません。PYTHONIOENCODINGには、utf-8がセットされている必要があります。")

    # ---- システム環境情報を出力 ----
    logger.debug("system/os name -> " + platform.system())
    logger.debug("[encoding] locale -> " + locale.getpreferredencoding())
    logger.debug("[encoding] default -> " + sys.getdefaultencoding())
    logger.debug("[encoding] filesystem -> " + sys.getfilesystemencoding())
    logger.debug("[encoding] stdin -> " + sys.stdin.encoding)
    logger.debug("[encoding] stdout -> " + sys.stdout.encoding)
    logger.debug("[encoding] stderr -> " + sys.stderr.encoding)

    # ---- 起動オプションのパース ----
    option_parser.set_usage("python2.7 -m git-synchronizer [-h][-f ARG][-d ARG]")

    option_parser.add_option("-f", "--repo_file",
                             help="Path of repository file to be synchronized. (e.g. config/repo-my-project.json)",
                             metavar="ARG")
    option_parser.add_option("-d", "--dst_dir", help="Path of destination directory. (e.g. ~/repo/)",
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
    if not context.check_state_after_parse_option():
        raise OptParseError(u"起動オプションが不正です。")

    # ---- シグナルハンドラーの設定 ----
    signal.signal(signal.SIGINT, terminate_subprocess)
    signal.signal(signal.SIGTERM, terminate_subprocess)
    if not platform.system() == "Windows":
        signal.signal(signal.SIGHUP, terminate_subprocess)
        signal.signal(signal.SIGQUIT, terminate_subprocess)

    # ---- 同期対象リポジトリファイルの読み込みと、妥当性チェック ----
    with open(context.repo_file, "rb") as f:
        repo_json = f.read().decode("utf-8")

    sync_repositories = json.loads(repo_json)

    if len(sync_repositories.keys()) > 1:
        raise StandardError(u"同期対象リポジトリファイルの内容が不正です。-> " + context.repo_file)

    # ---- 同期対象リポジトリファイルを元に、コンテキストオブジェクトを設定 ----
    context.project = sync_repositories.keys()[0]
    context.repositories = sync_repositories.values()[0]
    context.project_dir = os.path.abspath(os.path.join(context.dst_dir, context.project))

    # ---- 同期対象リポジトリファイルを読み込んだ後の、コンテキストオブジェクトの状態チェック ----
    if not context.check_state_after_load_repo_file():
        raise StandardError(u"同期対象リポジトリファイルの内容が不正です。-> " + context.repo_file)

    # ---- gitコマンドの実行と、レポート出力 ----
    Synchronizer(config, context).execute()

    if not context.check_state_after_synchronize():
        raise StandardError(u"リポジトリの同期に失敗しました。")

    Printer(context).execute()

    logger.info("[End] " + os.path.abspath(__file__))

except OptParseError as e:
    logger.exception(u"起動オプションが不正です。")
    traceback.print_exc()
    option_parser.print_help()
    sys.exit(1)

except Exception as e:
    logger.exception(u"想定外のエラーが発生しました。")
    traceback.print_exc()
    sys.exit(1)
