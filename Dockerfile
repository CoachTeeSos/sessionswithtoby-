FROM debian:13.4-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV HERMES_HOME=/opt/data
ENV HERMES_WRITE_SAFE_ROOT=/opt/data
ENV PATH="/opt/hermes/.venv/bin:/opt/data/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python-is-python3 python3-venv \
    git openssh-client xz-utils ffmpeg procps nodejs npm && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.11.6-python3.13-slim /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

RUN useradd -u 10000 -m -d /opt/data hermes

WORKDIR /opt/hermes

RUN git clone https://github.com/NousResearch/hermes-agent.git /tmp/hermes-src && \
    cd /tmp/hermes-src && \
    uv venv /opt/hermes/.venv && \
    uv pip install --python /opt/hermes/.venv/bin/python -e ".[all,messaging]" && \
    rm -rf /tmp/hermes-src

COPY config.yaml /opt/data/config.yaml
COPY start.sh /opt/hermes/start.sh
RUN chmod +x /opt/hermes/start.sh

RUN mkdir -p /opt/data && chown -R hermes:hermes /opt/data

USER hermes
ENTRYPOINT ["/opt/hermes/start.sh"]
