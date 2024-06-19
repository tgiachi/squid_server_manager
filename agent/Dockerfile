FROM python:3.12-slim
LABEL authors="tgiachi"
WORKDIR /app/agent
RUN dpkg --add-architecture i386
RUN apt-get update -y && apt install wget lib32gcc-s1 lib32stdc++6 make \
curl libstdc++6:i386 lib32z1 -y
COPY ../agent /app/agent
COPY ../commons /app/agent/commons
RUN make init

CMD ["python", "main.py"]