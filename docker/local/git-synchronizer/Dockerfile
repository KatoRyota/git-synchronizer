FROM ubuntu:18.04

WORKDIR /root/

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
    groupadd -g 61000 docker && \
    useradd  -m -g docker -u 61000 docker

USER docker
WORKDIR /home/docker/

# ---- ディレクトリの作成 ----
RUN mkdir -vp /app/log && \
    chown -R docker:docker /app/log

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

CMD ["/bin/bash"]
