FROM ubuntu:18.04

WORKDIR /root/

# ---- パッケージのインストール ----
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        tzdata \
        locales \
        less \
        python2.7 \
        git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

# ---- タイムゾーンとロケールの設定 ----
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata && \
    locale-gen ja_JP.UTF-8

ENV TZ="Asia/Tokyo" \
    LANG="ja_JP.UTF-8" \
    LANGUAGE="ja_JP:ja" \
    LC_ALL="ja_JP.UTF-8"

WORKDIR /app/

CMD ["/bin/bash"]
