# Build stage
FROM --platform=linux/amd64 ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    clang \
    libspdlog-dev \
    && rm -rf /var/lib/apt/lists/*

# Install CMake 3.28
RUN wget -q https://github.com/Kitware/CMake/releases/download/v3.28.1/cmake-3.28.1-linux-x86_64.sh -O /tmp/cmake.sh && \
    chmod +x /tmp/cmake.sh && \
    /tmp/cmake.sh --skip-license --prefix=/usr/local && \
    rm /tmp/cmake.sh

WORKDIR /app

COPY metal-inference-core/ ./
RUN rm -rf build && mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc)

# Runtime stage
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    libspdlog1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/build/bin/inference_cli /usr/local/bin/
COPY --from=builder /app/build/bin/libinference_core.a /usr/local/lib/
COPY --from=builder /app/build/bin/libinference_metal.a /usr/local/lib/

ENV MTL_ENABLE_STATS=0

ENTRYPOINT ["inference_cli"]
