FROM python:3.10-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    PYTRACKER_DOCKER_DIRECT_MOUSE=1 \
    PYTRACKER_DOCKER_MOUSE_HZ=50 \
    LIBGL_ALWAYS_SOFTWARE=1 \
    QT_X11_NO_MITSHM=1 \
    HOME=/tmp \
    XDG_CACHE_HOME=/tmp/.cache \
    MPLCONFIGDIR=/tmp/.matplotlib

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential ca-certificates curl git pkg-config \
      xvfb xauth x11vnc x11-utils openbox novnc websockify netcat-openbsd \
      libgl1 libgl1-mesa-dri libglu1-mesa libglib2.0-0 libgtk-3-0 \
      libx11-6 libxext6 libxi6 libxrender1 libxfixes3 libsm6 libxrandr2 \
      libxxf86vm1 libxkbcommon0 libxkbcommon-x11-0 libxcb-xinerama0 \
      libxcb-cursor0 libdbus-1-3 libnss3 \
      libasound2 libpulse0 portaudio19-dev libsndfile1 ffmpeg \
      fonts-dejavu-core fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
ARG UPSTREAM_REPO=https://github.com/sbobek/tobii-pytracker.git
ARG UPSTREAM_REF=main
RUN git clone "${UPSTREAM_REPO}" /workspace/tobii-pytracker \
    && git -C /workspace/tobii-pytracker checkout "${UPSTREAM_REF}" \
    && test -z "$(git -C /workspace/tobii-pytracker status --porcelain --untracked-files=no)"

COPY docker/requirements-docker.txt /opt/pytracker-docker/requirements-docker.txt
RUN python -m pip install --upgrade 'pip==24.3.1' 'wheel==0.43.0' \
    && python -m pip install --no-cache-dir -r /opt/pytracker-docker/requirements-docker.txt \
    && python -m pip install --no-cache-dir --no-deps /workspace/tobii-pytracker \
    && python -m pip install --no-cache-dir --no-deps 'psychopy==2024.1.4'

COPY docker/patch_installed_mouse_backend.py /opt/pytracker-docker/patch_installed_mouse_backend.py
COPY docker/validate_runtime.py /opt/pytracker-docker/validate_runtime.py
COPY docker/entrypoint.sh /opt/pytracker-docker/entrypoint.sh
RUN chmod +x /opt/pytracker-docker/entrypoint.sh \
    && python /opt/pytracker-docker/patch_installed_mouse_backend.py \
    && python -m py_compile /opt/pytracker-docker/patch_installed_mouse_backend.py /opt/pytracker-docker/validate_runtime.py \
    && python -c "import ctypes, psychopy, zmq, tables, Xlib, distro; ctypes.CDLL('libXfixes.so.3'); assert psychopy.__version__ == '2024.1.4'; print('Docker build dependency smoke: OK')" \
    && git -C /workspace/tobii-pytracker diff --exit-code -- . \
    && test -z "$(git -C /workspace/tobii-pytracker status --porcelain --untracked-files=no)"

WORKDIR /workspace/tobii-pytracker
EXPOSE 6080 8888
ENTRYPOINT ["/opt/pytracker-docker/entrypoint.sh"]
