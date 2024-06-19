FROM python:3.12-slim
LABEL authors="tgiachi"
WORKDIR /app/server
EXPOSE 8000
RUN apt-get update && apt-get install -y make
COPY ../server /app/server
COPY ../commons /app/commons
RUN make init
CMD ["fastapi", "run"]