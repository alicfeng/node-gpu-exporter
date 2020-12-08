FROM python:3.6-slim
LABEL Maintainer="AlicFeng <a@samego.com>" \
      Description="monitor gpu as well as disk resource container based on python3"

ENV NVIDIA_VISIBLE_DEVICES=all \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64 \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    NVIDIA_REQUIRE_CUDA="cuda>=8.0"

COPY gpu_disk_monitor.py /app/app.py
COPY requirements.txt /app/requirements.txt
COPY sources.list /etc/apt/sources.list

RUN apt-get update \
    && apt-get install g++ python3-dev -y \
    && pip3 install -r /app/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && apt-get autoremove python3-dev  g++ -y \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/tmp/*

CMD ["python3.6", "/app/app.py"]