FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

ARG GOOGLE_API_KEY
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}

COPY ./requirements.txt /app/requirements.txt
COPY ./main.py /app/main.py

EXPOSE 8000

RUN apt-get update && apt-get install -y python3-pip && \
    pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118 && \
    pip install -r requirements.txt

CMD ["python3", "main.py", "--host", "0.0.0.0", "--port", "8000"]
