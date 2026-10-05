FROM debian:bookworm-slim

# 安裝系統基本套件、Python 3、Nginx 以及 PHP (含 cURL 擴充套件)
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    curl \
    git \
    php-cli \
    php-curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 建立獨立虛擬環境並安裝 AI 套件 (避免污染系統環境)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 安裝核心套件以及 ONNX 轉檔專用套件
RUN pip install --no-cache-dir \
    pandas \
    scikit-learn \
    flask \
    joblib \
    # ipykernel: 讓 VS Code 可以遠端連線執行程式碼
    ipykernel \
    onnx \
    skl2onnx \
    onnxruntime

WORKDIR /var/www/html

EXPOSE 80 5000

CMD ["tail", "-f", "/dev/null"]
