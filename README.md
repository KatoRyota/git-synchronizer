# git-synchronizer

git-synchronizerは、複数のGitリポジトリを、一括で同期する為の、コマンドラインツールです。

以下は実行結果の一例です。

```text
docker@git-synchronizer:/app/git-synchronizer$ python2.7 -m gitsynchronizer -f gitsynchronizer/config/default/repo-my-project.json -d ~/repo/
[db-client                        ] Succeeded synchronization. - - - 1/3
[git-synchronizer                 ] Succeeded synchronization. - - - 2/3
[experimental-tools               ] Succeeded synchronization. - - - 3/3
-------------------------------------------------------------------------------
【結果レポート】

全てのリポジトリの同期に成功しました。
以下のディレクトリ配下のリポジトリの同期を行いました。
/home/docker/repo/KatoRyota

--- ワーキングディレクトリの内容を、Git Stashに保存したリポジトリ ---
　　・なし

--- 同期に失敗したリポジトリ ---
　　・なし

--- 同期に成功したリポジトリ ---
　　・db-client
　　・git-synchronizer
　　・experimental-tools
```

# Requirement

* python 2.6 <= 2.7
* git

# Getting Started

以下をご確認下さい。

* [README.md](docker/local/README.md)

# Installation

実行環境のターミナルで、ノンパスワードで`git clone`できることを確認して下さい。  
できない場合は、ノンパスワードで`git clone`できるように設定を行って下さい。  
git-synchronizer内部で、`git clone`コマンドを実行する為です。

以下のようにgit-synchronizerをダウンロードして下さい。

```shell
cd ~/repo/
git clone https://github.com/KatoRyota/git-synchronizer.git
```

以上です。

# Usage

プロファイル毎 (`gitsynchronizer/config/${PROFILE}/`) の設定ファイル (`application.conf`) に、  
Gitリポジトリの接続先情報 (`repository`セクション) を記載して下さい。  
設定ファイルは、デフォルトで`gitsynchronizer/config/default/`ディレクトリ配下のものを読み込みます。  
プロファイルは、`gitsynchronizer/config/`ディレクトリ直下に、任意の名前を付けて、追加することが可能です。  
プロファイルは、環境変数[`GITSYNCHRONIZER_PROFILE`]に、  
`gitsynchronizer/config/`ディレクトリ直下の、ディレクトリ名をセットすることで変更可能です。

以下を参考にして、同期対象リポジトリファイルを作成して下さい。

* [repo-my-project.json](gitsynchronizer/config/default/repo-my-project.json)

ターミナルのエンコーディングに、utf-8を設定して下さい。  
ターミナルの文字フォントに、MSゴシックなどの等幅フォントを設定して下さい。  
ターミナルの環境変数[`PYTHONIOENCODING`]に、`utf-8`をセットして下さい。

以下に使い方の一例を記載します。

```shell
cd ${APP_ROOT_DIR}

python -m gitsynchronizer -f gitsynchronizer/config/default/repo-my-project.json -d ~/repo/
```

上記コマンドがエラーになる場合は、以下を試してみて下さい。

```shell
cd ${APP_ROOT_DIR}

python -m gitsynchronizer.__main__ -f gitsynchronizer/config/default/repo-my-project.json -d ~/repo/
```

指定可能なオプションは、以下のコマンドでご確認下さい。

```shell
python -m gitsynchronizer -h
```
