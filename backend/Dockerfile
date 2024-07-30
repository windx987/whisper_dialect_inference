FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y python3-pip && \
    pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118 && \
    pip install -r requirements.txt

COPY ./app /code/app
CMD ["unvicorn", "main:app", "--reload"]