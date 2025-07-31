FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3.10 \
    python3-pip \
    python3.10-venv \
    git \
    curl \
    wget \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Python dependencies
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# Install additional dependencies added during TTS development
# These are commented out for now but can be uncommented when needed

# Python packages we installed during development
# RUN pip3 install --no-cache-dir \
#     # Performance optimization for TTS models
#     accelerate>=0.26.0 \
#     # Flash attention for performance (optional)
#     flash-attn

# System packages we installed during development
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends \
#     ffmpeg \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /workspace

# Switch to non-root user
USER $USERNAME 