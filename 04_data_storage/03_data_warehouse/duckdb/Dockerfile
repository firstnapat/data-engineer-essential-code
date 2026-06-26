FROM debian:bookworm-slim

ARG DUCKDB_VERSION=1.2.2

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl unzip ca-certificates socat \
    && rm -rf /var/lib/apt/lists/*

# detect arch at build time via uname -m (aarch64 → aarch64, x86_64 → amd64)
RUN UNAME=$(uname -m) \
    && ARCH=$([ "$UNAME" = "aarch64" ] && echo "aarch64" || echo "amd64") \
    && echo "Building for arch: $UNAME → duckdb_cli-linux-${ARCH}" \
    && curl -fsSL \
        "https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-${ARCH}.zip" \
        -o /tmp/duckdb.zip \
    && unzip /tmp/duckdb.zip -d /usr/local/bin/ \
    && rm /tmp/duckdb.zip \
    && chmod +x /usr/local/bin/duckdb

WORKDIR /app
COPY init.sql entrypoint.sh ./
RUN chmod +x entrypoint.sh

VOLUME ["/data"]

# 4213 = DuckDB local UI default port
EXPOSE 4213

ENTRYPOINT ["/app/entrypoint.sh"]
