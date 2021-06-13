# Dockerによるローカル環境構築手順

## 概要

本ドキュメントはDockerを利用して、git-synchronizerのローカル環境を構築する為の手順です。

## 前提

本ドキュメントは以下の環境における構築手順です。  
しかし、他の環境でも同様の手順で、構築できるはずです。

* Windows 10
* WSL 2 (Ubuntu 20.04 LTS)
* Docker Desktop 3

WSL 2 (Ubuntu 20.04 LTS) には、以下のソフトウェアがインストールされてる必要があります。

* Git

## git-synchronizerをダウンロード

```shell
# [Ubuntu]
cd ~/repo/
git clone https://github.com/KatoRyota/git-synchronizer.git
```

## Dockerコンテナの作成/起動

```shell
# [Ubuntu]
cd ~/repo/git-synchronizer/docker/local/
docker-compose up --build -d
docker-compose logs -f
```

## 動作確認

```shell
# [Ubuntu]
docker container exec -it git-synchronizer /bin/bash

export PYTHONIOENCODING=utf-8
cd /app/
mkdir -vp ~/repo

python2.7 -m git-synchronizer -f config/repo-my-project.json -d ~/repo/

exit
```

## Dockerコンテナの停止/削除

```shell
# [Ubuntu]
cd ~/repo/git-synchronizer/docker/local/
docker-compose down
```

# Tips

## Dockerコンテナを一括で作成/起動したい

```shell
# [Ubuntu]
cd ${DOCKER_COMPOSE_YML_DIR}
docker-compose up --build -d
docker-compose logs -f
```

## Dockerコンテナを一括で停止/削除したい

```shell
# [Ubuntu]
cd ${DOCKER_COMPOSE_YML_DIR}
docker-compose down
```

## Dockerリソースを一括で削除したい

```shell
# [Ubuntu]
docker container stop `docker ps -q`
docker system prune -a --volumes
```

## Dockerコンテナの一覧を確認したい

```shell
# [Ubuntu]
docker container ls -a
```

## Dockerイメージの一覧を確認したい

```shell
# [Ubuntu]
docker image ls -a
```

## Dockerネットワークの一覧を確認したい

```shell
# [Ubuntu]
docker network ls
```

## Dockerボリュームの一覧を確認したい

```shell
# [Ubuntu]
docker volume ls
```

## Dockerコンテナでインタラクティブシェルを起動したい

```shell
# [Ubuntu]
docker container exec -it ${CONTAINER_NAME} /bin/bash
```

## Dockerコンテナのログを確認したい

```shell
# [Ubuntu]
docker container logs -f ${CONTAINER_NAME}
```

## Dockerコンテナの詳細を確認したい

```shell
# [Ubuntu]
docker container inspect ${CONTAINER_NAME}
```

## Dockerfileを作成したい

### for ubuntu

```shell
# [Ubuntu]
docker container run --dns=8.8.8.8 --rm \
    --name=ubuntu18-04 --hostname=ubuntu18-04 \
    -itd ubuntu:18.04

# コンテナに入って、手動で環境構築（インストールなど）を行っていき、その手順をDockerfileに記載する。
docker container exec -it ubuntu18-04 /bin/bash
```

### for centos

```shell
# [Ubuntu]
docker container run --dns=8.8.8.8 --rm \
    --name=centos7 --hostname=centos7 \
    -itd centos:7 /sbin/init
  
# コンテナに入って、手動で環境構築（インストールなど）を行っていき、その手順をDockerfileに記載する。
docker container exec -it centos7 /bin/bash
```

## Dockerfileからイメージをビルドして起動したい

```shell
# [Ubuntu]
cd ${DOCKERFILE_DIR}
docker image build -t ${IMAGE_NAME}:${VERSION} .
docker container run --dns=8.8.8.8 --rm \
    --name=${CONTAINER_NAME} --hostname=${HOST_NAME} \
    -itd ${IMAGE_NAME}:${VERSION}

docker container exec -it ${CONTAINER_NAME} /bin/bash
```
