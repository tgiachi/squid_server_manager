FROM python:3.12-slim
LABEL authors="tgiachi"
WORKDIR /app/server
RUN apt-get update && apt-get install -y make
COPY ../server /app/server
COPY ../commons /app/server/commons
RUN make init
CMD ["fastapi", "run"]