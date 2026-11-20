FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DISPLAY=:99 \
    DB_PATH=/app/data/orders.db

# Python + Tk + виртуальный X-сервер + VNC + веб-клиент noVNC
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-tk \
        tk \
        xvfb \
        x11vnc \
        novnc \
        websockify \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

COPY . .
RUN mkdir -p /app/data

EXPOSE 6080

CMD ["bash", "-lc", "\
    Xvfb :99 -screen 0 1200x900x24 >/tmp/xvfb.log 2>&1 & \
    sleep 2 && \
    x11vnc -display :99 -nopw -forever -shared -rfbport 5900 -bg -o /tmp/x11vnc.log && \
    websockify --web=/usr/share/novnc/ 6080 localhost:5900 >/tmp/novnc.log 2>&1 & \
    exec python3 main.py"]