FROM python:3.10.2

RUN apt-get update

EXPOSE 8080

WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

CMD streamlit run --server.port 8080 professors_graph.py