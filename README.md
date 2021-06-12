# git-synchronizer

git-synchronizerは、複数のGitリポジトリを、一括で同期する為の、コマンドラインツールです。

# Requirement

* python 2.6 <= 2.7
* git

# Getting Started

以下をご確認下さい。

* [docker/local/README.md](docker/local/README.md)

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

設定ファイル(`application.conf`)に、Gitリポジトリの接続先情報を設定して下さい。  
以下を参考にして、同期対象リポジトリファイルを作成して下さい。

* [config/repo-my-project.json](config/repo-my-project.json)

ターミナルのエンコーディングに、utf-8を設定して下さい。  
ターミナルの文字フォントに、MSゴシックなどの等幅フォントを設定して下さい。  
ターミナルの環境変数[`PYTHONIOENCODING`]に、`utf-8`をセットして下さい。

以下に使い方の一例を記載します。

```shell
cd ${APP_ROOT_DIR}

python2.7 -m git-synchronizer -f config/repo-my-project.json -d ~/repo/
```

指定可能なオプションは、以下のコマンドでご確認下さい。

```shell
python2.7 -m git-synchronizer -h
```
