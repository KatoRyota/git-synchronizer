FROM ubuntu:18.04

RUN \
    # ---- パッケージのインストール ----
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less \
        python2.7 \
        git \
        curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    # ---- タイムゾーンとロケールの設定 ----
    ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    sed -i -E 's/# (ja_JP.UTF-8)/\1/' /etc/locale.gen && \
    locale-gen && \
    # ---- ユーザーとグループの追加 ----
    groupadd -g 61000 docker && \
    useradd -m -g docker -u 61000 docker && \
    # ---- pipのインストール ----
    curl https://bootstrap.pypa.io/pip/2.7/get-pip.py -o get-pip.py && \
    python2.7 get-pip.py && \
    python2.7 -m pip install --upgrade pip setuptools

# ---- アプリケーションのデプロイ ----
USER docker

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8" \
    PATH=/home/docker/.local/bin:${PATH}

COPY --chown=docker:docker . /app/git-synchronizer

WORKDIR /app/git-synchronizer

CMD ["/bin/bash"]
