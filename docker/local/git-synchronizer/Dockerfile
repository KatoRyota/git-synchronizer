FROM ubuntu:18.04

RUN \
    # ---- パッケージのインストール ----
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less \
        python2.7 \
        git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # ---- タイムゾーンとロケールの設定 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    locale-gen ja_JP.UTF-8 && \
    # ---- ユーザーとグループの追加 ----
    groupadd -r docker && \
    useradd -r -g docker docker

# ---- アプリケーションの配置 ----
USER docker

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

COPY --chown=docker:docker git-synchronizer /app/git-synchronizer
COPY --chown=docker:docker docker/local/git-synchronizer/config /app/config

# ---- アプリケーションの起動 ----
WORKDIR /app/
CMD ["/bin/bash"]
